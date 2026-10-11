"""OP1 tolerances from the pilot, by the rules of PREREG-OP1 Section 5 (the D7v3 rules, with fixed limits):
  M1    = 0.5 x the pilot's pooled advantage, rounded down to 0.005, within [0.01, 0.10]
  TOL1  = 1.25 x the pilot's worst cell shortfall (0 if no cell is behind), rounded up to 0.01, within [0.05, 0.25]
  TOL_N = 1.5 x the pilot's largest change of the pooled advantage between its two resolutions (over viscosities),
          rounded up to 0.005, within [0.01, 0.05]
A limit that binds is named in the output, so a bar the pilot did not set is visible as such.

    python op1_fix_tols.py pilot.json --out tolerances.json
    python op1_fix_tols.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import sys

from op1_grade import cells, pooled

LIMITS = {"M1": (0.01, 0.10), "TOL1": (0.05, 0.25), "TOL_N": (0.01, 0.05)}


def fix(pilot: dict) -> dict:
    cs = cells(pilot); p = pooled(cs); short = max(0.0, -min(c["a"] for c in cs)); d = 0.0
    for nu in {c["nu"] for c in cs}:
        ns = sorted({c["n"] for c in cs if c["nu"] == nu})
        if len(ns) >= 2:
            d = max(d, abs(pooled([c for c in cs if c["nu"] == nu and c["n"] == ns[-1]]) - pooled([c for c in cs if c["nu"] == nu and c["n"] == ns[-2]])))
    raw = {"M1": math.floor(0.5 * p / 0.005) * 0.005, "TOL1": math.ceil(1.25 * short / 0.01 - 1e-9) * 0.01, "TOL_N": math.ceil(1.5 * d / 0.005 - 1e-9) * 0.005}
    out, bound = {}, {}
    for k, v in raw.items():
        lo, hi = LIMITS[k]; out[k] = round(min(max(v, lo), hi), 3)
        if out[k] != round(v, 3): bound[k] = "lower limit" if v < lo else "upper limit"
    return {**out, "limits_binding": bound, "pilot": {"pooled_advantage": p, "worst_shortfall": short, "max_change_between_resolutions": d, "n_cells": len(cs)},
            "rule": "PREREG-OP1 Section 5: M1 0.5x pooled (down to 0.005) in [0.01, 0.10]; TOL1 1.25x worst shortfall (up to 0.01) in [0.05, 0.25]; TOL_N 1.5x resolution change (up to 0.005) in [0.01, 0.05]"}


def selftest() -> int:
    def world(n, read):
        L = {l: {"NONE": {"E": 1.0}, **{str(r): {"READ": {"E": read}, "ENERGY": {"E": 0.6}, "BALL": {"E": 0.7}, "SENS": {"E": 0.6}, "POD": {"E": 0.6}, "RANDOM_median_E": 0.8} for r in (2, 4)}} for l in ("lin", "rff")}
        return {"name": f"w{n}", "nu": 0.02, "n": n, "cutoffs": {"3": {"ladder": [2, 4], "lifts": L}}}
    t = fix({"worlds": [world(96, 0.54), world(128, 0.57)]})  # advantages 0.10 and 0.05: pooled 0.075, change 0.05
    ok = t["M1"] == 0.035 and t["TOL1"] == 0.05 and t["TOL_N"] == 0.05 and t["limits_binding"] == {"TOL1": "lower limit", "TOL_N": "upper limit"}
    print("tolerances from a synthetic pilot:", {k: t[k] for k in ("M1", "TOL1", "TOL_N")}, t["limits_binding"], "PASS" if ok else "FAIL")
    t2 = fix({"worlds": [world(96, 0.63), world(128, 0.63)]})  # READ behind everywhere: the margin stays at its floor
    ok2 = t2["M1"] == 0.01 and t2["limits_binding"].get("M1") == "lower limit" and t2["TOL1"] == 0.07
    print("a pilot with READ behind keeps M1 at its floor:", {k: t2[k] for k in ("M1", "TOL1", "TOL_N")}, "PASS" if ok2 else "FAIL")
    print("SELFTEST", "PASS" if ok and ok2 else "FAIL")
    return 0 if ok and ok2 else 1


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("pilot", nargs="?"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: return selftest()
    t = fix(json.load(open(a.pilot, encoding="utf-8"))); txt = json.dumps(t, indent=1); print(txt)
    if a.out: open(a.out, "w", encoding="utf-8").write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
