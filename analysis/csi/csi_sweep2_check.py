"""XPROTO-CSI-SWEEP2 graded runner -- bars per PREREG-XPROTO-CSI-SWEEP2.md. Coded
cooling-off + real-substrate guard.

    python3 csi_sweep2_check.py --check-family
    python3 csi_sweep2_check.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-CSI-SWEEP2.md")
FAMILY_CONSTRUCTED = date(2026, 8, 26)
GRADED_SEEDS = [20260827, 20260828, 20260829]

HIGH_FDS = ["50", "100", "200", "400"]
B2_HIGH_MAX = 2
B3_LOW_MIN, B3_LOW_MAX = 1, 6
B4_SLOPE_MAX = 0.14
MC2_TOL = 0.01
MC3_CONSTANTS = {"cal_margin": 0.09, "cal_seed": 999, "ntti": 12000}


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-CSI-SWEEP2.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off -- seal {d} not >= 1 day after {FAMILY_CONSTRUCTED}.")
    return d


def grade(c, constants):
    floors = {k: int(v) for k, v in c["floors_tti"].items()}
    fds_sorted = sorted(int(k) for k in floors)
    seq = [floors[str(fd)] for fd in fds_sorted]
    rows = c["bler_rows"]
    return {
        "B1": all(v <= 0.10 for v in c["fresh_bler"].values()),
        "B2": all(floors.get(fd, 99) <= B2_HIGH_MAX for fd in HIGH_FDS),
        "B3": B3_LOW_MIN <= floors.get("10", 0) <= B3_LOW_MAX,
        "B4": c["slope"] <= B4_SLOPE_MAX,
        "MC1": all(a >= b for a, b in zip(seq, seq[1:])),
        "MC2": all(r[-1] >= r[0] - MC2_TOL for r in rows.values()),
        "MC3": (c.get("mode") == "nrsionna"
                and constants.get("target") == 0.10
                and all(constants.get(k) == v for k, v in MC3_CONSTANTS.items())
                and constants.get("d_cal_db", 99) <= 4.0),
        "MC4": not c["censored_fds"],
    }


def report(rec, label):
    cells = rec["cells"]
    constants = {**rec["constants"], "target": rec.get("target")}
    if any(c.get("mode") != "nrsionna" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real NR substrate (mode nrsionna).")
    graded = [{**c, "grade": grade(c, constants)} for c in cells]
    keys = ("B1", "B2", "B3", "B4", "MC1", "MC2", "MC3", "MC4")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs = all(agg[k] for k in ("MC1", "MC2", "MC3", "MC4"))
    bars = all(agg[k] for k in ("B1", "B2", "B3", "B4"))
    verdict = "VOID" if not mcs else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: floors={g['floors_tti']} "
              f"censored={g['censored_fds']} slope={g['slope']} "
              f"fresh_worst={max(g['fresh_bler'].values())} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (" + ", ".join(f"{k} {agg[k]}" for k in keys[:4])
          + f"; MCs {mcs})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "CSISWEEP2REP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec, "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "CSISWEEP2REP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: CSISWEEP2REP-graded-raw.json missing -- run fam_csi_sweep2.py "
                 "--seeds 20260827 20260828 20260829 on Atlas first.")
    rec = json.load(open(raw, encoding="utf-8"))
    if sorted(c["seed"] for c in rec["cells"]) != sorted(GRADED_SEEDS):
        sys.exit("REFUSED: graded seeds mismatch prereg.")
    print(f"XPROTO-CSI-SWEEP2 graded -- sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(rec, "XPROTO-CSI-SWEEP2")
    out.update({"cell": "XPROTO-CSI-SWEEP2", "sealed": str(seal_date),
                "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-CSI-SWEEP2-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
