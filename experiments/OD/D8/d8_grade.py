"""Grades a D8 results.json against the bars of PREREG-D8 (draft revision 2, Sections 4 and 5).
Usage: python d8_grade.py results.json --tols tolerances.json [--out grade.json]
       python d8_grade.py --selftest

Index. A cell is (world, test trajectory). An observer's m* is read as its ladder index i(m*); a censored observer (no
sustained synchronization at the top of the ladder) is at index len(ladder), one step past the top. READ's advantage in a
cell is a = i_best - i_READ, i_best the smallest index among the graded controls BALL, ENSTROPHY and KE, in ladder steps.

Outcome of every case (Section 4). A cell is graded when READ or any graded control synchronizes, and uninformative when
all four are censored (excluded from L1 and N1, counted against E2). RANDOM is the median index of its draws and enters E2
only. SENS enters no bar. A world refused by the stability guard makes the gate INDETERMINATE.

Bars (Section 5). T1 every checked read beyond 2N at most 1e-10 of the largest first-octave read; T2 every Proposition 3
ratio at most 1; E1 everything observed holds delta <= 1e-10 over the final window and nothing observed ends at
delta >= 0.3, on every test trajectory; E2 at least three quarters of each world's cells graded, and the best graded
control's pooled mean index (the mean of i_best) below RANDOM's, so that scope depends on the classical observers alone and
neither READ nor SENS can move it; L1 pooled advantage >= M1 and no graded cell with a < -1 (TOL1 = 1 step, fixed); N1 for
each viscosity the pooled advantages at the two largest resolutions differ by at most TOL_N.

Verdict (Section 5). T1 or T2 missing: FAIL (the note's proposition), nothing else graded. Else a refused world, E1 or E2
missing: INDETERMINATE. Else FAIL if the pooled advantage <= -0.5 or more than a quarter of graded cells have a <= -2;
PASS if L1 and N1 hold; INDETERMINATE otherwise. A probe or pilot file gets the same computation labelled as not a verdict.
"""
from __future__ import annotations

import json
import sys

import numpy as np

CONTROLS = ("BALL", "ENSTROPHY", "KE")
GRADED = ("READ",) + CONTROLS
T1_LIMIT = 1e-10
E1_ALL = 1e-10
E1_NONE = 0.3
E2_GRADED_FRACTION = 0.75
TOL1 = 1.0
FAIL_POOLED = -0.5
FAIL_DEEP = -2.0
FAIL_DEEP_FRACTION = 0.25


def index(rec: dict, ladder: list[int]) -> int:
    return len(ladder) if rec["m_star"] is None else ladder.index(rec["m_star"])


def random_index(obs: dict, ladder: list[int]) -> float:
    return float(np.median([index(v, ladder) for k, v in obs.items() if k.startswith("RANDOM")]))


def cells(res: dict) -> list[dict]:
    """One row per (world, test trajectory) of every world that was not refused."""
    out = []
    for w in res["worlds"]:
        if w.get("refused"): continue
        L = w["ladder"]
        for t in w["tests"]:
            obs = t["observers"]; idx = {k: index(obs[k], L) for k in GRADED + ("SENS",) if k in obs}
            graded = any(idx[k] < len(L) for k in GRADED)
            best = min(idx[k] for k in CONTROLS)
            out.append({"world": w["name"], "n": w["n"], "nu": w["nu"], "test": t["index"], "L": len(L), "idx": idx, "random": random_index(obs, L),
                        "graded": graded, "a": float(best - idx["READ"]) if graded else None, "a_sens": float(best - idx["SENS"]) if graded and "SENS" in idx else None,
                        "lower_bound": bool(graded and all(idx[k] == len(L) for k in CONTROLS)), "best": int(best)})
    return out


def rank_corr(x, y) -> float | None:
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0: return None
    rx = np.argsort(np.argsort(x)).astype(float); ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


