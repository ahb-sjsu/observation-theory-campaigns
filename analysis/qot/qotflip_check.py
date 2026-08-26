"""XPROTO-QOT-FLIP graded runner -- bars per PREREG-XPROTO-QOT-FLIP.md. Coded
cooling-off + GNPy-substrate guard.

    python3 qotflip_check.py --check-family
    python3 qotflip_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-QOT-FLIP.md")
FAMILY_CONSTRUCTED = date(2026, 8, 26)
GRADED_SEEDS = [20260827, 20260828, 20260829]

B1_R_GAP = 0.15
B2_P_GAP = 0.10
MC2_MARGIN_TOL = 0.001


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-QOT-FLIP.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    fps = [c["fp_fc_R_A"], c["fp_fc_R_B"], c["fp_fc_P_A"], c["fp_fc_P_B"]]
    return {
        "B1": c["fp_fc_R_B"] - c["fp_fc_R_A"] >= B1_R_GAP,
        "B2": c["fp_fc_P_A"] - c["fp_fc_P_B"] >= B2_P_GAP,
        "B3": bool(c["fp_flip"]),
        "MC1": not c["fec_flip"],
        "MC2": abs(c["fp_mean_margin_A"] - c["fp_mean_margin_B"]) <= MC2_MARGIN_TOL,
        "MC3": all(0.0 < v < 1.0 for v in fps),
    }


def report(cells, label):
    if any(not c.get("mode", "").startswith("gnpy") for c in cells):
        sys.exit("REFUSED: sealed grading requires the GNPy substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: R A={g['fp_fc_R_A']} B={g['fp_fc_R_B']} | "
              f"P A={g['fp_fc_P_A']} B={g['fp_fc_P_B']} | flip={g['fp_flip']} "
              f"fec_null={not g['fec_flip']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "QOTFLIPREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "QOTFLIPREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: QOTFLIPREP-graded-raw.json missing -- run fam_qotflip.py "
                 "--seeds 20260827 20260828 20260829 first (qot venv).")
    rec = json.load(open(raw, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-QOT-FLIP graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec["cells"], "XPROTO-QOT-FLIP")
    out.update({"cell": "XPROTO-QOT-FLIP", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-QOT-FLIP-graded.json"), "w"), indent=1)


if __name__ == "____main__" or __name__ == "__main__":
    main()
