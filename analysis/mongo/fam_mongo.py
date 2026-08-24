"""XPROTO-MG family (F-MG): seeded measurement core + family shakedown.

The MongoDB twin of XPROTO-PG. Same claim, same bar shape, different
substrate: a replica set (primary + a **delayed secondary**,
`secondaryDelaySecs=1` — the analog of Postgres `recovery_min_apply_delay
=1000ms`) instead of streaming replication. The naive monitor is the
standard replica-lag gauge (`now − secondary.optimeDate`) graded against
every threshold in the sealed grid; the witness is the **oplog**
(`local.oplog.rs`): per-collection max change `ts` compared to the
secondary's applied optime `ts` — the direct analog of per-table max
change LSN vs the replica's replay LSN. Beacon ground truth is read on
the secondary exactly as in the PG cell.

Consumers: A's footprint = `hot_a` (bursty), B's = `hot_b` (sparse).
The family dimension is the seeded write schedule; each seeded cell
rebuilds fresh collections and re-baselines the oplog cursor.

    python3 fam_mongo.py                 # family shakedown, seeds 0 1 2
    python3 fam_mongo.py --seeds 7 8     # exploration only
"""

from __future__ import annotations

import argparse
import json
import random
import threading
import time
from datetime import datetime, timezone

import pymongo
from bson.timestamp import Timestamp

PRIMARY = "mongodb://127.0.0.1:55437/?directConnection=true"
SECONDARY = "mongodb://127.0.0.1:55438/?directConnection=true"
DB = "xproto"
NS = [f"{DB}.hot_a", f"{DB}.hot_b"]

