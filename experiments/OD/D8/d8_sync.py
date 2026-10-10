"""D8: which modes an observer must read to synchronize a nudged copy of a two-dimensional flow (OD track, gate D8).

World. Forced two-dimensional turbulence: D5's NS2D (vorticity form, pseudo-spectral, 2/3 dealiasing, RK4) with
Kolmogorov forcing f = F0 k_f cos(k_f y) and linear drag -alpha w, from a seeded random vorticity on |k| <= ic_kmax that
is the same physical field at every resolution, spun up to a statistically stationary state. An explicit-RK4 guard refuses
a world whose (nu k_max^2 + alpha + mu) dt exceeds 1 or whose advective CFL exceeds 0.5.

Units. Spectral fields are numpy fft2 arrays; math coefficients are fft / n^2, |f|^2 = (2 pi)^2 sum |f_k|^2, and the
velocity norm of a vorticity field is (2 pi) sqrt(sum |w_k|^2 / |k|^2), checked against physical space in the self-test.

Observers. Rankings of the candidate Fourier pairs (every dealiased k != 0, one per +-k pair), computed on a training
trajectory: READ, the training mean of |w_k|^2 times the sensitivity s_k = (|N_u e_re|^2 + |N_u e_im|^2) / 2 of the
nonlinear tendency to a unit perturbation of the pair (the dynamical read distortion, notes/dynamical-read-operator.md
Section 6); ENSTROPHY, the training mean of |w_k|^2 (the pair's enstrophy contribution, READ's amplitude factor); KE,
|w_k|^2 / |k|^2 (its kinetic energy); BALL, |k| ascending (the Foias-Prodi observer); these three are the graded controls.
SENS, s_k alone (recorded); RANDOM, seeded permutations (the null).

Nudging. On fresh test trajectories, v_t = F(v) - mu P_S (v - u), v(0) = 0, S the top m pairs of an observer, for every m
on the ladder, all integrated in one batch with the reference u; delta(t) = |w_v - w_u| / |w_u|. A cell is synchronized
when delta <= sync_threshold at every sample of the final window of length T_hold (sustained, not an endpoint crossing).
m* is the smallest ladder value at which it and every larger ladder value synchronize, None (censored) if the top does
not; it is a finite-time synchronization budget, not a count of determining modes. Beside every cell the Lyapunov
exponent of the finite-gain observer's linearised error, e_t = [DF(u) - mu P_S] e, and in declared roles that of the
discarded block Q_S DF(u) Q_S (its mu -> infinity limit). In declared roles the graded observers are re-run at dt / 2.

Theorem checks (notes/dynamical-read-operator.md). T1, Proposition 2: with the base state set to p = P_N u, the
central-difference read of the resolved tendency on every discarded pair with |k| > 2N, against the largest first-octave
read. T2, Proposition 3: the ratio |r_N| / (c_N (2|p| |Pi_(N,2N] q| + |q|^2)) in the velocity norm, c_N = N sqrt(K_N) / (2 pi).

    python d8_sync.py --selftest
    python d8_sync.py --config prereg_config.json --seed-role probe --out probe.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "D5"))
from d5_burgers import NS2D  # noqa: E402

TWO_PI = 2.0 * math.pi


class ForcedNS2D(NS2D):
    """D5's NS2D with Kolmogorov forcing and linear drag; every method accepts a batch (..., n, n) of spectral fields."""

    def __init__(self, n: int, nu: float, alpha: float, F0: float, kf: int):
        super().__init__(n, nu)
        self.alpha = alpha; self.kf = kf
        x = TWO_PI * np.arange(n) / n; _, Y = np.meshgrid(x, x, indexing="ij")
        self.fh = np.fft.fft2(F0 * kf * np.cos(kf * Y))
        self.kmag = np.sqrt(self.kx ** 2 + self.ky ** 2)
        self.k2true = self.kx ** 2 + self.ky ** 2

    def nl_hat(self, wh):
        u, v = self.velocity(wh)
        wx = np.real(np.fft.ifft2(1j * self.kx * wh)); wy = np.real(np.fft.ifft2(1j * self.ky * wh))
        nl = np.fft.fft2(u * wx + v * wy); nl[..., ~self.dealias] = 0
        return nl

    def tangent_nl(self, wh, dh):
        """The nonlinear part of the tangent, N_w d = -dealias(u . grad d + du . grad w); w may be one field, d a batch."""
        u, v = self.velocity(wh); du, dv = self.velocity(dh)
        wx = np.real(np.fft.ifft2(1j * self.kx * wh)); wy = np.real(np.fft.ifft2(1j * self.ky * wh))
        dx = np.real(np.fft.ifft2(1j * self.kx * dh)); dy = np.real(np.fft.ifft2(1j * self.ky * dh))
        nl = np.fft.fft2(u * dx + v * dy + du * wx + dv * wy); nl[..., ~self.dealias] = 0
        return -nl

    def frhs(self, wh):
        return -self.nl_hat(wh) - self.nu * self.k2 * wh - self.alpha * wh + self.fh

    def ftangent(self, wh, dh):
        return self.tangent_nl(wh, dh) - self.nu * self.k2 * dh - self.alpha * dh

    def fstep(self, wh, dt):
        k1 = self.frhs(wh); k2 = self.frhs(wh + 0.5 * dt * k1); k3 = self.frhs(wh + 0.5 * dt * k2); k4 = self.frhs(wh + dt * k3)
        return wh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# ---------------------------------------------------------------- norms and fields (math units: f_hat = fft / n^2)

