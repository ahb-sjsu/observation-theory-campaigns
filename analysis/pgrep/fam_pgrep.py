"""XPROTO-PG family (F-PG): seeded measurement core + family shakedown.

The sealed cell's instrument. One cell = one seeded run on the lab
(primary wal_level=logical + replica recovery_min_apply_delay=1000ms):
a seeded write schedule (the family dimension), the naive lag monitor
graded against every threshold in the sealed grid, the WAL-witness
footprint certificate, and beacon ground truth. The graded runner
(pgrep_check.py) imports THIS measurement unchanged; only bars differ
between shakedown and seal.

Family property (checked across seeds, per the OT-17 lesson): the
two-sided naive failure and two-sided witness success must hold on
EVERY seed, not on a lucky draw.

    python3 fam_pgrep.py                 # family shakedown, seeds 0 1 2
    python3 fam_pgrep.py --seeds 7 8     # exploration only
"""

from __future__ import annotations

import argparse
import json
import random
import threading
import time

import psycopg

PRIMARY = "postgresql://postgres:lab@127.0.0.1:55433/postgres"
REPLICA = "postgresql://postgres:lab@127.0.0.1:55434/postgres"

# ---- sealed cell constants (bars reference these; do not tune) -------
THRESHOLDS = [0.1, 0.5, 1.0, 2.0, 5.0]   # naive-monitor grid
APPLY_DELAY_S = 1.0                       # lab knob, fixed for the cell
DURATION_S = 120.0
TICK_S = 0.2
GUARD_S = 0.20
PHASE_S = 20.0                            # busy/quiet alternation
RATE_BAND = (4.0, 6.0)                    # hot_a writes/s in busy phases
B_INTERVAL_BAND = (6.0, 10.0)             # hot_b write spacing
SLOT = "ngpg_witness"


def lsn_int(s: str) -> int:
    hi, lo = s.split("/")
    return (int(hi, 16) << 32) | int(lo, 16)


