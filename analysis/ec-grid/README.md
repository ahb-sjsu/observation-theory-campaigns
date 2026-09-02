# EC-grid — consumer-relative sensor value on a transmission network (UNSEALED, exploratory)

Owner idea 2026-09-02: the grid is a textbook OT system. The state estimator
answers "how uncertain is the grid state"; the operator's consumers (thermal
limits, stability interfaces, contingencies, protection) each read that
uncertainty through their own P_C. Paper VIII's rank-one value-of-observation
identity (Lean-verified in `geometric-observation/lean/`;
V_C = (gᵀΣh)²/(hᵀΣh+r)) makes sensor value consumer-relative. The empirical
question is topology-dependent, not algebraic: does a real network produce
sensors near-equal in classical value but far apart operationally?

## Shakedown (2026-09-02, `ec_grid_voi_shakedown.py`)

New England 39-bus, DC-linear WLS (49 base measurements: all injections
σ=0.05 + 10 seeded flows σ=0.02; state dim 38). 84 candidates (every branch
flow σ=0.01, every non-slack bus PMU angle σ=0.005). Consumers chosen
mechanically from the base case: thermal = max-|P| branch (45, |P|=8.51 pu),
interface = max-separation generator pair (buses 35–38), local contrast =
min-|P| branch (38).

Provenance note: GPG was unavailable at run time, so the pre-stated
predictions are hash-anchored instead of commit-anchored: the prediction
header was written before any run; uploads c5d79943… (original; pandapower
3.5.4 import bug, never produced numbers), de239d1c… (loader fix; grades
printed, JSON dump crashed), final (serialization fix only; identical grades).
The prediction text is byte-identical across all three.

**All five pre-stated predictions PASS:**

| prediction | bar | measured | verdict |
|---|---|---|---|
| P1 divergence | Spearman(Δtr, V_thermal) ≤ 0.5 | **0.144** | pass |
| P2 dissociation pair | Δtr within 10%, V ratio ≥ 5× | Δtr within 0.7%, ratio **~10⁸** (flow_45 vs pmu_7) | pass |
| P3 inversion | top-5 disjoint AND Spearman ≤ 0.5 | disjoint; **0.415** | pass |
| P4 MC validation | rank-one V_C within 5% of realized | **2.1%** (4000 draws) | pass |
| P5 isotropic control | Spearman(V_iso, Δtr) ≥ 0.999 | **1.000** | pass |

Honest notes:

- The P2 record pair's winner is the thermal line's own flow measurement — a
  legitimate sensor, and the point stands (classical Δtr calls pmu_7 its
  equal), but the **non-self secondary** is the stronger exhibit:
  **flow_33 vs pmu_2 — Δtr within 3.6% (the PMU's is higher), V_thermal ratio
  ≈ 1.5 × 10⁵.** Two sensors a covariance-trace planner cannot distinguish;
  one is worth five orders of magnitude more to the imminent-overload
  consumer.
- The inversion is structural, not statistical: the thermal top-5 is the
  corridor around branch 45 (flow_45/34/33/32, pmu_37); the interface top-5 is
  a disjoint corridor (flow_28/29/26/22/23). No sensor set is best for both
  consumers — sensor value has no observer-independent ranking on this
  network, same shape as the OT-UMAP diagonal dominance.
- P4 closes the loop from formula to realized downstream error: the rank-one
  identity predicts the Monte-Carlo consumer-error reduction within 2.1%.

## Prior-art delineation (before any novelty claim)

Optimal PMU placement (observability- and variance-based) is a large
literature, application-aware placement variants exist, and weighted-trace
objectives are established in sensor selection (Joshi–Boyd), scheduling, and
LQG co-design — Paper VIII cites these explicitly. The registered contribution
shape: (1) P_C derived from the downstream decision's own read, not chosen as
an engineering weight; (2) the measured classical/operational dissociation and
cross-consumer inversion on standard test cases; (3) the operational
false-clear endpoint (successor cell). A domain-specific prior-art pass
(PES placement literature) is a prereg-time item.

## Next cells

1. AC/nonlinear estimation with the **false-clear endpoint**: P(thermal
   violation missed | estimator cleared) under classical-optimal vs
   consumer-optimal sensor additions at matched budget — the operational
   number a PES reviewer can use.
2. Contingency consumers (post-outage flow reads; P_C changes with topology —
   the freshness/staleness beat: yesterday's optimal PMU set reads the wrong
   directions after a switching event).
3. Multi-sensor budgeted selection (greedy V_C vs greedy Δtr at k sensors).
4. Prereg with the V2 instrument (cross-fit where estimation enters; matched
   nulls; honest constants), then the PES paper.
