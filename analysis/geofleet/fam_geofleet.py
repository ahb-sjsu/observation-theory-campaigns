"""XPROTO-GEO family (F-GEO): the geo-fleet cell.

Three routers compete to place each consumer on one replica of a real,
geo-distributed Postgres fleet; the consumer-relative WITNESSED
certificate is graded against two naive routers on two orthogonal axes:

  freshness : false-clear = routed to a replica STALE for the consumer's
              footprint (the consumer reads stale data).
  locality  : mean RTT of the chosen replica (from this consumer vantage).

Routers, per consumer (a consumer = a footprint = the relations it reads):
  nearest   : lowest-RTT replica            (ignores freshness)
  leastlag  : lowest GLOBAL replication lag  (ignores footprint + locality)
  cert      : nearest replica CERTIFIED fresh for the footprint
              (RTT-ordered, first-certified-wins; else the primary)

Claim: cert is FRESHER than nearest AND MORE LOCAL than leastlag -- it
beats each naive router on the axis that router optimizes.

Witness (no logical decoding needed, so the live primary is untouched):
the writer captures pg_current_wal_lsn() after each footprint write; a
replica is CERTIFIED for footprint F iff its replay LSN >= F's last-write
LSN. Ground truth is the beacon seq per relation, read on each replica --
independent of the LSN witness (as in XPROTO-PGX).

Runs IN-CLUSTER (a Job pod) so it reaches the primary + every replica.
    PRIMARY  env: libpq conninfo for the primary
    REPLICAS env: JSON [{"name","host","zone"}...]
"""

from __future__ import annotations

import argparse
import json
import os
import random
import threading
import time

import psycopg

# ---- sealed cell constants (bars reference these; do not tune) -------
DURATION_S = 90.0
TICK_S = 0.5
GUARD_S = 0.2
HOT_RATE = 8.0                 # writes/s to the hot footprint
COLD_INTERVAL_S = 6.0         # spacing of cold-footprint writes
RTT_PROBES = 3               # SELECT 1 round-trips per replica per tick
PAUSE_PERIOD_S = 6.0         # rotate which replica has replay paused
# consumer = footprint (the single relation it reads)
CONSUMERS = {"HOT": "orders", "COLD": "catalog"}
RELS = ("orders", "catalog")


def lsn_int(s: str) -> int:
    hi, lo = s.split("/")
    return (int(hi, 16) << 32) | int(lo, 16)


class Writer(threading.Thread):
    """Seeded beacon writer on the primary. Each write to relation R
    records (seq, commit_time) for ground truth and R's write LSN for the
    witness. Hot relation is written fast; cold rarely."""

    def __init__(self, prim_dsn: str, seed: int, duration: float):
        super().__init__(daemon=True)
        self.dsn = prim_dsn
        rng = random.Random(seed)
        self.hot_period = 1.0 / (HOT_RATE * rng.uniform(0.85, 1.15))
        self.cold_interval = COLD_INTERVAL_S * rng.uniform(0.85, 1.15)
        self.duration = duration
        self.log = {r: [] for r in RELS}          # [(seq, t, lsn)] per write
        self.seq = {r: 0 for r in RELS}
        self._lock = threading.Lock()

    def _write(self, conn, rel: str):
        self.seq[rel] += 1
        s, t = self.seq[rel], time.time()
        conn.execute(f"INSERT INTO {rel} (seq, t) VALUES (%s, %s)", (s, t))
        lsn = lsn_int(conn.execute("SELECT pg_current_wal_lsn()").fetchone()[0])
        with self._lock:
            self.log[rel].append((s, t, lsn))

    def committed(self, rel: str, before: float) -> int:
        with self._lock:
            return max((s for s, t, _ in self.log[rel] if t <= before), default=0)

    def guarded_lsn(self, rel: str, before: float) -> int:
        # LSN of the last footprint write at least GUARD old, so the witness
        # horizon MATCHES the truth guard. Comparing against the instantaneous
        # latest LSN would require replicas to hold an in-flight write no one
        # has yet -> nobody certified -> cert falls to the primary. Cf. the
        # XPROTO-PGX guard-consistency lesson.
        with self._lock:
            return max((l for _, t, l in self.log[rel] if t <= before), default=0)

    def run(self):
        conn = psycopg.connect(self.dsn, autocommit=True)
        t0 = time.time()
        next_cold = t0 + self.cold_interval / 2
        while time.time() - t0 < self.duration:
            self._write(conn, "orders")
            if time.time() >= next_cold:
                self._write(conn, "catalog")
                next_cold = time.time() + self.cold_interval
            time.sleep(self.hot_period)
        conn.close()


