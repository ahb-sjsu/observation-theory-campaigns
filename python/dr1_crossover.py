"""DR-1: the directional-staleness crossover exhibit.

Track: DR (experiments/DYNAMIC-RELEVANCE-TRACK.md).

Modes
-----
  pilot1   : the original single hand-built instance (disclosed pilot,
             2026-08-19, results/dr1-pilot1.json). Kept bit-reproducible.
  pilot2   : disclosed calibration of the RANDOM-SYSTEM generator
             (existence fraction, gap distribution, residual scale) --
             the inputs to freezing bars. NOT claim-bearing.
  governed : single governed run at the sealed seed against the GATES
             frozen in PREREG-DR1-001. Run once. Outcome recorded
             regardless of sign.

The exhibit (per system)
------------------------
Plant: x_{t+1} = A x_t + w, A = diag(a_slow, a_fast),
Q = diag(q_slow, q_fast), q_slow << q_fast. Two information sets about
the state at t = 0:
  arm A: scalar measurement along e_slow, AGE_OLD steps ago (OLD),
  arm B: scalar measurement along e_fast, AGE_FRESH steps ago (FRESH).
Age of information ranks B fresher at every read direction. A consumer
g(theta) = [cos theta, sin theta] has directional staleness
S_i(theta) = g' Sigma_i g; the ordering flips at

  tan^2 theta* = -D11 / D22,  D = Sigma_A - Sigma_B,  when D11 < 0 < D22,

computable in closed form BEFORE any rollout. Basis note: the generator
works in the mode frame WLOG -- rotating (A, Q, measurement directions,
consumer sweep plane) by a common orthogonal matrix is a change of
basis that leaves every number below identical, so a random rotation
would add generality in appearance only.

Random-system generator (frozen at seal; rng-driven per system)
---------------------------------------------------------------
  a_slow ~ U[0.995, 0.9995]   q_slow ~ U[2e-4, 1e-3]
  a_fast ~ U[0.90, 0.98]      q_fast ~ U[1e-2, 5e-2]
  AGE_OLD ~ int U[20, 40]     AGE_FRESH ~ int U[3, 8]
  r = 0.01 fixed              n_mc per arm: 200,000

Usage:
  python dr1_crossover.py pilot1  [--nmc 200000] [--seed 20260819]
  python dr1_crossover.py pilot2  [--nmc 200000] [--seed 20260820] [--nsys 20]
  python dr1_crossover.py governed --seed <sealed> [--nmc 200000] [--nsys 20]
"""

import argparse
import json
import pathlib

import numpy as np

R_MEAS = 0.01
N_THETA = 181  # grid over [0, pi/2]

# Frozen 2026-08-19 from disclosed pilot 2 (seed 20260820, 20 systems:
# existence 20/20, measured 20/20, gap median 0.70 / max 1.64 grid
# steps, residual max 0.0069, null flips 0). Bars set with margin BELOW
# pilot performance per PROTOCOL 5.1; sealed in PREREG-DR1-001.
GATES = {
    "G1_existence_fraction_min": 0.80,   # predicted-crossover systems / n_sys
    "G2_meas_crossover_fraction_min": 0.90,  # exactly-one-sign-change | predicted
    "G3_gap_median_max_grid_steps": 1.5,
    "G3_gap_max_max_grid_steps": 4.0,
    "G4_residual_max": 0.02,             # max rel analytic-vs-MC residual, any arm/system
    "G5_null_flips_max": 0,              # isotropic-consumer ordering flips
    "G6_old_wins_every_measured_crossover": True,  # bool gate
}


def steady_prior(A, Q):
    S = np.eye(2)
    for _ in range(20000):
        S = A @ S @ A.T + Q
    return S


def scalar_update(S, h, r):
    Sh = S @ h
    return S - np.outer(Sh, Sh) / (h @ Sh + r)


def propagate(S, A, Q, steps):
    for _ in range(steps):
        S = A @ S @ A.T + Q
    return S


