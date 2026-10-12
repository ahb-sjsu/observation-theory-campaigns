"""OP4: D6v3's spectral selector on D8's flow, the instrument or the system (OP track, gate OP4).

Design: `OP4-DESIGN-DRAFT.md`. D6v3 chose sensors on linear systems by the spectrum of the exact window Gramian: the count
d_obs of directions whose Gramian eigenvalue clears a threshold, greedy on that count with ties broken by the m-th
eigenvalue. OP4 carries the instrument to D8's forced two-dimensional turbulence, restricted to the flow's leading
tangent subspace, and puts the resulting ordering of Fourier pairs (GRAM) through D8's nudging protocol unchanged.

The instrument on the flow. Along the training trajectory (D8's seeds, D8's spin-up), m0 tangent vectors are carried
under D8's tangent `ftangent` and re-orthonormalized every dt_qr (a QR iteration); the mean logs of R's diagonal give the
finite-time Lyapunov spectrum, its leading exponent lambda_1 and the unstable dimension d_u (the count of positive
exponents, at least 1). The draft's rule then fixes, blind to any nudging result,
    T_w = 1 / lambda_1 (clipped to [t_min, t_max]),  m' = the smallest multiple of 8 >= 2 d_u (at most m0),
    frac = the largest of {0.1, 0.01, 0.001} at which the all-pairs Gramian identifies all m' directions in every window.
In each of n_win back-to-back windows, the leading m' vectors U at the window's start are propagated without
renormalization; pair k's rows C_k Phi(t_j) U are its real and imaginary coefficients in the propagated vectors, so
    W_k = sum_j (C_k Phi(t_j) U)^T (C_k Phi(t_j) U) dt_g        (an m' x m' block per pair and window),
and W_S = sum_{k in S} W_k, exactly as D6's Gramian is additive in C^T C. At the window's end the propagated vectors are
re-orthonormalized and become the next window's U.

The selector. Greedy over pairs, with D6's key while the count is being reached, summed over windows:
    (sum_w d_obs_w(S + k), sum_w lambda_{d_u}(W_{S+k,w}), -k);
once every window has d_obs >= d_u, the tie-break becomes the m'-th eigenvalue, so the ordering fills D8's ladder. On a
linear system with one window and the whole space as U it is D6's greedy (self-test).

    python op4_gram.py --selftest
    python op4_gram.py --config ../../OD/D8/prereg_config.json --op4 op4_config.json --seed-role pilot --world p_nu030_n96 --part gram --cache gram
    python op4_gram.py ... --part nudge --tests 0 --cache gram --out pilot_p_nu030_n96_t0.json
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "OD" / "D8")); sys.path.insert(0, str(HERE.parents[1] / "OD" / "D6v3"))
from d8_sync import Candidates, ForcedNS2D, amplitudes, initial_field, nudge_record, sensitivities, spin_up, sq, stability  # noqa: E402

FRACS = (0.1, 0.01, 0.001)


# ---------------------------------------------------------------- the system-agnostic core

def gram_blocks(Y: np.ndarray, dt_g: float) -> np.ndarray:
    """Y (samples, P, r, m'): each sensor's r readings of the m' propagated directions at each sample. Returns the per-sensor
    blocks W_k = sum_j Y_jk^T Y_jk dt_g, shape (P, m', m'), by the trapezoid rule over the samples."""
    w = np.full(len(Y), dt_g); w[0] = w[-1] = dt_g / 2
    return np.einsum("j,jkri,jkrl->kil", w, Y, Y)


def counts_and_tie(blocks_w: list[np.ndarray], WS_w: list[np.ndarray], thr: list[float], target: list[int]):
    """For every candidate k: sum over windows of d_obs(W_S + W_k) and of the target-th largest eigenvalue."""
    cnt = 0; tie = 0.0
    for B, WS, c, t in zip(blocks_w, WS_w, thr, target):
        lam = np.linalg.eigvalsh(WS[None] + B)[:, ::-1]  # descending, (P, m')
        cnt = cnt + (lam > c).sum(axis=1); tie = tie + lam[:, t - 1]
    return cnt, tie


def greedy_gram(blocks_w: list[np.ndarray], thr: list[float], d_u: list[int], length: int) -> tuple[list[int], int | None]:
    """D6's greedy summed over windows: key (count, d_u-th eigenvalue, -index) until every window reaches d_u, then the
    m'-th eigenvalue as the tie-break. Returns the ordering and the count at which every window first reached d_u."""
    P, mp = blocks_w[0].shape[0], blocks_w[0].shape[1]; S: list[int] = []; WS = [np.zeros((mp, mp)) for _ in blocks_w]
    avail = np.ones(P, bool); idx = np.arange(P); reached = None
    while len(S) < min(length, P):
        done = all(int((np.linalg.eigvalsh(W) > c).sum()) >= d for W, c, d in zip(WS, thr, d_u))
        if done and reached is None: reached = len(S)
        target = [mp] * len(d_u) if done else list(d_u)
        cnt, tie = counts_and_tie([B[avail] for B in blocks_w], WS, thr, target)
        cand = idx[avail]; best = cand[np.lexsort((-cand, tie, cnt))[-1]]
        S.append(int(best)); avail[best] = False
        for w, B in enumerate(blocks_w):
            WS[w] = WS[w] + B[best]
    if reached is None and all(int((np.linalg.eigvalsh(W) > c).sum()) >= d for W, c, d in zip(WS, thr, d_u)): reached = len(S)
    return S, reached


def choose_params(lyap: np.ndarray, m0: int, t_clip: tuple[float, float]) -> dict:
    """The draft's rule, from the Lyapunov spectrum alone: T_w = 1 / lambda_1 clipped, d_u = count of positive exponents
    (at least 1), m' = the smallest multiple of 8 >= 2 d_u, at most m0."""
    lyap = np.sort(np.asarray(lyap))[::-1]  # finite-time QR exponents need not come out ordered (smoke run, 2026-10-12)
    l1 = float(lyap[0]); d_u = max(1, int(np.sum(lyap > 0))); mp = min(m0, 8 * math.ceil(2 * d_u / 8))
    T = float(np.clip(1.0 / l1, *t_clip)) if l1 > 0 else float(t_clip[1])
    return {"lambda_1": l1, "d_u": d_u, "m_prime": mp, "T_w": T, "T_w_unclipped": (1.0 / l1) if l1 > 0 else None}


def choose_frac(Wall_w: list[np.ndarray], mp: int) -> tuple[float, bool]:
    """The largest frac at which the all-pairs Gramian identifies every one of the m' directions in every window."""
    for f in FRACS:
        if all(int((np.linalg.eigvalsh(W) > f * np.linalg.eigvalsh(W).max()).sum()) == mp for W in Wall_w): return f, True
    return FRACS[-1], False


# ---------------------------------------------------------------- the flow: tangents, QR, readings

def to_real(model, D: np.ndarray) -> np.ndarray:
    """Complex spectral batch (B, n, n) -> real rows whose dot product is D8's inner product Re sum conj(a) b / n^4."""
    return np.concatenate([D.real.reshape(len(D), -1), D.imag.reshape(len(D), -1)], axis=1) / model.n ** 2


def from_real(model, R: np.ndarray) -> np.ndarray:
    n = model.n; h = n * n; return (R[:, :h] + 1j * R[:, h:]).reshape(len(R), n, n) * n ** 2


def qr_basis(model, D: np.ndarray):
    Q, Rm = np.linalg.qr(to_real(model, D).T); s = np.sign(np.diag(Rm)); s[s == 0] = 1
    return from_real(model, (Q * s).T), np.abs(np.diag(Rm))


def step_with_tangents(model, uh, D, dt):
    k1 = model.frhs(uh); l1 = model.ftangent(uh, D); u2 = uh + 0.5 * dt * k1; k2 = model.frhs(u2); l2 = model.ftangent(u2, D + 0.5 * dt * l1)
    u3 = uh + 0.5 * dt * k2; k3 = model.frhs(u3); l3 = model.ftangent(u3, D + 0.5 * dt * l2); u4 = uh + dt * k3; k4 = model.frhs(u4); l4 = model.ftangent(u4, D + dt * l3)
    return uh + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4), D + dt / 6 * (l1 + 2 * l2 + 2 * l3 + l4)


