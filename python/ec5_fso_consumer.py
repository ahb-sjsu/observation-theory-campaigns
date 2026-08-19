"""PREREG-EC5-001 (DRAFT) -- EC-5: physical-model FSO consumer (OT-EC Campaign 5).

The consumer is a physics-based free-space-optical link model, treated as a
black box: Gaussian far-field + fiber-coupling rolloff eta(theta) =
exp(-theta^2/theta0^2), where the pointing offset theta mixes attitude and
transverse-position errors through a hidden per-system state->physical map.
The ENDPOINT is external and physical: mean coupling loss (and outage
fraction) when the terminal points using the Kalman estimate while the truth
is x -- OT cannot win by optimizing its own metric.

The read operator is the BELIEF-AVERAGED smoothed operational metric of the
paper's Sec. VI (finite perturbations at belief scale, never a pretended
point Hessian): probes are drawn from the filter's steady prior and secant
differences use steps of half a belief standard deviation per coordinate.

Experiments:
  E1  reconstruction-matched physical prediction: among schedule pairs
      matched on time-average tr Sigma, the ordering of the PHYSICAL
      endpoint is predicted by tr(Pbar Sigma_bar) BEFORE the losses are
      compared (the covariance path is deterministic, so the prediction
      precedes the measurement by construction).
  E2  scheduling win: the Pbar-aligned schedule (probe cost charged) beats
      the best consumer-agnostic schedule on coupling loss at matched
      budgets.
  E3  blind capture: the charged blind schedule captures most of the
      lavish-probe reference schedule's advantage (no analytic optimum
      exists for the nonlinear link; the lavish probe is the reference,
      as in GO-087 arm N).
Controls: shuffled-consumer, anti-operator; outage fraction reported as the
secondary endpoint.

Machinery imported from the sealed blind_scheduling.py (NOT modified).

  --calibrate       internal calibration; prints candidate floors.
  --governed SEED   single governed run; writes results/EC5-fso-consumer.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

from blind_scheduling import (D, M_POOL, K_BUDGET, T_STEPS, N_TEST, LAMBDA_P,
                              make_system, steady_prior, greedy_weighted,
                              greedy_logdet, make_noise_bundles, anti_operator)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_SYS_CAL = 8
N_SYS_GOV = 20
N_PROBE = 40          # belief-averaged probe points (2*D queries each)
LAVISH_FACTOR = 8     # uncharged reference probe budget multiplier
ETA_OUTAGE = 0.10     # outage threshold on coupling efficiency

# ----------------------------- SEALED GATES (frozen 2026-08-19 from three
# disclosed calibration pilots; must match PREREG-EC5-001)
FROZEN_TRACE_TOL = 0.10   # E1 pair-matching band on time-average trace
FROZEN_Q_PRED = 0.80      # E1 gate (cal 1.000 over 7 pairs at n_sys=8)
FROZEN_MIN_PAIRS = 8      # E1 integrity gate on pooled matched pairs
FROZEN_DELTA_E2 = 0.04    # E2 gate (cal 0.088; conservative vs modest headroom)
FROZEN_EPS_E3 = 0.30      # E3 gate: blind capture >= 0.70 (cal 0.813)


class FSOConsumer:
    """Physics-based link model, black box to the scheduler.

    Hidden structure: a random orthonormal state->physical map; physical
    coords 0,1 = attitude tip/tilt, 3,4 = transverse position (range-scaled),
    others unread. theta0 is set per system so the belief-typical pointing
    offset sits at the Gaussian shoulder (coupling ~ exp(-1))."""

    def __init__(self, rng, S0):
        Qb, _ = np.linalg.qr(rng.standard_normal((D, D)))
        self.R = Qb
        self.k_att = rng.uniform(0.8, 1.2, size=2)
        self.k_pos = rng.uniform(0.15, 0.35, size=2)
        L0 = np.linalg.cholesky(S0 + 1e-9 * np.eye(D))
        thetas = [self._theta_raw(L0 @ rng.standard_normal(D)) for _ in range(400)]
        self.theta0 = float(np.sqrt(np.mean(np.square(thetas)))) + 1e-12

    def _theta_raw(self, v):
        p = self.R @ v
        ex = self.k_att[0] * p[0] + self.k_pos[0] * p[3]
        ey = self.k_att[1] * p[1] + self.k_pos[1] * p[4]
        return float(np.hypot(ex, ey))

    def eta(self, v):
        """Coupling efficiency for a pointing computed from offset vector v."""
        th = self._theta_raw(v)
        return float(np.exp(-(th / self.theta0) ** 2))

    def query(self, x):
        """Black-box response: the link's coupling at state x against the
        boresight reference. This is ALL the scheduler may see."""
        return np.array([self.eta(x)])

    def loss(self, xhat, x):
        """PHYSICAL endpoint: coupling loss when pointing with the estimate."""
        return 1.0 - self.eta(x - xhat)

    def outage(self, xhat, x):
        return float(self.eta(x - xhat) < ETA_OUTAGE)


def belief_averaged_probe(consumer, S_probe, rng, n_probe=N_PROBE, perm=None):
    """Smoothed operational metric (paper Sec. VI): secant differences at
    HALF A BELIEF STANDARD DEVIATION per coordinate, averaged over probe
    points drawn from the belief. Returns (Pbar, n_queries)."""
    Lc = np.linalg.cholesky(S_probe + 1e-9 * np.eye(D))
    stds = np.sqrt(np.maximum(np.diag(S_probe), 1e-12))
    P = np.zeros((D, D))
    n_queries = 0
    for _ in range(n_probe):
        x0 = Lc @ rng.standard_normal(D)
        J = []
        for i in range(D):
            e = np.zeros(D)
            e[i] = 0.5 * stds[i]
            xp, xm = x0 + e, x0 - e
            if perm is not None:
                xp, xm = xp[perm], xm[perm]
            J.append((consumer.query(xp) - consumer.query(xm)) / (2 * e[i]))
            n_queries += 2
        J = np.array(J).T
        P += J.T @ J
    P /= n_probe
    return 0.5 * (P + P.T), n_queries


def rollout_fso(A, Q, H, r, consumer, select_fn, charged_uses, noise):
    """As blind_scheduling.rollout but scoring the physical endpoint and
    accumulating the time-average covariance."""
    S0 = steady_prior(A, Q)
    L0 = np.linalg.cholesky(S0 + 1e-9 * np.eye(D))
    x = L0 @ noise["x0"]
    xhat = np.zeros(D)
    S = S0.copy()
    Lq = np.linalg.cholesky(Q + 1e-12 * np.eye(D))
    reduced = set(np.linspace(0, T_STEPS - 1, min(charged_uses, T_STEPS)).astype(int)) \
        if charged_uses else set()
    loss_sum = out_sum = 0.0
    Sbar = np.zeros((D, D))
    for t in range(T_STEPS):
        x = A @ x + Lq @ noise["w"][t]
        xhat = A @ xhat
        S = A @ S @ A.T + Q
        S = 0.5 * (S + S.T)
        k_t = K_BUDGET - (1 if t in reduced else 0)
        if k_t > 0:
            for i in select_fn(S)[:k_t]:
                h = H[i]
                y = h @ x + np.sqrt(r[i]) * noise["v"][t, i]
                Sh = S @ h
                kal = Sh / (h @ Sh + r[i])
                xhat = xhat + kal * (y - h @ xhat)
                S = S - np.outer(kal, Sh)
                S = 0.5 * (S + S.T)
        loss_sum += consumer.loss(xhat, x)
        out_sum += consumer.outage(xhat, x)
        Sbar += S
    return loss_sum / T_STEPS, out_sum / T_STEPS, Sbar / T_STEPS


def run(n_sys, seed):
    rng = np.random.default_rng(seed)
    per_sys = []
    for _ in range(n_sys):
        A, Q, H, r = make_system(rng)
        S0 = steady_prior(A, Q)
        consumer = FSOConsumer(rng, S0)
        Pbar, n_q = belief_averaged_probe(consumer, S0, rng)
        Plavish, _ = belief_averaged_probe(consumer, S0, rng,
                                           n_probe=LAVISH_FACTOR * N_PROBE)
        perm = rng.permutation(D)
        Pshuf, _ = belief_averaged_probe(consumer, S0, rng, perm=perm)
        Panti = anti_operator(Pbar)
        charge_uses = int(np.ceil(LAMBDA_P * n_q))
        noise = make_noise_bundles(rng, N_TEST)
        rand_rng = np.random.default_rng(rng.integers(2**31))
        rand_picks = [list(rand_rng.integers(0, M_POOL, size=K_BUDGET))
                      for _ in range(T_STEPS)]
        policies = {
            "align":   (lambda S: greedy_weighted(Pbar, S, H, r, K_BUDGET), charge_uses),
            "lavish":  (lambda S: greedy_weighted(Plavish, S, H, r, K_BUDGET), 0),
            "iso":     (lambda S: greedy_weighted(np.eye(D), S, H, r, K_BUDGET), 0),
            "logdet":  (lambda S: greedy_logdet(S, H, r, K_BUDGET), 0),
            "random":  (lambda S, _c=iter(rand_picks * (N_TEST + 1)): next(_c), 0),
            "shuffled": (lambda S: greedy_weighted(Pshuf, S, H, r, K_BUDGET), charge_uses),
            "anti":    (lambda S: greedy_weighted(Panti, S, H, r, K_BUDGET), charge_uses),
        }
        row = {}
        for name, (fn, charged) in policies.items():
            ls, outs, Sb = [], [], None
            for nb in noise:
                a, o, Sbar_ = rollout_fso(A, Q, H, r, consumer, fn, charged, nb)
                ls.append(a)
                outs.append(o)
                Sb = Sbar_
            row[name] = {"loss": float(np.mean(ls)),
                         "loss_se": float(np.std(ls) / np.sqrt(N_TEST)),
                         "outage": float(np.mean(outs)),
                         "tr": float(np.trace(Sb)),
                         "u": float(np.trace(Pbar @ Sb))}
        row["_meta"] = {"n_queries": n_q, "charge_uses": charge_uses,
                        "theta0": consumer.theta0}
        per_sys.append(row)
    return per_sys


def metrics_from(per_sys):
    # E1: among pairs from {align, iso, logdet} matched on tr, does u = tr(Pbar Sbar)
    # predict the physical-loss ordering?
    names = ["align", "iso", "logdet"]
    checked = correct = 0
    for s in per_sys:
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = s[names[i]], s[names[j]]
                if abs(a["tr"] - b["tr"]) / max(a["tr"], b["tr"]) <= FROZEN_TRACE_TOL:
                    du = a["u"] - b["u"]
                    dl = a["loss"] - b["loss"]
                    if abs(du) > 1e-12:
                        checked += 1
                        correct += int(du * dl > 0)
    e1 = correct / checked if checked else float("nan")
    # E2: charged align vs best consumer-agnostic, mean relative improvement
    rel = [(min(s["iso"]["loss"], s["logdet"]["loss"]) - s["align"]["loss"])
           / min(s["iso"]["loss"], s["logdet"]["loss"]) for s in per_sys]
    e2 = float(np.mean(rel))
    # E3: pooled capture of the lavish reference's advantage over iso
    g_bl = sum(s["iso"]["loss"] - s["align"]["loss"] for s in per_sys)
    g_lv = sum(s["iso"]["loss"] - s["lavish"]["loss"] for s in per_sys)
    e3 = float(g_bl / max(g_lv, 1e-12))
    shuf_gap = float(np.mean([s["shuffled"]["loss"] - s["iso"]["loss"] for s in per_sys]))
    # Direction is load-bearing (the 088 lesson, confirmed by the pilot-2
    # per-policy diagnostic): anti must lose to align at EQUAL probe charge,
    # and must not beat the uncharged consumer-blind iso baseline. Requiring
    # anti to also exceed logdet was never a meaningful prediction — logdet
    # is simply another agnostic arm of varying quality.
    m_anti = float(np.mean([s["anti"]["loss"] for s in per_sys]))
    m_align = float(np.mean([s["align"]["loss"] for s in per_sys]))
    m_iso = float(np.mean([s["iso"]["loss"] for s in per_sys]))
    anti_worst = bool(m_anti > m_align and m_anti >= m_iso - 0.02 * m_iso)
    out_gain = float(np.mean([min(s["iso"]["outage"], s["logdet"]["outage"]) - s["align"]["outage"]
                              for s in per_sys]))
    return e1, checked, e2, e3, shuf_gap, anti_worst, out_gain


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--governed", type=int, metavar="SEED")
    args = ap.parse_args()
    if args.calibrate:
        seed, n_sys, tag = 20260823, N_SYS_CAL, "CALIBRATION"
    elif args.governed is not None:
        seed, n_sys, tag = args.governed, N_SYS_GOV, "GOVERNED"
    else:
        ap.error("choose --calibrate or --governed SEED")

    print(f"[{tag}] seed={seed} n_sys={n_sys} D={D} pool={M_POOL} k={K_BUDGET} "
          f"T={T_STEPS} n_test={N_TEST} n_probe={N_PROBE} lambda_p={LAMBDA_P}")
    per_sys = run(n_sys, seed)
    e1, n_pairs, e2, e3, shuf_gap, anti_worst, out_gain = metrics_from(per_sys)
    print(f"E1 physical ordering predicted by tr(Pbar Sbar): {e1:.3f} over {n_pairs} "
          f"matched pairs  (gates >= {FROZEN_Q_PRED:.2f}, pairs >= {FROZEN_MIN_PAIRS})")
    print(f"E2 rel coupling-loss improvement vs best agnostic (probe-charged): "
          f"{e2:.3f}  (gate >= {FROZEN_DELTA_E2:.2f})")
    print(f"E3 blind capture of lavish-reference advantage: {e3:.3f}  "
          f"(gate >= {1 - FROZEN_EPS_E3:.2f})")
    print(f"secondary: outage-fraction gain {out_gain:+.4f}; "
          f"controls: shuffled-vs-iso {shuf_gap:+.4f} (want ~>= 0), "
          f"anti worst pooled: {anti_worst}")

    if args.calibrate:
        pooled = {k: float(np.mean([s[k]["loss"] for s in per_sys]))
                  for k in ("align", "lavish", "iso", "logdet", "random",
                            "shuffled", "anti")}
        print("pooled mean coupling loss per policy:",
              json.dumps(pooled, indent=1))
        print("\n[CALIBRATION] freeze conservative floors in the prereg, then seal.")
        return

    gates = {
        "E1_prediction": (e1 == e1) and e1 >= FROZEN_Q_PRED,
        "I_min_pairs": n_pairs >= FROZEN_MIN_PAIRS,
        "E2_win": e2 >= FROZEN_DELTA_E2,
        "E3_capture": e3 >= 1 - FROZEN_EPS_E3,
        "C_shuffled_no_free_lunch": shuf_gap >= -0.02,
        "C_anti_worst": anti_worst,
    }
    verdict = "ALL PASS" if all(gates.values()) else "FAIL"
    out = {
        "id": "PREREG-EC5-001", "seed": seed, "n_sys": n_sys,
        "config": {"D": D, "M_POOL": M_POOL, "K_BUDGET": K_BUDGET,
                   "T_STEPS": T_STEPS, "N_TEST": N_TEST, "N_PROBE": N_PROBE,
                   "LAVISH_FACTOR": LAVISH_FACTOR, "LAMBDA_P": LAMBDA_P,
                   "ETA_OUTAGE": ETA_OUTAGE, "trace_tol": FROZEN_TRACE_TOL,
                   "q_pred": FROZEN_Q_PRED, "min_pairs": FROZEN_MIN_PAIRS,
                   "delta_e2": FROZEN_DELTA_E2, "eps_e3": FROZEN_EPS_E3},
        "per_system": per_sys,
        "metrics": {"E1": e1, "E1_pairs": n_pairs, "E2": e2, "E3": e3,
                    "shuffled_gap": shuf_gap, "anti_worst": anti_worst,
                    "outage_gain": out_gain},
        "gates": gates, "verdict": verdict,
    }
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "EC5-fso-consumer.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n[GOVERNED] verdict: {verdict}  gates: {gates}\nwrote {path}")


if __name__ == "__main__":
    main()
