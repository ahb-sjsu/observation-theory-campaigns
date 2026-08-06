# PREREG-PF4-004 (TEMPLATE, unsealed)

This template becomes PREREG-PF4-004.md when the slots marked
<<...>> are bound from the committed PF4-004 probe record
(results/pf4-004-probe.json) and the document is sealed into
experiments/SEALS.md. Nothing here is claim-bearing until sealed.

## 1. Lesson bound from PF4-003

PF4-003 sealed itself unevaluable, every cell capped without a
reversal, because its manifest was placed from a probe of a proxy
observable at different declared constants. The binding rule of
this registration, no cell enters the manifest unless the committed
direct-observable probe, run with the sealed dynamics verbatim at
identical constants, measured a reversal below half the probe cap
in that exact cell.

## 2. Claim and bars (unchanged from PF4-003)

The observable is N_rev(P), the slab count at reversal, on the
thermal-free pulse-train family with the smooth sech-squared slab
profile. The sealed claim, log N_rev is organized by the action
model a + b/P and not by a power law in P, judged on held-out
velocities. Bars, held-out weighted MSE ratio of the power-law
model over the action model at least 4.0, minimum three usable
held cells, and the mandatory C5 plant, the square-wave family
must be found power-law-organized with the two prescriptions in
disagreement by at least 0.5, or the run is void.

## 3. Declared constants (bound from the probe)

Field strength E = <<E_FIELD from the probe rung whose cells all
reversed below cap/2>>. Slab length L = 3.0, spacing D = 18.0,
timestep dt = 2e-3, integrator RK4 in proper time, cap N_CAP =
<<2x the largest probe-verified N_rev, rounded up to a round
number>>. Train velocities <<four P values whose probe cells
reversed below cap/2>>, held velocities <<three interleaved P
values, probe-verified likewise>>.

## 4. Manifest verification clause

At sealing time this document must cite, for every train and held
cell, the probe record's measured N_rev at identical constants,
each below half the probe cap. A sealed run that still caps in any
cell is a manifest failure charged to this document, not to the
family.

## 5. Outputs

results/prereg-pf4-004.json, append-only, hashed, with the plant
verdict computed before the claim verdict, harvest order plant
first as in PF4-003.
