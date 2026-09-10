# PREREG D5v2 (DRAFT, NOT SEALED): the observer-relative transition in Burgers shock formation as a law with its viscosity scope

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D5v2 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the rehabilitation of D5, registered after the track's
declared order was complete. Its bars and its tolerance rules were fixed in code (`d5v2_grade.py`,
`d5v2_fix_tols.py`) before its pilot ran; this text was written after the pilot and before the
seal, and Section 7 records the pilot.

## 1. Claim under test

D5 (`experiments/OD/D5/PREREG-D5.md`, INDETERMINATE) established that the read fraction of carried
perturbations, per spectral budget B, converges in resolution and collapses on x = B / B_c(t), B_c
the front wavenumber max |u_x| / max |u|, where a front forms; and it refuted, as it said in advance
it would, the two clauses the track's gate had attached: that a budgeted reader sees the shock
before the gradient does (the classical extrapolation is exact for inviscid Burgers, and the
reader's share falls after the gradient has grown), and that the read-fraction alarm does not fire
on a regular two-dimensional flow (it fires whenever the flow moves perturbation energy past the
reader's budget, singular or not). D5 also found the collapse failing at nu = 0.02, where viscosity
holds the front's wavenumber near its initial value and there is little for the scaling to
organise.

This registration takes what D5 established as the claim, with the boundary D5 found declared as a
scope, and replaces the negative control D5 refuted with the one the claim needs.

The claim. In the periodic Burgers equation at viscosity nu at most NU_MAX = 0.005, from seeded
smooth initial conditions, the read fraction f_B(t) of a fixed carried set of smooth perturbations
under the spectral reader of budget B (the quantity of D5 Section 1, unchanged) converges in
resolution and collapses on x = B / B_c(t): the points (log2 x, f_B(t) / f_B(0)) of every
trajectory at a given viscosity, on samples after the front has begun to steepen (B_c at least 1.2
times its initial value), fall on one curve, tighter than on the unscaled null x = B by a declared
ratio. The scope is declared, not fitted: nu = 0.02 at these amplitudes is outside it, is run, and
is reported, not claimed. The negative control is decaying two-dimensional turbulence with the same
carried-perturbation estimator, and the claim about it is that the same scaling does not organise
its read fractions: with x = B / B_c(t) and B_c = max |grad u| / max |u| defined on the control's
velocity field exactly as on Burgers, the control's points must not collapse more tightly on the
scaled variable than on the unscaled one. The one change to the workload is that the control now
records max |u| at every sample so that its front wavenumber is the same quantity as the Burgers
worlds'; D5 graded the control by its alarms only.

No lead clause and no alarm clause. D5 showed and said in advance that the budgeted reader is
not early and that its alarm is not specific; the alarms are still computed and recorded.

(E) The read fraction is nested in B and at most one, at every sample. (N) Convergence, inside the
scope: at the same initial condition and viscosity, the read fractions at N and 2N agree within
TOL_N up to 0.9 t*. (C) Collapse, inside the scope: at every viscosity in the scope, the scaled
collapse's median bin IQR is at most TOL_C and its worst bin at most 2 TOL_C, and the scaled
collapse's median bin IQR is at most RATIO times the unscaled null's. (R) Outside the scope,
reported: the scaled and unscaled median bin IQRs at nu = 0.02. (X) The control does not collapse:
its scaled median bin IQR is at least RATIO times its unscaled one.

## 2. World

Pilot (seed 20261038): four seeded initial conditions at N = 128 and 256 and nu in {0, 0.005},
sixteen trajectories, and one two-dimensional control at 48 squared. Run (seed 20261039): four
fresh initial conditions at N = 256 and 512 and nu in {0, 0.005, 0.02}, twenty-four trajectories,
and two controls at 64 squared. D5's world with fresh seeds: trajectories to 0.95 t*, sampled every
0.02; time step 0.002 at N = 256, scaled with N; budgets B in {2, 4, 8, 16, 32, 64} where B is at
most N/3; the control decaying two-dimensional Navier-Stokes in vorticity form (nu = 0.001) from a
seeded smooth field of four low modes at amplitude 4, run four time units, r = 8, budgets B in
{2, 4, 8, 16}. Probe seed 20261037, unused: no separate probe was run, D5's probe standing for an
unchanged estimator.

## 3. Estimators

`d5v2_burgers.py`, D5's `d5_burgers.py` with the control's max |u| recorded (one line). Self-test:
D5's seven checks (Atlas 2026-09-10, PASS). Grader `d5v2_grade.py`, importing D5's point and
scatter functions unchanged; the control's points by `control_points` with the same bins.

## 4. Errors and nulls

The quantities are deterministic given the seeds. The null for the collapse is the unscaled
variable x = B, on the Burgers worlds and on the control alike. Tolerances are fixed from the pilot
by the rules of Section 5.

## 5. Bars (TOL_N, TOL_C, RATIO FIXED FROM THE PILOT before sealing; NU_MAX = 0.005 declared; Section 7)

- E1, exact: read fractions nested in B and at most one at every sample of every world.
- N1: for every in-scope pair (N, 2N) at the same initial condition and viscosity, the largest
  difference in read fraction over shared budgets and t at most 0.9 t* is at most TOL_N (1.5 times
  the pilot's largest, rounded up to 0.01).
- C1: at every in-scope viscosity, the scaled collapse's median bin IQR is at most TOL_C (1.5 times
  the pilot's largest median, rounded up to 0.01) and its worst bin at most 2 TOL_C.
- C2: at every in-scope viscosity, the scaled collapse's median bin IQR is at most RATIO times the
  unscaled null's (RATIO = 1.25 times the pilot's largest in-scope scaled-over-unscaled ratio,
  rounded up to 0.05, at most 0.9).
- R1, reported: the scaled and unscaled median bin IQRs at nu = 0.02.
- C3: the controls' pooled scaled median bin IQR is at least RATIO times their unscaled one.

Pass: E1, N1, C1, C2, C3. Fail: an in-scope resolution difference above 3 TOL_N; an in-scope
scaled collapse median IQR above 3 TOL_C; the control's scaled median bin IQR below half its
unscaled one (the scaling organises a regular flow as well, and the collapse is not about the
front). Otherwise INDETERMINATE.

## 6. What falsifies

N1 failing by its fail clause says the transition is a discretisation artefact. C2 failing says
the front wavenumber is not the scale that organises what a budgeted reader sees inside the very
scope where D5 found it to be. C3 failing says the scaling is not about a forming front: a regular
two-dimensional flow's read fractions would then fall on the same kind of curve in B over its own
gradient scale, and the law would be about budget against gradient, not about the singular event.
R1 is not a bar; it records the boundary.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS, D5's seven checks on the revised file.

Probe: none separate; D5's probe (`experiments/OD/D5/probe.json`) stands, the estimator being
unchanged and the one added record a quantity the control's solver already computes.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261038, sixteen Burgers trajectories and
one control at 48 squared, Atlas 2026-09-10, 06:21 to 06:24 UTC). Every quantity exists on every
trajectory. Resolution: the eight in-scope pairs (N = 128 against 256) differ by 0.030 to 0.101 in
read fraction up to 0.9 t*, so TOL_N = 0.16 by the rule. Collapse: at nu = 0 the scaled collapse
has a median bin IQR of 0.086 over 14 half-octave bins and 990 points (worst bin 0.180) against
0.144 for the unscaled null, a ratio of 0.59; at nu = 0.005, 0.045 over 13 bins and 930 points
(worst 0.128) against 0.087, a ratio of 0.52; so TOL_C = 0.13 and RATIO = 0.75 by the rules. The
control: its front wavenumber, now recorded, moves with its gradient (which grew by a fifth over
the four time units as its vortices interacted); its 324 points fall in four bins on either
variable, with a scaled median bin IQR of 0.407 against 0.396 unscaled, a ratio of 1.03, so the
scaling does not organise the regular flow and C3 holds on the pilot's control with room (0.75
required). Recorded and not a bar: the control's read-fraction alarm fired at B = 2, 4 and 8 (at
t = 0.90, 1.75 and 3.25), as D5 found; the classical alarm did not fire on the two nu = 0.005
trajectories of initial condition 11, whose gradient grew 2.1 to 2.2 times before 0.95 t*. The
pilot's own rows give PASS under the fixed tolerances (`pilot_grade.json`); the run decides on
fresh initial conditions at N = 256 against 512, with nu = 0.02 outside the scope reported and
two controls.

## 8. Sealing procedure

1. Self-test and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7; commit
   `pilot.json`, `tolerances.json`.
2. Rename this file to `PREREG-D5V2.md`, commit, record its blob hash in the track document and
   the README status ledger.
3. Run on the run seed, grade with `d5v2_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the second version of `OD:singular-transition`.
