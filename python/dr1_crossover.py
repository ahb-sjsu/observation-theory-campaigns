"""DR-1 pilot: the directional-staleness crossover exhibit.

Track: DR (experiments/DYNAMIC-RELEVANCE-TRACK.md), design-draft stage.
THIS IS A DISCLOSED CALIBRATION PILOT, NOT A GOVERNED RUN. Nothing here
is claim-bearing; its outputs exist to calibrate bars for a future
PREREG-DR1-001 seal (PROTOCOL 5.1, power before bars).

The exhibit
-----------
Plant: x_{t+1} = A x_t + w,  A = diag(a_slow, a_fast),
Q = diag(q_slow, q_fast) with q_slow << q_fast. Two information sets
about the state at t = 0:

  I_A: a scalar measurement along e_slow taken AGE_A steps ago (OLD),
  I_B: a scalar measurement along e_fast taken AGE_B steps ago (FRESH),
       AGE_B < AGE_A.

Age of information ranks B fresher, always. A consumer reading
direction g(theta) = [cos theta, sin theta] has directional staleness
S_i(theta) = g' Sigma_i g. Because the slow mode holds information (low
q, a near 1), the OLD slow-mode measurement still dominates near
theta = 0, and the ordering flips at an angle theta* computable in
closed form from the two propagated covariances BEFORE any rollout:

  g'(Sigma_A - Sigma_B)g = 0  =>  tan^2 theta* = -D11 / D22,
  D = Sigma_A - Sigma_B   (valid when D11 < 0 < D22).

With a rotating consumer theta(t) = omega * t this is a crossover TIME
t* = theta*/omega: age-based freshness never flips, directional
staleness flips exactly once, at a preregisterable instant.

Pilot legs
----------
  P1 instrument: analytic S_i(theta) vs Monte-Carlo realized consumer
     loss mean((g'e_i)^2) under CRN rollouts of the full generative
     model; report max relative residual (EC7-003 lesson: the
     instrument is analytic; its residual is its own diagnostic).
  P2 crossover: theta*_pred (closed form) vs theta*_meas (sign change
     of the MC loss difference on a theta grid); report gap in grid
     steps and in radians.
  P3 isotropic null: P = I consumer; the trace ordering must NOT flip
     anywhere on the grid (directional relevance is the mechanism;
     remove direction, remove the effect).

Usage:  python dr1_crossover.py pilot1 [--nmc 200000] [--seed 20260819]
Writes: results/dr1-pilot1.json (pilot results are disclosed artifacts).
"""

import argparse
import json
import pathlib

import numpy as np

D = 2
A = np.diag([0.999, 0.97])
Q = np.diag([0.0005, 0.02])
R_MEAS = 0.01  # scalar measurement noise variance for both sets
AGE_A = 30    # slow-mode measurement age (OLD)
AGE_B = 5     # fast-mode measurement age (FRESH)
N_THETA = 181  # grid over [0, pi/2]


def steady_prior():
    S = np.eye(D)
    for _ in range(20000):
        S = A @ S @ A.T + Q
    return S


def scalar_update(S, h, r):
    Sh = S @ h
    return S - np.outer(Sh, Sh) / (h @ Sh + r)


def propagate(S, steps):
    for _ in range(steps):
        S = A @ S @ A.T + Q
    return S


def info_set_cov(h, age, S_inf):
    """Covariance at t=0 of the posterior given one scalar measurement
    along h taken `age` steps before t=0, prior at steady state."""
    return propagate(scalar_update(S_inf, h, R_MEAS), age)


