# PREREG D7v3 (DRAFT, NOT SEALED): the read-distortion closure of a filtered flow inside its rank scope, on a finer resolution ladder

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D7v3 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the third registration of D7, registered after D7v2.
Its bars and its tolerance rules were fixed in code (`d7v3_grade.py`, `d7v3_fix_tols.py`) before
its pilot ran; this text was written after the pilot and before the seal, and Section 7 records
the pilot.

## 1. Claim under test

D7v2 (`experiments/OD/D7v2/PREREG-D7V2.md`, INDETERMINATE) established that at closure rank 64
and above the read-distortion closure beats the energy closure, pooled by 2.1 percent at rank 64
and 8.1 percent at rank 128, and by nothing below the scope, so the scope is the regime where
the closure has a choice among modes of comparable energy. It missed the convergence bar: the
in-scope margin was 6.5 percent at n = 96 and 3.7 percent at n = 128, a change of 2.7 against an
allowed 2.0, and the margin fell with resolution where on D7's draw it had risen. D7v2's record
named the repair: a finer ladder, n = 128 against 192, to say whether the margin settles or keeps
falling. This registration is that repair and nothing else.

The claim is D7v2's, Sections 1 to 4 of `PREREG-D7V2.md` unchanged and incorporated by reference
(the world, the blind probe, the four closures, the error, the rank scope R_MIN = 64 and the bars
E1, L2, S1, N1 with the records R1), on a ladder one step finer: the pilot at n = 96 and 128, the
resolutions of D7v2's run, and the run at n = 128 and 192. The cutoffs stay at 8 and 16 and the
ranks at 16 to 128, so the subfilter space grows with n and the closure's choice widens.

## 2. World

D7's world with fresh seeds (probe 20261048 unused, pilot 20261049, run 20261050). Pilot: two
seeded fields at n = 96 and 128, snapshots at t = 1 and 2, cutoffs 8 and 16, sixteen snapshot
cells, 64 rank cells of which 32 in scope. Run: three fresh fields at n = 128 and 192, twenty-four
snapshot cells, 96 rank cells of which 48 in scope. Time step 0.002 at n = 64 scaled with n.

## 3. Estimators

`d7_closure.py`, D7's file unchanged. Grader `d7v3_grade.py`, D7v2's unchanged. Tolerance fixer
`d7v3_fix_tols.py`, D7v2's unchanged.

## 4. Errors and nulls

D7's, unchanged.

## 5. Bars (M2, TOL2, TOL_N FIXED FROM THE PILOT before sealing; R_MIN = 64 declared; Section 7)

D7v2's bars verbatim: E1, L2 (pooled advantage at least M2 at every in-scope rank, no in-scope
cell behind by more than TOL2), S1 (the pooled advantage below the scope smaller than inside it),
N1 (the in-scope pooled advantage at the run's two resolutions differing by at most TOL_N), and
the records R1. M2 = half the pilot's in-scope pooled advantage rounded down to 0.01, at least 0;
TOL2 = 1.25 times the pilot's largest in-scope shortfall rounded up to 0.01; TOL_N = 1.5 times the
pilot's change between its two resolutions rounded up to 0.01.

Pass: E1, L2, S1, N1. Fail: D7v2's. Otherwise INDETERMINATE.

## 6. What falsifies

D7v2's Section 6. What the finer ladder adds: N1 holding at n = 128 against 192 with a tolerance
fixed from the change at 96 against 128 says the margin settles; N1 failing again, with the
margin still falling, says the read-distortion advantage is a coarse-resolution effect that the
continuum does not keep, which is a boundary of the claim and not of the instrument.

## 7. Self-test, probe, pilot (before sealing)

Self-test: D7's, the file being unchanged.

Probe: none separate; D7's probe stands.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261049, two fields at n = 96 and 128,
sixteen snapshot cells, Atlas 2026-09-10, 13:18 to 13:29 UTC, the process paused for a few minutes
while the machine cooled). Every quantity exists. In scope (32 rank cells at ranks 64 and 128): the
read-distortion closure ahead of the energy closure pooled by 5.5 percent (3.3 at rank 64, 7.7 at
rank 128; 5.0 at n = 96, 6.0 at n = 128), behind it in 4 of the 32 cells by at most 3.4 percent and
ahead by up to 20 (field 12 at n = 128, t = 2, k_c = 8, rank 128, 0.174 against 0.219); so M2 = 0.02,
TOL2 = 0.05 and TOL_N = 0.02 by the rules, the change between the pilot's resolutions being 1.0
percent and upward. Below the scope (32 cells at ranks 16 and 32) the pooled advantage is 0.7
percent. Recorded: the eigen-direction closure behind the energy closure in 27 of the 32 in-scope
cells by a median of 17 percent; the full-rank remainder 0.023 at the median and at most 0.074 at
k_c = 8, and at most 0.002 at k_c = 16; the random closure at 0.94 to 1.00. The pilot's own rows
give PASS under the fixed tolerances (`pilot_grade.json`); the run decides on three fresh fields
at n = 128 and 192.

## 8. Sealing procedure

1. Pilot on Atlas; fix the tolerances; record them in Sections 5 and 7; commit `pilot.json`,
   `tolerances.json`.
2. Rename this file to `PREREG-D7V3.md`, commit, record its blob hash in the track document and
   the README status ledger.
3. Run on the run seed, grade with `d7v3_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the third version of `OD:closure-geometry`.
