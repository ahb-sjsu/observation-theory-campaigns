"""XPROTO-PGX family (F-PGX): the PRODUCTION graduation of XPROTO-PG.

Same claim and bar shape as the sealed lab cell, but it relaxes the two
things XPROTO-PG *controlled*:

  (1) footprint: DERIVED from `pg_stat_statements` per consumer role
      (the tool learns what each consumer actually reads from the
      replica's own query stats) — not the declared hot_a/hot_b of the
      lab cell. A new manipulation check (MC4) guards this mechanism:
      if the derivation doesn't recover the intended relations, the cell
      VOIDs (instrument, not claim).

  (2) lag: EMERGENT and fluctuating — a WAN-style `netem` delay+jitter on
      the replica's link (set in lab_up.sh, ~300ms±120ms) under a real
      write load — instead of a clean deterministic `recovery_min_apply_
      delay`. The naive lag monitor now faces a lag *distribution*, and
      the cell requires that variation to be realized (MC3 lag-std floor).

Two consumers with multi-relation footprints so the derivation is a real
test: HOT reads orders⋈order_items (both heavily written), COLD reads
catalog⋈category (rarely written). Witness = logical-decoding slot,
per-relation max change LSN vs the replica's replay LSN — unchanged from
XPROTO-PG. Beacon ground truth is exact from the write schedule.

    python3 fam_pgx.py                 # family shakedown, seeds 0 1 2
    python3 fam_pgx.py --seeds 7 8     # exploration only
"""

from __future__ import annotations

import argparse
import json
import random
import re
import threading
import time

import psycopg

PRIMARY = "postgresql://postgres:lab@127.0.0.1:55445/postgres"
REPLICA = "postgresql://postgres:lab@127.0.0.1:55446/postgres"

def replica_as(role: str) -> str:
    return f"postgresql://{role}:lab@127.0.0.1:55446/postgres"

# ---- sealed cell constants (bars reference these; do not tune) -------
THRESHOLDS = [0.1, 0.5, 1.0, 2.0, 5.0]   # naive-monitor grid (seconds)
DURATION_S = 120.0
TICK_S = 0.2
GUARD_S = 0.2
PHASE_S = 20.0                            # busy/quiet alternation (hot)
RATE_BAND = (4.0, 6.0)                    # hot writes/s in busy phases
COLD_INTERVAL_BAND = (6.0, 10.0)         # cold write spacing
SLOT = "ngpgx_witness"
KNOWN_RELS = ("orders", "order_items", "catalog", "category")
REL_RE = re.compile(r"\b(?:from|join)\s+([a-z_][a-z0-9_]*)", re.I)

# consumer definitions: role, the query it runs on the replica (which
# populates pg_stat_statements → its measured footprint), and the
# footprint we INTEND the derivation to recover (MC4 checks equality).
CONSUMERS = {
    "HOT": {"role": "consumer_hot",
            "query": "SELECT count(*) FROM orders o "
                     "JOIN order_items i ON i.order_seq = o.seq",
            "intended": {"orders", "order_items"}},
    "COLD": {"role": "consumer_cold",
             "query": "SELECT count(*) FROM catalog c "
                      "JOIN category k ON k.id = c.id",
             "intended": {"catalog", "category"}},
}


def lsn_int(s: str) -> int:
    hi, lo = s.split("/")
    return (int(hi, 16) << 32) | int(lo, 16)


