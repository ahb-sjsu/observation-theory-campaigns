"""PREREG-EC7-002 (DRAFT) -- EC-7 rehabilitation: closed-loop control, v2.

Successor to PREREG-EC7-001 (honest FAIL on its effort-matching integrity
gate; the predictions passed numerically but no comparison was claimed).
The registered flaw: 3-bundle effort matching under-powered per-system
transfer of the effort target to held-out rollouts -- deviations were
COMMON-MODE across arms (all four drifting together in 2/20 systems), so
within-system comparisons stayed fair while the absolute-target gate
failed. The principled fixes, per the designation in the EC track document:

  1. matching bundles 3 -> 8 (bisection 14 -> 12 iterations);
  2. the integrity gate is respecified to the fair-comparison quantity:
     CROSS-ARM EFFORT SPREAD on held-out rollouts -- per system, over the
     verdict arms, (max - min)/mean effort must sit inside a band.
     Absolute-target deviation is reported as a diagnostic, not gated.

All PREDICTION bars are inherited unchanged from the sealed EC7-001
(the rehabilitation fixes the instrument, never the claims): K1 >= 0.04,
K2 capture >= 0.60, K3 >= 0.00. Same arms, same charging, same audits.

Building blocks imported from the sealed ec7_closedloop.py (NOT modified).

  --calibrate       internal calibration; prints candidate spread band.
  --governed SEED   single governed run; writes results/EC7B-closedloop.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from blind_scheduling import (D, K_BUDGET, T_STEPS, N_TEST, LAMBDA_P,
                              make_system, steady_prior, make_noise_bundles,
                              probe_read_operator, anti_operator, LinearConsumer)
from ec7_closedloop import (M_U, DIAG_FAMILY, rollout_cl, mean_effort,
                            FROZEN_DELTA_K1, FROZEN_EPS_K2, FROZEN_DELTA_K3)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_SYS_CAL = 8
N_SYS_GOV = 20
N_CAL_BUNDLES_2 = 8   # fix 1: was 3 in EC7-001
BISECT_ITERS = 12

# ----------------------------- SEALED GATE (frozen 2026-08-19 from the
# calibration pilot; must match PREREG-EC7-002)
FROZEN_SPREAD_BAND = 0.15  # I2: cross-arm (max-min)/mean effort per system.
                           # Cal max 0.0853 over n=8 systems; this is a MAX
                           # statistic and the governed run has n=20, so the
                           # band is set at ~1.75x the calibration max rather
                           # than at the draft 0.10 it would have brushed.


def match_effort2(A, B, Q, H, r, consumer, Qc, target, cal_noise):
    """As ec7_closedloop.match_effort with the v2 iteration budget."""
    lo, hi = 1e-3, 1.0
    e_hi, _ = mean_effort(A, B, Q, H, r, consumer, Qc, hi, cal_noise)
    while e_hi > target and hi < 1e6:
        hi *= 8
        e_hi, _ = mean_effort(A, B, Q, H, r, consumer, Qc, hi, cal_noise)
    best = (None, float("inf"), None)
    for _ in range(BISECT_ITERS):
        mid = np.sqrt(lo * hi)
        e, K = mean_effort(A, B, Q, H, r, consumer, Qc, mid, cal_noise)
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

        cal_noise = make_noise_bundles(rng, N_CAL_BUNDLES_2)
        eval_noise = make_noise_bundles(rng, N_TEST)
        target, _ = mean_effort(A, B, Q, H, r, consumer, P_C + reg, 1.0, cal_noise)

        diag_cands = [np.eye(D)] + [np.diag(rng.uniform(0.1, 2.0, size=D))
                                    for _ in range(DIAG_FAMILY - 1)]
        best_diag, best_val = None, float("inf")
        for Dc in diag_cands:
            _, K_d = match_effort2(A, B, Q, H, r, consumer, Dc, target, cal_noise)
            val = float(np.mean([rollout_cl(A, B, Q, H, r, consumer, K_d, 0, nb)[0]
                                 for nb in cal_noise]))
            if val < best_val:
                best_diag, best_val = Dc, val

        arms = {
            "oracle":   (P_C + reg, 0),
            "blind":    (Phat + reg, charge),
            "iso":      (np.eye(D), 0),
            "hand-diag": (best_diag, 0),
            "shuffled": (Pshuf + reg, charge),
            "anti":     (Panti + reg, charge),
        }
        row = {}
        for name, (Qc, charged) in arms.items():
            rho, K = match_effort2(A, B, Q, H, r, consumer, Qc, target, cal_noise)
            sr = float(max(abs(np.linalg.eigvals(A - B @ K))))
            out = [rollout_cl(A, B, Q, H, r, consumer, K, charged, nb)
                   for nb in eval_noise]
            row[name] = {"loss": float(np.mean([o[0] for o in out])),
                         "loss_se": float(np.std([o[0] for o in out]) / np.sqrt(N_TEST)),
                         "effort": float(np.mean([o[1] for o in out])),
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
    # v2 integrity: cross-arm effort spread on held-out rollouts, per system
    spreads = []
    for s in per_sys:
        effs = [s[a]["effort"] for a in VERDICT_ARMS]
        spreads.append((max(effs) - min(effs)) / max(np.mean(effs), 1e-12))
    spread_max = float(max(spreads))
    spread_ok = bool(spread_max <= FROZEN_SPREAD_BAND)
    # diagnostic only (the EC7-001 gate, reported not gated):
    tgt_dev = float(max(abs(s[a]["effort"] - s["_meta"]["effort_target"])
                        / s["_meta"]["effort_target"]
                        for s in per_sys for a in VERDICT_ARMS))
    m_anti = float(np.mean([s["anti"]["loss"] for s in per_sys]))
    m_or = float(np.mean([s["oracle"]["loss"] for s in per_sys]))
    m_iso = float(np.mean([s["iso"]["loss"] for s in per_sys]))
    anti_ok = bool(m_anti > m_or and m_anti >= m_iso - 0.02 * m_iso)
    shuf_gap = float(np.mean([s["shuffled"]["loss"] - s["iso"]["loss"] for s in per_sys]))
    return k1, k2, k3, stable, bounded, spread_max, spread_ok, tgt_dev, anti_ok, shuf_gap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()
    if args.calibrate:
        seed, n_sys, tag = 20260829, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} D={D} m_u={M_U} k={K_BUDGET} "
          f"T={T_STEPS} n_test={N_TEST} cal_bundles={N_CAL_BUNDLES_2} "
          f"lambda_p={LAMBDA_P}")
    per_sys = run(n_sys, seed)
    (k1, k2, k3, stable, bounded, spread_max, spread_ok, tgt_dev,
     anti_ok, shuf_gap) = metrics_from(per_sys)
    print(f"K1 oracle vs iso (consumer endpoint, matched effort): {k1:.3f}  "
          f"(gate >= {FROZEN_DELTA_K1:.2f}, inherited)")
    print(f"K2 blind capture (probe-charged, pooled): {k2:.3f}  "
          f"(gate >= {1 - FROZEN_EPS_K2:.2f}, inherited)")
    print(f"K3 oracle vs best hand-diag: {k3:.3f}  (gate >= {FROZEN_DELTA_K3:.2f}, inherited)")
    print(f"I2 cross-arm effort spread (max over systems): {spread_max:.4f}  "
          f"(gate <= {FROZEN_SPREAD_BAND:.2f})")
    print(f"diagnostic (EC7-001's old gate, not gated here): max target dev {tgt_dev:.3f}")
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
        "id": "PREREG-EC7-002", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_U": M_U, "K_BUDGET": K_BUDGET, "T_STEPS": T_STEPS,
                   "N_TEST": N_TEST, "N_CAL_BUNDLES": N_CAL_BUNDLES_2,
                   "BISECT_ITERS": BISECT_ITERS, "DIAG_FAMILY": DIAG_FAMILY,
                   "LAMBDA_P": LAMBDA_P, "delta_k1": FROZEN_DELTA_K1,
                   "eps_k2": FROZEN_EPS_K2, "delta_k3": FROZEN_DELTA_K3,
                   "spread_band": FROZEN_SPREAD_BAND},
        "per_system": per_sys,
        "metrics": {"K1": k1, "K2": k2, "K3": k3, "stable": stable,
                    "bounded": bounded, "spread_max": spread_max,
                    "spread_ok": spread_ok, "target_dev_diagnostic": tgt_dev,
                    "shuffled_gap": shuf_gap, "anti_ok": anti_ok},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "EC7B-closedloop.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
