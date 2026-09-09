# PREREG D2v7: observer-relative hubness, the law with the Poisson hub excess as the target

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V7.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v7 of the OD track, the
successor of D2v6 (sealed, FAIL).

## 1. Claim under test

Three registrations, D2v4, D2v5 and D2v6, placed the same worlds on both sides of the same
limit, and D2v6's record named the family and not the discovery set as the limit: every law's
largest errors sat where the hubness skewness exceeds 12, on isotropic readers of heavy-tailed
or very high-dimensional clouds, where a linear law in the skewness, under either transform,
cannot turn over. The record said the next registration changes the target or the shape and
not the set. This gate changes the target.

The hubness measure is the Poisson hub excess of the program's instrument: the busiest point's
occurrence count divided by the ceiling that a random assignment of the same N k retrieval
slots would reach (the largest c with N P(Poisson(k) at least c) at least 1). It is the
measure the encyclopedia's hubness entry and the course's chapter 3 report, it carries its own
null (excess 1 is chance), and on the D2v6 run it spans 0.7 to 131 while its logarithm tracks
log(1 + skew) at a correlation of 0.97. The law predicts the log of the excess; errors are
root-mean-square log ratios, so 0.3 is a factor of 1.35; the chance level is the constant 0.
The world, observers, k ladder, budget cells, feature pool (79 features, tail variables
included) and search (at most three terms, ranked by held-out error) are D2v6's, so the two
registrations differ in the target alone. The frozen skew laws of D2 to D2v6 predict a
different quantity and are not competitors; the competitors are the nominal-only law on the
same target and the chance level.

(L) The law, discovered on D2v6's set and frozen, transfers without refitting to the unseen
families including the bracketed heavy tails and the d = 512 clouds that no skew law held at
once, to fresh real slices and to larger N, and beats both competitors on the transfer groups.
(X), (P), (B) as before, unchanged by the target.

## 2. World

D2v6's 73 worlds: 37 training, 9 held-out under unseen observer spectra, 15 unseen families
(run only), 4 real slices (run only; fresh: both Wikipedia slices from part 003 at offsets
250,000 and 750,000, SIFT base from 6,000,000, SIFT queries from 4,000, the last overlapping
earlier gates' windows since the query file has 10,000 rows), 8 scale cells (run only; the
Wikipedia cell from part 004). Seeds 20261010 (probe), 20261011 (pilot), 20261012 (run).

## 3. Estimators

As in D2v6, with the target `log_excess` = log(count_max / ceiling) recorded beside the
skewness for every row, the transform fixed to the identity (the target is already in the
log), and the chance level as a competitor. Self-test adds: planted counts with one point at
three times the ceiling read excess 3 and log excess log 3, the chance level predicts 0, and a
planted law in log excess is recovered exactly.

## 4. Errors and nulls

Errors are root-mean-square differences in log excess. REF is the frozen law's error pooled
over every pilot row. Nulls as before.

## 5. Bars (REF = 0.328 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled; L3
  real corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the competitors, pooled over the transfer groups: at most 0.8 times the nominal
  competitor's error and 0.8 times the chance level's, and within each group at most each
  competitor's.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, X1 and P1 hold. Fail: pooled unseen error above 3 REF, or either competitor's
pooled error below the law's on the transfer groups, or X1 failing in more than half the
worlds. Otherwise INDETERMINATE.

## 6. What falsifies

The claim is that the limit the skew registrations met was the target's shape. It is refuted
if the law in log excess misses the same worlds the skew laws missed, the heavy tails at
d = 256 or the clouds at d = 512, by more than the per-world limit, or misses both sides at
once as no skew law did; it is refuted more simply if the chance level or the nominal law is
the better predictor on the transfer groups. If the law holds the heavy tails and the d = 512
clouds together and the real corpora, the target was the limit and the family is not yet
exhausted. The skewness rows are recorded beside the excess for every world, so the record
can say afterwards, for the same worlds and readers, which target the family fits.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2v6's self-test (PASS, the log1p round-trip check now naming
the transform it tests), the excess target on planted counts, the chance level, and a planted
law in log excess. PASS.

Probe (`probe.json`, `probe.log`, seed 20261010, an isotropic Gaussian at d = 64, the swiss
roll at d = 64, Student t with 3 degrees at d = 256, and the held-out Gaussian at d = 192):
every quantity exists. The excess reads the reader as the skewness did: on the Gaussian at
d = 64 it falls from 10.8 under the isotropic reader to 1.1 under exponent 2; on Student t
with 3 degrees at d = 256 from 106 to 1.1, a range of a hundredfold that the skewness (26 to
0) compressed; on the swiss roll it sits at 0.7 to 1.0, chance or below under every reader,
where the skewness read −0.3 to 0.2. The chance level's own error, the RMS log excess, is
1.54 on the Gaussian, 2.89 on the Student t and 0.16 on the roll, so the bar against it is
demanding where the target is near chance and lenient where it is far above. Effective rank
3.1 to 4.6 against nulls of 12.0 to 23.9; hub-set overlap across orientations 0.27 to 0.44
against 0.09 to 0.22 across spectra; both unchanged by the target, as they must be.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20261011, 37 training and 9 held-out worlds,
2,988 law rows, Atlas 2026-09-09). The search over the declared family froze the law

    log(excess) = -1.1032 -0.0253 / cv_knn +0.1666 log(d_eff) +0.4338 sqrt(id_twonn)

(features `inv_cv_knn`, `log_d_eff`, `sqrt_id_twonn`, identity transform), held-out error 0.272,
training error 0.334, pooled 0.328 = REF, a factor of 1.39 in the excess. The nominal competitor
errs by 1.135 pooled (a factor of 3.1) and the chance level by 1.598 (a factor of 4.9). The
search chose no tail variable and no nominal dimension: the intrinsic dimension carries the
law, with the spectral dimension and the concentration of the k-th neighbour distance beside
it, the three variables the skew registrations chose in turn, now in one law. What the target
changed, in sample: the heavy tails at d = 256 that D2v6's law missed by 5.41 (Student t with
3 degrees) fit at 0.32, Student t with 5 degrees at 0.17, Laplace at d = 192 and 256 at 0.46
and 0.27, and the full-dimensional clouds at d = 256 at 0.31 to 0.61, at once; the training
error is the smallest of any registration relative to its target's range, which here runs
from 0.7 to 88. Where the law loses is stated before the run: on the manifold worlds whose
excess sits at chance (subspaces, the Fourier embeddings at m = 4 and 8, the tori, the swiss
roll, excess 0.7 to 2), the chance level's own error of 0.10 to 0.31 is below the law's 0.12
to 0.39, because a law that must also reach 88 over-predicts a world that never leaves 1;
those worlds are a minority of every transfer group's rows, and L5 is pooled by group, so the
bar stands as declared. The nominal competitor,

    log(excess) = 0.6166 -0.000145 N +0.0089 k +0.0915 sqrt(d_nom),

has held-out error 0.912. Effective-rank ratios run from 0.09 to 0.68 (the held-out ball at
d = 96), so FRAC_X = 0.90 by the cap; ratios and hub-set overlaps are the same numbers D2v6's
pilot read on these worlds, as they must be, the target not entering them. Hub-set overlap
across orientations exceeds the overlap across spectra in all 46 worlds. Budget sweep as
before. The pilot's own rows hold every bar the pilot can reach (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V7.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v7_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
