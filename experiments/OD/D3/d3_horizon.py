"""D3: the observational predictability horizon (OD track, gate D3).

Article `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`,
Section 6. An observer O = (C, G, B) measures a tangent perturbation delta(t), carried by the
linearised flow, in its own length d_C(delta) = sqrt(delta^T P_C delta). The observational
Lyapunov exponent over a window is (1/T) log(d_C(T) / d_C(0)), the classical one is
(1/T) log(|delta(T)| / |delta(0)|), and the horizon T_O(B) is the first time d_C exceeds B.

Proposition 1 and what this gate measures of it:
(E) positive definite observer, P with eigenvalues in [a, b]: the two window exponents differ by
    at most log(b / a) / (2 T), exactly, so they agree in the limit;
(K) an observer with a kernel: smaller than the classical exponent when the perturbation's
    Euclidean growth is carried by kernel components growing faster than its read components
    (World K, a decoupled unstable direction the observer does not read), equal when the read
    components grow faster (World K control), transiently larger for a perturbation started in a
    kernel that the flow does not preserve (Lorenz-63 read through one coordinate), and equal in
    the limit for a generic perturbation under such an observer;
(H) the horizon: non-decreasing in B, bracketed for a positive definite observer between the
    Euclidean horizons at B / sqrt(b) and B / sqrt(a), never earlier than the Euclidean horizon
    for a projection, and observer-dependent at fixed B where the flow has no symmetry relating
    the observers (Lorenz-63, x against z) and not where it has (Lorenz-96, one block of sites
    against the next).

Every observer here has a constant read operator P (a diagonal matrix), so one tangent
integration per (start, direction) serves every observer.

    python d3_horizon.py --selftest
    python d3_horizon.py --config prereg_config.json --seed-role probe|pilot|run --out FILE
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np

# ----------------------------------------------------------------------------- flows


def lorenz63(x, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    return np.array([sigma * (x[1] - x[0]), x[0] * (rho - x[2]) - x[1], x[0] * x[1] - beta * x[2]])


def lorenz63_jac(x, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    return np.array([[-sigma, sigma, 0.0], [rho - x[2], -1.0, -x[0]], [x[1], x[0], -beta]])


def lorenz96(x, F=8.0):
    return (np.roll(x, -1) - np.roll(x, 2)) * np.roll(x, 1) - x + F


def lorenz96_jac(x, F=8.0):
    n = len(x); J = -np.eye(n)
    for i in range(n):
        J[i, (i + 1) % n] += x[(i - 1) % n]
        J[i, (i - 2) % n] -= x[(i - 1) % n]
        J[i, (i - 1) % n] += x[(i + 1) % n] - x[(i - 2) % n]
    return J


class Flow:
    """A flow with a Jacobian, optionally extended by a decoupled linear direction u' = mu u
    (World K), which the observer does not read."""

    def __init__(self, kind: str, n: int = 3, F: float = 8.0, mu: float | None = None):
        self.kind = kind; self.n_core = n if kind == "lorenz96" else 3; self.F = F; self.mu = mu
        self.n = self.n_core + (1 if mu is not None else 0)

    def f(self, x):
        core = lorenz63(x[: self.n_core]) if self.kind == "lorenz63" else lorenz96(x[: self.n_core], self.F)
        return core if self.mu is None else np.concatenate([core, [self.mu * x[-1]]])

    def jac(self, x):
        J = lorenz63_jac(x[: self.n_core]) if self.kind == "lorenz63" else lorenz96_jac(x[: self.n_core], self.F)
        if self.mu is None:
            return J
        Jf = np.zeros((self.n, self.n)); Jf[: self.n_core, : self.n_core] = J; Jf[-1, -1] = self.mu
        return Jf


def rk4_state(flow: Flow, x, dt, steps):
    for _ in range(steps):
        k1 = flow.f(x); k2 = flow.f(x + 0.5 * dt * k1); k3 = flow.f(x + 0.5 * dt * k2); k4 = flow.f(x + dt * k3)
        x = x + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x


def rk4_tangent(flow: Flow, x, D, dt, steps, record_every, record_fn):
    """Integrates the state x and a matrix D of tangent vectors (columns) with one RK4 scheme on
    the augmented system; calls record_fn(step_index, x, D) every record_every steps, including
    at step 0."""
    def rhs(x, D):
        return flow.f(x), flow.jac(x) @ D
    record_fn(0, x, D)
    for s in range(1, steps + 1):
        k1x, k1D = rhs(x, D)
        k2x, k2D = rhs(x + 0.5 * dt * k1x, D + 0.5 * dt * k1D)
        k3x, k3D = rhs(x + 0.5 * dt * k2x, D + 0.5 * dt * k2D)
        k4x, k4D = rhs(x + dt * k3x, D + dt * k3D)
        x = x + dt / 6.0 * (k1x + 2 * k2x + 2 * k3x + k4x)
        D = D + dt / 6.0 * (k1D + 2 * k2D + 2 * k3D + k4D)
        if s % record_every == 0:
            record_fn(s, x, D)
    return x, D


# ----------------------------------------------------------------------------- observers and measures


def observer_P(spec: dict, n: int) -> np.ndarray:
    kind = spec["kind"]
    if kind == "full":
        return np.ones(n)
    if kind == "diag":
        d = np.array(spec["diag"], dtype=float); assert len(d) == n; return d
    if kind == "coords":
        p = np.zeros(n); p[list(spec["coords"])] = 1.0; return p
    if kind == "alternating":
        p = np.array([spec["values"][i % len(spec["values"])] for i in range(n)], dtype=float); return p
    raise ValueError(kind)


def unit(v):
    return v / np.linalg.norm(v)


def direction(spec: dict, n: int, rng: np.random.Generator, n_core: int) -> np.ndarray:
    kind = spec["kind"]
    if kind == "random":
        return unit(rng.normal(size=n))
    if kind == "kernel_of":
        p = spec["_P"]; v = rng.normal(size=n); v[p > 0] = 0.0; return unit(v)
    if kind == "core_plus_extra":
        # World K: the read (core) part of size sqrt(1 - w^2), the unread extra direction of size w
        w = float(spec["extra_weight"]); v = np.zeros(n); v[:n_core] = unit(rng.normal(size=n_core)) * np.sqrt(1 - w * w); v[-1] = w; return v
    raise ValueError(kind)


def window_exponent(lengths: np.ndarray, times: np.ndarray, t0: float, T: float) -> float:
    i0 = int(np.argmin(np.abs(times - t0))); i1 = int(np.argmin(np.abs(times - T)))
    if lengths[i0] <= 0.0:
        return float("nan")
    return float(np.log(lengths[i1] / lengths[i0]) / (times[i1] - times[i0]))


def horizon(lengths: np.ndarray, times: np.ndarray, B: float) -> float:
    idx = np.nonzero(lengths > B)[0]
    return float(times[idx[0]]) if len(idx) else float("inf")


# ----------------------------------------------------------------------------- one world


def run_world(world: dict, cfg: dict, rng: np.random.Generator, log=print) -> dict:
    flow = Flow(world["flow"], n=world.get("n", 3), F=world.get("F", 8.0), mu=world.get("mu"))
    n = flow.n; dt = float(world["dt"]); T_max = float(cfg["T_max"]); rec_every = int(round(float(cfg["record_dt"]) / dt))
    steps = int(round(T_max / dt)); times = np.arange(0, steps + 1, rec_every) * dt
    T_ladder = [float(t) for t in cfg["T_ladder"]]; B_ladder = [float(b) for b in cfg["B_ladder"]]; t0 = float(cfg["kernel_start_t0"])
    observers = {name: observer_P(spec, n) for name, spec in world["observers"].items()}
    dirs = world["directions"]
    # starts on the attractor: one long trajectory, spin-up then samples at a spacing
    x = np.array(world["x0"], dtype=float) + 0.01 * rng.normal(size=n)
    if flow.mu is not None:
        x[-1] = 0.0
    x = rk4_state(flow, x, dt, int(round(float(world["spinup"]) / dt)))
    starts = []
    for _ in range(int(world["n_starts"])):
        x = rk4_state(flow, x, dt, int(round(float(world["start_spacing"]) / dt)))
        xs = x.copy()
        if flow.mu is not None:
            xs[-1] = 1.0  # the decoupled direction's state, irrelevant to the linearisation (u' = mu u is linear)
        starts.append(xs)
    rows = []; t_start = time.time()
    for si, xs in enumerate(starts):
        cols = []; names = []
        for dname, dspec in dirs.items():
            spec = dict(dspec)
            if spec["kind"] == "kernel_of":
                spec["_P"] = observers[spec["observer"]]
            cols.append(direction(spec, n, rng, flow.n_core)); names.append(dname)
        D0 = np.stack(cols, axis=1)
        lengths = {"__euclid__": [], "__core__": []}; lengths.update({o: [] for o in observers})  # internal keys are distinct from any observer name
        def record(s, x, D):
            lengths["__euclid__"].append(np.linalg.norm(D, axis=0))
            lengths["__core__"].append(np.linalg.norm(D[: flow.n_core], axis=0))
            for o, p in observers.items():
                lengths[o].append(np.sqrt(np.einsum("ij,i,ij->j", D, p, D)))
        rk4_tangent(flow, xs, D0, dt, steps, rec_every, record)
        L = {k: np.array(v) for k, v in lengths.items()}  # (n_times, n_dirs)
        for di, dname in enumerate(names):
            kernel_start = dirs[dname]["kind"] == "kernel_of"
            tt0 = t0 if kernel_start else 0.0
            row = {"start": si, "direction": dname, "kernel_start": kernel_start, "t0": tt0,
                   "classical": {str(T): window_exponent(L["__euclid__"][:, di], times, tt0, T) for T in T_ladder},
                   "core_part": {str(T): window_exponent(L["__core__"][:, di], times, tt0, T) for T in T_ladder},
                   "observers": {}}
            for o in observers:
                row["observers"][o] = {"d0": float(L[o][0, di]),
                                       "exponent": {str(T): window_exponent(L[o][:, di], times, tt0, T) for T in T_ladder},
                                       "horizon": {str(B): horizon(L[o][:, di], times, B) for B in B_ladder}}
            row["euclid_horizon"] = {str(B): horizon(L["__euclid__"][:, di], times, B) for B in B_ladder}
            # the positive definite bracket needs the Euclidean horizon at scaled budgets
            row["euclid_horizon_scaled"] = {}
            for o, p in observers.items():
                if (p > 0).all():
                    a, b = float(p.min()), float(p.max())
                    row["euclid_horizon_scaled"][o] = {str(B): [horizon(L["__euclid__"][:, di], times, B / np.sqrt(b)), horizon(L["__euclid__"][:, di], times, B / np.sqrt(a))] for B in B_ladder}
            rows.append(row)
        if (si + 1) % 16 == 0:
            log(json.dumps({"world": world["name"], "starts_done": si + 1, "seconds": round(time.time() - t_start, 1)}))
    return {"name": world["name"], "n": n, "n_core": flow.n_core, "mu": flow.mu, "dt": dt, "times_recorded": len(times),
            "observers": {o: [float(v) for v in p] if n <= 8 else {"kind": world["observers"][o]["kind"], "min": float(p.min()), "max": float(p.max())} for o, p in observers.items()},
            "rows": rows, "seconds": time.time() - t_start}


def run(cfg: dict, seed_role: str, out_path: str) -> dict:
    seed = int(cfg[f"seed_{seed_role}"]); rng = np.random.default_rng(seed)
    result = {"config": cfg, "seed_role": seed_role, "seed": seed, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worlds": []}
    for world in cfg["worlds"]:
        if seed_role == "probe" and not world.get("in_probe", True):
            continue
        result["worlds"].append(run_world(world, cfg, rng))
        json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
        print(json.dumps({"world": world["name"], "rows": len(result["worlds"][-1]["rows"]), "seconds": round(result["worlds"][-1]["seconds"], 1)}))
    result["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    json.dump(result, open(out_path, "w", encoding="utf-8"), indent=1)
    return result


# ----------------------------------------------------------------------------- self test


def selftest() -> int:
    """A linear flow x' = A x with A = diag(1, 0, -1), whose exponents are known: the estimator
    must recover them, the positive definite bound must hold with equality structure, and the
    kernel cases must come out as the proposition says."""
    fails = 0

    class Lin(Flow):
        def __init__(self):
            self.kind = "linear"; self.n_core = 3; self.n = 3; self.mu = None; self.A = np.diag([1.0, 0.0, -1.0])
        def f(self, x):
            return self.A @ x
        def jac(self, x):
            return self.A

    flow = Lin(); dt = 0.001; T = 5.0; steps = int(T / dt); rec = 10; times = np.arange(0, steps + 1, rec) * dt
    D0 = np.stack([unit(np.array([1.0, 1.0, 1.0])), np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0])], axis=1)
    P_aniso = np.array([4.0, 1.0, 0.25]); P_third = np.array([0.0, 0.0, 1.0]); P_first = np.array([1.0, 0.0, 0.0])
    Ls = {"e": [], "an": [], "third": [], "first": []}
    def record(s, x, D):
        Ls["e"].append(np.linalg.norm(D, axis=0))
        for k, p in (("an", P_aniso), ("third", P_third), ("first", P_first)):
            Ls[k].append(np.sqrt(np.einsum("ij,i,ij->j", D, p, D)))
    rk4_tangent(flow, np.zeros(3), D0, dt, steps, rec, record)
    L = {k: np.array(v) for k, v in Ls.items()}
    # generic direction: classical exponent -> 1 (dominated by the unstable coordinate)
    lc = window_exponent(L["e"][:, 0], times, 0.0, T); la = window_exponent(L["an"][:, 0], times, 0.0, T)
    bound = np.log(4.0 / 0.25) / (2 * T)
    print(f"generic: classical {lc:.4f} (limit 1), anisotropic {la:.4f}, |diff| {abs(lc - la):.4f} <= bound {bound:.4f}")
    if abs(lc - 1.0) > 0.2 or abs(lc - la) > bound + 1e-9:
        print("FAIL positive definite bound or estimator"); fails += 1
    # direction e_3 under the observer reading only x_3: observational exponent -1 (smaller); classical -1 too
    lt = window_exponent(L["third"][:, 1], times, 0.0, T); lc3 = window_exponent(L["e"][:, 1], times, 0.0, T)
    print(f"e_3 read by x_3: observational {lt:.4f} classical {lc3:.4f} (both -1)")
    if abs(lt + 1.0) > 1e-3 or abs(lc3 + 1.0) > 1e-3:
        print("FAIL decaying direction"); fails += 1
    # generic direction read only through x_3: smaller than classical (kernel growth dominates)
    lt_g = window_exponent(L["third"][:, 0], times, 0.0, T)
    print(f"generic read by x_3: observational {lt_g:.4f} (-1) against classical {lc:.4f} (1): smaller")
    if not (lt_g < lc - 1.5):
        print("FAIL smaller-than-classical case"); fails += 1
    # generic direction read through x_1: equal to classical in the limit (both -> 1)
    lf = window_exponent(L["first"][:, 0], times, 0.0, T)
    print(f"generic read by x_1: observational {lf:.4f} against classical {lc:.4f}")
    if abs(lf - 1.0) > 1e-6:
        print("FAIL read component exact"); fails += 1
    # horizons: monotone in B, bracket for the anisotropic observer, projection never earlier
    for B in (2.0, 10.0, 50.0):
        hE = horizon(L["e"][:, 0], times, B); hA = horizon(L["an"][:, 0], times, B); hF = horizon(L["first"][:, 0], times, B)
        lo = horizon(L["e"][:, 0], times, B / 2.0); hi = horizon(L["e"][:, 0], times, B / 0.5)
        ok = (lo <= hA <= hi) and (hF >= hE)
        print(f"B={B}: euclid {hE:.3f} aniso {hA:.3f} in [{lo:.3f}, {hi:.3f}] projection {hF:.3f} >= {hE:.3f} {'ok' if ok else 'FAIL'}")
        fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--config"); ap.add_argument("--seed-role", default="pilot"); ap.add_argument("--out", default="out.json")
    a = ap.parse_args(argv)
    if a.selftest:
        return 1 if selftest() else 0
    cfg = json.load(open(a.config, encoding="utf-8"))
    run(cfg, a.seed_role, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