def records(res: dict, cs: list[dict]) -> dict:
    """R1, not graded."""
    rec = {"sens_advantage_pooled": None, "lyap_obs_sign_agreement": {}, "lyap_obs_at_mstar_and_below": {}, "block_vs_obs_sign_disagreement": None,
           "overlap_at_read_mstar": {}, "read_shells_at_mstar": {}, "nonmonotone_cells": {}, "mu_record_mstar": {}, "dt_half_agreement": None,
           "initial_rate_vs_index_rank_corr": None, "lower_bound_cells": sum(1 for c in cs if c["lower_bound"])}
    sens = [c["a_sens"] for c in cs if c["a_sens"] is not None]; rec["sens_advantage_pooled"] = float(np.mean(sens)) if sens else None
    agree = {k: [0, 0] for k in GRADED}; at = {k: [0, 0] for k in GRADED}; bd = [0, 0]; nonmono = {}; dt_eq = [0, 0]; rates = []; idxs = []
    overlap = {k: [] for k in CONTROLS + ("SENS",)}; shells = {}
    for w in res["worlds"]:
        if w.get("refused"): continue
        L = w["ladder"]
        for t in w["tests"]:
            obs = t["observers"]
            for name, o in obs.items():
                if o.get("nonmonotone"): nonmono[name] = nonmono.get(name, 0) + 1
            for name in GRADED:
                o = obs[name]; ly = o.get("lyap_obs")
                if ly is not None:
                    for s, l in zip(o["synced"], ly):
                        agree[name][0] += int((l < 0) == bool(s)); agree[name][1] += 1
                    i = index(o, L)
                    for j in (i, i - 1):
                        if 0 <= j < len(L):
                            at[name][0] += int((ly[j] < 0) == bool(o["synced"][j])); at[name][1] += 1
                    if o.get("lyap_block") is not None:
                        for a_, b_ in zip(ly, o["lyap_block"]):
                            bd[0] += int((a_ < 0) != (b_ < 0)); bd[1] += 1
                i = index(o, L); m = L[min(i, len(L) - 1)]
                rates.append(o["initial_spreading_rate"][L.index(m)]); idxs.append(i)
                if name in t.get("dt_half", {}):
                    dt_eq[0] += int(t["dt_half"][name]["m_star"] == o["m_star"]); dt_eq[1] += 1
                for mu, d in t.get("mu_record", {}).items():
                    if name in d: rec["mu_record_mstar"].setdefault(mu, {}).setdefault(name, []).append(d[name]["m_star"])
            m_read = obs["READ"]["m_star"]
            if m_read is not None:
                top = {tuple(x) for x in w["rankings"]["READ"][:m_read]}
                for k in overlap:
                    overlap[k].append(len(top & {tuple(x) for x in w["rankings"][k][:m_read]}) / m_read)
                for kx, ky in top:
                    s = int(np.floor(np.hypot(kx, ky))); shells[s] = shells.get(s, 0) + 1
    rec["lyap_obs_sign_agreement"] = {k: (v[0] / v[1] if v[1] else None) for k, v in agree.items()}
    rec["lyap_obs_at_mstar_and_below"] = {k: (v[0] / v[1] if v[1] else None) for k, v in at.items()}
    rec["block_vs_obs_sign_disagreement"] = bd[0] / bd[1] if bd[1] else None
    rec["overlap_at_read_mstar"] = {k: (float(np.mean(v)) if v else None) for k, v in overlap.items()}
    rec["read_shells_at_mstar"] = dict(sorted(shells.items())); rec["nonmonotone_cells"] = nonmono
    rec["dt_half_agreement"] = (dt_eq[0], dt_eq[1]) if dt_eq[1] else None
    rec["initial_rate_vs_index_rank_corr"] = rank_corr(rates, idxs)
    return rec


