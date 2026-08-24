"""XPROTO-ZK graded runner -- bars per PREREG-XPROTO-ZK.md. Coded cooling-off +
real-substrate guard. Mirrors the other DB/cellular cell checkers.

    python3 zk_check.py --check-family   # pre-seal record check
    python3 zk_check.py                    # graded run (needs seal + zk record)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-ZK.md")
FAMILY_CONSTRUCTED = date(2026, 8, 23)
GRADED_SEEDS = [20260824, 20260825, 20260826]

# ---- sealed bars (must match the prereg verbatim) --------------------
B1_NAIVE_HOT = 0.25        # local-read certificate vacuous for the hot footprint
B2_WITNESSED = 0.10        # sync() barrier holds
B3_DOMINANCE = 2.0         # witnessed <= naive_hot / 2
MC1_ZXID_GAP = 2.0         # staleness is real (mean leader-follower zxid gap)
MC2_NAIVE_COLD = 0.10      # cold footprint on the SAME follower is fresh
                           # (follower sane; the staleness is consumer-relative)
MC3_MIN_READS = 500
MC3_MIN_WRITES = 200


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-ZK.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(c: dict) -> dict:
    nh, wt = c["naive_hot"], c["witnessed"]
    return {
        "B1": nh >= B1_NAIVE_HOT,
        "B2": wt <= B2_WITNESSED,
        "B3": wt <= nh / B3_DOMINANCE,
        "MC1": c["mean_zxid_gap"] >= MC1_ZXID_GAP,
        "MC2": c["naive_cold"] <= MC2_NAIVE_COLD,
        "MC3": c["n_reads"] >= MC3_MIN_READS and c["n_writes"] >= MC3_MIN_WRITES,
    }


def report(cells: list[dict], label: str) -> dict:
    if any(c.get("mode") != "zk" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real ZooKeeper substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs_ok = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: naive_hot={g['naive_hot']} naive_cold={g['naive_cold']} "
              f"witnessed={g['witnessed']} zxid_gap={g['mean_zxid_gap']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs_ok})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "ZKREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "ZKREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: ZKREP-graded-raw.json missing -- run on Atlas first: "
                 "bash lab_up.sh 200 && fam_zk.py --seeds 20260824 20260825 20260826 "
                 "--out ZKREP-graded-raw.json.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    seeds = sorted(c["seed"] for c in cells)
    if seeds != sorted(GRADED_SEEDS):
        sys.exit(f"REFUSED: graded seeds {seeds} != prereg {sorted(GRADED_SEEDS)}.")
    print(f"XPROTO-ZK graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-ZK")
    out.update({"cell": "XPROTO-ZK", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-ZK-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
