"""Fixes the D8 tolerances from the pilot by the rules of PREREG-D8 Section 5 and prints the pilot summary.
Usage: python d8_fix_tols.py pilot.json tolerances.json

Rules, with their limits fixed before the pilot so a weak or variable pilot cannot loosen the claim. Advantages are in
ladder steps, computed on the pilot's graded cells by d8_grade.cells (the grader's own definition).
M1 = half the pilot's pooled advantage, rounded down to 0.1 step, and never below 0.5 step.
TOL1 = 1 step, fixed, not taken from the pilot.
TOL_N = 1.5 x the pilot's largest change in pooled advantage between its two resolutions (the largest over the
viscosities), rounded up to 0.1 step, then clamped to [0.2, 0.5] step.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d8_grade import GRADED, _world, cells  # noqa: E402

M1_FLOOR = 0.5
TOL_N_MIN = 0.2
TOL_N_MAX = 0.5


def fix(res: dict) -> dict:
    cs = cells(res); g = [c for c in cs if c["graded"]]
    if not g:
        raise SystemExit("no graded pilot cells; the tolerances cannot be fixed and the probe must be revisited")
    a = [c["a"] for c in g]; pooled = float(np.mean(a))
    changes = {}
    for nu in sorted(set(c["nu"] for c in g)):
        ns = sorted(set(c["n"] for c in g if c["nu"] == nu))
        pa = {n: float(np.mean([c["a"] for c in g if c["nu"] == nu and c["n"] == n])) for n in ns}
        changes[str(nu)] = {"pooled_by_n": pa, "change": abs(pa[ns[-1]] - pa[ns[-2]]) if len(ns) >= 2 else None}
    ch = [v["change"] for v in changes.values() if v["change"] is not None]
    if not ch:
        raise SystemExit("the pilot has no viscosity at two resolutions; TOL_N cannot be fixed")
    M1 = max(M1_FLOOR, math.floor(0.5 * pooled * 10 + 1e-9) / 10)
    TOL_N = min(TOL_N_MAX, max(TOL_N_MIN, math.ceil(1.5 * max(ch) * 10 - 1e-9) / 10))
    return {"M1": M1, "TOL1": 1.0, "TOL_N": TOL_N,
            "pilot": {"graded_cells": len(g), "uninformative_cells": len(cs) - len(g), "pooled_advantage_steps": pooled, "worst_cell": float(min(a)),
                      "by_viscosity": changes, "largest_change": float(max(ch)), "M1_unclamped": 0.5 * pooled, "TOL_N_unclamped": 1.5 * float(max(ch))},
            "rule": "PREREG-D8 Section 5: M1 = 0.5 x pilot pooled advantage rounded down to 0.1 step, at least 0.5; TOL1 = 1 step fixed; TOL_N = 1.5 x the pilot's largest change between its two resolutions rounded up to 0.1, clamped to [0.2, 0.5]"}


def selftest() -> int:
    fails = 0
    good = {"READ": 8, "BALL": 16, "ENSTROPHY": 16, "KE": 32, "SENS": 16, "RANDOM": None}

    def pilot(spec_lo, spec_hi):
        return {"seed_role": "pilot", "worlds": [_world(f"w{n}_{nu}", n, nu, [spec_lo if n == 64 else spec_hi] * 2, ladder=(4, 8, 16, 32, 64)) for nu in (0.004, 0.002) for n in (64, 96)]}

    cases = [("one-step advantage, no change: M1 at the floor, TOL_N at its minimum", pilot(good, good), 0.5, 0.2),
             ("three-step advantage: M1 = 1.5", pilot({**good, "READ": None, "BALL": None, "ENSTROPHY": None, "KE": None} | {"READ": 4, "BALL": 32, "ENSTROPHY": 32, "KE": 32}, {"READ": 4, "BALL": 32, "ENSTROPHY": 32, "KE": 32, "SENS": 16, "RANDOM": None}), 1.5, 0.2),
             ("no advantage: M1 stays at the floor", pilot({**good, "READ": 16}, {**good, "READ": 16}), 0.5, 0.2),
             ("a three-step change between resolutions: TOL_N capped at 0.5", pilot(good, {**good, "READ": 4, "BALL": 64, "ENSTROPHY": 64, "KE": 64}), None, 0.5)]
    for label, res, m1, tn in cases:
        t = fix(res); ok = (m1 is None or abs(t["M1"] - m1) < 1e-12) and abs(t["TOL_N"] - tn) < 1e-12 and t["TOL1"] == 1.0
        print(f"{label}: M1 {t['M1']} TOL_N {t['TOL_N']}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv: return 1 if selftest() else 0
    res = json.load(open(argv[0], encoding="utf-8-sig")); out = argv[1]
    for c in cells(res):
        print("%-14s n %3d nu %.4g test %d | %s | random %.1f | %s a %s" % (c["world"], c["n"], c["nu"], c["test"], " ".join("%s %d" % (k, c["idx"][k]) for k in GRADED + ("SENS",) if k in c["idx"]),
              c["random"], "graded" if c["graded"] else "uninformative", "-" if c["a"] is None else "%+.0f" % c["a"]))
    tols = fix(res); json.dump(tols, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(tols, indent=1)); return 0


if __name__ == "__main__":
    sys.exit(main())
