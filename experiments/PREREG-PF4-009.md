# Preregistration PF4-009: an analyticity-controlled exponent

**Status:** SEALED.

**Registration ID:** PREREG-PF4-009

**Date sealed:** 2026-08-07

**Authorization:** sealed on the project owner's standing
instruction to proceed with the recommended sequence (2026-08-07).
The sealing commit and blob hash are recorded in
`experiments/SEALS.md`. No field below may change; an edit voids
the seal. The governed runner is `python/pf4_009_run.py`,
committed at the sealing commit.

Numbering note. The identifiers PF4-005 through PF4-008 name
exploratory runs, so this registration takes 009 to keep every
identifier in the PF4 series unique.

## The question this answers

PREREG-PF4-002 sealed the negative that the Sauter family's
suppression is a Gaussian measure tail in the effective gap, and
left one question open, whether any constructible family has a
non-measure-tail exponent. PREREG-PF4-003 and the PF4-004 probe
closed the pulse-train route by measuring that family empty, and
the mechanism study explained why. The exploratory sequence
PF4-005 through PF4-008c located a family that answers it, and
this registration is the claim-bearing test of that family.

## Family binding

The Gudermannian profile. The tilt runs from minus one to plus one
as the signed quantity one minus four over pi times the arctangent
of the exponential of minus the absolute scaled time, and the force
is two over pi times the hyperbolic secant of the scaled time. Its
nearest complex singularity is a simple pole at pi over two times
the width and its tails decay exponentially.

Why this family and not the others. The Lorentzian profile carries
the same first-order singularity but algebraic tails, and its gate
run PF4-006 failed entry-point independence at 1.3e-2 because its
field never fully turns off. The Gudermannian was chosen to
separate the singularity order from the tail behaviour, and its
gate clauses pass in PF4-008c at 3.0e-9 for the entry point,
6.6e-13 for the timestep, and machine precision for translation.

## Gate precondition

CAMPAIGN.md section 6 requires PF-5 and PF-6 before a claim-bearing
run. Their content is applied to this profile in PF4-008c, record
sha 36932f0be2b3, which passed all eight of its items including
conservation of the extended system's Hamiltonian at 2.6e-12,
complete census, entry-point independence, timestep independence,
and translation covariance. The event-count clauses of PF-6 have
nothing to audit on non-folding crossings and are recorded not
applicable rather than passed.

## Claim under test

For the declared family, the per-crossing transfer is
exponentially suppressed with an exponent that depends only on the
adiabaticity built from the distance to the field's nearest
complex singularity, and is therefore independent of the width.
Because each crossing is deterministic with a single declared
initial condition, no distribution exists whose tail could produce
the suppression, so the exponent is dynamical and not a measure
tail.

## Manifest, disjoint from every prior run

Widths 1.8, 2.8, 3.8, and 4.6, a range of a factor 2.56.
Adiabaticities 1.05, 1.45, 1.85, 2.25, 2.65, and 3.05. Field 0.4,
timestep 1e-4, entry and exit at twenty widths, fourth-order
Runge-Kutta. Every value is disjoint from PF4-005b's widths of 2,
3, and 4 with adiabaticities 0.9 through 3.0 and from PF4-008c's
widths of 1.5, 2.5, and 3.5 with adiabaticities 1.0 through 3.2.

## Bars (fixed now)

Bars are set at the precision the measurements support and not at
the precision they appeared to have. PF4-008c and PF4-005b measured
the sech-squared exponent as minus 1.1013 and minus 1.0477 on two
disjoint grids, a five percent difference wider than either run's
internal spread, so no bar here is tighter than that except where a
quantity was shown to be stable.

1. Width universality, the primary bar. The four fitted exponents
   agree within two percent of their mean. PF4-008c measured 0.61
   percent across three widths.
2. Exponential form. Every cell's coefficient of determination is
   at least 0.995. PF4-008c measured 0.9987.
3. Conservation. The extended Hamiltonian drifts by at most 1e-11
   relative in every cell. PF4-008c measured 2.6e-12 with the
   corrected tilt evaluation.
4. Entry-point independence. Moving the entry half again further
   out changes every transfer by at most 1e-7 relative. PF4-008c
   measured 3.0e-9.
5. Anti-vacuity. Every transfer lies strictly between 1e-12 and 1,
   so no fit rests on numerical noise or on an unsuppressed value.
6. Census. No cell is nonfinite and none folds.

The run PASSES iff all six hold.

## Falsification

If the fitted exponents vary across widths beyond bar 1, the
exponent is not fixed by the adiabaticity alone and the claim
fails. A clean negative is a result.

## Non-claims, binding on the report

The observable is the per-crossing transfer and not an event rate.
The step from one to the other is blocked by the cancellation
measured in the mechanism study and no claim about a pair
production rate follows from this registration. The constant
multiplying the adiabaticity is not predicted by this
registration, and the separate observation that a first-order
singularity gives close to minus two while a second-order pole
gives about minus 1.1 is an exploratory finding of PF4-008c and is
not sealed here. Nothing in this registration is a claim about
quantum field theory or about any physical process.

## Outputs

results/prereg-pf4-009.json, append-only, hashed, verdict computed
from the bars by the governed runner.
