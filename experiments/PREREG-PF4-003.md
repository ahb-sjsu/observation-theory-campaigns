# Preregistration PF4-003: the frozen-measure pulse-train family

**Status:** SEALED.

**Registration ID:** PREREG-PF4-003

**Date sealed:** 2026-08-04

**Authorization:** sealed on the project owner's explicit instruction.
The sealing commit and blob hash are recorded in `experiments/SEALS.md`.
No field below may change; an edit voids the seal. The governed runner
is `python/pf4_frozen_run.py`, committed at the sealing commit, which
takes every constant from this document.

## Why this family exists

PREREG-PF4-002 sealed the negative for the thermal Sauter family, whose
exponent is the Gaussian tail of its initial measure. Hunt probes zero
and one then located a dynamics-set alternative in the same physics.
The reversible in-slab dip is power-law, but the post-crossing residual
carries the analyticity exponential of the sech^2 profile, measured
log-linear in 1/P over two decades in a thermal-free system, with the
moderate-adiabaticity slope quantitatively matching the exact
Landau-Zener-type form. This preregistration constructs the family
whose reversal is governed by that residual and by nothing else.

## The family

A single deterministic event (u at the Newton-solved shifted
equilibrium, pu = 0, no ensemble, no measure anywhere) crosses an
alternating train of Sauter slabs,

tilt(t) = g E L sum_k (-1)^k tanh((t - kD)/L),

with (omega_u, lambda, g) = (1.2, 0.1, 0.25) as throughout, E = 0.6,
L = 3, D = 18. Each crossing deposits the action-suppressed residual;
deposits accumulate; the event reverses when the gap is spent. The
observable is N_rev(P), the slab count at reversal, with cap 4000
slabs (an uncrossed cap makes the cell unusable, reported). Continuous
RK4 at dt = 2e-3 per the closure clause.

## Claim

On held-out velocities, log N_rev of the smooth family is organized by
the action model log N = a + b/P and not by the power-law model
log N = a' + c log P. PASSES iff the power-law model's held-out mean
squared error is at least 4 times the action model's. REFUTED iff the
power law fits held-out as well or better. Otherwise neither-model,
reported with both residual sets.

## The C5 plant (mandatory, this is a rate-law claim)

The square-wave variant replaces tanh by sign, the sudden limit whose
transfer per slab has no analyticity suppression, so its N_rev must be
organized by the power law. Before any claim is read, the pipeline
must find (a) the plant NOT action-favored (power/action held-out
ratio at most 1) and (b) the smooth and plant prescriptions in
disagreement (max |log N_rev difference| over common usable cells
greater than 0.5). If either fails, the run is VOID and no claim is
readable, per PF4-DESIGN clause C5.

## Manifest

Training velocities P in {1.2, 1.5, 1.8, 2.1}; held-out velocities
P in {1.35, 1.65, 1.95}, interleaved and disjoint. One deterministic
trajectory per cell; there are no seeds. Fewer than three usable
held-out cells is a manifest-design failure, reported as unevaluable.

## Secondary outcomes (cannot rescue the primary)

The fitted action slope b against the analyticity band
[pi omega_u L / 2, pi omega_u L] = [5.65, 11.31] (coherent versus
diffusive accumulation shift the prefactor and the slope within the
band; which accumulation regime the family realizes is itself an
open question this run will inform); the plant's fitted power
exponent; the per-cell N_rev tables of both prescriptions.

## Estimator, stopping, envelope, record

The committed runner, ordinary least squares on the declared models,
fixed manifest, no sequential analysis. Single Atlas process in a
named screen session, single-threaded BLAS. One JSON record with all
cells, fits, the C5 verdict, code commit, and SHA-256 hashes,
appended to `results/`.

## Interpretation ceiling

A pass earns [demonstrated-in-model]: a constructible hidden-dynamics
family exists whose reversal count law is action-set, exponential in
one power of the velocity scale, in a system containing no measure to
imitate it. That is the structural shape the Schwinger exponent has
and the thermal family lacked. It licenses nothing about physical
pair production and does not by itself produce a rate-per-volume law;
the bridge from slab counts to rates, and any quantitative
Schwinger-form comparison, would require further sealed work.
