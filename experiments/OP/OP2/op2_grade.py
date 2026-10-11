"""OP2 grader and tolerance rules (PREREG-OP2-DRAFT.md Section 5), written before the pilot runs.

A graded cell is one (world, cutoff, r). The statistic is the memory share of the consumer block, chosen on the probe by
the READ-blind split-half rule (lower is better). The advantage of READ is a = (s_ctrl - s_READ) / s_ctrl, s_ctrl the
better (lower) of ENERGY's and BALL's shares in that cell. Bars:
  E1   pooled, READ, ENERGY and BALL each leave a smaller share than the RANDOM median
  L1   the pooled advantage at least M1, and no cell below -TOL1
  L1E  READ's best forecast with memory no worse: pooled (E_ctrl - E_READ) / E_ctrl >= -0.01, E_ctrl the better of
       ENERGY's and BALL's min_L E_L (fixed before the pilot, not from it)
  L2   L1's pooled condition in each cutoff separately (the observer family of OP2)
  N1   per viscosity, the pooled advantage at the two resolutions differs by at most TOL_N
PASS when every bar holds; FAIL when the pooled advantage is at most zero in either cutoff; INDETERMINATE otherwise.
Tolerances from the pilot, the rules of OP1 with the same limits: M1 = 0.5 x pooled (down to 0.005) in [0.01, 0.10];
TOL1 = 1.25 x worst shortfall (up to 0.01) in [0.05, 0.25]; TOL_N = 1.5 x resolution change (up to 0.005) in [0.01, 0.05].

    python op2_grade.py results.json --tols tolerances.json [--out grade.json]
    python op2_grade.py --fix-tols pilot.json --out tolerances.json
    python op2_grade.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import sys

import numpy as np

E_TOL = 0.01
LIMITS = {"M1": (0.01, 0.10), "TOL1": (0.05, 0.25), "TOL_N": (0.01, 0.05)}


def cells(res: dict) -> list[dict]:
    out = []
    for w in res["worlds"]:
        for kc, c in w["cutoffs"].items():
            for r, cell in c["cells"].items():
                s = {k: cell[k]["share"] for k in ("READ", "ENERGY", "BALL", "SENS")}; e = {k: cell[k]["E_min"] for k in ("READ", "ENERGY", "BALL")}
                rnd = float(np.median([v["share"] for k, v in cell.items() if k.startswith("RANDOM")]))
                sc = min(s["ENERGY"], s["BALL"]); ec = min(e["ENERGY"], e["BALL"])
                out.append({"world": w["name"], "nu": w["nu"], "n": w["n"], "kc": str(kc), "r": int(r), **{f"share_{k}": v for k, v in s.items()}, "share_RANDOM": rnd,
                            "a": (sc - s["READ"]) / sc if sc > 0 else 0.0, "aE": (ec - e["READ"]) / ec if ec > 0 else 0.0})
    return out


def pooled(cs, key="a") -> float:
    return float(np.mean([c[key] for c in cs])) if cs else float("nan")


def grade(res: dict, tols: dict) -> dict:
    cs = cells(res); M1, TOL1, TOL_N = float(tols["M1"]), float(tols["TOL1"]), float(tols["TOL_N"])
    rnd = pooled(cs, "share_RANDOM")
    E1 = {k: {"pooled_share": pooled(cs, f"share_{k}"), "random": rnd} for k in ("READ", "ENERGY", "BALL")}
    E1 = {"by_ranking": E1, "holds": all(v["pooled_share"] < rnd for v in E1.values())}
    pa = pooled(cs); worst = min(cs, key=lambda c: c["a"])
    L1 = {"pooled_advantage": pa, "margin": M1, "worst_cell": {k: worst[k] for k in ("world", "kc", "r", "a")}, "tol": TOL1, "cells_behind": sum(c["a"] < 0 for c in cs),
          "n_cells": len(cs), "holds": pa >= M1 and worst["a"] >= -TOL1}
    pe = pooled(cs, "aE"); L1E = {"pooled_E_advantage": pe, "limit": -E_TOL, "holds": pe >= -E_TOL}
    by_kc = {k: pooled([c for c in cs if c["kc"] == k]) for k in sorted({c["kc"] for c in cs})}
    L2 = {"pooled_by_cutoff": by_kc, "margin": M1, "holds": all(v >= M1 for v in by_kc.values())}
    n1 = {}
    for nu in sorted({c["nu"] for c in cs}):
        ns = sorted({c["n"] for c in cs if c["nu"] == nu})
        if len(ns) < 2: continue
        byn = {str(n): pooled([c for c in cs if c["nu"] == nu and c["n"] == n]) for n in ns[-2:]}
        n1[str(nu)] = {"pooled_by_n": byn, "diff": abs(byn[str(ns[-1])] - byn[str(ns[-2])])}
    N1 = {"by_nu": n1, "limit": TOL_N, "holds": bool(n1) and all(v["diff"] <= TOL_N for v in n1.values())}
    bars = {"E1": E1, "L1": L1, "L1E": L1E, "L2": L2, "N1": N1}
    gate = "FAIL" if any(v <= 0 for v in by_kc.values()) else ("PASS" if all(b["holds"] for b in bars.values()) else "INDETERMINATE")
    return {"tolerances": tols, "n_cells": len(cs), "bars": bars, "records": {"pooled_share_SENS": pooled(cs, "share_SENS")}, "gate": gate}


def fix_tols(pilot: dict) -> dict:
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
    return {**out, "limits_binding": bound, "pilot": {"pooled_advantage": p, "worst_shortfall": short, "max_change_between_resolutions": d, "n_cells": len(cs)}}


def selftest() -> int:
    def world(n, kc_shares, e_read=0.30):
        cut = {}
        for kc, sr in kc_shares.items():
            cells_ = {}
            for r in (2, 4):
                cells_[str(r)] = {"READ": {"share": sr, "E_min": e_read}, "ENERGY": {"share": 0.60, "E_min": 0.30}, "BALL": {"share": 0.55, "E_min": 0.31}, "SENS": {"share": 0.58, "E_min": 0.3},
                                  **{f"RANDOM{j}": {"share": 0.70, "E_min": 0.33} for j in range(3)}}
            cut[kc] = {"cells": cells_}
        return {"name": f"w{n}", "nu": 0.02, "n": n, "cutoffs": cut}
    tols = {"M1": 0.02, "TOL1": 0.1, "TOL_N": 0.02}; fails = 0
    cases = [("less memory in both cutoffs", [world(96, {"3": 0.50, "5": 0.51}), world(128, {"3": 0.50, "5": 0.51})], "PASS"),
             ("more memory at one cutoff", [world(96, {"3": 0.50, "5": 0.57}), world(128, {"3": 0.50, "5": 0.57})], "FAIL"),
             ("less memory but a worse forecast", [world(96, {"3": 0.50, "5": 0.51}, 0.32), world(128, {"3": 0.50, "5": 0.51}, 0.32)], "INDETERMINATE"),
             ("not converged in n", [world(96, {"3": 0.45, "5": 0.46}), world(128, {"3": 0.52, "5": 0.53})], "INDETERMINATE")]
    for label, ws, want in cases:
        g = grade({"worlds": ws}, tols); ok = g["gate"] == want; fails += 0 if ok else 1
        print(f"{label}: gate {g['gate']} (want {want}), pooled {g['bars']['L1']['pooled_advantage']:.4f}", "PASS" if ok else "FAIL")
    t = fix_tols({"worlds": [world(96, {"3": 0.495, "5": 0.495}), world(128, {"3": 0.5225, "5": 0.5225})]})  # advantages 0.10 and 0.05
    ok = t["M1"] == 0.035 and t["TOL1"] == 0.05 and t["TOL_N"] == 0.05; fails += 0 if ok else 1
    print("tolerances from a synthetic pilot:", {k: t[k] for k in ("M1", "TOL1", "TOL_N")}, t["limits_binding"], "PASS" if ok else "FAIL")
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("results", nargs="?"); ap.add_argument("--tols"); ap.add_argument("--out")
    ap.add_argument("--fix-tols", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: return 1 if selftest() else 0
    data = json.load(open(a.results, encoding="utf-8"))
    out = fix_tols(data) if a.fix_tols else grade(data, json.load(open(a.tols, encoding="utf-8")))
    txt = json.dumps(out, indent=1); print(txt)
    if a.out: open(a.out, "w", encoding="utf-8").write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
