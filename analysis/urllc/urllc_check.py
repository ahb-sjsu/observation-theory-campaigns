"""XPROTO-URLLC graded runner -- bars per PREREG-XPROTO-URLLC.md. Coded
cooling-off + real-NR-substrate guard. Mirrors the other cell checkers.

    python3 urllc_check.py --check-family
    python3 urllc_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-URLLC.md")
FAMILY_CONSTRUCTED = date(2026, 8, 23)
GRADED_SEEDS = [20260824, 20260825, 20260826]

# ---- sealed bars (must match the prereg verbatim) --------------------
B1_NAIVE_FACTOR = 30.0     # naive achieved >= 30x URLLC target (cert vacuous for URLLC)
B2_AWARE_MAX = 1e-3        # consumer-aware holds URLLC at its target
B3_DOMINANCE = 30.0        # aware <= naive / 30
MC1_EMBB_MAX = 0.15        # the SAME cert serves eMBB fine (<= 1.5x its 0.1 target)
MC2_MIN_MARGIN = 1.0       # the two consumers genuinely need different MCS
MC3_MIN_TTI = 5000
MC3_MIN_MCSVAR = 2


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-URLLC.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after "
                 f"{FAMILY_CONSTRUCTED}.")
    return d


def grade(c: dict) -> dict:
    return {
        "B1": c["achieved_urllc_naive"] >= B1_NAIVE_FACTOR * c["urllc_target"],
        "B2": c["achieved_urllc_aware"] <= B2_AWARE_MAX,
        "B3": c["achieved_urllc_aware"] <= c["achieved_urllc_naive"] / B3_DOMINANCE,
        "MC1": c["achieved_embb"] <= MC1_EMBB_MAX,
        "MC2": c["mcs_margin"] >= MC2_MIN_MARGIN,
        "MC3": c["n_tti"] >= MC3_MIN_TTI and c["mcs_var"] >= MC3_MIN_MCSVAR,
    }


def report(cells, label):
    if any(c.get("mode") != "nrsionna" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real NR substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: eMBB={g['achieved_embb']:.4f} "
              f"URLLC naive={g['achieved_urllc_naive']:.4f} aware={g['achieved_urllc_aware']:.2e} "
              f"margin={g['mcs_margin']:.2f} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "URLLCREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "URLLCREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: URLLCREP-graded-raw.json missing -- run fam_urllc.py "
                 "--seeds 20260824 20260825 20260826 --out URLLCREP-graded-raw.json on Atlas.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    if sorted(c["seed"] for c in cells) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-URLLC graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-URLLC")
    out.update({"cell": "XPROTO-URLLC", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-URLLC-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