def rollout_errors(h, age, n_mc, rng, S_inf):
    """CRN Monte-Carlo of the generative model: draw x at measurement
    time from the steady prior, observe, run the (single-update) Kalman
    posterior mean forward `age` steps with the true process noise, and
    return the error at t=0. Exact-linear model, so errors are Gaussian
    with the analytic covariance -- this leg checks the HARNESS, not
    the theorem."""
    L_inf = np.linalg.cholesky(S_inf)
    Lq = np.linalg.cholesky(Q)
    x = rng.standard_normal((n_mc, D)) @ L_inf.T
    y = x @ h + np.sqrt(R_MEAS) * rng.standard_normal(n_mc)
    S_post = scalar_update(S_inf, h, R_MEAS)
    kal = (S_inf @ h) / (h @ S_inf @ h + R_MEAS)
    m = np.outer(y, kal)  # prior mean is 0 at steady state
    e = x - m
    del x, m
    for _ in range(age):
        e = e @ A.T + rng.standard_normal((n_mc, D)) @ Lq.T
        # error propagates: e_{t+1} = A e_t + w (mean propagates by A,
        # true state by A + w; no further measurements)
    return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pilot1"])
    ap.add_argument("--nmc", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=20260819)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    S_inf = steady_prior()
    e_slow = np.array([1.0, 0.0])
    e_fast = np.array([0.0, 1.0])

    S_A = info_set_cov(e_slow, AGE_A, S_inf)
    S_B = info_set_cov(e_fast, AGE_B, S_inf)
    Dmat = S_A - S_B

    # --- predicted crossover (closed form, before any rollout) ---
    crossover_exists = bool(Dmat[0, 0] < 0 < Dmat[1, 1])
    theta_pred = float(np.arctan(np.sqrt(-Dmat[0, 0] / Dmat[1, 1]))) if crossover_exists else None

    thetas = np.linspace(0.0, np.pi / 2, N_THETA)
    gs = np.stack([np.cos(thetas), np.sin(thetas)], axis=1)
    S_ana_A = np.einsum("ti,ij,tj->t", gs, S_A, gs)
    S_ana_B = np.einsum("ti,ij,tj->t", gs, S_B, gs)

    # --- P1 instrument: Monte-Carlo realized losses ---
    # Arms use independent derived streams (strict CRN pairing is not
    # meaningful here: the arms differ in measurement direction AND
    # age, so their noise histories have different lengths).
    child = np.random.default_rng(args.seed + 1)
    e_A = rollout_errors(e_slow, AGE_A, args.nmc, np.random.default_rng(child.integers(2**32)), S_inf)
    e_B = rollout_errors(e_fast, AGE_B, args.nmc, np.random.default_rng(child.integers(2**32)), S_inf)
    # mean((g'e)^2) == g' C_emp g with C_emp the empirical second moment
    C_emp_A = e_A.T @ e_A / args.nmc
    C_emp_B = e_B.T @ e_B / args.nmc
    L_mc_A = np.einsum("ti,ij,tj->t", gs, C_emp_A, gs)
    L_mc_B = np.einsum("ti,ij,tj->t", gs, C_emp_B, gs)
    resid_A = float(np.max(np.abs(L_mc_A - S_ana_A) / S_ana_A))
    resid_B = float(np.max(np.abs(L_mc_B - S_ana_B) / S_ana_B))

    # --- P2 measured crossover from the MC losses ---
    diff = L_mc_A - L_mc_B
    sign_changes = np.where(np.diff(np.sign(diff)) != 0)[0]
    theta_meas = float(thetas[sign_changes[0]]) if len(sign_changes) else None
    n_flips = int(len(sign_changes))

    # --- P3 isotropic null: trace ordering must not flip ---
    tr_gap = float(np.trace(Dmat))
    mc_tr_A = float(np.mean(np.sum(e_A**2, axis=1)))
    mc_tr_B = float(np.mean(np.sum(e_B**2, axis=1)))
    null_flip = bool(np.sign(mc_tr_A - mc_tr_B) != np.sign(tr_gap))

    out = {
        "pilot": "DR1-pilot1 (disclosed calibration; NOT claim-bearing)",
        "seed": int(args.seed),
        "n_mc": int(args.nmc),
        "design": {
            "A": np.diag(A).tolist(),
            "Q": np.diag(Q).tolist(),
            "r_meas": R_MEAS,
            "age_old_slow": AGE_A,
            "age_fresh_fast": AGE_B,
        },
        "covariances": {
            "Sigma_A": S_A.tolist(),
            "Sigma_B": S_B.tolist(),
            "difference_diag": [float(Dmat[0, 0]), float(Dmat[1, 1])],
        },
        "P2_crossover": {
            "exists_analytically": crossover_exists,
            "theta_pred_rad": theta_pred,
            "theta_meas_rad": theta_meas,
            "n_sign_changes_on_grid": n_flips,
            "gap_rad": (abs(theta_pred - theta_meas) if (theta_pred is not None and theta_meas is not None) else None),
            "grid_step_rad": float(thetas[1] - thetas[0]),
        },
        "P1_instrument": {
            "max_rel_residual_arm_A": resid_A,
            "max_rel_residual_arm_B": resid_B,
        },
        "P3_isotropic_null": {
            "trace_gap_analytic": tr_gap,
            "mc_trace_A": mc_tr_A,
            "mc_trace_B": mc_tr_B,
            "ordering_flip_observed": null_flip,
        },
        "age_ordering": "B fresher than A at every theta by construction (ages 5 vs 30); age never flips",
    }

    outp = pathlib.Path(__file__).resolve().parent.parent / "results" / "dr1-pilot1.json"
    outp.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print(f"\nwritten: {outp}")


if __name__ == "__main__":
    main()
