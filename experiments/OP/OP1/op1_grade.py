"""OP1 grader: the bars of PREREG-OP1 Section 5 on a results file, with tolerances from tolerances.json.

A graded cell is one (world, cutoff, lift, r). Its advantage is a = (E_ctrl - E_READ) / E_ctrl, E_ctrl the better of
ENERGY and BALL in that cell. Bars:
  E1  pooled over cells, READ, ENERGY and BALL each below the RANDOM median; the best of them at the top r below NONE
  L1  the pooled advantage at least M1, and no cell below -TOL1
  L2  L1's pooled condition in each lift separately
  N1  per viscosity, the pooled advantage at the two resolutions differs by at most TOL_N (worst viscosity reported)
PASS when every bar holds; FAIL when the pooled advantage is at most zero in either lift; INDETERMINATE otherwise.

    python op1_grade.py results.json --tols tolerances.json [--out grade.json]
    python op1_grade.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys

import numpy as np


def cells(res: dict) -> list[dict]:
    """Every graded cell. The graded lifts are the config's `graded_lifts` (fixed by the lift rule of PREREG-OP1 Section 7
    before the pilot); a results file without them (the synthetic self-test) grades every lift it holds."""
    graded = res.get("config", {}).get("graded_lifts"); out = []
    for w in res["worlds"]:
        if "refused" in w: continue
        for kc, c in w["cutoffs"].items():
            top = str(max(c["ladder"]))
            for lift, L in c["lifts"].items():
                if graded is not None and lift not in graded: continue
                for r in c["ladder"]:
                    x = L[str(r)]; e = {k: (x[k]["E"] if x.get(k) else None) for k in ("READ", "ENERGY", "BALL", "SENS", "POD")}
                    ctrl = min(e["ENERGY"], e["BALL"])
                    out.append({"world": w["name"], "nu": w["nu"], "n": w["n"], "kc": kc, "lift": lift, "r": r, **e,
                                "RANDOM": x["RANDOM_median_E"], "NONE": L["NONE"]["E"], "PERSIST": L.get("PERSIST", {}).get("E"),
                                "GREEDY": x.get("GREEDY", {}).get("E"), "ctrl": ctrl, "a": (ctrl - e["READ"]) / ctrl if ctrl > 0 else 0.0,
                                "top": str(r) == top, "diverged": sum(bool(x[k].get("diverged")) for k in ("READ", "ENERGY", "BALL"))})
    return out


def pooled(cs: list[dict]) -> float:
    return float(np.mean([c["a"] for c in cs])) if cs else float("nan")


def grade(res: dict, tols: dict) -> dict:
    cs = cells(res); M1, TOL1, TOL_N = float(tols["M1"]), float(tols["TOL1"]), float(tols["TOL_N"])
    mean = lambda k, sub=None: float(np.mean([c[k] for c in (sub or cs)]))
    e1_rand = {k: {"pooled": mean(k), "random": mean("RANDOM"), "holds": mean(k) < mean("RANDOM")} for k in ("READ", "ENERGY", "BALL")}
    tops = [c for c in cs if c["top"]]; best_top = float(np.mean([min(c["READ"], c["ENERGY"], c["BALL"]) for c in tops])); none_top = mean("NONE", tops)
    E1 = {"structured_below_random": e1_rand, "best_at_top_r": best_top, "none": none_top, "holds": all(v["holds"] for v in e1_rand.values()) and best_top < none_top}
    pa = pooled(cs); worst = min(cs, key=lambda c: c["a"])
    L1 = {"pooled_advantage": pa, "margin": M1, "worst_cell": {k: worst[k] for k in ("world", "kc", "lift", "r", "a")}, "tol": TOL1,
          "cells_behind": sum(c["a"] < 0 for c in cs), "n_cells": len(cs), "holds": pa >= M1 and worst["a"] >= -TOL1}
    by_lift = {l: pooled([c for c in cs if c["lift"] == l]) for l in sorted({c["lift"] for c in cs})}
    L2 = {"pooled_by_lift": by_lift, "margin": M1, "holds": all(v >= M1 for v in by_lift.values())}
    n1 = {}
    for nu in sorted({c["nu"] for c in cs}):
        ns = sorted({c["n"] for c in cs if c["nu"] == nu})
        if len(ns) < 2: continue
        byn = {str(n): pooled([c for c in cs if c["nu"] == nu and c["n"] == n]) for n in ns[-2:]}
        n1[str(nu)] = {"pooled_by_n": byn, "diff": abs(byn[str(ns[-1])] - byn[str(ns[-2])])}
    N1 = {"by_nu": n1, "limit": TOL_N, "holds": bool(n1) and all(v["diff"] <= TOL_N for v in n1.values()), "note": None if n1 else "one resolution only: N1 not gradable"}
    rec = {k: mean(k) for k in ("READ", "ENERGY", "BALL", "SENS", "RANDOM", "NONE")}
    pods = [c["POD"] for c in cs if c["POD"] is not None]; rec["POD"] = float(np.mean(pods)) if pods else None  # no POD under TEND
    rec["GREEDY_lin"] = float(np.mean([c["GREEDY"] for c in cs if c["GREEDY"] is not None])) if any(c["GREEDY"] is not None for c in cs) else None
    rec["PERSIST"] = float(np.mean([c["PERSIST"] for c in cs if c["PERSIST"] is not None])) if any(c["PERSIST"] is not None for c in cs) else None
    rec["diverged_arm_cells"] = int(sum(c["diverged"] for c in cs))
    rec["pooled_advantage_by_kc"] = {k: pooled([c for c in cs if c["kc"] == k]) for k in sorted({c["kc"] for c in cs})}
    rec["pooled_advantage_by_r"] = {str(r): pooled([c for c in cs if c["r"] == r]) for r in sorted({c["r"] for c in cs})}
    bars = {"E1": E1, "L1": L1, "L2": L2, "N1": N1}
    if any(v <= 0 for v in by_lift.values()): gate = "FAIL"
    elif all(b["holds"] for b in bars.values()): gate = "PASS"
    else: gate = "INDETERMINATE"
    return {"tolerances": tols, "n_cells": len(cs), "bars": bars, "records": rec, "gate": gate}


def selftest() -> int:
    """Synthetic results: a READ that wins in both lifts passes; one that loses in one lift fails; a missing margin is
    INDETERMINATE; N1 reads the two finest resolutions per viscosity."""
    def world(name, nu, n, read_lin, read_rff):
        L = {}
        for lift, rd in (("lin", read_lin), ("rff", read_rff)):
            cells_ = {"NONE": {"E": 1.0}, "PERSIST": {"E": 0.9}}
            for r in (2, 4):
                cells_[str(r)] = {"READ": {"E": rd}, "ENERGY": {"E": 0.6}, "BALL": {"E": 0.7}, "SENS": {"E": 0.65}, "POD": {"E": 0.62}, "RANDOM_median_E": 0.8}
            L[lift] = cells_
        return {"name": name, "nu": nu, "n": n, "cutoffs": {"3": {"ladder": [2, 4], "lifts": L}}}
    tols = {"M1": 0.02, "TOL1": 0.1, "TOL_N": 0.02}
    fails = 0
    cases = [("wins in both lifts", [world("a", 0.02, 96, 0.54, 0.55), world("b", 0.02, 128, 0.54, 0.55)], "PASS"),
             ("loses in one lift", [world("a", 0.02, 96, 0.54, 0.62), world("b", 0.02, 128, 0.54, 0.62)], "FAIL"),
             ("ahead but under the margin", [world("a", 0.02, 96, 0.595, 0.595), world("b", 0.02, 128, 0.595, 0.595)], "INDETERMINATE"),
             ("not converged in n", [world("a", 0.02, 96, 0.54, 0.55), world("b", 0.02, 128, 0.57, 0.575)], "INDETERMINATE")]
    for label, ws, want in cases:
        g = grade({"worlds": ws}, tols); ok = g["gate"] == want; fails += 0 if ok else 1
        print(f"{label}: gate {g['gate']} (want {want}), pooled {g['bars']['L1']['pooled_advantage']:.4f}", "PASS" if ok else "FAIL")
    a = cells({"worlds": [world("a", 0.02, 96, 0.54, 0.55)]})[0]["a"]; ok = abs(a - (0.6 - 0.54) / 0.6) < 1e-12; fails += 0 if ok else 1
    print(f"advantage against the better control: {a:.4f}", "PASS" if ok else "FAIL")
    # only the configured lifts are graded: a READ that loses only in an ungraded lift passes
    ws = [world("a", 0.02, 96, 0.54, 0.62), world("b", 0.02, 128, 0.54, 0.62)]; g = grade({"config": {"graded_lifts": ["lin"]}, "worlds": ws}, tols)
    ok = g["gate"] == "PASS" and set(g["bars"]["L2"]["pooled_by_lift"]) == {"lin"}; fails += 0 if ok else 1
    print(f"ungraded lift ignored: gate {g['gate']}, lifts {sorted(g['bars']['L2']['pooled_by_lift'])}", "PASS" if ok else "FAIL")
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("results", nargs="?"); ap.add_argument("--tols"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: return 1 if selftest() else 0
    g = grade(json.load(open(a.results, encoding="utf-8")), json.load(open(a.tols, encoding="utf-8")))
    txt = json.dumps(g, indent=1); print(txt)
    if a.out: open(a.out, "w", encoding="utf-8").write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