def sq(model, X):
    """Sum of |coefficient|^2 over the last two axes in math units (mean of |f|^2 over the box)."""
    return np.sum(np.abs(X) ** 2, axis=(-2, -1)) / model.n ** 4


def vel_norm(model, wh) -> float:
    """L2 norm of the velocity of a vorticity field, (2 pi) sqrt(sum |w_k|^2 / |k|^2)."""
    k2 = model.k2true.copy(); k2[0, 0] = np.inf
    return float(TWO_PI * np.sqrt(np.sum(np.abs(wh) ** 2 / k2) / model.n ** 4))


def initial_field(model, rng: np.random.Generator, kmax: int, omega_rms: float) -> np.ndarray:
    """Seeded vorticity on 0 < |k| <= kmax, the same physical field at every n (draws in a fixed k order); rms = omega_rms."""
    n = model.n; coef = {}
    for kx in range(-kmax, kmax + 1):
        for ky in range(-kmax, kmax + 1):
            if (kx > 0 or (kx == 0 and ky > 0)) and kx * kx + ky * ky <= kmax * kmax:
                coef[(kx, ky)] = complex(rng.normal(), rng.normal())
    s = math.sqrt(2 * sum(abs(c) ** 2 for c in coef.values()))
    wh = np.zeros((n, n), complex)
    for (kx, ky), c in coef.items():
        c *= omega_rms / s; wh[kx % n, ky % n] = n * n * c; wh[-kx % n, -ky % n] = n * n * np.conj(c)
    return wh


def spin_up(model, wh, T: float, dt: float):
    for _ in range(int(round(T / dt))):
        wh = model.fstep(wh, dt)
    return wh


def spectrum_tail(model, wh) -> float:
    """Shell enstrophy at the dealiasing wavenumber over the peak shell enstrophy."""
    shells = np.rint(model.kmag).astype(int); Z = np.bincount(shells.ravel(), weights=(np.abs(wh) ** 2).ravel())
    kd = int((2.0 / 3.0) * (model.n / 2)); return float(Z[kd] / Z[1:].max())


# ---------------------------------------------------------------- candidates and rankings

class Candidates:
    """Every dealiased Fourier pair k != 0, one representative per +-k (kx > 0, or kx = 0 and ky > 0)."""

    def __init__(self, model):
        n = model.n; kx = model.kx.astype(int); ky = model.ky.astype(int)
        half = model.dealias & ((kx > 0) | ((kx == 0) & (ky > 0)))
        self.ix, self.iy = np.nonzero(half); self.kx = kx[self.ix, self.iy]; self.ky = ky[self.ix, self.iy]
        self.nix = (-self.ix) % n; self.niy = (-self.iy) % n; self.kmag = np.sqrt(self.kx ** 2 + self.ky ** 2); self.size = len(self.ix)

    def unit(self, sel: np.ndarray, n: int, imag: bool) -> np.ndarray:
        E = np.zeros((len(sel), n, n), complex); r = np.arange(len(sel))
        E[r, self.ix[sel], self.iy[sel]] = 1j if imag else 1.0; E[r, self.nix[sel], self.niy[sel]] = -1j if imag else 1.0
        return E

    def mask(self, sel: np.ndarray, n: int) -> np.ndarray:
        M = np.zeros((n, n)); M[self.ix[sel], self.iy[sel]] = 1.0; M[self.nix[sel], self.niy[sel]] = 1.0
        return M

    def ball_order(self) -> np.ndarray:
        ang = np.arctan2(self.ky, self.kx); return np.lexsort((np.arange(self.size), ang, np.round(self.kmag, 12)))