class Writer(threading.Thread):
    """Seeded beacon writer. The seed draws the busy-phase rate and the
    hot_b spacing from the sealed bands; phases alternate busy/quiet so
    every seed has interior in both regimes."""

    def __init__(self, seed: int, duration: float):
        super().__init__(daemon=True)
        rng = random.Random(seed)
        self.rate_a = rng.uniform(*RATE_BAND)
        self.int_b = rng.uniform(*B_INTERVAL_BAND)
        self.jitter = rng.uniform(0.0, 0.08)
        self.duration = duration
        self.log = {"hot_a": [], "hot_b": []}
        self.seq = {"hot_a": 0, "hot_b": 0}
        self._lock = threading.Lock()

    def _write(self, conn, table: str):
        self.seq[table] += 1
        conn.execute(f"INSERT INTO {table} (seq, t) VALUES (%s, %s)",
                     (self.seq[table], time.time()))
        with self._lock:
            self.log[table].append((self.seq[table], time.time()))

    def latest_committed(self, table: str, before: float) -> int:
        with self._lock:
            return max((s for s, t in self.log[table] if t <= before),
                       default=0)

    def run(self):
        conn = psycopg.connect(PRIMARY, autocommit=True)
        t0 = time.time()
        next_b = t0 + self.int_b / 2
        period = 1.0 / self.rate_a
        while True:
            now = time.time()
            el = now - t0
            if el >= self.duration:
                break
            if int(el // PHASE_S) % 2 == 0:          # busy phase
                self._write(conn, "hot_a")
            if now >= next_b:
                self._write(conn, "hot_b")
                next_b = now + self.int_b
            time.sleep(period + self.jitter * 0.1)
        conn.close()


def run_cell(seed: int, duration: float = DURATION_S) -> dict:
    """One seeded cell. Fresh tables + fresh slot; returns the full
    metric record the bars are evaluated on."""
    prim = psycopg.connect(PRIMARY, autocommit=True)
    prim.execute("DROP TABLE IF EXISTS hot_a, hot_b")
    prim.execute("CREATE TABLE hot_a (seq bigint, t float8)")
    prim.execute("CREATE TABLE hot_b (seq bigint, t float8)")
    # a previously killed client can leave the slot 'active'; reclaim it
    prim.execute("SELECT pg_terminate_backend(active_pid) FROM "
                 "pg_replication_slots WHERE slot_name = %s "
                 "AND active_pid IS NOT NULL", (SLOT,))
    time.sleep(0.5)
    prim.execute("SELECT pg_drop_replication_slot(%s) FROM "
                 "pg_replication_slots WHERE slot_name = %s", (SLOT, SLOT))
    prim.execute("SELECT pg_create_logical_replication_slot(%s, "
                 "'test_decoding')", (SLOT,))
    # sentinel rows mark the fresh table generation: with the 1 s apply
    # delay the replica can still serve the PREVIOUS generation (a
    # readiness probe on table existence races the DROP mid-run --
    # caught 2026-08-19). Ready = both tables report exactly max(seq)=0.
    prim.execute("INSERT INTO hot_a (seq, t) VALUES (0, 0)")
    prim.execute("INSERT INTO hot_b (seq, t) VALUES (0, 0)")
    wit = psycopg.connect(PRIMARY, autocommit=True)
    repl = psycopg.connect(REPLICA, autocommit=True)
    for _ in range(90):
        try:
            r = repl.execute(
                "SELECT (SELECT max(seq) FROM hot_a), "
                "(SELECT max(seq) FROM hot_b)").fetchone()
            if r == (0, 0):
                break
        except psycopg.errors.UndefinedTable:
            pass
        time.sleep(1.0)
    else:
        raise RuntimeError("replica never converged to the fresh tables")

    writer = Writer(seed, duration)
    writer.start()
    last_change = {"hot_a": 0, "hot_b": 0}
    samples = []
    t0 = time.time()
    while time.time() - t0 < duration:
        tick_t = time.time()
        for lsn, _x, data in wit.execute(
                "SELECT lsn, xid, data FROM "
                "pg_logical_slot_get_changes(%s, NULL, NULL)", (SLOT,)):
            for tbl in ("hot_a", "hot_b"):
                if f"table public.{tbl}:" in data:
                    last_change[tbl] = max(last_change[tbl],
                                           lsn_int(str(lsn)))
        row = repl.execute(
            "SELECT COALESCE(EXTRACT(EPOCH FROM "
            "  now() - pg_last_xact_replay_timestamp()), 1e9)::float8, "
            "pg_last_wal_replay_lsn()::text, "
            "(SELECT COALESCE(max(seq),0) FROM hot_a), "
            "(SELECT COALESCE(max(seq),0) FROM hot_b)").fetchone()
        lag, rlsn = float(row[0]), lsn_int(row[1])
        vis = {"hot_a": int(row[2]), "hot_b": int(row[3])}
        samples.append({
            "t": round(tick_t - t0, 2),
            "busy": int((tick_t - t0) // PHASE_S) % 2 == 0,
            "lag": round(lag, 3),
            "stale": {c: vis[t] < writer.latest_committed(t, tick_t - GUARD_S)
                      for c, t in (("A", "hot_a"), ("B", "hot_b"))},
            "aware": {c: last_change[t] <= rlsn
                      for c, t in (("A", "hot_a"), ("B", "hot_b"))}})
        time.sleep(max(0.0, TICK_S - (time.time() - tick_t)))
    writer.join()

    n = len(samples)
    def frac(pred):
        return round(sum(1 for s in samples if pred(s)) / n, 4)

    naive = {}
    for T in THRESHOLDS:
        naive[f"{T}"] = {
            c: {"fc": frac(lambda s, c=c, T=T: s["lag"] < T and s["stale"][c]),
                "fa": frac(lambda s, c=c, T=T: s["lag"] >= T
                           and not s["stale"][c])}
            for c in ("A", "B")}
    aware = {c: {"fc": frac(lambda s, c=c: s["aware"][c] and s["stale"][c]),
                 "fa": frac(lambda s, c=c: not s["aware"][c]
                            and not s["stale"][c])}
             for c in ("A", "B")}
    # per-threshold worst error across consumers/directions; its min is
    # the best the naive monitor can do at any threshold
    naive_minmax = min(max(e[c][d] for c in ("A", "B") for d in ("fc", "fa"))
                       for e in naive.values())
    aware_max = max(aware[c][d] for c in ("A", "B") for d in ("fc", "fa"))
    busy_lags = [s["lag"] for s in samples if s["busy"]]
    return {
        "seed": seed, "n_samples": n,
        "writes": {t: len(writer.log[t]) for t in writer.log},
        "rate_a": round(writer.rate_a, 2), "int_b": round(writer.int_b, 2),
        "naive": naive, "aware": aware,
        "naive_minmax": round(naive_minmax, 4),
        "aware_max": round(aware_max, 4),
        "truth_stale_frac": {c: frac(lambda s, c=c: s["stale"][c])
                             for c in ("A", "B")},
        "max_busy_lag": round(max(busy_lags), 3) if busy_lags else 0.0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default="PGREP-family.json")
    args = ap.parse_args()
    cells = []
    for seed in args.seeds:
        print(f"cell seed {seed}…", flush=True)
        c = run_cell(seed)
        cells.append(c)
        print(f"  naive_minmax={c['naive_minmax']} aware_max={c['aware_max']}"
              f" stale_frac={c['truth_stale_frac']}"
              f" writes={c['writes']}", flush=True)
    rec = {"family": "F-PG", "sealed": False, "shakedown": True,
           "constants": {"thresholds": THRESHOLDS,
                         "apply_delay_s": APPLY_DELAY_S,
                         "duration_s": DURATION_S, "tick_s": TICK_S,
                         "guard_s": GUARD_S, "phase_s": PHASE_S,
                         "rate_band": RATE_BAND,
                         "b_interval_band": B_INTERVAL_BAND},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
