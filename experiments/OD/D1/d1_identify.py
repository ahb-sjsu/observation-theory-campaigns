"""D1: identifiability at a budget, finite-sample form. Second design (2026-09-09).

Theorem 2 of `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`
(machine-checked in `lean/GET/Identifiability.lean`): a perturbation of size rho along a
direction v is distinguishable at budget B exactly when v^T P v > B^2 / rho^2. The theorem is a
statement about one direction at a time. The first pilot of this gate showed what that means in
finite samples: queries in random directions on the sphere of radius rho trace the ellipsoid
{delta : delta^T P delta = B^2} wherever the sphere crosses it, and that pins every eigenvalue,
including those below the threshold. So the gate has two worlds.

World A, single-parameter probes. The experimenter perturbs one coordinate at a time, in a
declared basis that is not the eigenbasis, by sizes on a ladder, and reads the oracle. This is the
identifiability setting of inverse problems. Prediction: parameter i is reported identifiable at
(B, rho) exactly when P_ii > B^2 / rho^2, the count equals d_obs in that basis, the diagonal
entries are bracketed by the size ladder to within its resolution, and nothing about the
off-diagonal entries is revealed (any operator with the same diagonal answers every query the
same way, so the off-diagonal error of a consistent estimate is at chance).

World B, mixed probes. Queries in random directions at radius rho. Prediction: when
lambda_min rho^2 < B^2 < lambda_max rho^2, with lambda_min the smallest eigenvalue including
zero, the consistent estimator recovers every eigenvalue, above and below the threshold, with
error falling as queries grow, in cells where the crossing is substantial (both oracle answers
in at least a tenth of the queries); when B^2 lies outside that interval the oracle is constant
and nothing is recovered. The estimator is the analytic centre of the set of positive
semidefinite operators consistent with the answers, inside a declared cap on the operator norm,
a canonical point of the feasible set.

    python d1_identify.py --selftest
    python d1_identify.py --config prereg_config.json --seed-role pilot --out pilot.json
    python d1_identify.py --config prereg_config.json --seed-role run --out results.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np


# ----------------------------------------------------------------------------- world

def make_operator(n: int, spectrum: list[float], rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    V, _ = np.linalg.qr(rng.normal(size=(n, n)))
    lam = np.array(sorted(spectrum, reverse=True), dtype=float)
    P = V @ np.diag(lam) @ V.T
    return 0.5 * (P + P.T), lam, V


def oracle(P: np.ndarray, B: float, deltas: np.ndarray) -> np.ndarray:
    return np.einsum("ij,jk,ik->i", deltas, P, deltas) > B ** 2


# ----------------------------------------------------------------------------- world A

def axis_probe(P: np.ndarray, B: float, rho_ladder: list[float]) -> dict:
    """One coordinate at a time, both signs, every size on the ladder. Returns per coordinate the
    largest size at which the oracle said indistinguishable and the smallest at which it said
    distinguishable, hence a bracket on P_ii, and the identifiability verdict at the largest
    size (the gate's rho)."""
    n = P.shape[0]
    rho_max = max(rho_ladder)
    out = {"identifiable": [], "bracket_lo": [], "bracket_hi": [], "true_diag": [float(P[i, i]) for i in range(n)]}
    for i in range(n):
        lo, hi = 0.0, float("inf")
        for r in rho_ladder:
            d = np.zeros((2, n)); d[0, i] = r; d[1, i] = -r
            dist = oracle(P, B, d)
            if dist.any():                       # distinguishable at size r: P_ii > B^2 / r^2
                lo = max(lo, B ** 2 / r ** 2)
            else:                                # indistinguishable at size r: P_ii <= B^2 / r^2
                hi = min(hi, B ** 2 / r ** 2)
        e = np.zeros((1, n)); e[0, i] = rho_max
        out["identifiable"].append(bool(oracle(P, B, e)[0]))
        out["bracket_lo"].append(lo); out["bracket_hi"].append(hi)
    return out


def analyse_axis(P: np.ndarray, B: float, rho: float, probe: dict) -> dict:
    n = P.shape[0]; thr = B ** 2 / rho ** 2
    diag = np.diag(P)
    pred = [bool(diag[i] > thr) for i in range(n)]
    d_obs = int(sum(pred))
    d_rep = int(sum(probe["identifiable"]))
    inside = [probe["bracket_lo"][i] <= diag[i] <= probe["bracket_hi"][i] for i in range(n)]
    # off-diagonal unrevealed: the answers depend on the diagonal only; a consistent estimate is
    # the diagonal bracket midpoint with zero off-diagonal, whose off-diagonal error equals the
    # true off-diagonal mass, and chance is the same mass for a random frame with this spectrum
    off_true = float(np.linalg.norm(P - np.diag(diag)))
    return {"threshold": thr, "d_obs": d_obs, "d_reported": d_rep, "count_matches": bool(d_obs == d_rep),
            "verdicts_match": bool(pred == probe["identifiable"]), "bracket_holds_all": bool(all(inside)),
            "off_diagonal_mass": off_true}


# ----------------------------------------------------------------------------- world B

def queries(n: int, rho: float, n_q: int, rng: np.random.Generator) -> np.ndarray:
    u = rng.normal(size=(n_q, n)); u /= np.linalg.norm(u, axis=1, keepdims=True)
    return rho * u


def estimate(deltas: np.ndarray, answers: np.ndarray, B: float, solver: str | None = "CLARABEL",
             cap: float = 1000.0, rho: float = 1.0) -> np.ndarray:
    """Analytic centre of the set of positive semidefinite operators consistent with the answers,
    inside the declared cap P <= cap * (B^2 / rho^2) * I, which keeps the set bounded where the
    answers bound a direction only from below."""
    import cvxpy as cp
    n = deltas.shape[1]

    def solve(prob):
        for s in (solver, "SCS"):
            try:
                prob.solve(solver=s)
            except cp.error.SolverError:
                continue
            if prob.value is not None and prob.status in ("optimal", "optimal_inaccurate"):
                return True
        return False

    # analytic center of the feasible set: maximise the summed log slacks of every answer,
    # slack = (q - B^2) / B^2 for a distinguishable query and (B^2 - q) / B^2 otherwise
    P = cp.Variable((n, n), PSD=True)
    forms = [cp.quad_form(d, P) / B ** 2 for d in deltas]
    slacks = cp.hstack([(f - 1.0) if a else (1.0 - f) for f, a in zip(forms, answers)])
    thr = B ** 2 / rho ** 2
    cons = [cap * thr * np.eye(n) - P >> 0]
    if not solve(cp.Problem(cp.Maximize(cp.sum(cp.log(slacks))), cons)):
        raise RuntimeError("analytic-centre program failed")
    Ph = np.asarray(P.value); return 0.5 * (Ph + Ph.T)


def analyse_mixed(P: np.ndarray, lam: np.ndarray, V: np.ndarray, Ph: np.ndarray, B: float, rho: float) -> dict:
    """Relative error of every eigenvalue along the true eigenvectors, split above and below the
    threshold, the top-subspace angle, and whether the sphere crosses the ellipsoid."""
    thr = B ** 2 / rho ** 2
    est_along = np.array([V[:, i] @ Ph @ V[:, i] for i in range(len(lam))])
    rel = np.abs(est_along - lam) / np.maximum(lam, thr)
    above = lam > thr; below = ~above
    # the sphere of radius rho crosses the ellipsoid (a cylinder along the kernel) exactly when
    # the smallest eigenvalue, zero included, sits below the threshold and the largest above it
    crossing = bool((lam.min() * rho ** 2 < B ** 2) and (B ** 2 < lam.max() * rho ** 2))
    d_obs = int(above.sum())
    angle = 0.0
    if d_obs > 0:
        Uh = np.linalg.eigh(Ph)[1][:, ::-1][:, :d_obs]
        s = np.linalg.svd(V[:, :d_obs].T @ Uh, compute_uv=False)
        angle = float(np.degrees(np.arccos(np.clip(s.min(), -1, 1))))
    return {"threshold": thr, "d_obs": d_obs, "crossing": crossing,
            "above_rel_err": [float(x) for x in rel[above]], "below_rel_err": [float(x) for x in rel[below]],
            "all_rel_err_median": float(np.median(rel)), "top_subspace_angle_deg": angle,
            "frobenius_rel_err": float(np.linalg.norm(Ph - P) / np.linalg.norm(P))}


def chance_mixed(lam: np.ndarray, V: np.ndarray, B: float, rho: float, rng: np.random.Generator, n_draws: int = 64) -> dict:
    n = len(lam); rows = []
    for _ in range(n_draws):
        Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
        Pr = Q @ np.diag(lam) @ Q.T
        rows.append(analyse_mixed(V @ np.diag(lam) @ V.T, lam, V, Pr, B, rho))
    out = {}
    for key in ("above_rel_err", "below_rel_err"):
        vals = [x for r in rows for x in r[key]]
        out[key] = float(np.median(vals)) if vals else float("nan")
    out["all_rel_err_median"] = float(np.median([r["all_rel_err_median"] for r in rows]))
    out["frobenius_rel_err"] = float(np.median([r["frobenius_rel_err"] for r in rows]))
    out["top_subspace_angle_deg"] = float(np.median([r["top_subspace_angle_deg"] for r in rows]))
    return out


# ----------------------------------------------------------------------------- cells

def run_cells(cfg: dict, seed: int, out_path: str) -> dict:
    rng = np.random.default_rng(seed)
    rho = float(cfg["rho"]); ladder = [float(r) for r in cfg["axis_size_ladder"]]
    result = {"config": cfg, "seed": seed, "cells": [], "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    n_ev = int(cfg["evaluators_per_cell"])
    for world in cfg["worlds"]:
        n = int(world["n"]); spectrum = [float(x) for x in world["spectrum"]]
        for B in cfg["budget_ladder"]:
            # world A
            rows = []; t0 = time.time()
            for e in range(n_ev):
                P, lam, V = make_operator(n, spectrum, rng)
                r = analyse_axis(P, float(B), rho, axis_probe(P, float(B), ladder))
                Q, _ = np.linalg.qr(rng.normal(size=(n, n))); Pr = Q @ np.diag(lam) @ Q.T
                r["chance_off_diagonal_mass"] = float(np.linalg.norm(Pr - np.diag(np.diag(Pr))))
                rows.append(r)
            summA = {"count_match_fraction": float(np.mean([r["count_matches"] for r in rows])),
                     "verdicts_match_fraction": float(np.mean([r["verdicts_match"] for r in rows])),
                     "bracket_holds_fraction": float(np.mean([r["bracket_holds_all"] for r in rows])),
                     "d_obs_median": float(np.median([r["d_obs"] for r in rows]))}
            result["cells"].append({"world": world["name"], "kind": "axis", "n": n, "B": float(B), "rows": rows, "summary": summA, "seconds": time.time() - t0})
            print(json.dumps({"world": world["name"], "kind": "axis", "B": float(B), **{k: round(v, 3) for k, v in summA.items()}}))
            # world B
            for n_q in cfg["query_ladder"]:
                rows = []; t0 = time.time()
                for e in range(n_ev):
                    P, lam, V = make_operator(n, spectrum, rng)
                    D = queries(n, rho, int(n_q), rng); ans = oracle(P, float(B), D)
                    if ans.all() or (~ans).all():
                        rows.append({"skipped": True, "reason": "oracle constant", "crossing": False}); continue
                    try:
                        Ph = estimate(D, ans, float(B), cfg.get("solver", "CLARABEL"), float(cfg.get("cap", 1000.0)), rho)
                    except RuntimeError as ex:
                        rows.append({"skipped": True, "reason": str(ex)}); continue
                    r = analyse_mixed(P, lam, V, Ph, float(B), rho)
                    r["answer_balance"] = float(min(ans.mean(), 1.0 - ans.mean()))
                    r["chance"] = chance_mixed(lam, V, float(B), rho, np.random.default_rng(seed + 31 * e + 7 * int(n_q) + 3 * n))
                    r["n_distinguishable"] = int(ans.sum())
                    rows.append(r)
                good = [r for r in rows if not r.get("skipped")]
                summ = {"n_graded": len(good), "n_skipped_constant": sum(1 for r in rows if r.get("reason") == "oracle constant")}
                if good:
                    bal = float(np.median([r["answer_balance"] for r in good]))
                    summ.update({"crossing": bool(good[0]["crossing"]),
                                 "answer_balance_median": bal,
                                 "well_crossed": bool(bal >= float(cfg.get("well_crossed_min_balance", 0.1)) and len(good) >= 0.9 * n_ev),
                                 "above_rel_err_median": float(np.median([x for r in good for x in r["above_rel_err"]])) if any(r["above_rel_err"] for r in good) else float("nan"),
                                 "below_rel_err_median": float(np.median([x for r in good for x in r["below_rel_err"]])) if any(r["below_rel_err"] for r in good) else float("nan"),
                                 "chance_above": float(np.median([r["chance"]["above_rel_err"] for r in good])),
                                 "chance_below": float(np.median([r["chance"]["below_rel_err"] for r in good])),
                                 "frobenius_median": float(np.median([r["frobenius_rel_err"] for r in good])),
                                 "chance_frobenius": float(np.median([r["chance"]["frobenius_rel_err"] for r in good])),
                                 "angle_median": float(np.median([r["top_subspace_angle_deg"] for r in good])),
                                 "chance_angle": float(np.median([r["chance"]["top_subspace_angle_deg"] for r in good]))})
                result["cells"].append({"world": world["name"], "kind": "mixed", "n": n, "B": float(B), "n_queries": int(n_q), "rows": rows, "summary": summ, "seconds": time.time() - t0})
                print(json.dumps({"world": world["name"], "kind": "mixed", "B": float(B), "n_q": int(n_q), **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in summ.items()}}))
                json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


# ----------------------------------------------------------------------------- self test

def selftest() -> int:
    import cvxpy  # noqa: F401
    rng = np.random.default_rng(0)
    fails = 0
    n, rho = 5, 1.0
    spectrum = [4.0, 2.0, 0.5, 0.1, 0.0]
    ladder = [0.125, 0.25, 0.5, 1.0]
    # world A: verdicts and brackets exact by the theorem
    for B in (0.5, 1.0):
        P, lam, V = make_operator(n, spectrum, rng)
        r = analyse_axis(P, B, rho, axis_probe(P, B, ladder))
        print(f"axis B={B}: d_obs {r['d_obs']} reported {r['d_reported']} verdicts match {r['verdicts_match']} bracket holds {r['bracket_holds_all']}")
        if not (r["verdicts_match"] and r["bracket_holds_all"]):
            print("FAIL world A"); fails += 1
    # world B: crossing -> every eigenvalue recovered; no crossing -> oracle constant
    for B in (0.5, 1.0, 1.5, 2.5):
        P, lam, V = make_operator(n, spectrum, rng)
        D = queries(n, rho, 800, rng); ans = oracle(P, B, D)
        if ans.all() or (~ans).all():
            print(f"mixed B={B}: oracle constant (crossing expected False)")
            if lam.min() < B ** 2 < lam.max():
                print("FAIL constant oracle inside the crossing interval"); fails += 1
            continue
        Ph = estimate(D, ans, B, rho=rho)
        r = analyse_mixed(P, lam, V, Ph, B, rho)
        print(f"mixed B={B}: crossing {r['crossing']} above {[round(x,3) for x in r['above_rel_err']]} below {[round(x,3) for x in r['below_rel_err']]} frob {r['frobenius_rel_err']:.3f}")
        # recovery under crossing is slow when B^2 is small against the typical form on the
        # sphere, since few queries land near the boundary; the logic check is 'well below chance'
        # (chance for this spectrum in a random frame is about 0.7), the pilot sets the bars
        if r["crossing"] and r["frobenius_rel_err"] > 0.35:
            print("FAIL recovery under crossing"); fails += 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config"); ap.add_argument("--out", default="results.json")
    ap.add_argument("--seed-role", choices=["pilot", "run"], default="run")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    cfg = json.load(open(a.config, encoding="utf-8"))
    seed = int(cfg["seed_pilot"] if a.seed_role == "pilot" else cfg["seed_run"])
    run_cells(cfg, seed, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
