"""XPROTO-QUOTE graded runner -- bars per PREREG-XPROTO-QUOTE.md. Coded
cooling-off + refuses to seal on the synthetic model (mode "sim"): a sealed run
needs real tick data, as the CSI cell needs real NR and CCA needs SDR hardware.

    python3 quote_check.py --check-family   # pre-seal record check (any mode)
    python3 quote_check.py                    # graded run (needs seal + real ticks)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-QUOTE.md")
FAMILY_CONSTRUCTED = date(2026, 8, 23)
GRADED_SEEDS = [20260824, 20260825, 20260826]

# ---- sealed bars (must match the prereg verbatim) --------------------
B1_NAIVE_FC = 0.25         # stale quote vacuous (adverse selection >> target)
B2_WITNESSED_FC = 0.10     # price-triggered re-quote holds
B3_DOMINANCE = 2.0         # witnessed <= naive / 2
MC1_DEV_OVER_SPREAD = 0.5  # the mid drifts a real fraction of the spread (aging real)
MC2_FRESH_FC = 0.10        # a fresh quote is sane
MC3_MIN_STEPS = 5000


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-QUOTE.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(c: dict) -> dict:
    nf, wf = c["naive_fc"], c["witnessed_fc"]
    return {
        "B1": nf >= B1_NAIVE_FC,
        "B2": wf <= B2_WITNESSED_FC,
        "B3": wf <= nf / B3_DOMINANCE,
        "MC1": c["mean_dev_over_spread"] >= MC1_DEV_OVER_SPREAD,
        "MC2": c["fresh_fc"] <= MC2_FRESH_FC,
        "MC3": c["n_steps"] >= MC3_MIN_STEPS and c["n_requotes"] >= 1
        and c["naive_tight"] > c["naive_wide"],
    }


def report(cells: list[dict], label: str) -> dict:
    if any(c.get("mode") == "sim" for c in cells):
        sys.exit("REFUSED: sealed grading requires real tick data; the "
                 "efficient-price model validates the phenomenon only.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: naive_fc={g['naive_fc']} witnessed_fc={g['witnessed_fc']} "
              f"fresh_fc={g['fresh_fc']} tight/wide={g['naive_tight']}/{g['naive_wide']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "QUOTEREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required; sim allowed here):", flush=True)
        # phenomenon check tolerates sim (validation); only sealed grading refuses it
        cells = rec["cells"]
        graded = [{**c, "grade": grade(c)} for c in cells]
        keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
        agg = {k: all(g["grade"][k] for g in graded) for k in keys}
        ok = all(agg.values())
        for g in graded:
            gr = g["grade"]
            print(f"  seed {g['seed']}: naive_fc={g['naive_fc']} witnessed_fc={g['witnessed_fc']} "
                  f"fresh_fc={g['fresh_fc']} tight/wide={g['naive_tight']}/{g['naive_wide']} -> "
                  + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
        print(f"family record vs bars: {'PASS' if ok else 'FAIL'} "
              f"(B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
              f"MCs {all(agg[k] for k in ('MC1','MC2','MC3'))})", flush=True)
        sys.exit(0 if ok else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "QUOTEREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: QUOTEREP-graded-raw.json missing -- run fam_quote.py "
                 "on real ticks: --seeds 20260824 20260825 20260826 (mode ticks).")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    if sorted(c["seed"] for c in cells) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-QUOTE graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-QUOTE")
    out.update({"cell": "XPROTO-QUOTE", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-QUOTE-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
