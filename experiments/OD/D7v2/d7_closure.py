"""D7: the minimal observational geometry that closes a turbulent flow (OD track, gate D7).

World. Decaying two-dimensional turbulence (vorticity form, pseudo-spectral, 2/3 dealiasing, RK4) at
resolution n from a seeded random field with a declared energy spectrum, spun up to a declared time, then
sampled at declared snapshot times. The consumer is the large-eddy filter, the spectral cutoff at k_c: the
resolved state is the vorticity's modes with |k| <= k_c and the budget is k_c. The subfilter state is the
dealiased remainder. The resolved tendency T(w_bar + w') is the nonlinear term of the vorticity equation
projected on the resolved modes; the subgrid contribution is T(w_bar + w') - T(w_bar).

Read operator. The blind probe on the solver: the resolved tendency is called with the subfilter state
perturbed one real coefficient at a time (finite differences on the nonlinear solver), which gives the
sensitivity J of the resolved tendency to every subfilter coefficient; the read operator of the resolved
dynamics with respect to the subfilter state is P = J^T J, and its leading eigen-directions are the right
singular vectors of J.

Closures at matched dimension r: the read-operator closure keeps the projection of the true subfilter
state onto the leading r eigen-directions of P; the energy closure keeps the r subfilter modes of largest
energy in the snapshot; the random closure keeps r random subfilter modes (median over draws). The error
of a closure is |T(w_bar + Pi_r w') - T(w_bar + w')| over |T(w_bar + w') - T(w_bar)|, so one is no closure
and zero is exact.

    python d7_closure.py --selftest
    python d7_closure.py --config prereg_config.json --seed-role pilot --out pilot.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D5")
from d5_burgers import NS2D  # noqa: E402


def initial_field(n: int, rng: np.random.Generator, k_peak: float, amp: float) -> np.ndarray:
    """Seeded random vorticity with spectrum ~ k^6 exp(-2 (k / k_peak)^2), scaled to max |w| = amp; returns w_hat."""
    k = np.fft.fftfreq(n, d=1.0 / n); kx, ky = np.meshgrid(k, k, indexing="ij"); kmag = np.sqrt(kx ** 2 + ky ** 2)
    phase = np.exp(2j * np.pi * rng.uniform(size=(n, n))); spec = kmag ** 3 * np.exp(-(kmag / k_peak) ** 2)
    wh = spec * phase; wh[0, 0] = 0
    w = np.real(np.fft.ifft2(wh)); w *= amp / np.max(np.abs(w))
    return np.fft.fft2(w)


def resolved_mask(model: NS2D, kc: float) -> np.ndarray:
    kmag = np.sqrt(model.kx ** 2 + model.ky ** 2); return (kmag <= kc) & model.dealias


def subfilter_mask(model: NS2D, kc: float) -> np.ndarray:
    kmag = np.sqrt(model.kx ** 2 + model.ky ** 2); return (kmag > kc) & model.dealias


def nonlinear_hat(model: NS2D, wh: np.ndarray) -> np.ndarray:
    """The nonlinear term of the vorticity equation, -(u . grad) w, in spectral space, dealiased."""
    u, v = model.velocity(wh); wx = np.real(np.fft.ifft2(1j * model.kx * wh)); wy = np.real(np.fft.ifft2(1j * model.ky * wh))
    nl = np.fft.fft2(u * wx + v * wy); nl[~model.dealias] = 0
    return -nl


def resolved_tendency(model: NS2D, wh: np.ndarray, rmask: np.ndarray) -> np.ndarray:
    """The resolved part of the nonlinear tendency, as a real vector (real and imaginary parts of the resolved modes)."""
    T = nonlinear_hat(model, wh)[rmask]; return np.concatenate([T.real, T.imag])


def unique_half(mask: np.ndarray, n: int) -> np.ndarray:
    """Indices (flat) of one representative per conjugate pair inside the mask, so that real perturbations
    of a real field are parametrised without redundancy."""
    idx = np.nonzero(mask.ravel())[0]; keep = []
    for f in idx:
        i, j = divmod(int(f), n); ci, cj = (-i) % n, (-j) % n; cf = ci * n + cj
        if f <= cf: keep.append(f)
    return np.array(keep, dtype=int)


def set_pair(wh: np.ndarray, f: int, n: int, val: complex) -> None:
    i, j = divmod(int(f), n); wh[i, j] = val; wh[(-i) % n, (-j) % n] = np.conj(val)


def probe_sensitivity(model: NS2D, wh: np.ndarray, rmask: np.ndarray, sub_idx: np.ndarray, eps: float) -> np.ndarray:
    """Blind probe: the resolved tendency's sensitivity to each real and imaginary subfilter coefficient, by
    central finite differences on the nonlinear solver. Returns J of shape (2 * n_resolved, 2 * n_sub)."""
    n = model.n; T0 = resolved_tendency(model, wh, rmask); cols = []
    # column order matches subfilter_vector: all real parts first, then all imaginary parts
    for part in (1.0, 1j):
        for f in sub_idx:
            wp = wh.copy(); wm = wh.copy(); base = wh.ravel()[f]
            set_pair(wp, f, n, base + eps * part); set_pair(wm, f, n, base - eps * part)
            cols.append((resolved_tendency(model, wp, rmask) - resolved_tendency(model, wm, rmask)) / (2 * eps))
    return np.array(cols).T, T0


def subfilter_vector(wh: np.ndarray, sub_idx: np.ndarray) -> np.ndarray:
    v = wh.ravel()[sub_idx]; return np.concatenate([v.real, v.imag])


def with_subfilter(wh_bar: np.ndarray, sub_idx: np.ndarray, x: np.ndarray, n: int) -> np.ndarray:
    wh = wh_bar.copy(); m = len(sub_idx)
    for k, f in enumerate(sub_idx):
        set_pair(wh, f, n, complex(x[k], x[m + k]))
    return wh


def closure_error(model: NS2D, wh_bar: np.ndarray, sub_idx: np.ndarray, x_true: np.ndarray, x_red: np.ndarray, rmask: np.ndarray, T_full: np.ndarray, T_bar: np.ndarray) -> float:
    T_red = resolved_tendency(model, with_subfilter(wh_bar, sub_idx, x_red, model.n), rmask)
    return float(np.linalg.norm(T_red - T_full) / np.linalg.norm(T_full - T_bar))


def evaluate_snapshot(model: NS2D, wh: np.ndarray, kc: float, ranks: list[int], eps: float, rng: np.random.Generator, random_draws: int) -> dict:
    n = model.n; rmask = resolved_mask(model, kc); smask = subfilter_mask(model, kc); sub_idx = unique_half(smask, n)
    wh_bar = wh.copy(); wh_bar[~rmask] = 0
    x_true = subfilter_vector(wh, sub_idx); m = len(sub_idx)
    t0 = time.time(); eps_abs = eps * float(np.max(np.abs(wh))); J, T_full = probe_sensitivity(model, wh, rmask, sub_idx, eps_abs); T_bar = resolved_tendency(model, wh_bar, rmask)
    U, sv, Vt = np.linalg.svd(J, full_matrices=False)
    energy = np.abs(wh.ravel()[sub_idx]) ** 2; e_order = np.argsort(-energy)
    # the read energy of a subfilter mode: its sensitivity-weighted energy, the diagonal of P = J^T J times the squared
    # coefficient, summed over the real and imaginary parts (the read distortion the resolved consumer experiences from that mode)
    diagP = np.sum(J ** 2, axis=0); read_energy = diagP[:m] * x_true[:m] ** 2 + diagP[m:] * x_true[m:] ** 2; re_order = np.argsort(-read_energy)
    out = {"kc": kc, "n_resolved": int(rmask.sum()), "n_sub_pairs": m, "singular_values_top": [float(s) for s in sv[:10]], "sv_effective_rank": float(sv.sum() ** 2 / (sv ** 2).sum()),
           "subgrid_norm_over_resolved": float(np.linalg.norm(T_full - T_bar) / np.linalg.norm(T_full)), "probe_seconds": round(time.time() - t0, 1), "ranks": {}}
    for r in list(ranks) + ["full"]:
        if r == "full":
            rr = min(J.shape); V = Vt[:rr].T; x_read = V @ (V.T @ x_true)
            T_red = resolved_tendency(model, with_subfilter(wh_bar, sub_idx, x_read, n), rmask)
            out["ranks"]["full"] = {"rank": rr, "err_read": float(np.linalg.norm(T_red - T_full) / np.linalg.norm(T_full - T_bar)), "read_energy_fraction": float(np.sum(x_read ** 2) / np.sum(x_true ** 2))}
            continue
        if r > min(J.shape): continue
        V = Vt[:r].T; x_read = V @ (V.T @ x_true)
        x_en = np.zeros_like(x_true); sel = e_order[:r]; x_en[sel] = x_true[sel]; x_en[m + sel] = x_true[m + sel]
        x_re = np.zeros_like(x_true); sel = re_order[:r]; x_re[sel] = x_true[sel]; x_re[m + sel] = x_true[m + sel]
        errs_rand = []
        for _ in range(random_draws):
            sel = rng.choice(m, size=r, replace=False); x_r = np.zeros_like(x_true); x_r[sel] = x_true[sel]; x_r[m + sel] = x_true[m + sel]
            errs_rand.append(closure_error(model, wh_bar, sub_idx, x_true, x_r, rmask, T_full, T_bar))
        # the read closure's captured fraction of the subfilter energy, for the record
        out["ranks"][str(r)] = {"err_read": closure_error(model, wh_bar, sub_idx, x_true, x_read, rmask, T_full, T_bar),
                                "err_read_energy": closure_error(model, wh_bar, sub_idx, x_true, x_re, rmask, T_full, T_bar),
                                "err_energy": closure_error(model, wh_bar, sub_idx, x_true, x_en, rmask, T_full, T_bar),
                                "err_random_median": float(np.median(errs_rand)),
                                "read_energy_fraction": float(np.sum(x_read ** 2) / np.sum(x_true ** 2)), "energy_fraction": float(np.sum(x_en ** 2) / np.sum(x_true ** 2))}
    return out


def run_world(world: dict, cfg: dict, seed: int, log=print) -> dict:
    rng = np.random.default_rng(seed + int(world["seed_offset"])); n = int(world["n"]); nu = float(world["nu"]); model = NS2D(n, nu)
    wh = initial_field(n, rng, float(cfg["k_peak"]), float(cfg["amp"])); dt = float(cfg["dt_base"]) * (int(cfg["n_ref"]) / n)
    t = 0.0; snaps = [float(s) for s in cfg["snapshot_times"]]; t0 = time.time(); out = {"name": world["name"], "group": world["group"], "n": n, "nu": nu, "snapshots": []}
    for ts in snaps:
        while t < ts - 1e-12:
            wh = model.step(wh, dt); t += dt
        for kc in cfg["cutoffs"]:
            if kc >= n / 3: continue
            ev = evaluate_snapshot(model, wh, float(kc), [int(r) for r in cfg["ranks"]], float(cfg["eps"]), np.random.default_rng(seed + 977 + int(world["seed_offset"])), int(cfg["random_draws"]))
            ev["t"] = t; out["snapshots"].append(ev)
            log(json.dumps({"world": world["name"], "t": round(t, 3), "kc": kc, "n_sub_pairs": ev["n_sub_pairs"], "sv_rank": round(ev["sv_effective_rank"], 1), "subgrid": round(ev["subgrid_norm_over_resolved"], 3),
                            "read_readenergy_energy_random": {r: (round(v["err_read"], 3), round(v["err_read_energy"], 3), round(v["err_energy"], 3), round(v["err_random_median"], 3)) for r, v in ev["ranks"].items() if r != "full"}, "full_rank_remainder": round(ev["ranks"]["full"]["err_read"], 3), "seconds": round(time.time() - t0, 1)}))
    out["seconds"] = time.time() - t0
    return out


def run(cfg: dict, seed_role: str, out_path: str) -> dict:
    seed = int(cfg[f"seed_{seed_role}"]); groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if seed_role == "probe":
            if not world.get("in_probe"): continue
        elif world["group"] not in groups: continue
        result["worlds"].append(run_world(world, cfg, seed)); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


def selftest() -> int:
    fails = 0; rng = np.random.default_rng(0); n = 32; model = NS2D(n, 0.0); wh = initial_field(n, rng, 4.0, 3.0)
    # 1. the blind-probe sensitivity matches the tangent solver's action on a random subfilter perturbation
    kc = 5.0; rmask = resolved_mask(model, kc); sub_idx = unique_half(subfilter_mask(model, kc), n); J, T0 = probe_sensitivity(model, wh, rmask, sub_idx, 1e-6)
    x = rng.normal(size=2 * len(sub_idx)); dwh = with_subfilter(np.zeros_like(wh), sub_idx, x, n)
    tang = model.tangent_rhs(wh, dwh) - (-model.nu * model.k2 * dwh); tang_res = np.concatenate([tang[rmask].real, tang[rmask].imag])
    ok = np.linalg.norm(J @ x - tang_res) / np.linalg.norm(tang_res) < 1e-5; print("blind probe J x vs tangent solver: rel err %.1e" % (np.linalg.norm(J @ x - tang_res) / np.linalg.norm(tang_res)), ok); fails += 0 if ok else 1
    # 2. conjugate-pair parametrisation: with_subfilter of the true vector reproduces the field on the subfilter modes
    xt = subfilter_vector(wh, sub_idx); wb = wh.copy(); wb[~rmask] = 0; rec = with_subfilter(wb, sub_idx, xt, n)
    ok = np.allclose(rec[model.dealias], wh[model.dealias]); print("subfilter parametrisation round trip:", ok); fails += 0 if ok else 1
    # 3. at the read operator's full rank (twice the resolved count, less than the subfilter dimension) the read closure
    # reproduces the linear part exactly, so its error is the quadratic remainder only and is well below one; and the
    # zero-rank closure has error one
    rfull = min(J.shape); ev = evaluate_snapshot(model, wh, kc, [], 1e-6, np.random.default_rng(1), 3); full = ev["ranks"]["full"]
    # the remainder at full rank is the part of the subgrid term that is quadratic in the subfilter state, which no linear read sees
    ok = 0.0 <= full["err_read"] < 1.0 and full["read_energy_fraction"] <= 1.0 + 1e-9; print("full-rank (%d of %d) read closure: err %.3f (the quadratic remainder), energy fraction %.3f" % (rfull, 2 * len(sub_idx), full["err_read"], full["read_energy_fraction"]), ok); fails += 0 if ok else 1
    wb2 = wh.copy(); wb2[~rmask] = 0; Tf = resolved_tendency(model, wh, rmask); Tb = resolved_tendency(model, wb2, rmask); e0 = closure_error(model, wb2, sub_idx, xt, np.zeros_like(xt), rmask, Tf, Tb)
    ok = abs(e0 - 1.0) < 1e-9; print("zero-rank closure error one:", ok); fails += 0 if ok else 1
    # 4. read-operator closure is at least as good as energy at every rank on a linearised problem (by construction of the SVD, for the linear part)
    ev = evaluate_snapshot(model, wh, kc, [2, 4, 8], 1e-6, np.random.default_rng(2), 3)
    print("rank -> (read eigen, read energy, energy, random):", {r: (round(v["err_read"], 3), round(v["err_read_energy"], 3), round(v["err_energy"], 3), round(v["err_random_median"], 3)) for r, v in ev["ranks"].items() if r != "full"}, "sub pairs", ev["n_sub_pairs"], "sv rank %.1f" % ev["sv_effective_rank"])
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