# ---- sealed cell constants (bars reference these; do not tune) -------
THRESHOLDS = [0.1, 0.5, 1.0, 2.0, 5.0]   # naive-monitor grid (seconds)
DELAY_S = 1.0                             # secondaryDelaySecs, fixed
DURATION_S = 120.0
TICK_S = 0.2
GUARD_S = 0.20
PHASE_S = 20.0                            # busy/quiet alternation
RATE_BAND = (4.0, 6.0)                    # hot_a writes/s in busy phases
B_INTERVAL_BAND = (6.0, 10.0)            # hot_b write spacing


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Writer(threading.Thread):
    """Seeded beacon writer — identical schedule logic to F-PG's Writer,
    so the two cells differ only in substrate, not in stimulus."""

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

    def _write(self, db, coll: str):
        self.seq[coll] += 1
        db[coll].insert_one({"seq": self.seq[coll], "t": time.time()})
        with self._lock:
            self.log[coll].append((self.seq[coll], time.time()))

    def latest_committed(self, coll: str, before: float) -> int:
        with self._lock:
            return max((s for s, t in self.log[coll] if t <= before),
                       default=0)

    def run(self):
        # w=1: async ack from the primary only. The default w:majority
        # would block every write on the DELAYED secondary (throttling
        # writes AND making "committed" mean "the delayed member already
        # applied it", which erases the staleness this cell measures).
        cli = pymongo.MongoClient(PRIMARY, w=1)
        db = cli[DB]
        t0 = time.time()
        next_b = t0 + self.int_b / 2
        period = 1.0 / self.rate_a
        while True:
            now = time.time()
            el = now - t0
            if el >= self.duration:
                break
            if int(el // PHASE_S) % 2 == 0:          # busy phase
                self._write(db, "hot_a")
            if now >= next_b:
                self._write(db, "hot_b")
                next_b = now + self.int_b
            time.sleep(period + self.jitter * 0.1)
        cli.close()


def _secondary_optime(sec) -> tuple[Timestamp, datetime]:
    """The delayed secondary's own APPLIED optime (ts for the witness,
    date for the naive lag), read from the SECONDARY directly (its `self`
    member). Reading it via the primary's replSetGetStatus would carry up
    to a heartbeat-interval (~2 s) of staleness in the primary's view of
    the secondary, injecting false STALE into the witness."""
    st = sec.admin.command("replSetGetStatus")
    me = next(m for m in st["members"] if m.get("self"))
    d = me["optimeDate"]
    if d.tzinfo is None:                  # pymongo may decode this naive
        d = d.replace(tzinfo=timezone.utc)
    return me["optime"]["ts"], d


def run_cell(seed: int, duration: float = DURATION_S) -> dict:
    """One seeded cell. Fresh collections + re-baselined oplog cursor;
    returns the full metric record the bars are evaluated on."""
    # tz_aware so secondary.optimeDate is offset-aware UTC (pymongo returns
    # naive datetimes by default) and the naive-lag subtraction is valid.
    # w=1 so sentinel/structural writes here also don't block on the delay.
    prim = pymongo.MongoClient(PRIMARY, tz_aware=True, w=1)
    sec = pymongo.MongoClient(
        SECONDARY, read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED)
    pdb, sdb = prim[DB], sec[DB]
    oplog = prim.local.oplog.rs

    # baseline the oplog cursor at the newest entry BEFORE this cell's
    # writes, so the witness only counts changes from this cell.
    top = list(oplog.find().sort("$natural", -1).limit(1))
    last_seen = top[0]["ts"] if top else Timestamp(0, 0)

    pdb.hot_a.drop()
    pdb.hot_b.drop()
    # sentinel rows mark the fresh generation: with the 1 s delay the
    # secondary can still serve the PREVIOUS generation. Ready = both
    # collections report exactly max(seq)=0 on the secondary.
    pdb.hot_a.insert_one({"seq": 0, "t": 0.0})
    pdb.hot_b.insert_one({"seq": 0, "t": 0.0})

    def sec_max(coll: str) -> int:
        d = list(sdb[coll].find({}, {"seq": 1}).sort("seq", -1).limit(1))
        return int(d[0]["seq"]) if d else -1

    for _ in range(90):
        if sec_max("hot_a") == 0 and sec_max("hot_b") == 0:
            break
        time.sleep(1.0)
    else:
        raise RuntimeError("secondary never converged to the fresh collections")

    writer = Writer(seed, duration)
    writer.start()
    last_change = {"hot_a": Timestamp(0, 0), "hot_b": Timestamp(0, 0)}
    samples = []
    t0 = time.time()
    while time.time() - t0 < duration:
        tick_t = time.time()
        # consume new oplog entries touching the footprints (witness)
        for doc in oplog.find({"ns": {"$in": NS}, "ts": {"$gt": last_seen}}):
            last_seen = max(last_seen, doc["ts"])
            coll = doc["ns"].split(".", 1)[1]
            if coll in last_change and doc["ts"] > last_change[coll]:
                last_change[coll] = doc["ts"]
        sec_ts, sec_date = _secondary_optime(sec)
        lag = max(0.0, (now_utc() - sec_date).total_seconds())
        vis = {"hot_a": sec_max("hot_a"), "hot_b": sec_max("hot_b")}
        samples.append({
            "t": round(tick_t - t0, 2),
            "busy": int((tick_t - t0) // PHASE_S) % 2 == 0,
            "lag": round(lag, 3),
            "stale": {c: vis[k] < writer.latest_committed(k, tick_t - GUARD_S)
                      for c, k in (("A", "hot_a"), ("B", "hot_b"))},
            "aware": {c: last_change[k] <= sec_ts
                      for c, k in (("A", "hot_a"), ("B", "hot_b"))}})
        time.sleep(max(0.0, TICK_S - (time.time() - tick_t)))
    writer.join()
    prim.close()
    sec.close()

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
    naive_minmax = min(max(e[c][d] for c in ("A", "B") for d in ("fc", "fa"))
                       for e in naive.values())
    aware_max = max(aware[c][d] for c in ("A", "B") for d in ("fc", "fa"))
    busy_lags = [s["lag"] for s in samples if s["busy"]]
    return {
        "seed": seed, "n_samples": n,
        "writes": {c: len(writer.log[c]) for c in writer.log},
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
    ap.add_argument("--out", default="MGREP-family.json")
    args = ap.parse_args()
    cells = []
    for seed in args.seeds:
        print(f"cell seed {seed}…", flush=True)
        c = run_cell(seed)
        cells.append(c)
        print(f"  naive_minmax={c['naive_minmax']} aware_max={c['aware_max']}"
              f" stale_frac={c['truth_stale_frac']}"
              f" writes={c['writes']}", flush=True)
    rec = {"family": "F-MG", "sealed": False, "shakedown": True,
           "constants": {"thresholds": THRESHOLDS,
                         "delay_s": DELAY_S,
                         "duration_s": DURATION_S, "tick_s": TICK_S,
                         "guard_s": GUARD_S, "phase_s": PHASE_S,
                         "rate_band": RATE_BAND,
                         "b_interval_band": B_INTERVAL_BAND},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
