# Preregistration PF5-001: conservation and complete accounting

**Status:** SEALED.

**Registration ID:** PREREG-PF5-001

**Date sealed:** 2026-08-06

**Authorization:** sealed on the project owner's explicit instruction
("go ahead" with the recommended gate binding, 2026-08-06). The
sealing commit and blob hash are recorded in `experiments/SEALS.md`.
No field below may change; an edit voids the seal. The governed
runner is `python/pf5_gate_run.py`, committed at the sealing commit.

## Family binding

The going-forward family is the PF4-002 Sauter-slab family, the
populated sealed family, unchanged dynamics and thermal ensemble as
implemented by the frozen instrument's `census_run`. The PF4-003
pulse-train family is excluded, measured empty by
results/prereg-pf4-003.json and results/pf4-004-probe.json.

## Claim under test

For the Sauter-slab family, the apparent pair events are compatible
with conservation and complete accounting, not a branch-counting
illusion.

## Instrument (frozen)

`python/pf5_accounting.py`, validated in
`results/pf5-instrument.json` (evidence 99de4a8). Census classes
nonfinite / reversing / transmitted / capped with declared priority;
charge = sign(dt/dtau); path-degree rule via the sealed polyline
instrument; census_fraction with explicit denominators.

## Grid

Gaps P in {0.60, 0.70, 0.80, 0.90} crossed with fields E in
{0.45, 0.70}, eight cells, disjoint from the pilot grid, from
PREREG-PF4-001, and from PREREG-PF4-002 (training {0.55, 0.75,
0.95}, held {0.65, 0.85}, pilot fields {0.3, 0.4, 0.5, 0.65, 0.8,
1.0}). Ensemble n = 20000 per cell. Seeds 8100000 + 1000 iP + iE
with iP, iE the grid indices. Twelve declared polyline members per
cell, indices 0 through 11. Path-degree levels are the declared
multipliers (-0.61, -0.26, 0.14, 0.41, 0.69) of the exit time.

## Bars (fixed now)

1. Census sums exactly to n in every cell; missing-trajectory
   count 0.
2. Max relative energy residual < 1e-5 per cell, taken over every
   member including failures up to their failure step.
3. Path-degree rule holds at every generic level on the 12 declared
   members per cell, zero failures; refused levels counted, not
   skipped.
4. Every reported statistic uses the census-complete denominator n.
5. Nonfinite + capped fraction < 0.20 per cell, else that cell is
   declared unevaluable (not deleted). At least 6 of 8 cells must
   be evaluable, else the run is a manifest-design failure.

The run PASSES iff bars 1 through 4 hold on every evaluable cell
under bar 5's rule.

## Falsification

Any unexplained creation of conserved quantities, any
charge-balance failure (a path-degree failure is one), or any
dependence of a claim on a deleted class rejects the model family.
A clean negative is a result.

## Out of scope

Field-energy matching (external-field family; clause binds when a
dynamical field model is declared).

## Outputs

results/prereg-pf5-001.json, append-only, hashed, verdict computed
from the bars by the governed runner.
