# PREREG D6v3: sensor placement as the choice of an observer under a budget, with feasibility at the cap and a tie-break for the exact search

Status: SEALED 2026-09-10 by the rename to `PREREG-D6V3.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D6v3 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the third registration of D6, registered after D6v2. Its
bars, its tolerance rules and its two definitions were fixed in code (`d6v3_placement.py`,
`d6v3_grade.py`, `d6v3_fix_tols.py`) before its pilot ran; this text was written after the pilot
and before the seal, and Section 7 records the pilot.

## 1. Claim under test

D6v2 (`experiments/OD/D6v2/PREREG-D6V2.md`, INDETERMINATE) closed the cell D6 had lost to the
energy ranking and missed by two single cells that its record called definitions: a required
count that the exact search proved unreachable under the sensor cap while the full sensor set
reaches it, which the feasibility test (the full set reaching the count) does not see; and a
horizon 10.3 percent shorter than the energy placement's against a tolerance of 10.0, because
the smallest sensor set is not unique and the exact search returned the first in index order
where D6's greedy breaks ties by the m-th eigenvalue. D6v2's record named both repairs and said
they were definitions, not a claim. This registration is those two definitions on D6v2's claim,
with everything else unchanged and incorporated by reference (`PREREG-D6.md` Sections 1 to 4 for
the world, the read operator, the baselines, the exhaustive reference and the horizon;
`PREREG-D6V2.md` Section 1 for the selector).

The two definitions. First, among the smallest sensor sets reaching the count, the exact search
returns the one whose window Gramian has the largest m-th eigenvalue, the eigenvalue that has to
clear the threshold, then the first in index order; this is greedy's tie-break, applied to the
exact search. Second, a cell is feasible when the full sensor set reaches the count and the count
is not proved unreachable under the cap: where every subset size up to the cap is under the
reference's limit of 200,000 subsets, the exact search decides, and a cell in which it finds no set
of at most 12 sensors reaching the count is recorded as unreachable at the cap and not graded;
where a size exceeds the limit before the count is reached the question is open and the cell is
graded as before, the pruned greedy standing in.

The claim is D6v2's: the spectrum places sensors. The selector never needs more sensors than the
energy ranking, a random ordering or D6's greedy, needs strictly fewer than the energy ranking in
a registered fraction of the cells where placement matters, and leaves a longer forecast horizon
than the energy placement at the same count.

## 2. World

D6's five worlds with fresh seeds (probe 20261042, pilot 20261043, run 20261044): the diffusion
chain, the Lorenz-96 Jacobian and the shallow-water grid at n = 16, 16 and 20 on the pilot, at
n = 20, 20 and 24 with the unseen advection-diffusion chain and the unseen Lorenz-96 at F = 10 and
n = 24 on the run; window 0.5, rho = 1, cap 12, thresholds frac in {0.001, 0.01, 0.1}, counts m in
{4, 6, 8, 10}.

## 3. Estimators

`d6v3_placement.py`, D6v2's file with the tie-break in `exact_subset` and the feasibility record
`feasible_at_cap` per cell. Self-test: D6v2's eight checks and one more, the exact search
reporting the count reachable at the cap on the chain at m = 4 with the selector's length.

## 4. Errors and nulls

D6's: exact given the seeds; randomness in the sensor draw and the random placements;
tolerances fixed from the pilot by the rules of Section 5.

## 5. Bars (FACTOR = 1.3, PHI = 0.25, TOL_H = 0.05, MARGIN_H = 0.1 fixed from the pilot; `tolerances.json`; Section 7)

D6v2's seven bars on the feasible cells as defined in Section 1, with D6's rules: E1 (antitone
count); P1 (the selector reaches m in every feasible cell); G1 (the selector's count within FACTOR
of the exhaustive minimum where checkable, FACTOR = 1.25 times the pilot's largest ratio rounded
up to 0.1, at least 1.0); C1 (the energy ranking never reaches m with fewer sensors; the selector
strictly fewer in at least PHI of the discriminating cells, PHI = half the pilot's fraction
rounded down to 0.05); C2 (never more than the median random ordering); H1 (the horizon never
shorter than (1 - TOL_H) times the energy placement's, TOL_H = 1.25 times the pilot's largest
shortfall rounded up to 0.05; pooled advantage over the discriminating growth cells at least
MARGIN_H, half the pilot's rounded down to 0.05); C3 (never more sensors than D6's greedy). The
cells unreachable at the cap are counted and listed.

Pass: all seven. Fail: as D6 (a ratio above 2 anywhere; the energy ranking needing fewer sensors
in more than a tenth of the feasible cells; the pooled horizon advantage negative). Otherwise
INDETERMINATE.

## 6. What falsifies

D6's Section 6, unchanged. What the two definitions add: a selector at the cap without the count
in a feasible cell is now the pruned greedy's failure in an open cell, since a checkable cell
cannot show it; and a horizon shorter than the energy placement's at the same count can no
longer be laid to the tie-break, so it is the spectrum's.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS.

Probe (`probe.json`, `probe.log`, seed 20261042, the three pilot worlds, Atlas 2026-09-10, 13:16 to
13:28 UTC). Every quantity exists; 31 of 36 cells feasible, none unreachable at the cap. The exact
search is slower than D6v2's, since it now enumerates a whole subset size to break ties instead
of stopping at the first set that reaches the count.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261043, the three families at n = 16,
16 and 20, Atlas 2026-09-10, 13:28 to 13:41 UTC). 31 of 36 cells feasible, none unreachable at the
cap (every subset size up to 12 is under the reference's limit on these worlds, so the exact
search decided every cell); the selector equal to the exhaustive minimum in all 31, so FACTOR = 1.3
by the rule from a largest ratio of 1.00. Placement matters in 14 cells; the selector needs
strictly fewer sensors than the energy ranking in 7 of those 14 (0.50; on the diffusion chain at
frac 0.001 and m = 8 and 10, 4 and 5 against 5 and 6, and at frac 0.01 and m = 8, 5 against 6; on
Lorenz-96 at frac 0.001 and m = 6 and 10, 2 and 5 against 3 and 6, at frac 0.01 and m = 4 and 6, 2
and 3 against 3 and 7, and at frac 0.1 and m = 4, 4 against 6; on shallow water at frac 0.01 and
m = 8 and 10, 4 and 5 against 6 and 8; ties elsewhere), and the energy ranking needs fewer in no
cell, so PHI = 0.25 by the rule. The selector needs fewer sensors than D6's greedy in one cell
(the diffusion chain at frac 0.01 and m = 8, 5 against 6) and more in none. On the seven growth
cells the selector's horizon is shorter than the energy placement's in one, by 1.4 percent
(Lorenz-96 at frac 0.001 and m = 4, 0.503 against 0.511, one sensor each), so TOL_H = 0.05 by the
rule; pooled over the four discriminating growth cells the selector's horizon exceeds the energy
placement's by 27.7 percent and the random placements' by 18.1 percent, so MARGIN_H = 0.10 by
the rule. The pooled advantage is larger than D6v2's pilot found (8.6 percent on a different
sensor draw, so the two are not a controlled comparison); the tie-break's effect on the run is
what H1 measures. The pilot's own cells give
PASS under the fixed tolerances (`pilot_grade.json`); the run decides on fresh draws at n = 20,
20 and 24 and the two unseen worlds, where the Lorenz-96 at n = 24 is beyond the reference's
limit from subset size 7 and the question of feasibility at the cap is open there.

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7;
   commit `probe.json`, `pilot.json`, `tolerances.json`. Done.
2. Rename this file to `PREREG-D6V3.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d6v3_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the third version of `OD:observer-choice`.
