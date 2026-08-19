"""DR-3 pilot: directional-staleness scheduling at matched budgets.

Track: DR (experiments/DYNAMIC-RELEVANCE-TRACK.md §5, DR-3).
DISCLOSED CALIBRATION PILOT MODE unless run with `governed` (which
refuses to run until GATES are frozen at seal). Generator imported from
the sealed `dr1_crossover.py`.

The operational question, disciplined by its anchor
---------------------------------------------------
Signal-aware sampling already beats age-optimal sampling
(Sun-Polyanskiy-Uysal 2020), so beating periodic/age is NOT the claim.
The only admissible claim is DIRECTIONAL beats the best ISOTROPIC
signal-aware policy at matched realized budgets, on the consumer's
endpoint — plus the EC-style anti-control and a structural null.

Setting (smart-sensor update scheduling, EC-4 idealization)
-----------------------------------------------------------
Plant x_{t+1} = A x_t + w (exogenous — identical across policies, so
common random numbers are exact). A monitor holds x-hat: on transmit it
receives x exactly (e resets to 0); otherwise x-hat propagates open
loop, so the error obeys e <- A e + w. The sensor is smart: it knows
e_t before deciding. Consumer reads the monitor estimate through the
planted direction g (theta_g ~ U[10, 80] deg per system): per-step
consumer loss (g'e)^2 AFTER the decision.

Policies (all causal; thresholds bisected on SEPARATE calibration
trajectories to hit the target budget beta in expectation; realized
budgets reported and gated — the budget-integrity leg):
  periodic : transmit every k = round(1/beta) steps (== age-threshold
             here: the channel is deterministic, age == time since
             transmit, so an age threshold IS periodic. Recorded, not
             duplicated.)
  iso      : transmit when ||e||^2 > tau        (isotropic signal-aware)
  dir      : transmit when (g'e)^2 > tau        (directional staleness,
             realized-error form per the EC-4 registered null)
  anti     : transmit when (g_perp'e)^2 > tau   (anti-control; pooled
             load-bearing form per the 088 lesson: anti must NOT beat
             iso pooled)
Structural null, stated not measured: for an isotropic consumer
(P_C = I) the dir policy IS the iso policy — the advantage vanishes
identically by construction.

Pilot legs
----------
  P1 effect: pooled relative consumer-loss improvement of dir over iso
     at matched realized budgets (the load-bearing number), and dir
     over periodic (context).
  P2 budget integrity: max cross-policy spread of realized transmit
     fraction per system (calibration-to-evaluation transfer of the
     bisected thresholds — the EC-7 lesson zone; measured as its own
     diagnostic).
  P3 anti-control: anti does not beat iso pooled.
  P4 MC stability: half-sample agreement of the P1 pooled number (drop
     when < a few percent — sets n_eval for the seal).

Usage:  python dr3_scheduling.py pilot1 [--nsys 20] [--neval 200] [--seed 20260920]
Writes: results/dr3-pilot1.json
"""

import argparse
import json
import pathlib

import numpy as np

from dr1_crossover import draw_system

BETA = 0.10        # target transmit fraction
T_EVAL = 400       # counted steps per trajectory
T_BURN = 50        # burn-in steps (not counted)
N_CAL = 100        # calibration trajectories for threshold bisection
BISECT_ITERS = 45

GATES = {
    "D1_dir_vs_iso_pooled_min": None,
    "D2_dir_vs_periodic_pooled_min": None,
    "D3_anti_not_better_than_iso": None,
    "D4_budget_spread_max": None,
    "D5_residual_halfsample_max": None,
    "D6_spearman_theta_vs_impr_max": None,  # angle structure: advantage
    # shrinks as g rotates toward the fast mode (disclosed after pilot 1
    # surfaced the monotone structure; confirmed by pilot 2 before any
    # bar was frozen)
}


def make_noise(sysp, n_traj, rng):
    """Pre-draw the exogenous streams: initial error from the open-loop
    stationary law is approximated by burn-in from 0, so only w."""
    T = T_BURN + T_EVAL
    Lq = np.diag([np.sqrt(sysp["q_slow"]), np.sqrt(sysp["q_fast"])])
    return rng.standard_normal((T, n_traj, 2)) @ Lq.T


