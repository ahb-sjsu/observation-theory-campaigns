"""D9: the barrier, where any observer-theory estimate meant for regularity must fail (OD track, gate D9).

Model. The viscous dyadic model of Katz and Pavlovic in Cheskidov's form (Trans. Amer. Math. Soc. 360 (2008) 5101-5120,
arXiv:math/0601074v2, eq. 1.1), unforced:

    d/dt u_n + nu lam^(2 alpha n) u_n - lam^n u_(n-1)^2 + lam^(n+1) u_n u_(n+1) = 0,   n >= 1,   u_0 = 0,

truncated by the paper's own Galerkin scheme (eq. 4.2): shells n <= J, the last shell drops its lam^(J+1) u_J u_(J+1)
term, so the nonlinearity conserves energy exactly. Blow-up for alpha < 1/3 from nonnegative data with large H^eps norm
(Theorem 5.3), global regularity for alpha >= 1/2. Norms: |u|_g = (sum_n lam^(2 g n) u_n^2)^(1/2).

Candidates (PREREG-D9-DRAFT Section 3), each a functional Phi(J) over [0, T], classified along the J ladder in a blow-up
world B and a regular world R as BOUNDED / DIVERGING / UNSETTLED per world, and then PASSES THE BARRIER (R bounded, B
diverging) / TRANSPARENT (bounded in both) / FALSE (diverging in R) / UNSETTLED:
  C0  positive control: int_0^T |u|_(1/3+eps)^3 dt (carried as an extra ODE component).
  C1  negative control: sup_t |r_N(t)| / (lam^(N+1) |u(0)|^2), r_N = -lam^(N+1) u_N u_(N+1) e_N the feedback of the
      discarded shells on the observed ones; bounded by 1/2 by the energy inequality in every world (transparent by theorem).
  C2  D8's observers carried to the model: the sustained-synchronization budget (in shells) of a nudged copy for BALL,
      READ (training mean of u_n^2 times the sensitivity |N_u e_n|^2 of the nonlinear tendency), ENSTROPHY (lam^(2n) u_n^2),
      KE (u_n^2), SENS (sensitivity alone) and RANDOM. Recorded, no prediction.
  C3  a harmless-budget candidate: Q(t) the smallest shell above which every shell's local Reynolds number
      lam^n |u_n| / (nu lam^(2 alpha n)) is below c0, Lambda = lam^Q, Phi = int_0^T Lambda^q dt for each declared q.
      Recorded, no exponent claimed.

    python d9_barrier.py --selftest
    python d9_barrier.py --config prereg_config.json --seed-role probe --out probe.json
    python d9_barrier.py --grade results.json --out grade.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------- the model and its truncation

class Dyadic:
    """Galerkin truncation (4.2) of the dyadic model at J shells, n = 1..J stored at index n - 1."""

    def __init__(self, J: int, alpha: float, lam: float = 2.0, nu: float = 1.0):
        self.J = J; self.alpha = alpha; self.lam = lam; self.nu = nu
        n = np.arange(1, J + 1, dtype=float)
        self.n = n; self.ln = lam ** n; self.ln1 = lam ** (n + 1); self.diss = nu * lam ** (2 * alpha * n)

    def nonlinear(self, u):
        """-B(u, u): +lam^n u_(n-1)^2 - lam^(n+1) u_n u_(n+1), with u_0 = 0 and the last shell's outgoing term dropped."""
        um1 = np.concatenate([[0.0], u[:-1]]); up1 = np.concatenate([u[1:], [0.0]])
        return self.ln * um1 ** 2 - self.ln1 * u * up1

    def rhs(self, u):
        return -self.diss * u + self.nonlinear(u)

    def jac(self, u):
        """Analytic Jacobian of rhs (tridiagonal)."""
        J = self.J; Jm = np.diag(-self.diss)
        up1 = np.concatenate([u[1:], [0.0]])
        Jm[np.arange(J), np.arange(J)] += -self.ln1 * up1                      # d/du_n of -lam^(n+1) u_n u_(n+1)
        if J > 1:
            Jm[np.arange(J - 1), np.arange(1, J)] += -self.ln1[:-1] * u[:-1]   # d/du_(n+1) of -lam^(n+1) u_n u_(n+1)
            Jm[np.arange(1, J), np.arange(J - 1)] += 2 * self.ln[1:] * u[:-1]  # d/du_(n-1) of lam^n u_(n-1)^2
        return Jm

    def norm(self, u, g: float):
        return float(np.sqrt(np.sum(self.lam ** (2 * g * self.n) * u ** 2)))

    def sensitivity(self, u):
        """s_n = |N_u e_n|^2, the squared norm of the nonlinear tendency's derivative along shell n (Jacobian columns)."""
        Jn = self.jac(u) + np.diag(self.diss)  # nonlinear part only
        return np.sum(Jn ** 2, axis=0)

    def feedback(self, u, N: int):
        """r_N = P_N F(u) - P_N F(P_N u): the discarded shells' effect on the observed tendency."""
        p = u.copy(); p[N:] = 0.0
        return (self.rhs(u) - self.rhs(p))[:N]


