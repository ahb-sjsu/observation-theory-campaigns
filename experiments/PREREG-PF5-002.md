# Preregistration PF5-002: conservation and complete accounting on
probe-placed cells

**Status:** SEALED.

**Registration ID:** PREREG-PF5-002

**Date sealed:** 2026-08-06

**Authorization:** sealed on the project owner's standing
instruction to proceed with the recommended gate sequence
(2026-08-06). The sealing commit and blob hash are recorded in
`experiments/SEALS.md`. No field below may change; an edit voids
the seal. The governed runner is `python/pf5b_gate_run.py`,
committed at the sealing commit.

## Why this registration exists

PREREG-PF5-001 passed every declared bar on a product grid of gaps
against fields that produced zero reversing trajectories in all
eight cells, so its accounting claim about apparent pair events was
untested. The named error was the manifest, a product grid was
declared where PF4-002 placed cells by bisection. This
registration binds probe-verified cells and adds a bar that makes a
vacuous pass impossible.

## Family binding

The PF4-002 Sauter-slab family, unchanged dynamics and thermal
ensemble as implemented by the frozen instrument's `census_run`.

## Claim under test

For the Sauter-slab family, on cells that contain apparent pair
events, those events are compatible with conservation and complete
accounting, not a branch-counting illusion.

## Instrument (frozen)

`python/pf5_accounting.py`, validated in
`results/pf5-instrument.json` (evidence 99de4a8). Census classes
nonfinite / reversing / transmitted / capped with declared
priority; charge = sign(dt/dtau); path-degree rule via the sealed
polyline instrument; census_fraction with explicit denominators.

## Manifest, bound from the committed placement probe

Bound from `results/pf5-placement-probe.json` (record sha
047cd23006db...), which bisected the field at each declared gap
with 2000 members per step and landed the reversing fraction inside
the declared window 0.02 to 0.30 in all four cells. The bound cells
are

- gap 0.60, field 0.8957885742187499, probe fraction 0.1000
- gap 0.70, field 1.0448364257812501, probe fraction 0.0970
- gap 0.80, field 1.2020141601562502, probe fraction 0.0995
- gap 0.90, field 1.3605468750000003, probe fraction 0.1030

Four cells, ensemble n = 20000 per cell, seeds 8300000 + 1000 i
with i the cell index, disjoint from the pilot grid, from
PREREG-PF4-001, from PREREG-PF4-002, and from PREREG-PF5-001.
Twelve declared polyline members per cell, indices 0 through 11.
Path-degree levels are the declared multipliers (-0.61, -0.26,
0.14, 0.41, 0.69) of the exit time.

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
   declared unevaluable (not deleted). At least 3 of 4 cells must
   be evaluable, else the run is a manifest-design failure.
6. The anti-vacuity bar. Every evaluable cell must record a
   reversing count above zero, and the run must record at least
   2000 reversing trajectories in total across evaluable cells. A
   run that satisfies bars 1 through 5 with too few events is
   recorded as vacuous, not as a pass.

The run PASSES iff bars 1 through 4 and bar 6 hold on the
evaluable cells under bar 5's rule.

## Falsification

Any unexplained creation of conserved quantities, any
charge-balance failure (a path-degree failure is one), or any
dependence of a claim on a deleted class rejects the model family.
A clean negative is a result.

## Out of scope

Field-energy matching (external-field family; clause binds when a
dynamical field model is declared).

## Outputs

results/prereg-pf5-002.json, append-only, hashed, verdict computed
from the bars by the governed runner.
