"""XPROTO-PG shakedown: consumer-relative staleness certificates for
Postgres streaming replication. NO evidential weight -- construction +
shakedown for a future sealed cell (the first non-routing cell of the
vacuity taxonomy).

The question, D8-shaped: when the standard replication monitor says
"caught up", how often is a CONSUMER-relevant read on the replica
actually stale -- and does a witness-based, footprint-aware certificate
do better in both directions?

Substrate (lab containers, set up by the caller):
  primary  (wal_level=logical)  -- beacon writes at known times
  replica  (recovery_min_apply_delay=1000ms) -- genuine staleness window

Actors per sample tick (~5 Hz):
  naive monitor    now() - pg_last_xact_replay_timestamp() on the
                   replica -- the query every runbook uses -- CLEAR iff
                   lag < T for each threshold T. Known pathology carried
                   honestly: on an idle primary the replay timestamp
                   stops advancing, so the metric grows while the
                   replica is perfectly current (false-ALARM regime).
  witness          logical-decoding slot on the primary; per-table max
                   change LSN. Consumer-aware certificate: CLEAR for
                   consumer i iff last_change_lsn(footprint_i) <=
                   replica replay LSN. (P_i = the consumer's table
                   footprint; this is tr(P_i . drift) == 0.)
  ground truth     the beacon schedule: writer records (table, seq,
                   commit time); consumer i is TRULY stale at t iff a
                   row in its footprint committed >= GUARD before t is
                   not yet visible on the replica.

Consumers: A reads hot_a only (bursty churn: 5 writes/s in alternating
20 s phases); B reads hot_b only (sparse: one write / 8 s). A global
lag metric cannot serve both -- that asymmetry is the consumer-
relativity claim, measured.

    python3 pgrep_shakedown.py --duration 120
"""

from __future__ import annotations

import argparse
import json
import threading
import time

import psycopg

PRIMARY = "postgresql://postgres:lab@127.0.0.1:55433/postgres"
REPLICA = "postgresql://postgres:lab@127.0.0.1:55434/postgres"
THRESHOLDS = [0.1, 0.5, 1.0, 2.0, 5.0]
GUARD = 0.20            # truth guard: a write must be this old to count
TICK = 0.2
SLOT = "ngpg_witness"


def lsn_int(s: str) -> int:
    hi, lo = s.split("/")
    return (int(hi, 16) << 32) | int(lo, 16)