def grade(res: dict, tols: dict) -> dict:
    M1 = float(tols["M1"]); TOL_N = float(tols["TOL_N"]); role = res.get("seed_role", "run")
    out = {"tolerances": tols, "seed_role": role, "bars": {}, "gate": None}
    # T1, T2: the theorem checks
    ch = [c for w in res["worlds"] for c in w.get("theorem_checks", [])]
    t1 = bool(ch) and all(c["T1_ratio"] is not None and c["T1_ratio"] <= T1_LIMIT and c["first_octave_max_read"] > 0 for c in ch)
    t2 = bool(ch) and all(c["T2_ratio"] is not None and c["T2_ratio"] <= 1.0 for c in ch)
    out["bars"]["T1_octave_locality"] = {"checks": len(ch), "max_ratio": max((c["T1_ratio"] or 0.0) for c in ch) if ch else None, "limit": T1_LIMIT, "holds": t1}
    t2r = [c["T2_ratio"] for c in ch if c["T2_ratio"] is not None]
    out["bars"]["T2_feedback_bound"] = {"checks": len(ch), "max_ratio": max(t2r) if t2r else None, "median_ratio": float(np.median(t2r)) if t2r else None, "holds": t2}
    if not (t1 and t2):
        out["gate"] = _label(role, "FAIL (a proposition of notes/dynamical-read-operator.md misses on the solver; nothing else graded)"); return out
    refused = [w["name"] for w in res["worlds"] if w.get("refused")]
    out["refused_worlds"] = refused
    # E1
    tests = [(w["name"], t) for w in res["worlds"] if not w.get("refused") for t in w["tests"]]
    bad = [(nm, t["index"]) for nm, t in tests if not (t["all_hold_max"] <= E1_ALL and t["none_final"] >= E1_NONE)]
    e1 = bool(tests) and not bad
    out["bars"]["E1_instrument"] = {"tests": len(tests), "misses": bad, "all_hold_max_worst": max((t["all_hold_max"] for _, t in tests), default=None), "none_final_least": min((t["none_final"] for _, t in tests), default=None), "holds": e1}
    # E2
    cs = cells(res); worlds = sorted(set(c["world"] for c in cs))
    frac = {w: float(np.mean([c["graded"] for c in cs if c["world"] == w])) for w in worlds}
    pooled_idx = {k: float(np.mean([c["idx"][k] for c in cs])) for k in GRADED} if cs else {}
    pooled_best = float(np.mean([c["best"] for c in cs])) if cs else None; pooled_rand = float(np.mean([c["random"] for c in cs])) if cs else None
    e2 = bool(cs) and all(f >= E2_GRADED_FRACTION for f in frac.values()) and pooled_best < pooled_rand
    out["bars"]["E2_scope"] = {"graded_fraction_by_world": frac, "best_control_pooled_mean_index": pooled_best, "random_pooled_mean_index": pooled_rand,
                               "pooled_mean_index_recorded": pooled_idx, "holds": e2}
    # L1, N1 on graded cells
    g = [c for c in cs if c["graded"]]; a = [c["a"] for c in g]
    pooled = float(np.mean(a)) if a else None; worst = float(min(a)) if a else None
    l1 = bool(a) and pooled >= M1 and worst >= -TOL1
    deep = (sum(1 for x in a if x <= FAIL_DEEP) / len(a)) if a else None
    out["bars"]["L1_read_vs_best_control"] = {"graded_cells": len(g), "uninformative_cells": len(cs) - len(g), "pooled_advantage_steps": pooled, "worst_cell": worst,
                                             "cells_behind": sum(1 for x in a if x < 0), "cells_ahead": sum(1 for x in a if x > 0), "lower_bound_cells": sum(1 for c in g if c["lower_bound"]),
                                             "margin_M1": M1, "tol1": TOL1, "deep_shortfall_fraction": deep, "holds": l1}
    n1_by = {}
    for nu in sorted(set(c["nu"] for c in g)):
        ns = sorted(set(c["n"] for c in g if c["nu"] == nu))
        pa = {n: float(np.mean([c["a"] for c in g if c["nu"] == nu and c["n"] == n])) for n in ns}
        n1_by[str(nu)] = {"pooled_by_n": pa, "diff_top_two": abs(pa[ns[-1]] - pa[ns[-2]]) if len(ns) >= 2 else None}
    diffs = [v["diff_top_two"] for v in n1_by.values()]
    n1 = None if (not diffs or any(d is None for d in diffs)) else all(d <= TOL_N for d in diffs)
    out["bars"]["N1_resolution"] = {"by_viscosity": n1_by, "limit": TOL_N, "holds": n1}
    out["bars"]["R1_records"] = records(res, cs)
    # verdict
    if refused:
        verdict = "INDETERMINATE (a world refused by the stability guard: %s)" % ", ".join(refused)
    elif not e1:
        verdict = "INDETERMINATE (E1: the instrument does not separate the extremes)"
    elif not e2:
        verdict = "INDETERMINATE (E2: outside the scope the ladder measures)"
    elif pooled <= FAIL_POOLED or deep > FAIL_DEEP_FRACTION:
        verdict = "FAIL"
    elif l1 and n1:
        verdict = "PASS"
    else:
        verdict = "INDETERMINATE"
    out["gate"] = _label(role, verdict)
    return out


def _label(role: str, verdict: str) -> str:
    return verdict if role == "run" else f"{role.upper()} GRADE, NOT A VERDICT: {verdict}"


# ---------------------------------------------------------------- self-test on synthetic results

def _obs(m_star, ladder):
    syn = [m_star is not None and m >= m_star for m in ladder]
    return {"m_star": m_star, "censored": m_star is None, "nonmonotone": False, "synced": syn, "lyap_obs": [(-1.0 if s else 1.0) for s in syn],
            "initial_spreading_rate": [float(len(ladder) - i) for i in range(len(ladder))]}


