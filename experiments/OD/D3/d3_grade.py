"""Grades a D3 results.json against the sealed bars of PREREG-D3.md.
Usage: python d3_grade.py results.json --tols tolerances.json [--out grade.json]

Exact bars (theorems, zero violations allowed): E1 the positive definite window bound
|lambda_O - lambda_cl| <= log(b/a) / (2 (T - t0)); KX in World K the core reader's exponent equals
the exponent of the perturbation's core part; H1 horizons non-decreasing in B, the positive
definite bracket, and a projection never earlier than the Euclidean horizon.
Tolerance bars (numbers fixed from the pilot, `tolerances.json`): E2 convergence for the
anisotropic observers; K1 World K mu = 2, observational exponent below the classical by at least
0.5 and the classical near mu; K1c the mu = 0.5 control, the two exponents agree; K2 kernel starts,
transiently larger and converging; K3 generic starts under a projection, converging; H2 horizons
observer-dependent in Lorenz-63 (x against z) and not in Lorenz-96 (one block of sites against the
next), by an exact paired sign test on the horizons of the same start and perturbation."""
from __future__ import annotations

import json
import sys

import numpy as np

EPS = 1e-9


def med(v):
    v = [x for x in v if x == x]
    return float(np.median(v)) if v else float("nan")


def sign_p(a, b):
    """Exact two-sided sign test on the paired differences a - b (same start and perturbation read
    by two observers); ties and unreached horizons are excluded. Returns (p, n_pairs, fraction a > b)."""
    from math import comb
    pairs = [(x, y) for x, y in zip(a, b) if np.isfinite(x) and np.isfinite(y) and x != y]
    n = len(pairs)
    if n < 8:
        return float("nan"), n, float("nan")
    k = sum(x > y for x, y in pairs)
    tail = sum(comb(n, j) for j in range(0, min(k, n - k) + 1)) / 2 ** n
    return min(1.0, 2 * tail), n, k / n