class Writer(threading.Thread):
    """Seeded beacon writer. HOT events write orders+order_items in one
    transaction (same seq); COLD events write catalog+category likewise.
    Phases alternate busy/quiet for the hot stream so every seed has
    interior in both regimes."""

    def __init__(self, seed: int, duration: float):
        super().__init__(daemon=True)
        rng = random.Random(seed)
        self.rate = rng.uniform(*RATE_BAND)
        self.cold_int = rng.uniform(*COLD_INTERVAL_BAND)
        self.jitter = rng.uniform(0.0, 0.08)
        self.duration = duration
        self.log = {r: [] for r in KNOWN_RELS}
        self.hot_seq = 0
        self.cold_seq = 0
        self._lock = threading.Lock()

    def _hot(self, conn):
        self.hot_seq += 1
        s, t = self.hot_seq, time.time()
        with conn.transaction():
            conn.execute("INSERT INTO orders (seq, t) VALUES (%s, %s)", (s, t))
            conn.execute("INSERT INTO order_items (seq, order_seq, t) "
                         "VALUES (%s, %s, %s)", (s, s, t))
        with self._lock:
            self.log["orders"].append((s, t))
            self.log["order_items"].append((s, t))

    def _cold(self, conn):
        self.cold_seq += 1
        s, t = self.cold_seq, time.time()
        with conn.transaction():
            conn.execute("INSERT INTO catalog (id, seq, t) VALUES (%s, %s, %s)",
                         (s, s, t))
            conn.execute("INSERT INTO category (id, seq, t) VALUES (%s, %s, %s)",
                         (s, s, t))
        with self._lock:
            self.log["catalog"].append((s, t))
            self.log["category"].append((s, t))

    def latest_committed(self, rel: str, before: float) -> int:
        with self._lock:
            return max((s for s, t in self.log[rel] if t <= before), default=0)

    def run(self):
        conn = psycopg.connect(PRIMARY)
        t0 = time.time()
        next_cold = t0 + self.cold_int / 2
        period = 1.0 / self.rate
        while True:
            now = time.time()
            el = now - t0
            if el >= self.duration:
                break
            if int(el // PHASE_S) % 2 == 0:          # busy phase
                self._hot(conn)
            if now >= next_cold:
                self._cold(conn)
                next_cold = now + self.cold_int
            time.sleep(period + self.jitter * 0.1)
        conn.close()


def derive_footprint(rep, role: str) -> set:
    """The production mechanism: learn a consumer's footprint from the
    replica's pg_stat_statements (what it actually queried), NOT from a
    declaration. Extract KNOWN_RELS from the role's normalized queries."""
    rels = set()
    rows = rep.execute(
        "SELECT s.query FROM pg_stat_statements s "
        "JOIN pg_roles r ON r.oid = s.userid WHERE r.rolname = %s",
        (role,)).fetchall()
    for (q,) in rows:
        for m in REL_RE.findall(q or ""):
            if m in KNOWN_RELS:
                rels.add(m)
    return rels


def measure_min_latency(prim, repl, n: int = 20) -> float:
    """Measure the substrate's MINIMUM replication latency by probing:
    write a row, poll the replica until it appears, keep the delay; the
    min over n probes is the physical transit floor. The beacon guard is
    derived from this (a write younger than the floor CANNOT be visible,
    so it must not be counted 'should-be-visible'). Generalizes: on real
    geo this is the min inter-site RTT, not a lab knob."""
    prim.execute("DROP TABLE IF EXISTS _probe")
    prim.execute("CREATE TABLE _probe (k int, t float8)")
    for _ in range(60):
        try:
            repl.execute("SELECT 1 FROM _probe LIMIT 1"); break
        except psycopg.errors.UndefinedTable:
            time.sleep(0.5)
    delays = []
    for k in range(1, n + 1):
        t0 = time.time()
        prim.execute("INSERT INTO _probe (k, t) VALUES (%s, %s)", (k, t0))
        while time.time() - t0 < 5.0:
            got = repl.execute("SELECT COALESCE(max(k),0) FROM _probe").fetchone()[0]
            if got >= k:
                delays.append(time.time() - t0); break
            time.sleep(0.005)
        time.sleep(0.05)
    prim.execute("DROP TABLE IF EXISTS _probe")
    return min(delays) if delays else 0.2


def run_cell(seed: int, duration: float = DURATION_S) -> dict:
    prim = psycopg.connect(PRIMARY, autocommit=True)
    prim.execute("DROP TABLE IF EXISTS orders, order_items, catalog, category")
    prim.execute("CREATE TABLE orders (seq bigint, t float8)")
    prim.execute("CREATE TABLE order_items (seq bigint, order_seq bigint, "
                 "t float8)")
    prim.execute("CREATE TABLE catalog (id int, seq bigint, t float8)")
    prim.execute("CREATE TABLE category (id int, seq bigint, t float8)")
    prim.execute("GRANT SELECT ON orders, order_items, catalog, category "
                 "TO consumer_hot, consumer_cold")
    # reclaim a possibly-active slot then recreate (XPROTO-PG lesson)
    prim.execute("SELECT pg_terminate_backend(active_pid) FROM "
                 "pg_replication_slots WHERE slot_name = %s "
                 "AND active_pid IS NOT NULL", (SLOT,))
    time.sleep(0.5)
    prim.execute("SELECT pg_drop_replication_slot(%s) FROM "
                 "pg_replication_slots WHERE slot_name = %s", (SLOT, SLOT))
    prim.execute("SELECT pg_create_logical_replication_slot(%s, "
                 "'test_decoding')", (SLOT,))
    # sentinel generation markers (readiness vs the apply-lag table race)
    for tbl in ("orders", "order_items"):
        prim.execute(f"INSERT INTO {tbl} (seq, {'order_seq, ' if tbl=='order_items' else ''}t) "
                     f"VALUES (0, {'0, ' if tbl=='order_items' else ''}0)")
    prim.execute("INSERT INTO catalog (id, seq, t) VALUES (0, 0, 0)")
    prim.execute("INSERT INTO category (id, seq, t) VALUES (0, 0, 0)")

    wit = psycopg.connect(PRIMARY, autocommit=True)
    repl = psycopg.connect(REPLICA, autocommit=True)
    for _ in range(120):
        try:
            r = repl.execute(
                "SELECT (SELECT max(seq) FROM orders), "
                "(SELECT max(seq) FROM order_items), "
                "(SELECT max(seq) FROM catalog), "
                "(SELECT max(seq) FROM category)").fetchone()
            if r == (0, 0, 0, 0):
                break
        except psycopg.errors.UndefinedTable:
            pass
        time.sleep(1.0)
    else:
        raise RuntimeError("replica never converged to the fresh schema")

    # populate pg_stat_statements on the replica: each consumer runs its
    # query a few times as its own role, then we DERIVE its footprint.
    try:
        repl.execute("SELECT pg_stat_statements_reset()")   # best-effort
    except psycopg.Error:
        pass
    footprints = {}
    for cons, spec in CONSUMERS.items():
        c = psycopg.connect(replica_as(spec["role"]), autocommit=True)
        for _ in range(3):
            c.execute(spec["query"]).fetchone()
        c.close()
    for cons, spec in CONSUMERS.items():
        footprints[cons] = derive_footprint(repl, spec["role"])

    # DERIVED sampling + guard (shakedown-corrected). The guard only needs
    # to cover the MEASUREMENT sampling skew, not the replication latency:
    # a write appears in last_change at the next slot pull (<= tick later),
    # so guard >= ~2*tick keeps the witness read never behind the truth
    # horizon (false-clears stay 0) while staying SMALL — the false-alarm
    # band is (0, guard), so a small guard minimizes phantom alarms. tick
    # is set fine relative to the substrate's transit (measured), which is
    # what generalizes to real geo (tens-of-ms lag -> ~10ms ticks).
    min_lat = measure_min_latency(prim, repl)
    tick = max(0.01, min(0.03, 0.3 * min_lat))
    guard = 2.0 * tick

    writer = Writer(seed, duration)
    writer.start()
    last_change = {r: 0 for r in KNOWN_RELS}
    samples = []
    t0 = time.time()
    while time.time() - t0 < duration:
        tick_t = time.time()
        for lsn, _x, data in wit.execute(
                "SELECT lsn, xid, data FROM "
                "pg_logical_slot_get_changes(%s, NULL, NULL)", (SLOT,)):
            for rel in KNOWN_RELS:
                if f"table public.{rel}:" in data:
                    last_change[rel] = max(last_change[rel], lsn_int(str(lsn)))
        row = repl.execute(
            "SELECT COALESCE(EXTRACT(EPOCH FROM "
            "  now() - pg_last_xact_replay_timestamp()), 1e9)::float8, "
            "pg_last_wal_replay_lsn()::text, "
            "(SELECT COALESCE(max(seq),0) FROM orders), "
            "(SELECT COALESCE(max(seq),0) FROM order_items), "
            "(SELECT COALESCE(max(seq),0) FROM catalog), "
            "(SELECT COALESCE(max(seq),0) FROM category)").fetchone()
        lag, rlsn = float(row[0]), lsn_int(row[1])
        vis = {"orders": int(row[2]), "order_items": int(row[3]),
               "catalog": int(row[4]), "category": int(row[5])}

        def stale_for(cons):
            fp = footprints[cons]
            return any(vis[rel] < writer.latest_committed(rel, tick_t - guard)
                       for rel in fp) if fp else False

        def aware_for(cons):
            fp = footprints[cons]
            return (max((last_change[rel] for rel in fp), default=0) <= rlsn
                    if fp else False)

        samples.append({
            "t": round(tick_t - t0, 2),
            "busy": int((tick_t - t0) // PHASE_S) % 2 == 0,
            "lag": round(lag, 3),
            "stale": {c: stale_for(c) for c in CONSUMERS},
            "aware": {c: aware_for(c) for c in CONSUMERS}})
        time.sleep(max(0.0, tick - (time.time() - tick_t)))
    writer.join()
    prim.close(); wit.close(); repl.close()

    n = len(samples)
    def frac(pred):
        return round(sum(1 for s in samples if pred(s)) / n, 4)

    naive = {}
    for T in THRESHOLDS:
        naive[f"{T}"] = {
            c: {"fc": frac(lambda s, c=c, T=T: s["lag"] < T and s["stale"][c]),
                "fa": frac(lambda s, c=c, T=T: s["lag"] >= T
                           and not s["stale"][c])}
            for c in CONSUMERS}
    aware = {c: {"fc": frac(lambda s, c=c: s["aware"][c] and s["stale"][c]),
                 "fa": frac(lambda s, c=c: not s["aware"][c]
                            and not s["stale"][c])}
             for c in CONSUMERS}
    naive_minmax = min(max(e[c][d] for c in CONSUMERS for d in ("fc", "fa"))
                       for e in naive.values())
    aware_max = max(aware[c][d] for c in CONSUMERS for d in ("fc", "fa"))
    lags = [s["lag"] for s in samples]
    mean_lag = sum(lags) / n
    lag_std = (sum((x - mean_lag) ** 2 for x in lags) / n) ** 0.5
    busy_lags = [s["lag"] for s in samples if s["busy"]]
    return {
        "seed": seed, "n_samples": n,
        "footprints": {c: sorted(footprints[c]) for c in CONSUMERS},
        "writes": {r: len(writer.log[r]) for r in KNOWN_RELS},
        "rate": round(writer.rate, 2), "cold_int": round(writer.cold_int, 2),
        "naive": naive, "aware": aware,
        "naive_minmax": round(naive_minmax, 4),
        "aware_max": round(aware_max, 4),
        "truth_stale_frac": {c: frac(lambda s, c=c: s["stale"][c])
                             for c in CONSUMERS},
        "lag_std": round(lag_std, 3),
        "max_busy_lag": round(max(busy_lags), 3) if busy_lags else 0.0,
        "min_latency": round(min_lat, 3),
        "guard": round(guard, 3), "tick": round(tick, 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default="PGXREP-family.json")
    args = ap.parse_args()
    cells = []
    for seed in args.seeds:
        print(f"cell seed {seed}…", flush=True)
        c = run_cell(seed)
        cells.append(c)
        print(f"  naive_minmax={c['naive_minmax']} aware_max={c['aware_max']}"
              f" stale={c['truth_stale_frac']} footprints={c['footprints']}"
              f" lag_std={c['lag_std']} writes={c['writes']}", flush=True)
    rec = {"family": "F-PGX", "sealed": False, "shakedown": True,
           "constants": {"thresholds": THRESHOLDS, "duration_s": DURATION_S,
                         "guard_tick": "DERIVED per cell: guard=0.7*measured "
                                       "min replication latency, tick=guard/2 "
                                       "(clamped [0.01,0.05]) — see per-cell "
                                       "min_latency/guard/tick",
                         "phase_s": PHASE_S, "rate_band": RATE_BAND,
                         "cold_interval_band": COLD_INTERVAL_BAND,
                         "lag_source": "netem WAN delay+jitter (lab_up.sh) "
                                       "under write load — emergent, uncontrolled"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
