"""The four declared variants of the sealed runs (experiments/OP/SEALED-RUN-PLAN.md, Section 3).

V1 GRAM-UN  OP4's window-Gramian greedy with the required count raised to the unstable and neutral manifold,
            d_un = #{lambda_i > -0.1 lambda_1} (Trevisan, D'Isidoro and Talagrand 2010). m' = the smallest multiple of
            8 >= 2 d_un, at most m0 (stated cap; m0 = 32 in the config).
V2 ESA      full-covariance sensitivity (Ancell and Hakim 2007): ESA_k = |E_t[v_t dx_k,t]|^2 / Var(x_k) summed over the
            pair's real and imaginary parts, v_t = N_{w_t}(w_t - mean w), computed through the T x T Gram matrix of the v_t.
V3 READ-KE  each gate's READ with only the response norm changed from enstrophy to kinetic energy.
V4 SV       singular-vector targeting in the leading tangent subspace: per window, the SVD of Phi U = A S B^T, pair k
            scored by sum_{i <= d_u} sigma_i^2 |(U b_i)[k]|^2, summed over windows (Buizza and Montani 1999).
Every variant reduces to an arm already run in a stated limit; the self-test checks each reduction.

Parts, so that the probe and the run fan out as one Job each on NRP:
    --part rank   the training-trajectory rankings READ-KE and ESA (and D8's READ recomputed, as a check), cached
    --part gram   the tangent-subspace instruments GRAM-UN and SV (and GRAM at the same m', as a record), cached
    --part nudge  one variant's ordering through D8's nudging protocol on one test trajectory

    python op_variants.py --selftest
    python op_variants.py --config ../../OD/D8/prereg_config.json --vcfg variants_config.json --seed-role pilot \
        --world p_nu030_n96 --part rank --cache cache
    python op_variants.py ... --part nudge --variant ESA --tests 0 --cache cache --out probe_ESA_p_nu030_n96_t0.json
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
sys.path.insert(0, str(HERE.parents[1] / "OD" / "D8")); sys.path.insert(0, str(HERE.parent / "OP4"))
from d8_sync import Candidates, ForcedNS2D, amplitudes, initial_field, merge_halves, nudge_record, sensitivities, spin_up, sq, vel_norm  # noqa: E402
from op4_gram import choose_frac, gram_blocks, greedy_gram, lyapunov_spectrum, qr_basis, to_real, window_readings  # noqa: E402

VARIANTS = ("READ_KE", "ESA", "GRAM_UN", "SV", "GRAM")


# ---------------------------------------------------------------- norms and the two training rankings

def ke_sq(model, X):
    """Sum of |X_k|^2 / |k|^2 over the last two axes in math units: the squared velocity norm over (2 pi)^2."""
    k2 = model.k2true.copy(); k2[0, 0] = np.inf
    return np.sum(np.abs(X) ** 2 / k2, axis=(-2, -1)) / model.n ** 4


def sensitivities_norm(model, wh, cand, chunk: int, norm, mask=None) -> np.ndarray:
    """D8's sensitivities with the response measured in `norm` (sq for enstrophy, ke_sq for kinetic energy) and an
    optional consumer mask: s_k = (norm(M N_w e_re) + norm(M N_w e_im)) / 2."""
    s = np.empty(cand.size); M = 1.0 if mask is None else mask
    for a in range(0, cand.size, chunk):
        sel = np.arange(a, min(a + chunk, cand.size))
        s[sel] = 0.5 * (norm(model, M * model.tangent_nl(wh, cand.unit(sel, model.n, False))) + norm(model, M * model.tangent_nl(wh, cand.unit(sel, model.n, True))))
    return s


def esa_core(V: np.ndarray, dx: np.ndarray) -> np.ndarray:
    """|mean_t v_t dx_t|^2 for every column of dx (T, P), from the Gram matrix V (T, T) of the responses v_t:
    |sum_t v_t dx_t|^2 / T^2 = dx^T V dx / T^2."""
    T = len(V); return np.einsum("tk,ts,sk->k", dx, V, dx) / T ** 2


def esa_scores(model, W: np.ndarray, cand, mask=None) -> np.ndarray:
    """ESA for every candidate pair from training samples W (T, n, n): v_t = N_{w_t}(w_t - mean w), optionally
    masked to the consumer; ESA_k = sum over re/im of |E[v dx_k]|^2 / Var(x_k)."""
    T = len(W); wbar = W.mean(axis=0); M = 1.0 if mask is None else mask
    v = np.stack([M * model.tangent_nl(W[t], W[t] - wbar) for t in range(T)])
    R = to_real(model, v); V = R @ R.T  # <v_t, v_s> in D8's inner product (Re sum conj(a) b / n^4)
    out = np.zeros(cand.size)
    for part in (np.real, np.imag):
        x = part(W[:, cand.ix, cand.iy]) / model.n ** 2; dx = x - x.mean(axis=0); var = (dx ** 2).mean(axis=0)
        out += np.where(var > 0, esa_core(V, dx) / np.where(var > 0, var, 1.0), 0.0)
    return out


def training_samples(model, uh, nsamp: int, per: int, dt: float):
    """D8's training loop: a sample, then `per` steps, nsamp times; returns the samples and the final state."""
    S = []
    for _ in range(nsamp):
        S.append(uh.copy())
        for _ in range(per):
            uh = model.fstep(uh, dt)
    return np.array(S), uh