def rollout_errors(A, Q, h, age, n_mc, rng, S_inf):
    """Monte-Carlo of the generative model: draw x at measurement time
    from the steady prior, observe along h, run the single-update
    posterior mean forward `age` steps against fresh process noise,
    return the error at t=0. Exact-linear, so errors are Gaussian with
    the analytic covariance -- this leg checks the HARNESS."""
    L_inf = np.linalg.cholesky(S_inf)
    Lq = np.linalg.cholesky(Q)
    x = rng.standard_normal((n_mc, 2)) @ L_inf.T
    y = x @ h + np.sqrt(R_MEAS) * rng.standard_normal(n_mc)
    kal = (S_inf @ h) / (h @ S_inf @ h + R_MEAS)
    e = x - np.outer(y, kal)  # prior mean 0 at steady state
    del x
    for _ in range(age):
        # e_{t+1} = A e_t + w: mean propagates by A, truth by A plus noise
        e = e @ A.T + rng.standard_normal((n_mc, 2)) @ Lq.T
    return e


def draw_system(rng):
    return {
        "a_slow": float(rng.uniform(0.995, 0.9995)),
        "a_fast": float(rng.uniform(0.90, 0.98)),
        "q_slow": float(rng.uniform(2e-4, 1e-3)),
        "q_fast": float(rng.uniform(1e-2, 5e-2)),
        "age_old": int(rng.integers(20, 41)),
        "age_fresh": int(rng.integers(3, 9)),
    }


def exhibit_metrics(sysp, n_mc, rng):
    A = np.diag([sysp["a_slow"], sysp["a_fast"]])
    Q = np.diag([sysp["q_slow"], sysp["q_fast"]])
    e_slow = np.array([1.0, 0.0])
    e_fast = np.array([0.0, 1.0])
    S_inf = steady_prior(A, Q)

    S_A = propagate(scalar_update(S_inf, e_slow, R_MEAS), A, Q, sysp["age_old"])
    S_B = propagate(scalar_update(S_inf, e_fast, R_MEAS), A, Q, sysp["age_fresh"])
    Dm = S_A - S_B

    exists_pred = bool(Dm[0, 0] < 0 < Dm[1, 1])
    theta_pred = float(np.arctan(np.sqrt(-Dm[0, 0] / Dm[1, 1]))) if exists_pred else None

    thetas = np.linspace(0.0, np.pi / 2, N_THETA)
    gs = np.stack([np.cos(thetas), np.sin(thetas)], axis=1)
    S_ana_A = np.einsum("ti,ij,tj->t", gs, S_A, gs)
    S_ana_B = np.einsum("ti,ij,tj->t", gs, S_B, gs)

    e_A = rollout_errors(A, Q, e_slow, sysp["age_old"], n_mc, rng, S_inf)
    e_B = rollout_errors(A, Q, e_fast, sysp["age_fresh"], n_mc, rng, S_inf)
    C_A = e_A.T @ e_A / n_mc
    C_B = e_B.T @ e_B / n_mc
    L_mc_A = np.einsum("ti,ij,tj->t", gs, C_A, gs)
    L_mc_B = np.einsum("ti,ij,tj->t", gs, C_B, gs)

    diff = L_mc_A - L_mc_B
    sc = np.where(np.diff(np.sign(diff)) != 0)[0]
    n_flips = int(len(sc))
    theta_meas = float(thetas[sc[0]]) if n_flips else None
    grid_step = float(thetas[1] - thetas[0])

    # isotropic null: trace ordering, analytic vs MC, no dependence on theta
    tr_gap = float(np.trace(Dm))
    null_flip = bool(np.sign(np.trace(C_A) - np.trace(C_B)) != np.sign(tr_gap))

    # does the OLD observation win somewhere (theta below the crossing)?
    old_wins_frac = float(np.mean(diff < 0))

    return {
        "system": sysp,
        "exists_pred": exists_pred,
        "theta_pred_rad": theta_pred,
        "theta_meas_rad": theta_meas,
        "n_sign_changes": n_flips,
        "gap_grid_steps": (abs(theta_pred - theta_meas) / grid_step
                           if (theta_pred is not None and theta_meas is not None) else None),
        "residual_A": float(np.max(np.abs(L_mc_A - S_ana_A) / S_ana_A)),
        "residual_B": float(np.max(np.abs(L_mc_B - S_ana_B) / S_ana_B)),
        "null_flip": null_flip,
        "old_wins_grid_fraction": old_wins_frac,
    }


