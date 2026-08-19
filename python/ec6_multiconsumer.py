"""PREREG-EC6-001 (DRAFT) -- EC-6: multi-consumer state service (OT-EC Campaign 6).

When can one sensor schedule serve two consumers, and when does their
operational geometry force a MULTI-CONSUMER TAX? Two planted rank-3 linear
consumers whose read subspaces sit at a CONTROLLED principal angle
phi in {0, 30, 60, 90} degrees (same within-subspace weights, so the angle
is the only contrast). Policies at one matched budget:

  joint        greedy V_C on the scalarized (P1+P2)/2
  split        time-sharing: odd steps greedy on P1, even steps on P2
  dedicated-i  full budget on consumer i (the per-consumer UTOPIA -- what i
               would get with the whole budget to itself; infeasible for
               both at once, so it prices the sharing)
  iso, random  consumer-agnostic baselines

The tax at angle phi is the egalitarian service ratio

    tax(phi) = W_best-shared / W_utopia,
    W = max(loss_1, loss_2),  W_utopia = max(loss_1(ded-1), loss_2(ded-2)),

so tax >= 1 measures the price of sharing one budget across two geometries.
The two-observer coding theorem motivates the shape (nesting -> free
sharing; incompatibility -> tax) but is NOT imported as a result: the
campaign measures whether the dynamic analogue exists.

Predictions: M1 sharing near-free at phi=0; M2 tax rises with angle;
M3 a genuine tax exists at orthogonality; M4 consumer-aware shared policies
beat agnostic sharing at every angle. The joint-vs-split crossover by angle
is reported as exploratory, not gated.

No probing (planted consumers; the recovery question was Campaign 3's).
Machinery imported from the sealed blind_scheduling.py (NOT modified).

  --calibrate       internal calibration; prints candidate floors.
  --governed SEED   single governed run; writes results/EC6-multiconsumer.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from blind_scheduling import (D, M_POOL, K_BUDGET, T_STEPS, N_TEST,
                              make_system, steady_prior, greedy_weighted,
                              make_noise_bundles)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_SYS_CAL = 8
N_SYS_GOV = 20
ANGLES_DEG = (0, 30, 60, 90)

# ----------------------------- SEALED GATES (frozen 2026-08-19 from two
# disclosed calibration pilots; must match PREREG-EC6-001)
FROZEN_M1_BAND = 0.05     # M1 gate: tax(0) <= 1.05 (cal 1.0000 exactly)
FROZEN_M2_GAP = 0.05      # M2 gate: tax(90)-tax(0) >= 0.05 (cal 0.0950)
FROZEN_M3_TAX = 0.05      # M3 gate: tax(90) >= 1.05 (cal 1.0950)
FROZEN_M4_IMPR = 0.05     # M4: pooled mean relative W improvement of best-shared
                          #     over iso (per-cell fraction reported, not gated:
                          #     brittle near ties -- pilot-1 lesson)


class PairConsumer:
    """One of a controlled-angle pair: z = L x, rank 3."""

    def __init__(self, L):
        self.L = L

    def loss(self, xhat, x):
        d = self.L @ (xhat - x)
        return float(d @ d)

    def pc(self):
        return self.L.T @ self.L


def make_pair(rng, phi_deg):
    """Two rank-3 consumers whose read subspaces sit at principal angle
    phi (all three principal angles equal phi by construction), sharing the
    same within-subspace weights so the angle is the only contrast."""
    Qb, _ = np.linalg.qr(rng.standard_normal((D, D)))
    B1, W6 = Qb[:, 0:3], Qb[:, 3:6]          # base subspace and its partner
    phi = np.deg2rad(phi_deg)
    B2 = np.cos(phi) * B1 + np.sin(phi) * W6
    w = rng.uniform(0.5, 1.5, size=3)[:, None]
    return PairConsumer(w * B1.T), PairConsumer(w * B2.T)


def rollout_mc(A, Q, H, r, c1, c2, select_fn, noise):
    """Two-consumer rollout; select_fn(S, t) so time-sharing policies see
    the step index. CRN via the noise bundle."""
    S0 = steady_prior(A, Q)
    L0 = np.linalg.cholesky(S0 + 1e-9 * np.eye(D))
    x = L0 @ noise["x0"]
    xhat = np.zeros(D)
    S = S0.copy()
    Lq = np.linalg.cholesky(Q + 1e-12 * np.eye(D))
    l1 = l2 = 0.0
    for t in range(T_STEPS):
        x = A @ x + Lq @ noise["w"][t]
        xhat = A @ xhat
        S = A @ S @ A.T + Q
        S = 0.5 * (S + S.T)
        for i in select_fn(S, t):
            h = H[i]
            y = h @ x + np.sqrt(r[i]) * noise["v"][t, i]
            Sh = S @ h
            kal = Sh / (h @ Sh + r[i])
            xhat = xhat + kal * (y - h @ xhat)
            S = S - np.outer(kal, Sh)
            S = 0.5 * (S + S.T)
        l1 += c1.loss(xhat, x)
        l2 += c2.loss(xhat, x)
    return l1 / T_STEPS, l2 / T_STEPS


def run(n_sys, seed):
    rng = np.random.default_rng(seed)
    per_sys = []
    for _ in range(n_sys):
        A, Q, H, r = make_system(rng)
        noise = make_noise_bundles(rng, N_TEST)
        rand_rng = np.random.default_rng(rng.integers(2**31))
        rand_picks = [list(rand_rng.integers(0, M_POOL, size=K_BUDGET))
                      for _ in range(T_STEPS)]
        pair_rng_seed = int(rng.integers(2**31))
        sysrow = {}
        for phi in ANGLES_DEG:
            # same pair construction randomness at every angle: only phi varies
            c1, c2 = make_pair(np.random.default_rng(pair_rng_seed), phi)
            P1, P2 = c1.pc(), c2.pc()
            Pj = 0.5 * (P1 + P2)
            policies = {
                "joint": lambda S, t: greedy_weighted(Pj, S, H, r, K_BUDGET),
                "split": lambda S, t: greedy_weighted(P1 if t % 2 == 0 else P2,
                                                      S, H, r, K_BUDGET),
                "ded-1": lambda S, t: greedy_weighted(P1, S, H, r, K_BUDGET),
                "ded-2": lambda S, t: greedy_weighted(P2, S, H, r, K_BUDGET),
                "iso":   lambda S, t: greedy_weighted(np.eye(D), S, H, r, K_BUDGET),
                "random": (lambda S, t, _c=iter(rand_picks * (N_TEST + 1)): next(_c)),
            }
            arow = {}
            for name, fn in policies.items():
                L1s, L2s = [], []
                for nb in noise:
                    a, b = rollout_mc(A, Q, H, r, c1, c2, fn, nb)
                    L1s.append(a)
                    L2s.append(b)
                arow[name] = {"loss1": float(np.mean(L1s)),
                              "loss2": float(np.mean(L2s))}
            sysrow[str(phi)] = arow
        per_sys.append(sysrow)
    return per_sys


def W(cell):
    return max(cell["loss1"], cell["loss2"])


def metrics_from(per_sys):
    taxes = {phi: [] for phi in ANGLES_DEG}
    m4_hits = m4_tot = 0
    m4_rel = []
    ded1_gap, ded2_gap = [], []
    rnd_worst = True
    joint_wins = {phi: 0 for phi in ANGLES_DEG}
    for s in per_sys:
        for phi in ANGLES_DEG:
            a = s[str(phi)]
            w_utopia = max(a["ded-1"]["loss1"], a["ded-2"]["loss2"])
            w_shared = min(W(a["joint"]), W(a["split"]))
            taxes[phi].append(w_shared / max(w_utopia, 1e-12))
            m4_tot += 1
            m4_hits += int(w_shared < W(a["iso"]))
            m4_rel.append((W(a["iso"]) - w_shared) / W(a["iso"]))
            joint_wins[phi] += int(W(a["joint"]) <= W(a["split"]))
            # pooled dedicated sanity (greedy dominance is NOT a theorem;
            # per-cell strictness was the pilot-1 mis-specification)
            ded1_gap.append(a["joint"]["loss1"] - a["ded-1"]["loss1"])
            ded2_gap.append(a["joint"]["loss2"] - a["ded-2"]["loss2"])
            rnd_worst &= (W(a["random"]) >=
                          max(W(a["joint"]), W(a["split"]), W(a["iso"])) - 1e-9)
    tax_mean = {phi: float(np.mean(taxes[phi])) for phi in ANGLES_DEG}
    m1 = tax_mean[0]
    m2 = tax_mean[90] - tax_mean[0]
    m3 = tax_mean[90]
    m4 = float(np.mean(m4_rel))
    m4_frac = m4_hits / m4_tot
    ded_sane = bool(np.mean(ded1_gap) >= -1e-9 and np.mean(ded2_gap) >= -1e-9)
    return tax_mean, m1, m2, m3, m4, m4_frac, ded_sane, rnd_worst, \
        {str(k): v for k, v in joint_wins.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()
    if args.calibrate:
        seed, n_sys, tag = 20260825, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} D={D} pool={M_POOL} k={K_BUDGET} "
          f"T={T_STEPS} n_test={N_TEST} angles={ANGLES_DEG}")
    per_sys = run(n_sys, seed)
    tax_mean, m1, m2, m3, m4, m4_frac, ded_sane, rnd_worst, joint_wins = \
        metrics_from(per_sys)
    print("mean tax by angle:", json.dumps({str(k): round(v, 4) for k, v in tax_mean.items()}))
    print(f"M1 tax(0) = {m1:.4f}  (gate <= {1 + FROZEN_M1_BAND:.2f})")
    print(f"M2 tax(90) - tax(0) = {m2:.4f}  (gate >= {FROZEN_M2_GAP:.2f})")
    print(f"M3 tax(90) = {m3:.4f}  (gate >= {1 + FROZEN_M3_TAX:.2f})")
    print(f"M4 pooled rel W improvement of best-shared over iso: {m4:.3f}  "
          f"(gate >= {FROZEN_M4_IMPR:.2f}; per-cell fraction {m4_frac:.3f} reported)")
    print(f"exploratory joint-vs-split wins by angle (not gated): {joint_wins}")
    print(f"controls: dedicated sane (pooled): {ded_sane}; random worst on W: {rnd_worst}")

    if args.calibrate:
        print("\n[CALIBRATION] freeze conservative floors in the prereg, then seal.")
        return

    gates = {
        "M1_free_when_aligned": m1 <= 1 + FROZEN_M1_BAND,
        "M2_tax_rises": m2 >= FROZEN_M2_GAP,
        "M3_tax_at_orthogonal": m3 >= 1 + FROZEN_M3_TAX,
        "M4_geometry_beats_blind": m4 >= FROZEN_M4_IMPR,
        "C_dedicated_sane": ded_sane,
        "C_random_worst": rnd_worst,
    }
    verdict = "ALL PASS" if all(gates.values()) else "FAIL"
    out = {
        "id": "PREREG-EC6-001", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_POOL": M_POOL, "K_BUDGET": K_BUDGET,
                   "T_STEPS": T_STEPS, "N_TEST": N_TEST,
                   "angles_deg": list(ANGLES_DEG),
                   "m1_band": FROZEN_M1_BAND, "m2_gap": FROZEN_M2_GAP,
                   "m3_tax": FROZEN_M3_TAX, "m4_impr": FROZEN_M4_IMPR},
        "per_system": per_sys,
        "metrics": {"tax_mean": {str(k): v for k, v in tax_mean.items()},
                    "M1": m1, "M2": m2, "M3": m3, "M4": m4, "M4_frac": m4_frac,
                    "joint_wins_by_angle": joint_wins,
                    "dedicated_sane": ded_sane, "random_worst": rnd_worst},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "EC6-multiconsumer.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