# ---------------------------------------------------------------- the tangent-subspace instruments

def gram_from_blocks(blocks: list, mp: int, d: int, length: int):
    """GRAM on the leading mp directions of a larger window run: the readings are linear in the basis, so the blocks of
    the first mp basis vectors are the leading mp x mp sub-blocks, and Gram-Schmidt keeps the leading subspace across
    windows. OP4's rules on that subspace: frac by choose_frac, thresholds frac x lambda_max, greedy on count d."""
    sub = [B[:, :mp, :mp] for B in blocks]; Wall = [B.sum(axis=0) for B in sub]
    frac, met = choose_frac(Wall, mp); thr = [frac * float(np.linalg.eigvalsh(W).max()) for W in Wall]
    order, reached = greedy_gram(sub, thr, [min(d, mp)] * len(sub), length)
    return order, reached, frac, met


def un_count(lyap: np.ndarray, factor: float) -> tuple[int, int]:
    """(d_u, d_un): positive exponents (at least 1), and those above -factor * lambda_1 (at least d_u)."""
    l = np.sort(np.asarray(lyap))[::-1]; d_u = max(1, int(np.sum(l > 0)))
    return d_u, max(d_u, int(np.sum(l > -factor * l[0]))) if l[0] > 0 else d_u


def m_prime(d: int, m0: int) -> int:
    return min(m0, 8 * math.ceil(2 * d / 8))


def sv_core(PU: np.ndarray, U: np.ndarray, d: int) -> np.ndarray:
    """PU (dim, m'): the propagated subspace; U (m', dim): its starting basis rows. Returns, per coordinate of dim,
    sum_{i<d} sigma_i^2 (U^T b_i)_c^2 with PU = A S B^T."""
    _, S, Bt = np.linalg.svd(PU, full_matrices=False); F = Bt[:d] @ U  # (d, dim): the right singular vectors in the state
    return np.sum((S[:d, None] ** 2) * F ** 2, axis=0)


def sv_pair_scores(model, cand, U: np.ndarray, Dend: np.ndarray, d: int) -> np.ndarray:
    """SV targeting score of every pair for one window: right singular vectors of Phi U in the state, read at the pair."""
    _, S, Bt = np.linalg.svd(to_real(model, Dend).T, full_matrices=False)
    F = np.tensordot(Bt[:d], U, axes=(1, 0))  # (d, n, n) complex fields
    a = np.abs(F[:, cand.ix, cand.iy]) ** 2 / model.n ** 4
    return np.sum((S[:d, None] ** 2) * a, axis=0)


# ---------------------------------------------------------------- parts

def world_model(world, cfg):
    n = int(world["n"]); model = ForcedNS2D(n, float(world["nu"]), float(cfg["alpha"]), float(cfg["F0"]), int(cfg["kf"]))
    return model, Candidates(model), float(cfg["dt_base"]) * int(cfg["n_ref"]) / n