def run_multi(mode, seed, n_sys, n_mc):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_sys):
        sysp = draw_system(rng)
        child = np.random.default_rng(rng.integers(2**63))
        rows.append(exhibit_metrics(sysp, n_mc, child))
        print(f"sys {i:2d}: pred={rows[-1]['exists_pred']} "
              f"flips={rows[-1]['n_sign_changes']} "
              f"gap={rows[-1]['gap_grid_steps'] if rows[-1]['gap_grid_steps'] is not None else '-'} "
              f"resid=({rows[-1]['residual_A']:.4f},{rows[-1]['residual_B']:.4f})")

    pred = [r for r in rows if r["exists_pred"]]
    meas = [r for r in pred if r["n_sign_changes"] == 1]
    gaps = [r["gap_grid_steps"] for r in meas]
    agg = {
        "n_sys": n_sys,
        "existence_fraction_pred": len(pred) / n_sys,
        "meas_crossover_fraction_given_pred": (len(meas) / len(pred)) if pred else None,
        "gap_median_grid_steps": float(np.median(gaps)) if gaps else None,
        "gap_max_grid_steps": float(np.max(gaps)) if gaps else None,
        "residual_max": float(np.max([max(r["residual_A"], r["residual_B"]) for r in rows])),
        "null_flips": int(sum(r["null_flip"] for r in rows)),
        "old_wins_in_every_measured_crossover": bool(all(r["old_wins_grid_fraction"] > 0 for r in meas)),
    }

    verdicts = None
    if mode == "governed":
        if any(v is None for v in GATES.values()):
            raise SystemExit("GATES not frozen; refusing to run governed mode before seal.")
        verdicts = {
            "G1": agg["existence_fraction_pred"] >= GATES["G1_existence_fraction_min"],
            "G2": (agg["meas_crossover_fraction_given_pred"] or 0.0) >= GATES["G2_meas_crossover_fraction_min"],
            "G3_median": (agg["gap_median_grid_steps"] is not None
                          and agg["gap_median_grid_steps"] <= GATES["G3_gap_median_max_grid_steps"]),
            "G3_max": (agg["gap_max_grid_steps"] is not None
                       and agg["gap_max_grid_steps"] <= GATES["G3_gap_max_max_grid_steps"]),
            "G4": agg["residual_max"] <= GATES["G4_residual_max"],
            "G5": agg["null_flips"] <= GATES["G5_null_flips_max"],
            "G6": agg["old_wins_in_every_measured_crossover"] == GATES["G6_old_wins_every_measured_crossover"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {
        "mode": mode,
        "disclosure": ("DISCLOSED CALIBRATION PILOT, not claim-bearing" if mode != "governed"
                       else "GOVERNED RUN against sealed GATES (PREREG-DR1-001)"),
        "seed": int(seed),
        "n_mc": int(n_mc),
        "gates": GATES if mode == "governed" else None,
        "verdicts": verdicts,
        "aggregate": agg,
        "per_system": rows,
    }
    name = {"pilot2": "dr1-pilot2.json", "governed": "DR1-governed.json"}[mode]
    outp = pathlib.Path(__file__).resolve().parent.parent / "results" / name
    outp.write_text(json.dumps(out, indent=2))
    print(json.dumps({"aggregate": agg, "verdicts": verdicts}, indent=2))
    print(f"\nwritten: {outp}")


def run_pilot1(seed, n_mc):
    # Original hand-built instance, kept verbatim for reproducibility of
    # results/dr1-pilot1.json (disclosed 2026-08-19).
    sysp = {"a_slow": 0.999, "a_fast": 0.97, "q_slow": 0.0005,
            "q_fast": 0.02, "age_old": 30, "age_fresh": 5}
    rng = np.random.default_rng(seed)
    child = np.random.default_rng(np.random.default_rng(seed + 1).integers(2**32))
    _ = rng  # pilot1's stream layout predates the multi-system runner
    m = exhibit_metrics(sysp, n_mc, child)
    print(json.dumps(m, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pilot1", "pilot2", "governed"])
    ap.add_argument("--nmc", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--nsys", type=int, default=20)
    args = ap.parse_args()

    if args.mode == "pilot1":
        run_pilot1(args.seed if args.seed is not None else 20260819, args.nmc)
    else:
        if args.mode == "governed" and args.seed is None:
            raise SystemExit("governed mode requires the sealed --seed")
        seed = args.seed if args.seed is not None else 20260820
        run_multi(args.mode, seed, args.nsys, args.nmc)


if __name__ == "__main__":
    main()
