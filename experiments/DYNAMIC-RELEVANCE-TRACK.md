# DR Track: Dynamic Relevance — the Age of Operationally Relevant Uncertainty

**Status:** Chip 🕒 DR. **DR-1 measured — ALL PASS 7/7 under seal**
([`PREREG-DR1-001`](PREREG-DR1-001.md), sealed `4a3a304`, governed seed
20260905, class `[predicted]`; see §8). DR-2/DR-3 remain design-stage:
their thresholds are PENDING PILOT and no run may be sealed against
them until disclosed pilots fix them (PROTOCOL §5.1, power before
bars).

## 1. Question

Paper VIII (`geometric-observation/paper/ot-estimation-control.tex`,
§IX) states its third interface as an explicit conjecture: an
observation is stale when the uncertainty it leaves *in the consumer's
read directions* becomes operationally expensive,

    S_C(Δ) = tr[ P_C(t+Δ) · Σ(t+Δ | I_t) ],

age of information weighted by operational geometry rather than by the
clock. The track's question: does scheduling updates by **directional
staleness** beat the established freshness and signal-aware lines at
matched update budgets, on a held-out consumer endpoint — or does
long-horizon structure dominate, leaving S_C a feature rather than a
policy? The paper commits to either answer: the negative outcome "would
be a scientific boundary, not a failure to be patched."

## 2. Anchors (citations verified in the 2026-08-19 reference sweep)

- Sun, Polyanskiy, Uysal, *Sampling of the Wiener process for remote
  estimation over a channel with random delay*, IEEE Trans. Inf.
  Theory 66(2), 2020 — **signal-aware MSE-optimal sampling provably
  beats age-optimal sampling.** This is the anchor that disciplines the
  track's novelty claim (see below).
- Maatouk, Assaad, Ephremides, *The age of incorrect information*,
  IEEE Trans. Wireless Commun. 22(4), 2023 — AoII, semantics-aware
  freshness.
- Soleymani, Baras, Hirche (+ Johansson), *Value of information in
  feedback control: Quantification / Global optimality*, IEEE TAC
  67(7) 2022 / 68(6) 2023 — VoI-threshold triggering globally optimal
  for **multi-dimensional Gauss–Markov** processes under LQG cost.
  (NOT scalar-only; the sweep corrected our earlier characterization.)
- Paper VIII §IX: the prior-art sweep found **no anisotropic-staleness
  formulation** — freshness weighted by a consumer's read geometry,
  with the geometry recovered by probing, is the open conjunction.

**What the anchors force.** Because Sun et al. already beat age-based
scheduling with signal-aware sampling, *beating AoI is not a finding.*
The only claim this track may aim at is that **directional** staleness
(consumer geometry in the loop) beats BOTH the age-based line AND the
best isotropic signal-aware policy at matched update budgets — and
that the advantage disappears when the consumer's read geometry is
isotropic (that null is the control, not a failure).

## 3. Anti-circularity contract

Mirrors the EC track. Consumers may not be constructed so that
direction matters by fiat alone: every governed comparison carries a
probe-charged blind arm (P̂_C recovered by query-only probing, probe
cost λ_p per use), an isotropic-consumer null arm (predicted NO
advantage), and baselines implemented competently: age-optimal (AoI),
AoII, MSE-optimal signal-aware sampling (the Sun policy or its
discrete-time analogue), the VoI trigger where the LQG structure makes
it computable, periodic, and covariance-trace threshold. No threshold,
weighting, or feature tuned on confirmatory data. No schedule chosen
after seeing its error.

## 4. The claim, in three types, never conflated

**Instrument claim.** Under linear dynamics the whole comparison is
analytically instrumentable: Σ(t+Δ|I_t) propagates by Lyapunov
recursion, expected budgets and efforts by joint second-moment
propagation — the EC7-003 lesson (NEVER simulation-bisection; the
instrument residual is measured as its own diagnostic, ledger VI-13).

**Structural claim (the staleness flip).** Two consumers reading the
same plant through different geometries, identical update budgets and
identical AoI profiles, produce **opposite freshness orderings** of
the same observation history — WHEN complements EC-2's WHERE. Target
form: verdict inversion rate at matched budgets, bar PENDING PILOT.

**Operational claim.** S_C-greedy update scheduling beats every
baseline arm above on held-out consumer loss at matched realized
update budgets, blind arm probe-charged; and captures a preregistered
fraction of the true-operator (oracle P_C) advantage. Bars PENDING
PILOT. Inherits the EC-4 registered null: covariance-only triggers
collapse to quasi-periodic — the trigger must be signal- or
belief-aware, so S_C enters through the *realized* posterior, not the
open-loop covariance alone.