def simulate(sysp, g, policy, tau, w):
    """Run the error recursion under a policy. Returns (mean per-step
    consumer loss over counted steps, realized transmit fraction)."""
    A = np.diag([sysp["a_slow"], sysp["a_fast"]])
    g_perp = np.array([-g[1], g[0]])
    T, n, _ = w.shape
    k_per = max(1, round(1.0 / BETA))
    e = np.zeros((n, 2))
    loss = 0.0
    ntx = 0
    for t in range(T):
        if policy == "periodic":
            tx = np.full(n, (t - T_BURN) % k_per == 0) if t >= T_BURN else np.zeros(n, bool)
            if t < T_BURN and t % k_per == 0:
                tx = np.ones(n, bool)  # keep periodic cadence in burn-in
        elif policy == "iso":
            tx = np.einsum("ni,ni->n", e, e) > tau
        elif policy == "dir":
            tx = (e @ g) ** 2 > tau
        elif policy == "anti":
            tx = (e @ g_perp) ** 2 > tau
        else:
            raise ValueError(policy)
        e[tx] = 0.0
        if t >= T_BURN:
            loss += float(np.mean((e @ g) ** 2))
            ntx += int(np.sum(tx))
        e = e @ A.T + w[t]
    return loss / T_EVAL, ntx / (T_EVAL * n)


