"""D1: identifiability at a budget, finite-sample form.

Theorem 2 of `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`:
at budget B a direction v is identifiable for perturbations of size rho exactly when
v^T P v > B^2 / rho^2, so the number of identifiable eigen-directions is
d_obs(B, rho) = #{i : lambda_i > B^2 / rho^2}. The gate gives an estimator only the
distinguishability oracle, whether a perturbation of size rho in a random direction is
distinguishable from the base state at budget B, and asks what it recovers.

Estimator. The read operator is the ellipsoid {delta : delta^T P delta <= B^2}, so the oracle
answers are membership queries on an ellipsoid, and the max-margin semidefinite program of GET
Theorem 3(a) recovers it: maximise t over P_hat positive semidefinite subject to
delta_i^T P_hat delta_i >= B^2 (1 + t) for distinguishable queries and <= B^2 (1 - t) for
indistinguishable ones. The scale is fixed by B^2, so nothing is normalised. Directions whose
true eigenvalue is above B^2 / rho^2 have the ellipsoid's boundary inside the query sphere and
are pinned from both sides; directions below it are only bounded above, which is what the
theorem calls unrevealed.

Predictions graded (per cell, medians over evaluators relative to chance as in G5):
P1 the number of recovered directions, eigenvalues of P_hat within tolerance of an eigenvalue
   of P above the threshold in the matching eigenspace, equals d_obs(B, rho);
P2 above-threshold eigenvalues and eigenspaces are recovered (error a small fraction of chance);
P3 below-threshold eigenvalues are unrevealed (error at chance) and never estimated above
   the threshold beyond tolerance;
P4 kernel directions are unrevealed and never estimated above the threshold;
P5 recovery improves monotonically with the number of queries.

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
    """A read operator with the given eigenvalues (zeros allowed) in a random orthonormal frame.
    Returns P, its eigenvalues (descending), and the frame (columns)."""
    V, _ = np.linalg.qr(rng.normal(size=(n, n)))
    lam = np.array(sorted(spectrum, reverse=True), dtype=float)
    P = V @ np.diag(lam) @ V.T
    return 0.5 * (P + P.T), lam, V


def oracle(P: np.ndarray, B: float, deltas: np.ndarray) -> np.ndarray:
    """Distinguishable at budget B: delta^T P delta > B^2."""
    return np.einsum("ij,jk,ik->i", deltas, P, deltas) > B ** 2


def queries(n: int, rho: float, n_q: int, rng: np.random.Generator) -> np.ndarray:
    u = rng.normal(size=(n_q, n)); u /= np.linalg.norm(u, axis=1, keepdims=True)
    return rho * u


# ----------------------------------------------------------------------------- estimator

def estimate(deltas: np.ndarray, answers: np.ndarray, B: float, solver: str | None = "CLARABEL") -> np.ndarray:
    import cvxpy as cp
    n = deltas.shape[1]
    P = cp.Variable((n, n), PSD=True)
    t = cp.Variable()
    cons = []
    for d, a in zip(deltas, answers):
        q = cp.quad_form(d, P)
        cons.append(q >= B ** 2 * (1 + t) if a else q <= B ** 2 * (1 - t))
    cons.append(t <= 1.0)
    prob = cp.Problem(cp.Maximize(t), cons)
    for s in (solver, "SCS"):
        try:
            prob.solve(solver=s)
        except cp.error.SolverError:
            continue
        if P.value is not None:
            break
    if P.value is None:
        raise RuntimeError(f"program returned no point: {prob.status}")
    Ph = np.asarray(P.value); return 0.5 * (Ph + Ph.T)


# ----------------------------------------------------------------------------- errors

def analyse(P: np.ndarray, lam: np.ndarray, V: np.ndarray, Ph: np.ndarray, B: float, rho: float, tol: float) -> dict:
    """Per true eigen-direction: the estimated form along it and its relative error; the count of
    recovered directions; the estimated operator's own spectrum above the threshold."""
    thr = B ** 2 / rho ** 2
    est_along = np.array([V[:, i] @ Ph @ V[:, i] for i in range(len(lam))])
    above = lam > thr
    kernel = lam <= 1e-12
    below = (~above) & (~kernel)
    rel_err = np.abs(est_along - lam) / np.maximum(lam, thr)
    recovered = above & (rel_err <= tol)
    d_obs = int(above.sum())
    # estimated count: eigenvalues of P_hat above the threshold by more than tol
    eh = np.linalg.eigvalsh(Ph)
    d_est = int((eh > thr * (1 + tol)).sum())
    # eigenspace agreement for the above-threshold block: principal angle between true and
    # estimated top-d_obs subspaces
    angle = 0.0
    if d_obs > 0:
        Uh = np.linalg.eigh(Ph)[1][:, ::-1][:, :d_obs]
        s = np.linalg.svd(V[:, :d_obs].T @ Uh, compute_uv=False)
        angle = float(np.degrees(np.arccos(np.clip(s.min(), -1, 1))))
    return {"threshold": thr, "d_obs": d_obs, "d_est": d_est, "count_matches": bool(d_est == d_obs),
            "above_rel_err": [float(x) for x in rel_err[above]],
            "below_rel_err": [float(x) for x in rel_err[below]],
            "below_est_over_threshold": [float(x / thr) for x in est_along[below]],
            "kernel_est_over_threshold": [float(x / thr) for x in est_along[kernel]],
            "above_recovered_fraction": float(recovered.sum() / max(above.sum(), 1)) if above.any() else float("nan"),
            "below_pushed_above": bool(np.any(est_along[below] > thr * (1 + tol))) if below.any() else False,
            "kernel_pushed_above": bool(np.any(est_along[kernel] > thr * (1 + tol))) if kernel.any() else False,
            "top_subspace_angle_deg": angle}