## 5. Candidate campaign designs

- **DR-1 (crossover exhibit, positive control).** Time-varying read
  direction P_C(t) rotating against anisotropic dynamics: the analytic
  case where age-ranking and S_C-ranking of two candidate updates
  provably cross. The crossover time is predicted before the run.
- **DR-2 (the staleness flip).** The structural claim above, planted
  orthogonal consumers first (clean case), EC-2 harness lineage.
- **DR-3 (scheduling at matched budgets).** The operational claim, all
  baseline arms, blind arm charged; the paper's stated boundary
  outcome (S_C as feature, not policy) is a registered possible
  verdict, reported at equal prominence.

## 6. Inherited instrument discipline (EC track lessons, binding here)

Common random numbers across policies; per-use probe charging (not
blackouts); x₀ drawn from the steady prior; analytic budget matching
wherever dynamics permit, residual measured; numpy bools cast before
json.dump; anti-controls specified in load-bearing pooled form;
single governed run per seal at a sealed seed, outcome recorded
regardless of sign.

## 7. Disclosed pilots

**Pilot 1 (2026-08-19, seed 20260819, n=200,000; harness
[`python/dr1_crossover.py`](../python/dr1_crossover.py), results
[`results/dr1-pilot1.json`](../results/dr1-pilot1.json)).** The DR-1
crossover exhibit in its minimal form: 2-mode plant (a = 0.999/0.97,
q = 0.0005/0.02), an OLD scalar measurement of the slow mode (age 30)
vs a FRESH one of the fast mode (age 5), read direction g(θ) swept
over [0, π/2].

- P2 crossover: exists and is predicted before rollout — θ*_pred =
  0.7684 rad from the closed form, θ*_meas = 0.7679 from 200k-rollout
  realized losses; gap 5.0e-4 rad, well inside one grid step
  (8.7e-3); exactly one sign change on the grid. The 6×-older
  observation wins at every θ below ≈44° — age ranks it stale, the
  read geometry does not.
- P1 instrument: analytic g'Σg vs Monte-Carlo realized loss, max
  relative residual 1.9e-3 (arm A) / 9.8e-3 (arm B) — consistent with
  MC scatter at this n; calibrates the residual bar for a future seal
  (a 1e-2-scale bar at n=2e5 would be scatter-limited, not
  instrument-limited; drive n up or bar down accordingly).
- P3 isotropic null: PASS — trace ordering constant across the grid,
  MC agrees with the analytic gap (+0.016). Remove direction, remove
  the effect.

Calibration lessons carried forward: the exhibit needs no dynamics
beyond diagonal 2-mode to exist; the closed-form θ* is grid-accurate
at n=2e5, so a DR-1 seal can put a tight bar on |θ*_pred − θ*_meas|;
arm-B residual scale sets the instrument-gate floor.

## 8. DR-1 governed result (ALL PASS 7/7, seed 20260905, class [predicted])

Sealed [`PREREG-DR1-001`](PREREG-DR1-001.md) at `4a3a304` (SEALS row
`b22ca45`) after the two disclosed pilots; single governed run on 20
fresh generator draws, n = 200,000 rollouts per arm
([`results/DR1-governed.json`](../results/DR1-governed.json)):

- **G1/G2 existence and measurement**: the closed form predicted a
  crossover in **20/20** systems (gate ≥ 80%) and **20/20** showed
  exactly one sign change of the realized loss difference (gate ≥ 90%).
- **G3 preregistered accuracy**: |θ*_pred − θ*_meas| median **0.665**
  grid steps (gate ≤ 1.5), max **1.435** (gate ≤ 4.0) — the crossing
  is predicted before any rollout to sub-degree accuracy.
- **G4 instrument integrity**: max analytic-vs-MC residual **0.0096**
  (gate ≤ 0.02) — the analytic instrument holds; no other gate needed
  its protection.
- **G5 isotropic null**: **0** trace-ordering flips in 20 (gate 0) —
  remove direction, remove the effect.
- **G6 age is wrong below the crossing**: the older observation's
  realized loss was lower on a nonempty part of the grid in **all 20**
  measured-crossover systems.

The track's vocabulary is licensed: age-based freshness and directional
staleness measurably disagree over a declared random system class, the
disagreement point is preregisterable in closed form, and the effect is
direction-borne. What this does NOT claim: any scheduling advantage
(DR-3's question, disciplined by the Sun–Polyanskiy–Uysal anchor).

## 9. Roadmap

DR-2 (the staleness flip) and DR-3 (scheduling at matched budgets):
disclosed calibration pilots → power analysis → freeze floors → seal →
single governed run each, same discipline as DR-1.
