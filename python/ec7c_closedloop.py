"""PREREG-EC7-003 (DRAFT) -- EC-7 third seal: ANALYTIC effort matching.

Successor to PREREG-EC7-001 (FAIL: absolute-transfer integrity) and
PREREG-EC7-002 (FAIL: cross-arm spread, arm-differential in 1/20 systems).
Both misses were failures of the same instrument: simulation-bisection
effort matching, whose calibration-to-heldout transfer error can be
common-mode (v1) or comparison-contaminating (v2).

The v3 instrument is ANALYTIC and removes the error class entirely. The
Kalman covariance recursion is control-independent, so the sensing schedule
and per-step gains are FIXED per (system, charge level) and computed once.
The expected effort E||u_t||^2 = tr(K Xi_t K') then follows exactly by
propagating the joint second moment of (x, xhat) through the identical
schedule: predict z+ = F z + [w;0] with F = [[A, -BK],[0, A-BK]], and for
each scalar update with gain kal and row h, z <- G z + [0;kal] v with
G = [[I,0],[kal h', I - kal h']]. rho is bisected so the ANALYTIC mean
effort hits the ANALYTIC target (the oracle arm at rho = 1) -- no noise
bundles enter the matching at all. Held-out evaluation rollouts (CRN across
arms) then scatter around a genuinely common expected effort, and the
cross-arm spread gate measures only that scatter.

All PREDICTION bars inherited unchanged for the third time (K1 >= 0.04,
K2 capture >= 0.60, K3 >= 0.00). Building blocks imported from the sealed
ec7_closedloop.py (NOT modified).

  --calibrate       internal calibration; prints candidate spread band.
  --governed SEED   single governed run; writes results/EC7C-closedloop.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from blind_scheduling import (D, K_BUDGET, T_STEPS, N_TEST, LAMBDA_P,
                              make_system, steady_prior, greedy_weighted,
                              make_noise_bundles, probe_read_operator,
                              anti_operator, LinearConsumer)
from ec7_closedloop import (M_U, DIAG_FAMILY, dare_gain, rollout_cl,
                            FROZEN_DELTA_K1, FROZEN_EPS_K2, FROZEN_DELTA_K3)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_SYS_CAL = 8
N_SYS_GOV = 20
N_ENDPOINT_BUNDLES = 6   # hand-diag family selection only (not matching)
BISECT_ITERS = 20        # analytic evaluation is cheap; bisect tightly

# ----------------------------- SEALED GATE (frozen 2026-08-19 from the
# calibration pilot; must match PREREG-EC7-003)
FROZEN_SPREAD_BAND = 0.10  # I2: cross-arm (max-min)/mean HELD-OUT effort per
                           # system. With analytic matching this is PURE CRN
                           # eval scatter of a common expectation: cal max
                           # 0.0439 over n=8 (2.3x headroom for the n=20
                           # max statistic); the analytic residual itself
                           # measured 1e-5.


def precompute_schedule(A, Q, H, r, charged_uses):
    """The sensing schedule and Kalman gains are control-independent:
    compute once per (system, charge). Returns per-step lists of
    (h, kal) pairs in application order."""
    S = steady_prior(A, Q)
    reduced = set(np.linspace(0, T_STEPS - 1, min(charged_uses, T_STEPS)).astype(int)) \
        if charged_uses else set()
    sched = []
    for t in range(T_STEPS):
        S = A @ S @ A.T + Q
        S = 0.5 * (S + S.T)
        steps = []
        k_t = K_BUDGET - (1 if t in reduced else 0)
        if k_t > 0:
            for i in greedy_weighted(np.eye(D), S, H, r, K_BUDGET)[:k_t]:
                h = H[i]
                Sh = S @ h
                kal = Sh / (h @ Sh + r[i])
                steps.append((h.copy(), kal.copy(), float(r[i])))
                S = S - np.outer(kal, Sh)
                S = 0.5 * (S + S.T)
        sched.append(steps)
    return sched


def analytic_effort(A, B, Q, K, sched, S0):
    """Exact mean E||u_t||^2 over the horizon by joint second-moment
    propagation of z = (x, xhat), replicating rollout_cl's order exactly:
    u from the current xhat, then predict, then the scheduled updates."""
    n = 2 * D
    Pz = np.zeros((n, n))
    Pz[:D, :D] = S0
    F = np.zeros((n, n))
    F[:D, :D] = A
    F[:D, D:] = -B @ K
    F[D:, D:] = A - B @ K
    Wn = np.zeros((n, n))
    Wn[:D, :D] = Q
    eff = 0.0
    for t in range(T_STEPS):
        Xi = Pz[D:, D:]
        eff += float(np.trace(K @ Xi @ K.T))
        Pz = F @ Pz @ F.T + Wn
        for h, kal, r_i in sched[t]:
            G = np.eye(n)
            G[D:, :D] = np.outer(kal, h)
            G[D:, D:] -= np.outer(kal, h)
            Pz = G @ Pz @ G.T
            Pz[D:, D:] += np.outer(kal, kal) * r_i
            Pz[:D, D:] += 0.0  # measurement noise enters xhat only
            Pz = 0.5 * (Pz + Pz.T)
            # cross term x-xhat from v: E[x v] = 0, so only the xhat block
            # gains kal r kal' -- already added above; the x,xhat cross block
            # gains nothing from v.
    return eff / T_STEPS


def match_effort_analytic(A, B, Q, Qc, target, sched, S0):
    """Bisect rho so the ANALYTIC effort hits the ANALYTIC target."""
    def eff(rho):
        K = dare_gain(A, B, Qc, rho)
        return analytic_effort(A, B, Q, K, sched, S0), K
    lo, hi = 1e-3, 1.0
    e_hi, _ = eff(hi)
    while e_hi > target and hi < 1e6:
        hi *= 8
        e_hi, _ = eff(hi)
    best = (None, float("inf"), None)
    for _ in range(BISECT_ITERS):
        mid = np.sqrt(lo * hi)
        e, K = eff(mid)
        if abs(e - target) < best[1]:
            best = (mid, abs(e - target), K)
        if e > target:
            lo = mid
        else:
            hi = mid
    return best[0], best[2]


def run(n_sys, seed):
    rng = np.random.default_rng(seed)
    per_sys = []
    for _ in range(n_sys):
        A, Q, H, r = make_system(rng)
        B = rng.standard_normal((D, M_U)) / np.sqrt(D)
        S0 = steady_prior(A, Q)
        consumer = LinearConsumer(rng)
        P_C = consumer.true_pc()
        Phat, n_q = probe_read_operator(consumer, S0, rng)
        perm = rng.permutation(D)
        Pshuf, _ = probe_read_operator(consumer, S0, rng, perm=perm)
        Panti = anti_operator(Phat)
        charge = int(np.ceil(LAMBDA_P * n_q))
        reg = 1e-3 * np.eye(D)

        sched0 = precompute_schedule(A, Q, H, r, 0)
        schedC = precompute_schedule(A, Q, H, r, charge)
        K_ref = dare_gain(A, B, P_C + reg, 1.0)
        target = analytic_effort(A, B, Q, K_ref, sched0, S0)

        endpoint_noise = make_noise_bundles(rng, N_ENDPOINT_BUNDLES)
        eval_noise = make_noise_bundles(rng, N_TEST)

        diag_cands = [np.eye(D)] + [np.diag(rng.uniform(0.1, 2.0, size=D))
                                    for _ in range(DIAG_FAMILY - 1)]
        best_diag, best_val = None, float("inf")
        for Dc in diag_cands:
            _, K_d = match_effort_analytic(A, B, Q, Dc, target, sched0, S0)
            val = float(np.mean([rollout_cl(A, B, Q, H, r, consumer, K_d, 0, nb)[0]
                                 for nb in endpoint_noise]))
            if val < best_val:
                best_diag, best_val = Dc, val

        arms = {
            "oracle":   (P_C + reg, 0, sched0),
            "blind":    (Phat + reg, charge, schedC),
            "iso":      (np.eye(D), 0, sched0),
            "hand-diag": (best_diag, 0, sched0),
            "shuffled": (Pshuf + reg, charge, schedC),
            "anti":     (Panti + reg, charge, schedC),
        }
        row = {}
        for name, (Qc, charged, sched) in arms.items():
            rho, K = match_effort_analytic(A, B, Q, Qc, target, sched, S0)
            sr = float(max(abs(np.linalg.eigvals(A - B @ K))))
            an_eff = analytic_effort(A, B, Q, K, sched, S0)
            out = [rollout_cl(A, B, Q, H, r, consumer, K, charged, nb)
                   for nb in eval_noise]
            row[name] = {"loss": float(np.mean([o[0] for o in out])),
                         "loss_se": float(np.std([o[0] for o in out]) / np.sqrt(N_TEST)),
                         "effort": float(np.mean([o[1] for o in out])),
                         "analytic_effort": float(an_eff),
                         "xmax": float(max(o[2] for o in out)),
                         "rho": float(rho), "spec_radius": sr}
        row["_meta"] = {"n_queries": n_q, "charge_uses": charge,
                        "effort_target": float(target)}
        per_sys.append(row)
    return per_sys


VERDICT_ARMS = ("oracle", "blind", "iso", "hand-diag")


def metrics_from(per_sys):
    k1 = float(np.mean([(s["iso"]["loss"] - s["oracle"]["loss"]) / s["iso"]["loss"]
                        for s in per_sys]))
    g_bl = sum(s["iso"]["loss"] - s["blind"]["loss"] for s in per_sys)
    g_or = sum(s["iso"]["loss"] - s["oracle"]["loss"] for s in per_sys)
    k2 = float(g_bl / max(g_or, 1e-12))
    k3 = float(np.mean([(s["hand-diag"]["loss"] - s["oracle"]["loss"])
                        / s["hand-diag"]["loss"] for s in per_sys]))
    stable = all(s[a]["spec_radius"] < 1.0 for s in per_sys
                 for a in VERDICT_ARMS + ("shuffled", "anti"))
    bounded = all(s[a]["xmax"] < 1e3 for s in per_sys
                  for a in VERDICT_ARMS + ("shuffled", "anti"))
    spreads = []
    an_spreads = []
    for s in per_sys:
        effs = [s[a]["effort"] for a in VERDICT_ARMS]
        spreads.append((max(effs) - min(effs)) / max(np.mean(effs), 1e-12))
        aeffs = [s[a]["analytic_effort"] for a in VERDICT_ARMS]
        an_spreads.append((max(aeffs) - min(aeffs)) / max(np.mean(aeffs), 1e-12))
    spread_max = float(max(spreads))
    an_spread_max = float(max(an_spreads))   # instrument residual (bisection only)
    spread_ok = bool(spread_max <= FROZEN_SPREAD_BAND)
    m_anti = float(np.mean([s["anti"]["loss"] for s in per_sys]))
    m_or = float(np.mean([s["oracle"]["loss"] for s in per_sys]))
    m_iso = float(np.mean([s["iso"]["loss"] for s in per_sys]))
    anti_ok = bool(m_anti > m_or and m_anti >= m_iso - 0.02 * m_iso)
    shuf_gap = float(np.mean([s["shuffled"]["loss"] - s["iso"]["loss"] for s in per_sys]))
    return (k1, k2, k3, stable, bounded, spread_max, an_spread_max, spread_ok,
            anti_ok, shuf_gap)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()
    if args.calibrate:
        seed, n_sys, tag = 20260831, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} D={D} m_u={M_U} k={K_BUDGET} "
          f"T={T_STEPS} n_test={N_TEST} matching=ANALYTIC lambda_p={LAMBDA_P}")
    per_sys = run(n_sys, seed)
    (k1, k2, k3, stable, bounded, spread_max, an_spread_max, spread_ok,
     anti_ok, shuf_gap) = metrics_from(per_sys)
    print(f"K1 oracle vs iso: {k1:.3f}  (gate >= {FROZEN_DELTA_K1:.2f}, inherited)")
    print(f"K2 blind capture: {k2:.3f}  (gate >= {1 - FROZEN_EPS_K2:.2f}, inherited)")
    print(f"K3 oracle vs best hand-diag: {k3:.3f}  (gate >= {FROZEN_DELTA_K3:.2f}, inherited)")
    print(f"I2 cross-arm HELD-OUT effort spread (max over systems): {spread_max:.4f}  "
          f"(gate <= {FROZEN_SPREAD_BAND:.2f})")
    print(f"instrument residual: cross-arm ANALYTIC effort spread {an_spread_max:.5f} "
          f"(bisection precision only; should be ~0)")
    print(f"integrity: stable {stable}; bounded {bounded}")
    print(f"controls: shuffled-vs-iso {shuf_gap:+.4f}; anti ok: {anti_ok}")

    if args.calibrate:
        print("\n[CALIBRATION] freeze the spread band in the prereg, then seal.")
        return

    gates = {
        "K1_consumer_penalty_wins": k1 >= FROZEN_DELTA_K1,
        "K2_blind_capture": k2 >= 1 - FROZEN_EPS_K2,
        "K3_vs_hand_diag": k3 >= FROZEN_DELTA_K3,
        "I_stable": stable,
        "I_bounded": bounded,
        "I2_effort_spread": spread_ok,
        "C_shuffled_no_free_lunch": shuf_gap >= -0.02,
        "C_anti": anti_ok,
    }
    verdict = "ALL PASS" if all(gates.values()) else "FAIL"
    out = {
        "id": "PREREG-EC7-003", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_U": M_U, "K_BUDGET": K_BUDGET, "T_STEPS": T_STEPS,
                   "N_TEST": N_TEST, "N_ENDPOINT_BUNDLES": N_ENDPOINT_BUNDLES,
                   "BISECT_ITERS": BISECT_ITERS, "DIAG_FAMILY": DIAG_FAMILY,
                   "LAMBDA_P": LAMBDA_P, "delta_k1": FROZEN_DELTA_K1,
                   "eps_k2": FROZEN_EPS_K2, "delta_k3": FROZEN_DELTA_K3,
                   "spread_band": FROZEN_SPREAD_BAND},
        "per_system": per_sys,
        "metrics": {"K1": k1, "K2": k2, "K3": k3, "stable": stable,
                    "bounded": bounded, "spread_max": spread_max,
                    "analytic_spread_max": an_spread_max, "spread_ok": spread_ok,
                    "shuffled_gap": shuf_gap, "anti_ok": anti_ok},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "EC7C-closedloop.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
