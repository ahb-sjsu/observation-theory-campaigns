"""DR-2 pilot: the staleness flip — freshness is consumer-relative.

Track: DR (experiments/DYNAMIC-RELEVANCE-TRACK.md §5, DR-2).
DISCLOSED CALIBRATION PILOT MODE unless run with `governed` (which
refuses to run until GATES are frozen at seal). Machinery imported from
the sealed `dr1_crossover.py` (unmodified — the EC-6 pattern).

The exhibit (per system)
------------------------
Same plant class and information sets as DR-1: arm A = OLD scalar
measurement of the slow mode, arm B = FRESH scalar measurement of the
fast mode. Age of information is a property of the HISTORIES alone:
every consumer, asked to rank the two sets by age, ranks B fresher.

Two planted rank-one consumers at FIXED CANONICAL angles — declared
here, before any system is drawn, identical across all systems
(anti-circularity: nothing is tuned to any system's crossover angle):

    C1: g1 = [cos 15°, sin 15°]   (reads mostly the slow mode)
    C2: g2 = [cos 75°, sin 75°]   (reads mostly the fast mode)

Directional staleness S_i(H) = g_i' Sigma_H g_i. The FLIP is the
two-consumer verdict inversion on the SAME pair of histories:

    S_1(A) < S_1(B)  and  S_2(A) > S_2(B)

— consumer 1 calls the OLD set fresher, consumer 2 calls the FRESH set
fresher, while AoI (consumer-blind) calls B fresher for both. Predicted
per system by the closed form (signs of g_i' D g_i, D = Sigma_A -
Sigma_B); measured on realized MC consumer losses L_i(H) =
mean((g_i' e_H)^2). This is EC-2's WHERE-flip transported to WHEN.

Pilot legs
----------
  F1 prediction coverage: fraction of systems where the closed form
     predicts the flip (both signs). Generator is NOT tuned to the
     canonical angles, so this calibrates attainable coverage.
  F2 measured | predicted: of predicted-flip systems, fraction where
     the realized-loss inversion holds (both inequalities).
  F3 effect size: pooled mean relative staleness gap
     min(|L_i(A)-L_i(B)|)/max(L_i(A),L_i(B)) over the two consumers in
     predicted-flip systems (the margin the flip rests on).
  F4 instrument: max relative analytic-vs-MC residual over both
     consumers, arms, systems.
  F5 isotropic null: the trace consumer produces NO inversion anywhere
     (it cannot — one number per history — recorded as the mechanism
     statement: without direction there is nothing to disagree about).

Usage:  python dr2_staleness_flip.py pilot1 [--nsys 20] [--nmc 200000] [--seed 20260910]
Writes: results/dr2-pilot1.json
"""

import argparse
import json
import pathlib

import numpy as np

from dr1_crossover import R_MEAS, draw_system, propagate, rollout_errors, scalar_update, steady_prior

THETA1_DEG = 15.0
THETA2_DEG = 75.0

# Frozen 2026-08-19 from disclosed pilot 1 (seed 20260910, 20 systems:
# flip predicted 20/20, measured 20/20, pooled min-rel-gap 0.395
# (smallest single 0.107), residual max 0.0106, null consistent). Bars
# set with margin BELOW pilot performance per PROTOCOL 5.1; sealed in
# PREREG-DR2-001.
GATES = {
    "F1_flip_predicted_fraction_min": 0.80,
    "F2_flip_measured_given_pred_min": 0.90,
    "F3_pooled_rel_gap_min": 0.10,
    "F4_residual_max": 0.02,
    "F5_null_inversions_max": 0,
}


def consumer_vectors():
    t1 = np.deg2rad(THETA1_DEG)
    t2 = np.deg2rad(THETA2_DEG)
    return np.array([np.cos(t1), np.sin(t1)]), np.array([np.cos(t2), np.sin(t2)])


