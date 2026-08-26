"""XPROTO-CSI-CTRL graded runner -- bars per PREREG-XPROTO-CSI-CTRL.md. Coded cooling-off
+ real-substrate guard.

    python3 csi_ctrl_check.py --check-family
    python3 csi_ctrl_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-CSI-CTRL.md")
FAMILY_CONSTRUCTED = date(2026, 8, 25)
GRADED_SEEDS = [20260826, 20260827, 20260828]

B1_SOD_MAX = 0.16
B2_OH_MAX = 0.5
B2_BLER_RATIO = 1.4
B3_FIXED40_MIN = 0.20
MC1_OH_RATIO = 3.0
MC2_LO, MC2_HI = 0.1, 0.4
MC3_FIXED1_MAX = 0.14


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CSI-CTRL.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    sw = c["sweep"]
    inr = ("10", "25", "50", "100", "200", "400")
    return {
        "B1": max(sw[f]["sod"]["bler"] for f in inr) <= B1_SOD_MAX,
        "B2": sw["25"]["sod"]["overhead"] <= B2_OH_MAX
        and sw["25"]["sod"]["bler"] <= B2_BLER_RATIO * sw["25"]["fixed1"]["bler"],
        "B3": sw["100"]["fixed40"]["bler"] >= B3_FIXED40_MIN,
        "MC1": sw["400"]["sod"]["overhead"] >= MC1_OH_RATIO * sw["10"]["sod"]["overhead"],
        "MC2": all(MC2_LO <= sw[f]["sod"]["p_eff"] / sw[f]["tcoh_ms"] <= MC2_HI
                   for f in ("10", "25", "50")),
        "MC3": max(sw[f]["fixed1"]["bler"] for f in sw) <= MC3_FIXED1_MAX,
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
        k = sw["25"]["sod"]["p_eff"] / sw["25"]["tcoh_ms"]
        print(f"  seed {g['seed']}: SoD bler@200={sw['200']['sod']['bler']} "
              f"oh@25={sw['25']['sod']['overhead']} Peff/Tcoh@25={k:.2f} "
              f"fixed40@100={sw['100']['fixed40']['bler']} -> "
              + " ".join(f"{x}:{'ok' if gr[x] else 'X'}" for x in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "CTRLREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "CTRLREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: CTRLREP-graded-raw.json missing -- run fam_csi_ctrl.py on Atlas "
                 "for seeds 20260826-28 first.")
    rec = json.load(open(raw, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-CSI-CTRL graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec["cells"], "XPROTO-CSI-CTRL")
    out.update({"cell": "XPROTO-CSI-CTRL", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-CSI-CTRL-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
