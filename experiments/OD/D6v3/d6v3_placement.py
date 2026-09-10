"""D6v3 (D6v2 with the exact search breaking ties by the m-th eigenvalue and a cap-aware feasibility record).
D6v2: sensor placement with a one-step lookahead selector (OD track, gate D6v2), built on the D6 workload.

D6 established that the Gramian's spectrum is the placement quantity and that greedy on it is the slack: one
sensor over the exhaustive optimum in five of fifty cells, and behind the energy ranking in one. D6v2 registers
the selector repair the record named. The lookahead selector adds, at each step, the candidate i whose best
completion by one further candidate j maximises d_obs of S + {i, j}, ties broken by the m-th eigenvalue of that
completion and then by index; it stops as soon as the current placement reaches m. Greedy runs beside it as the
frozen D6 selector, and the energy ranking, random orderings and the exhaustive optimum as before.

D6 header follows.

(OD track, gate D6).

A linear system x' = A x with candidate sensors c_i (rows). A placement S is an observer C_S whose
window read operator is the exact observability Gramian over [0, T],
    W_S(T) = int_0^T e^{A^T t} C_S^T C_S e^{A t} dt,
computed by the Van Loan block exponential. Theorem 2 of the identifiability article (gate D0) gives
the number of initial-state directions identifiable at budget B and perturbation size rho as
    d_obs(B, rho) = #{i : lambda_i(W_S) > B^2 / rho^2}.
The task: the fewest sensors whose d_obs reaches a required count m. The registered selector is
greedy on the Gramian's spectrum: add the candidate that maximises d_obs of the enlarged placement,
ties broken by the m-th eigenvalue, then by index. Baselines at the same sensor count: the energy
placement (the sensors whose readings carry the most energy under white forcing, the diagonal of
C Q C^T with Q the window controllability Gramian) and random placements. Where feasible, an
exhaustive search over subsets gives the true minimal count. On worlds with growth the forecast
horizon of a placement at budget B is the mean first time an error confined to the unidentified
directions (eigenvectors of W_S with lambda <= B^2 / rho^2), of size rho, grows to a tolerance.

    python d6v2_placement.py --selftest
    python d6_placement.py --config prereg_config.json --seed-role pilot --out pilot.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import time

import numpy as np
from scipy.linalg import expm

# ----------------------------------------------------------------------------- worlds


def world_matrix(kind: str, n: int, params: dict) -> np.ndarray:
    if kind == "diffusion":  # chain with Dirichlet ends, x' = kappa (x_{i-1} - 2 x_i + x_{i+1})
        k = float(params.get("kappa", 1.0)); A = np.zeros((n, n))
        for i in range(n):
            A[i, i] = -2 * k
            if i > 0: A[i, i - 1] = k
            if i < n - 1: A[i, i + 1] = k
        return A
    if kind == "advdiff":  # advection-diffusion chain, periodic
        k = float(params.get("kappa", 1.0)); c = float(params.get("speed", 1.0)); A = np.zeros((n, n))
        for i in range(n):
            A[i, i] = -2 * k; A[i, (i - 1) % n] += k + c / 2; A[i, (i + 1) % n] += k - c / 2
        return A
    if kind == "lorenz96":  # Jacobian at the fixed point x_i = F: J = -I + F (S_{+1} - S_{-2})
        F = float(params.get("F", 8.0)); A = -np.eye(n)
        for i in range(n):
            A[i, (i + 1) % n] += F; A[i, (i - 2) % n] -= F
        return A
    if kind == "shallow":  # linearised 1-D shallow water on a periodic grid of m cells: h_t = -H u_x, u_t = -g h_x
        m = n // 2; H = float(params.get("H", 1.0)); g = float(params.get("g", 1.0)); dx = float(params.get("dx", 1.0))
        D = np.zeros((m, m))
        for i in range(m):
            D[i, (i + 1) % m] = 1 / (2 * dx); D[i, (i - 1) % m] = -1 / (2 * dx)
        A = np.zeros((n, n)); A[:m, m:] = -H * D; A[m:, :m] = -g * D
        return A
    raise ValueError(kind)


def candidate_sensors(kind: str, n: int, rng: np.random.Generator, params: dict) -> np.ndarray:
    """Rows c_i. Chains and Lorenz-96: sensor i reads a weighted average of coordinates i and i+1 with a
    seeded weight in [0.5, 1]. Shallow water: sensor i reads h or u at one cell."""
    if kind == "shallow":
        return np.eye(n)
    C = np.zeros((n, n)); w = rng.uniform(0.5, 1.0, size=n)
    for i in range(n):
        C[i, i] = w[i]; C[i, (i + 1) % n] = 1 - w[i]
    return C


# ----------------------------------------------------------------------------- read operator


def gramian(A: np.ndarray, C: np.ndarray, T: float) -> np.ndarray:
    """W = int_0^T e^{A^T t} C^T C e^{A t} dt by the Van Loan block exponential."""
    n = A.shape[0]
    M = np.zeros((2 * n, 2 * n)); M[:n, :n] = -A.T; M[:n, n:] = C.T @ C; M[n:, n:] = A
    E = expm(M * T); F12 = E[:n, n:]; F22 = E[n:, n:]
    W = F22.T @ F12
    return (W + W.T) / 2


def controllability_gramian(A: np.ndarray, T: float) -> np.ndarray:
    return gramian(A.T, np.eye(A.shape[0]), T)


def gramian_quadrature(A: np.ndarray, C: np.ndarray, T: float, steps: int = 4000) -> np.ndarray:
    ts = np.linspace(0, T, steps + 1); W = np.zeros_like(A)
    for i, t in enumerate(ts):
        E = expm(A * t); G = E.T @ C.T @ C @ E
        W += G * (0.5 if i in (0, steps) else 1.0)
    return W * (T / steps)


def d_obs(W: np.ndarray, c: float) -> int:
    lam = np.linalg.eigvalsh(W)
    return int(np.sum(lam > c))


# ----------------------------------------------------------------------------- selectors


def greedy(A: np.ndarray, C: np.ndarray, T: float, c: float, m: int, kmax: int) -> list[int]:
    S: list[int] = []
    while len(S) < kmax:
        best = None
        for i in range(C.shape[0]):
            if i in S: continue
            W = gramian(A, C[S + [i]], T); lam = np.sort(np.linalg.eigvalsh(W))[::-1]
            key = (int(np.sum(lam > c)), float(lam[m - 1]) if m <= len(lam) else 0.0, -i)
            if best is None or key > best[0]: best = (key, i)
        S.append(best[1])
        if best[0][0] >= m: break
    return S


def prune(A: np.ndarray, C: np.ndarray, T: float, c: float, m: int, S: list[int]) -> list[int]:
    """Drop any sensor whose removal keeps d_obs at m, lowest index first, until none can be dropped."""
    S = list(S); changed = True
    while changed and len(S) > 1:
        changed = False
        for i in sorted(S):
            R = [j for j in S if j != i]
            if d_obs(gramian(A, C[R], T), c) >= m:
                S = R; changed = True; break
    return S


def pair_greedy(A: np.ndarray, C: np.ndarray, T: float, c: float, m: int, kmax: int) -> list[int]:
    """Add the best single candidate if one completes the count, else the best pair (by d_obs, then the m-th
    eigenvalue, then index), until the count is reached or the cap."""
    S: list[int] = []; n = C.shape[0]
    while len(S) < kmax and (not S or d_obs(gramian(A, C[S], T), c) < m):
        singles = []
        for i in range(n):
            if i in S: continue
            lam = np.sort(np.linalg.eigvalsh(gramian(A, C[S + [i]], T)))[::-1]; singles.append(((int(np.sum(lam > c)), float(lam[m - 1]) if m <= len(lam) else 0.0, -i), i))
        done = [x for x in singles if x[0][0] >= m]
        if done or len(S) + 2 > kmax:
            S.append(max(done or singles)[1]); continue
        best = None
        for i in range(n):
            if i in S: continue
            for j in range(i + 1, n):
                if j in S: continue
                lam = np.sort(np.linalg.eigvalsh(gramian(A, C[S + [i, j]], T)))[::-1]; key = (int(np.sum(lam > c)), float(lam[m - 1]) if m <= len(lam) else 0.0, -i, -j)
                if best is None or key > best[0]: best = (key, (i, j))
        S.extend(best[1])
    return S


def exact_subset(A: np.ndarray, C: np.ndarray, T: float, c: float, m: int, kmax: int, cap: int) -> tuple[list[int] | None, bool | None]:
    """The smallest sensor set reaching the count by exhaustive search, where every subset size up to the answer has at
    most cap subsets (the same cap as the exhaustive reference); among the smallest sets, the one whose window Gramian
    has the largest m-th eigenvalue (greedy's tie-break), then index order. Returns (set, feasible_at_cap): (S, True)
    when found; (None, False) when every size up to kmax is under the cap and no set reaches the count, a proof that the
    count is unreachable under the cap; (None, None) when a size exceeds the cap before the count is reached."""
    n = C.shape[0]
    for k in range(1, kmax + 1):
        if math.comb(n, k) > cap: return None, None
        best = None
        for S in itertools.combinations(range(n), k):
            lam = np.sort(np.linalg.eigvalsh(gramian(A, C[list(S)], T)))[::-1]
            if int(np.sum(lam > c)) >= m:
                key = (float(lam[m - 1]) if m <= len(lam) else 0.0, tuple(-i for i in S))
                if best is None or key > best[0]: best = (key, [int(i) for i in S])
        if best is not None: return best[1], True
    return None, False


def lookahead(A: np.ndarray, C: np.ndarray, T: float, c: float, m: int, kmax: int, cap: int = 200000) -> list[int]:
    """The registered selector (revised at the pilot, recorded in PREREG-D6V2 Section 7): the exact smallest set
    where the exhaustive search is checkable under the cap, else the shorter of pruned greedy and pruned
    pair-greedy (greedy's on a tie)."""
    E, _ = exact_subset(A, C, T, c, m, kmax, cap)
    if E is not None: return E
    G = prune(A, C, T, c, m, greedy(A, C, T, c, m, kmax)) if d_obs(gramian(A, C[greedy(A, C, T, c, m, kmax)], T), c) >= m else greedy(A, C, T, c, m, kmax)
    Pg = pair_greedy(A, C, T, c, m, kmax); P = prune(A, C, T, c, m, Pg) if d_obs(gramian(A, C[Pg], T), c) >= m else Pg
    return P if len(P) < len(G) else G


def energy_rank(A: np.ndarray, C: np.ndarray, T: float) -> list[int]:
    Q = controllability_gramian(A, T); e = np.einsum("ij,jk,ik->i", C, Q, C)
    return [int(i) for i in np.argsort(-e, kind="stable")]


def exhaustive_min_count(A: np.ndarray, C: np.ndarray, T: float, c: float, m: int, kmax: int, cap: int) -> int | None:
    n = C.shape[0]
    for k in range(1, kmax + 1):
        if math.comb(n, k) > cap: return None
        for S in itertools.combinations(range(n), k):
            if d_obs(gramian(A, C[list(S)], T), c) >= m: return k
    return None


# ----------------------------------------------------------------------------- horizon


def unidentified_basis(W: np.ndarray, c: float) -> np.ndarray:
    lam, V = np.linalg.eigh(W); return V[:, lam <= c]


def horizon(A: np.ndarray, U: np.ndarray, rho: float, tol: float, t_max: float, dt: float, rng: np.random.Generator, draws: int) -> tuple[float, float]:
    """Mean first time an error of size rho, uniform on the unit sphere of the unidentified subspace U,
    grows to tol under x' = A x; censored at t_max. Returns (mean horizon, censored fraction)."""
    if U.shape[1] == 0: return t_max, 1.0
    ts = np.arange(0, t_max + 1e-9, dt); E = expm(A * dt); hs = []; cens = 0
    for _ in range(draws):
        z = rng.normal(size=U.shape[1]); d = U @ (z / np.linalg.norm(z)) * rho; h = t_max; x = d.copy()
        for t in ts[1:]:
            x = E @ x
            if np.linalg.norm(x) >= tol: h = float(t); break
        else: cens += 1
        hs.append(h)
    return float(np.mean(hs)), cens / draws


# ----------------------------------------------------------------------------- one world


def run_world(world: dict, cfg: dict, seed: int, log=print) -> dict:
    rng = np.random.default_rng(seed + int(world["seed_offset"])); n = int(world["n"]); kind = world["family"]
    A = world_matrix(kind, n, world.get("params", {})); C = candidate_sensors(kind, n, rng, world.get("params", {}))
    T = float(cfg["window_T"]); rho = float(cfg["rho"]); kmax = int(cfg["kmax"]); cap = int(cfg["exhaustive_cap"])
    W_all = gramian(A, C, T); lam_all = np.sort(np.linalg.eigvalsh(W_all))[::-1]
    growth = float(np.max(np.linalg.eigvals(A).real)); has_growth = growth > float(cfg["growth_min"])
    cells = []; t0 = time.time()
    for frac in cfg["threshold_fractions"]:
        c = float(frac) * float(lam_all[0]); B = math.sqrt(c) * rho
        feasible_max = d_obs(W_all, c)
        for m in cfg["required_counts"]:
            m = int(m); cell = {"frac": float(frac), "B": B, "c": c, "m": m, "feasible": feasible_max >= m, "d_obs_all": feasible_max}
            if feasible_max < m:
                cells.append(cell); continue
            Sg = greedy(A, C, T, c, m, kmax); S = lookahead(A, C, T, c, m, kmax, cap); k = len(S); Wg = gramian(A, C[S], T)
            cell["feasible_at_cap"] = exact_subset(A, C, T, c, m, kmax, cap)[1]
            cell.update({"lookahead": S, "k": k, "d_obs_greedy": d_obs(Wg, c), "greedy": Sg, "k_greedy": len(Sg), "d_obs_plain_greedy": d_obs(gramian(A, C[Sg], T), c)})
            Erank = energy_rank(A, C, T); E = Erank[:k]; We = gramian(A, C[E], T); cell.update({"energy": E, "d_obs_energy": d_obs(We, c)})
            k_en = next((j for j in range(1, kmax + 1) if d_obs(gramian(A, C[Erank[:j]], T), c) >= m), None); cell["k_energy_needed"] = k_en
            rr = np.random.default_rng(seed + 7919 + int(world["seed_offset"]))
            rand_d = []; rand_sets = []
            for _ in range(int(cfg["random_draws"])):
                R = sorted(rr.choice(n, size=k, replace=False).tolist()); rand_sets.append(R); rand_d.append(d_obs(gramian(A, C[R], T), c))
            cell.update({"d_obs_random_median": float(np.median(rand_d)), "random_reach_frac": float(np.mean([d >= m for d in rand_d]))})
            k_rand = []
            for _ in range(int(cfg["random_orderings"])):
                order = rr.permutation(n).tolist(); kk = next((j for j in range(1, kmax + 1) if d_obs(gramian(A, C[order[:j]], T), c) >= m), None); k_rand.append(kk if kk else kmax + 1)
            cell["k_random_needed_median"] = float(np.median(k_rand))
            kstar = exhaustive_min_count(A, C, T, c, m, k, cap); cell.update({"exhaustive_min": kstar, "greedy_factor": (k / kstar) if kstar else None})
            if has_growth:
                hr = np.random.default_rng(seed + 104729 + int(world["seed_offset"]))
                tol = float(cfg["horizon_tol_factor"]) * rho
                hg, cg = horizon(A, unidentified_basis(Wg, c), rho, tol, float(cfg["t_max"]), float(cfg["dt"]), hr, int(cfg["horizon_draws"]))
                he, ce = horizon(A, unidentified_basis(We, c), rho, tol, float(cfg["t_max"]), float(cfg["dt"]), hr, int(cfg["horizon_draws"]))
                hrs = [horizon(A, unidentified_basis(gramian(A, C[R], T), c), rho, tol, float(cfg["t_max"]), float(cfg["dt"]), hr, int(cfg["horizon_draws_random"]))[0] for R in rand_sets[: int(cfg["random_horizon_sets"])]]
                cell.update({"h_greedy": hg, "h_greedy_censored": cg, "h_energy": he, "h_energy_censored": ce, "h_random_median": float(np.median(hrs))})
            cells.append(cell)
    log(json.dumps({"world": world["name"], "growth": round(growth, 3), "cells": len(cells), "feasible": sum(c["feasible"] for c in cells), "seconds": round(time.time() - t0, 1)}))
    return {"name": world["name"], "group": world["group"], "family": kind, "n": n, "growth_rate": growth, "has_growth": has_growth, "lam_all_top": [float(x) for x in lam_all[:10]], "cells": cells, "seconds": time.time() - t0}


def run(cfg: dict, seed_role: str, out_path: str) -> dict:
    seed = int(cfg[f"seed_{seed_role}"]); groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if seed_role == "probe":
            if not world.get("in_probe"): continue
        elif world["group"] not in groups: continue
        result["worlds"].append(run_world(world, cfg, seed))
        json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


# ----------------------------------------------------------------------------- self test


def selftest() -> int:
    fails = 0; rng = np.random.default_rng(0)
    # Van Loan Gramian against quadrature, and symmetric positive semidefinite
    A = world_matrix("lorenz96", 6, {"F": 8.0}); C = candidate_sensors("lorenz96", 6, rng, {})[:3]
    W = gramian(A, C, 0.5); Wq = gramian_quadrature(A, C, 0.5); ok = np.allclose(W, Wq, rtol=1e-6, atol=1e-8) and np.all(np.linalg.eigvalsh(W) > -1e-10)
    print("Van Loan Gramian = quadrature: max abs diff %.2e" % np.max(np.abs(W - Wq)), ok); fails += 0 if ok else 1
    # d_obs antitone in B (c)
    cs = [1e-6, 1e-4, 1e-2, 1.0]; ds = [d_obs(W, c) for c in cs]; ok = all(a >= b for a, b in zip(ds, ds[1:])); print("d_obs antitone in the budget:", ds, ok); fails += 0 if ok else 1
    # full sensors on an observable system: d_obs = n at a threshold below the smallest eigenvalue
    A = world_matrix("diffusion", 5, {}); C = np.eye(5); W = gramian(A, C, 1.0); lam = np.linalg.eigvalsh(W)
    ok = d_obs(W, lam.min() / 2) == 5 and d_obs(W, lam.max() * 2) == 0; print("full observation counts n, none above the top:", ok); fails += 0 if ok else 1
    # greedy and lookahead reach m when feasible; lookahead never needs more sensors than greedy; both at least the exhaustive minimum
    A = world_matrix("lorenz96", 8, {"F": 8.0}); C = candidate_sensors("lorenz96", 8, rng, {}); Wa = gramian(A, C, 0.5); c = 1e-3 * np.linalg.eigvalsh(Wa).max()
    S = greedy(A, C, 0.5, c, 4, 8); L = lookahead(A, C, 0.5, c, 4, 8); E, fa = exact_subset(A, C, 0.5, c, 4, 8, 100000); ok2 = fa is True and len(E) == len(L); print("exact feasible at cap", fa, len(E) if E else None, ok2); fails += 0 if ok2 else 1; ks = exhaustive_min_count(A, C, 0.5, c, 4, len(S), 100000)
    ok = d_obs(gramian(A, C[S], 0.5), c) >= 4 and d_obs(gramian(A, C[L], 0.5), c) >= 4 and ks is not None and ks <= len(L) <= len(S); print("greedy reaches m = 4 with", len(S), "sensors, lookahead with", len(L), "; exhaustive minimum", ks, ok); fails += 0 if ok else 1
    # on a diffusion chain at a threshold where the probe found greedy one over the optimum, lookahead is not worse than greedy
    A = world_matrix("diffusion", 12, {}); C = candidate_sensors("diffusion", 12, rng, {}); Wa = gramian(A, C, 0.5); c = 1e-2 * np.linalg.eigvalsh(Wa).max()
    S = greedy(A, C, 0.5, c, 8, 12); L = lookahead(A, C, 0.5, c, 8, 12); ok = len(L) <= len(S) and d_obs(gramian(A, C[L], 0.5), c) >= 8; print("diffusion chain m = 8: greedy", len(S), "lookahead", len(L), ok); fails += 0 if ok else 1
    # horizon: an error in a stable subspace never grows; in an unstable direction it crosses the tolerance
    A = np.diag([1.0, -1.0]); hz = np.random.default_rng(1)
    h_stable, cens = horizon(A, np.array([[0.0], [1.0]]), 1.0, 10.0, 5.0, 0.01, hz, 5); h_unst, _ = horizon(A, np.array([[1.0], [0.0]]), 1.0, 10.0, 5.0, 0.01, hz, 5)
    ok = cens == 1.0 and abs(h_unst - math.log(10.0)) < 0.02; print("horizon: stable censored %.0f, unstable %.3f (log 10 = %.3f)" % (cens, h_unst, math.log(10.0)), ok); fails += 0 if ok else 1
    # the shallow-water matrix is neutral (eigenvalues on the imaginary axis), Lorenz-96 has growth, diffusion decays
    for kind, n, sign in (("shallow", 12, 0), ("lorenz96", 12, 1), ("diffusion", 12, -1)):
        g = np.max(np.linalg.eigvals(world_matrix(kind, n, {})).real); ok = (abs(g) < 1e-9) if sign == 0 else (g > 0.1 if sign > 0 else g < -0.01)
        print("%-9s max real eigenvalue %.3f" % (kind, g), ok); fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--seed-role", default="pilot"); ap.add_argument("--out", default="out.json")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    run(json.load(open(a.config, encoding="utf-8")), a.seed_role, a.out); return 0


if __name__ == "__main__":
    sys.exit(main())
