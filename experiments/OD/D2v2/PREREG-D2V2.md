# PREREG D2v2: observer-relative hubness, the law with a shape variable

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V2.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v2 of the OD track, the
successor of D2 (sealed, FAIL).

## 1. Claim under test

D2 froze a hubness law on Gaussian clouds in the spectral summaries of the observed covariance
and the concentration of pairwise distances, and the law did not transfer: it over-predicted
hubness on round clouds (uniform balls, Wikipedia embeddings at effective dimension 156 with
skewness at most 1.1) and under-predicted it on heavy tails (Student t). The D2 record named
the repair: a variable that separates shape from spectrum, and a discovery set of more than
one family. This gate registers that repair and tests it the same way.

(L) The law. Within the observer family of D2, the hubness of a cloud under an observer
(skewness of the k-occurrence counts) is a low-complexity function of quantities measured on
the observed cloud alone, spectral summaries of its covariance together with shape summaries
that do not depend on the family it was drawn from, and of N and k; discovered on seven
families at once and frozen, it transfers without refitting to families it was not discovered
on, to real embeddings and to larger N, and it beats both the best nominal-dimension formula
and the frozen D2 law on the transfer groups.

(X) The latent rank and (P) polarity as in D2, on every world. (B) Budget, exploratory, as in
D2.

## 2. World

Observers as in D2: C = diag(i^-alpha) R, G = I, alpha on 0, 0.25, 0.5, 1, 1.5, 2 with four
rotations (M = 24), the held-out worlds under alpha 0.1, 0.75, 1.25; k on 5, 10, 20, the law's
k being 10; N = 4000 unless stated; budget cells as in D2.

Training families (discovery, pilot; fresh seeds on the run), each at d = 32, 64, 128:
Gaussian with covariance exponent 0, 0.5, 1; uniform cube; uniform ball; Student t with 5
degrees of freedom; a four-centre Gaussian mixture; plus the Gaussian at exponent 0.5, d = 64,
N = 2000 (22 worlds). Held-out worlds (ranking, pilot; fresh seeds on the run), under unseen
observer spectra: Gaussian at exponents 0.25 (d 48) and 0.75 (d 96), Student t with 3 degrees
of freedom (d 64), ball (d 96), anisotropic cube (d 96), an eight-centre mixture (d 48), cube
at d 48 and N 2000 (7 worlds). Unseen families (run only, never run before the seal): Laplace
(d 64 and 128), log-normal coordinates (d 64), the unit sphere (d 64), a two-scale mixture
(d 64), Student t with 2.5 degrees of freedom (d 32), the cube at d 256, Gaussian at exponent
1.5 (d 64). Real corpora (run only): 4000 Cohere Wikipedia embeddings from rows 500000 on of
part 000 and 4000 from rows 200000 on of part 001, 4000 BigANN SIFT base descriptors from
rows 500000 on, and 4000 BigANN SIFT query descriptors, a different distribution of the same
space. Scale cells (run only, two rotations per alpha): Gaussian at exponent 0.5 and Student
t with 5 degrees of freedom at N = 16000, Wikipedia at N = 12000, SIFT at N = 16000.

## 3. Estimators

Neighbour search, counts, hubness statistics, polarity, the cross-observer matrix and the
spectral variables as in D2. Shape variables, measured on the observed cloud with no knowledge
of its family: the coefficient of variation, skewness and excess kurtosis of the distances to
the centroid; the mean excess kurtosis of the observed coordinates; the TwoNN intrinsic
dimension (Facco et al. 2017, trimmed at the 90th percentile of the ratio, as the program's
`corpus_geometry` does); the coefficient of variation over points of the k-th neighbour
distance; the relative contrast, the mean pairwise distance over the mean k-th neighbour
distance.

The law family. A model is c_0 + sum of up to three terms c_i f_i with f from a declared pool
of 66 features (each base variable, its log, root and inverse where positive, shifted logs of
the signed moments, and thirteen declared products and ratios), fitted by least squares on the
training rows either to the skewness or to log(1 + skewness) with the prediction transformed
back, and ranked by root-mean-square error on the held-out rows in skewness; the best model is
the law. Competitors: the best model of the same form in nominal-dimension features only, and
the D2 law with its frozen coefficients. All three are frozen at the pilot into `law.json` and
never refitted.

