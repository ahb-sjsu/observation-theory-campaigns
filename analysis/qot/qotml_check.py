"""XPROTO-QOT Result 2 (F-QOTML) graded runner -- bars per PREREG-XPROTO-QOT-ML.md.
Coded cooling-off. Substrate = GNPy GSNR + sklearn (run in the qot venv, numpy<2).

    python3 qotml_check.py --check-family
    python3 qotml_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-QOT-ML.md")
FAMILY_CONSTRUCTED = date(2026, 8, 24)
GRADED_SEEDS = [20260825, 20260826, 20260827]

B1_FC_MSE = 0.03          # the average-error estimator materially false-clears at the cliff
B2_FC_AWARE = 0.03        # the consumer-aware objective holds
B3_DOMINANCE = 2.0        # fc_aware <= fc_mse / 2
MC2_CAP_RATIO = 0.90      # aware keeps comparable capacity (not degenerate conservatism)


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-QOT-ML.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c):
    return {"B1": c["fc_mse"] >= B1_FC_MSE, "B2": c["fc_aware"] <= B2_FC_AWARE,
            "B3": c["fc_aware"] <= c["fc_mse"] / B3_DOMINANCE,
            "MC1": c["mae_mse"] < c["mae_aware"],                    # MSE wins reconstruction
            "MC2": c["bps_aware"] >= MC2_CAP_RATIO * c["bps_mse"],   # comparable capacity
            "MC3": c["n_test"] >= 100}


def report(cells, label):
    if any("gnpy" not in c.get("mode", "") for c in cells):
        sys.exit("REFUSED: sealed grading requires the GNPy substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: MAE mse={g['mae_mse']} aware={g['mae_aware']} | "
              f"FC mse={g['fc_mse']} aware={g['fc_aware']} | bps mse={g['bps_mse']} "
              f"aware={g['bps_aware']} -> " + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys),
              flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; MCs {mcs})",
          flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "QOTMLREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "QOTMLREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: QOTMLREP-graded-raw.json missing -- run fam_qotml.py in the qot "
                 "venv for seeds 20260825-27 first.")
    rec = json.load(open(raw, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-QOT-ML graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec["cells"], "XPROTO-QOT-ML")
    out.update({"cell": "XPROTO-QOT-ML", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-QOT-ML-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
