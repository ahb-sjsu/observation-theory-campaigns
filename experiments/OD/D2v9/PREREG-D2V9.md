# PREREG D2v9: observer-relative hubness, the boundary of the excess law

Status: SEALED 2026-09-10 by the rename to `PREREG-D2V9.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v9 of the OD track, the
successor of D2v8 (sealed, FAIL).

## 1. Claim under test

This gate registers a boundary, not a new law. Eight registrations (D2 to D2v8) and an
exploration on their rows (`experiments/OD/D2v9_explore/README.md`) placed the frozen D2v7 law

    log(excess) = -1.1032 - 0.0253 / cv_knn + 0.1666 log(d_eff) + 0.4338 sqrt(id_twonn)

at the frontier of the declared family on this world: twelve family shapes (products of tail
and dimension, four terms, softened reciprocals, the divergent terms removed, a concentrated
world held out) each moved its error and none removed it, and none beat the D2v7 law pooled on
the transfer groups. The exploration also named the boundary. The law's concentration term is
a reciprocal of the coefficient of variation of the k-th neighbour distance on the observed
data, cv_knn; on over-concentrated worlds under near-isotropic readers, where every point's
neighbours sit at almost the same distance, the term diverges and the law predicts an excess
near zero. The uniform ball at d = 384 under the isotropic reader reads cv_knn 0.003, six times
below the Gaussian's at the same dimension, and an excess of 1.4 against the law's 0.1; at
readers with exponent 0.5 and above the same ball reads cv_knn above 0.03 and fits within the
law's usual error. The boundary is a property of rows, not of worlds: the same world is inside
the scope under one reader and outside it under another.

The claim. Let the scope be the rows with cv_knn at least TAU = 0.015. Inside the scope, the
frozen D2v7 law, applied without change, predicts the log Poisson hub excess on fresh worlds,
fresh real slices and larger N within the limits of Section 5, and beats the nominal-only law
and the chance level; outside the scope the law is not claimed, and its error there exceeds
the in-scope limit, which is what makes the scope a boundary and not a convenience. The
threshold is declared here, before the pilot, from the collected rows: at 0.015 the
out-of-scope rows of the D2v7 and D2v8 runs are 87 of 4,644 and 156 of 5,076, every one a
full-dimensional cloud or ball under a reader with exponent at most 0.25, no world is wholly
outside, and the law's in-scope error pooled is 0.30 and 0.32 against 0.31 and 0.35 unmasked.

The scope does not cover the second miss of the record. Laplace at d = 64 and N = 12000, a
scale cell, sits inside the scope under every reader and the law under-predicts it by a factor
of three to four under the isotropic reader (0.656 against a limit of 0.655 on D2v7's seed, 0.92
on D2v8's), while Student t at the same N fits. The law carries no term in N, and the Laplace
family at scale is where that shows. That cell stays in the world with its bar unchanged; it is
the risk this gate carries, and a miss there is recorded as INDETERMINATE, not absorbed by the
scope. A scope that excluded it would be a convenience.

(L) inside the scope: L1 to L5 as in D2v7. (S) the boundary: S1. (X), (P), (B) as before,
unchanged by the scope.

## 2. World

D2v8's 79 worlds with an unseen ball at d = 256 added (80 worlds: 41 training, 9 held-out
under unseen observer spectra, 18 unseen families, 4 real slices, 8 scale cells), fresh seeds
and fresh real slices (both Wikipedia slices from part 004 at offsets 600,000 and 800,000, the
scale Wikipedia cell from part 002 at 900,000, SIFT base from 10,000,000 and 11,000,000, SIFT
queries from 3,000, the last overlapping earlier gates' windows since the query file holds
10,000 rows). The training and held-out groups exist only to fix REF and to test L1 on fresh
seeds; there is no search. Seeds 20261016 (probe), 20261017 (pilot), 20261018 (run).

## 3. Estimators

The D2v8 workload unchanged (`d2v9_hubness.py`); `law.json` is D2v7's law file verbatim, the
law, its nominal-only competitor and the chance level, with the scope recorded beside it.
The grader `d2v9_grade.py` masks rows by scope: every L bar is computed on in-scope rows, a
world's per-world bar applies when it has in-scope rows, and S1 is computed on the out-of-scope
rows pooled over every world. Out-of-scope rows are reported per world with the law's error and
the median sign of its residual. Self-test as D2v8's.

## 4. Errors and nulls

Root-mean-square differences in log excess, as in D2v7. REF is the frozen law's error pooled
over the in-scope pilot rows.

## 5. Bars (REF = 0.319 and FRAC_X = 0.90 fixed from the pilot, TAU = 0.015 declared; `tolerances.json`; Section 7)

- L1 fresh seeds (in-scope training and held-out rows) within 1.5 REF; L2 unseen families
  within 2 REF each on in-scope rows (worlds with in-scope rows) and 1.5 REF pooled; L3 real
  corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the nominal-only law and the chance level, pooled over the in-scope rows of the
  transfer groups: at most 0.8 times each, and within each group at most each.
- S1, the boundary: at least 30 out-of-scope rows exist across the run, and the law's error
  pooled over them exceeds 2 REF.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, S1, X1 and P1 hold. Fail: pooled in-scope unseen error above 3 REF, or either
competitor's pooled in-scope error below the law's on the transfer groups, or the out-of-scope
rows fitting within REF (the scope excluded rows the law predicts, and the boundary claim is
false as stated), or X1 failing in more than half the worlds. Otherwise INDETERMINATE.

## 6. What falsifies

The claim is that the law's failures on this world are a boundary and not a defect: that they
sit on the rows the scope names and nowhere else. It is refuted if in-scope rows miss their
limits on worlds the earlier gates held (the heavy tails, the manifolds, the real corpora, the
clouds at d = 448 to 640 at steeper readers); it is refuted the other way if the out-of-scope
rows fit, in which case the scope was not a boundary. The Laplace scale cell decides between
PASS and INDETERMINATE and is named as such in advance; a miss there says the law has a second
boundary, in N for one family, that this gate does not declare. Nothing in this gate can turn
a FAIL of D2v8 into a PASS of D2v8: the D2v8 law is not in play, and the D2v7 law's errors on
the D2v8 run are on record unmasked (0.44 pooled, the ball at d = 384 at 1.21).

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): D2v8's self-test with the D2v7 law applying. PASS.

Probe (`probe.json`, `probe.log`, seed 20261016, Laplace at d = 128, the cube at d = 512, and
the unseen ball at d = 384): every quantity exists and the scope splits where the collected
rows said it would. Laplace at d = 128 is in scope under every reader (72 of 72 rows, error
0.51). The cube at d = 512 and the ball at d = 384 are out of scope under the readers with
exponent 0 and 0.25 (24 of 72 rows each) and in scope from exponent 0.5 up, where the law reads
them at 0.43 and 0.52, against 0.71 and 1.24 unmasked. On the out-of-scope rows the law misses
in both directions, the ball under-predicted (median residual -0.88 in log excess) and the
cube over-predicted (+1.05), which is why the boundary is stated as "not claimed" and not as a
sign; pooled over the 48 out-of-scope rows the error is 1.62, above 2 REF at any REF the pilot
can return. Effective rank 4.1 to 15.5 against nulls of 23.9 (the ball at 0.65, the highest
ratio of any world in the track, below the cap); hub-set overlap across orientations 0.19 to
0.34 against 0.02 to 0.15 across spectra.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261017, 41 training and 9 held-out
worlds, 3,276 rows, Atlas 2026-09-10; no search). In scope: 3,183 rows; REF = 0.319 pooled over
them, a factor of 1.38 in the excess, against 1.169 for the nominal-only law and 1.624 for the
chance level. Out of scope: 93 rows in seven worlds, every one under a reader with exponent
0.25 or below: the balls at d = 64, 96 and 128 (12 rows each), the torus at m = 8 in d = 64 (12),
and the cubes at d = 256, 384 and 512 (12, 12 and 21). The law's error pooled over them is
0.675, above 2 REF = 0.638, so S1 holds on the pilot rows, by a margin that is recorded as
narrow; and the pilot shows what the declared threshold catches on both sides of the law. It
catches rows the law misses, the cube at d = 384 and 512 under the isotropic reader
over-predicted by a factor of 2.3 to 2.6 and the balls at d = 96 and 128 under-predicted by
0.57 to 0.58 in log excess; and it catches rows the law fits, the ball at d = 64 (0.29), the
torus (0.14) and the cube at d = 256 (0.26). The scope therefore names the regime where the
concentration term is unreliable, not the rows where it is wrong: inside that regime the law
is sometimes right, and the claim withdraws it there anyway. The threshold stays at 0.015 as
declared before the pilot; a threshold tuned to the pilot's rows would be a fit. On the run the
out-of-scope set gains the balls at d = 256 and 384 and the cubes at d = 448 and 640 under the
same readers, where the probe read 2.0 and the D2v8 run read 1.2, and S1 is expected to hold
with room; the bar that decides PASS against INDETERMINATE remains the Laplace scale cell.
Effective-rank ratios run from 0.09 to 0.67 (the held-out ball at d = 96), so FRAC_X = 0.90 by
the cap. Hub-set overlap across orientations exceeds the overlap across spectra in all 50
worlds. Budget sweep as before. The pilot's own rows hold every bar the pilot can reach
(`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; fix REF and FRAC_X; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V9.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v9_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
