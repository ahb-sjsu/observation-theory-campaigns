"""XPROTO-CSI-FLIP graded runner -- bars per PREREG-XPROTO-CSI-FLIP.md. Coded
cooling-off + real-substrate guard.

    python3 csiflip_check.py --check-family
    python3 csiflip_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-CSI-FLIP.md")
FAMILY_CONSTRUCTED = date(2026, 8, 26)
GRADED_SEEDS = [20260827, 20260828, 20260829]

B1_M_GAP = 0.08
B2_S_GAP = 0.06
MC2_TOL = 0.01


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CSI-FLIP.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    fcs = [c["fc_M_A"], c["fc_M_B"], c["fc_S_A"], c["fc_S_B"]]
    return {
        "B1": c["fc_M_B"] - c["fc_M_A"] >= B1_M_GAP,
        "B2": c["fc_S_A"] - c["fc_S_B"] >= B2_S_GAP,
        "B3": bool(c["flip"]),
        "MC1": not c["null_flip"],
        "MC2": abs(c["mean_margin_A"] - c["mean_margin_B"]) <= MC2_TOL,
        "MC3": all(0.0 < v < 1.0 for v in fcs),
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
        gr = g["grade"]
        print(f"  seed {g['seed']}: M A={g['fc_M_A']} B={g['fc_M_B']} | "
              f"S A={g['fc_S_A']} B={g['fc_S_B']} | flip={g['flip']} "
              f"null holds={not g['null_flip']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "CSIFLIPREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "CSIFLIPREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: CSIFLIPREP-graded-raw.json missing -- run fam_csiflip.py "
                 "--seeds 20260827 20260828 20260829 on Atlas first.")
    rec = json.load(open(raw, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-CSI-FLIP graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec["cells"], "XPROTO-CSI-FLIP")
    out.update({"cell": "XPROTO-CSI-FLIP", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-CSI-FLIP-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
