"""OP2: which modes a reduced model should carry explicitly, so that the rest needs the least memory (OP track, gate OP2).

Design: `OP2-DESIGN-DRAFT.md`. Mori's linear projection with the time-average inner product, the operators recovered
from two-time correlations by the recursion of Lin and coauthors (arXiv:2101.05873) as used by Tian, Lin, Anghel and
Livescu (Phys. Fluids 33, 125118, 2021):
    C(n) = < g((n + i) D) g(i D)^T >_i,   Omega(0) = C(1) C(0)^-1,
    Omega(n) = [ C(n + 1) - sum_{l < n} Omega(l) C(n - l) ] C(0)^-1,
so that g(n + 1) = sum_{l=0}^{n} Omega(l) g(n - l) + W(n + 1), with W orthogonal to g(0).

Observables per (world, cutoff, ranking, r): the consumer's coordinates, the r pool pairs ranked first, and OP1's TEND
observable on them (the consumer's tendency on the chosen pairs), centered and scaled on the training record. World,
split, rankings and TEND are OP1's (imported); the trajectories are OP1's cached ones (no new simulation).

Per cell: E_L, the consumer forecast error of the best linear predictor with L lags (least squares on g(n), ..., g(n - L),
the Wiener projection of Lin and Lu, J. Comput. Phys. 2021), for L on a ladder, iterated to the horizons; E_gle_L, the
forecast of the truncated generalized Langevin equation with the orthogonal dynamics set to zero (Tian and coauthors,
eq. 36), recorded for comparison with their results (it is not the best linear predictor, since W(n + 1) is orthogonal
only to g(0), not to the later history); L*, the smallest L within a declared fraction of min_L E_L; tau_90 and
tau_int of the consumer block of the kernel; the memory share sum_{l>=1} |Omega(l)_CC| / |Omega(0)_CC|; the same three
statistics on each half of the training record (for the READ-blind reliability rule of the design draft); and the
generalized fluctuation-dissipation relation Omega(l) C(-D) = -<W(l+1) W(1)^T> as an extraction check.

    python op2_mz.py --selftest
    python op2_mz.py --config op2_config.json --seed-role probe --traj-dir ../OP1/traj --out probe.json [--world NAME]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):  # one core per run, set before numpy loads
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "OP1"))
from op1_edmd import Candidates, ForcedNS2D, Split, make_tend, pool_cols, rankings  # noqa: E402


# ---------------------------------------------------------------- Mori-Zwanzig operators from correlations

def correlations(G: np.ndarray, nmax: int) -> list[np.ndarray]:
    """C(n) = mean_i g(i + n) g(i)^T for n = 0..nmax; rows of G are g at successive samples."""
    N = len(G); return [G[n:].T @ G[:N - n] / (N - n) for n in range(nmax + 1)]


def kernels(C: list[np.ndarray], L: int, ridge: float) -> list[np.ndarray]:
    """Omega(0..L) by the recursion C(n + 1) = sum_{l=0}^{n} Omega(l) C(n - l)."""
    C0 = C[0] + ridge * np.trace(C[0]) / len(C[0]) * np.eye(len(C[0])); C0inv = np.linalg.inv(C0); Om = []
    for n in range(L + 1):
        acc = C[n + 1] - sum((Om[l] @ C[n - l] for l in range(n)), np.zeros_like(C[0])); Om.append(acc @ C0inv)
    return Om


def orthogonal_dynamics(G: np.ndarray, Om: list[np.ndarray], n: int) -> np.ndarray:
    """W(n + 1) at every initial index i: g(i + n + 1) - sum_{l=0}^{n} Omega(l) g(i + n - l)."""
    N = len(G); idx = np.arange(N - n - 1); W = G[idx + n + 1].copy()
    for l in range(n + 1):
        W -= G[idx + n - l] @ Om[l].T
    return W


def gfd_check(G: np.ndarray, Om: list[np.ndarray], C1: np.ndarray, lags: list[int]) -> dict:
    """Relative mismatch of Omega(l) C(-D) and -<W(l+1) W(1)^T> (C(-D) = C(1)^T), per lag."""
    W1 = orthogonal_dynamics(G, Om, 0); out = {}
    for l in lags:
        Wl = orthogonal_dynamics(G, Om, l); m = min(len(Wl), len(W1)); rhs = -(Wl[:m].T @ W1[:m]) / m; lhs = Om[l] @ C1.T
        out[str(l)] = float(np.linalg.norm(lhs - rhs) / max(np.linalg.norm(rhs), 1e-300))
    return out


def gle_errors(Om: list[np.ndarray], Gte: np.ndarray, L: int, horizons: list[int], starts: np.ndarray, ccols: np.ndarray, mu: np.ndarray, sd: np.ndarray, Xte_cons: np.ndarray, cap: float) -> dict:
    """Forecast with memory truncated at L and W = 0: true history up to each start, predictions after it. Errors of
    the consumer's coordinates in math units relative to the climatology (the training mean)."""
    hmax = max(horizons); hist = [Gte[starts - k] for k in range(L + 1)]  # hist[k] = g(start - k)
    e = {}
    with np.errstate(all="ignore"):
        for h in range(1, hmax + 1):
            nxt = sum(hist[l] @ Om[l].T for l in range(L + 1)); hist = [nxt] + hist[:L]
            if h in horizons:
                est = nxt[:, ccols] * sd[ccols] + mu[ccols]; tru = Xte_cons[starts + h]
                num = float(np.sum((est - tru) ** 2)); den = float(np.sum((tru - mu[ccols]) ** 2))
                e[h] = math.sqrt(num / den) if np.isfinite(num) else math.inf
    vals = [min(v, cap) if math.isfinite(v) else cap for v in e.values()]
    return {"e": {str(h): (v if math.isfinite(v) else None) for h, v in e.items()}, "E": float(np.mean(vals))}