def system_metrics(sysp, n_mc, rng):
    A = np.diag([sysp["a_slow"], sysp["a_fast"]])
    Q = np.diag([sysp["q_slow"], sysp["q_fast"]])
    e_slow = np.array([1.0, 0.0])
    e_fast = np.array([0.0, 1.0])
    g1, g2 = consumer_vectors()
    S_inf = steady_prior(A, Q)

    S_A = propagate(scalar_update(S_inf, e_slow, R_MEAS), A, Q, sysp["age_old"])
    S_B = propagate(scalar_update(S_inf, e_fast, R_MEAS), A, Q, sysp["age_fresh"])

    ana = {
        "S1_A": float(g1 @ S_A @ g1), "S1_B": float(g1 @ S_B @ g1),
        "S2_A": float(g2 @ S_A @ g2), "S2_B": float(g2 @ S_B @ g2),
    }
    flip_pred = bool(ana["S1_A"] < ana["S1_B"] and ana["S2_A"] > ana["S2_B"])

    e_A = rollout_errors(A, Q, e_slow, sysp["age_old"], n_mc, rng, S_inf)
    e_B = rollout_errors(A, Q, e_fast, sysp["age_fresh"], n_mc, rng, S_inf)
    C_A = e_A.T @ e_A / n_mc
    C_B = e_B.T @ e_B / n_mc
    mc = {
        "L1_A": float(g1 @ C_A @ g1), "L1_B": float(g1 @ C_B @ g1),
        "L2_A": float(g2 @ C_A @ g2), "L2_B": float(g2 @ C_B @ g2),
    }
    flip_meas = bool(mc["L1_A"] < mc["L1_B"] and mc["L2_A"] > mc["L2_B"])

    resid = max(
        abs(mc["L1_A"] - ana["S1_A"]) / ana["S1_A"],
        abs(mc["L1_B"] - ana["S1_B"]) / ana["S1_B"],
        abs(mc["L2_A"] - ana["S2_A"]) / ana["S2_A"],
        abs(mc["L2_B"] - ana["S2_B"]) / ana["S2_B"],
    )

    gap1 = abs(mc["L1_A"] - mc["L1_B"]) / max(mc["L1_A"], mc["L1_B"])
    gap2 = abs(mc["L2_A"] - mc["L2_B"]) / max(mc["L2_A"], mc["L2_B"])

    # F5: trace consumer — one number per history, orderings identical for
    # any consumer built on it; inversion is structurally impossible. We
    # still record the analytic-vs-MC trace ordering agreement.
    null_consistent = bool(
        np.sign(np.trace(C_A) - np.trace(C_B)) == np.sign(np.trace(S_A) - np.trace(S_B))
    )

    return {
        "system": sysp,
        "analytic": ana,
        "mc": mc,
        "flip_pred": flip_pred,
        "flip_meas": flip_meas,
        "min_rel_gap": float(min(gap1, gap2)),
        "residual": float(resid),
        "null_trace_ordering_consistent": null_consistent,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pilot1", "governed"])
    ap.add_argument("--nsys", type=int, default=20)
    ap.add_argument("--nmc", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.mode == "governed":
        if any(v is None for v in GATES.values()):
            raise SystemExit("GATES not frozen; refusing to run governed mode before seal.")
        if args.seed is None:
            raise SystemExit("governed mode requires the sealed --seed")
    seed = args.seed if args.seed is not None else 20260910

    rng = np.random.default_rng(seed)
    rows = []
    for i in range(args.nsys):
        sysp = draw_system(rng)
        child = np.random.default_rng(rng.integers(2**63))
        rows.append(system_metrics(sysp, args.nmc, child))
        r = rows[-1]
        print(f"sys {i:2d}: pred={r['flip_pred']} meas={r['flip_meas']} "
              f"min_gap={r['min_rel_gap']:.4f} resid={r['residual']:.4f}")

    pred = [r for r in rows if r["flip_pred"]]
    meas = [r for r in pred if r["flip_meas"]]
    agg = {
        "n_sys": args.nsys,
        "canonical_consumer_angles_deg": [THETA1_DEG, THETA2_DEG],
        "flip_predicted_fraction": len(pred) / args.nsys,
        "flip_measured_given_pred": (len(meas) / len(pred)) if pred else None,
        "pooled_min_rel_gap_pred_systems": (float(np.mean([r["min_rel_gap"] for r in pred])) if pred else None),
        "smallest_min_rel_gap": (float(np.min([r["min_rel_gap"] for r in pred])) if pred else None),
        "residual_max": float(np.max([r["residual"] for r in rows])),
        "null_trace_consistent_all": bool(all(r["null_trace_ordering_consistent"] for r in rows)),
    }

    verdicts = None
    if args.mode == "governed":
        verdicts = {
            "F1": agg["flip_predicted_fraction"] >= GATES["F1_flip_predicted_fraction_min"],
            "F2": (agg["flip_measured_given_pred"] or 0.0) >= GATES["F2_flip_measured_given_pred_min"],
            "F3": (agg["pooled_min_rel_gap_pred_systems"] or 0.0) >= GATES["F3_pooled_rel_gap_min"],
            "F4": agg["residual_max"] <= GATES["F4_residual_max"],
            "F5": agg["null_trace_consistent_all"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {
        "mode": args.mode,
        "disclosure": ("DISCLOSED CALIBRATION PILOT, not claim-bearing" if args.mode != "governed"
                       else "GOVERNED RUN against sealed GATES (PREREG-DR2-001)"),
        "seed": int(seed),
        "n_mc": int(args.nmc),
        "gates": GATES if args.mode == "governed" else None,
        "verdicts": verdicts,
        "aggregate": agg,
        "per_system": rows,
    }
    name = {"pilot1": "dr2-pilot1.json", "governed": "DR2-governed.json"}[args.mode]
    outp = pathlib.Path(__file__).resolve().parent.parent / "results" / name
    outp.write_text(json.dumps(out, indent=2))
    print(json.dumps({"aggregate": agg, "verdicts": verdicts}, indent=2))
    print(f"\nwritten: {outp}")


if __name__ == "__main__":
    main()