class Pauser(threading.Thread):
    """Induces the staleness the fast NRP backbone does not: rotates which
    replica has WAL replay PAUSED (one at a time), so at any moment one
    replica is behind on the hot footprint and the nearest router can be
    routed onto a stale replica. A controlled, disclosed stand-in for
    maintenance / load / network-lag events (cf. the roaming trial's
    pg_wal_replay_pause). Real inter-zone RTT still supplies the LOCALITY
    axis; this supplies the FRESHNESS axis. Resumes all replicas on exit."""

    def __init__(self, replicas: list[dict], seed: int, duration: float):
        super().__init__(daemon=True)
        self.replicas = replicas
        rng = random.Random(seed + 4242)
        self.order = [r["name"] for r in replicas]
        rng.shuffle(self.order)
        self.duration = duration

    def run(self):
        conns = {}
        for rep in self.replicas:
            dsn = (f"host={rep['host']} port=5432 user=postgres "
                   f"dbname=postgres connect_timeout=5")
            conns[rep["name"]] = psycopg.connect(dsn, autocommit=True)
        n = len(self.order)
        cycle = 0
        t0 = time.time()
        while time.time() - t0 < self.duration:
            paused = self.order[cycle % n]
            for name, c in conns.items():
                try:
                    c.execute("SELECT pg_wal_replay_pause()" if name == paused
                              else "SELECT pg_wal_replay_resume()")
                except psycopg.Error:
                    pass
            cycle += 1
            time.sleep(PAUSE_PERIOD_S)
        for c in conns.values():          # resume all on exit
            try:
                c.execute("SELECT pg_wal_replay_resume()")
            except psycopg.Error:
                pass
            c.close()


