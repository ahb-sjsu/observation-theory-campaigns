# PREREG D7v2 (DRAFT, NOT SEALED): the read-distortion closure of a filtered flow inside its rank scope

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D7v2 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the rehabilitation of D7, registered after the track's
declared order was complete. Its bars and its tolerance rules were fixed in code (`d7v2_grade.py`,
`d7v2_fix_tols.py`) before its pilot ran; this text was written after the pilot and before the
seal, and Section 7 records the pilot.

## 1. Claim under test

D7 (`experiments/OD/D7/PREREG-D7.md`, INDETERMINATE) refuted its declared arm: the leading
eigen-directions of the read operator of the resolved tendency with respect to the subfilter state
close a filtered two-dimensional flow worse than the same number of energy-ranked modes, in 87 of
96 rank cells. Its second arm, registered beside the declared one before the probe, held where the
theory says it should: the read-distortion closure, which keeps the subfilter modes of largest
sensitivity times energy, beat the energy closure pooled at every rank, by 0.4 and 0.7 percent at
ranks 16 and 32, below D7's margin of 1 percent, and by 1.4 and 6.1 percent at ranks 64 and 128,
above it, the margin growing with rank and with the cutoff and converging in resolution.

This registration takes the second arm as the claim, with the ranks where D7 found the two
rankings to separate declared as a scope. The reason for the scope is in the closures: at low
rank both rankings keep the same few energetic modes, and the sensitivity weight cannot separate
what it has not been given a choice about; at higher rank the choice is among many modes of
comparable energy, and sensitivity decides.

The claim. For decaying two-dimensional turbulence with the spectral cutoff k_c as consumer and
budget, at closure rank r at least R_MIN = 64, the read-distortion closure (the r subfilter modes of
largest diag(P) times squared coefficient, P = J^T J the read operator probed blind on the solver by
central differences, as in D7) predicts the resolved tendency better than the r modes of largest
energy, pooled over snapshot cells, by a margin M2 at every in-scope rank, and is behind the energy
closure in no in-scope cell by more than TOL2; the margin changes by at most TOL_N between the run's
two resolutions; and below the scope the pooled margin is smaller than inside it, which is what
makes the scope a scope and not a selection. The eigen-direction closure and the full-rank
remainder are computed and recorded, not claimed. The world, the probe, the closures and the error
are D7's, unchanged, on fresh seeds.

(E) Structure beats random: every closure's error at most the random median's, every in-scope
cell. (L) The read-distortion closure's relative advantage over the energy closure, pooled over
in-scope cells at each rank, at least M2, and at least -TOL2 in every in-scope cell. (S) The pooled
advantage below the scope (ranks 16 and 32) is smaller than the pooled advantage inside it. (N)
The in-scope pooled advantage at the run's two resolutions differs by at most TOL_N. (R) Records:
the eigen-direction closure against the energy closure in scope; the full-rank remainder.

## 2. World

D7's world with fresh seeds. Pilot (seed 20261035): two seeded fields at n = 64 and 96, snapshots at
t = 1 and 2, cutoffs 8 and 16, sixteen snapshot cells, 64 rank cells of which 32 in scope. Run (seed
20261036): three fresh fields at n = 96 and 128, twenty-four snapshot cells, 96 rank cells of which
48 in scope. Spectrum k^3 exp(-(k / 6)^2) at amplitude 5, viscosity 0.0005, time step 0.002 at n = 64
scaled with n, probe step 1e-6 of the largest coefficient, eight random draws. Probe seed 20261034,
unused: no separate probe was run, D7's probe standing for an unchanged estimator.

## 3. Estimators

`d7_closure.py`, D7's file unchanged (self-test PASS on Atlas 2026-09-10 in D7's registration: the
blind probe against the tangent solver at 1.3e-7). Grader `d7v2_grade.py`; tolerance fixer
`d7v2_fix_tols.py`.

## 4. Errors and nulls

Deterministic given the seeds. The null is the random closure; the classical control is the
energy closure. Tolerances are fixed from the pilot by the rules of Section 5.

## 5. Bars (M2, TOL2, TOL_N FIXED FROM THE PILOT before sealing; R_MIN = 64 declared; Section 7)

- E1: every closure's error at most the random median's, every in-scope cell.
- L2: the read-distortion closure's relative advantage over the energy closure, pooled over
  in-scope cells, at least M2 at every rank 64 and above (M2 = half the pilot's in-scope pooled
  advantage, rounded down to 0.01, at least 0), and at least -TOL2 in every in-scope cell (TOL2 =
  1.25 times the pilot's largest in-scope shortfall, rounded up to 0.01).
- S1: the pooled advantage over the cells below the scope is smaller than the pooled advantage
  inside it.
- N1: the in-scope pooled advantage at the run's two resolutions differs by at most TOL_N (1.5
  times the pilot's change between its two resolutions, rounded up to 0.01).
- R1: the eigen-direction closure's median advantage over the energy closure in scope and its
  count of cells behind; the full-rank remainder, reported.

Pass: E1, L2, S1, N1. Fail: E1 failing (a structured closure worse than random); the
read-distortion closure behind the energy closure pooled at every in-scope rank. Otherwise
INDETERMINATE.

## 6. What falsifies

L2 is falsified by the energy closure matching the read-distortion closure at the ranks where D7
found them to separate, which would mean the consumer's sensitivity adds nothing to amplitude
even when there is a choice. S1 is falsified by the advantage being as large below the scope as
inside it, which would make the declared scope an arbitrary cut rather than the boundary of a
regime. N1 failing says the margin is a resolution artefact.

## 7. Self-test, probe, pilot (before sealing)

Self-test: D7's, the file being unchanged.

Probe: none separate; D7's probe (`experiments/OD/D7/probe.json`) stands.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261035, two fields at n = 64 and 96,
sixteen snapshot cells, Atlas 2026-09-10, 06:24 to 06:30 UTC). Every quantity exists. In scope (32
rank cells at ranks 64 and 128): the read-distortion closure ahead of the energy closure pooled by
5.5 percent (3.8 at rank 64, 7.2 at rank 128; 4.5 at k_c = 8, 6.5 at k_c = 16; 6.0 at n = 64, 5.0 at
n = 96), behind it in 7 of the 32 cells, at worst by 11.6 percent (field 11 at n = 64, t = 1, k_c = 8,
rank 128, 0.212 against 0.190) and ahead by up to 20 percent (field 11 at n = 64, t = 2, k_c = 16,
rank 128, 0.384 against 0.482); so M2 = 0.02, TOL2 = 0.15 and TOL_N = 0.02 by the rules. Below the
scope (32 cells at ranks 16 and 32) the pooled advantage is 1.0 percent, so S1 holds on the pilot
by a factor of five. Recorded: the eigen-direction closure behind the energy closure in 27 of the
32 in-scope cells, by a median of 22 percent; the full-rank remainder 0.025 at the median and at
most 0.075 at k_c = 8, and at most 0.002 at k_c = 16; the random closure at 0.85 to 1.00. The
pilot's own rows give PASS under the fixed tolerances (`pilot_grade.json`); the run decides on
three fresh fields at n = 96 and 128.

## 8. Sealing procedure

1. Pilot on Atlas; fix the tolerances; record them in Sections 5 and 7; commit `pilot.json`,
   `tolerances.json`.
2. Rename this file to `PREREG-D7V2.md`, commit, record its blob hash in the track document and
   the README status ledger.
3. Run on the run seed, grade with `d7v2_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the second version of `OD:closure-geometry`.
