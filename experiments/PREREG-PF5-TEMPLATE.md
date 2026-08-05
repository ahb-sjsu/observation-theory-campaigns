# PREREG-PF5-001 (TEMPLATE — not sealed; bind and seal after the PF4-003 harvest)

Slots marked <<...>> are bound before sealing; everything else is fixed now.

## Claim under test
For the going-forward family <<FAMILY: from the PF4-003 harvest>>, the
apparent pair events are compatible with conservation and complete
accounting, not a branch-counting illusion.

## Instrument (frozen)
`python/pf5_accounting.py` at commit <<COMMIT>>, validated in
`results/pf5-instrument.json` (evidence 99de4a8). Census classes
nonfinite / reversing / transmitted / capped with declared priority;
charge = sign(dt/dtau); path-degree rule via the sealed polyline
instrument; census_fraction with explicit denominators.

## Grid
<<P values, E values, n per cell, seeds — disjoint from all prior runs>>

## Bars (fixed now)
1. Census sums exactly to n in every cell; missing-trajectory count 0.
2. Max relative energy residual < 1e-5 per member, every member,
   including failures up to their failure step.
3. Path-degree rule holds at every generic level on <<K>> sampled
   members per cell (refused levels counted, not skipped).
4. Every reported statistic uses the census-complete denominator; any
   discrepant-flagged fraction in a claim VOIDS the run.
5. Nonfinite + capped fraction < <<F_MAX>> per cell, else that cell is
   declared unevaluable (not deleted).

## Falsification
Any unexplained creation of conserved quantities, any charge-balance
failure, or any dependence of a claim on a deleted class rejects the
model family. A clean negative is a result.

## Out of scope
Field-energy matching (external-field family; clause binds when a
dynamical field model is declared).
