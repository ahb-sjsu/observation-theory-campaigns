# PF-5 instrument layer: conservation and complete accounting

**Status.** Instrument implemented and passing on exact controls,
unsealed, exploratory. The claim-bearing PF-5 run is NOT this
document. It awaits the family selected by the PREREG-PF4-003
harvest, and it must be sealed, with bars frozen against this
instrument, before it runs. CAMPAIGN.md section PF-5 is the
governing design and calls this gate mandatory.

Runner `python/pf5_accounting.py`, evidence
`results/pf5-instrument.json` (commit 99de4a8).

## What the layer provides

**Complete census.** Every trajectory ends in exactly one declared
class, nonfinite (numerical failure), reversing (first p_t zero
crossing), transmitted (exits the slab forward), or capped (alive at
the step cap), with the classification priority declared in the
runner. The census must sum exactly to the ensemble size, so the
missing-trajectory count is identically zero by construction, and
the fraction interface returns any statistic only against an
explicitly declared denominator, always alongside the
census-complete value, with a nan-safe discrepancy flag that fires
whenever a deletion changes the number.

**Continuous conservation.** The Stueckelberg Hamiltonian has no
explicit evolution-parameter dependence, so H is conserved along
every trajectory. The maximum relative residual is tracked every 25
steps for every member, including failed members up to their failure
step. The frozen instrument bar is 1e-5, with the harmonic control
measured at 4.4e-7 and the smoke cell at 5.6e-7.

**Declared charge assignment.** The orientation charge of a branch
is the sign of dt/dtau, declared here before any claim run. The
conservation statement is the path-degree rule, the signed crossing
count of any generic level equals the endpoint bookkeeping, which is
exactly the statement that folds create orientation charge only in
cancelling pairs. The rule is checked per member per level by the
sealed polyline instrument, and non-generic levels it refuses are
counted, never silently skipped.

**Field-energy matching** is declared out of scope for
external-field families, where the tilt is a fixed background. The
campaign clause applies to dynamical-field models, and any such
model must implement the matching before a claim run.

## Controls (all passing)

C1, harmonic conservation, drift 4.4e-7 against the 1e-6 control
bar. C2a, a field-free cell classifies 2000 of 2000 transmitted.
C2b, a deterministically reversing cell classifies 2000 of 2000
reversing. C3, with the field off so reversal cannot preempt the
classification, an absurd step size overflows the quartic and all
200 members are counted nonfinite with zero missing. C3b, a short
step cap counts 100 of 100 capped. C4, the analytic double fold
obeys the path-degree rule at all 41 generic levels. C5, the
deletion trap, dropping a populated class is mechanically flagged,
including the empty-denominator edge.

## Smoke application, no claim

One Sauter cell of the PF-4 family (P 0.75, E 0.65, five thousand
members, constants imported from the committed pilot) produces the
full witness record, census 5000 transmitted with zero missing,
maximum energy residual 5.6e-7, and the charge rule exact on the
sampled worldlines. The cell sits outside the razor band, so no
reversals occurred and no rate statement of any kind is made.

## What remains before the gate can close

The sealed PF-5 run on the going-forward family, with bars frozen
against this instrument, executed after the PREREG-PF4-003 harvest.
PF-6 (observer, Lorentz, and gauge audit) remains unimplemented and
is the following mandatory gate. PF-7 stays gated behind both.