def sensitivities(model, wh, cand: Candidates, chunk: int) -> np.ndarray:
    """s_k = (|N_w e_re|^2 + |N_w e_im|^2) / 2 for every candidate pair, in math units."""
    s = np.empty(cand.size)
    for a in range(0, cand.size, chunk):
        sel = np.arange(a, min(a + chunk, cand.size))
        s[sel] = 0.5 * (sq(model, model.tangent_nl(wh, cand.unit(sel, model.n, False))) + sq(model, model.tangent_nl(wh, cand.unit(sel, model.n, True))))
    return s


def amplitudes(model, wh, cand: Candidates) -> np.ndarray:
    return np.abs(wh[cand.ix, cand.iy]) ** 2 / model.n ** 4


# ---------------------------------------------------------------- theorem checks (Propositions 2 and 3)

def theorem_checks(model, wh, cand: Candidates, N: float, chunk: int) -> dict:
    n = model.n; obs = model.kmag <= N; p = np.where(obs, wh, 0); q = np.where(obs, 0, wh)

    def T(W):  # the resolved nonlinear tendency, P_N of -nl
        return np.where(obs, -model.nl_hat(W), 0)

    disc = np.nonzero(cand.kmag > N)[0]; eps = float(np.max(np.abs(p))) or 1.0; reads = np.empty(len(disc))
    for a in range(0, len(disc), chunk):
        sel = disc[a:a + chunk]; r2 = 0.0
        for imag in (False, True):
            E = cand.unit(sel, n, imag); r2 = r2 + sq(model, (T(p + eps * E) - T(p - eps * E)) / (2 * eps))
        reads[a:a + len(sel)] = np.sqrt(r2)
    octave = cand.kmag[disc] <= 2 * N; first = float(reads[octave].max()) if octave.any() else 0.0; beyond = float(reads[~octave].max()) if (~octave).any() else 0.0
    # Proposition 3 in the velocity norm
    rN = T(wh) - T(p); KN = int(np.sum((model.kmag > 0) & (model.kmag <= N))); cN = N * math.sqrt(KN) / TWO_PI
    oct_q = np.where((model.kmag > N) & (model.kmag <= 2 * N), wh, 0)
    bound = cN * (2 * vel_norm(model, p) * vel_norm(model, oct_q) + vel_norm(model, q) ** 2)
    return {"N": N, "eps": eps, "first_octave_max_read": first, "beyond_2N_max_read": beyond, "T1_ratio": beyond / first if first > 0 else None,
            "n_first_octave": int(octave.sum()), "n_beyond": int((~octave).sum()), "rN_vel": vel_norm(model, rN), "bound": bound, "T2_ratio": vel_norm(model, rN) / bound if bound > 0 else None, "c_N": cN}


# ---------------------------------------------------------------- batched nudging

def nudged_rhs(model, W, M, mu: float):
    """Row 0 of W is the reference u, rows 1.. the nudged copies; M[0] = 0. Copy b obeys v_t = F(v) - mu M_b (v - u)."""
    return model.frhs(W) - mu * M * (W - W[0])


def observer_tangent(model, u, D, M, mu: float):
    """The linearised error of the finite-gain observer, e_t = [DF(u) - mu P_S] e (review point 3, 2026-10-09)."""
    return model.ftangent(u, D) - mu * M * D


def block_tangent(model, u, D, Q):
    """The discarded block Q_S DF(u) Q_S, the mu -> infinity limit of the observer (recorded only)."""
    return Q * model.ftangent(u, D)


