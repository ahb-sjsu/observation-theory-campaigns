# Preregistration PF6-002: observer, covariance, and gauge audit on
probe-placed members

**Status:** SEALED.

**Registration ID:** PREREG-PF6-002

**Date sealed:** 2026-08-06

**Authorization:** sealed on the project owner's standing
instruction to proceed with the recommended gate sequence
(2026-08-06). The sealing commit and blob hash are recorded in
`experiments/SEALS.md`. No field below may change; an edit voids
the seal. The governed runner is `python/pf6b_gate_run.py`,
committed at the sealing commit.

## Why this registration exists

PREREG-PF6-001 returned vacuous. Its anti-vacuity bar caught that
the deterministic member at each bound cell produces no folds, so
its covariance audits ran on fold-free worldlines. The named error
is the member, not the cell. The thermal ensemble reverses about
ten percent of the time at these cells, so the reversing members
carry transverse momentum in the tail while the declared
deterministic member at pu0 = 0.1 does not. This is the third
instance of one error class in this campaign, a manifest placed
without verifying that it contains the events its claim is about,
after PF4-003's empty cells and PREREG-PF5-001's event-free grid.
The standing rule this registration adopts, every gate registration
must cite a committed probe that verifies event presence for every
bound cell and member.

## Precondition

PREREG-PF5-002 passed on probe-placed cells with 8068 audited pair
events, record sha feaf9e36c100..., which satisfies the PF-6
template's precondition.

## Family and member binding

The PF4-002 Sauter-slab family on the PREREG-PF5-002 cells, with
members bound from the committed member probe
`results/pf6-member-probe.json` (record sha in that record), which
scanned the initial transverse momentum and verified folds.

- gap 0.60, field 0.8957885742187499, pu0 = 3.0, probe folds 4
- gap 0.70, field 1.0448364257812501, pu0 = 3.0, probe folds 2
- gap 0.80, field 1.2020141601562502, pu0 = 3.0, probe folds 2
- gap 0.90, field 1.3605468750000003, pu0 = 2.0, probe folds 2

Step budget 40000 per member, matching the probe.

## Claim under test

The events of the Sauter-slab family are physical, not
coordinate-specific folds. Their counts and worldpoints are
invariant under the declared passive transformations, and every
observer dependence is predicted by the declared detector model.

## Instrument (frozen)

`python/pf6_covariance.py`, validated in
`results/pf6-instrument.json` (evidence d064041).

## Bars (fixed now)

1. Translation covariance. For declared field-center shifts t0 in
   {-2.0, -0.5, 0.5, 2.0}, the fold count per member is exactly
   equal to the unshifted count, and the first-fold worldpoint is
   equivariant within 1e-6 in both coordinates.
2. Reparametrization invariance. At Hamiltonian scale alpha = 2,
   the per-member fold count is exactly invariant and the rate per
   unit parameter scales as alpha within 1e-12 on the same
   physical segment.
3. Boost audit. On the frozen instrument's declared hyperbolic
   control, flow-boost commutation below 1e-10, invariant
   conservation below 1e-10, positive future-cone margin across the
   declared rapidity grid.
4. Gauge clause. Recorded not-applicable, the Sauter tilt is
   declared non-electromagnetic.
5. Observer audit. For the declared observer grid alpha in
   (-0.45, -0.2, 0.0, 0.2, 0.45, 3.0), the event count read from
   the observer's record equals the detector-model prediction
   exactly for every alpha and every member. One unpredicted
   mismatch rejects.
6. Anti-vacuity. Every bound member must exhibit at least one fold,
   and the total fold count across members must be at least 8,
   matching the probe's verified counts. A run below that is
   recorded vacuous, not as a pass.
7. Parity record, measurement with no bar. The per-member fold
   count is recorded for the PF-8 parity argument, which predicts
   even counts for complete worldlines under generic projections.

The run PASSES iff bars 1, 2, 3, 5, and 6 hold on every bound
member, with bar 4 recorded not-applicable.

## Falsification

A count that changes under any passive transformation, or an
observer-dependent count not predicted by the declared detector
model, rejects the family.

## Outputs

results/prereg-pf6-002.json, append-only, hashed, verdict computed
from the bars by the governed runner.
