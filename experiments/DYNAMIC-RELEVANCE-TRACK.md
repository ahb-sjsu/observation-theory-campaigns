# DR Track: Dynamic Relevance — the Age of Operationally Relevant Uncertainty

**Status:** design draft, unsealed, non-claim-bearing. Chip 🕒 DR.
No bar in this document is calibrated yet; every threshold below is
marked PENDING PILOT and no run may be sealed against it until a
disclosed pilot fixes it (PROTOCOL §5.1, power before bars).

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

## 7. Roadmap

Disclosed calibration pilots → power analysis → freeze floors → seal
(PREREG-DR1-001 naming, SEALS.md discipline, "Authorized by: A. H.
Bond (session instruction)") → single governed run each. Until a seal
exists, nothing in this document is claim-bearing.