def nudge_group(model, uh0, masks: np.ndarray, mu: float, dt: float, T: float, dt_sample: float, obs_lyap: bool, block_lyap: bool, rng: np.random.Generator) -> dict:
    """Integrate the reference and one nudged copy per mask in one batch; masks (B, n, n) in {0, 1}. With obs_lyap, carry one
    tangent vector per mask under the full finite-gain observer DF(u) - mu P_S; with block_lyap, one under Q_S DF(u) Q_S. Both
    are renormalised at every sample and their exponents returned."""
    B = masks.shape[0]; n = model.n
    W = np.concatenate([uh0[None], np.zeros((B, n, n), complex)]); M = np.concatenate([np.zeros((1, n, n)), masks]); Mc = masks
    Q = (1.0 - masks) * model.dealias; tang = {}
    if obs_lyap:
        D = np.fft.fft2(rng.normal(size=(B, n, n))) * model.dealias; tang["obs"] = [D / np.sqrt(sq(model, D))[:, None, None], np.zeros(B), lambda u, X: observer_tangent(model, u, X, Mc, mu)]
    if block_lyap:
        D = np.fft.fft2(rng.normal(size=(B, n, n))) * Q; tang["block"] = [D / np.sqrt(sq(model, D))[:, None, None], np.zeros(B), lambda u, X: block_tangent(model, u, X, Q)]

    per = int(round(dt_sample / dt)); steps = int(round(T / dt)); nrec = steps // per
    delta = np.empty((nrec + 1, B)); times = np.empty(nrec + 1)

    def record(i, t):
        times[i] = t; delta[i] = np.sqrt(sq(model, W[1:] - W[0]) / sq(model, W[0]))

    record(0, 0.0)
    for i in range(1, nrec + 1):
        for _ in range(per):
            u = W[0]
            k1 = nudged_rhs(model, W, M, mu); W2 = W + 0.5 * dt * k1; k2 = nudged_rhs(model, W2, M, mu); W3 = W + 0.5 * dt * k2
            k3 = nudged_rhs(model, W3, M, mu); W4 = W + dt * k3; k4 = nudged_rhs(model, W4, M, mu)
            for tv in tang.values():
                D, H = tv[0], tv[2]
                l1 = H(u, D); l2 = H(W2[0], D + 0.5 * dt * l1); l3 = H(W3[0], D + 0.5 * dt * l2); l4 = H(W4[0], D + dt * l3)
                tv[0] = D + dt / 6 * (l1 + 2 * l2 + 2 * l3 + l4)
            W = W + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        record(i, i * per * dt)
        for tv in tang.values():
            nr = np.sqrt(sq(model, tv[0])); tv[1] += np.log(nr); tv[0] = tv[0] / nr[:, None, None]
    out = {"times": times, "delta": delta, "u_final": W[0]}
    for k, tv in tang.items():
        out[f"lyap_{k}"] = tv[1] / times[-1]
    return out


def stability(model, uh, dt: float, mu: float) -> dict:
    """Explicit-RK4 numbers for the declared step (review point 6): the linear stiffness (nu k_max^2 + alpha + mu) dt, which
    must stay inside RK4's real-axis stability interval (2.78) with margin, and the advective CFL max|u| dt / dx."""
    kmax2 = float(model.k2true[model.dealias].max()); u, v = model.velocity(uh); umax = float(np.sqrt(u ** 2 + v ** 2).max())
    lin = (model.nu * kmax2 + model.alpha + mu) * dt; cfl = umax * dt / (TWO_PI / model.n)
    return {"linear_stiffness": lin, "cfl": cfl, "ok": bool(lin <= 1.0 and cfl <= 0.5)}


def synced(times: np.ndarray, d: np.ndarray, thr: float, hold: float) -> tuple[bool, float]:
    """Sustained synchronization (review point 5): delta <= thr at every sample of the final hold window. The slope of
    log10 delta over that window is returned for the record only."""
    q = times >= times[-1] - hold - 1e-9; y = np.log10(np.maximum(d[q], 1e-300)); slope = float(np.polyfit(times[q], y, 1)[0]) if q.sum() >= 2 else 0.0
    return bool(np.all(d[q] <= thr)), slope


def m_star(ladder: list[int], flags: list[bool]) -> tuple[int | None, bool]:
    ms = None
    for m, f in sorted(zip(ladder, flags), reverse=True):
        if not f: break
        ms = m
    nonmono = ms is not None and any(f for m, f in zip(ladder, flags) if m < ms) or (ms is None and any(flags))
    return ms, bool(nonmono)


# ---------------------------------------------------------------- one world

def lyapunov(model, uh, dt: float, T: float, dt_sample: float, rng) -> float:
    D = np.fft.fft2(rng.normal(size=(model.n, model.n))) * model.dealias; D /= math.sqrt(sq(model, D)); per = int(round(dt_sample / dt)); s = 0.0; t = 0.0
    for _ in range(int(round(T / dt_sample))):
        for _ in range(per):
            k1 = model.frhs(uh); l1 = model.ftangent(uh, D); u2 = uh + 0.5 * dt * k1; k2 = model.frhs(u2); l2 = model.ftangent(u2, D + 0.5 * dt * l1)
            u3 = uh + 0.5 * dt * k2; k3 = model.frhs(u3); l3 = model.ftangent(u3, D + 0.5 * dt * l2); u4 = uh + dt * k3; k4 = model.frhs(u4); l4 = model.ftangent(u4, D + dt * l3)
            uh = uh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); D = D + dt / 6 * (l1 + 2 * l2 + 2 * l3 + l4); t += dt
        nr = math.sqrt(sq(model, D)); s += math.log(nr); D /= nr
    return s / t


