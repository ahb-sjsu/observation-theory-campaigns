"""XPROTO-PGX graded runner — bars per PREREG-XPROTO-PGX.md. Reuses the
family's measurement (fam_pgx.run_cell) unchanged; runs on seeds DISJOINT
from the shakedown's {0,1,2}. Refuses to grade unless the prereg is
SEALED with a date >= one day after family construction (2026-08-20) --
the cooling-off is a code guard.

    python3 pgx_check.py                  # graded run (needs seal)
    python3 pgx_check.py --check-family   # pre-seal record check only
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

PREREG = os.path.join(HERE, "PREREG-XPROTO-PGX.md")
FAMILY_CONSTRUCTED = date(2026, 8, 20)
GRADED_SEEDS = [20260821, 20260822, 20260823]

# ---- the sealed bars (must match the prereg verbatim) ----------------
# Production regime: bars set slightly looser than the XPROTO-PG lab twin
# (0.25 / 0.10 / 3x), because measured footprints + emergent netem lag
# add noise the clean lab did not have. Each is justified in the prereg;
# all are validated against the family record (--check-family) before any
# seal.
B1_NAIVE_MINMAX = 0.20     # no threshold serves both consumers
B2_AWARE_MAX = 0.12        # witness correct in both directions
B3_DOMINANCE = 2.5         # witness beats naive best by >= 2.5x
MC1_INTERIOR = (0.15, 0.85)  # HOT truth-stale fraction
MC3_MIN_WRITES = (100, 8)    # orders (hot), catalog (cold)
MC3_LAG_BITE = 0.5           # max busy lag >= 0.5s (emergent lag realized)
MC3_LAG_STD = 0.10           # lag actually VARIED (uncontrolled, not a knob)
# MC4: the derived footprints must equal the intended relations — this
# guards the production footprint-derivation mechanism itself.
INTENDED = {"HOT": ["order_items", "orders"], "COLD": ["catalog", "category"]}


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-PGX.md is not SEALED.")
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
    ts = cell["truth_stale_frac"]
    fp = cell["footprints"]
    return {
        "B1": mm >= B1_NAIVE_MINMAX,
        "B2": am <= B2_AWARE_MAX,
        "B3": am <= mm / B3_DOMINANCE,
        "MC1": MC1_INTERIOR[0] <= ts["HOT"] <= MC1_INTERIOR[1],
        "MC2": ts["COLD"] < ts["HOT"],
        "MC3": (cell["writes"]["orders"] >= MC3_MIN_WRITES[0]
                and cell["writes"]["catalog"] >= MC3_MIN_WRITES[1]
                and cell["max_busy_lag"] >= MC3_LAG_BITE
                and cell["lag_std"] >= MC3_LAG_STD),
        "MC4": (sorted(fp["HOT"]) == INTENDED["HOT"]
                and sorted(fp["COLD"]) == INTENDED["COLD"]),
    }


def report(cells: list[dict], label: str) -> dict:
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3", "MC4")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs_ok = all(agg[k] for k in ("MC1", "MC2", "MC3", "MC4"))
    bars_ok = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars_ok else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: minmax={g['naive_minmax']} "
              f"aware={g['aware_max']} staleHOT={g['truth_stale_frac']['HOT']} "
              f"fp={g['footprints']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys),
              flush=True)
    print(f"{label}: {verdict} "
          f"(B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs_ok})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record",
                    default=os.path.join(HERE, "PGXREP-family.json"))
    args = ap.parse_args()

    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)

    seal_date = require_seal()
    import fam_pgx as fam  # psycopg needed only here
    print(f"XPROTO-PGX graded — sealed {seal_date}, seeds {GRADED_SEEDS}",
          flush=True)
    cells = []
    for seed in GRADED_SEEDS:
        print(f"cell seed {seed}…", flush=True)
        cells.append(fam.run_cell(seed))
    out = report(cells, "XPROTO-PGX")
    out.update({"cell": "XPROTO-PGX", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS,
                "constants_from": "fam_pgx.py (sealed grid)"})
    path = os.path.join(HERE, "XPROTO-PGX-graded.json")
    json.dump(out, open(path, "w"), indent=1)
    print(f"-> {path}", flush=True)


if __name__ == "__main__":
    main()