def rank_part(world, cfg8, vcfg, role, log=print) -> dict:
    cfg = {**cfg8, **world.get("overrides", {})}; t0 = time.time(); off = int(world["seed_offset"]); model, cand, dt = world_model(world, cfg)
    rng = np.random.default_rng(int(cfg[f"seed_{role}_train"]) + off); uh = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
    per = int(round(float(cfg["dt_sample"]) / dt)); n8 = int(round(float(cfg["T_train"]) / float(cfg["dt_sample"]))); ne = int(vcfg["esa_samples"])
    W, _ = training_samples(model, uh, max(n8, ne), per, dt); chunk = int(cfg["chunk"])
    # D8's READ recomputed on D8's own training samples, and READ-KE on the same samples (the norm alone changes)
    A = np.zeros(cand.size); R = np.zeros(cand.size); RK = np.zeros(cand.size)
    for t in range(n8):
        a = amplitudes(model, W[t], cand); R += a * sensitivities(model, W[t], cand, chunk); RK += a * sensitivities_norm(model, W[t], cand, chunk, ke_sq)
    E = esa_scores(model, W[:ne], cand); half = ne // 2
    Ea, Eb = esa_scores(model, W[:half], cand), esa_scores(model, W[half:ne], cand)
    rk = lambda x: np.argsort(np.argsort(x)); split = float(np.corrcoef(rk(Ea), rk(Eb))[0, 1])
    out = {"world": world["name"], "orders": {"READ_recomputed": np.argsort(-R / n8, kind="stable").tolist(), "READ_KE": np.argsort(-RK / n8, kind="stable").tolist(),
           "ESA": np.argsort(-E, kind="stable").tolist()}, "esa_samples": ne, "esa_split_half_spearman": split, "seconds": time.time() - t0}
    for k in ("READ_KE", "ESA"):
        out[f"{k}_first12_kmag"] = [float(cand.kmag[i]) for i in out["orders"][k][:12]]
    log(json.dumps({"world": world["name"], "part": "rank", "esa_split_half": round(split, 3), "READ_KE_first12": [round(x, 2) for x in out["READ_KE_first12_kmag"]], "ESA_first12": [round(x, 2) for x in out["ESA_first12_kmag"]], "seconds": round(out["seconds"], 1)}))
    return out


def gram_part(world, cfg8, vcfg, role, log=print) -> dict:
    cfg = {**cfg8, **world.get("overrides", {})}; t0 = time.time(); off = int(world["seed_offset"]); model, cand, dt = world_model(world, cfg)
    seed = int(cfg[f"seed_{role}_train"]) + off; m0 = int(vcfg["m0"])
    rng = np.random.default_rng(seed); uh = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
    uh, D, lyap = lyapunov_spectrum(model, uh, m0, dt, float(vcfg["dt_qr"]), float(vcfg["T_qr_spin"]), float(vcfg["T_qr_meas"]), np.random.default_rng(seed + 4041))
    l = np.sort(lyap)[::-1]; d_u, d_un = un_count(lyap, float(vcfg["neutral_factor"])); mp = m_prime(d_un, m0)
    T_w = float(np.clip(1.0 / l[0], *vcfg["T_w_clip"])) if l[0] > 0 else float(vcfg["T_w_clip"][1]); U = D[:mp]
    log(json.dumps({"world": world["name"], "part": "gram", "phase": "lyapunov", "lyap_top": [round(float(x), 4) for x in l[:12]], "d_u": d_u, "d_un": d_un, "m_prime": mp, "m_prime_capped": mp < 2 * d_un, "T_w": T_w, "seconds": round(time.time() - t0, 1)}))
    blocks, Wall, sv = [], [], np.zeros(cand.size)
    for _ in range(int(vcfg["n_windows"])):
        uh, Dend, Y, dt_g = window_readings(model, cand, uh, U, dt, T_w, int(vcfg["samples_per_window"]))
        B = gram_blocks(Y, dt_g); blocks.append(B); Wall.append(B.sum(axis=0)); sv += sv_pair_scores(model, cand, U, Dend, d_u)
        U, _ = qr_basis(model, Dend)
    frac, met = choose_frac(Wall, mp); thr = [frac * float(np.linalg.eigvalsh(W).max()) for W in Wall]
    ladder = [m for m in cfg["ladder"] if m <= cand.size]; L = max(ladder)
    o_un, r_un = greedy_gram(blocks, thr, [min(d_un, mp)] * len(blocks), L); o_g, r_g = greedy_gram(blocks, thr, [min(d_u, mp)] * len(blocks), L)
    o_sv = np.argsort(-sv, kind="stable").tolist()
    # GRAM by OP4's rule with the cap stated: its own m' from d_u, on the leading sub-blocks of this run
    mp_g = m_prime(d_u, m0); o_gram, r_gram, frac_g, met_g = gram_from_blocks(blocks, mp_g, d_u, L)
    out = {"world": world["name"], "lyapunov_spectrum": l.tolist(), "d_u": d_u, "d_un": d_un, "m_prime": mp, "m0": m0, "T_w": T_w, "frac": frac, "frac_rule_met": met,
           "orders": {"GRAM_UN": o_un, "SV": o_sv, "GRAM": o_gram, "GRAM_same_subspace": o_g}, "count_to_d_un": r_un, "count_to_d_u": r_g,
           "gram": {"m_prime": mp_g, "frac": frac_g, "frac_rule_met": met_g, "count_to_d_u": r_gram}, "seconds": time.time() - t0}
    for k in ("GRAM_UN", "SV"):
        out[f"{k}_first12_kmag"] = [float(cand.kmag[i]) for i in out["orders"][k][:12]]
    log(json.dumps({"world": world["name"], "part": "gram", "phase": "done", "frac": frac, "count_to_d_un": r_un, "GRAM_UN_first12": [round(x, 2) for x in out["GRAM_UN_first12_kmag"]], "SV_first12": [round(x, 2) for x in out["SV_first12_kmag"]], "seconds": round(out["seconds"], 1)}))
    return out