GRADED = ("READ", "BALL", "ENSTROPHY", "KE")


def nudge_record(model, u0, cand, o, ladder, mu, dt, cfg, lyap: tuple[bool, bool], rng, d0) -> dict:
    n = model.n; masks = np.stack([cand.mask(o[:m], n) for m in ladder])
    g = nudge_group(model, u0, masks, mu, dt, float(cfg["T_sync"]), float(cfg["dt_sample"]), lyap[0], lyap[1], rng)
    flags, slopes = zip(*[synced(g["times"], g["delta"][:, b], float(cfg["sync_threshold"]), float(cfg["T_hold"])) for b in range(len(ladder))])
    ms, nonmono = m_star(ladder, list(flags)); st = int(cfg["series_stride"])
    rec = {"m_star": ms, "censored": ms is None, "nonmonotone": nonmono, "synced": list(flags), "slope_hold": list(slopes), "delta_final": g["delta"][-1].tolist(),
           "delta_series": g["delta"][::st].tolist(), "times": g["times"][::st].tolist(),
           "initial_spreading_rate": [float(d0.sum() - d0[o[:m]].sum()) for m in ladder]}
    for k in ("lyap_obs", "lyap_block"):
        if k in g: rec[k] = g[k].tolist()
    return rec


def run_world(world: dict, cfg: dict, seed_train: int, seed_test: int, K: int, seed_role: str, log=print) -> dict:
    n = int(world["n"]); model = ForcedNS2D(n, float(world["nu"]), float(cfg["alpha"]), float(cfg["F0"]), int(cfg["kf"]))
    dt = float(cfg["dt_base"]) * int(cfg["n_ref"]) / n; ds = float(cfg["dt_sample"]); chunk = int(cfg["chunk"]); cand = Candidates(model); mu = float(cfg["mu"])
    ladder = [m for m in cfg["ladder"] if m <= cand.size]; off = int(world["seed_offset"]); t0 = time.time()
    out = {"name": world["name"], "group": world["group"], "n": n, "nu": model.nu, "dt": dt, "n_candidates": cand.size, "ladder": ladder}

    # training trajectory: rankings and theorem checks
    rng = np.random.default_rng(seed_train + off); uh = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
    out["train_spectrum_tail"] = spectrum_tail(model, uh); out["stability"] = stability(model, uh, dt, mu)
    nsamp = int(round(float(cfg["T_train"]) / ds)); per = int(round(ds / dt)); A = np.zeros(cand.size); S = np.zeros(cand.size); R = np.zeros(cand.size)
    th_at = set(np.linspace(0, nsamp - 1, int(cfg["theorem_snapshots"])).round().astype(int).tolist()); checks = []; cfl_max = 0.0
    for i in range(nsamp):
        a = amplitudes(model, uh, cand); s = sensitivities(model, uh, cand, chunk); A += a; S += s; R += a * s
        cfl_max = max(cfl_max, stability(model, uh, dt, mu)["cfl"])
        if i in th_at:
            for N in cfg["cutoffs"]:
                checks.append({"sample": i, **theorem_checks(model, uh, cand, float(N), chunk)})
        for _ in range(per):
            uh = model.fstep(uh, dt)
    A /= nsamp; S /= nsamp; R /= nsamp
    out["stability"]["cfl_max_train"] = cfl_max; out["stability"]["ok"] = bool(out["stability"]["linear_stiffness"] <= 1.0 and cfl_max <= 0.5)
    # ENSTROPHY ranks |w_k|^2, the amplitude factor READ uses (|w_k|^2 is the pair's enstrophy contribution, not its energy);
    # KE ranks the kinetic energy |w_k|^2 / |k|^2; both are graded controls beside BALL; SENS is recorded only
    orders = {"READ": np.argsort(-R, kind="stable"), "ENSTROPHY": np.argsort(-A, kind="stable"), "KE": np.argsort(-A / cand.kmag ** 2, kind="stable"),
              "BALL": cand.ball_order(), "SENS": np.argsort(-S, kind="stable")}
    rr = np.random.default_rng(seed_train + off + 977)
    for j in range(int(cfg["random_draws"])):
        orders[f"RANDOM{j}"] = rr.permutation(cand.size)
    top = max(ladder)
    out["rankings"] = {k: [[int(cand.kx[i]), int(cand.ky[i])] for i in o[:top]] for k, o in orders.items()}
    out["theorem_checks"] = checks; out["train_seconds"] = time.time() - t0
    log(json.dumps({"world": world["name"], "phase": "train", "candidates": cand.size, "tail": round(out["train_spectrum_tail"], 9), "stability": out["stability"],
                    "T1_max": max((c["T1_ratio"] or 0.0) for c in checks) if checks else None, "T2_max": max((c["T2_ratio"] or 0.0) for c in checks) if checks else None, "seconds": round(time.time() - t0, 1)}))
    if not out["stability"]["ok"]:
        out["tests"] = []; out["refused"] = "explicit RK4 stability guard failed; no nudging run (fix dt and re-probe)"; log(json.dumps({"world": world["name"], "refused": out["refused"]}))
        return out

    # test trajectories: nudging
    out["tests"] = []; lyap = (bool(cfg["obs_lyap"]), seed_role in cfg.get("block_lyap_roles", []))
    mu_rec = [float(m) for m in cfg.get("mu_record", [])] if seed_role in cfg.get("mu_record_roles", []) else []
    refine = seed_role in cfg.get("dt_refine_roles", [])
    for j in range(K):
        t1 = time.time(); rng = np.random.default_rng(seed_test + 100 * off + j)
        u0 = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
        a0 = amplitudes(model, u0, cand); s0 = sensitivities(model, u0, cand, chunk); d0 = a0 * s0
        test = {"index": j, "spectrum_tail": spectrum_tail(model, u0), "observers": {}, "mu_record": {}, "dt_half": {}}
        test["lyapunov"] = lyapunov(model, u0, dt, float(cfg["T_lyap"]), ds, np.random.default_rng(seed_test + 100 * off + j + 55)) if cfg.get("lyapunov", True) else None
        # instrument group (E1): nothing observed and everything observed
        g = nudge_group(model, u0, np.stack([np.zeros((n, n)), cand.mask(np.arange(cand.size), n)]), mu, dt, float(cfg["T_sync"]), ds, False, False, rng)
        test["none_final"] = float(g["delta"][-1, 0]); test["all_final"] = float(g["delta"][-1, 1])
        test["all_hold_max"] = float(g["delta"][g["times"] >= g["times"][-1] - float(cfg["T_hold"]) - 1e-9, 1].max())
        for name, o in orders.items():
            rec = nudge_record(model, u0, cand, o, ladder, mu, dt, cfg, lyap, np.random.default_rng(seed_test + 7 * j + 3), d0); test["observers"][name] = rec
            log(json.dumps({"world": world["name"], "test": j, "observer": name, "m_star": rec["m_star"], "nonmonotone": rec["nonmonotone"], "seconds": round(time.time() - t1, 1)}))
        for m_ in mu_rec:
            for name in GRADED:
                test["mu_record"].setdefault(str(m_), {})[name] = nudge_record(model, u0, cand, orders[name], ladder, m_, dt, cfg, (False, False), rng, d0)
        if refine:  # time-step refinement on the graded observers
            for name in GRADED:
                test["dt_half"][name] = nudge_record(model, u0, cand, orders[name], ladder, mu, dt / 2, cfg, (False, False), rng, d0)
                log(json.dumps({"world": world["name"], "test": j, "observer": name, "dt_half_m_star": test["dt_half"][name]["m_star"], "m_star": test["observers"][name]["m_star"]}))
        test["seconds"] = time.time() - t1; out["tests"].append(test)
    out["seconds"] = time.time() - t0
    return out