def integrate(model: Dyadic, u0, T: float, n_samples: int, rtol: float, atol: float, eps: float) -> dict:
    """Integrate with Radau. The state is augmented by the dissipation integral 2 nu int |u|_alpha^2 (energy balance) and by
    C0's integral int |u|_(1/3+eps)^3."""
    J = model.J; w = model.lam ** (2 * (1.0 / 3.0 + eps) * model.n)

    def f(t, y):
        u = y[:J]; du = model.rhs(u)
        return np.concatenate([du, [2 * np.sum(model.diss * u ** 2)], [float(np.sum(w * u ** 2)) ** 1.5]])

    def jac(t, y):
        u = y[:J]; Jm = np.zeros((J + 2, J + 2)); Jm[:J, :J] = model.jac(u)
        Jm[J, :J] = 4 * model.diss * u; s = float(np.sum(w * u ** 2)); Jm[J + 1, :J] = 1.5 * math.sqrt(max(s, 0.0)) * 2 * w * u
        return Jm

    y0 = np.concatenate([np.asarray(u0, float), [0.0, 0.0]]); ts = np.linspace(0.0, T, n_samples)
    sol = solve_ivp(f, (0.0, T), y0, method="Radau", jac=jac, rtol=rtol, atol=np.concatenate([np.full(J, atol), [atol, atol]]), t_eval=ts)
    if not sol.success:
        raise RuntimeError(f"Radau failed at J = {J}, alpha = {model.alpha}: {sol.message}")
    U = sol.y[:J].T; E0 = float(np.sum(np.asarray(u0, float) ** 2))
    bal = (np.sum(U ** 2, axis=1) + sol.y[J]) / E0 - 1.0
    return {"t": sol.t, "U": U, "c0_integral": float(sol.y[J + 1, -1]), "energy_balance_max": float(np.max(np.abs(bal))), "nfev": int(sol.nfev)}


# ---------------------------------------------------------------- candidates

def c1_value(model: Dyadic, run: dict, N: int, E0: float) -> float:
    return float(max(np.linalg.norm(model.feedback(u, N)) for u in run["U"]) / (model.lam ** (N + 1) * E0))


def harmless_shell(model: Dyadic, u, c0: float) -> int:
    """Q: the smallest q >= 0 such that every shell p > q has local Reynolds number
    Re_p = lam^p |u_p| / (nu lam^(2 alpha p)) < c0, i.e. its nonlinear turnover rate below c0 times its viscous rate. This
    is the dyadic analogue of Cheskidov and Shvydkoy's condition 2^(-p) |u_p|_inf < c0 nu (their Q(t)). Revised 2026-10-10:
    the first definition compared a shell's nonlinear EXCHANGE with its dissipation, which in the dissipation range are
    nearly equal by the shell's own energy balance, so Q came out as the top shell J in every world and C3 diverged by
    construction (the n <= 10 smoke run on Atlas)."""
    re = model.ln * np.abs(u) / model.diss
    bad = np.nonzero(~(re < c0))[0]
    return int(bad[-1] + 1) if len(bad) else 0  # shells are 1-based: the last shell whose Reynolds number reaches c0


def c3_values(model: Dyadic, run: dict, c0: float, qs: list[float]) -> dict:
    Q = np.array([harmless_shell(model, u, c0) for u in run["U"]], float); Lam = model.lam ** Q
    return {str(q): float(np.trapezoid(Lam ** q, run["t"])) for q in qs} | {"Q_max": int(Q.max())}