def lag_errors(Gtr: np.ndarray, Gte: np.ndarray, L: int, ridge: float, horizons: list[int], starts: np.ndarray, ccols: np.ndarray, mu: np.ndarray, sd: np.ndarray, Xte_cons: np.ndarray, cap: float) -> dict:
    """The best linear predictor with L lags: g(n + 1) ~ sum_{l=0}^{L} A_l g(n - l), fitted by ridge least squares on the
    training record and iterated from the true history at each test start."""
    d = Gtr.shape[1]; N = len(Gtr); F = np.hstack([Gtr[L - l:N - 1 - l] for l in range(L + 1)]); Y = Gtr[L + 1:]
    M = F.T @ F; A = np.linalg.solve(M + ridge * np.trace(M) / len(M) * np.eye(len(M)), F.T @ Y)  # (d (L + 1), d)
    hist = [Gte[starts - k] for k in range(L + 1)]; e = {}
    with np.errstate(all="ignore"):
        for h in range(1, max(horizons) + 1):
            nxt = np.hstack(hist) @ A; hist = [nxt] + hist[:L]
            if h in horizons:
                est = nxt[:, ccols] * sd[ccols] + mu[ccols]; tru = Xte_cons[starts + h]
                num = float(np.sum((est - tru) ** 2)); den = float(np.sum((tru - mu[ccols]) ** 2))
                e[h] = math.sqrt(num / den) if np.isfinite(num) else math.inf
    vals = [min(v, cap) if math.isfinite(v) else cap for v in e.values()]
    return {"e": {str(h): (v if math.isfinite(v) else None) for h, v in e.items()}, "E": float(np.mean(vals))}


def memory_stats(Om: list[np.ndarray], ccols: np.ndarray, dt: float) -> dict:
    """tau_90, tau_int and the memory share of the consumer block (rows and columns of the consumer's coordinates)."""
    norms = np.array([np.linalg.norm(o[np.ix_(ccols, ccols)]) for o in Om]); mem = norms[1:]
    if mem[0] <= 0: return {"tau90": 0.0, "tau_int": 0.0, "share": 0.0, "norms": norms.tolist()}
    below = np.nonzero(mem <= 0.1 * mem[0])[0]; tau90 = float((below[0] + 1) * dt) if len(below) else float(len(mem) * dt)
    return {"tau90": tau90, "tau_int": float(mem.sum() / mem[0] * dt), "share": float(mem.sum() / norms[0]), "norms": norms.tolist()}


def lag_ladder(ladder: list[int], d: int, n: int, ratio: float) -> list[int]:
    """The lags the sample budget allows: L = 0 always, any other L only if d (L + 1) <= n / ratio."""
    return [int(L) for L in ladder if int(L) == 0 or d * (int(L) + 1) <= n / ratio]