def grade(res: dict, tols: dict) -> dict:
    cfg = res["config"]; Ts = [str(float(t)) for t in cfg["T_ladder"]]; Tmax = Ts[-1]; Bs = [str(float(b)) for b in cfg["B_ladder"]]
    out = {"tolerances": tols, "exact": {}, "bars": {}, "gate": None}
    fail = False; all_pass = True
    e1_viol = 0; e1_checked = 0; kx_viol = 0; h1_viol = 0; h1_checked = 0
    worlds = {w["name"]: w for w in res["worlds"]}
    for w in res["worlds"]:
        n = w["n"]; obs_spec = {name: o for name, o in w["observers"].items()}
        for name, o in obs_spec.items():
            if isinstance(o, list):
                p = np.array(o); pd = bool((p > 0).all()); a, b = (float(p.min()), float(p.max())) if pd else (None, None)
            else:
                pd = bool(o["min"] > 0); a, b = (o["min"], o["max"]) if pd else (None, None)
            obs_spec[name] = {"pd": pd, "a": a, "b": b}
        for r in w["rows"]:
            t0 = r["t0"]
            for name, spec in obs_spec.items():
                ro = r["observers"][name]
                if spec["pd"]:
                    for T in Ts:
                        lo, lc = ro["exponent"][T], r["classical"][T]
                        if lo == lo and lc == lc:
                            e1_checked += 1
                            if abs(lo - lc) > np.log(spec["b"] / spec["a"]) / (2 * (float(T) - t0)) + EPS:
                                e1_viol += 1
                # H1
                hs = [ro["horizon"][B] for B in Bs]
                for i in range(len(hs) - 1):
                    h1_checked += 1
                    if hs[i + 1] < hs[i] - EPS:
                        h1_viol += 1
                if spec["pd"] and name in r.get("euclid_horizon_scaled", {}):
                    for B in Bs:
                        lo_, hi_ = r["euclid_horizon_scaled"][name][B]; h1_checked += 1
                        if not (lo_ - EPS <= ro["horizon"][B] <= hi_ + EPS):
                            h1_viol += 1
                if not spec["pd"]:
                    for B in Bs:
                        h1_checked += 1
                        if ro["horizon"][B] < r["euclid_horizon"][B] - EPS:
                            h1_viol += 1
            if w.get("mu") is not None:
                for T in Ts:
                    if abs(r["observers"]["core"]["exponent"][T] - r["core_part"][T]) > 1e-7:
                        kx_viol += 1
    out["exact"] = {"E1_pd_bound": {"checked": e1_checked, "violations": e1_viol, "holds": e1_viol == 0},
                    "KX_core_reader_equals_core_part": {"violations": kx_viol, "holds": kx_viol == 0},
                    "H1_horizons": {"checked": h1_checked, "violations": h1_viol, "holds": h1_viol == 0}}
    if e1_viol or kx_viol or h1_viol:
        fail = True; all_pass = False

    def rows(world, direction):
        return [r for r in worlds[world]["rows"] if r["direction"] == direction]

    def diff_seq(rs, obs):
        return [med([abs(r["observers"][obs]["exponent"][T] - r["classical"][T]) for r in rs]) for T in Ts]

    def nonincreasing(seq):
        return all(seq[i + 1] <= seq[i] * 1.05 + 1e-12 for i in range(len(seq) - 1))

    # E2: anisotropic observers, random direction
    for world, obs in (("lorenz63", "aniso"), ("lorenz96", "aniso")):
        seq = diff_seq(rows(world, "random"), obs)
        ok = nonincreasing(seq) and seq[-1] <= tols["E2"]
        out["bars"][f"E2_{world}"] = {"median_abs_diff_by_T": seq, "nonincreasing": nonincreasing(seq), "final_within": seq[-1] <= tols["E2"], "holds": ok}
        all_pass = all_pass and ok
    # K1: World K mu = 2
    rs = rows("K_mu2", "core_plus_u")
    gaps = [r["classical"][Tmax] - r["observers"]["core"]["exponent"][Tmax] for r in rs]
    cls = [r["classical"][Tmax] for r in rs]
    k1_gap = all(g >= 0.5 for g in gaps); k1_mu = all(abs(c - 2.0) <= 0.15 for c in cls)
    out["bars"]["K1_mu2_smaller"] = {"gap_min": float(min(gaps)), "gap_median": med(gaps), "classical_median": med(cls), "observational_median": med([r["observers"]["core"]["exponent"][Tmax] for r in rs]),
                                     "all_gaps_ge_0.5": k1_gap, "classical_within_0.15_of_mu": k1_mu, "holds": k1_gap and k1_mu}
    all_pass = all_pass and k1_gap and k1_mu
    if sum(g < 0.5 for g in gaps) > len(gaps) / 2:
        fail = True
    # K1c: control mu = 0.5
    rs = rows("K_mu05", "core_plus_u")
    d = [abs(r["classical"][Tmax] - r["observers"]["core"]["exponent"][Tmax]) for r in rs]
    ok = max(d) <= tols["K1c"]
    out["bars"]["K1c_mu05_equal"] = {"abs_diff_max": float(max(d)), "abs_diff_median": med(d), "holds": ok}
    all_pass = all_pass and ok
    # K2: kernel starts, transient then convergence
    for world, direction, obs in (("lorenz63", "kernel_x", "x_only"), ("lorenz63", "kernel_z", "z_only"), ("lorenz96", "kernel_sub", "sub")):
        rs = rows(world, direction); T1 = Ts[0]
        frac = float(np.mean([r["observers"][obs]["exponent"][T1] > r["classical"][T1] for r in rs]))
        seq = diff_seq(rs, obs)
        excess = [med([r["observers"][obs]["exponent"][T] - r["classical"][T] for r in rs]) for T in Ts]
        ok = frac >= tols["K2_frac"] and seq[-1] <= tols["K2"]
        out["bars"][f"K2_{world}_{direction}"] = {"fraction_larger_at_T1": frac, "median_excess_by_T": excess, "median_abs_diff_by_T": seq, "holds": ok}
        all_pass = all_pass and ok
    # K3: generic starts under projections
    for world, obs in (("lorenz63", "x_only"), ("lorenz63", "z_only"), ("lorenz96", "sub"), ("lorenz96", "sub2")):
        seq = diff_seq(rows(world, "random"), obs)
        ok = nonincreasing(seq) and seq[-1] <= tols["K3"]
        out["bars"][f"K3_{world}_{obs}"] = {"median_abs_diff_by_T": seq, "nonincreasing": nonincreasing(seq), "holds": ok}
        all_pass = all_pass and ok
    # H2: observer dependence of the horizon
    for world, o1, o2, expect_different in (("lorenz63", "x_only", "z_only", True), ("lorenz96", "sub", "sub2", False)):
        rs = rows(world, "random"); entry = {}; ok = True
        for B in Bs:
            h1 = [r["observers"][o1]["horizon"][B] for r in rs]; h2 = [r["observers"][o2]["horizon"][B] for r in rs]
            m1, m2 = med(h1), med(h2)
            if not (np.isfinite(m1) and np.isfinite(m2)):
                entry[B] = {"median_1": m1, "median_2": m2, "note": "median horizon not reached; not graded"}; continue
            p, npairs, frac = sign_p(h1, h2)
            holds = (p <= 0.01) if expect_different else (p >= 0.01)
            entry[B] = {"median_1": m1, "median_2": m2, "sign_test_p": p, "pairs": npairs, "fraction_first_later": frac, "holds": holds}; ok = ok and holds
        out["bars"][f"H2_{world}_{o1}_vs_{o2}"] = {"expect_different": expect_different, "by_B": entry, "holds": ok}
        all_pass = all_pass and ok
    out["gate"] = "PASS" if all_pass else ("FAIL" if fail else "INDETERMINATE")
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0]
    tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), tols)
    text = json.dumps(g, indent=1)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