def nudge(model: Dyadic, u0, mask: np.ndarray, mu: float, T: float, n_samples: int, rtol: float, atol: float) -> dict:
    J = model.J

    def f(t, y):
        u, v = y[:J], y[J:]
        return np.concatenate([model.rhs(u), model.rhs(v) - mu * mask * (v - u)])

    def jac(t, y):
        u, v = y[:J], y[J:]; Jm = np.zeros((2 * J, 2 * J)); Jm[:J, :J] = model.jac(u)
        Jm[J:, J:] = model.jac(v) - mu * np.diag(mask); Jm[J:, :J] = mu * np.diag(mask)
        return Jm

    ts = np.linspace(0.0, T, n_samples)
    sol = solve_ivp(f, (0.0, T), np.concatenate([np.asarray(u0, float), np.zeros(J)]), method="Radau", jac=jac, rtol=rtol, atol=atol, t_eval=ts)
    if not sol.success:
        raise RuntimeError(f"nudged Radau failed: {sol.message}")
    U, V = sol.y[:J].T, sol.y[J:].T
    return {"t": sol.t, "delta": np.linalg.norm(V - U, axis=1) / np.maximum(np.linalg.norm(U, axis=1), 1e-300)}


def sustained(t, d, thr: float, hold: float) -> bool:
    return bool(np.all(d[t >= t[-1] - hold - 1e-12] <= thr))


def c2_values(model: Dyadic, run: dict, cfg: dict, rng: np.random.Generator) -> dict:
    """Synchronization budget m* (in shells) per observer, from the reference run's own initial data, v(0) = 0."""
    U = run["U"]; J = model.J
    amp = np.mean(U ** 2, axis=0); sens = np.mean([model.sensitivity(u) for u in U], axis=0)
    read = np.mean([u ** 2 * model.sensitivity(u) for u in U], axis=0)
    orders = {"BALL": np.arange(J), "READ": np.argsort(-read, kind="stable"), "ENSTROPHY": np.argsort(-amp * model.lam ** (2 * model.n), kind="stable"),
              "KE": np.argsort(-amp, kind="stable"), "SENS": np.argsort(-sens, kind="stable")}
    for j in range(int(cfg["random_draws"])):
        orders[f"RANDOM{j}"] = rng.permutation(J)
    out = {}
    for name, o in orders.items():
        flags = []
        for m in range(1, J + 1):
            mask = np.zeros(J); mask[o[:m]] = 1.0
            g = nudge(model, U[0], mask, float(cfg["mu"]), float(cfg["T_sync"]), int(cfg["n_samples_sync"]), float(cfg["rtol"]), float(cfg["atol_sync"]))
            flags.append(sustained(g["t"], g["delta"], float(cfg["sync_threshold"]), float(cfg["T_hold"])))
        ms = None
        for m in range(J, 0, -1):
            if not flags[m - 1]: break
            ms = m
        out[name] = {"m_star": ms, "censored": ms is None, "order": [int(i) + 1 for i in o]}
    return out


# ---------------------------------------------------------------- classification

def classify_world(values: list[float], shrink: float, tol: float, D: float) -> str:
    """BOUNDED when every increment along the J ladder is at most `shrink` times the previous one (or below tol relative
    to the value) and the last increment is at most tol relative; DIVERGING when the top value is at least D times the
    bottom and the last increment is no smaller than `shrink` times the first; otherwise UNSETTLED."""
    v = np.asarray(values, float)
    if len(v) < 3 or not np.all(np.isfinite(v)): return "UNSETTLED"
    d = np.abs(np.diff(v)); scale = np.maximum(np.abs(v[1:]), 1e-300)
    small = d <= tol * scale
    shrinking = all(small[i + 1] or d[i + 1] <= shrink * d[i] for i in range(len(d) - 1))
    if shrinking and small[-1]: return "BOUNDED"
    if abs(v[-1]) >= D * max(abs(v[0]), 1e-300) and d[-1] >= shrink * d[0] and not small[-1]: return "DIVERGING"
    return "UNSETTLED"


def classify(r: str, b: str) -> str:
    if r == "DIVERGING": return "FALSE"
    if r == "BOUNDED" and b == "DIVERGING": return "PASSES THE BARRIER"
    if r == "BOUNDED" and b == "BOUNDED": return "TRANSPARENT"
    return "UNSETTLED"


