"""XPROTO-URLLC-SNR graded runner -- bars per PREREG-XPROTO-URLLC-SNR.md. Coded
cooling-off + real-substrate guard.

    python3 urllc_snr_check.py --check-family
    python3 urllc_snr_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-URLLC-SNR.md")
FAMILY_CONSTRUCTED = date(2026, 8, 25)
GRADED_SEEDS = [20260826, 20260827, 20260828]

B1_NAIVE_MIN = 0.05        # URLLC false-clear >= 50x its target at every in-range SNR
B2_AWARE_MAX = 1e-3        # aware holds at target across the operating range
B3_NAIVE_21 = 0.03         # gap never closes at cell centre (>= 30x)
MC1_EDGE_EMBB = 0.15       # cell-edge eMBB breakdown (> 1.5x eMBB target)
MC2_CENTRE_EMBB = 0.15     # sane at cell centre
IN_RANGE = ("9", "12", "15", "18")


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-URLLC-SNR.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    sw = c["sweep"]
    naive_in = [sw[m]["urllc_naive"] for m in IN_RANGE]
    aware_in = [sw[m]["urllc_aware"] for m in IN_RANGE]
    return {
        "B1": min(naive_in) >= B1_NAIVE_MIN,
        "B2": max(aware_in) <= B2_AWARE_MAX,
        "B3": sw["21"]["urllc_naive"] >= B3_NAIVE_21,
        "MC1": sw["3"]["embb"] >= MC1_EDGE_EMBB,
        "MC2": sw["15"]["embb"] <= MC2_CENTRE_EMBB and sw["18"]["embb"] <= MC2_CENTRE_EMBB,
        "MC3": len(c["snr_grid_db"]) >= 5,
    }


def report(cells, label):
    if any(c.get("mode") != "nrsionna" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real NR substrate (mode nrsionna).")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        sw = g["sweep"]; gr = g["grade"]
        print(f"  seed {g['seed']}: un@12={sw['12']['urllc_naive']} ua@12={sw['12']['urllc_aware']} "
              f"embb@3={sw['3']['embb']} embb@18={sw['18']['embb']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "URLLCSNRREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "URLLCSNRREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: URLLCSNRREP-graded-raw.json missing -- run fam_urllc_snr.py "
                 "on Atlas for seeds 20260826-28 first.")
    rec = json.load(open(raw, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-URLLC-SNR graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec["cells"], "XPROTO-URLLC-SNR")
    out.update({"cell": "XPROTO-URLLC-SNR", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-URLLC-SNR-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
