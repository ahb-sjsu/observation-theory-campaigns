# Preregistration PF6-001: observer, covariance, and gauge audit

**Status:** SEALED.

**Registration ID:** PREREG-PF6-001

**Date sealed:** 2026-08-06

**Authorization:** sealed on the project owner's standing
instruction to proceed with the recommended gate sequence
(2026-08-06). The sealing commit and blob hash are recorded in
`experiments/SEALS.md`. No field below may change; an edit voids
the seal. The governed runner is `python/pf6_gate_run.py`,
committed at the sealing commit.

## Precondition

The PF-6 template binds after PF-5 passes. PREREG-PF5-002 passed on
probe-placed cells with 8068 audited pair events, record sha
feaf9e36c100..., which satisfies the precondition. PREREG-PF5-001
passed its bars on a grid with no events and is not the
precondition.

## Family binding

The PF4-002 Sauter-slab family on the cells bound by
PREREG-PF5-002, taken from the committed placement probe
`results/pf5-placement-probe.json` (record sha 047cd23006db...),

- gap 0.60, field 0.8957885742187499
- gap 0.70, field 1.0448364257812501
- gap 0.80, field 1.2020141601562502
- gap 0.90, field 1.3605468750000003

The PF-6 audits are deterministic per member, so this registration
uses the frozen instrument's deterministic integrator rather than
the thermal ensemble, one member per cell at the declared initial
transverse momentum pu0 = 0.1 and 20000 steps.

## Claim under test

The events of the Sauter-slab family are physical, not
coordinate-specific folds. Their counts and worldpoints are
invariant under the declared passive transformations, and every
observer dependence is predicted by the declared detector model.

## Instrument (frozen)

`python/pf6_covariance.py`, validated in
`results/pf6-instrument.json` (evidence d064041): translation,
reparametrization, boost, gauge machinery, and observer/detector
audits.

## Bars (fixed now)

1. Translation covariance. For declared field-center shifts t0 in
   {-2.0, -0.5, 0.5, 2.0}, the fold count per cell is exactly equal
   to the unshifted count, and the first-fold worldpoint is
   equivariant, the shifted worldpoint minus the shift agreeing
   with the unshifted worldpoint within 1e-6 in the time
   coordinate and 1e-6 in the transverse coordinate.
2. Reparametrization invariance. At Hamiltonian scale alpha = 2,
   the per-member fold count is exactly invariant and the measured
   rate per unit parameter scales as alpha within 1e-12, compared
   on the same physical segment.
3. Boost audit. On the declared hyperbolic control of the frozen
   instrument, flow-boost commutation below 1e-10, invariant
   conservation below 1e-10, and a positive future-cone margin
   across the declared rapidity grid.
4. Gauge clause. The Sauter tilt is declared non-electromagnetic,
   so this clause is recorded not-applicable, as the frozen
   instrument's validation established. It binds only when an
   electromagnetic family is declared.
5. Observer audit. For the declared observer grid alpha in
   (-0.45, -0.2, 0.0, 0.2, 0.45, 3.0), the event count N(alpha)
   read from the observer's record equals the detector-model
   prediction exactly for every alpha and every cell. One
   unpredicted mismatch rejects.
6. Anti-vacuity. Every cell must exhibit at least one fold in the
   unshifted deterministic member, else the run is recorded vacuous
   rather than passing, the PREREG-PF5-001 lesson carried forward.

The run PASSES iff bars 1, 2, 3, 5, and 6 hold on every cell, with
bar 4 recorded not-applicable.

## Falsification

A count that changes under any passive transformation, or an
observer-dependent count not predicted by the declared detector
model, rejects the family.

## Outputs

results/prereg-pf6-001.json, append-only, hashed, verdict computed
from the bars by the governed runner.