def chance(lam: np.ndarray, V: np.ndarray, B: float, rho: float, tol: float, rng: np.random.Generator, n_draws: int = 64) -> dict:
    """The same analysis for a guess from the operator prior with the same spectrum in a random
    frame, the reference for 'no better than chance'."""
    n = len(lam); rows = []
    for _ in range(n_draws):
        Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
        Pr = Q @ np.diag(lam) @ Q.T
        rows.append(analyse(Pr, lam, V, Pr, B, rho, tol))
    out = {}
    for key in ("above_rel_err", "below_rel_err"):
        vals = [x for r in rows for x in r[key]]
        out[key] = float(np.median(vals)) if vals else float("nan")
    out["count_matches"] = float(np.mean([r["count_matches"] for r in rows]))
    out["top_subspace_angle_deg"] = float(np.median([r["top_subspace_angle_deg"] for r in rows]))
    return out


# ----------------------------------------------------------------------------- cells

def run_cells(cfg: dict, seed: int, out_path: str) -> dict:
    rng = np.random.default_rng(seed)
    tol = float(cfg["recovery_tolerance"])
    rho = float(cfg["rho"])
    result = {"config": cfg, "seed": seed, "cells": [], "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    for world in cfg["worlds"]:
        n = int(world["n"]); spectrum = [float(x) for x in world["spectrum"]]
        for B in cfg["budget_ladder"]:
            for n_q in cfg["query_ladder"]:
                rows = []; t0 = time.time()
                for e in range(int(cfg["evaluators_per_cell"])):
                    P, lam, V = make_operator(n, spectrum, rng)
                    D = queries(n, rho, int(n_q), rng)
                    ans = oracle(P, float(B), D)
                    if ans.all() or (~ans).all():
                        rows.append({"skipped": True, "reason": "oracle constant"}); continue
                    try:
                        Ph = estimate(D, ans, float(B), cfg.get("solver", "CLARABEL"))
                    except RuntimeError as ex:
                        rows.append({"skipped": True, "reason": f"solver: {ex}"}); continue
                    r = analyse(P, lam, V, Ph, float(B), rho, tol)
                    r["chance"] = chance(lam, V, float(B), rho, tol, np.random.default_rng(seed + 31 * e + 7 * int(n_q) + 3 * n))
                    r["n_distinguishable"] = int(ans.sum())
                    rows.append(r)
                good = [r for r in rows if not r.get("skipped")]
                summ = {}
                if good:
                    summ = {"count_match_fraction": float(np.mean([r["count_matches"] for r in good])),
                            "d_obs": good[0]["d_obs"],
                            "above_rel_err_median": float(np.median([x for r in good for x in r["above_rel_err"]])) if any(r["above_rel_err"] for r in good) else float("nan"),
                            "below_rel_err_median": float(np.median([x for r in good for x in r["below_rel_err"]])) if any(r["below_rel_err"] for r in good) else float("nan"),
                            "chance_above_rel_err": float(np.median([r["chance"]["above_rel_err"] for r in good])),
                            "chance_below_rel_err": float(np.median([r["chance"]["below_rel_err"] for r in good])),
                            "below_pushed_above_fraction": float(np.mean([r["below_pushed_above"] for r in good])),
                            "kernel_pushed_above_fraction": float(np.mean([r["kernel_pushed_above"] for r in good])),
                            "top_angle_median": float(np.median([r["top_subspace_angle_deg"] for r in good])),
                            "chance_top_angle": float(np.median([r["chance"]["top_subspace_angle_deg"] for r in good])),
                            "n_graded": len(good)}
                cell = {"world": world["name"], "n": n, "spectrum": spectrum, "B": float(B), "n_queries": int(n_q),
                        "rows": rows, "summary": summ, "seconds": time.time() - t0}
                result["cells"].append(cell)
                print(json.dumps({"world": world["name"], "B": float(B), "n_q": int(n_q), **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in summ.items()}}))
                json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


# ----------------------------------------------------------------------------- self test

def selftest() -> int:
    """With a spectrum straddling the threshold and a kernel, many queries must recover the
    above-threshold eigenvalues, leave the below-threshold and kernel ones unrevealed and never
    above the threshold, and count exactly d_obs; the count must fall as the budget grows."""
    import cvxpy  # noqa: F401
    rng = np.random.default_rng(0)
    n, rho, tol = 5, 1.0, 0.25
    spectrum = [4.0, 2.0, 0.5, 0.1, 0.0]
    fails = 0
    counts = []
    for B in (0.5, 1.0, 1.5):
        P, lam, V = make_operator(n, spectrum, rng)
        D = queries(n, rho, 600, rng); ans = oracle(P, B, D)
        Ph = estimate(D, ans, B)
        r = analyse(P, lam, V, Ph, B, rho, tol)
        counts.append((B, r["d_obs"], r["d_est"]))
        print(f"B={B}: threshold {r['threshold']:.2f} d_obs {r['d_obs']} d_est {r['d_est']} above err {[round(x,3) for x in r['above_rel_err']]} below est/thr {[round(x,2) for x in r['below_est_over_threshold']]} kernel est/thr {[round(x,2) for x in r['kernel_est_over_threshold']]} angle {r['top_subspace_angle_deg']:.1f}")
        if not r["count_matches"]:
            print("FAIL count"); fails += 1
        if r["above_rel_err"] and max(r["above_rel_err"]) > tol:
            print("FAIL above-threshold recovery"); fails += 1
        if r["below_pushed_above"] or r["kernel_pushed_above"]:
            print("FAIL an unrevealed direction was estimated above the threshold"); fails += 1
    if not all(counts[i][2] >= counts[i + 1][2] for i in range(len(counts) - 1)):
        print("FAIL count not antitone in the budget"); fails += 1
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