## 4. Errors and nulls

As in D2. REF is the frozen law's error pooled over every pilot row (training and held-out),
the definition D2 arrived at before its seal.

## 5. Bars (REF = 0.922 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1, fresh seeds: pooled error over the run's training and held-out worlds at most 1.5 REF.
- L2, unseen families: at most 2 REF per world and 1.5 REF pooled.
- L3, real corpora: at most 3 REF per corpus.
- L4, scale: at most 2 REF per cell.
- L5, against the competitors: pooled over the unseen, real and scale groups the law's error is
  at most 0.8 times the nominal-dimension competitor's and 0.8 times the frozen D2 law's, and
  within each of those groups the law's error is at most each competitor's.
- X1, latent rank: effective-rank ratio at most FRAC_X in every world, FRAC_X being 1.5 times
  the pilot's largest ratio rounded up to two decimals, at most 0.9 (the pilot now includes
  balls, where D2 found the ratio largest).
- P1, polarity: hub-set overlap across orientations above that across spectra in every world.
- B1, budget: reported, not graded.

Pass: L1 to L5, X1 and P1 hold. Fail: the pooled unseen error above 3 REF, or either
competitor's pooled error below the law's on the transfer groups, or X1 failing in more than
half the worlds. Otherwise INDETERMINATE.

## 6. What falsifies

As in D2, with the frozen D2 law added as a competitor: a law that does not transfer, a
nominal-dimension or a shape-blind formula that predicts as well, a cross-observer matrix no
lower in rank than its null, spectra that change the hub sets no more than orientations.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2's self-test (PASS) and three additions: the shape variables
order a ball, a Gaussian and a Student t with 3 degrees of freedom at d = 32 as expected
(centroid-distance coefficient of variation 0.030, 0.127, 0.715; coordinate excess kurtosis
-0.19, 0.00, 20.3) and the TwoNN dimension of the Gaussian is 32.3; the frozen D2 law applies
with its published coefficients; a planted log(1 + skewness) law is recovered exactly with its
transform. PASS.

Probe (`probe.json`, `probe.log`, seed 20260924, the cube at d = 32 and the held-out Gaussian at
d = 48, 2026-09-09 16:12 UTC): every shape variable exists and moves along the observer ladder
as the observer coarsens (cube: centroid-distance coefficient of variation 0.08 to 0.64, TwoNN
dimension 30 to 9, relative contrast 1.4 to 8.0, skewness 3.5 to 0.3), the coordinate kurtosis
staying at the cube's -0.1 throughout, as a shape variable should under a linear observer.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20260925, 22 training and 7 held-out worlds,
1,836 law rows, Atlas 2026-09-09 16:13 to 16:20 UTC). The search over the declared family, 66
features in up to three terms under two target transforms, fitted on the training rows and
ranked on the held-out rows, froze the law

    log(1 + skew) = 2.8110 + 0.0047 d_ent -0.0928 / cv_d -2.4613 sqrt(top_share)

(features `d_ent`, `inv_cv_d`, `sqrt_top_share`, transform log1p), held-out error 0.448,
training error 0.976, pooled 0.922 = REF. The law contains no shape variable: the search had
seven of them and chose the entropy dimension of the observed covariance, the concentration of
pairwise distances and the top eigenvalue's share, under the transform that compresses large
skewness; the shape variables were available and did not improve the held-out ranking. Whether
that is enough for the shapes the training set did not contain is the run's question. The
nominal-dimension competitor,

    skew = -0.1596 -0.7847 / k -0.3991 log(k / N)

(no dimension term survived the held-out ranking), has held-out error 1.972 and pooled 2.043;
the frozen D2 law has held-out error 2.468 and pooled 2.128. Per world the law's error runs from
0.19 to 1.97, the largest on Student t at d = 128 whose skewness reaches 13; on the balls, where
D2's law erred by up to 4.5, the new law errs by 0.44 to 0.95. Effective-rank ratios run from
0.09 (Student t) to 0.67 (the ball at d = 96), so FRAC_X = 0.90 by the cap. Hub-set overlap
across orientations exceeds the overlap across spectra in all 29 worlds (0.11 to 0.47 against
0.03 to 0.29). Budget sweep as in D2. The pilot's own rows hold every bar the pilot can reach
(`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V2.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v2_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
