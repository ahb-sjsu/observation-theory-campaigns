# PREREG D5v4 (DRAFT, NOT SEALED): the observer-relative transition in Burgers shock formation as a law, with the control bar taken per control

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D5v4 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the fourth registration of D5, registered after D5v3.
Its bars and its tolerance rules were fixed in code (`d5v4_grade.py`, `d5v4_fix_tols.py`) before
its pilot ran; this text was written after the pilot and before the seal, and Section 7 records
the pilot.

## 1. Claim under test

D5v3 (`experiments/OD/D5v3/PREREG-D5V3.md`, INDETERMINATE) held every bar but the control bar, and
its record showed with the grader's own numbers that the miss was the bar's definition: pooled
over the two controls, the scaled variable B / B_c(t) placed the two controls' points in different
bins because their front wavenumbers differ (3.0 and 2.4), and since their read fractions differ
the separation between the controls read as a collapse (0.57 against 0.70); taken one control at
a time, each control's scaled and unscaled scatters coincide exactly (1.00 and 1.00), because a
control's front wavenumber barely moves and the scaling is then a constant shift of its points.
The quantity the claim needs is the within-control comparison. This registration is that
definition and nothing else.

The claim is D5v3's, Sections 1 to 4 of `PREREG-D5V3.md` unchanged and incorporated by reference
(the collapse inside the viscosity scope at most 0.005, the convergence bar on f_B(t) / f_B(0) at
budgets 8 and above, the ratio against the unscaled null), with the control bar taken per control:
for each two-dimensional control, its scaled median bin IQR is at least RATIO times its own
unscaled median bin IQR. The bar says that the front-wavenumber scaling organises nothing on a
regular flow; a control whose front wavenumber does not move satisfies it identically, and the
bar has content only where a control's gradient moves, which the run's controls have done by up
to a fifth on earlier draws.

## 2. World

D5v3's world with fresh seeds (probe 20261051 unused, pilot 20261052, run 20261053): four seeded
initial conditions at N = 128 and 256 and nu in {0, 0.005} with one control at 48 squared on the
pilot; four fresh initial conditions at N = 256 and 512 and nu in {0, 0.005, 0.02} with two
controls at 64 squared on the run.

## 3. Estimators

`d5v4_burgers.py`, D5v2's workload unchanged. Grader `d5v4_grade.py`, D5v3's with C3 per control.
Tolerance fixer `d5v4_fix_tols.py`.

## 4. Errors and nulls

D5v3's, unchanged.

## 5. Bars (TOL_N, TOL_C, RATIO FIXED FROM THE PILOT before sealing; NU_MAX = 0.005 and B_MIN_N = 8 declared; Section 7)

- E1, N1, C1, C2, R1: D5v3's, verbatim, with TOL_N, TOL_C and RATIO by D5v3's rules.
- C3: for every control, its scaled median bin IQR is at least RATIO times its own unscaled median
  bin IQR.

Pass: E1, N1, C1, C2, C3. Fail: D5v3's fail clauses, with the control clause per control (any
control's scaled median bin IQR below half its own unscaled one). Otherwise INDETERMINATE.

## 6. What falsifies

D5v3's Section 6. What the per-control bar adds: a control whose own read fractions fall on a
tighter curve in B over its own front wavenumber than in B would say the scaling organises a
regular flow's reader as well as a forming front's, and the collapse would be about budget
against gradient, not about the singular event. Two controls with different front wavenumbers
no longer count as a collapse between them.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS, D5's seven checks on the unchanged workload.

Probe: none separate; D5's probe stands.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261052, sixteen Burgers trajectories and
one control at 48 squared, Atlas 2026-09-10, 15:41 to 15:44 UTC). Every quantity exists on every
trajectory. Convergence: the eight in-scope pairs (N = 128 against 256) differ by 0.017 to 0.070 in
f_B(t) / f_B(0) over budgets 8 and above up to 0.9 t*, so TOL_N = 0.11 by the rule. Collapse: at
nu = 0 the scaled collapse has a median bin IQR of 0.073 over 15 bins and 1,034 points (worst bin
0.176) against 0.126 unscaled, a ratio of 0.58; at nu = 0.005, 0.039 over 14 bins (worst 0.130)
against 0.079, a ratio of 0.50; so TOL_C = 0.11 and RATIO = 0.75 by the rules. The control, taken
on its own: its gradient grew by 6 percent over the four time units, its front wavenumber moved
little, and its scaled and unscaled collapses coincide (median bin IQR 0.203 on 324 points in four
bins, a ratio of 1.00), so C3 holds per control with room; the run's two controls at 64 squared
decide, and the bar has content only where a control's gradient moves. Recorded and not a bar:
the control's read-fraction alarm fired at B = 2 at t = 0.60; no Burgers trajectory fired the
read-fraction alarm before 0.95 t*, and the classical alarm fired on all sixteen. The pilot's own
rows give PASS under the fixed tolerances (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7; commit
   `pilot.json`, `tolerances.json`.
2. Rename this file to `PREREG-D5V4.md`, commit, record its blob hash in the track document and
   the README status ledger.
3. Run on the run seed, grade with `d5v4_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the fourth version of `OD:singular-transition`.