def run(cfg: dict, seed_role: str, out_path: str) -> dict:
    if seed_role == "probe":
        seed_train = seed_test = int(cfg["seed_probe"]); seed_test += 5000
    else:
        seed_train = int(cfg[f"seed_{seed_role}_train"]); seed_test = int(cfg[f"seed_{seed_role}_test"])
    K = int(cfg["K_by_role"][seed_role]); groups = cfg["groups_by_role"][seed_role]
    result = {"config": cfg, "seed_role": seed_role, "seed_train": seed_train, "seed_test": seed_test, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if world["group"] not in groups: continue
        result["worlds"].append(run_world(world, cfg, seed_train, seed_test, K, seed_role)); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    return result


# ---------------------------------------------------------------- self-test

def selftest() -> int:
    fails = 0; rng = np.random.default_rng(0)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    n = 32; nu = 0.01; alpha = 0.1; model = ForcedNS2D(n, nu, alpha, 1.0, 4); cand = Candidates(model)
    # 1. the laminar Kolmogorov flow is a fixed point of the forced solver
    x = TWO_PI * np.arange(n) / n; _, Y = np.meshgrid(x, x, indexing="ij"); lam = np.fft.fft2(4 * np.cos(4 * Y) / (nu * 16 + alpha))
    r = math.sqrt(sq(model, model.frhs(lam)) / sq(model, model.fh)); check("laminar fixed point |F(w*)| / |f|", r < 1e-10, f"{r:.1e}")
    # 2. batched evaluation equals one-at-a-time evaluation
    wh = initial_field(model, rng, 6, 3.0); W = np.stack([wh, 0.5 * wh, initial_field(model, rng, 6, 2.0)])
    e = max(math.sqrt(sq(model, model.frhs(W)[b] - model.frhs(W[b])) / sq(model, model.frhs(W[b]))) for b in range(3)); check("batched rhs equals single rhs", e < 1e-12, f"{e:.1e}")
    # 3. the central-difference read equals the nonlinear tangent (exact for a quadratic map up to rounding)
    d = initial_field(model, rng, 10, 1.0); eps = 0.7
    cd = (-model.nl_hat(wh + eps * d) + model.nl_hat(wh - eps * d)) / (2 * eps); tg = model.tangent_nl(wh, d)
    e = math.sqrt(sq(model, cd - tg) / sq(model, tg)); check("central difference = tangent_nl", e < 1e-10, f"{e:.1e}")
    # 4. velocity norm by Parseval equals the physical-space L2 norm of the velocity
    u, v = model.velocity(wh); phys = math.sqrt(TWO_PI ** 2 * np.mean(u ** 2 + v ** 2)); e = abs(vel_norm(model, wh) - phys) / phys; check("velocity norm Parseval", e < 1e-12, f"{e:.1e}")
    # 5. Proposition 1: the explicit discarded triad j = (N+1, 1), l = (-N, -1) feeds the observed mode (1, 0)
    N = 4; tri = np.zeros((n, n), complex)
    for (kx, ky) in [(N + 1, 1), (-N, -1)]:
        tri[kx % n, ky % n] = n * n; tri[-kx % n, -ky % n] = n * n
    fed = abs(model.nl_hat(tri)[1, 0]) / n ** 2; check("Proposition 1 triad feeds (1, 0)", fed > 1e-3, f"|coef| {fed:.3f}")
    # 6. Proposition 2 (T1) and Proposition 3 (T2) on a broadband random field
    wb = initial_field(model, rng, 10, 3.0)
    for N in (3.0, 4.0):
        c = theorem_checks(model, wb, cand, N, 64)
        check(f"T1 at N = {N:g} (beyond-2N read / first-octave read)", c["T1_ratio"] is not None and c["T1_ratio"] < 1e-10 and c["first_octave_max_read"] > 0, f"{c['T1_ratio']:.1e} over {c['n_beyond']} pairs")
        check(f"T2 at N = {N:g} (feedback / Proposition 3 bound)", c["T2_ratio"] is not None and c["T2_ratio"] <= 1.0, f"{c['T2_ratio']:.3f}")
    # 7. the nudging term alone (review point 1): with the reference in row 0, nudged_rhs - F = -mu M (W - u) exactly, so the
    # error tendency's nudging contribution is exactly -mu P_S e and the reference row is untouched
    M = np.stack([np.zeros((n, n)), cand.mask(np.arange(0, cand.size, 3), n), cand.mask(np.arange(cand.size), n)]); mu = 37.0
    W = np.stack([wh, initial_field(model, rng, 9, 2.0), initial_field(model, rng, 9, 1.0)])
    diff = nudged_rhs(model, W, M, mu) - model.frhs(W); e = max(math.sqrt(sq(model, diff[b] + mu * M[b] * (W[b] - W[0])) / sq(model, mu * M[b] * (W[b] - W[0]))) for b in (1, 2))
    check("nudging contribution = -mu P_S e", e < 1e-14 and sq(model, diff[0]) == 0.0, f"{e:.1e}, reference row untouched")
    # 8. the finite-gain observer tangent (review point 3) is the derivative of the nudged copy's tendency at v = u, by central
    # difference (exact for the quadratic map); the block tangent is Q DF(u) Q
    d = initial_field(model, rng, 10, 1.0); eps = 0.3; M1 = M[1]
    cd = (nudged_rhs(model, np.stack([wh, wh + eps * d]), M[:2], mu)[1] - nudged_rhs(model, np.stack([wh, wh - eps * d]), M[:2], mu)[1]) / (2 * eps)
    ot = observer_tangent(model, wh, d, M1, mu); e = math.sqrt(sq(model, cd - ot) / sq(model, ot)); check("observer tangent = derivative of the nudged tendency", e < 1e-10, f"{e:.1e}")
    Q = (1.0 - M1) * model.dealias; bt = block_tangent(model, wh, Q * d, Q); e = math.sqrt(sq(model, bt - Q * model.ftangent(wh, Q * d)) / sq(model, bt)); check("block tangent = Q DF Q", e < 1e-14 and sq(model, (1 - Q) * bt) == 0.0, f"{e:.1e}")
    # 9. nothing observed: the nudged copy is exactly the free solver started from zero (an identity of the code, not a
    # property of the dynamics)
    dt = 0.01; g = nudge_group(model, wh, np.zeros((1, n, n)), 50.0, dt, 0.5, 0.1, False, False, rng)
    free = np.zeros((n, n), complex); u_end = wh
    for _ in range(50):
        free = model.fstep(free, dt); u_end = model.fstep(u_end, dt)
    e = abs(g["delta"][-1, 0] - math.sqrt(sq(model, free - u_end) / sq(model, u_end))); check("nothing observed = free solver from zero", e < 1e-10, f"{e:.1e}")
    # 10. the stability guard reports the declared quantities and refuses a step outside RK4's interval
    st = stability(model, wh, 0.01, 50.0); kmax2 = float(model.k2true[model.dealias].max())
    ok = abs(st["linear_stiffness"] - (nu * kmax2 + alpha + 50.0) * 0.01) < 1e-12 and st["ok"] and not stability(model, wh, 0.05, 50.0)["ok"]
    check("stability guard", ok, f"stiffness {st['linear_stiffness']:.3f}, cfl {st['cfl']:.3f}")
    # 11. rankings are permutations, BALL starts on the shell |k| = 1, masks are Hermitian-symmetric
    o = cand.ball_order(); ok = sorted(o.tolist()) == list(range(cand.size)) and np.allclose(cand.kmag[o[:2]], 1.0)
    Mm = cand.mask(o[:7], n); ok = ok and np.array_equal(Mm, Mm[(-np.arange(n)) % n][:, (-np.arange(n)) % n]); check("rankings and masks", ok, f"{cand.size} candidate pairs")
    # 12. the initial field is the same physical field at two resolutions
    m2 = ForcedNS2D(48, nu, alpha, 1.0, 4); f1 = initial_field(model, np.random.default_rng(5), 8, 2.0); f2 = initial_field(m2, np.random.default_rng(5), 8, 2.0)
    e = np.max(np.abs(f1[:9, :9] / 32 ** 2 - f2[:9, :9] / 48 ** 2)); check("initial field resolution-independent", e < 1e-12, f"{e:.1e}")
    # 13. sustained synchronization (review point 5) and m*: a temporary crossing below the threshold is not synchronization
    t = np.linspace(0, 10, 41); hold = 2.5
    cross = np.full(41, 0.5); cross[-1] = 1e-6
    osc = 1e-5 * (1 + 1e3 * (np.arange(41) % 2))
    ok = synced(t, 10.0 ** (-t), 1e-4, hold)[0] and not synced(t, np.full(41, 0.5), 1e-4, hold)[0] and synced(t, np.full(41, 1e-14), 1e-4, hold)[0]
    ok = ok and not synced(t, cross, 1e-4, hold)[0] and not synced(t, osc, 1e-4, hold)[0]
    ok = ok and m_star([4, 8, 16, 32], [False, True, True, True]) == (8, False) and m_star([4, 8, 16, 32], [True, False, True, True]) == (16, True) and m_star([4, 8], [False, False]) == (None, False)
    check("sustained synchronization rule and m*", ok)
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--seed-role", default="probe"); ap.add_argument("--out", default="out.json")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    run(json.load(open(a.config, encoding="utf-8")), a.seed_role, a.out); return 0


if __name__ == "__main__":
    sys.exit(main())
