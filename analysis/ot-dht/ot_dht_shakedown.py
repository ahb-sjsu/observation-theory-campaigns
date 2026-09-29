#!/usr/bin/env python3
"""OT-DHT shakedown (UNSEALED, exploratory) -- the five principles of
Observation Theory v1.0, measured on a live BitTorrent DHT router.

Object (readscope PRINCIPLES.md, the common object): a consumer C reading a
representation x through P_C = E_D[J^T G J]. Here x is a 160-bit DHT id (a
lookup target), and C is Kademlia routing: C(x) = the node XOR-nearest to x
among the node ids the tqp-dht daemon on Atlas has seen on the public DHT. P_C
is identified blind, as readscope does: flip each of the 160 bits of x and ask
whether the routing decision changes; diag P_C at bit i is the share of targets
under D for which it does. The routing consumer is expected to read the leading
bits and stop near log2 N; the rest is ker P_C.

Instrument: turboquant-pro plugins/tqp-dht/tqp_dht/observe.py at commit
adeb05221a445f1af6e81f9324f6e0c654b95778 (sha256 dd5c0caf...1490b45ba),
validated before this registration on synthetic node sets (exact against brute
force including top-word ties; knee within 3 bits of log2 N; +1 bit of read
depth per doubling of N; invariant under a common XOR relabelling; the flip
reversing between routing and a sharder; blind probing at k/d; kernel silence).

Substrate: the daemon's frozen node set (nodes.bin: every node id seen as a
query sender, response sender or listed node, newest 65536; its SHA-256 is
recorded), its lookup targets (targets.jsonl), and our own node ids (meta.json).
Probe distributions, 512 targets each, seed 20260929:
  D_uniform  uniform 160-bit ids;
  D_self     ids sharing >= 16 leading bits with our first node id (sorted);
  D_traffic  the most recent 512 targets our node itself looked up.
Kernel = bits with measured diag P_C == 0 under D_uniform.

PRE-STATED PREDICTIONS (graded after the run, disclosed either way):
  P1 consumer relativity. Under D_uniform the router's read spectrum is not
     the isotropic observer's (1.0 on every bit): its knee K (first bit read
     < 50%) lies in [log2 N - 6, log2 N + 2] (the seen set clusters near our
     ids and our targets, so uniform space is sparser than N suggests, hence
     the lower side is wider); bits < K - 4 are read >= 0.9; bits >= K + 8
     are read <= 0.05. And the flip: codes keeping the top 32 bits (A) and
     the bottom 32 bits (B) have equal reconstruction error (128 bits); the
     router agrees with A >= 0.95 and with B <= 0.05. (The sharder, which
     buckets by the low 16 bits, ranks them oppositely by construction; its
     numbers are printed, not graded.)
  P2 measure dependence. The same probe reads differently depending on where
     it probes: tr P_C (read depth, bits) under D_self exceeds D_uniform's by
     >= 3 bits, and under D_traffic exceeds D_uniform's by >= 1 bit. (Noise:
     the depth's standard error is ~0.1 bit at 512 targets.)
  P3 observation complexity. Blind identification spends d = 160 flips per
     target to find a read subspace of effective rank r = #bits read >= 50%:
     d / r >= 5. (The k/d recovery table for blind probe subsets is an
     identity for random subsets, printed as such, not graded.)
  P4 temporal nonstationarity. P_C is a process: over six successive node
     sets written 10 minutes apart, with the same D_uniform targets, the
     staleness price L1(first spectrum, last spectrum) is >= 3x the sampling
     noise floor (L1 between two independent D_uniform draws on the last node
     set), and the read depth moves by >= 0.5 bit. Non-claim: no mechanism is
     named (P4 names drift as mechanism only where the staleness channel is
     shown to dominate, which this shakedown does not attempt).
  P5 metric consequence. For random 1-5 bit perturbations delta,
     Spearman(delta' P delta, graded damage) >= 0.5, the graded consumer being
     the change in shared prefix between the target and its nearest node; the
     selection consumer (did the nearest node change) is printed beside it at
     equal prominence and is predicted to correlate less (P5 excludes
     selection consumers); and perturbations confined to the kernel change the
     routing decision in <= 0.2% of trials (P5's floor: silence, never
     confident error).

Usage (on Atlas):
  PYTHONPATH=<turboquant-pro>/plugins/tqp-dht python ot_dht_shakedown.py \\
      --observe /archive/tqp-dht/observe --freeze /archive/tqp-dht/frozen \\
      --out ot_dht_result.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import sys
import time

import numpy as np
from tqp_dht import observe as O

SEED = 20260929
N_TARGETS = 512
DUMPS = 6


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load(directory):
    meta = json.load(open(os.path.join(directory, "meta.json")))
    raw = open(os.path.join(directory, "nodes.bin"), "rb").read()
    ids = [raw[i : i + 20] for i in range(0, len(raw), 20)]
    tg = [json.loads(x) for x in open(os.path.join(directory, "targets.jsonl"))]
    return meta, O.pack(ids), tg


def freeze(src, dst_root, meta):
    """Copy one dump and check the copy against its own meta record: the
    daemon rewrites every 10 minutes, so a copy taken across a rewrite is
    retried, never used."""
    for _ in range(10):
        dst = os.path.join(dst_root, f"{int(meta['t'])}")
        os.makedirs(dst, exist_ok=True)
        for f in ("meta.json", "nodes.bin", "targets.jsonl"):
            shutil.copy2(os.path.join(src, f), dst)
        meta = json.load(open(os.path.join(dst, "meta.json")))
        if sha(os.path.join(dst, "nodes.bin")) == meta["nodes_sha256"]:
            return dst
        time.sleep(2)
    raise SystemExit("could not copy a whole dump in ten tries")


def wait_new(src, after_t, timeout_s=1800):
    end = time.time() + timeout_s
    while time.time() < end:
        try:
            m = json.load(open(os.path.join(src, "meta.json")))
            if m["t"] > after_t:
                return m
        except (OSError, ValueError):
            pass
        time.sleep(20)
    raise SystemExit("no new dump within the wait: the daemon is not writing")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--observe", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    rng = np.random.default_rng(SEED)
    res = {"instrument_sha256": sha(O.__file__), "seed": SEED, "grades": {}}

    meta = json.load(open(os.path.join(args.observe, "meta.json")))
    first = freeze(args.observe, args.freeze, meta)
    meta, nodes, tg = load(first)
    n = len(nodes)
    ours = O.pack([bytes.fromhex(meta["our_ids"][0])])[0]
    res["substrate"] = {"n_nodes": n, "nodes_sha256": meta["nodes_sha256"],
                        "t": meta["t"], "log2_n": math.log2(n)}  # fmt: skip

    d_uni = O.random_ids(rng, N_TARGETS)
    d_self = O.near(rng, ours, N_TARGETS, 16)
    recent = [bytes.fromhex(x["target"]) for x in tg][-N_TARGETS:]
    d_traffic = O.pack(recent)
    t0 = time.time()
    spec = {k: O.read_spectrum(nodes, d) for k, d in
            (("uniform", d_uni), ("self", d_self), ("traffic", d_traffic))}  # fmt: skip
    res["spectra"] = {k: v.tolist() for k, v in spec.items()}
    res["seconds_for_three_spectra"] = time.time() - t0
    depth = {k: O.read_depth(v) for k, v in spec.items()}
    s = spec["uniform"]
    k = O.knee(s)
    lg = math.log2(n)
    res["P1"] = {"knee": k, "depth": depth, "read_before": float(s[: max(k - 4, 0)].min()
                 if k > 4 else float("nan")),
                 "read_after": float(s[k + 8:].max()) if k + 8 < 160 else 0.0}  # fmt: skip
    f = O.flip(nodes, d_uni, rng, keep=32)
    res["P1"]["flip"] = f
    res["grades"]["P1"] = bool(
        lg - 6 <= k <= lg + 2
        and res["P1"]["read_before"] >= 0.9
        and res["P1"]["read_after"] <= 0.05
        and f["routing"]["A_top"] >= 0.95
        and f["routing"]["B_bottom"] <= 0.05
    )
    res["P2"] = {"self_minus_uniform": depth["self"] - depth["uniform"],
                 "traffic_minus_uniform": depth["traffic"] - depth["uniform"],
                 "n_traffic_targets": len(recent)}  # fmt: skip
    res["grades"]["P2"] = bool(
        res["P2"]["self_minus_uniform"] >= 3 and res["P2"]["traffic_minus_uniform"] >= 1
    )
    r = int(np.sum(s >= 0.5))
    res["P3"] = {"d": O.D_BITS, "effective_rank": r, "d_over_r": O.D_BITS / max(r, 1),
                 "blind_budget_identity": O.blind_budget(s, rng)}  # fmt: skip
    res["grades"]["P3"] = bool(O.D_BITS / max(r, 1) >= 5)
    c = O.consequence(nodes, d_uni, s, rng)
    ks = c["kernel_silence"]
    res["P5"] = c
    res["grades"]["P5"] = bool(
        c["rho_graded"] is not None
        and c["rho_graded"] >= 0.5
        and (c["rho_selection"] is None or c["rho_selection"] < c["rho_graded"])
        and ks["trials"] > 0
        and ks["changed"] / ks["trials"] <= 0.002
    )
    json.dump(res, open(args.out, "w"), indent=1)  # P1-P3, P5 before the wait

    hist = [(meta["t"], s)]
    last_t = meta["t"]
    for _ in range(DUMPS - 1):
        m = wait_new(args.observe, last_t)
        d = freeze(args.observe, args.freeze, m)
        m, nd, _ = load(d)
        hist.append((m["t"], O.read_spectrum(nd, d_uni)))
        last_t = m["t"]
        res.setdefault("P4_node_sets", []).append(
            {"t": m["t"], "n_nodes": len(nd), "nodes_sha256": m["nodes_sha256"]}
        )
    floor = float(np.sum(np.abs(O.read_spectrum(nd, O.random_ids(rng, N_TARGETS))
                                - hist[-1][1])))  # fmt: skip
    st = O.staleness(hist)
    price = st[0]["l1_bits"]
    moved = abs(O.read_depth(hist[-1][1]) - O.read_depth(hist[0][1]))
    res["P4"] = {"staleness": st, "noise_floor_l1": floor, "price_l1": price,
                 "depth_moved": moved, "depths": [O.read_depth(x) for _, x in hist]}  # fmt: skip
    res["grades"]["P4"] = bool(price >= 3 * floor and moved >= 0.5)
    json.dump(res, open(args.out, "w"), indent=1)
    for p in ("P1", "P2", "P3", "P4", "P5"):
        print(p, "PASS" if res["grades"][p] else "FAIL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
