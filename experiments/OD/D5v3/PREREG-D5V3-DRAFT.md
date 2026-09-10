# PREREG D5v3 (DRAFT, NOT SEALED): the observer-relative transition in Burgers shock formation as a law, with convergence measured on the quantity the collapse uses

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D5v3 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the third registration of D5, registered after D5v2.
Its bars and its tolerance rules were fixed in code (`d5v3_grade.py`, `d5v3_fix_tols.py`) before
its pilot ran; this text was written after the pilot and before the seal, and Section 7 records
the pilot.

## 1. Claim under test

D5v2 (`experiments/OD/D5v2/PREREG-D5V2.md`, INDETERMINATE) established the collapse and its
control: inside the viscosity scope the read fractions of carried perturbations collapse on B
over the front wavenumber at 0.48 and 0.39 of the unscaled null, and the same construction on a
regular two-dimensional flow organises nothing (1.02). It missed one bar on one of four initial
conditions, the convergence in resolution, where the raw read fractions at budgets 2 and 4
differed by 0.18 between N = 256 and 512 near 0.9 of the shock time, on the initial condition
whose front is sharpest and which the coarser grid under-resolves. D5v2's record named the
repair: measure convergence on f_B(t) / f_B(0), the quantity the collapse uses, at the budgets
the coarser grid resolves. This registration is that repair and nothing else.

The claim is D5v2's, Sections 1 to 4 of `PREREG-D5V2.md` unchanged and incorporated by reference,
with the convergence bar taken on f_B(t) / f_B(0) over budgets 8 and above, up to 0.9 t*, at the
same initial condition and viscosity between N and 2N. Budgets 2 and 4 are still run, still enter
the collapse and its bars, and their raw resolution differences are reported. The scope
(viscosity at most 0.005), the collapse bars, the ratio against the null and the control bar are
D5v2's, with tolerances fixed from this registration's own pilot by D5v2's rules.

## 2. World

D5v2's world with fresh seeds (probe 20261045 unused, pilot 20261046, run 20261047): four seeded
initial conditions at N = 128 and 256 and nu in {0, 0.005} with one control at 48 squared on the
pilot; four fresh initial conditions at N = 256 and 512 and nu in {0, 0.005, 0.02} with two
controls at 64 squared on the run.

## 3. Estimators

`d5v3_burgers.py`, D5v2's workload unchanged. Grader `d5v3_grade.py`, D5v2's with the convergence
bar as stated (B_MIN_N = 8). Tolerance fixer `d5v3_fix_tols.py`.

## 4. Errors and nulls

D5v2's, unchanged.

## 5. Bars (TOL_N, TOL_C, RATIO FIXED FROM THE PILOT before sealing; NU_MAX = 0.005 and B_MIN_N = 8 declared; Section 7)

- E1, exact: read fractions nested in B and at most one at every sample of every world.
- N1: for every in-scope pair (N, 2N) at the same initial condition and viscosity, the largest
  difference in f_B(t) / f_B(0) over budgets 8 and above and t at most 0.9 t* is at most TOL_N (1.5
  times the pilot's largest, rounded up to 0.01).
- C1, C2, R1, C3: D5v2's, verbatim, with TOL_C and RATIO by D5v2's rules.

Pass: E1, N1, C1, C2, C3. Fail: D5v2's fail clauses. Otherwise INDETERMINATE.

## 6. What falsifies

D5v2's Section 6. What this registration adds: N1 failing on the normalised read fraction at
budgets 8 and above is a failure of the instrument to converge where the front is resolved,
and would say the transition is not a property of the continuum limit at this ladder.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS, D5's seven checks on the unchanged workload.

Probe: none separate; D5's probe stands.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261046, sixteen Burgers trajectories and
one control at 48 squared, Atlas 2026-09-10, 13:18 to 13:20 UTC). Every quantity exists on every
trajectory. Convergence on the bar's quantity: the eight in-scope pairs (N = 128 against 256)
differ by 0.011 to 0.062 in f_B(t) / f_B(0) over budgets 8 and above up to 0.9 t*, so TOL_N = 0.10 by
the rule; on the raw read fractions over all budgets, reported and not a bar, the same pairs
differ by 0.05 to 0.13, the largest at budget 2 on the initial condition whose front is sharpest,
as in D5v2. Collapse: at nu = 0 the scaled collapse has a median bin IQR of 0.074 over 15 bins and
1,221 points (worst bin 0.192) against 0.135 unscaled, a ratio of 0.54; at nu = 0.005, 0.038 over
14 bins (worst 0.208) against 0.087, a ratio of 0.44; so TOL_C = 0.12 and RATIO = 0.70 by the
rules. The control: its gradient did not grow over the four time units (ratio 1.000) and its front
wavenumber did not move, so its scaled and unscaled collapses coincide (median bin IQR 0.056 on
324 points in four bins, a ratio of 1.00), and C3 holds with room; the run's two controls at 64
squared, whose gradients moved by up to a fifth on D5's and D5v2's draws, decide. Recorded: the
read-fraction alarm fired on one Burgers trajectory (initial condition 12 at N = 256, nu = 0, at
B = 2 at 0.80, after the classical alarm at 0.58) and on the control at B = 2 at t = 0.75. The
pilot's own rows give PASS under the fixed tolerances (`pilot_grade.json`). One operational note
on record: the pilot's launch script was rewritten on disk while its shell was reading it, so its
last line, the done marker, did not print; the pilot's Python process ran to completion and wrote
`pilot.json` unaffected.

## 8. Sealing procedure

1. Self-test and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7; commit
   `pilot.json`, `tolerances.json`.
2. Rename this file to `PREREG-D5V3.md`, commit, record its blob hash in the track document and
   the README status ledger.
3. Run on the run seed, grade with `d5v3_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the third version of `OD:singular-transition`.
