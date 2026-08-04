# Preregistration QO3-001: quantifier activation on a fresh coupling grid

**Status:** SEALED.

**Registration ID:** PREREG-QO3-001

**Date sealed:** 2026-08-04

**Authorization:** sealed on the project owner's explicit instruction.
The sealing commit and blob hash are recorded in `experiments/SEALS.md`.
No field below may change; an edit voids the seal. The governed runner is
`python/qo3_prereg_run.py`, committed at the sealing commit, which takes
every constant from this document.

## Claim

Two claims, each refutable separately, on a coupling grid disjoint from
the exploratory one.

1. **Activation.** For the shared-event family of nested windows, the
   joint requirement (quadratic law within epsilon for every window AND
   universality of the constants within delta) holds on a strictly
   smaller fraction of the coupling grid than the smallest
   single-window fraction.
2. **Inertness.** For the disjoint-probe wedge family, the joint
   requirement holds on exactly the same fraction as the smallest
   single-consumer fraction.

## Scope

Model family: 8-qubit open-chain Ising H = -J sum ZZ - h sum X, thermal
reference at beta = 0.4. The exploratory grid (J in {0.6, 0.8, 1.0, 1.2},
h in {1.6, 1.8, 2.0, 2.2}) and exploratory excitation strengths
{0.05, 0.10, 0.15, 0.20} are excluded. The exploratory record
`results/qo3-family.json` retains its exploratory label and is superseded
for claim purposes.

Family A (disjoint probes): right-exterior wedges of cuts 1..6, each
probed by a Z rotation at its own boundary site. Family B (shared
event): nested windows {3}, {3,4}, {2,3,4}, {1,2,3,4,5}, {0..7}, all
containing the shared excitation site 3, probed by one Z rotation at
site 3. Flux weight: theta^2, from the excitation parameter alone.

## Manifest

- Coupling grid: J in {0.7, 0.9, 1.1, 1.3}, h in
  {1.7, 1.9, 2.1, 2.3} (16 points).
- Excitation strengths: theta in {0.06, 0.11, 0.16, 0.21}.
- Thresholds, fixed here and not revisitable: epsilon = 0.05 (quadratic
  residual), delta = 0.05 (universality spread). A loose sensitivity
  report at 0.15 is descriptive only and carries no claim weight.

All computations are deterministic; there are no seeds.

## Primary outcome

Two numbers per family at (epsilon, delta) = (0.05, 0.05): the joint
survival fraction of the full family and the minimum single-consumer
survival fraction. Claim 1 requires joint(B) < min-single(B). Claim 2
requires joint(A) = min-single(A).

## Secondary outcomes

Cannot rescue a failed primary: the tightening curve of joint survival
versus nested family size for family B; the identity of the surviving
coupling set (predicted, not required, to be the weak-J edge);
monotonicity of the family-B universality spread with coupling strength;
lambda saturation beyond the correlation length on the surviving set.

## Instrument controls

All bars of PEQO-FREEZE-002 apply, in particular B5, B6, B7, B11, and
B13. Per coupling point: the wedge no-signalling null (< 1e-10), strictly
increasing divergence in theta, finiteness of every divergence, thermal
floor clearance, and the nested-window monotonicity of family-B
divergences at the top strength (a DPI theorem; violation invalidates
the instrument).

## Estimator

The committed code path `python/qo3_family.py` at the sealed commit,
modified only by the declared grids above, executed on Atlas in the
committed venv with single-threaded BLAS. The quadratic constant is the
least-squares fit through the origin against theta^2; the spread is the
range of constants divided by their mean.

## Falsification bar

Claim 1 is refuted if joint(B) >= min-single(B). Claim 2 is refuted if
joint(A) < min-single(A) (the quantifier doing work on disjoint probes
would falsify the stated mechanism). If no coupling point satisfies the
family-B requirement even at the loose thresholds, the declaration fails
and both claims are reported as unevaluable with the failure.

## Missing-data rule

Every (coupling point, family, window, theta) cell receives a value; any
non-finite value voids the run under B6 and the void is reported.

## Multiple-comparison rule

Fixed hierarchy: claim 1, then claim 2. Each is one preregistered
comparison at fixed thresholds; no correction.

## Stopping rule

The manifest is fixed and exhaustive. No sequential analysis.

## Resource envelope

Single Atlas process, single-threaded BLAS, expected under one hour. No
NRP objects.

## Evidence record

One JSON record with per-point constants, residuals, spreads, survival
tables at both threshold pairs, code commit, dependency versions, and
SHA-256 hashes, appended to `results/` and never rewritten.

## Interpretation ceiling

If both claims pass they earn [demonstrated-in-model]: in this model
family, an all-observers consistency requirement constrains couplings
exactly when the observers share events. Nothing is licensed about
continuum wedge families, area scaling, type III settings, or physical
gravity.