def nudge_part(world, cfg8, order, name: str, role, tests, log=print, ladder_half: int | None = None) -> dict:
    """One ordering through D8's nudging protocol, unchanged (same seeds and generator per record as D8's graded arms).
    ladder_half: 0 or 1 integrates only that half of the ladder (records carry no m*); merge_variant_halves joins them."""
    cfg = {**cfg8, **world.get("overrides", {})}; off = int(world["seed_offset"]); model, cand, dt = world_model(world, cfg)
    mu = float(cfg["mu"]); chunk = int(cfg["chunk"]); seed_test = int(cfg[f"seed_{role}_test"]); ladder = [m for m in cfg["ladder"] if m <= cand.size]
    lyap = (bool(cfg["obs_lyap"]), role in cfg.get("block_lyap_roles", []))
    out = {"world": world["name"], "variant": name, "ladder": ladder, "ladder_half": ladder_half, "tests": []}
    for j in tests:
        t1 = time.time(); rng = np.random.default_rng(seed_test + 100 * off + j)
        u0 = spin_up(model, initial_field(model, rng, int(cfg["ic_kmax"]), float(cfg["omega_rms"])), float(cfg["T_spin"]), dt)
        d0 = amplitudes(model, u0, cand) * sensitivities(model, u0, cand, chunk)
        rec = nudge_record(model, u0, cand, np.array(order), ladder, mu, dt, cfg, lyap, np.random.default_rng(seed_test + 7 * j + 3), d0, half=ladder_half)
        out["tests"].append({"index": j, "observers": {name: rec}})
        log(json.dumps({"world": world["name"], "test": j, "observer": name, "ladder_half": ladder_half, "m_star": rec.get("m_star"), "synced": rec["synced"],
                        "seconds": round(time.time() - t1, 1)}))
    return out


def merge_variant_halves(lo: dict, hi: dict) -> dict:
    """Two nudge_part outputs of one variant and world, ladder halves 0 and 1 -> the whole ladder's output (D8's merge_halves)."""
    if (lo.get("ladder_half"), hi.get("ladder_half")) != (0, 1): raise ValueError("need nudge outputs of ladder halves 0 and 1")
    for k in ("world", "variant", "ladder"):
        if lo[k] != hi[k]: raise ValueError(f"halves differ in {k}")
    if [t["index"] for t in lo["tests"]] != [t["index"] for t in hi["tests"]]: raise ValueError("halves ran different test trajectories")
    tests = [{"index": a["index"], "observers": {lo["variant"]: merge_halves(a["observers"][lo["variant"]], b["observers"][lo["variant"]], lo["ladder"])}}
             for a, b in zip(lo["tests"], hi["tests"])]
    return {**lo, "ladder_half": None, "merged_from_halves": True, "tests": tests}


# ---------------------------------------------------------------- self-test