def _rtt(conn) -> float:
    """Median of RTT_PROBES SELECT-1 round-trips (seconds) on an open
    connection -- the network RTT to that replica from here."""
    xs = []
    for _ in range(RTT_PROBES):
        a = time.perf_counter()
        conn.execute("SELECT 1").fetchone()
        xs.append(time.perf_counter() - a)
    xs.sort()
    return xs[len(xs) // 2]


def run_cell(prim_dsn: str, replicas: list[dict], seed: int,
             duration: float = DURATION_S) -> dict:
    prim = psycopg.connect(prim_dsn, autocommit=True)
    # one persistent connection per replica (for RTT + reads)
    conns = {}
    for rep in replicas:
        dsn = (f"host={rep['host']} port=5432 user=postgres dbname=postgres "
               f"connect_timeout=5")
        conns[rep["name"]] = psycopg.connect(dsn, autocommit=True)
    # defensive: resume any replica a prior cell left paused (else it can't
    # replay the fresh schema and convergence would hang)
    for c in conns.values():
        try:
            c.execute("SELECT pg_wal_replay_resume()")
        except psycopg.Error:
            pass
    for r in RELS:
        prim.execute(f"DROP TABLE IF EXISTS {r}")
        prim.execute(f"CREATE TABLE {r} (seq bigint, t float8)")
        prim.execute(f"INSERT INTO {r} (seq, t) VALUES (0, 0)")  # sentinel

    # wait for every replica to replay the fresh generation (a replica may
    # not yet have the CREATE -> UndefinedTable -> treat as not-converged)
    def converged() -> bool:
        for c in conns.values():
            try:
                if c.execute("SELECT (SELECT max(seq) FROM orders),"
                             "(SELECT max(seq) FROM catalog)").fetchone() != (0, 0):
                    return False
            except psycopg.Error:
                return False
        return True
    for _ in range(150):
        if converged():
            break
        time.sleep(1.0)
    else:
        raise RuntimeError("not all replicas converged to the fresh schema")

    writer = Writer(prim_dsn, seed, duration)
    pauser = Pauser(replicas, seed, duration)   # induces rotating staleness
    writer.start()
    pauser.start()
    samples = []
    t0 = time.time()
    while time.time() - t0 < duration:
        tick = time.time()
        # per-replica state this tick
        st = {}
        for rep in replicas:
            c = conns[rep["name"]]
            rtt = _rtt(c)
            row = c.execute(
                "SELECT COALESCE(EXTRACT(EPOCH FROM "
                "  now()-pg_last_xact_replay_timestamp()),1e9)::float8,"
                "pg_last_wal_replay_lsn()::text,"
                "(SELECT COALESCE(max(seq),0) FROM orders),"
                "(SELECT COALESCE(max(seq),0) FROM catalog)").fetchone()
            st[rep["name"]] = {
                "rtt": rtt, "lag": float(row[0]),
                "replay": lsn_int(row[1]),
                "vis": {"orders": int(row[2]), "catalog": int(row[3])},
                "zone": rep.get("zone", "?")}
        # ground truth + witness per (replica, relation)
        commit = {r: writer.committed(r, tick - GUARD_S) for r in RELS}
        glsn = {r: writer.guarded_lsn(r, tick - GUARD_S) for r in RELS}
        for name, s in st.items():
            s["stale"] = {r: s["vis"][r] < commit[r] for r in RELS}        # truth (seq)
            s["cert"] = {r: glsn[r] <= s["replay"] for r in RELS}          # witness (guarded LSN)

        # three routers, per consumer -> (picked replica, false-clear, rtt)
        picks = {}
        for cons, rel in CONSUMERS.items():
            order_rtt = sorted(st, key=lambda n: st[n]["rtt"])
            nearest = order_rtt[0]
            leastlag = min(st, key=lambda n: st[n]["lag"])
            certified = next((n for n in order_rtt if st[n]["cert"][rel]), None)
            picks[cons] = {
                "nearest": nearest,
                "leastlag": leastlag,
                "cert": certified,           # None -> would fall to primary (fresh)
            }
        samples.append({"t": round(tick - t0, 2), "st": st, "picks": picks,
                        "commit": commit})
        time.sleep(max(0.0, TICK_S - (time.time() - tick)))
    writer.join()
    pauser.join()          # resumes all replicas on exit
    for c in conns.values():
        c.close()
    prim.close()

    # ---- aggregate: per consumer, per router: false-clear rate + mean rtt ----
    n = len(samples)
    routers = ("nearest", "leastlag", "cert")
    agg = {cons: {} for cons in CONSUMERS}
    for cons, rel in CONSUMERS.items():
        for rk in routers:
            fc = 0
            rtts = []
            for smp in samples:
                pick = smp["picks"][cons][rk]
                if pick is None:                 # cert found none -> primary (fresh, far)
                    rtts.append(max(s["rtt"] for s in smp["st"].values()) * 1.5)
                    continue
                s = smp["st"][pick]
                if s["stale"][rel]:
                    fc += 1
                rtts.append(s["rtt"])
            agg[cons][rk] = {
                "fc": round(fc / n, 4),
                "mean_rtt_ms": round(1000 * sum(rtts) / n, 3)}
    # manipulation-check data
    nearest_stale_hot = round(sum(
        1 for smp in samples
        if smp["st"][smp["picks"]["HOT"]["nearest"]]["stale"]["orders"]) / n, 4)
    rtts_by_rep = {name: 1000 * sum(smp["st"][name]["rtt"] for smp in samples) / n
                   for name in st}
    rtt_spread = (max(rtts_by_rep.values()) / max(min(rtts_by_rep.values()), 1e-6))
    # footprint-dependence: cert picks HOT and COLD differently on some ticks
    fp_diff = round(sum(1 for smp in samples
                        if smp["picks"]["HOT"]["cert"] != smp["picks"]["COLD"]["cert"]) / n, 4)
    return {
        "seed": seed, "n_samples": n, "n_replicas": len(replicas),
        "zones": sorted({r.get("zone", "?") for r in replicas}),
        "agg": agg,
        "nearest_stale_hot": nearest_stale_hot,
        "rtt_ms_by_replica": {k: round(v, 2) for k, v in rtts_by_rep.items()},
        "rtt_spread": round(rtt_spread, 2),
        "footprint_dependence": fp_diff,
        "hot_writes": writer.seq["orders"], "cold_writes": writer.seq["catalog"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--duration", type=float, default=DURATION_S)
    ap.add_argument("--out", default="GEOREP-family.json")
    args = ap.parse_args()
    prim = os.environ["PRIMARY"]
    replicas = json.loads(os.environ["REPLICAS"])
    cells = []
    for seed in args.seeds:
        print(f"cell seed {seed}…", flush=True)
        c = run_cell(prim, replicas, seed, args.duration)
        cells.append(c)
        h = c["agg"]["HOT"]
        print(f"  HOT fc: nearest={h['nearest']['fc']} leastlag={h['leastlag']['fc']} "
              f"cert={h['cert']['fc']} | mean_rtt_ms cert={h['cert']['mean_rtt_ms']} "
              f"nearest={h['nearest']['mean_rtt_ms']} leastlag={h['leastlag']['mean_rtt_ms']} "
              f"| MC nearest_stale={c['nearest_stale_hot']} rtt_spread={c['rtt_spread']} "
              f"fp_dep={c['footprint_dependence']}", flush=True)
    rec = {"family": "F-GEO", "sealed": False, "shakedown": True,
           "constants": {"duration_s": args.duration, "tick_s": TICK_S,
                         "guard_s": GUARD_S, "hot_rate": HOT_RATE,
                         "consumers": CONSUMERS},
           "cells": cells}
    print("RESULT_JSON:" + json.dumps(rec), flush=True)   # fallback: pod log
    # robust collection: write the record INTO the primary DB, so the driver
    # reads it via `kubectl exec` on the primary (avoids kubelet log-fetch
    # timeouts on the measure pod's node).
    try:
        pc = psycopg.connect(prim, autocommit=True)
        pc.execute("CREATE TABLE IF NOT EXISTS _geo_result "
                   "(id serial primary key, ts timestamptz default now(), rec jsonb)")
        pc.execute("INSERT INTO _geo_result (rec) VALUES (%s)", (json.dumps(rec),))
        pc.close()
        print("wrote result to primary._geo_result", flush=True)
    except Exception as e:
        print(f"WARN: could not write result to primary: {e}", flush=True)
    with open(args.out, "w") as f:
        json.dump(rec, f, indent=1)


if __name__ == "__main__":
    main()
