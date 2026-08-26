"""XPROTO-ZK-FLIP family (F-ZK-FLIP): the two-consumer verdict inversion (the
Flip) in coordination-service reads, with its taxonomy-predicted null.

Two staleness axes, varied independently by the lab (lab_up_flip.sh):
  churn : hot znodes take a write every ~12 ms, cold ones every ~3.6 s
  lag   : the fast follower lags 50 ms, the slow one 400 ms
Two reader fleets with misaligned reads:
  H-fleet: hot znodes through the FAST follower (churn dominates its staleness)
  L-fleet: cold znodes through the SLOW follower (lag dominates its staleness)

Policies: a fixed sync() budget, mean probability 0.5 per read, allocated two
ways. Policy A syncs by churn (0.9 on hot keys, 0.1 on cold). Policy B syncs by
lag (0.9 through the slow follower, 0.1 through the fast). A read false-clears
when it is served without a fresh view and the follower's mzxid is behind the
leader's. Claim: the H-fleet does better under A, the L-fleet under B. The fleet
aggregate prefers A while the L-fleet strongly prefers B, so the aggregate
misserves half the readers.

Registered null: two consumers on the SAME stream (hot znodes through the fast
follower) that differ only in staleness tolerance (any gap, versus gap > 5
zxids). A tolerance shift leaves both reading the same projection, so the same
two policies must move their failure rates together, and no inversion is
expected.

Substrate: real ZooKeeper 3.9 ensemble on Atlas, zxid witness, guard-consistent
order (leader mzxid read BEFORE the follower). Run in ~/zk-venv. Emits
ZKFLIPREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import threading
import time

from kazoo.client import KazooClient

HERE = os.path.dirname(os.path.abspath(__file__))
TOPO = json.load(open(os.path.join(os.path.expanduser("~/zk"), "topology_flip.json")))
N_ZNODES = 10
HOT = [0, 1, 2]
COLD = [9]                 # pilot 3: a single cold znode. With three, a cold write
                           # lands on one of them, so a reader of a random cold
                           # znode sees only a third of the 400 ms stale windows
                           # (0.11/3, then sync dilution), which is why pilot 2's
                           # L-gaps were thin. One znode restores the full
                           # lag/interval fraction (~0.11) the design doc computes.
HOT_INTERVAL_S = 0.012
COLD_EVERY = 300
DURATION_S = 60
N_READS = 600              # per fleet per policy (pilot 4: doubled for power)
READ_SPACING_S = 0.05      # pace reads so cold-key reads span many write cycles
                           # (pilot 1: 300 back-to-back reads covered < 1 cold
                           # cycle, so the L-fleet's lag axis was under-sampled)
# PILOT 4 (declared BEFORE the run, with a stopping rule): slow lag raised to
# 1200 ms (lab_up_flip.sh 50 1200). A priori expectation from lag/interval
# arithmetic: unsynced cold-read stale fraction ~ 1.2/3.6 = 0.33, so
# L_A ~ 0.30 and L_B ~ 0.03, gap ~ 0.27 (~14 sigma at n=600). STOPPING RULE:
# if any seed's L-gap comes in under 0.10, the ZK flip is recorded as a kept
# exploration and NOT registered. No pilot 5.
SYNC_MEAN = 0.5            # matched budget: mean sync probability per read
P_HI, P_LO = 0.9, 0.1      # allocation extremes (mean 0.5 over the two fleets)
NULL_TOL = 5               # zxid-gap tolerance for the null's second consumer


def _p(i):
    return f"/flip/n{i}"


def _client(port):
    c = KazooClient(hosts=f"127.0.0.1:{port}")
    c.start(timeout=15)
    return c


def run_cell(seed):
    rng = random.Random(seed)
    w = _client(TOPO["leader_port"])
    t = _client(TOPO["leader_port"])         # truth reader (leader, committed mzxid)
    rf = _client(TOPO["fast_port"])          # fast follower
    rs = _client(TOPO["slow_port"])          # slow follower
    w.ensure_path("/flip")
    for i in range(N_ZNODES):
        if not w.exists(_p(i)):
            w.create(_p(i), b"0")
    stop = [False]
    wr = random.Random(seed + 1)

    def writer():
        k = 0
        while not stop[0]:
            k += 1
            w.set(_p(wr.choice(HOT)), str(wr.random()).encode())
            if k % COLD_EVERY == 0:
                w.set(_p(wr.choice(COLD)), str(wr.random()).encode())
            time.sleep(HOT_INTERVAL_S)

    th = threading.Thread(target=writer, daemon=True)
    th.start()
    time.sleep(2.0)

    def read_fc(keys, reader, p_sync, tol=0):
        """Stale-read fraction over N_READS: sync first with probability p_sync;
        stale when the follower's mzxid trails the leader's by more than tol."""
        stale = 0
        for _ in range(N_READS):
            i = rng.choice(keys)
            if rng.random() < p_sync:
                reader.sync(_p(i))
            lz = t.get(_p(i))[1].mzxid       # truth BEFORE the follower read
            fz = reader.get(_p(i))[1].mzxid
            if lz - fz > tol:
                stale += 1
            time.sleep(READ_SPACING_S)       # span many cold-write cycles
        return stale / N_READS

    out = {"seed": int(seed), "mode": "zk", "fast_ms": TOPO["fast_ms"],
           "slow_ms": TOPO["slow_ms"], "n_reads": N_READS,
           "mean_sync_A": SYNC_MEAN, "mean_sync_B": SYNC_MEAN}
    # policy A: sync by churn (hot 0.9, cold 0.1); policy B: by lag (slow 0.9, fast 0.1)
    out["fc_H_A"] = round(read_fc(HOT, rf, P_HI), 4)     # H under A: hot -> 0.9
    out["fc_L_A"] = round(read_fc(COLD, rs, P_LO), 4)    # L under A: cold -> 0.1
    out["fc_H_B"] = round(read_fc(HOT, rf, P_LO), 4)     # H under B: fast -> 0.1
    out["fc_L_B"] = round(read_fc(COLD, rs, P_HI), 4)    # L under B: slow -> 0.9
    out["fc_fleet_A"] = round(0.5 * (out["fc_H_A"] + out["fc_L_A"]), 4)
    out["fc_fleet_B"] = round(0.5 * (out["fc_H_B"] + out["fc_L_B"]), 4)
    out["flip"] = bool(out["fc_H_A"] < out["fc_H_B"] and out["fc_L_B"] < out["fc_L_A"])
    # null: hot-through-fast at two tolerances; both consumers are hot AND fast, so
    # A gives both 0.9 and B gives both 0.1; their rates must move together.
    out["null_fc_t0_A"] = round(read_fc(HOT, rf, P_HI, tol=0), 4)
    out["null_fc_t5_A"] = round(read_fc(HOT, rf, P_HI, tol=NULL_TOL), 4)
    out["null_fc_t0_B"] = round(read_fc(HOT, rf, P_LO, tol=0), 4)
    out["null_fc_t5_B"] = round(read_fc(HOT, rf, P_LO, tol=NULL_TOL), 4)
    out["null_flip"] = bool(out["null_fc_t0_A"] < out["null_fc_t0_B"]
                            and out["null_fc_t5_B"] < out["null_fc_t5_A"])
    stop[0] = True
    th.join(timeout=3)
    for c in (w, t, rf, rs):
        c.stop(); c.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "ZKFLIPREP-family.json"))
    args = ap.parse_args()
    cells = []
    for s in args.seeds:
        c = run_cell(s)
        cells.append(c)
        print(f"seed {s}: H A={c['fc_H_A']} B={c['fc_H_B']} | L A={c['fc_L_A']} "
              f"B={c['fc_L_B']} | fleet A={c['fc_fleet_A']} B={c['fc_fleet_B']} | "
              f"FLIP={c['flip']} null_flip={c['null_flip']}", flush=True)
    rec = {"family": "F-ZK-FLIP", "mode": "zk",
           "constants": {"fast_ms": TOPO["fast_ms"], "slow_ms": TOPO["slow_ms"],
                         "hot_interval_s": HOT_INTERVAL_S, "cold_every": COLD_EVERY,
                         "n_reads": N_READS, "p_hi": P_HI, "p_lo": P_LO,
                         "null_tol": NULL_TOL,
                         "substrate": "real ZooKeeper 3.9 ensemble, two netem lag "
                                      "profiles, zxid witness"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
