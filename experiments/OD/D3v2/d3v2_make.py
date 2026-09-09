"""Builds d3v2_horizon.py from d3_horizon.py: general (matrix) read operators including rank-one
projections along declared unit vectors, and an independent long-trajectory estimate of the
leading Lyapunov exponent and of the mean log read-fraction of the leading Lyapunov vector under
each observer, which the horizon offset law of D3v2 predicts from."""
import os

SP = r"C:\Users\abptl\AppData\Local\Temp\claude\C--source\f9dd774c-068a-466c-aa48-fbb6bdd82c75\scratchpad"
s = open(os.path.join(SP, "d3_horizon.py"), encoding="utf-8").read().replace("\r\n", "\n")


def sub(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:60])
    s = s.replace(a, b)


sub('"""D3: the observational predictability horizon (OD track, gate D3).', '''"""D3v2: the horizon offset law (OD track, gate D3v2), built on the D3 workload.

D3 found that the horizon T_O(B) of an observer O reading a perturbation is later than the full
reader's on the same perturbation, by an amount whose paired significance faded along the budget
ladder. D3v2 registers the law behind it. Once the perturbation has aligned with the leading
Lyapunov vector v_1(x(t)), the observer's length is d_O = |delta| f_O(x(t)) with the read fraction
f_O(x) = sqrt(v_1^T P_O v_1), so the horizons of O and of the full reader (f = 1) differ by
T_O(B) - T_full(B) ~= -log f_O / lambda, evaluated where the budget is crossed. Averaged over
starts on the attractor the offset should therefore converge, as B grows, to
    Delta_O = -E[log f_O(x)] / lambda_1,
with the expectation over the invariant measure and lambda_1 the leading exponent, both measured
on one independent long trajectory (Benettin renormalisation) and not on the horizon runs.

Original D3 header follows.
''')

# matrix read operators
sub('''def observer_P(spec: dict, n: int) -> np.ndarray:
    kind = spec["kind"]
    if kind == "full":
        return np.ones(n)
    if kind == "diag":
        d = np.array(spec["diag"], dtype=float); assert len(d) == n; return d
    if kind == "coords":
        p = np.zeros(n); p[list(spec["coords"])] = 1.0; return p
    if kind == "alternating":
        p = np.array([spec["values"][i % len(spec["values"])] for i in range(n)], dtype=float); return p
    raise ValueError(kind)''', '''def observer_P(spec: dict, n: int) -> np.ndarray:
    """The read operator as an n x n matrix."""
    kind = spec["kind"]
    if kind == "full":
        return np.eye(n)
    if kind == "diag":
        d = np.array(spec["diag"], dtype=float); assert len(d) == n; return np.diag(d)
    if kind == "coords":
        p = np.zeros(n); p[list(spec["coords"])] = 1.0; return np.diag(p)
    if kind == "alternating":
        return np.diag(np.array([spec["values"][i % len(spec["values"])] for i in range(n)], dtype=float))
    if kind == "rank1":
        u = np.zeros(n); v = np.array(spec["vector"], dtype=float); u[: len(v)] = v / np.linalg.norm(v); return np.outer(u, u)
    raise ValueError(kind)


def obs_lengths(D: np.ndarray, P: np.ndarray) -> np.ndarray:
    """Observational lengths of the columns of D under P."""
    return np.sqrt(np.maximum(np.einsum("ij,ik,kj->j", D, P, D), 0.0))


def pd_bounds(P: np.ndarray) -> tuple[bool, float, float]:
    lam = np.linalg.eigvalsh(0.5 * (P + P.T))
    return bool(lam.min() > 1e-12), float(lam.min()), float(lam.max())


def clv_stats(flow, x0: np.ndarray, dt: float, T_long: float, T_transient: float, observers: dict, renorm_every: float = 0.5) -> dict:
    """One long trajectory with one tangent vector renormalised every renorm_every time units:
    the leading Lyapunov exponent from the accumulated log growth after the transient, and for
    each observer the mean and standard deviation of log f_O over the renormalisation points,
    f_O = sqrt(v^T P v) for the unit tangent vector v (the leading Lyapunov vector once aligned)."""
    x = x0.copy(); v = np.ones(flow.n) / np.sqrt(flow.n)
    steps_block = int(round(renorm_every / dt)); n_blocks = int(round(T_long / renorm_every)); n_skip = int(round(T_transient / renorm_every))
    logs = {o: [] for o in observers}; growth = 0.0; kept = 0
    for b in range(n_blocks):
        x, D = rk4_tangent(flow, x, v[:, None], dt, steps_block, steps_block + 1, lambda s, xx, DD: None)
        v = D[:, 0]; nv = np.linalg.norm(v); v = v / nv
        if b >= n_skip:
            growth += np.log(nv); kept += 1
            for o, P in observers.items():
                f = float(np.sqrt(max(v @ P @ v, 0.0)))
                logs[o].append(np.log(f) if f > 0 else float("-inf"))
    lam1 = growth / (kept * renorm_every)
    out = {"lambda_1": float(lam1), "T_long": T_long, "T_transient": T_transient, "n_points": kept, "observers": {}}
    for o, L in logs.items():
        L = np.array(L); fin = L[np.isfinite(L)]
        out["observers"][o] = {"mean_log_f": float(fin.mean()) if len(fin) else float("nan"), "std_log_f": float(fin.std()) if len(fin) else float("nan"),
                               "n_zero": int((~np.isfinite(L)).sum()), "predicted_offset": float(-fin.mean() / lam1) if len(fin) else float("nan")}
    return out''')

