"""Grades a D7 results.json against the sealed bars of PREREG-D7.md.
Usage: python d7_grade.py results.json --tols tolerances.json [--out grade.json]
tolerances.json carries M1 (the eigen-direction closure's required relative advantage over the energy closure, every
cell, ranks >= R_MIN), M2 (the read-energy closure's required pooled relative advantage), TOL2 (its allowed shortfall
in any cell) and TOL_N (the change of the pooled advantage between the two run resolutions)."""
from __future__ import annotations

import json
import sys

import numpy as np

R_MIN = 16


def cells(res: dict) -> list[dict]:
    out = []
    for w in res["worlds"]:
        for sn in w["snapshots"]:
            for r, v in sn["ranks"].items():
                if r == "full" or int(r) < R_MIN: continue
                out.append({"world": w["name"], "n": w["n"], "t": sn["t"], "kc": sn["kc"], "r": int(r), **v})
    return out


def grade(res: dict, tols: dict) -> dict:
    M1 = float(tols["M1"]); M2 = float(tols["M2"]); TOL2 = float(tols["TOL2"]); TOL_N = float(tols["TOL_N"])
    cs = cells(res); out = {"tolerances": tols, "n_cells": len(cs), "bars": {}, "gate": None}; fail = False
    # E1: structure beats random: every closure's error at most the random median's, every cell
    e1 = all(c["err_read"] <= c["err_random_median"] + 1e-9 and c["err_read_energy"] <= c["err_random_median"] + 1e-9 and c["err_energy"] <= c["err_random_median"] + 1e-9 for c in cs)
    out["bars"]["E1_structure_beats_random"] = {"holds": bool(e1)}
    if not e1:
        fail = True
    # L1 the declared arm: eigen-direction closure ahead of the energy closure by M1 in every cell
    adv1 = [(c["err_energy"] - c["err_read"]) / c["err_energy"] for c in cs]
    l1 = all(a >= M1 for a in adv1)
    out["bars"]["L1_eigen_vs_energy"] = {"min_advantage": float(min(adv1)), "median_advantage": float(np.median(adv1)), "cells_behind": sum(1 for a in adv1 if a < 0), "margin": M1, "holds": bool(l1)}
    # L2 the read-energy arm: pooled advantage over energy at each rank at least M2, and no cell behind by more than TOL2
    by_r = {}
    for c in cs:
        by_r.setdefault(c["r"], []).append((c["err_energy"] - c["err_read_energy"]) / c["err_energy"])
    pooled = {r: float(np.mean(v)) for r, v in by_r.items()}; worst = min((c["err_energy"] - c["err_read_energy"]) / c["err_energy"] for c in cs)
    l2 = all(p >= M2 for p in pooled.values()) and worst >= -TOL2
    out["bars"]["L2_readenergy_vs_energy"] = {"pooled_advantage_by_rank": pooled, "worst_cell": float(worst), "margin": M2, "tol": TOL2, "holds": bool(l2)}
    if all(p < 0 for p in pooled.values()):
        fail = True
    # N1 convergence: the pooled read-energy advantage changes by at most TOL_N between the two run resolutions
    ns = sorted(set(c["n"] for c in cs))
    if len(ns) >= 2:
        pa = {n: float(np.mean([(c["err_energy"] - c["err_read_energy"]) / c["err_energy"] for c in cs if c["n"] == n])) for n in ns}
        d = abs(pa[ns[-1]] - pa[ns[-2]]); n1 = d <= TOL_N
    else:
        pa = {}; d = None; n1 = None
    out["bars"]["N1_convergence"] = {"pooled_advantage_by_n": pa, "diff_top_two": d, "limit": TOL_N, "holds": n1}
    # Q1 record: the quadratic remainder at the read operator's full rank
    q = [sn["ranks"]["full"]["err_read"] for w in res["worlds"] for sn in w["snapshots"] if "full" in sn["ranks"]]
    out["bars"]["Q1_quadratic_remainder"] = {"median": float(np.median(q)) if q else None, "max": float(max(q)) if q else None, "n": len(q)}
    bars = [e1, l1, l2, n1]
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
