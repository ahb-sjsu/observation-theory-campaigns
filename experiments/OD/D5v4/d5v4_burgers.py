"""D5v4: D5v2's workload unchanged, renamed for the registration. D5v2: the observer-relative transition in Burgers shock formation as a law (OD track, gate D5v2), the D5
workload with the control's max |u| recorded so that its front wavenumber max |grad u| / max |u| is defined
the same way as the Burgers worlds'. The claim of D5v2 drops the lead and alarm clauses D5 showed cannot hold
and declares a viscosity scope; see PREREG-D5V2.md.

D5 header follows.

(OD track, gate D5).

World. The periodic Burgers equation u_t + u u_x = nu u_xx on [0, 2 pi) at resolution N (pseudo-spectral,
2/3 dealiasing, RK4), from seeded initial conditions u0 with a few Fourier modes, with nu on a ladder
including nu = 0 (the inviscid case, whose exact pre-shock solution follows from characteristics and
whose shock time is t* = -1 / min u0'). Observers are spectral readers: the observer with budget B keeps
the first B Fourier modes (cosine and sine) of a perturbation. The observer-induced geometry of
perturbations at time t is the Gramian of the tangent propagator M(t, t + tau) over a short window,
read through the observer, G_B(t) = M^T C_B^T C_B M, estimated in a seeded random subspace of r
perturbation directions (a sketch, the same estimator for every world): its leading eigenvalue, its
effective dimension (participation ratio) and its shell thickness (the ratio of the second eigenvalue
to the first). The observational alarm at budget B is the first time the log of the leading eigenvalue
grows faster than a declared rate kappa; the classical alarm is the first time max |u_x| exceeds a
declared multiple of its initial value; the classical prediction of the shock time is the linear
extrapolation of 1 / max |u_x| to zero, exact for inviscid Burgers before the shock. The negative
control is decaying two-dimensional Navier-Stokes (vorticity form, pseudo-spectral) from a seeded
smooth field, with the same observers (spectral budgets) and the same estimator.

    python d5v2_burgers.py --selftest
    python d5_burgers.py --config prereg_config.json --seed-role pilot --out pilot.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np

# ----------------------------------------------------------------------------- Burgers, pseudo-spectral


class Burgers:
    def __init__(self, N: int, nu: float):
        self.N = N; self.nu = nu; self.x = 2 * np.pi * np.arange(N) / N
        self.k = np.fft.rfftfreq(N, d=1.0 / N)  # integer wavenumbers 0..N/2
        self.dealias = self.k <= (2.0 / 3.0) * (N / 2)

    def rhs_hat(self, uh: np.ndarray) -> np.ndarray:
        u = np.fft.irfft(uh, n=self.N); ux = np.fft.irfft(1j * self.k * uh, n=self.N)
        nl = np.fft.rfft(u * ux); nl[~self.dealias] = 0
        return -nl - self.nu * self.k ** 2 * uh

    def step(self, uh: np.ndarray, dt: float) -> np.ndarray:
        k1 = self.rhs_hat(uh); k2 = self.rhs_hat(uh + 0.5 * dt * k1); k3 = self.rhs_hat(uh + 0.5 * dt * k2); k4 = self.rhs_hat(uh + dt * k3)
        return uh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def tangent_rhs_hat(self, uh: np.ndarray, dh: np.ndarray) -> np.ndarray:
        u = np.fft.irfft(uh, n=self.N); d = np.fft.irfft(dh, n=self.N)
        nl = np.fft.rfft(u * np.fft.irfft(1j * self.k * dh, n=self.N) + d * np.fft.irfft(1j * self.k * uh, n=self.N)); nl[~self.dealias] = 0
        return -nl - self.nu * self.k ** 2 * dh

    def tangent_step(self, uh: np.ndarray, dh: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
        """One RK4 step of the state and of a tangent perturbation along it."""
        k1 = self.rhs_hat(uh); l1 = self.tangent_rhs_hat(uh, dh)
        k2 = self.rhs_hat(uh + 0.5 * dt * k1); l2 = self.tangent_rhs_hat(uh + 0.5 * dt * k1, dh + 0.5 * dt * l1)
        k3 = self.rhs_hat(uh + 0.5 * dt * k2); l3 = self.tangent_rhs_hat(uh + 0.5 * dt * k2, dh + 0.5 * dt * l2)
        k4 = self.rhs_hat(uh + dt * k3); l4 = self.tangent_rhs_hat(uh + dt * k3, dh + dt * l3)
        return uh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), dh + dt / 6 * (l1 + 2 * l2 + 2 * l3 + l4)

    def max_grad(self, uh: np.ndarray) -> float:
        return float(np.max(np.abs(np.fft.irfft(1j * self.k * uh, n=self.N))))


def initial_condition(N: int, rng: np.random.Generator, modes: int, amp: float) -> tuple[np.ndarray, float]:
    """u0 = sum of `modes` random Fourier modes with unit-scaled amplitude, and its exact inviscid shock time."""
    x = 2 * np.pi * np.arange(4096) / 4096; u = np.zeros_like(x); du = np.zeros_like(x)
    for m in range(1, modes + 1):
        a, b = rng.normal(size=2) / m
        u += a * np.cos(m * x) + b * np.sin(m * x); du += -a * m * np.sin(m * x) + b * m * np.cos(m * x)
    scale = amp / np.max(np.abs(u)); u *= scale; du *= scale
    t_star = float(-1.0 / du.min()) if du.min() < 0 else float("inf")
    xN = 2 * np.pi * np.arange(N) / N; uN = np.zeros(N)
    return np.interp(xN, x, u, period=2 * np.pi) if N != 4096 else u, t_star


def exact_inviscid(u0_fine: np.ndarray, t: float, x_eval: np.ndarray) -> np.ndarray:
    """Pre-shock inviscid solution by characteristics: u(x, t) = u0(xi) with x = xi + t u0(xi)."""
    xi = 2 * np.pi * np.arange(len(u0_fine)) / len(u0_fine); xs = xi + t * u0_fine
    order = np.argsort(xs); xs_s = xs[order]; us = u0_fine[order]
    xs_ext = np.concatenate([xs_s - 2 * np.pi, xs_s, xs_s + 2 * np.pi]); us_ext = np.concatenate([us, us, us])
    return np.interp(x_eval, xs_ext, us_ext)


# ----------------------------------------------------------------------------- observers and geometry


def observer_mask(N: int, B: int) -> np.ndarray:
    """The spectral reader with budget B keeps wavenumbers 1..B (the mean is not read)."""
    k = np.fft.rfftfreq(N, d=1.0 / N); return (k >= 1) & (k <= B)


def smooth_directions(N: int, r: int, rng: np.random.Generator) -> np.ndarray:
    """r seeded smooth unit perturbations: random Fourier coefficients with amplitude 1/k on wavenumbers
    1..N/3, zero mean, unit Euclidean norm; the same set is used at every sample of a trajectory."""
    k = np.fft.rfftfreq(N, d=1.0 / N); D = []
    for _ in range(r):
        c = (rng.normal(size=len(k)) + 1j * rng.normal(size=len(k))); c[0] = 0; c[k > N // 3] = 0; c[1:] /= k[1:]
        d = np.fft.irfft(c, n=N); d -= d.mean(); D.append(d / np.linalg.norm(d))
    return np.array(D)


def read_geometry(N: int, Dh: np.ndarray, budgets: list[int]) -> dict:
    """For the carried tangent set Dh (spectral), per budget B: the read fraction, the mean over the set of the
    share of each perturbation's energy in modes 1..B; and the Gram matrix of the read images, its leading
    eigenvalue, effective dimension (participation ratio) and shell thickness."""
    k = np.fft.rfftfreq(N, d=1.0 / N); w = np.where((k > 0) & (k < N / 2), 2.0, 1.0)  # Parseval weights for the real FFT
    tot = np.array([np.sum(w * np.abs(dh) ** 2) for dh in Dh]); out = {}
    for B in budgets:
        m = observer_mask(N, B); R = Dh[:, m]; e = np.array([np.sum(w[m] * np.abs(dh[m]) ** 2) for dh in Dh])
        G = np.real((R * w[m]) @ R.conj().T) / N; lam = np.maximum(np.sort(np.linalg.eigvalsh(G))[::-1], 0); s1 = lam.sum(); s2 = (lam ** 2).sum()
        out[str(B)] = {"read_fraction": float(np.mean(e / tot)), "lam1": float(lam[0]), "d_eff": float(s1 ** 2 / s2) if s2 > 0 else 0.0, "shell": float(lam[1] / lam[0]) if lam[0] > 0 else 0.0, "trace": float(s1)}
    out["total_energy"] = float(np.mean(tot))
    return out


# ----------------------------------------------------------------------------- one Burgers trajectory


def run_trajectory(world: dict, cfg: dict, seed: int, log=print) -> dict:
    rng = np.random.default_rng(seed + int(world["seed_offset"])); N = int(world["N"]); nu = float(world["nu"])
    u0, t_star = initial_condition(N, rng, int(cfg["ic_modes"]), float(cfg["ic_amp"]))
    model = Burgers(N, nu); uh = np.fft.rfft(u0); dt = float(cfg["dt_base"]) * (int(cfg["N_ref"]) / N)
    t_end = float(cfg["t_end_factor"]) * t_star; sample = float(cfg["sample_dt"]); n_samples = int(t_end / sample)
    budgets = [int(b) for b in cfg["budgets"] if b <= N // 3]; g0 = model.max_grad(uh)
    rec = {"t": [], "max_grad": [], "inv_grad": [], "geom": []}; t = 0.0; t0 = time.time()
    D0 = smooth_directions(N, int(cfg["sketch_r"]), np.random.default_rng(seed + 31 + int(world["seed_offset"]))); Dh = np.array([np.fft.rfft(d) for d in D0])
    for i in range(n_samples + 1):
        rec["t"].append(t); mg = model.max_grad(uh); rec["max_grad"].append(mg); rec["inv_grad"].append(1.0 / mg); rec.setdefault("max_u", []).append(float(np.max(np.abs(np.fft.irfft(uh, n=N)))))
        rec["geom"].append(read_geometry(N, Dh, budgets))
        steps = int(round(sample / dt))
        for _ in range(steps):
            new = []
            for dh in Dh:
                _, dn = model.tangent_step(uh, dh, dt); new.append(dn)
            uh = model.step(uh, dt); Dh = np.array(new)
        t += steps * dt
        if not np.all(np.isfinite(uh)): break
    # alarms
    fthr = float(cfg["read_fraction_alarm"]); mult = float(cfg["classical_multiple"]); ts = np.array(rec["t"])
    alarms = {}
    for B in budgets:
        f = np.array([g[str(B)]["read_fraction"] for g in rec["geom"]])
        idx = np.nonzero(f < fthr * f[0])[0]; alarms[str(B)] = float(ts[idx[0]]) if len(idx) else None
    mg = np.array(rec["max_grad"]); idx = np.nonzero(mg > mult * g0)[0]; classical_alarm = float(ts[idx[0]]) if len(idx) else None
    # classical prediction of t* from the first sample where the gradient has grown by 10 percent: linear extrapolation of 1/max|u_x|
    inv = np.array(rec["inv_grad"]); idx = np.nonzero(mg > 1.1 * g0)[0]
    if len(idx) >= 1 and idx[0] >= 1:
        i = idx[0]; slope = (inv[i] - inv[i - 1]) / (ts[i] - ts[i - 1]); classical_pred = float(ts[i] - inv[i] / slope) if slope < 0 else None
    else:
        classical_pred = None
    log(json.dumps({"world": world["name"], "N": N, "nu": nu, "t_star": round(t_star, 4), "samples": len(rec["t"]), "classical_alarm": classical_alarm, "obs_alarms": alarms, "seconds": round(time.time() - t0, 1)}))
    return {"name": world["name"], "group": world["group"], "N": N, "nu": nu, "ic_seed": int(world["seed_offset"]), "t_star": t_star, "g0": g0, "record": rec, "alarms_obs": alarms, "alarm_classical": classical_alarm, "classical_pred_t_star": classical_pred, "seconds": time.time() - t0}


# ----------------------------------------------------------------------------- 2-D Navier-Stokes negative control


class NS2D:
    def __init__(self, n: int, nu: float):
        self.n = n; self.nu = nu; k = np.fft.fftfreq(n, d=1.0 / n); self.kx, self.ky = np.meshgrid(k, k, indexing="ij")
        self.k2 = self.kx ** 2 + self.ky ** 2; self.k2[0, 0] = 1.0; kmax = (2.0 / 3.0) * (n / 2)
        self.dealias = (np.abs(self.kx) <= kmax) & (np.abs(self.ky) <= kmax)

    def velocity(self, wh):
        psih = wh / self.k2; return np.real(np.fft.ifft2(1j * self.ky * psih)), np.real(np.fft.ifft2(-1j * self.kx * psih))

    def rhs(self, wh):
        u, v = self.velocity(wh); wx = np.real(np.fft.ifft2(1j * self.kx * wh)); wy = np.real(np.fft.ifft2(1j * self.ky * wh))
        nl = np.fft.fft2(u * wx + v * wy); nl[~self.dealias] = 0
        return -nl - self.nu * self.k2 * wh

    def tangent_rhs(self, wh, dh):
        u, v = self.velocity(wh); du, dv = self.velocity(dh)
        wx = np.real(np.fft.ifft2(1j * self.kx * wh)); wy = np.real(np.fft.ifft2(1j * self.ky * wh))
        dx = np.real(np.fft.ifft2(1j * self.kx * dh)); dy = np.real(np.fft.ifft2(1j * self.ky * dh))
        nl = np.fft.fft2(u * dx + v * dy + du * wx + dv * wy); nl[~self.dealias] = 0
        return -nl - self.nu * self.k2 * dh

    def step(self, wh, dt):
        k1 = self.rhs(wh); k2 = self.rhs(wh + 0.5 * dt * k1); k3 = self.rhs(wh + 0.5 * dt * k2); k4 = self.rhs(wh + dt * k3)
        return wh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def tangent_step(self, wh, dh, dt):
        k1 = self.rhs(wh); l1 = self.tangent_rhs(wh, dh)
        k2 = self.rhs(wh + 0.5 * dt * k1); l2 = self.tangent_rhs(wh + 0.5 * dt * k1, dh + 0.5 * dt * l1)
        k3 = self.rhs(wh + 0.5 * dt * k2); l3 = self.tangent_rhs(wh + 0.5 * dt * k2, dh + 0.5 * dt * l2)
        k4 = self.rhs(wh + dt * k3); l4 = self.tangent_rhs(wh + dt * k3, dh + dt * l3)
        return wh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), dh + dt / 6 * (l1 + 2 * l2 + 2 * l3 + l4)

    def max_grad(self, wh):
        u, v = self.velocity(wh); ux = np.real(np.fft.ifft2(1j * self.kx * np.fft.fft2(u))); vy = np.real(np.fft.ifft2(1j * self.ky * np.fft.fft2(v)))
        uy = np.real(np.fft.ifft2(1j * self.ky * np.fft.fft2(u))); vx = np.real(np.fft.ifft2(1j * self.kx * np.fft.fft2(v)))
        return float(np.max(np.sqrt(ux ** 2 + uy ** 2 + vx ** 2 + vy ** 2)))


def ns_smooth_directions(n: int, r: int, rng: np.random.Generator) -> list:
    k = np.fft.fftfreq(n, d=1.0 / n); kx, ky = np.meshgrid(k, k, indexing="ij"); kmag = np.sqrt(kx ** 2 + ky ** 2); D = []
    for _ in range(r):
        c = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); c[kmag == 0] = 0; c[kmag > n // 3] = 0; c[kmag > 0] /= kmag[kmag > 0]
        d = np.real(np.fft.ifft2(c)); d -= d.mean(); D.append(np.fft.fft2(d / np.linalg.norm(d)))
    return D


def ns_read_geometry(model: NS2D, Dh, budgets) -> dict:
    n = model.n; out = {}; kmag = np.sqrt(model.kx ** 2 + model.ky ** 2); tot = np.array([np.sum(np.abs(dh) ** 2) for dh in Dh])
    for B in budgets:
        m = (kmag >= 1) & (kmag <= B); R = np.array([dh[m] for dh in Dh]); e = np.array([np.sum(np.abs(dh[m]) ** 2) for dh in Dh])
        G = np.real(R @ R.conj().T) / (n * n); lam = np.maximum(np.sort(np.linalg.eigvalsh(G))[::-1], 0); s1 = lam.sum(); s2 = (lam ** 2).sum()
        out[str(B)] = {"read_fraction": float(np.mean(e / tot)), "lam1": float(lam[0]), "d_eff": float(s1 ** 2 / s2) if s2 > 0 else 0.0, "shell": float(lam[1] / lam[0]) if lam[0] > 0 else 0.0, "trace": float(s1)}
    out["total_energy"] = float(np.mean(tot))
    return out


def run_ns_control(world: dict, cfg: dict, seed: int, log=print) -> dict:
    rng = np.random.default_rng(seed + int(world["seed_offset"])); n = int(world["N"]); nu = float(world["nu"]); model = NS2D(n, nu)
    # smooth seeded initial vorticity: a few low modes
    x = 2 * np.pi * np.arange(n) / n; X, Y = np.meshgrid(x, x, indexing="ij"); w = np.zeros((n, n))
    for _ in range(int(cfg["ns_modes"])):
        kx, ky = rng.integers(1, 4, size=2); a, b = rng.normal(size=2)
        w += a * np.cos(kx * X + b) * np.sin(ky * Y + a)
    w *= float(cfg["ns_amp"]) / np.max(np.abs(w)); wh = np.fft.fft2(w); dt = float(cfg["ns_dt"]); sample = float(cfg["sample_dt"]); t_end = float(cfg["ns_t_end"])
    budgets = [int(b) for b in cfg["budgets"] if b <= n // 3]; g0 = model.max_grad(wh); rec = {"t": [], "max_grad": [], "geom": []}; t = 0.0; t0 = time.time()
    Dh = ns_smooth_directions(n, int(cfg["ns_sketch_r"]), np.random.default_rng(seed + 31 + int(world["seed_offset"]))); sample = float(cfg["ns_sample_dt"])
    for i in range(int(t_end / sample) + 1):
        rec["t"].append(t); rec["max_grad"].append(model.max_grad(wh)); uu, vv = model.velocity(wh); rec.setdefault("max_u", []).append(float(np.max(np.sqrt(uu ** 2 + vv ** 2))))
        rec["geom"].append(ns_read_geometry(model, Dh, budgets))
        for _ in range(int(round(sample / dt))):
            new = []
            for dh in Dh:
                _, dn = model.tangent_step(wh, dh, dt); new.append(dn)
            wh = model.step(wh, dt); Dh = new
        t += int(round(sample / dt)) * dt
    fthr = float(cfg["read_fraction_alarm"]); ts = np.array(rec["t"]); alarms = {}
    for B in budgets:
        f = np.array([g[str(B)]["read_fraction"] for g in rec["geom"]])
        idx = np.nonzero(f < fthr * f[0])[0]; alarms[str(B)] = float(ts[idx[0]]) if len(idx) else None
    log(json.dumps({"world": world["name"], "N": n, "nu": nu, "samples": len(ts), "max_grad_ratio": round(max(rec["max_grad"]) / g0, 3), "obs_alarms": alarms, "seconds": round(time.time() - t0, 1)}))
    return {"name": world["name"], "group": world["group"], "N": n, "nu": nu, "g0": g0, "record": rec, "alarms_obs": alarms, "max_grad_ratio": max(rec["max_grad"]) / g0, "seconds": time.time() - t0}


def run(cfg: dict, seed_role: str, out_path: str) -> dict:
    seed = int(cfg[f"seed_{seed_role}"]); groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if seed_role == "probe":
            if not world.get("in_probe"): continue
        elif world["group"] not in groups: continue
        result["worlds"].append(run_ns_control(world, cfg, seed) if world["family"] == "ns2d" else run_trajectory(world, cfg, seed))
        json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


# ----------------------------------------------------------------------------- self test


def selftest() -> int:
    fails = 0; rng = np.random.default_rng(0)
    # 1. the spectral inviscid solver matches the characteristics solution before the shock, and converges with N
    u0f, t_star = initial_condition(4096, rng, 2, 1.0); errs = []
    for N in (128, 256, 512):
        m = Burgers(N, 0.0); u0 = np.interp(m.x, 2 * np.pi * np.arange(4096) / 4096, u0f, period=2 * np.pi); uh = np.fft.rfft(u0); dt = 0.002 * 256 / N; t = 0.0
        while t < 0.5 * t_star - 1e-12:
            uh = m.step(uh, dt); t += dt
        errs.append(float(np.max(np.abs(np.fft.irfft(uh, n=N) - exact_inviscid(u0f, t, m.x)))))
    # the reference is the characteristics solution interpolated from 4096 points (about 1e-6 itself), so the check is that every
    # resolution sits at that floor and none is worse than twice the coarsest
    ok = max(errs) < 1e-4 and errs[2] <= 2 * errs[0]; print("inviscid solver vs characteristics at t*/2: errors", ["%.1e" % e for e in errs], ok); fails += 0 if ok else 1
    # 2. the classical extrapolation of 1/max|u_x| recovers t* exactly for inviscid Burgers (pre-shock)
    m = Burgers(512, 0.0); u0 = np.interp(m.x, 2 * np.pi * np.arange(4096) / 4096, u0f, period=2 * np.pi); uh = np.fft.rfft(u0); dt = 0.001; t = 0.0; inv = []; ts = []
    for i in range(int(0.3 * t_star / dt)):
        if i % 50 == 0: ts.append(t); inv.append(1 / m.max_grad(uh))
        uh = m.step(uh, dt); t += dt
    slope = (inv[-1] - inv[-2]) / (ts[-1] - ts[-2]); pred = ts[-1] - inv[-1] / slope; ok = abs(pred - t_star) < 0.02 * t_star
    print("classical extrapolation predicts t* = %.4f (exact %.4f)" % (pred, t_star), ok); fails += 0 if ok else 1
    # 3. tangent propagator matches a finite difference of the nonlinear solver
    m = Burgers(128, 0.01); uh = np.fft.rfft(np.sin(m.x)); dh = np.fft.rfft(np.cos(2 * m.x)) * 1e-6
    u1, d1 = m.tangent_step(uh, dh, 0.005); u1b = m.step(uh + dh, 0.005); fd = u1b - u1
    ok = np.linalg.norm(fd - d1) / np.linalg.norm(d1) < 1e-4; print("tangent step vs finite difference: rel err %.1e" % (np.linalg.norm(fd - d1) / np.linalg.norm(d1)), ok); fails += 0 if ok else 1
    # 4. the observer with budget B reads exactly the modes 1..B; a larger budget reads at least as much trace
    Dh = np.array([np.fft.rfft(d) for d in smooth_directions(128, 8, np.random.default_rng(3))]); g = read_geometry(128, Dh, [4, 16, 42])
    ok = g["4"]["read_fraction"] <= g["16"]["read_fraction"] <= g["42"]["read_fraction"] <= 1.0 + 1e-9 and abs(g["42"]["read_fraction"] - 1.0) < 1e-9 and all(1 <= g[b]["d_eff"] <= 8 for b in ("4", "16", "42"))
    print("budgets read nested fractions:", ["%.3f" % g[b]["read_fraction"] for b in ("4", "16", "42")], "(42 = every mode of the set)", ok); fails += 0 if ok else 1
    # 5. NS2D: the vorticity solver conserves energy and enstrophy at nu = 0 over a short run (to 1e-6), and its tangent matches a finite difference
    ns = NS2D(32, 0.0); x = 2 * np.pi * np.arange(32) / 32; X, Y = np.meshgrid(x, x, indexing="ij"); wh = np.fft.fft2(np.sin(X) * np.cos(Y) + 0.5 * np.cos(2 * X + Y))
    def energy(wh):
        u, v = ns.velocity(wh); return float(np.mean(u ** 2 + v ** 2))
    e0 = energy(wh); z0 = float(np.mean(np.real(np.fft.ifft2(wh)) ** 2)); w2 = wh.copy()
    for _ in range(50): w2 = ns.step(w2, 0.002)
    e1 = energy(w2); z1 = float(np.mean(np.real(np.fft.ifft2(w2)) ** 2)); ok = abs(e1 - e0) / e0 < 1e-6 and abs(z1 - z0) / z0 < 1e-5
    print("NS2D energy %.3e -> %.3e, enstrophy %.3e -> %.3e" % (e0, e1, z0, z1), ok); fails += 0 if ok else 1
    dh = np.fft.fft2(np.cos(3 * X) * 1e-6); w1, d1 = ns.tangent_step(wh, dh, 0.002); fd = ns.step(wh + dh, 0.002) - w1
    ok = np.linalg.norm(fd - d1) / np.linalg.norm(d1) < 1e-4; print("NS2D tangent vs finite difference: rel err %.1e" % (np.linalg.norm(fd - d1) / np.linalg.norm(d1)), ok); fails += 0 if ok else 1
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
