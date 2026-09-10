# PREREG D6v2: sensor placement as the choice of an observer under a budget, with the spectrum tested without greedy's slack

Status: SEALED 2026-09-10 by the rename to `PREREG-D6V2.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D6v2 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the rehabilitation of D6, registered after the track's
declared order was complete. Its bars and tolerance rules were fixed in code (`d6v2_grade.py`,
`d6v2_fix_tols.py`) before its pilot ran; the selector was revised once at the pilot, before the
seal, and Section 7 records both pilots.

## 1. Claim under test

D6 (`experiments/OD/D6/PREREG-D6.md`, INDETERMINATE) missed by two single cells of 55, and both
misses were greedy's and not the spectrum's: in one cell greedy reached the sensor cap without
the count while the all-sensor placement reaches it; in one unseen cell the energy ranking found
the exhaustive optimum with one sensor fewer than greedy. D6's record named the repair, "the
exhaustive optimum where feasible and greedy beyond, a repair of the selector and not of the
claim". This registration is that repair. The claim is D6's, Sections 1 to 4 of `PREREG-D6.md`
unchanged and incorporated here by reference, with one term replaced: the registered selector.

The registered selector. For a required count m at threshold c, the selector returns the
smallest sensor set reaching d_obs at least m by exhaustive search in index order over subsets
of size 1, 2, ... up to the cap of 12, wherever every subset size up to the answer has at most
200,000 subsets, the same cap as the exhaustive reference; where a size exceeds the cap before
the count is reached, it returns the shorter of two greedy placements pruned of every sensor
whose removal keeps the count, D6's greedy on the spectrum and a pair-greedy that adds the best
single sensor if one completes the count and otherwise the best pair, greedy's on a tie. On the
pilot worlds (16 to 20 candidates) the selector is exact in every cell; on the run worlds the
Lorenz-96 at n = 24 exceeds the cap from size 7, and there the pruned greedy stands in. D6's greedy
is computed in every cell beside the selector and recorded, and the selector is required never to
need more sensors than it (bar C3).

Every other term is D6's: the exact window Gramian as the placement's read operator, d_obs by
Theorem 2, the energy ranking and random placements as baselines at the same count and by the
count they need, the exhaustive reference, the forecast horizon on the growth worlds; the bars E1,
P1, G1, C1, C2 and H1 of D6 applied to the registered selector's placement, with tolerances fixed
from this registration's own pilot by D6's rules.

## 2. World

D6's world with fresh seeds: the diffusion chain, the Lorenz-96 Jacobian and the shallow-water
grid at n = 16, 16 and 20 on the pilot (seed 20261032), at n = 20, 20 and 24 with the unseen
advection-diffusion chain and the unseen Lorenz-96 at F = 10 and n = 24 on the run (seed 20261033);
window 0.5, rho = 1, cap 12, thresholds frac in {0.001, 0.01, 0.1}, counts m in {4, 6, 8, 10}.
Probe seed 20261031.

## 3. Estimators

`d6v2_placement.py`, D6's file with the selector of Section 1 added (`exact_subset`, `prune`,
`pair_greedy`, `lookahead`) and D6's greedy kept and recorded per cell. Self-test: D6's seven
checks and one more, the selector never longer than greedy on a chain at m = 4 and m = 8.

## 4. Errors and nulls

D6's: exact given the seeds; randomness in the sensor draw and the random placements;
tolerances fixed from the pilot by the rules of Section 5.

## 5. Bars (FACTOR = 1.3, PHI = 0.30, TOL_H = 0.10, MARGIN_H = 0.00 fixed from the pilot; `tolerances.json`; Section 7)

D6's bars on the registered selector's placement, with D6's rules: E1 (antitone count); P1 (the
selector reaches m in every feasible cell); G1 (the selector's count within FACTOR of the
exhaustive minimum where checkable, FACTOR = 1.25 times the pilot's largest ratio rounded up to
0.1, at least 1.0); C1 (the energy ranking never reaches m with fewer sensors; the selector
strictly fewer in at least PHI of the discriminating cells, PHI = half the pilot's fraction
rounded down to 0.05); C2 (never more than the median random ordering); H1 (the horizon never
shorter than (1 - TOL_H) times the energy placement's, TOL_H = 1.25 times the pilot's largest
shortfall rounded up to 0.05; pooled advantage over the discriminating growth cells at least
MARGIN_H, half the pilot's rounded down to 0.05). Added: C3, the selector never needs more
sensors than D6's greedy in any feasible cell; the cells where it needs fewer are recorded.

Pass: E1, P1, G1, C1, C2, H1, C3. Fail: as D6 (a ratio above 2 anywhere; the energy ranking
needing fewer sensors in more than a tenth of the feasible cells; the pooled horizon advantage
negative). Otherwise INDETERMINATE.

## 6. What falsifies

D6's Section 6, unchanged. What the selector adds: with the search's slack removed wherever the
search is checkable, an energy ranking that reaches the count with fewer sensors than the
selector, or a selector at the cap without the count, is the spectrum's failure and not greedy's;
and G1 is exact by construction where the selector is exact, so its content on the run is the
Lorenz-96 at n = 24, where the pruned greedy stands in.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS.

First probe and pilot (`first_pilot/`, seeds 20261031 and 20261032), with the selector as first
built, the shorter of the pruned greedy and the pruned pair-greedy without the exact search: 31 of
36 pilot cells feasible, placement mattering in 14, the selector strictly ahead of the energy
ranking in 9 of those and behind in none; the selector equal to D6's greedy in every cell,
including the one cell where greedy is one sensor over the exhaustive optimum (Lorenz-96 at
frac 0.001 and m = 8, 4 against 3). A selector that matches greedy where greedy misses does not
test the spectrum without the slack, so the exact search under the reference's cap was put in
front of it, declared here before the second pilot; the first pilot's files are kept and not
graded.

Probe (`probe.json`, `probe.log`, seed 20261031, the three pilot worlds, Atlas 2026-09-10, with the
exact selector). Every quantity exists; 31 of 36 cells feasible, Lorenz-96 losing five at the
higher thresholds as in D6.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261032, the three families at n = 16,
16 and 20, Atlas 2026-09-10, 06:34 to 06:41 UTC). 31 of 36 cells feasible; the selector is exact
in all 31 (the largest subset size searched is within the cap on every pilot world), so its count
equals the exhaustive minimum everywhere and FACTOR = 1.3 by the rule from a largest ratio of
1.00. Placement matters in 15 cells (the median random ordering needs more sensors than the
selector); the selector needs strictly fewer sensors than the energy ranking in 10 of those 15
(0.67; on the diffusion chain at frac 0.01 and m = 8 and 10, 6 and 8 against 7 and 10, and at
frac 0.1 and m = 8 and 10; on shallow water at frac 0.01 and m = 8 and 10, 4 and 5 against 6 and 8;
on Lorenz-96 at frac 0.001 and m = 8 and 10, 3 and 5 against 5 and 6, at frac 0.01 and m = 6, 3
against 5, and at frac 0.1 and m = 4, 4 against 6), and the energy ranking needs fewer in no cell,
so PHI = 0.30 by the rule. The selector needs fewer sensors than D6's greedy in one cell, the one
where the first pilot found greedy one over the optimum (Lorenz-96 at frac 0.001 and m = 8, 3
against 4), and more in none. On the seven growth cells the selector's horizon is shorter than
the energy placement's in three, by 1.0, 6.1 and 2.5 percent (Lorenz-96 at frac 0.001 and m = 4
and 6, and at frac 0.01 and m = 4, cells where the two placements need the same count or nearly),
so TOL_H = 0.10 by the rule; pooled over the five discriminating growth cells the selector's
horizon exceeds the energy placement's by 8.6 percent and the random placements' by 10.4 percent,
so MARGIN_H = 0.00 by the rule (half of 0.086 rounded down to 0.05), and H1's pooled clause on
the run is that the advantage is not negative. The exact selector, which takes the first
smallest set in index order, does not pick among equally small sets by the m-th eigenvalue as
greedy does, and its horizon is a few percent shorter than greedy's in some cells for that reason
(0.58 against 0.63 at frac 0.001 and m = 6); the registration keeps the selector as declared and
records this. The pilot's own cells give PASS under the fixed tolerances (`pilot_grade.json`); the
run decides on fresh draws at n = 20, 20 and 24 and the two unseen worlds, where the Lorenz-96 at
n = 24 is beyond the cap from subset size 7 and the pruned greedy stands in.

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7;
   commit `probe.json`, `pilot.json`, `tolerances.json`, and the first pilot's files. Done.
2. Rename this file to `PREREG-D6V2.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d6v2_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test in
   `claims/transformations/OD.toml` as the second version of `OD:observer-choice`.