def selftest() -> int:
    fails = 0

    def check(label, ok, detail=""):
        nonlocal fails
        print(f"{label}: {detail}", "PASS" if ok else "FAIL"); fails += 0 if ok else 1

    model = ForcedNS2D(32, 0.02, 0.1, 1.0, 4); cand = Candidates(model); wh = initial_field(model, np.random.default_rng(5), 6, 3.0)
    # 1. the kinetic-energy norm is D8's velocity norm squared over (2 pi)^2
    e = abs(ke_sq(model, wh) * (2 * math.pi) ** 2 - vel_norm(model, wh) ** 2) / vel_norm(model, wh) ** 2
    check("ke_sq = velocity norm^2 / (2 pi)^2", e < 1e-12, f"{e:.1e}")
    # 2. READ-KE reduces to READ: with the enstrophy norm, sensitivities_norm is D8's sensitivities exactly
    s8 = sensitivities(model, wh, cand, 64); sn = sensitivities_norm(model, wh, cand, 64, sq)
    check("READ-KE with the enstrophy norm = D8's READ sensitivity", np.array_equal(s8, sn), f"max diff {np.max(np.abs(s8 - sn)):.1e}")
    sk = sensitivities_norm(model, wh, cand, 64, ke_sq); check("the kinetic-energy sensitivity differs from the enstrophy one", not np.allclose(sk, s8) and np.all(sk >= 0), "")
    # 3. ESA's Gram identity: dx^T V dx / T^2 = |mean_t v_t dx_t|^2 exactly, on random vectors
    rng = np.random.default_rng(1); T, P, D = 40, 7, 30; v = rng.normal(size=(T, D)); dx = rng.normal(size=(T, P))
    direct = np.array([np.sum((v * dx[:, [k]]).mean(axis=0) ** 2) for k in range(P)]); gram = esa_core(v @ v.T, dx)
    check("ESA's Gram identity", np.allclose(direct, gram, rtol=1e-12), f"{np.max(np.abs(direct - gram)):.1e}")
    # 4. ESA reduces to READ when the response is linear, constant and the modes are independent: ESA_k -> |J_k|^2 Var(x_k)
    T, P, D = 200000, 4, 6; J = rng.normal(size=(P, D)); sd = np.array([0.5, 1.0, 2.0, 0.3]); X = rng.normal(size=(T, P)) * sd
    v = X @ J; dxx = X - X.mean(axis=0); esa = np.array([np.sum((v * dxx[:, [k]]).mean(axis=0) ** 2) for k in range(P)]) / dxx.var(axis=0)
    read = np.sum(J ** 2, axis=1) * sd ** 2; err = float(np.max(np.abs(esa - read) / read))
    check("ESA -> READ for independent modes and a constant linear response", err < 0.02, f"max rel diff {err:.4f} (sampling)")
    # 5. ESA on the flow runs and returns finite, non-negative scores for every pair
    W = np.stack([wh, model.fstep(wh, 0.01), model.fstep(model.fstep(wh, 0.01), 0.01), initial_field(model, np.random.default_rng(6), 6, 3.0)])
    E = esa_scores(model, W, cand); check("ESA on the flow: finite and non-negative for every pair", E.shape == (cand.size,) and np.all(np.isfinite(E)) and np.all(E >= 0), f"{cand.size} pairs")
    # 6. the unstable-plus-neutral count, on OP4's probe spectrum (6 positive; -0.0014, -0.0042, -0.0064 above -0.0083)
    probe = np.array([0.0832, 0.0797, 0.0699, 0.0573, 0.0495, 0.0411, -0.0014, -0.0042, -0.0064, -0.0179, -0.0758])
    du, dun = un_count(probe, 0.1); check("d_u and d_un on OP4's probe spectrum", (du, dun) == (6, 9) and m_prime(9, 32) == 24 and m_prime(17, 32) == 32 and un_count(np.array([-0.1, -0.2]), 0.1) == (1, 1), f"d_u {du}, d_un {dun}")
    # 7. SV reduces to the leading direction: a diagonal system propagated from the identity scores the fastest coordinate
    lam = np.array([0.9, 0.4, -0.2, -0.5]); PU = np.diag(np.exp(lam * 1.0)); sc = sv_core(PU, np.eye(4), 1)
    check("SV with one singular vector picks the fastest-growing coordinate", int(np.argmax(sc)) == 0 and np.allclose(sc[1:], 0) and abs(sc[0] - math.exp(1.8)) < 1e-9, str(np.round(sc, 4)))
    sc2 = sv_core(PU, np.eye(4), 2); check("SV with two singular vectors scores the two growing coordinates by sigma^2", np.allclose(sc2, [math.exp(1.8), math.exp(0.8), 0, 0]), str(np.round(sc2, 4)))
    # 8. SV on the flow: the pair scores equal the coordinate scores of sv_core gathered at the pairs
    U, _ = qr_basis(model, np.stack([initial_field(model, np.random.default_rng(10 + i), 6, 1.0) for i in range(4)]))
    Dend = U * 1.0; Dend[0] *= 3.0; ps = sv_pair_scores(model, cand, U, Dend, 2)
    _, S, Bt = np.linalg.svd(to_real(model, Dend).T, full_matrices=False); F = np.tensordot(Bt[:2], U, axes=(1, 0))
    ref = np.sum((S[:2, None] ** 2) * (np.abs(F[:, cand.ix, cand.iy]) ** 2 / 32 ** 4), axis=0)
    check("SV pair scores consistent; the stretched direction leads", np.allclose(ps, ref) and abs(S[0] - 3.0) < 1e-9, f"sigma_1 {S[0]:.3f}")
    # 9. GRAM from sub-blocks: on the flow, the window run of the first 4 of 8 basis vectors gives exactly the leading 4 x 4
    # sub-blocks of the 8-vector run, and the next window's leading basis is the same (Gram-Schmidt keeps the leading subspace)
    D8i = np.fft.fft2(np.random.default_rng(11).normal(size=(8, 32, 32))) * model.dealias; D8i[:, 0, 0] = 0; U8, _ = qr_basis(model, D8i)
    _, De8, Y8, dg = window_readings(model, cand, wh, U8, 0.01, 0.2, 4); _, De4, Y4, _ = window_readings(model, cand, wh, U8[:4], 0.01, 0.2, 4)
    B8 = gram_blocks(Y8, dg); B4 = gram_blocks(Y4, dg); e_b = float(np.max(np.abs(B8[:, :4, :4] - B4)) / np.max(np.abs(B4)))
    Q8, _ = qr_basis(model, De8); Q4, _ = qr_basis(model, De4); e_q = float(np.max(np.abs(Q8[:4] - Q4)) / np.max(np.abs(Q4)))
    check("GRAM sub-blocks: blocks of the leading 4 of 8 vectors = leading sub-blocks; QR keeps the leading basis", e_b < 1e-12 and e_q < 1e-10, f"blocks {e_b:.1e}, basis {e_q:.1e}")
    # 10. gram_from_blocks on the full subspace equals greedy_gram run directly with choose_frac's thresholds
    o1, r1, f1, _ = gram_from_blocks([B8], 8, 3, 12); W = B8.sum(axis=0); f2, _ = choose_frac([W], 8); o2, r2 = greedy_gram([B8], [f2 * float(np.linalg.eigvalsh(W).max())], [3], 12)
    check("gram_from_blocks with the full subspace = OP4's rule applied directly", o1 == o2 and r1 == r2 and f1 == f2, f"order[:6] {o1[:6]}")
    print("SELFTEST", "PASS" if fails == 0 else f"FAIL ({fails})")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--config"); ap.add_argument("--vcfg"); ap.add_argument("--seed-role", default="pilot")
    ap.add_argument("--world"); ap.add_argument("--part", choices=["rank", "gram", "nudge"]); ap.add_argument("--variant", choices=VARIANTS)
    ap.add_argument("--tests", default="0"); ap.add_argument("--cache", default="cache"); ap.add_argument("--out")
    ap.add_argument("--ladder-half", type=int, choices=[0, 1], default=None, help="nudge part: integrate only this half of the ladder")
    a = ap.parse_args(argv)
    if a.selftest: return 1 if selftest() else 0
    cfg8 = json.load(open(a.config, encoding="utf-8")); vcfg = json.load(open(a.vcfg, encoding="utf-8"))
    world = next(w for w in cfg8["worlds"] if w["name"] == a.world); Path(a.cache).mkdir(exist_ok=True)
    if a.part in ("rank", "gram"):
        res = rank_part(world, cfg8, vcfg, a.seed_role) if a.part == "rank" else gram_part(world, cfg8, vcfg, a.seed_role)
        p = Path(a.cache) / f"{a.part}_{a.world}_{a.seed_role}.json"; tmp = p.with_suffix(".tmp"); tmp.write_text(json.dumps(res, default=float), encoding="utf-8"); tmp.replace(p)
        if a.out: Path(a.out).write_text(json.dumps(res, default=float), encoding="utf-8")
        return 0
    src = "rank" if a.variant in ("READ_KE", "ESA") else "gram"; p = Path(a.cache) / f"{src}_{a.world}_{a.seed_role}.json"  # GRAM comes from the gram part
    if not p.exists(): raise SystemExit(f"{p} missing: run --part {src} first")
    order = json.loads(p.read_text(encoding="utf-8"))["orders"][a.variant]
    res = nudge_part(world, cfg8, order, a.variant, a.seed_role, [int(x) for x in a.tests.split(",")], ladder_half=a.ladder_half)
    json.dump(res, open(a.out, "w", encoding="utf-8"), indent=1, default=float); return 0


if __name__ == "__main__":
    sys.exit(main())