class Writer(threading.Thread):
    """Beacon writer: known writes at known times, commit times recorded."""

    def __init__(self, duration: float):
        super().__init__(daemon=True)
        self.duration = duration
        self.log: dict[str, list[tuple[int, float]]] = {"hot_a": [],
                                                        "hot_b": []}
        self.seq = {"hot_a": 0, "hot_b": 0}
        self._lock = threading.Lock()

    def write(self, conn, table: str):
        self.seq[table] += 1
        s = self.seq[table]
        conn.execute(f"INSERT INTO {table} (seq, t) VALUES (%s, %s)",
                     (s, time.time()))
        with self._lock:
            self.log[table].append((s, time.time()))   # post-commit stamp

    def latest_committed(self, table: str, before: float) -> int:
        with self._lock:
            best = 0
            for s, t in self.log[table]:
                if t <= before and s > best:
                    best = s
            return best

    def run(self):
        conn = psycopg.connect(PRIMARY, autocommit=True)
        t0 = time.time()
        next_b = t0
        while True:
            now = time.time()
            el = now - t0
            if el >= self.duration:
                break
            busy = int(el // 20) % 2 == 0        # 20 s busy/quiet phases
            if busy:
                self.write(conn, "hot_a")
            if now >= next_b:
                self.write(conn, "hot_b")
                next_b = now + 8.0
            time.sleep(0.2)
        conn.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=120.0)
    ap.add_argument("--out", default="PGREP-shakedown.json")
    args = ap.parse_args()

    prim = psycopg.connect(PRIMARY, autocommit=True)
    prim.execute("DROP TABLE IF EXISTS hot_a, hot_b")
    prim.execute("CREATE TABLE hot_a (seq bigint, t float8)")
    prim.execute("CREATE TABLE hot_b (seq bigint, t float8)")
    prim.execute("SELECT pg_drop_replication_slot(%s) FROM "
                 "pg_replication_slots WHERE slot_name = %s", (SLOT, SLOT))
    prim.execute("SELECT pg_create_logical_replication_slot(%s, "
                 "'test_decoding')", (SLOT,))
    wit = psycopg.connect(PRIMARY, autocommit=True)
    repl = psycopg.connect(REPLICA, autocommit=True)
    # wait for the replica to have the tables (basebackup + stream)
    for _ in range(60):
        try:
            repl.execute("SELECT 1 FROM hot_a LIMIT 1")
            break
        except psycopg.errors.UndefinedTable:
            time.sleep(1.0)
    print("lab ready; starting writer + sampler", flush=True)

    writer = Writer(args.duration)
    writer.start()

    last_change: dict[str, int] = {"hot_a": 0, "hot_b": 0}
    samples = []
    t0 = time.time()
    while time.time() - t0 < args.duration:
        tick_t = time.time()
        # witness: consume decoding stream, track per-table max LSN
        for lsn, _xid, data in wit.execute(
                "SELECT lsn, xid, data FROM "
                "pg_logical_slot_get_changes(%s, NULL, NULL)", (SLOT,)):
            for tbl in ("hot_a", "hot_b"):
                if f"table public.{tbl}:" in data:
                    v = lsn_int(str(lsn))
                    if v > last_change[tbl]:
                        last_change[tbl] = v
        # replica state, one round trip
        row = repl.execute(
            "SELECT COALESCE(EXTRACT(EPOCH FROM "
            "  now() - pg_last_xact_replay_timestamp()), 1e9)::float8, "
            "pg_last_wal_replay_lsn()::text, "
            "(SELECT COALESCE(max(seq),0) FROM hot_a), "
            "(SELECT COALESCE(max(seq),0) FROM hot_b)").fetchone()
        naive_lag, replay_lsn, vis_a, vis_b = (
            float(row[0]), lsn_int(row[1]), int(row[2]), int(row[3]))
        truth_stale = {
            "A": vis_a < writer.latest_committed("hot_a", tick_t - GUARD),
            "B": vis_b < writer.latest_committed("hot_b", tick_t - GUARD)}
        aware_clear = {
            "A": last_change["hot_a"] <= replay_lsn,
            "B": last_change["hot_b"] <= replay_lsn}
        samples.append({
            "t": round(tick_t - t0, 2),
            "busy": int((tick_t - t0) // 20) % 2 == 0,
            "naive_lag_s": round(naive_lag, 3),
            "truth_stale": truth_stale,
            "aware_clear": aware_clear})
        time.sleep(max(0.0, TICK - (time.time() - tick_t)))
    writer.join()

    # -- aggregate ------------------------------------------------------
    def rate(pred) -> tuple[float, int]:
        hits = [s for s in samples if pred(s)]
        return (round(len(hits) / len(samples), 4), len(hits))

    report = {"cell": "XPROTO-PG", "sealed": False, "shakedown": True,
              "n_samples": len(samples),
              "duration_s": args.duration,
              "apply_delay_ms": 1000,
              "writes": {t: len(writer.log[t]) for t in writer.log},
              "naive": {}, "aware": {}}
    for T in THRESHOLDS:
        e = {}
        for c in ("A", "B"):
            fc, nfc = rate(lambda s, c=c, T=T:
                           s["naive_lag_s"] < T and s["truth_stale"][c])
            fa, nfa = rate(lambda s, c=c, T=T:
                           s["naive_lag_s"] >= T and not s["truth_stale"][c])
            e[c] = {"false_clear": fc, "n_false_clear": nfc,
                    "false_alarm": fa, "n_false_alarm": nfa}
        report["naive"][f"{T}s"] = e
    for c in ("A", "B"):
        fc, nfc = rate(lambda s, c=c:
                       s["aware_clear"][c] and s["truth_stale"][c])
        fa, nfa = rate(lambda s, c=c:
                       not s["aware_clear"][c] and not s["truth_stale"][c])
        stale_frac, _ = rate(lambda s, c=c: s["truth_stale"][c])
        report["aware"][c] = {"false_clear": fc, "n_false_clear": nfc,
                              "false_alarm": fa, "n_false_alarm": nfa,
                              "truth_stale_frac": stale_frac}
    report["samples_head"] = samples[:25]

    json.dump(report, open(args.out, "w"), indent=1)
    print(json.dumps({k: report[k] for k in
                      ("n_samples", "writes", "naive", "aware")}, indent=1))
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
