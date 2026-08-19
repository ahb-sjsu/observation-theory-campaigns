# PREREG-DR3-001 — DR-3: directional-staleness scheduling at matched budgets

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

The DR track's operational campaign (experiments/DYNAMIC-RELEVANCE-TRACK.md
§5, DR-3), disciplined by its anchor: signal-aware sampling already beats
age-optimal sampling (Sun–Polyanskiy–Uysal, IEEE T-IT 66(2), 2020), so
beating periodic/age is context, not the claim. The sealed claim: a
**directional** trigger — transmit when the realized error in the
consumer's read direction (gᵀe)² exceeds a threshold — beats the best
**isotropic signal-aware** policy (transmit when ‖e‖² exceeds a
threshold) on pooled held-out consumer loss at matched realized transmit
budgets; the advantage has the predicted **angle structure** (it shrinks
as the read direction rotates toward the noise-dominant fast mode, where
the two triggers converge); and the anti-control (triggering on the
orthogonal component) is not better than isotropic. On pass, class
`[predicted]`: WHEN to spend an update budget is consumer-relative in the
operational sense, completing the DR arc (DR-1: the orderings disagree
predictably; DR-2: consumers disagree with each other; DR-3: acting on
the directional ordering wins at matched cost).

## Design

Harness `python/dr3_scheduling.py`, governed mode; generator imported
unmodified from the sealed `dr1_crossover.py`. Smart-sensor update
scheduling (the EC-4 idealization): exogenous 2-mode plant — the state
stream is independent of transmissions, so common random numbers are
EXACT across policies; monitor error e ← Ae + w between transmissions,
e ← 0 on transmit; consumer loss (gᵀe)² per step after the decision,
θ_g ~ U[10°, 80°] per system. 20 fresh systems, β = 0.10 target budget,
T = 400 counted steps (+50 burn-in), n_eval = 200 CRN trajectories per
system, thresholds bisected on 100 SEPARATE calibration trajectories.
Per the EC-4 registered null, the trigger statistics are realized-error
(signal-aware) quantities, not open-loop covariances. Budget integrity
(D4) and Monte-Carlo stability (D5) are integrity gates in the EC7-003
sense: on their failure no comparison gate is interpreted.

Structural null, stated not measured: for an isotropic consumer
(P_C = I) the directional policy IS the isotropic policy — the
advantage vanishes identically by construction.

## Two disclosed calibration pilots

1. **Pilot 1** (seed 20260920, `results/dr3-pilot1.json`): pooled
   dir-over-iso +19.5% (20/20 positive), dir-over-periodic +66%, anti
   −33%, budget spread max 0.55% absolute, half-sample 0.001. Surfaced
   the monotone angle structure; disclosed design change: Spearman
   ρ(θ_g, improvement) added as metric D6.
2. **Pilot 2** (seed 20260921, fresh draws, D6 active,
   `results/dr3-pilot-seed20260921.json`): +17.5% pooled, Spearman
   −0.872, anti −37%, budget spread 0.37%, half-sample 0.0004; one
   near-coincidence system at −0.4% confirming POOLED improvement as
   the load-bearing form (the 088 lesson). No further design changes.

```yaml
id: PREREG-DR3-001
date: 2026-08-19
retrospective: false
kind: directional vs isotropic signal-aware update scheduling at matched
      realized budgets (DR-3, operational claim); smart-sensor
      idealization, planted consumers, exogenous-plant exact CRN
harness: python/dr3_scheduling.py
code_hash: sha256:c1de84d867d4fd46cf8663dcf3fd1efe775f68d87fb6469f7e4244d600c8c3ca
imports_sealed: python/dr1_crossover.py (PREREG-DR1-001,
      code_hash sha256:caeb9f4141982bb5a37228247ace8a8c5b26ad007401765934b160e1004c292a)
governed_seed: 20260925
calibration_seeds: [20260920, 20260921]
frozen_config:
  n_sys: 20
  n_eval: 200
  beta_target: 0.10
  t_eval: 400
  t_burn: 50
  n_cal: 100
  theta_g_range_deg: [10, 80]
  generator: inherited from PREREG-DR1-001 (identical ranges)
sealed_gates:
  D1: pooled relative consumer-loss improvement of directional over
      isotropic signal-aware at matched budgets >= 0.08 (cal 0.195/0.175)
  D2: pooled improvement over periodic/age >= 0.30 (cal 0.66; context,
      not the novelty claim)
  D3: anti-control not better than isotropic, pooled (cal -0.33/-0.37)
  D4: budget integrity - max cross-policy realized transmit-fraction
      spread <= 0.02 absolute (cal 0.0055/0.0037); integrity gate: on
      failure NO comparison gate is interpreted
  D5: MC stability - half-sample split of the pooled D1 number agrees
      to <= 0.02 (cal 0.001/0.0004); integrity gate as D4
  D6: angle structure - Spearman rho(theta_g, dir-over-iso improvement)
      <= -0.5 (cal -0.872)
stopping: fixed-n, single governed run
falsification: D1 fail -> directional staleness does not beat honest
  isotropic signal-aware scheduling at matched cost; per the track's
  own anchor discipline this is the BOUNDARY OUTCOME the paper commits
  to honoring - S_C remains a feature, not a policy; reported as the
  campaign's answer. D2 fail -> the signal-aware family itself failed
  here (would contradict the anchor; investigate instrument first).
  D3 fail -> the advantage is not direction-borne. D4/D5 fail ->
  instrument integrity broken, no comparison claimed (EC-7 discipline).
  D6 fail -> the advantage exists but lacks the predicted geometric
  structure; the mechanism story is wrong even if the win is real.
  All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Planted known consumers; the blind probe-charged P̂_C arm is a designated
FUTURE seal (EC-track machinery), not part of this claim. Smart-sensor
idealization (exact-state transmission, deterministic channel — hence
age ≡ periodic here); random-delay channels, where the age-based line
has its native force, are future work. Exact-linear plant; no
optimality claim for any threshold policy (all four are matched-budget
heuristics); no claim that the directional trigger is the optimal
directional policy.
