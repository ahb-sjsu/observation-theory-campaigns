# PF-6 instrument layer: observer, Lorentz, and gauge audit

**Status.** Instrument implemented and passing, unsealed,
exploratory. The claim-bearing PF-6 run is NOT this document. It
awaits the family selected by the PREREG-PF4-003 harvest, runs after
the sealed PF-5 gate, and must itself be sealed before it runs.
CAMPAIGN.md section PF-6 is the governing design and calls this gate
mandatory. Runner `python/pf6_covariance.py`, evidence
`results/pf6-instrument.json` (commit d064041).

## The five audits and their measured validations

**P1, translation covariance.** Shifting the field profile and the
initial data together shifts every trajectory and every event
worldpoint by exactly the offset, measured at 2.7e-13 on both a
transmitted and a reversing Sauter member, with the reversing
member's single fold worldpoint exactly equivariant.

**P2, reparametrization invariance.** Scaling the Hamiltonian
relabels the evolution parameter. With the scale a power of two the
stepwise arithmetic is exactly the base arithmetic, so the path
deviation is exactly zero, the per-worldline event count is exactly
invariant (the integer one on the audited member), and the rate per
unit parameter scales by exactly the predicted factor. The witness
this freezes for any claim run, the physical rate of this model
class is per worldline, never per parameter tick.

**P3, boost audit** on the family with genuine hyperbolic structure,
the PF-3 Stueckelberg replication, whose continuous accumulation is
a rapidity flow in the (tdot+1, w) plane. Flow and boosts commute at
4.5e-13, the invariant is conserved at 7.1e-11 across the grid of
states, rapidities, and couplings, and the future cone margin stays
positive everywhere, so the campaign's never-reverses finding is
boost-invariant.

**P4, gauge machinery**, validated on a declared electromagnetic
control, the length gauge against the velocity gauge for a pulsed
field on an anharmonic degree of freedom. Physical histories agree
at 2.2e-13 and the canonical momenta differ by exactly the predicted
gauge shift at 1.1e-12. The Sauter families' tilt coupling is
declared non-electromagnetic (a scalar tilt with no field tensor),
so the campaign's gauge clause binds only when an electromagnetic
family is declared, and this machinery stands validated for that
day.

**P5, observer and detector audit.** For the declared observer
family T_alpha = t + alpha tau, the event count is measured twice,
from the observer's own record (sign changes of the
finite-difference slope of T_alpha) and from the model's detector
prediction (crossings of p_t through the level -alpha). The counts
agree exactly at every declared alpha, and the measured curve on the
reversing member is 0, 1, 1, 1, 0, 0 across alphas -0.45 to 3. This
is the campaign clause made mechanical, observer-dependent particle
number is retained lawfully because a physical detector model
predicts every count exactly, and any residual observer dependence a
claim run cannot predict this way trips the bar.

## What remains before the gate can close

The sealed PF-6 run on the going-forward family, after the sealed
PF-5 gate, with these five audits as its frozen instrument. PF-7
(quantum-structure ceiling) stays gated behind both.
