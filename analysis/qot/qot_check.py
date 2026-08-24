"""XPROTO-QOT graded runner -- bars per PREREG-XPROTO-QOT.md. Coded cooling-off.
Substrate = GNPy (the optical-networking-standard GN-model QoT engine); like the
Sionna cellular cells this is the evidence rung, with a fibre testbed / field
pre-FEC BER as the external-validity graduation.

    python3 qot_check.py --check-family
    python3 qot_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-QOT.md")
FAMILY_CONSTRUCTED = date(2026, 8, 24)
GRADED_SEEDS = [20260825, 20260826, 20260827]

B1_NAIVE = 0.25            # QoT cert (ref loading) false-clears under full loading
B2_AWARE = 0.10            # footprint-aware cert holds
B3_DOMINANCE = 2.0
MC1_PENALTY = 0.5          # the certificate genuinely ages: real loading penalty (dB)
MC2_SPREAD = 0.10          # false-clears are footprint-relative (both clears + fails exist)
MC3_MIN_PATHS = 30
MC3_MIN_BPS = 2.0          # aware delivers real capacity (not degenerate all-fail/all-QPSK)


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-QOT.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    return {"B1": c["naive_fc"] >= B1_NAIVE, "B2": c["aware_fc"] <= B2_AWARE,
            "B3": c["aware_fc"] <= c["naive_fc"] / B3_DOMINANCE,
            "MC1": c["mean_loading_penalty_db"] >= MC1_PENALTY,
            "MC2": c["fc_spread"] >= MC2_SPREAD,
            "MC3": c["n_paths"] >= MC3_MIN_PATHS and c["mean_bits_per_symbol_aware"] >= MC3_MIN_BPS}


def report(cells, label):
    if any(not c.get("mode","").startswith("gnpy") for c in cells):
        sys.exit("REFUSED: sealed grading requires the GNPy substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: naive_fc={g['naive_fc']} aware_fc={g['aware_fc']} "
              f"penalty={g['mean_loading_penalty_db']}dB spread={g['fc_spread']} "
              f"bps={g['mean_bits_per_symbol_aware']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "QOTREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "QOTREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: QOTREP-graded-raw.json missing -- run fam_qot.py --seeds "
                 "20260825 20260826 20260827 --out QOTREP-graded-raw.json first.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    if sorted(c["seed"] for c in cells) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-QOT graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-QOT")
    out.update({"cell": "XPROTO-QOT", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-QOT-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