def bisect_threshold(sysp, g, policy, w_cal):
    """Monotone bisection of tau to hit BETA realized transmit fraction
    on the calibration streams."""
    lo, hi = 0.0, None
    # bracket: find hi with budget < BETA
    hi = 1.0
    for _ in range(60):
        _, b = simulate(sysp, g, policy, hi, w_cal)
        if b < BETA:
            break
        hi *= 4.0
    for _ in range(BISECT_ITERS):
        mid = 0.5 * (lo + hi)
        _, b = simulate(sysp, g, policy, mid, w_cal)
        if b > BETA:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def system_run(sysp, theta_g_deg, n_eval, rng):
    g = np.array([np.cos(np.deg2rad(theta_g_deg)), np.sin(np.deg2rad(theta_g_deg))])
    w_cal = make_noise(sysp, N_CAL, np.random.default_rng(rng.integers(2**63)))
    w_eval = make_noise(sysp, n_eval, np.random.default_rng(rng.integers(2**63)))

    res = {}
    for pol in ["periodic", "iso", "dir", "anti"]:
        tau = 0.0 if pol == "periodic" else bisect_threshold(sysp, g, pol, w_cal)
        loss, budget = simulate(sysp, g, pol, tau, w_eval)  # CRN: same w_eval
        # half-sample split for stability leg
        loss_h1, _ = simulate(sysp, g, pol, tau, w_eval[:, : n_eval // 2])
        loss_h2, _ = simulate(sysp, g, pol, tau, w_eval[:, n_eval // 2 :])
        res[pol] = {"tau": float(tau), "loss": loss, "budget": budget,
                    "loss_h1": loss_h1, "loss_h2": loss_h2}

    budgets = [res[p]["budget"] for p in res]
    return {
        "system": sysp,
        "theta_g_deg": float(theta_g_deg),
        "policies": res,
        "rel_impr_dir_vs_iso": float(1.0 - res["dir"]["loss"] / res["iso"]["loss"]),
        "rel_impr_dir_vs_periodic": float(1.0 - res["dir"]["loss"] / res["periodic"]["loss"]),
        "rel_anti_vs_iso": float(1.0 - res["anti"]["loss"] / res["iso"]["loss"]),
        "budget_spread": float(max(budgets) - min(budgets)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pilot1", "governed"])
    ap.add_argument("--nsys", type=int, default=20)
    ap.add_argument("--neval", type=int, default=200)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.mode == "governed":
        if any(v is None for v in GATES.values()):
            raise SystemExit("GATES not frozen; refusing to run governed mode before seal.")
        if args.seed is None:
            raise SystemExit("governed mode requires the sealed --seed")
    seed = args.seed if args.seed is not None else 20260920

    rng = np.random.default_rng(seed)
    rows = []
    for i in range(args.nsys):
        sysp = draw_system(rng)
        theta_g = float(rng.uniform(10.0, 80.0))
        rows.append(system_run(sysp, theta_g, args.neval, rng))
        r = rows[-1]
        print(f"sys {i:2d}: theta_g={r['theta_g_deg']:5.1f}  "
              f"dir/iso {r['rel_impr_dir_vs_iso']:+.4f}  "
              f"dir/per {r['rel_impr_dir_vs_periodic']:+.4f}  "
              f"anti/iso {r['rel_anti_vs_iso']:+.4f}  "
              f"bspread {r['budget_spread']:.4f}")

    # pooled = mean of per-system relative improvements
    pooled_di = float(np.mean([r["rel_impr_dir_vs_iso"] for r in rows]))
    pooled_dp = float(np.mean([r["rel_impr_dir_vs_periodic"] for r in rows]))
    pooled_ai = float(np.mean([r["rel_anti_vs_iso"] for r in rows]))
    # half-sample stability of the pooled dir/iso number
    h1 = float(np.mean([1.0 - r["policies"]["dir"]["loss_h1"] / r["policies"]["iso"]["loss_h1"] for r in rows]))
    h2 = float(np.mean([1.0 - r["policies"]["dir"]["loss_h2"] / r["policies"]["iso"]["loss_h2"] for r in rows]))
    # D6 angle structure: rank correlation between the consumer angle
    # (distance from the slow mode) and the dir-over-iso improvement.
    def _ranks(v):
        return np.argsort(np.argsort(v)).astype(float)
    thetas_g = np.array([r["theta_g_deg"] for r in rows])
    imprs = np.array([r["rel_impr_dir_vs_iso"] for r in rows])
    spearman = float(np.corrcoef(_ranks(thetas_g), _ranks(imprs))[0, 1])

    agg = {
        "n_sys": args.nsys, "n_eval": args.neval, "beta_target": BETA,
        "pooled_rel_impr_dir_vs_iso": pooled_di,
        "pooled_rel_impr_dir_vs_periodic": pooled_dp,
        "pooled_rel_anti_vs_iso": pooled_ai,
        "dir_beats_iso_systems": int(sum(r["rel_impr_dir_vs_iso"] > 0 for r in rows)),
        "budget_spread_max": float(np.max([r["budget_spread"] for r in rows])),
        "halfsample_pooled_dir_vs_iso": [h1, h2],
        "halfsample_abs_diff": abs(h1 - h2),
        "spearman_theta_vs_impr": spearman,
    }

    verdicts = None
    if args.mode == "governed":
        verdicts = {
            "D1": pooled_di >= GATES["D1_dir_vs_iso_pooled_min"],
            "D2": pooled_dp >= GATES["D2_dir_vs_periodic_pooled_min"],
            "D3": pooled_ai <= 0.0 if GATES["D3_anti_not_better_than_iso"] else True,
            "D4": agg["budget_spread_max"] <= GATES["D4_budget_spread_max"],
            "D5": agg["halfsample_abs_diff"] <= GATES["D5_residual_halfsample_max"],
            "D6": agg["spearman_theta_vs_impr"] <= GATES["D6_spearman_theta_vs_impr_max"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {
        "mode": args.mode,
        "disclosure": ("DISCLOSED CALIBRATION PILOT, not claim-bearing" if args.mode != "governed"
                       else "GOVERNED RUN against sealed GATES (PREREG-DR3-001)"),
        "seed": int(seed),
        "gates": GATES if args.mode == "governed" else None,
        "verdicts": verdicts,
        "aggregate": agg,
        "per_system": rows,
    }
    name = ("DR3-governed.json" if args.mode == "governed"
            else f"dr3-pilot-seed{seed}.json")
    outp = pathlib.Path(__file__).resolve().parent.parent / "results" / name
    outp.write_text(json.dumps(out, indent=2))
    print(json.dumps({"aggregate": agg, "verdicts": verdicts}, indent=2))
    print(f"\nwritten: {outp}")


if __name__ == "__main__":
    main()
