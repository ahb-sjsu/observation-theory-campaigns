"""XPROTO-MG graded runner — bars per PREREG-XPROTO-MG.md. Reuses the
family's measurement (fam_mongo.run_cell) unchanged; runs on seeds
DISJOINT from the shakedown's {0,1,2}. Refuses to grade unless the
prereg is SEALED with a date >= one day after family construction
(2026-08-20) -- the cooling-off is a code guard.

    python3 mongo_check.py                  # graded run (needs seal)
    python3 mongo_check.py --check-family   # pre-seal record check only

The pre-seal record check evaluates every bar against the committed
family record at enforcement granularity BEFORE sealing. It needs no
seal and moves no data.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PREREG = os.path.join(HERE, "PREREG-XPROTO-MG.md")
FAMILY_CONSTRUCTED = date(2026, 8, 20)
GRADED_SEEDS = [20260821, 20260822, 20260823]

# ---- the sealed bars (must match the prereg verbatim) ----------------
# Bound identical to the XPROTO-PG twin; validated against the family
# record with --check-family before any seal (a bar the F-MG record
# cannot pass does not get sealed).
B1_NAIVE_MINMAX = 0.25     # no threshold serves both consumers
B2_AWARE_MAX = 0.10        # witness correct in both directions
B3_DOMINANCE = 3.0         # witness beats naive best by >= 3x
MC1_INTERIOR = (0.20, 0.80)  # A truth-stale fraction
MC3_MIN_WRITES = (100, 10)   # hot_a, hot_b
MC3_LAG_BITE = 0.8           # max busy lag >= 0.8s (delay realized)


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-MG.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(cell: dict) -> dict:
    mm, am = cell["naive_minmax"], cell["aware_max"]
    tsA = cell["truth_stale_frac"]["A"]
    tsB = cell["truth_stale_frac"]["B"]
    return {
        "B1": mm >= B1_NAIVE_MINMAX,
        "B2": am <= B2_AWARE_MAX,
        "B3": am <= mm / B3_DOMINANCE,
        "MC1": MC1_INTERIOR[0] <= tsA <= MC1_INTERIOR[1],
        "MC2": tsB < tsA,
        "MC3": (cell["writes"]["hot_a"] >= MC3_MIN_WRITES[0]
                and cell["writes"]["hot_b"] >= MC3_MIN_WRITES[1]
                and cell["max_busy_lag"] >= MC3_LAG_BITE),
    }


def report(cells: list[dict], label: str) -> dict:
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs_ok = agg["MC1"] and agg["MC2"] and agg["MC3"]
    bars_ok = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars_ok else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: minmax={g['naive_minmax']} "
              f"aware={g['aware_max']} staleA={g['truth_stale_frac']['A']} "
              f"-> " + " ".join(f"{k}:{'ok' if gr[k] else 'X'}"
                                for k in keys), flush=True)
    print(f"{label}: {verdict} "
          f"(B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs_ok})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record",
                    default=os.path.join(HERE, "MGREP-family.json"))
    args = ap.parse_args()

    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)

    seal_date = require_seal()
    import fam_mongo as fam  # pymongo needed only here
    print(f"XPROTO-MG graded — sealed {seal_date}, seeds {GRADED_SEEDS}",
          flush=True)
    cells = []
    for seed in GRADED_SEEDS:
        print(f"cell seed {seed}…", flush=True)
        cells.append(fam.run_cell(seed))
    out = report(cells, "XPROTO-MG")
    out.update({"cell": "XPROTO-MG", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS,
                "constants_from": "fam_mongo.py (sealed grid)"})
    path = os.path.join(HERE, "XPROTO-MG-graded.json")
    json.dump(out, open(path, "w"), indent=1)
    print(f"-> {path}", flush=True)


if __name__ == "__main__":
    main()
