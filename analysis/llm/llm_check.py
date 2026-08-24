"""XPROTO-LLM graded runner -- bars per PREREG-XPROTO-LLM.md. Coded cooling-off.
Substrate = a REAL pretrained MNLI model on REAL MNLI (benchmark) + HANS
(deployment). The evidence rung; production traffic / incident logs are the
external-validity graduation.

    python3 llm_check.py --check-family
    python3 llm_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-LLM.md")
FAMILY_CONSTRUCTED = date(2026, 8, 24)
GRADED_SEEDS = [20260825, 20260826, 20260827]

B1_NAIVE = 0.25            # benchmark-certified model false-clears on deployment slices
B2_AWARE = 0.10            # footprint-aware evaluation holds
B3_DOMINANCE = 2.0
MC2_SPREAD = 0.15          # consumer-relativity: per-slice accuracy genuinely varies
MC3_MIN_CONSUMERS = 20


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-LLM.md is not SEALED.")
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
            "MC1": c["certified"],                                   # model passes the benchmark
            "MC2": c["consumer_acc_spread"] >= MC2_SPREAD,          # consumer-relative
            "MC3": c["n_consumers"] >= MC3_MIN_CONSUMERS and 0 < c["naive_fc"] < 1.0}


def report(cells, label):
    if any("mnli" not in c.get("mode", "") for c in cells):
        sys.exit("REFUSED: sealed grading requires the real MNLI/HANS substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: bench_acc={g['benchmark_acc']} (cert={g['certified']}) "
              f"naive_fc={g['naive_fc']} aware_fc={g['aware_fc']} spread={g['consumer_acc_spread']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "LLMREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "LLMREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: LLMREP-graded-raw.json missing -- run fam_llm.py --seeds "
                 "20260825 20260826 20260827 --out LLMREP-graded-raw.json first.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    if sorted(c["seed"] for c in cells) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-LLM graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-LLM")
    out.update({"cell": "XPROTO-LLM", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-LLM-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