def lyapunov_spectrum(model, uh, m0: int, dt: float, dt_qr: float, T_spin_qr: float, T_meas: float, rng):
    """QR iteration with m0 tangent vectors: T_spin_qr to align them, then T_meas to average log R's diagonal."""
    D = np.fft.fft2(rng.normal(size=(m0, model.n, model.n))) * model.dealias; D[:, 0, 0] = 0  # no pair observes the mean
    D, _ = qr_basis(model, D); per = int(round(dt_qr / dt)); acc = np.zeros(m0); t = 0.0
    for phase, T in (("spin", T_spin_qr), ("meas", T_meas)):
        for _ in range(int(round(T / dt_qr))):
            for _ in range(per):
                uh, D = step_with_tangents(model, uh, D, dt)
            D, r = qr_basis(model, D)
            if phase == "meas": acc += np.log(r); t += dt_qr
    return uh, D, acc / t


def window_readings(model, cand: Candidates, uh, U, dt: float, T_w: float, n_samples: int):
    """Propagate U (m', n, n) over the window without renormalization; at n_samples + 1 equally spaced times read every
    pair's real and imaginary coefficient in each propagated vector. Returns (uh_end, U_end, Y (samples, P, 2, m'), dt_g)."""
    steps = int(round(T_w / dt)); per = max(1, steps // n_samples); D = U.copy(); Y = []

    def read(D):
        v = D[:, cand.ix, cand.iy] / model.n ** 2; return np.stack([v.real.T, v.imag.T], axis=1)  # (P, 2, m')
    Y.append(read(D))
    for s in range(1, steps + 1):
        uh, D = step_with_tangents(model, uh, D, dt)
        if s % per == 0: Y.append(read(D))
    return uh, D, np.array(Y), per * dt


def gram_part(world: dict, cfg8: dict, op4: dict, seed_role: str, log=print) -> dict:
    """The per-world instrument: Lyapunov spectrum, the rule's parameters, the window Gramians, frac and the GRAM order."""
    cfg = {**cfg8, **world.get("overrides", {})}; t0 = time.time(); n = int(world["n"]); off = int(world["seed_offset"])
    model = ForcedNS2D(n, float(world["nu"]), float(cfg["alpha"]), float(cfg["F0"]), int(cfg["kf"])); cand = Candidates(model)
    dt = float(cfg["dt_base"]) * int(cfg["n_ref"]) / n; seed_train = int(cfg[f"seed_{seed_role}_train"])
    rng = np.random.default_rng(seed_train + off); uh = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
    uh, D, lyap = lyapunov_spectrum(model, uh, int(op4["m0"]), dt, float(op4["dt_qr"]), float(op4["T_qr_spin"]), float(op4["T_qr_meas"]), np.random.default_rng(seed_train + off + 4041))
    par = choose_params(lyap, int(op4["m0"]), tuple(op4["T_w_clip"])); mp = par["m_prime"]; U = D[:mp]
    log(json.dumps({"world": world["name"], "phase": "lyapunov", "lyap_top": [round(float(x), 4) for x in lyap[:8]], **par, "seconds": round(time.time() - t0, 1)}))
    blocks_w = []; Wall_w = []; ftle_w = []
    for w in range(int(op4["n_windows"])):
        uh, Dend, Y, dt_g = window_readings(model, cand, uh, U, dt, par["T_w"], int(op4["samples_per_window"]))
        B = gram_blocks(Y, dt_g); blocks_w.append(B); Wall_w.append(B.sum(axis=0))
        U, r = qr_basis(model, Dend); ftle_w.append((np.log(r) / par["T_w"]).tolist())
    frac, met = choose_frac(Wall_w, mp); thr = [frac * float(np.linalg.eigvalsh(W).max()) for W in Wall_w]; d_u = [min(par["d_u"], mp)] * len(blocks_w)
    ladder = [m for m in cfg["ladder"] if m <= cand.size]; order, reached = greedy_gram(blocks_w, thr, d_u, max(ladder))
    out = {"world": world["name"], "params": par, "frac": frac, "frac_rule_met": met, "thresholds": thr, "lyapunov_spectrum": lyap.tolist(), "window_ftle": ftle_w,
           "order": order, "count_to_d_u": reached, "order_k": [[int(cand.kx[i]), int(cand.ky[i])] for i in order[:64]],
           "order_kmag_first32": [float(np.hypot(cand.kx[i], cand.ky[i])) for i in order[:32]], "seconds": time.time() - t0}
    log(json.dumps({"world": world["name"], "phase": "gram", "frac": frac, "frac_rule_met": met, "count_to_d_u": reached, "first12_kmag": [round(x, 2) for x in out["order_kmag_first32"][:12]], "seconds": round(out["seconds"], 1)}))
    return out


def nudge_part(world: dict, cfg8: dict, gram: dict, seed_role: str, tests: list[int], recheck_ball: bool, log=print) -> dict:
    """GRAM through D8's nudging protocol, on D8's test trajectories (same seeds, same generator for each record)."""
    cfg = {**cfg8, **world.get("overrides", {})}; n = int(world["n"]); off = int(world["seed_offset"])
    model = ForcedNS2D(n, float(world["nu"]), float(cfg["alpha"]), float(cfg["F0"]), int(cfg["kf"])); cand = Candidates(model)
    dt = float(cfg["dt_base"]) * int(cfg["n_ref"]) / n; mu = float(cfg["mu"]); chunk = int(cfg["chunk"])
    seed_test = int(cfg[f"seed_{seed_role}_test"]); ladder = [m for m in cfg["ladder"] if m <= cand.size]
    lyap = (bool(cfg["obs_lyap"]), seed_role in cfg.get("block_lyap_roles", [])); order = np.array(gram["order"]); out = {"world": world["name"], "tests": []}
    for j in tests:
        t1 = time.time(); rng = np.random.default_rng(seed_test + 100 * off + j)
        u0 = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
        d0 = amplitudes(model, u0, cand) * sensitivities(model, u0, cand, chunk); rec = {"index": j, "observers": {}}
        rec["observers"]["GRAM"] = nudge_record(model, u0, cand, order, ladder, mu, dt, cfg, lyap, np.random.default_rng(seed_test + 7 * j + 3), d0)
        log(json.dumps({"world": world["name"], "test": j, "observer": "GRAM", "m_star": rec["observers"]["GRAM"]["m_star"], "seconds": round(time.time() - t1, 1)}))
        if recheck_ball:  # D8's results are seed-deterministic; BALL is rerun here to check that they reproduce
            rec["observers"]["BALL_recheck"] = nudge_record(model, u0, cand, cand.ball_order(), ladder, mu, dt, cfg, lyap, np.random.default_rng(seed_test + 7 * j + 3), d0)
            log(json.dumps({"world": world["name"], "test": j, "observer": "BALL_recheck", "m_star": rec["observers"]["BALL_recheck"]["m_star"], "seconds": round(time.time() - t1, 1)}))
        out["tests"].append(rec)
    return out


# ---------------------------------------------------------------- self-test

def selftest() -> int:
    import d6v3_placement as d6
    from scipy.linalg import expm
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    # 1. On a linear D6 world with one window and the whole space as U, OP4's greedy is D6's greedy
    rng = np.random.default_rng(0); A = d6.world_matrix("lorenz96", 10, {"F": 8.0}); C = d6.candidate_sensors("lorenz96", 10, rng, {}); T = 0.5
    blocks = np.stack([d6.gramian(A, C[[i]], T) for i in range(10)]); Wa = np.linalg.eigvalsh(d6.gramian(A, C, T)).max()
    for frac, m in ((1e-3, 4), (1e-2, 8), (1e-1, 6), (1e-1, 8)):  # higher thresholds and counts force longer selections
        c = frac * Wa
        Sd = d6.greedy(A, C, T, c, m, 10); So, reached = greedy_gram([blocks], [c], [m], len(Sd))
        check(f"OP4's greedy = D6's greedy on Lorenz-96 n = 10, frac = {frac}, m = {m}", So == Sd and reached == (len(Sd) if d6.d_obs(d6.gramian(A, C[Sd], T), c) >= m else None), f"D6 {Sd}, OP4 {So}, reached {reached}")
    # 2. The sampled Gramian from propagated directions equals D6's Van Loan Gramian (U = the whole space)
    ts = np.linspace(0, T, 401); Y = np.array([[C[[i]] @ expm(A * t) for i in range(10)] for t in ts])  # (samples, P, 1, n)
    Bs = gram_blocks(Y, ts[1] - ts[0]); err = float(np.max(np.abs(Bs.sum(0) - d6.gramian(A, C, T))) / np.abs(d6.gramian(A, C, T)).max())
    check("sampled Gramian = Van Loan Gramian", err < 1e-4, f"relative {err:.1e}")
    # 3. On a system with a known unstable subspace, pairs that observe it identify d_u directions, pairs that miss it do not
    A2 = np.diag([0.8, 0.5, -0.3, -0.6, -1.0, -1.2]); U = np.eye(6)[:, :2]; C2 = np.eye(6)  # sensors read single coordinates
    Y2 = np.array([[C2[[i]] @ expm(A2 * t) @ U for i in range(6)] for t in ts]); B2 = gram_blocks(Y2, ts[1] - ts[0]); thr = 1e-3 * np.linalg.eigvalsh(B2.sum(0)).max()
    seen = int((np.linalg.eigvalsh(B2[0] + B2[1]) > thr).sum()); missed = int((np.linalg.eigvalsh(B2[2] + B2[3] + B2[4]) > thr).sum()); So, reached = greedy_gram([B2], [thr], [2], 6)
    check("unstable subspace: observing it identifies d_u, missing it does not; greedy takes it first", seen == 2 and missed == 0 and sorted(So[:2]) == [0, 1] and reached == 2, f"seen {seen}, missed {missed}, order {So}")
    # 4. The parameter rule
    p = choose_params(np.array([0.1, 0.25, -0.05, 0.02, -0.3]), 32, (1.0, 20.0)); p2 = choose_params(np.array([-0.01, -0.2]), 32, (1.0, 20.0))
    check("parameter rule on unordered exponents (T_w = 1 / largest, d_u, m' a multiple of 8 >= 2 d_u)", p["d_u"] == 3 and p["m_prime"] == 8 and abs(p["T_w"] - 4.0) < 1e-12 and p2["d_u"] == 1 and p2["T_w"] == 20.0, str({k: p[k] for k in ("d_u", "m_prime", "T_w")}))
    # 5. QR iteration recovers the growth rates of a diagonal linear system
    rates = np.array([0.6, 0.2, -0.4]); M = np.eye(3); acc = np.zeros(3)
    for _ in range(50):
        M = expm(np.diag(rates) * 0.5) @ M; Q, R = np.linalg.qr(M); M = Q; acc += np.log(np.abs(np.diag(R)))
    check("QR exponents", np.allclose(acc / 25.0, rates, atol=1e-10), str(np.round(acc / 25.0, 6)))
    # 6. On the flow: the propagated tangent equals the central difference of D8's solver over a short window
    model = ForcedNS2D(32, 0.02, 0.1, 1.0, 4); cand = Candidates(model); wh = initial_field(model, np.random.default_rng(5), 6, 3.0); dt = 0.01
    d = np.fft.fft2(np.random.default_rng(6).normal(size=(32, 32))) * model.dealias; d = d / math.sqrt(sq(model, d)) * math.sqrt(sq(model, wh)); eps = 1e-6
    up, um = wh + eps * d, wh - eps * d; base, D = wh, d[None]
    for _ in range(50):
        up = model.fstep(up, dt); um = model.fstep(um, dt); base, D = step_with_tangents(model, base, D, dt)
    cd = (up - um) / (2 * eps); e6 = math.sqrt(sq(model, cd - D[0]) / sq(model, D[0])); check("propagated tangent = central difference of the solver over 0.5", e6 < 1e-6, f"{e6:.1e}")
    # 7. The pair readings cover the state: summed over every pair, the blocks are half the full Gram matrix of the vectors
    D7i = np.fft.fft2(np.random.default_rng(7).normal(size=(4, 32, 32))) * model.dealias; D7i[:, 0, 0] = 0; U7, _ = qr_basis(model, D7i)
    _, _, Y7, dtg = window_readings(model, cand, wh, U7, dt, 0.3, 6); Bsum = gram_blocks(Y7, dtg).sum(0)
    ts7 = np.arange(len(Y7)) * dtg; D7 = U7.copy(); base7 = wh; G = []; per = int(round(dtg / dt))
    G.append(to_real(model, D7) @ to_real(model, D7).T)
    for s in range(1, len(Y7)):
        for _ in range(per):
            base7, D7 = step_with_tangents(model, base7, D7, dt)
        G.append(to_real(model, D7) @ to_real(model, D7).T)
    w = np.full(len(G), dtg); w[0] = w[-1] = dtg / 2; Gfull = sum(wi * g for wi, g in zip(w, G)); e7 = float(np.max(np.abs(Bsum - 0.5 * Gfull)) / np.abs(Gfull).max())
    check("pair readings: sum of blocks = half the full Gram matrix (each pair stands for +-k)", e7 < 1e-12, f"{e7:.1e}")
    # 8. With every pair observed, the Gramian identifies all m' directions, and choose_frac reports the rule met
    frac, met = choose_frac([Bsum], 4); check("all pairs identify every direction; frac rule met", met and int((np.linalg.eigvalsh(Bsum) > frac * np.linalg.eigvalsh(Bsum).max()).sum()) == 4, f"frac {frac}")
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config", help="D8's prereg_config.json (worlds, seeds, nudging)")
    ap.add_argument("--op4", help="op4_config.json (the instrument's settings)"); ap.add_argument("--seed-role", default="pilot"); ap.add_argument("--world")
    ap.add_argument("--part", choices=["gram", "nudge"]); ap.add_argument("--tests", default="0"); ap.add_argument("--cache", default="gram")
    ap.add_argument("--recheck-ball", action="store_true"); ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    cfg8 = json.load(open(a.config, encoding="utf-8")); op4 = json.load(open(a.op4, encoding="utf-8"))
    world = next(w for w in cfg8["worlds"] if w["name"] == a.world); Path(a.cache).mkdir(exist_ok=True); cache = Path(a.cache) / f"{a.world}_{a.seed_role}.json"
    if a.part == "gram":
        g = gram_part(world, cfg8, op4, a.seed_role); tmp = cache.with_suffix(".tmp"); tmp.write_text(json.dumps(g, default=float), encoding="utf-8"); tmp.replace(cache); return 0
    if not cache.exists(): raise SystemExit(f"{cache} missing: run --part gram first")
    g = json.loads(cache.read_text(encoding="utf-8")); res = nudge_part(world, cfg8, g, a.seed_role, [int(x) for x in a.tests.split(",")], a.recheck_ball)
    res["gram"] = {k: v for k, v in g.items() if k != "order"}; json.dump(res, open(a.out, "w", encoding="utf-8"), indent=1, default=float); return 0


if __name__ == "__main__":
    sys.exit(main())
