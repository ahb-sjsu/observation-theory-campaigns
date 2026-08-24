"""XPROTO-ZK family (F-ZK): the ZooKeeper local-read staleness cell -- the
coordination-service twin of the PostgreSQL/MongoDB delayed-replica cells.

Certificate = a local follower read is fresh enough. Consumer = the reader's
znode footprint. False-clear = a local read returns a STALE version (the
follower's applied mzxid for that znode is behind the leader's committed mzxid).
Witness = the zxid: each znode carries its modification zxid (mzxid); the leader's
committed mzxid is the ground truth, the follower's is what a local read sees.
Deployed correction = sync(), ZooKeeper's freshness barrier (flush leader->
follower before the read). Writes stay linearizable through the leader (Zab);
only local reads go stale.

Consumer-relativity is the crux and is measured directly on ONE delayed follower:
a HOT footprint (frequently-written znodes) reads stale; a COLD footprint
(rarely-written znodes) on the SAME follower reads fresh -- no single "follower
is fresh enough" assumption serves both, and the cold footprint being fresh shows
the follower is sane (the staleness is footprint-relative, not a broken replica).

Three policies per sampled read:
  naive     : trust the local follower read (no check).      -> stale rate
  witnessed : sync() the path, then read the follower.       -> ~0 (the barrier)
  (fresh)   : read the leader; the truth reference (control).

Staleness is guard-consistent: truth (leader mzxid) is captured BEFORE the
follower read, so a write that commits during the read is not counted stale
(in-flight writes do not disqualify the follower) -- the geo/PGX guard lesson.

  mode "zk": real 3-node ensemble on Atlas (see lab_up.sh, topology.json).
Emits ZKREP-family.json.
"""
import argparse
import json
import os
import random
import threading
import time

from kazoo.client import KazooClient

HERE = os.path.dirname(os.path.abspath(__file__))
TOPO = json.load(open("/home/claude/zk/topology.json"))

# ---- sealed cell constants (bars reference these; do not tune) -------
N_ZNODES = 10
HOT = [0, 1, 2]            # hot footprint: frequently written
COLD = [7, 8, 9]           # cold footprint: rarely written
DURATION_S = 12.0          # fast naive-sampling phase
N_WIT = 60                 # witnessed (sync) samples (each ~one induced-delay RTT)
HOT_INTERVAL_S = 0.012     # a hot write every ~12 ms (<< the induced lag)
COLD_EVERY = 300           # a cold write every ~300 hot writes (~3.6 s >> lag)
SETTLE_S = 0.5             # let the follower lag build before sampling
TARGET = 0.10


def _p(i):
    return f"/z/{i}"


def run_cell(seed, duration=DURATION_S):
    w = KazooClient(hosts=f"localhost:{TOPO['leader_port']}")
    r = KazooClient(hosts=f"localhost:{TOPO['follower_port']}")
    t = KazooClient(hosts=f"localhost:{TOPO['leader_port']}")
    w.start(); r.start(); t.start()
    for i in range(N_ZNODES):
        w.ensure_path(_p(i))
        w.set(_p(i), b"0")

    stop = threading.Event()
    nwrites = [0]

    def writer():
        wr = random.Random(seed * 7 + 1)
        k = 0
        while not stop.is_set():
            w.set(_p(wr.choice(HOT)), str(wr.random()).encode()); nwrites[0] += 1
            if k % COLD_EVERY == 0:
                w.set(_p(wr.choice(COLD)), str(wr.random()).encode()); nwrites[0] += 1
            k += 1
            time.sleep(HOT_INTERVAL_S)

    th = threading.Thread(target=writer, daemon=True)
    th.start()
    time.sleep(SETTLE_S)

    rng = random.Random(seed)
    hot_stale = n_hot = cold_stale = n_cold = 0
    wit_stale = n_wit = 0
    gaps = []
    # phase 1 -- fast naive sampling (no sync): hot + cold footprints on the
    # SAME delayed follower; truth (leader mzxid) read BEFORE the follower.
    end = time.time() + duration
    while time.time() < end:
        i = rng.choice(HOT)
        lz = t.get(_p(i))[1].mzxid
        fz = r.get(_p(i))[1].mzxid
        gaps.append(lz - fz); n_hot += 1
        if fz < lz:
            hot_stale += 1
        j = rng.choice(COLD)
        lzc = t.get(_p(j))[1].mzxid
        fzc = r.get(_p(j))[1].mzxid
        n_cold += 1
        if fzc < lzc:
            cold_stale += 1
    # phase 2 -- witnessed: sync() barrier then read (each waits one induced RTT)
    for _ in range(N_WIT):
        i = rng.choice(HOT)
        lz = t.get(_p(i))[1].mzxid
        r.sync(_p(i)); wz = r.get(_p(i))[1].mzxid
        n_wit += 1
        if wz < lz:
            wit_stale += 1

    stop.set(); th.join(timeout=2)
    w.stop(); r.stop(); t.stop()
    return {
        "seed": int(seed), "mode": "zk", "delay_ms": TOPO.get("delay_ms"),
        "naive_hot": round(hot_stale / max(1, n_hot), 4),
        "naive_cold": round(cold_stale / max(1, n_cold), 4),
        "witnessed": round(wit_stale / max(1, n_wit), 4),
        "mean_zxid_gap": round(sum(gaps) / max(1, len(gaps)), 3),
        "n_reads": n_hot + n_cold, "n_wit": n_wit,
        "n_writes": nwrites[0], "target": TARGET,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "ZKREP-family.json"))
    args = ap.parse_args()
    cells = []
    for seed in args.seeds:
        c = run_cell(seed)
        cells.append(c)
        print(f"seed {seed}: naive_hot={c['naive_hot']} naive_cold={c['naive_cold']} "
              f"witnessed={c['witnessed']} zxid_gap={c['mean_zxid_gap']} "
              f"reads={c['n_reads']} writes={c['n_writes']}", flush=True)
    rec = {"family": "F-ZK", "mode": "zk",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"n_znodes": N_ZNODES, "hot": HOT, "cold": COLD,
                         "duration_s": DURATION_S, "hot_interval_s": HOT_INTERVAL_S,
                         "cold_every": COLD_EVERY, "delay_ms": TOPO.get("delay_ms"),
                         "target": TARGET,
                         "substrate": ("3-node ZooKeeper ensemble; local follower reads "
                                       "vs leader-committed mzxid witness; sync() barrier; "
                                       "staleness induced by leader->follower netem delay")},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
