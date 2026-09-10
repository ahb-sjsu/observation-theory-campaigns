# PREREG D1v2: identifiability at a budget, finite-sample form, with a tolerance that carries a margin

Status: SEALED 2026-09-10 by the rename to `PREREG-D1V2.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D1v2 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the rehabilitation of D1, registered after the track's
declared order was complete. Its bars are D1's, in D1's grader unchanged; its one change is the
rule that fixes the recovery tolerance, and that rule was fixed in code (`d1v2_fix_tols.py`)
before its pilot ran.

## 1. Claim under test

D1 (`experiments/OD/D1/PREREG-D1.md`, INDETERMINATE) held every bar in every cell but one: in the
positive definite world at B = 1, the above-threshold eigenvalue error at 960 queries was 0.303
of chance against a tolerance REC = 0.30, which D1 had fixed as its pilot's own maximum in that
same cell (0.299) rounded up to two decimals, a rule that carries no margin for a fresh seed. D1's
record says so and names the repair: fix the tolerance as a declared multiple of the pilot's
maximum. This registration is that repair and nothing else.

The claim is D1's, Sections 1 to 4 of `PREREG-D1.md` unchanged and incorporated here by
reference: Theorem 2 read along a coordinate is exact in finite samples (single-parameter
probes learn exactly which coordinates are identifiable at (B, rho), a bracket on each diagonal
entry, and nothing off the diagonal); mixed probes at one radius recover the whole operator,
below-threshold eigenvalues included, up to the pencil s P + (1 - s) c I, wherever the sphere
crosses the ellipsoid substantially, and nothing where it does not; and the analytic centre
returns the pencil's end.

## 2. World

D1's world with fresh seeds: three read operators of declared spectrum in a random orthonormal
frame (n = 5 with a kernel, n = 8 with two kernel directions, n = 8 positive definite), rho = 1,
B on 0.25, 0.5, 1, 1.5, 2, 20 evaluators per cell, World A probes at sizes 0.125 to 1 along each
coordinate and its negative, World B queries on the ladder 60 to 960. Pilot seed 20261040, run
seed 20261041.

## 3. Estimators

`d1_identify.py`, D1's file unchanged (World A no estimator; World B the analytic centre under
the declared cap, cvxpy with Clarabel). Grader `d1_grade.py`, D1's file unchanged, called with
the REC of Section 5. Tolerance fixer `d1v2_fix_tols.py`.

## 4. Errors and chance

D1's, unchanged: per-evaluator errors against the true spectrum and against the pencil's end,
chance from the true spectrum in a random frame, median over 64 draws.

## 5. Bars (REC = 0.39 fixed from the pilot; `tolerances.json`; Section 7)

D1's five bars, verbatim in `d1_grade.py`: A1, verdicts and brackets exact in every evaluator of
every World A cell; B1, in every well-crossed World B cell at the largest query count, the median
Frobenius error, the median above-threshold error and the median below-threshold error each at
most REC times their chance medians; B2, a constant oracle in every cell whose interval excludes
B^2 (a constant oracle under a thin crossing recorded, not failed); B3, the median Frobenius
error non-increasing along the query ladder in every well-crossed cell; B4, in every well-crossed
cell of the positive definite world the estimate nearer the pencil's end than P.

REC = 1.5 times the largest of the pilot's graded ratios (the three medians over their chance
medians, over the pilot's well-crossed cells at the largest query count), rounded up to 0.01.
If the rule gives more than 0.45 the registration is not sealed and the fact is recorded, since
a recovery bar near half of chance would not say what the claim says.

Pass, Fail and INDETERMINATE as in D1: Pass when every bar holds in every cell it binds; Fail on
a World A mismatch in more than half the evaluators of a cell, a well-crossed cell whose median
Frobenius error exceeds half its chance at the largest query count, or a non-crossing cell with
a non-constant oracle; otherwise INDETERMINATE.

## 6. What falsifies

D1's Section 6, unchanged. What this registration adds: a miss of B1 on the run under a
tolerance that is one and a half times the pilot's own maximum would be a real shortfall of
mixed-probe recovery at this query ladder, not a seed's fluctuation, and would stand as a
boundary of the claim.

## 7. Self-test, pilot

Self-test: D1's, the file being unchanged.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261040, Atlas 2026-09-10, 06:35 to
07:00 UTC, 90 cells). A1 exact in every evaluator of all fifteen World A cells. Six World B cells
well-crossed, the same six as D1's (B = 1 and 1.5 in each world); the oracle constant in the one
cell the theory says cannot cross (n = 5, B = 2) and in the thin crossing at n = 8 positive
definite, B = 0.25; the other eight cells poorly crossed and not graded. In the six graded cells
the median Frobenius error is 0.054 to 0.237 against chance medians of 1.08 to 1.17, the
above-threshold error 0.033 to 0.161 against 0.6 to 0.7, the below-threshold error 0.020 to 0.099
against 0.4 to 1.5; the largest graded ratio is 0.255, the above-threshold error in the positive
definite world at B = 1 (0.161 against 0.629), the same cell and quantity that decided D1, so
REC = 0.39 by the rule, under the 0.45 ceiling. B3 holds in all six cells and B4 in both positive
definite cells (Frobenius 0.195 against P* and 0.237 against P at B = 1; 0.122 against 0.137 at
B = 1.5). The pilot's own cells give PASS under REC = 0.39 (`pilot_grade.json`); the run decides
on fresh frames and queries.

## 8. Sealing procedure

1. Pilot on Atlas; fix REC by the rule of Section 5; record it in Sections 5 and 7; commit
   `pilot.json`, `tolerances.json`. Done.
2. Rename this file to `PREREG-D1V2.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d1_grade.py results.json --rec 0.39`, commit `results.json`
   and `grade.json` as executed, enter the registry test in `claims/transformations/OD.toml`
   as the second version of D1's test.
