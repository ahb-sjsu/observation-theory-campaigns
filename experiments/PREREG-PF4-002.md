# Preregistration PF4-002: axis discrimination with bars set against
model error

**Status:** SEALED.

**Registration ID:** PREREG-PF4-002

**Date sealed:** 2026-08-04

**Authorization:** sealed on the project owner's explicit instruction.
The sealing commit and blob hash are recorded in `experiments/SEALS.md`.
No field below may change; an edit voids the seal. The governed runner
is `python/pf4_prereg2_run.py`, committed at the sealing commit.

## The section 9.0 declaration

PF4-DESIGN section 9.0 requires any second attempt to either model the
two-variable exponent explicitly or set bars against model error, and
to declare which in writing before the preregistration exists. This
preregistration takes the second branch. The governed PREREG-PF4-001
run established that the effective-gap model's residual structure
exceeds binomial noise, so bars measured in binomial units test a
model that was never claimed. Here every bar is a ratio to the model's
own training inadequacy, so the claim tested is the one actually made,
that the effective-gap axis organizes and generalizes while the
Schwinger-shaped axis does not.

## Claim

In the declared Sauter-slab family (unchanged from PREREG-PF4-001),
with weighted least squares exactly as before,

(a) the effective-gap model G generalizes, meaning its held-out
weighted MSE is at most twice its training weighted MSE, and

(b) the Schwinger-shaped model S fails to compete, meaning its
held-out weighted MSE is at least twice model G's held-out weighted
MSE.

The claim PASSES iff both hold, is REFUTED iff MSE_S <= MSE_G on
held-out cells, and is otherwise neither-axis, reported with both
residual sets.

## Manifest (adaptive, probe-placed, disjoint from both prior runs)

- Training gaps P in {0.55, 0.75, 0.95}; held-out gaps P in
  {0.65, 0.85}. Disjoint from the pilot grid and from PREREG-PF4-001.
- Probe targets d/E in {0.22, 0.30, 0.38, 0.46}, bisected exactly as
  in the sealed PF4-001 runner, disjoint from its targets.
- Ensemble size 5 x 10^4 per cell, twenty cells, seeds from the
  committed formula. No importance sampling, no sequential analysis.

## Controls

Identical rules to PREREG-PF4-001: per-cell drift bar 1e-4, probe
under both prescriptions with |d_verlet - d_rk4| < 1e-3, zero-field
null, and post-training C3/C4 controls (RK4 and half-step) on the two
training cells with fractions nearest 0.01 and 0.1, each within z < 4.
Usable-cell rule and the minimum of three usable held-out cells carry
over; fewer is a manifest-design failure.

## Estimator

`python/pf4_prereg2_run.py` at the sealed commit, which reuses the
sealed PF4-001 machinery (cell placement, weighted fits, axes) and
changes only the grids above and the bar arithmetic of this document.

## Multiple-comparison and stopping rules

Fixed hierarchy, bar (a) then bar (b); fixed manifest; no sequential
analysis.

## Resource envelope

Single Atlas process in a named screen session, single-threaded BLAS,
two to three hours.

## Evidence record

One JSON record with all cells, probes, training and held-out fits and
MSEs, control outcomes, code commit, dependency versions, and SHA-256
hashes, appended to `results/`.

## Interpretation ceiling

A pass earns [demonstrated-in-model]: in this family the suppression
is organized by the effective-gap Gaussian axis in the precise sense
that the axis generalizes across gaps within its own accuracy class
while the Schwinger-shaped axis does not, which is the campaign's
disciplined negative for the Schwinger question in this family. It
licenses nothing about other families and nothing about physical pair
production, and the construction question, whether any family has a
non-measure-tail exponent, remains open.