# ---------------------------------------------------------------- run and grade

def run_world(world: dict, cfg: dict, seed: int, log=print) -> dict:
    out = {"name": world["name"], "alpha": world["alpha"], "amplitude": float(world.get("amplitude", cfg["amplitude"])), "graded": world.get("graded", True), "ladder": {}}
    for J in cfg["J_ladder"]:
        t0 = time.time(); model = Dyadic(int(J), float(world["alpha"]), float(cfg["lam"]), float(cfg["nu"]))
        u0 = np.zeros(int(J)); u0[0] = float(world.get("amplitude", cfg["amplitude"])); E0 = float(np.sum(u0 ** 2)); rec = {}
        for tag, scale in (("base", 1.0), ("half_tol", 0.5)):
            run = integrate(model, u0, float(cfg["T"]), int(cfg["n_samples"]), scale * float(cfg["rtol"]), scale * float(cfg["atol"]), float(cfg["eps"]))
            r = {"C0": run["c0_integral"], "C1": c1_value(model, run, int(cfg["N_observer"]), E0), "C3": c3_values(model, run, float(cfg["c0"]), [float(q) for q in cfg["qs"]]),
                 "energy_balance_max": run["energy_balance_max"], "nfev": run["nfev"],
                 "norm_peak_time": float(run["t"][int(np.argmax([model.norm(u, 1.0 / 3.0 + float(cfg["eps"])) for u in run["U"]]))])}
            if tag == "base" and cfg.get("c2", True):
                r["C2"] = c2_values(model, run, cfg, np.random.default_rng(seed + int(J)))
            rec[tag] = r
        rec["seconds"] = time.time() - t0; out["ladder"][str(J)] = rec
        log(json.dumps({"world": world["name"], "J": J, "C0": rec["base"]["C0"], "C1": rec["base"]["C1"], "C3_Qmax": rec["base"]["C3"]["Q_max"], "balance": rec["base"]["energy_balance_max"],
                        "C2": {k: v["m_star"] for k, v in rec["base"].get("C2", {}).items() if not k.startswith("RANDOM")}, "seconds": round(rec["seconds"], 1)}))
    return out