sub('''    if kind == "kernel_of":
        p = spec["_P"]; v = rng.normal(size=n); v[p > 0] = 0.0; return unit(v)''',
    '''    if kind == "kernel_of":
        P = spec["_P"]; v = rng.normal(size=n)
        lam, U = np.linalg.eigh(0.5 * (P + P.T)); K = U[:, lam <= 1e-12]
        return unit(K @ (K.T @ v)) if K.shape[1] else unit(v)''')

sub('''        def record(s, x, D):
            lengths["__euclid__"].append(np.linalg.norm(D, axis=0))
            lengths["__core__"].append(np.linalg.norm(D[: flow.n_core], axis=0))
            for o, p in observers.items():
                lengths[o].append(np.sqrt(np.einsum("ij,i,ij->j", D, p, D)))''',
    '''        def record(s, x, D):
            lengths["__euclid__"].append(np.linalg.norm(D, axis=0))
            lengths["__core__"].append(np.linalg.norm(D[: flow.n_core], axis=0))
            for o, P in observers.items():
                lengths[o].append(obs_lengths(D, P))''')

sub('''            for o, p in observers.items():
                if (p > 0).all():
                    a, b = float(p.min()), float(p.max())
                    row["euclid_horizon_scaled"][o] = {str(B): [horizon(L["__euclid__"][:, di], times, B / np.sqrt(b)), horizon(L["__euclid__"][:, di], times, B / np.sqrt(a))] for B in B_ladder}''',
    '''            for o, P in observers.items():
                pd, a, b = pd_bounds(P)
                if pd:
                    row["euclid_horizon_scaled"][o] = {str(B): [horizon(L["__euclid__"][:, di], times, B / np.sqrt(b)), horizon(L["__euclid__"][:, di], times, B / np.sqrt(a))] for B in B_ladder}''')

