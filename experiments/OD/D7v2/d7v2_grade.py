"""Grades a D7v2 results.json against the sealed bars of PREREG-D7V2.md.
Usage: python d7v2_grade.py results.json --tols tolerances.json [--out grade.json]
The claim is the read-distortion closure (subfilter modes ranked by sensitivity times energy) against the energy
closure, inside a declared scope of rank at least R_MIN = 64 (the ranks at which the pilot of D7 found the two
rankings to separate); ranks below the scope are reported and not claimed. tolerances.json carries M2 (the pooled
relative advantage required at each in-scope rank), TOL2 (the allowed shortfall in any in-scope cell) and TOL_N
(the change of the pooled advantage between the run's two resolutions). The eigen-direction closure of D7 is
recorded per cell and not claimed."""
from __future__ import annotations

import json
import sys

import numpy as np

R_MIN = 64


def cells(res: dict, rmin: int = R_MIN) -> list[dict]:
    out = []
    for w in res["worlds"]:
        for sn in w["snapshots"]:
            for r, v in sn["ranks"].items():
                if r == "full" or int(r) < rmin: continue
                out.append({"world": w["name"], "n": w["n"], "t": sn["t"], "kc": sn["kc"], "r": int(r), **v})
    return out


def adv(c: dict) -> float:
    return (c["err_energy"] - c["err_read_energy"]) / c["err_energy"]


def grade(res: dict, tols: dict) -> dict:
    M2 = float(tols["M2"]); TOL2 = float(tols["TOL2"]); TOL_N = float(tols["TOL_N"])
    cs = cells(res); below = cells(res, 16); below = [c for c in below if c["r"] < R_MIN]
    out = {"tolerances": tols, "scope_rank_min": R_MIN, "n_cells_in_scope": len(cs), "n_cells_below_scope": len(below), "bars": {}, "gate": None}; fail = False
    # E1: structure beats random in every in-scope cell
    e1 = all(c["err_read_energy"] <= c["err_random_median"] + 1e-9 and c["err_energy"] <= c["err_random_median"] + 1e-9 for c in cs)
    out["bars"]["E1_structure_beats_random"] = {"holds": bool(e1)}
    if not e1: fail = True
    # L2 in scope: pooled advantage at each rank at least M2, no cell behind by more than TOL2
    by_r = {}
    for c in cs: by_r.setdefault(c["r"], []).append(adv(c))
    pooled = {r: float(np.mean(v)) for r, v in by_r.items()}; worst = float(min(adv(c) for c in cs))
    l2 = all(p >= M2 for p in pooled.values()) and worst >= -TOL2
    out["bars"]["L2_readenergy_vs_energy_in_scope"] = {"pooled_advantage_by_rank": pooled, "worst_cell": worst, "cells_behind": sum(1 for c in cs if adv(c) < 0), "margin": M2, "tol": TOL2, "holds": bool(l2)}
    if all(p < 0 for p in pooled.values()): fail = True
    # S1 the scope is where the separation is: below the scope the pooled advantage is smaller than in it (reported, and a bar)
    pooled_below = float(np.mean([adv(c) for c in below])) if below else None; pooled_in = float(np.mean([adv(c) for c in cs]))
    s1 = (pooled_below is not None and pooled_below < pooled_in)
    out["bars"]["S1_scope_is_where_separation_is"] = {"pooled_below_scope": pooled_below, "pooled_in_scope": pooled_in, "holds": bool(s1) if pooled_below is not None else None}
    # N1 convergence
    ns = sorted(set(c["n"] for c in cs))
    if len(ns) >= 2:
        pa = {n: float(np.mean([adv(c) for c in cs if c["n"] == n])) for n in ns}; d = abs(pa[ns[-1]] - pa[ns[-2]]); n1 = d <= TOL_N
    else:
        pa = {}; d = None; n1 = None
    out["bars"]["N1_convergence"] = {"pooled_advantage_by_n": pa, "diff_top_two": d, "limit": TOL_N, "holds": n1}
    # records: the eigen-direction closure and the full-rank remainder
    eig = [(c["err_energy"] - c["err_read"]) / c["err_energy"] for c in cs]
    q = [sn["ranks"]["full"]["err_read"] for w in res["worlds"] for sn in w["snapshots"] if "full" in sn["ranks"]]
    out["bars"]["R1_records"] = {"eigen_vs_energy_median_in_scope": float(np.median(eig)), "eigen_cells_behind": sum(1 for a in eig if a < 0), "quadratic_remainder_median": float(np.median(q)) if q else None, "quadratic_remainder_max": float(max(q)) if q else None}
    bars = [e1, l2, s1 if pooled_below is not None else None, n1]
    if any(b is None for b in bars):
        out["gate"] = "NOT ALL GROUPS RUN (pilot or probe): " + ("all run bars hold" if all(b for b in bars if b is not None) else "a run bar fails")
        return out
    out["gate"] = "PASS" if all(bars) else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]; tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), tols); text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