def _world(name, n, nu, cells_spec, ladder=(4, 8, 16, 32), refused=False, t1=1e-16, t2=0.02, all_hold=1e-12, none_final=0.9):
    L = list(ladder); tests = []
    for j, spec in enumerate(cells_spec):
        obs = {k: _obs(spec.get(k), L) for k in GRADED + ("SENS",)}
        for r in range(3):
            obs[f"RANDOM{r}"] = _obs(spec.get("RANDOM"), L)
        tests.append({"index": j, "observers": obs, "all_hold_max": all_hold, "none_final": none_final, "mu_record": {}, "dt_half": {}})
    rk = [[i + 1, 0] for i in range(64)]
    w = {"name": name, "n": n, "nu": nu, "ladder": L, "tests": [] if refused else tests, "rankings": {k: rk for k in GRADED + ("SENS",)},
         "theorem_checks": [{"T1_ratio": t1, "first_octave_max_read": 1.0, "T2_ratio": t2}]}
    if refused: w["refused"] = "stability"
    return w


def selftest() -> int:
    fails = 0; tols = {"M1": 0.5, "TOL_N": 0.3}

    def check(label, res, expect):
        nonlocal fails
        g = grade({"seed_role": "run", "worlds": res}, tols)["gate"]; ok = g.startswith(expect)
        print(f"{label}: {g}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    good = {"READ": 8, "BALL": 16, "ENSTROPHY": 16, "KE": 32, "SENS": 16, "RANDOM": None}
    worlds = lambda spec, **kw: [_world(f"w{n}_{nu}", n, nu, [spec] * 4, **kw) for nu in (0.004, 0.002) for n in (96, 128)]  # noqa: E731
    check("READ one step ahead of every control everywhere", worlds(good), "PASS")
    check("READ level with the best control", worlds({**good, "READ": 16}), "INDETERMINATE")
    check("READ one step behind everywhere", worlds({**good, "READ": 32}), "FAIL")
    check("READ censored, controls synchronize (shortfall 2 steps)", worlds({**good, "READ": None}), "FAIL")
    lb = [good, good, good, {**good, "BALL": None, "ENSTROPHY": None, "KE": None}]
    check("READ synchronizes where all controls are censored in one cell (lower bound)", [_world(f"w{n}_{nu}", n, nu, lb) for nu in (0.004, 0.002) for n in (96, 128)], "PASS")
    check("all controls censored everywhere (outside the ladder, E2)", worlds({**good, "BALL": None, "ENSTROPHY": None, "KE": None}), "INDETERMINATE (E2")
    check("all graded observers censored (uninformative, E2)", worlds({k: None for k in good}), "INDETERMINATE (E2")
    check("the best control no better than RANDOM (E2)", worlds({**good, "BALL": 32, "ENSTROPHY": 32, "KE": 32, "RANDOM": 32}), "INDETERMINATE (E2")
    check("READ no better than RANDOM is graded, not out of scope", worlds({**good, "READ": None}), "FAIL")
    check("T1 miss stops the gate", worlds(good, t1=1e-6), "FAIL (a proposition")
    check("T2 miss stops the gate", worlds(good, t2=1.5), "FAIL (a proposition")
    check("E1 miss (everything observed does not synchronize)", worlds(good, all_hold=1e-3), "INDETERMINATE (E1")
    ws = worlds(good); ws[0] = _world("w96_0.004", 96, 0.004, [], refused=True)
    check("a refused world", ws, "INDETERMINATE (a world refused")
    ws = [_world(f"w{n}_{nu}", n, nu, [good if n == 96 else {**good, "READ": 4}] * 4) for nu in (0.004, 0.002) for n in (96, 128)]
    check("advantage changes by one step between resolutions (N1)", ws, "INDETERMINATE")
    mix = [good, good, good, {**good, "READ": 32}]
    check("one cell behind by one step, pooled 0.5 (L1 edge)", [_world(f"w{n}_{nu}", n, nu, mix) for nu in (0.004, 0.002) for n in (96, 128)], "PASS")
    g = grade({"seed_role": "pilot", "worlds": worlds(good)}, tols)["gate"]; ok = g.startswith("PILOT GRADE, NOT A VERDICT: PASS")
    print(f"pilot label: {g}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv: return 1 if selftest() else 0
    path = argv[0]; tols = json.load(open(argv[argv.index("--tols") + 1], encoding="utf-8-sig"))
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    g = grade(json.load(open(path, encoding="utf-8-sig")), tols); text = json.dumps(g, indent=1, default=float)
    if outp:
        open(outp, "w", encoding="utf-8").write(text + "\n")
    print(text); return 0


if __name__ == "__main__":
    sys.exit(main())
