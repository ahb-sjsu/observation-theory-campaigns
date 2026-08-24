"""XPROTO-PHY graded runner (PMI/RI/TA) -- bars per PREREG-XPROTO-PHY.md.
Coded cooling-off + refuses to seal on the parametric model (mode "model"): the
sealed rung uses the real Sionna 5G NR LDPC curves (mode "nrsionna").

    python3 phy_check.py --check-family
    python3 phy_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-PHY.md")
FAMILY_CONSTRUCTED = date(2026, 8, 23)
GRADED_SEEDS = [20260824, 20260825, 20260826]

B1_NAIVE = 0.25
B2_WITNESSED = 0.15
B3_DOMINANCE = 2.0
MC1_AGING = 0.05          # the certificate genuinely ages (mode-agnostic floor)
MC2_FRESH = 0.15
MC3_MIN_TTI = 5000


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-PHY.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    nf, wf = c["naive_fc"], c["witnessed_fc"]
    return {"B1": nf >= B1_NAIVE, "B2": wf <= B2_WITNESSED, "B3": wf <= nf / B3_DOMINANCE,
            "MC1": c["aging"] >= MC1_AGING, "MC2": c["fresh_fc"] <= MC2_FRESH,
            "MC3": c["n_tti"] >= MC3_MIN_TTI and c["n_requotes"] >= 1}


def report(cells, label, allow_model):
    if not allow_model and any(c.get("mode") == "model" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real NR substrate (mode nrsionna).")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  {g['cell']:3s} seed {g['seed']}: naive_fc={g['naive_fc']} "
              f"witnessed_fc={g['witnessed_fc']} fresh_fc={g['fresh_fc']} "
              f"{g['aging_name']}={g['aging']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "PHYREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (model allowed):", flush=True)
        out = report(rec["cells"], "family record vs bars", allow_model=True)
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "PHYREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: PHYREP-graded-raw.json missing -- run fam_phy.py on the "
                 "real NR substrate for seeds 20260824-26 first.")
    rec = json.load(open(raw, encoding="utf-8"))
    print(f"XPROTO-PHY graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec["cells"], "XPROTO-PHY", allow_model=False)
    out.update({"cell": "XPROTO-PHY", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-PHY-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