def run(cfg: dict, seed_role: str, out_path: str, only_world: str | None = None) -> dict:
    seed = int(cfg[f"seed_{seed_role}"]); res = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    groups = cfg["groups_by_role"][seed_role]
    for w in cfg["worlds"]:
        if w.get("group") not in groups or (only_world and w["name"] != only_world): continue
        res["worlds"].append(run_world(w, cfg, seed)); json.dump(res, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    res["finished"] = time.strftime("%Y-%m-%d %H:%M:%S"); json.dump(res, open(out_path, "w", encoding="utf-8"), indent=1, default=float)
    return res


def series(world: dict, key: str, sub: str | None = None) -> list[float]:
    vals = []
    for J in sorted(world["ladder"], key=int):
        v = world["ladder"][J]["base"][key]
        vals.append(float(v[sub]["m_star"] or (int(J) + 1)) if key == "C2" else float(v[sub] if sub else v))
    return vals


def grade(res: dict) -> dict:
    cfg = res["config"]; shrink, tol, D = float(cfg["shrink"]), float(cfg["tol"]), float(cfg["D"])
    W = {w["name"]: w for w in res["worlds"]}; R, B = W[cfg["world_R"]], W[cfg["world_B"]]
    out = {"bars": {}, "classes": {}, "gate": None}

    def cls(key, sub=None):
        r = classify_world(series(R, key, sub), shrink, tol, D); b = classify_world(series(B, key, sub), shrink, tol, D)
        return {"R": r, "B": b, "class": classify(r, b), "R_series": series(R, key, sub), "B_series": series(B, key, sub)}

    c0 = cls("C0"); c1 = cls("C1"); out["classes"]["C0"] = c0; out["classes"]["C1"] = c1
    for q in cfg["qs"]:
        out["classes"][f"C3_q{q}"] = cls("C3", str(float(q)))
    for name in ("BALL", "READ", "ENSTROPHY", "KE", "SENS"):
        if "C2" in R["ladder"][str(cfg["J_ladder"][0])]["base"]:
            out["classes"][f"C2_{name}"] = cls("C2", name)
    # I2: numerics, every graded Phi stable under halved tolerances, energy balance closed
    worst = 0.0; bal = 0.0
    for w in (R, B):
        for J, rec in w["ladder"].items():
            for k in ("C0", "C1"):
                a, b = rec["base"][k], rec["half_tol"][k]; worst = max(worst, abs(a - b) / max(abs(a), 1e-300))
            bal = max(bal, rec["base"]["energy_balance_max"], rec["half_tol"]["energy_balance_max"])
    i1 = c0["class"] == "PASSES THE BARRIER"; i2 = worst <= float(cfg["tol_numerics"]) and bal <= float(cfg["tol_energy"]); n1 = c1["class"] == "TRANSPARENT"
    out["bars"] = {"I1_positive_control_passes": i1, "I2_numerics": {"worst_relative_change_half_tol": worst, "energy_balance_worst": bal, "holds": i2}, "N1_negative_control_transparent": n1}
    if not (i1 and i2):
        out["gate"] = "INDETERMINATE (" + ("I1: the ladder does not see the known blow-up" if not i1 else "I2: numerics") + ")"
    elif not n1:
        out["gate"] = "FAIL (the negative control is not transparent on a numerically sound run: a theorem of the model is contradicted, so the code or the derivation is wrong)"
    else:
        out["gate"] = "PASS (instrument and both controls behave; the C2 and C3 classes are the result)"
    if res.get("seed_role") != "run": out["gate"] = f"{res.get('seed_role', '?').upper()} GRADE, NOT A VERDICT: " + out["gate"]
    return out


# ---------------------------------------------------------------- self-test

def selftest() -> int:
    fails = 0; rng = np.random.default_rng(0)

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    for alpha in (0.25, 0.6):
        m = Dyadic(12, alpha)
        # 1. energy cancellation of the truncated nonlinearity, sum_n u_n (B(u, u))_n = 0
        e = max(abs(float(np.dot(u, m.nonlinear(u)))) / float(np.sum(m.ln1 * np.abs(u) ** 3)) for u in rng.normal(size=(20, 12)))
        check(f"energy cancellation of the truncation (alpha = {alpha})", e < 1e-13, f"{e:.1e}")
        # 2. analytic Jacobian = central finite difference
        u = np.abs(rng.normal(size=12)) * 0.01; h = 1e-7
        fd = np.stack([(m.rhs(u + h * np.eye(12)[k]) - m.rhs(u - h * np.eye(12)[k])) / (2 * h) for k in range(12)], axis=1)
        e = float(np.max(np.abs(fd - m.jac(u))) / np.max(np.abs(m.jac(u)))); check(f"analytic Jacobian (alpha = {alpha})", e < 1e-6, f"{e:.1e}")
        # 3. the C1 identity r_N = -lam^(N+1) u_N u_(N+1) e_N
        u = rng.normal(size=12); N = 5; r = m.feedback(u, N); ex = np.zeros(N); ex[N - 1] = -m.lam ** (N + 1) * u[N - 1] * u[N]
        check(f"C1 identity r_N = -lam^(N+1) u_N u_(N+1) e_N (alpha = {alpha})", np.allclose(r, ex, rtol=1e-12, atol=1e-12 * np.max(np.abs(ex))), f"{np.max(np.abs(r - ex)):.1e}")
    # 4. energy conserved by the truncation at nu = 0
    m0 = Dyadic(10, 0.3, nu=0.0); u0 = np.zeros(10); u0[0] = 1.0
    run = integrate(m0, u0, 2.0, 41, 1e-11, 1e-14, 0.05); e = float(np.max(np.abs(np.sum(run["U"] ** 2, axis=1) - 1.0)))
    check("energy conserved at nu = 0", e < 1e-8, f"{e:.1e}")
    # 5. energy balance closes with dissipation, nonnegativity preserved from nonnegative data (Theorem 4.2)
    m1 = Dyadic(14, 0.25); u0 = np.zeros(14); u0[0] = 20.0
    run = integrate(m1, u0, 1.0, 201, 1e-10, 1e-14, 0.05)
    check("energy balance closes (E + 2 nu int |u|_alpha^2 = E0)", run["energy_balance_max"] < 1e-6, f"{run['energy_balance_max']:.1e}")
    check("nonnegativity preserved", float(run["U"].min()) > -1e-10, f"min u {float(run['U'].min()):.1e}")
    # 6. C1 bounded by 1/2 by the energy inequality on that run
    c1 = c1_value(m1, run, 6, 400.0); check("C1 <= 1/2 (energy inequality)", c1 <= 0.5 + 1e-9, f"{c1:.3e}")
    # 7. nudging: nothing observed is the free solver from zero (F(0) = 0, so that copy stays at zero and delta = 1:
    # a check of the nudging plumbing, not of the dynamics); everything observed synchronizes
    m2 = Dyadic(10, 0.6); u0 = np.zeros(10); u0[0] = 2.0
    g = nudge(m2, u0, np.zeros(10), 50.0, 1.0, 11, 1e-10, 1e-14)
    free = solve_ivp(lambda t, y: m2.rhs(y), (0, 1.0), np.zeros(10), method="Radau", jac=lambda t, y: m2.jac(y), rtol=1e-10, atol=1e-14, t_eval=np.linspace(0, 1.0, 11))
    ref = integrate(m2, u0, 1.0, 11, 1e-10, 1e-14, 0.05)
    d_free = np.linalg.norm(free.y.T - ref["U"], axis=1) / np.linalg.norm(ref["U"], axis=1)
    check("nothing observed = free solver from zero", float(np.max(np.abs(d_free - g["delta"]))) < 1e-6, f"{float(np.max(np.abs(d_free - g['delta']))):.1e}")
    g = nudge(m2, u0, np.ones(10), 50.0, 2.0, 21, 1e-10, 1e-14); check("everything observed synchronizes", sustained(g["t"], g["delta"], 1e-4, 0.5), f"delta end {g['delta'][-1]:.1e}")
    # 8. the harmless shell: zero field has Q = 0; a field with energy only at the top shell and large amplitude has Q = J
    m3 = Dyadic(8, 0.25); check("harmless shell of the zero field", harmless_shell(m3, np.zeros(8), 1.0) == 0)
    # a strong field in shell 7 alone: shell 7's Reynolds number is huge and shell 8's is zero, so Q = 7 (under the first,
    # exchange-based definition the inflow into the empty shell 8 failed instead and Q was 8)
    u = np.zeros(8); u[6] = 1e6; check("harmless shell of a strong field in shell 7", harmless_shell(m3, u, 1.0) == 7)
    # a field whose top shells are all viscous: Re_n < 1 above shell 3, so Q = 3
    u = np.zeros(8); u[:3] = 50.0; u[3:] = 1e-12; check("harmless shell where the top is viscous", harmless_shell(m3, u, 1.0) == 3, f"Q = {harmless_shell(m3, u, 1.0)}")
    # 9. the classification rule on constructed sequences
    conv = [1.0 - 0.5 ** k for k in range(1, 6)]; growth = [2.0 ** k for k in range(1, 6)]; slow = [1.0, 1.1, 1.2, 1.3, 1.4]
    ok = classify_world(conv, 0.8, 0.1, 4.0) == "BOUNDED" and classify_world(growth, 0.8, 0.01, 4.0) == "DIVERGING" and classify_world(slow, 0.8, 0.01, 4.0) == "UNSETTLED"
    ok = ok and classify("BOUNDED", "DIVERGING") == "PASSES THE BARRIER" and classify("BOUNDED", "BOUNDED") == "TRANSPARENT" and classify("DIVERGING", "BOUNDED") == "FALSE" and classify("UNSETTLED", "DIVERGING") == "UNSETTLED"
    check("classification rule", ok)
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--seed-role", default="probe")
    ap.add_argument("--out", default="out.json"); ap.add_argument("--grade", default=None)
    ap.add_argument("--world", default=None, help="run only this world (one NRP Job per world)")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    if a.grade:
        g = grade(json.load(open(a.grade, encoding="utf-8"))); text = json.dumps(g, indent=1, default=float)
        open(a.out, "w", encoding="utf-8").write(text + "\n"); print(text); return 0
    res = run(json.load(open(a.config, encoding="utf-8")), a.seed_role, a.out, a.world)
    if a.world and not res["worlds"]: raise SystemExit(f"no world named {a.world} in role {a.seed_role}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
