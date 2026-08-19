# DR Track: Dynamic Relevance — the Age of Operationally Relevant Uncertainty

**Status:** Chip 🕒 DR. **ALL THREE CAMPAIGNS MEASURED, ALL PASS,
under seal, class `[predicted]`**: DR-1 the crossover exhibit
([`PREREG-DR1-001`](PREREG-DR1-001.md), `4a3a304`, seed 20260905, 7/7;
§8), DR-2 the staleness flip ([`PREREG-DR2-001`](PREREG-DR2-001.md),
`997c31f`, seed 20260915, 5/5; §9), DR-3 scheduling at matched budgets
([`PREREG-DR3-001`](PREREG-DR3-001.md), `b7ed62b`, seed 20260925, 6/6;
§11). The arc: the orderings disagree predictably (DR-1), consumers
disagree with each other (DR-2), and acting on the directional
ordering wins at matched cost (DR-3). Open: blind probe-charged arm,
random-delay channels, nonlinear plants (§12).

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

## 9. DR-2 governed result (ALL PASS 5/5, seed 20260915, class [predicted])

Sealed [`PREREG-DR2-001`](PREREG-DR2-001.md) at `997c31f` (SEALS row
`8ba572a`) after one disclosed pilot (seed 20260910: flip 20/20
predicted and measured, no design changes); harness
[`python/dr2_staleness_flip.py`](../python/dr2_staleness_flip.py)
importing the sealed DR-1 machinery unmodified; single governed run on
20 fresh draws ([`results/DR2-governed.json`](../results/DR2-governed.json)):

- **F1 coverage**: the closed form predicted the two-consumer flip in
  **19/20** systems (gate ≥ 80%). The 20th is an honest and priced
  outcome: the fixed 15°/75° canonical window did not straddle that
  system's crossover, the closed form said NO flip — and the
  measurement agreed. The prediction machinery was right in both
  directions.
- **F2 measurement**: realized-loss inversion in **19/19** predicted
  systems (gate ≥ 90%): consumer 1 found the OLD history fresher,
  consumer 2 the FRESH one, on identical data with identical AoI.
- **F3 margin**: pooled min relative staleness gap **0.388** (gate
  ≥ 0.10; smallest single system 0.056) — the flip rests on
  operationally large margins, not ties.
- **F4 instrument integrity**: max residual **0.0075** (gate ≤ 0.02).
- **F5 null**: trace orderings consistent in all 20 — a consumer-blind
  scalar cannot invert; direction is what disagrees.

The claim licensed at `[predicted]`: **freshness orderings are
consumer-relative** over the declared system class — no consumer-blind
freshness clock (AoI-style) can serve two consumers whose read
geometries straddle the crossover. WHERE (EC-2) and WHEN (DR-2) now
both flip.

## 10. DR-3 disclosed pilots (2026-08-19; harness
[`python/dr3_scheduling.py`](../python/dr3_scheduling.py))

Smart-sensor update scheduling (EC-4 idealization): exogenous 2-mode
plant (CRN exact across policies), monitor error e ← Ae + w between
transmissions, e ← 0 on transmit, consumer loss (gᵀe)² with θ_g ~
U[10°, 80°] per system; four causal policies at matched realized
budgets (β = 0.10; thresholds bisected on separate calibration
streams): periodic (≡ age-threshold here — deterministic channel),
isotropic ‖e‖² > τ, directional (gᵀe)² > τ, anti (g⊥ᵀe)² > τ.

- **Pilot 1** (seed 20260920, 20 systems,
  [`results/dr3-pilot1.json`](../results/dr3-pilot1.json)): pooled
  dir-over-iso **+19.5%** (positive in 20/20, range +0.1% to +61.5%),
  dir-over-periodic +66%, anti −33% pooled, budget spread max 0.55%
  absolute, half-sample stability 0.001. Pilot 1 SURFACED the angle
  structure: the advantage shrinks monotonically as g rotates toward
  the fast mode (where the isotropic trigger and the directional one
  converge). Disclosed design change: the Spearman correlation
  ρ(θ_g, improvement) added to the harness as metric D6.
- **Pilot 2** (seed 20260921, fresh draws, D6 active,
  [`results/dr3-pilot-seed20260921.json`](../results/dr3-pilot-seed20260921.json)):
  confirms — pooled dir-over-iso **+17.5%**, dir-over-periodic +65.8%,
  anti −37%, budget spread max 0.37%, half-sample 0.0004, **Spearman
  −0.872**. One system at θ_g = 71° measured dir/iso −0.4% — the
  near-coincidence regime, confirming the load-bearing form is POOLED
  improvement (the 088 lesson), never per-system positivity.

Calibration lessons for the seal: pooled dir-over-iso is the D1
quantity (bar must sit well below ~0.17–0.20); budget integrity
transfers at ≤ 0.6% absolute spread (D4 bar can sit at 2%); n_eval =
200 is stability-limited at 1e-3 (D5 bar 0.02 is conservative); the
angle structure is a sealable prediction (D6: ρ ≤ −0.5); the
structural null (P_C = I makes dir ≡ iso identically) is stated, not
measured.

## 11. DR-3 governed result (ALL PASS 6/6, seed 20260925, class [predicted])

Sealed [`PREREG-DR3-001`](PREREG-DR3-001.md) at `b7ed62b` (SEALS row
`23a719c`) after the two disclosed pilots; single governed run on 20
fresh systems ([`results/DR3-governed.json`](../results/DR3-governed.json)):

- **D1 (the claim)**: pooled relative consumer-loss improvement of the
  directional trigger over the best isotropic signal-aware policy at
  matched realized budgets: **+16.3%** (gate ≥ 8%), positive in 20/20
  systems (per-system range +0.1% to +49.2%).
- **D2 (context)**: **+65.3%** over periodic/age (gate ≥ 30%) — the
  anchor's expected result, not the novelty claim.
- **D3 anti-control**: triggering on the orthogonal component is
  **61.5% worse** than isotropic pooled — the advantage is
  direction-borne, in every system.
- **D4/D5 integrity**: budget spread max **0.58%** absolute (gate 2%);
  half-sample stability **0.0009** (gate 0.02). The instrument held.
- **D6 angle structure**: Spearman ρ(θ_g, improvement) = **−0.928**
  (gate ≤ −0.5) — the advantage shrinks exactly as predicted as the
  read direction rotates toward the noise-dominant mode, where the
  directional and isotropic triggers converge.

The operational claim licensed at `[predicted]`: **WHEN to spend an
update budget is consumer-relative** — at identical realized cost, the
schedule that watches the consumer's read direction beats the schedule
that watches error magnitude, by a margin with predictable geometric
structure, and the paper's boundary outcome (S_C as feature, not
policy) did NOT occur in this system class.

## 12. Open

- Blind probe-charged P̂_C arm (EC-track recovery machinery) capturing
  a preregistered fraction of the planted-consumer advantage — own seal.
- Random-delay channels (where the age-based line has its native
  force); multi-consumer update scheduling (DR × EC-6).
- Nonlinear plants / non-Gaussian posteriors; belief-averaged P̄_C
  triggers for cliff consumers (DR × Paper VIII §VI).