sub('''    return {"name": world["name"], "n": n, "n_core": flow.n_core, "mu": flow.mu, "dt": dt, "times_recorded": len(times),
            "observers": {o: [float(v) for v in p] if n <= 8 else {"kind": world["observers"][o]["kind"], "min": float(p.min()), "max": float(p.max())} for o, p in observers.items()},
            "rows": rows, "seconds": time.time() - t_start}''',
    '''    # the independent long trajectory: leading exponent and mean log read-fraction per observer
    clv = clv_stats(flow, starts[0], dt, float(world.get("clv_T_long", 1000.0)), float(world.get("clv_T_transient", 50.0)), observers)
    log(json.dumps({"world": world["name"], "lambda_1": round(clv["lambda_1"], 4), "predicted_offsets": {o: round(v["predicted_offset"], 3) for o, v in clv["observers"].items()}}))
    obs_out = {}
    for o, P in observers.items():
        pd, a, b = pd_bounds(P)
        obs_out[o] = {"kind": world["observers"][o]["kind"], "pd": pd, "min": a, "max": b, "trace": float(np.trace(P))}
    return {"name": world["name"], "n": n, "n_core": flow.n_core, "mu": flow.mu, "dt": dt, "times_recorded": len(times),
            "observers": obs_out, "clv": clv, "rows": rows, "seconds": time.time() - t_start}''')

# self test: matrices in place of diagonals, plus the offset law on the linear flow
sub('''    P_aniso = np.array([4.0, 1.0, 0.25]); P_third = np.array([0.0, 0.0, 1.0]); P_first = np.array([1.0, 0.0, 0.0])
    Ls = {"e": [], "an": [], "third": [], "first": []}
    def record(s, x, D):
        Ls["e"].append(np.linalg.norm(D, axis=0))
        for k, p in (("an", P_aniso), ("third", P_third), ("first", P_first)):
            Ls[k].append(np.sqrt(np.einsum("ij,i,ij->j", D, p, D)))''',
    '''    P_aniso = np.diag([4.0, 1.0, 0.25]); P_third = np.diag([0.0, 0.0, 1.0]); P_first = np.diag([1.0, 0.0, 0.0])
    Ls = {"e": [], "an": [], "third": [], "first": []}
    def record(s, x, D):
        Ls["e"].append(np.linalg.norm(D, axis=0))
        for k, p in (("an", P_aniso), ("third", P_third), ("first", P_first)):
            Ls[k].append(obs_lengths(D, p))''')
sub('''    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''', '''    # offset law on the linear flow: the leading vector is e_1, so a rank-one reader along
    # u = (cos t, sin t, 0) has f = |cos t| and predicted offset -log|cos t| / 1; the measured
    # horizon of that reader against the full reader must match it at large B
    th = 0.7; P_u = observer_P({"kind": "rank1", "vector": [np.cos(th), np.sin(th), 0.0]}, 3)
    clv = clv_stats(flow, np.zeros(3), dt, 40.0, 5.0, {"u": P_u, "full": np.eye(3)})
    pred = clv["observers"]["u"]["predicted_offset"]; exact = -np.log(np.cos(th)) / 1.0
    Lu = []; Le = []
    rk4_tangent(flow, np.zeros(3), D0[:, :1], dt, int(12.0 / dt), rec, lambda s, x, D: (Lu.append(obs_lengths(D, P_u)[0]), Le.append(np.linalg.norm(D[:, 0]))))
    tt = np.arange(0, int(12.0 / dt) + 1, rec) * dt; B = 1e4
    meas = horizon(np.array(Lu), tt, B) - horizon(np.array(Le), tt, B)
    ok = abs(clv["lambda_1"] - 1.0) < 1e-3 and abs(pred - exact) < 1e-3 and abs(meas - exact) < 0.02
    print(f"offset law (linear flow): lambda_1 {clv['lambda_1']:.4f}, predicted {pred:.4f}, exact {exact:.4f}, measured {meas:.4f} {'ok' if ok else 'FAIL'}")
    fails += 0 if ok else 1
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails''')
open(os.path.join(SP, "d3v2_horizon.py"), "w", encoding="utf-8", newline="\n").write(s)
print("d3v2_horizon.py written")