def l_star(E: dict, frac: float) -> int:
    best = min(E.values()); return min(int(L) for L, v in E.items() if v <= (1 + frac) * best)


# ---------------------------------------------------------------- one cell, one world

def observables(X: np.ndarray, split: Split, tend, sel_cols: np.ndarray) -> np.ndarray:
    ccols = split.cols(np.arange(split.nc), 0); pairs = np.concatenate([np.arange(split.nc), sel_cols[:len(sel_cols) // 2]]) if len(sel_cols) else np.arange(split.nc)
    return np.hstack([X[:, ccols], X[:, sel_cols], tend(X, pairs)]) if len(sel_cols) else np.hstack([X[:, ccols], tend(X, pairs)])


def cell(Xtr, Xte, split, tend, sel_cols, cfg, dt) -> dict:
    Gtr_raw = observables(Xtr, split, tend, sel_cols); Gte_raw = observables(Xte, split, tend, sel_cols)
    mu = Gtr_raw.mean(axis=0); sd = Gtr_raw.std(axis=0); sd[sd == 0] = 1.0; Gtr = (Gtr_raw - mu) / sd; Gte = (Gte_raw - mu) / sd
    Lmax = max(cfg["memory_ladder"]); ridge = float(cfg["ridge"]); H = [int(h) for h in cfg["horizons"]]; nc2 = 2 * split.nc; ccols = np.arange(nc2)
    C = correlations(Gtr, Lmax + 1); Om = kernels(C, Lmax, ridge)
    starts = np.arange(Lmax, len(Gte) - max(H), int(cfg["test_start_stride"])); Xc = Xte[:, split.cols(np.arange(split.nc), 0)]
    # the lag ladder is capped by the sample budget: the lag predictor's d (L + 1) features may not exceed N / budget_ratio
    # (owner, 2026-10-11, after the probe showed the predictor overfitting where they did); L = 0 is always fitted
    Ls = lag_ladder(cfg["memory_ladder"], Gtr.shape[1], len(Gtr), float(cfg["lag_budget_ratio"]))
    E = {str(L): lag_errors(Gtr, Gte, L, ridge, H, starts, ccols, mu, sd, Xc, float(cfg["error_cap"])) for L in Ls}
    E_gle = {str(L): gle_errors(Om, Gte, L, H, starts, ccols, mu, sd, Xc, float(cfg["error_cap"]))["E"] for L in cfg["memory_ladder"]}
    Ev = {L: v["E"] for L, v in E.items()}; ms = memory_stats(Om, ccols, dt)
    half = len(Gtr) // 2; halves = []
    for part in (Gtr[:half], Gtr[half:]):
        Oh = kernels(correlations(part, Lmax + 1), Lmax, ridge); halves.append({k: v for k, v in memory_stats(Oh, ccols, dt).items() if k != "norms"})
    return {"E": E, "E_gle": E_gle, "lags_fitted": Ls, "E_min": min(Ev.values()), "L_star": l_star(Ev, float(cfg["lstar_fraction"])), **{k: ms[k] for k in ("tau90", "tau_int", "share")},
            "consumer_kernel_norms": ms["norms"], "halves": halves, "gfd": gfd_check(Gtr, Om, C[1], [1, 2, 3]), "dim": int(Gtr.shape[1])}


def run_world(world: dict, cfg: dict, seed: int, traj_dir: str, log=print) -> dict:
    t0 = time.time(); n = int(world["n"]); off = int(world["seed_offset"])
    model = ForcedNS2D(n, float(world["nu"]), float(cfg["alpha"]), float(cfg["F0"]), int(cfg["kf"])); cand = Candidates(model)
    z = np.load(Path(traj_dir) / f"{world['name']}_seed{seed}.npz"); keep_all = np.nonzero(cand.kmag <= float(cfg["k_pool"]))[0]
    if not np.array_equal(z["keep"], keep_all): raise SystemExit("cached pairs differ from this config's")
    Xtr_all, S_all, S_at, Xte_all = z["Xtr"], z["S"], z["S_at"], z["Xte"]; pos = {int(j): i for i, j in enumerate(keep_all)}; m_all = len(keep_all)
    out = {"name": world["name"], "group": world["group"], "n": n, "nu": model.nu, "trajectory_cache": f"{world['name']}_seed{seed}.npz", "cutoffs": {}}; sofs = 0
    for kc in cfg["cutoffs"]:
        split = Split(cand, float(kc), float(cfg["k_pool"])); idx = np.array([pos[int(j)] for j in split.keep]); colmap = np.concatenate([idx, m_all + idx])
        Xtr = Xtr_all[:, colmap]; Xte = Xte_all[:, colmap]; S = S_all[:, sofs:sofs + split.npool]; sofs += split.npool
        orders, _ = rankings(Xtr, S, S_at, split, cand.kmag[split.pool], int(cfg["random_draws"]), np.random.default_rng(seed + off + 977))
        tend = make_tend(cand, split); ladder = [r for r in cfg["ladder"] if r <= split.npool]; dt = float(cfg["dt_sample"])
        rec = {"ladder": ladder, "NONE": cell(Xtr, Xte, split, tend, np.array([], int), cfg, dt), "cells": {}}
        for r in ladder:
            rec["cells"][str(r)] = {name: cell(Xtr, Xte, split, tend, pool_cols(split, o, r), cfg, dt) for name, o in orders.items()}
            c = rec["cells"][str(r)]
            log(json.dumps({"world": world["name"], "kc": kc, "r": r, **{k: [round(c[k]["E_min"], 4), c[k]["L_star"], round(c[k]["tau90"], 2)] for k in ("READ", "ENERGY", "BALL", "SENS")},
                            "RANDOM_Emin_median": round(float(np.median([c[f"RANDOM{j}"]["E_min"] for j in range(int(cfg["random_draws"]))])), 4), "seconds": round(time.time() - t0, 1)}))
        out["cutoffs"][str(kc)] = rec
    out["seconds"] = time.time() - t0
    return out


def run(cfg: dict, seed_role: str, out_path: str, traj_dir: str, only_world: str | None = None) -> dict:
    seed = int(cfg[f"seed_{seed_role}"]); groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if world["group"] not in groups or (only_world and world["name"] != only_world): continue
        result["worlds"].append(run_world(world, cfg, seed, traj_dir)); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    if only_world and not result["worlds"]: raise SystemExit(f"no world named {only_world} in role {seed_role}")
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    return result


# ---------------------------------------------------------------- self-test

def selftest() -> int:
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    # A consumer x driven by a hidden autoregressive y: x' = a x + b y, y' = c y + eta. Observed alone, x needs memory
    # (its best linear predictor uses its whole past); carried with y, the pair is exactly Markov.
    rng = np.random.default_rng(3); N = 200000; a, b, c = 0.5, 0.8, 0.9; x = np.zeros(N); y = np.zeros(N)
    for t in range(N - 1):
        y[t + 1] = c * y[t] + rng.normal(); x[t + 1] = a * x[t] + b * y[t]
    Gx = ((x - x.mean()) / x.std())[:, None]; Gxy = np.stack([(x - x.mean()) / x.std(), (y - y.mean()) / y.std()], axis=1); L = 8
    # exact correlations: T the transition of (x, y), Q the noise covariance, Sigma = T Sigma T^T + Q, C(n) = T^n Sigma
    T = np.array([[a, b], [0.0, c]]); Sig = np.eye(2)
    for _ in range(5000):
        Sig = T @ Sig @ T.T + np.diag([0.0, 1.0])
    Cxy = [np.linalg.matrix_power(T, n) @ Sig for n in range(L + 2)]; dsc = np.diag(1 / np.sqrt(np.diag(Sig)))
    Om_xy_exact = kernels([dsc @ Cn @ dsc for Cn in Cxy], L, 0.0); Om_x_exact = kernels([np.array([[Cn[0, 0] / Sig[0, 0]]]) for Cn in Cxy], L, 0.0)
    mem_xy = sum(float(np.linalg.norm(o)) for o in Om_xy_exact[1:]); mem_x = sum(abs(float(o[0, 0])) for o in Om_x_exact[1:])
    check("exact correlations: the consumer alone has memory, carrying its driver removes it", mem_x > 1e-3 and mem_xy < 1e-10, f"memory norm alone {mem_x:.4f}, with driver {mem_xy:.1e}")
    Om_x = kernels(correlations(Gx, L + 1), L, 0.0); Om_xy = kernels(correlations(Gxy, L + 1), L, 0.0)
    dev = max(abs(float(Om_x[l][0, 0] - Om_x_exact[l][0, 0])) for l in range(L + 1))
    check("kernels learned from data match the exact kernels", dev < 0.01, f"max deviation {dev:.4f}")
    # With y explicit, Omega(0) is the true transition matrix in the scaled coordinates
    Tsc = dsc @ T @ np.linalg.inv(dsc); err = float(np.max(np.abs(Om_xy[0] - Tsc)))
    check("the Markov operator with the driver explicit is the true transition", err < 0.01, f"max error {err:.4f}")
    # The recursion reproduces every correlation it was built from: C(n + 1) = sum Omega(l) C(n - l)
    C = correlations(Gx, L + 1); rec = max(float(abs((C[n + 1] - sum(Om_x[l] @ C[n - l] for l in range(n + 1)))[0, 0])) for n in range(L))
    check("the recursion reproduces the correlations", rec < 1e-12, f"{rec:.1e}")
    # The generalized fluctuation-dissipation relation holds on data for the consumer alone (a sampling check)
    g = gfd_check(Gx, Om_x, C[1], [1, 2, 3]); check("GFD relation on data", max(g.values()) < 0.05, str({k: round(v, 4) for k, v in g.items()}))
    # x(t+1) = (a + c) x(t) - a c x(t-1) + b eta(t-1): an AR(2) whose innovation is orthogonal to the whole past of x, so
    # the lag-1 predictor reaches the optimum b / std(x) and the Markov one does not; with y carried, x is exact in one step
    half = N // 2; mu = np.array([x.mean()]); sd = np.array([x.std()]); starts = np.arange(L, N - half - 2, 7); Xc = x[half:, None]
    e0 = lag_errors(Gx[:half], Gx[half:], 0, 0.0, [1], starts, np.array([0]), mu, sd, Xc, 2.0)["e"]["1"]
    e1 = lag_errors(Gx[:half], Gx[half:], 1, 0.0, [1], starts, np.array([0]), mu, sd, Xc, 2.0)["e"]["1"]; opt = b / x.std()
    ex = lag_errors(Gxy[:half], Gxy[half:], 0, 0.0, [1], starts, np.array([0]), mu, sd, Xc, 2.0)["e"]["1"]
    check("one lag brings the consumer alone to the optimal predictor; with its driver it is exact", abs(e1 - opt) < 0.005 and e0 > e1 + 0.02 and ex < 1e-4,  # 1e-4: normal equations over 1e5 samples leave ~1e-6
          f"Markov {e0:.4f}, one lag {e1:.4f}, optimum {opt:.4f}, with driver {ex:.1e}")
    # Memory statistics and L* on a constructed kernel sequence
    Om_c = [np.eye(2)] + [np.eye(2) * 0.5 ** l for l in range(1, 9)]; ms = memory_stats(Om_c, np.arange(2), 0.5)
    ok = abs(ms["tau90"] - 0.5 * 5) < 1e-12 and abs(ms["share"] - sum(0.5 ** l for l in range(1, 9))) < 1e-12 and l_star({"0": 1.0, "1": 0.8, "2": 0.795, "4": 0.79}, 0.01) == 2
    check("memory statistics and L*", ok, f"tau90 {ms['tau90']}, share {ms['share']:.4f}")
    # The lag cap: with 2000 samples and ratio 4, 56 observables allow L up to 7, 160 allow 2, 224 allow 1, 600 allow only 0
    caps = [lag_ladder([0, 1, 2, 4, 8, 16], d, 2000, 4.0) for d in (56, 160, 224, 600)]
    check("the lag ladder is capped by the sample budget", caps == [[0, 1, 2, 4], [0, 1, 2], [0, 1], [0]], str(caps))
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--seed-role", default="probe")
    ap.add_argument("--out", default="out.json"); ap.add_argument("--world", default=None); ap.add_argument("--traj-dir", default="../OP1/traj")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    run(json.load(open(a.config, encoding="utf-8")), a.seed_role, a.out, a.traj_dir, a.world); return 0


if __name__ == "__main__":
    sys.exit(main())
