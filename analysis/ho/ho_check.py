"""XPROTO-HO graded runner — bars per PREREG-XPROTO-HO.md. Coded cooling-off
+ real-NR-substrate guard. Mirrors csi_check / beam_check / aicsi_check.

    python3 ho_check.py --check-family   # pre-seal record check
    python3 ho_check.py                   # graded run (needs seal + NR record)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG-XPROTO-HO.md")
FAMILY_CONSTRUCTED = date(2026, 8, 22)
GRADED_SEEDS = [20260823, 20260824, 20260825]

# ---- sealed bars (must match the prereg verbatim) --------------------
B1_NAIVE_BLER = 0.25       # stale RSRP report vacuous under mobility
B2_RLM_BLER = 0.15         # RLM-witnessed re-selection holds
B3_DOMINANCE = 2.0         # rlm <= naive / 2
MC1_HO_LAG = 0.10          # mobility causes real serving-vs-best mismatch
MC2_FRESH_BLER = 0.15      # best-cell serving is sane
MC3_MIN_SLOT = 5000
MC3_MIN_HO = 1             # handovers actually happen


def require_seal() -> date:
    t = open(PREREG, encoding="utf-8").read()
    if "STATUS: UNSEALED" in t or "STATUS: SEALED" not in t:
        sys.exit("REFUSED: PREREG-XPROTO-HO.md is not SEALED.")
    m = re.search(r"STATUS: SEALED (\d{4})-(\d{2})-(\d{2})", t)
    if not m:
        sys.exit("REFUSED: seal carries no parseable date.")
    d = date(int(m[1]), int(m[2]), int(m[3]))
    if (d - FAMILY_CONSTRUCTED).days < 1:
        sys.exit(f"REFUSED: cooling-off — seal {d} not >= 1 day after "
                 f"family construction {FAMILY_CONSTRUCTED}.")
    return d


def grade(c: dict) -> dict:
    nb, rb = c["naive_bler"], c["rlm_bler"]
    return {
        "B1": nb >= B1_NAIVE_BLER,
        "B2": rb <= B2_RLM_BLER,
        "B3": rb <= nb / B3_DOMINANCE,
        "MC1": c["ho_lag_frac"] >= MC1_HO_LAG,
        "MC2": c["fresh_bler"] <= MC2_FRESH_BLER,
        "MC3": c["n_slot"] >= MC3_MIN_SLOT and c["n_ho"] >= MC3_MIN_HO,
    }


def report(cells: list[dict], label: str) -> dict:
    if any(c.get("mode") == "sim" for c in cells):
        sys.exit("REFUSED: sealed grading requires the real NR substrate.")
    graded = [{**c, "grade": grade(c)} for c in cells]
    keys = ("B1", "B2", "B3", "MC1", "MC2", "MC3")
    agg = {k: all(g["grade"][k] for g in graded) for k in keys}
    mcs_ok = all(agg[k] for k in ("MC1", "MC2", "MC3"))
    bars = agg["B1"] and agg["B2"] and agg["B3"]
    verdict = "VOID" if not mcs_ok else ("PASS" if bars else "FAIL")
    for g in graded:
        gr = g["grade"]
        print(f"  seed {g['seed']}: naive_bler={g['naive_bler']} rlm_bler={g['rlm_bler']} "
              f"fresh_bler={g['fresh_bler']} ho_lag={g['ho_lag_frac']} -> "
              + " ".join(f"{k}:{'ok' if gr[k] else 'X'}" for k in keys), flush=True)
    print(f"{label}: {verdict} (B1 {agg['B1']}, B2 {agg['B2']}, B3 {agg['B3']}; "
          f"MCs {mcs_ok})", flush=True)
    return {"cells": graded, "aggregate": agg, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-family", action="store_true")
    ap.add_argument("--family-record", default=os.path.join(HERE, "HOREP-family.json"))
    args = ap.parse_args()
    if args.check_family:
        rec = json.load(open(args.family_record, encoding="utf-8"))
        print("pre-seal record check (no seal required):", flush=True)
        out = report(rec["cells"], "family record vs bars")
        sys.exit(0 if out["verdict"] == "PASS" else 1)
    seal_date = require_seal()
    raw = os.path.join(HERE, "HOREP-graded-raw.json")
    if not os.path.exists(raw):
        sys.exit("REFUSED: HOREP-graded-raw.json missing — run on Atlas GPU "
                 "first: fam_ho.py --seeds 20260823 20260824 20260825 "
                 "--out HOREP-graded-raw.json.")
    rec = json.load(open(raw, encoding="utf-8"))
    cells = rec["cells"]
    seeds = sorted(c["seed"] for c in cells)
    if seeds != sorted(GRADED_SEEDS):
        sys.exit(f"REFUSED: graded seeds {seeds} != prereg {sorted(GRADED_SEEDS)}.")
    if any(c.get("mode") != "nrsionna_ho" for c in cells):
        sys.exit("REFUSED: sealed grading requires mode nrsionna_ho.")
    print(f"XPROTO-HO graded — sealed {seal_date}, seeds {GRADED_SEEDS}", flush=True)
    out = report(cells, "XPROTO-HO")
    out.update({"cell": "XPROTO-HO", "sealed": str(seal_date), "seeds": GRADED_SEEDS})
    json.dump(out, open(os.path.join(HERE, "XPROTO-HO-graded.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
