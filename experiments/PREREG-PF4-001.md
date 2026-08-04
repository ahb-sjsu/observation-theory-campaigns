# Preregistration PF4-001: the Sauter family follows the effective-gap
axis and excludes the Schwinger axis

**Status:** SEALED.

**Registration ID:** PREREG-PF4-001

**Date sealed:** 2026-08-04

**Authorization:** sealed on the project owner's explicit instruction.
The sealing commit and blob hash are recorded in `experiments/SEALS.md`.
No field below may change; an edit voids the seal. The governed runner
is `python/pf4_prereg_run.py`, committed at the sealing commit, which
takes every constant from this document.

## Claim

In the declared Sauter-slab family, the fluctuation-regime suppression
of time reversal is organized by the effective-gap Gaussian axis and
not by the Schwinger-shaped axis. Concretely, with d(P, E) the
deterministic minimum of the time momentum measured by the thermal-free
probe, and f the reversal fraction, the weighted linear model

-log f = alpha + beta (d/E)^2       (model G)

predicts held-out cells while the alternative

-log f = alpha' + beta' d^2/E      (model S)

does not, under the bars below. This is the campaign's disciplined
negative for this family: its exponent is a measure tail in the
effective gap, not the Schwinger form. The claim is refutable in both
directions, and a both-models-fail outcome is reportable as
neither-axis.

## Scope

The family, exactly as committed in `python/pf4_pilot.py` at the
sealing commit: H = p_t^2/2 + p_u^2/2 + omega_u^2 u^2/2 + lambda u^4/4
+ g E L tanh(t/L) u with omega_u = 1.2, lambda = 0.1, g = 0.25,
L = 3, T = 1, t(0) = -4L, thermal initialization in the shifted well,
velocity Verlet at dt = 1e-3, tau_max = 40, reversal meaning p_t <= 0
at any step. The pilot record `results/pf4-pilot.json` is exploratory
and superseded for claim purposes.

Closure-prescription compliance (PF4-DESIGN clauses): C1, all dynamics
integrated continuously; C2, the prescriptions are declared here; C3
and C4, controls below on verified-measurable cells; C5, the planted
Cayley trap is DEFERRED with justification, because this claim
compares axes within one declared continuous prescription rather than
asserting a rate value against an external target, and C3/C4 remain
active. Any later preregistration that claims a rate law against a
physical target must implement the full trap.

## Manifest (adaptive, probe-placed, deterministic)

The pilot showed fixed rectangular grids buy mostly bounds, so cells
are placed by the deterministic probe, which involves no ensemble and
no rate information.

- Gap values: training P in {0.5, 0.7, 0.9}; held-out P in
  {0.6, 0.8}. The held-out set is disjoint in P from training.
- For each P, four cells at probe targets d/E in
  {0.20, 0.28, 0.36, 0.44}, each E found by bisection of the probe on
  E in (0.05, 1.6) to tolerance 1e-3 in d/E. Twenty cells total.
- Ensemble size 5 x 10^4 per cell, seeds derived from the committed
  seed formula in the runner. No importance sampling.

## Primary outcome

Fit both models on the twelve training cells by weighted least squares
with binomial weights var(-log f) = (1 - f)/(f N). Predict the
held-out cells. With weighted mean squared prediction error MSE_G and
MSE_S over usable held-out cells, the claim PASSES iff

(a) MSE_G <= 4 (the G model predicts held-out cells within roughly
    twice the binomial scatter), and
(b) MSE_S >= 4 x MSE_G (the S model is decisively worse).

The claim is REFUTED iff MSE_S <= MSE_G. If neither passes nor
refutes, the outcome is neither-axis and is reported with both
residual sets.

## Secondary outcomes (cannot rescue the primary)

Fitted training slopes and intercepts of both models; the pilot
two-point prediction beta approximately 41 for model G; residual
structure against P, E, and d separately; the measured critical
manifold E_crit(P) from the probes.

## Instrument controls

All PEQO-FREEZE-002 bars where applicable, plus per cell: drift below
1e-4, deterministic probe run under both Verlet and RK4 with
|d_verlet - d_rk4| < 1e-3, zero-field null (no reversal at E = 0,
asserted). Prescription-pair and step-halving controls (C3/C4): after
the training cells complete, the two training cells with measured
fraction nearest 0.01 and 0.1 are re-run under RK4 at dt = 1e-3 and
under Verlet at dt = 5e-4; each must agree with its training fraction
within z < 4 pooled binomial standard errors. The pilot's vacuous-
control lesson is thereby closed: controls sit on cells verified
measurable before the controls run, by a rule fixed here.

## Estimator

The committed runner at the sealed commit. Usable cell: count >= 5,
fraction < 0.9, drift < 1e-4, probe sub-critical (d > 0). Weighted
least squares as above; MSE over usable held-out cells only.

## Falsification bar

Stated in the primary outcome. Bars may not move. If fewer than three
held-out cells are usable, the run is unevaluable and reported as a
manifest-design failure, not a pass or refutation.

## Missing-data rule

Every cell reports its count, including zeros; non-finite values void
the run under B6 of PEQO-FREEZE-002.

## Multiple-comparison rule

Fixed hierarchy: bar (a), then bar (b). One preregistered comparison.

## Stopping rule

Fixed manifest, fixed ensemble sizes, no sequential analysis.

## Resource envelope

Single Atlas process in a named screen session, single-threaded BLAS,
roughly two to three hours. No NRP objects. No thermal-relevant load.

## Evidence record

One JSON record with all cells, probes, fits, control outcomes, code
commit, dependency versions, and SHA-256 hashes, appended to
`results/` and never rewritten.

## Interpretation ceiling

A pass earns [demonstrated-in-model]: in this family, reversal
suppression is a Gaussian measure tail in the probe-measured effective
gap, and the Schwinger-shaped axis is excluded. It licenses no
statement about other families, nothing about physical pair
production, and it leaves the campaign's founding question, whether
any constructible family has a non-measure-tail exponent, open and
sharpened.
