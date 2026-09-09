# PREREG D2: observer-relative hubness, the law

Status: SEALED 2026-09-09 by the rename to `PREREG-D2.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2 of the OD track; its paper
is the draft *Hub Relativity* (Bond 2026).

## 1. Claim under test

An observer O = (C, G, B) reads a point cloud X through the distance
d_O(x, x')^2 = (x - x')^T C^T G C (x - x') at resolution B, and the k-occurrence of a point,
H_k(x | O), is the number of other points whose k nearest neighbours under d_O include it. That
"a change of representation changes hubness" is known (Radovanovic, Nanopoulos and Ivanovic
2010; hubness reduction by local scaling and mutual proximity, Schnitzer et al. 2012;
Feldbauer and Flexer 2019). The gate's claims are the law and the latent rank:

(L) The law. Within a family of observers with declared spectra and random orientation, the
hubness of a cloud under an observer, measured by the skewness of the k-occurrence
distribution, is a low-complexity function of spectral summaries of the observed covariance
Sigma_obs = C Sigma_data C^T (an effective dimension first), of N and of k, and not of the
nominal dimension; the function, discovered on Gaussian clouds and frozen, transfers without
refitting to distributions it was not discovered on, to real embeddings, and to a larger N,
and it beats the best function of the nominal dimension at the same complexity.

(X) The latent rank. The cross-observer hubness matrix H[i, j] = H_k(x_i | O_j) over N points
and M observers has an effective rank far below that of a matrix whose columns are the same
counts with the points' identities shuffled.

(P) Polarity. Changing the observer's spectrum changes which points are hubs more than
changing its orientation at a fixed spectrum: the hub sets of two observers overlap less (a
smaller Jaccard index) across spectra than across orientations. Direct reversals, hub under
one observer and anti-hub under another, are counted and reported; the probe found them rare
at N = 4000 under the fixed thresholds (one to three points in ten thousand), too rare to grade.

(B) Budget, exploratory. Coarsening the observer's resolution changes polarity monotonically
in the resolution, and small resolutions change nothing.

## 2. World

Observers C = diag(i^-alpha) R with R a Haar-random rotation drawn by seed, G = I, alpha on
0, 0.25, 0.5, 1, 1.5, 2 with four rotations each (M = 24 per world), and for the held-out
worlds alpha on 0.1, 0.75, 1.25 (unseen spectra). Budget B = 0 for the law; the budget cells
quantize the observed coordinates at B equal to 0.1, 0.25, 0.5, 1, 2 times the observed median
nearest-neighbour distance, for alpha 0 and 1 at one rotation. k on 5, 10, 20, the law's k
being 10; N = 4000 unless stated.

Training worlds (law discovery, pilot; fresh seeds on the run): Gaussian clouds with
covariance eigenvalues i^-alpha_data, alpha_data on 0, 0.5, 1 and d on 32, 64, 128, plus
alpha_data 0.5, d 64 at N = 2000. Held-out worlds (law scoring, pilot; fresh seeds on the run):
Gaussian with alpha_data 0.25 and 0.75 at d 48 and 96 under the unseen spectra. Unseen
families (run only, never run before the seal): uniform cube, uniform ball, Student t with 3
degrees of freedom, a four-centre Gaussian mixture, an anisotropic cube, at d 64, and the
cube at 32, the ball at 128, the Student at 32. Real corpora (run only): 4000 Cohere
multilingual-v3 Wikipedia embeddings (1024 dimensions, `/archive/tqp_real/wiki1024`, rows
100000 on) and 4000 SIFT descriptors of BigANN (128 dimensions, `/archive/tqp_bigann`, rows
100000 on). Scale cells (run only): the alpha_data 0.5, d 64 Gaussian at N = 16000 and the
Wikipedia embeddings at N = 12000 (rows 300000 on), two rotations per alpha.

## 3. Estimators

Exact k-nearest-neighbour search under each observer's distance (blocked, self excluded);
counts H_k; the hubness statistics of the program's instrument (openvector-bench,
`hubness.py`): skewness of the counts, the busiest point's count over the Poisson ceiling for
N points each querying once with k slots, the share of slots held by the busiest one percent,
the anti-hub fraction. Polarity: hub when the standardised count is at least 2, anti-hub when
the count is 0. Variables of the law per (world, observer, k): d_eff, the participation ratio
of the observed covariance's eigenvalues; d_ent, the exponential of their entropy; the top
eigenvalue's share; the coefficient of variation of pairwise distances in a 512-point sample;
d_nom, N, k.

The law family. A model is c_0 + c_1 f_1 (+ c_2 f_2) with f from a declared pool of 27
features (logs, roots and inverses of the variables and a few declared products and ratios),
fitted by least squares on the training rows and ranked by root-mean-square error on the
held-out rows; the best model with at most two terms is the law. The competitor is the best
model of the same form whose features involve only d_nom, N and k. Both are frozen at the
pilot into `law.json` and never refitted. (Theory-radar's engine searches formula
classifiers scored by F1; this gate's target is a real number, so the search above is its
regression form with the same shape, enumeration of a declared family scored on held-out
data, and the G5 recovery of the program's own evaluation metric over the criteria is deferred
to a later gate.)

## 4. Errors and nulls

The law's error on a group of rows is its root-mean-square error against the measured
skewness. The reference error is the frozen law's held-out error at the pilot. The latent-rank
null shuffles each column of H independently, destroying point identity while keeping every
column's distribution. Polarity reversal fractions are computed over all pairs of observers of
a world, split by whether the pair shares its spectrum.

## 5. Bars (REF = 0.796 and FRAC_X = 0.48 fixed from the pilot; `tolerances.json`; Section 7)

- L1, fresh seeds. On the run's training and held-out worlds (fresh seeds, the same families
  and spectra) the frozen law's error is at most 1.5 times its held-out error at the pilot,
  REF.
- L2, unseen families. On every unseen world the frozen law's error is at most 2 REF, and
  pooled over the unseen group at most 1.5 REF.
- L3, real corpora. On each real corpus the frozen law's error is at most 3 REF.
- L4, scale. On each scale cell the frozen law's error is at most 2 REF.
- L5, against the nominal dimension. Pooled over the unseen, real and scale groups the frozen
  law's error is at most 0.8 times the frozen competitor's error.
- X1, latent rank. In every world the standardised cross-observer matrix's effective rank is
  at most FRAC_X times the shuffled null's.
- P1, polarity. In every world with at least one same-spectrum pair, the mean Jaccard overlap
  of hub sets over same-spectrum pairs exceeds that over different-spectrum pairs; reversal
  fractions are reported.
- B1, budget, exploratory (reported, not graded): the fraction of points whose polarity
  changes is non-decreasing in the relative resolution, and at 0.1 it is at most 0.05.

Tolerance rule. REF is the frozen law's root-mean-square error pooled over every pilot row,
training and held-out (the draft said the held-out error alone; the pilot showed the held-out
worlds easier than the training worlds, 0.37 against 0.80 pooled, so a fresh-seed bar at 1.5
times the held-out error would have failed on the training worlds by construction, and the
pooled error is the reference the fresh-seed bar must be read against). FRAC_X is 1.5 times the
pilot's largest ratio of effective ranks, rounded up to two decimals, at most 0.9. The
multiples 1.5, 2, 3 and 0.8 are declared here, before any unseen, real or scale cell runs.

Pass: L1 to L5, X1 and P1 hold. Fail: the frozen law's pooled error on the unseen group above
3 REF (the law does not transfer), or the competitor's pooled error below the law's on those
groups (nominal dimension predicts as well), or X1 failing in more than half the worlds.
Otherwise INDETERMINATE.

## 6. What falsifies

A frozen law that fails on distributions it was not discovered on, on real embeddings, or at
a larger N; a nominal-dimension formula that predicts as well; a cross-observer matrix no
lower in rank than its shuffled null; spectra that change the hub sets no more than orientations do.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): exact neighbour search against brute force; counts summing to
N k and the Poisson ceiling above the mean; an alpha = 0 observer leaving counts unchanged
(rotation invariance); d_eff 31.4 for an isotropic cloud at d = 32 and 1.17 under alpha = 2;
skewness rising from -0.31 at d = 4 to 5.03 at d = 64 on isotropic Gaussians (the classical
effect); a planted law recovered exactly by the search; effective rank 1 for a rank-one matrix
and near min(N, M) for a random one. PASS.

Probe (`probe_v1.json`, seed 20260918, one training and one held-out world, 2026-09-09
15:30 UTC): every quantity exists and moves. Under the isotropic Gaussian at d = 32, skewness
falls monotonically along the observer ladder from 4.18 (alpha 0, d_eff 31.7) to 0.23 (alpha 2,
d_eff 1.2), the Poisson excess from 8.9 to 1.1, the anti-hub fraction from 0.114 to 0.003; the
standardised cross-observer matrix has effective rank 2.6 against 23.9 for its shuffled null.
Direct hub-to-anti-hub reversals are rare, one to three points in ten thousand per pair, so the
polarity bar was restated on the overlap of hub sets before the pilot (Section 1, P), and the
polarity record gained the Jaccard indices.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20260919, ten training and four held-out
worlds, 864 law rows, Atlas 2026-09-09 15:34 to 15:37 UTC). The search over the declared
family, fitted on the training rows and ranked on the held-out rows, froze the law

    skew = -0.0262 + 0.4207 / cv_d + 0.8172 sqrt(d_eff) / k

(features `inv_cv_d`, `sqrt_d_eff_over_k`), held-out error 0.372, training error 0.856, pooled
0.796 = REF; and the competitor over nominal-dimension features

    skew = -4.0031 + -0.0798 d_nom + 1.4604 sqrt(d_nom)

with held-out error 1.784 and pooled error 1.863. The law is the paper's causal chain in one
line, distance concentration (the inverse coefficient of variation of pairwise distances under
the observer) and the effective dimension of the observed covariance per neighbour, and it
carries no nominal dimension. Per world the law's error runs from 0.26 to 1.70, the largest in
the alpha_data 0.5, d 64 world whose skewness reaches 8.5 at k = 5. Effective-rank ratios of
the standardised cross-observer matrix to its shuffled null run from 0.11 to 0.31, so
FRAC_X = 0.48. Hub-set overlap across orientations at a fixed spectrum exceeds the overlap
across spectra in every world (Jaccard 0.29 to 0.41 against 0.12 to 0.23). Budget sweep
(alpha_data 0.5, d 64): the fraction of points whose polarity changes is non-decreasing in the
relative resolution for both observers (0.12, 0.22, 0.37, 0.86, 0.86 under alpha 0; 0.04, 0.07,
0.12, 0.22, 0.85 under alpha 1) and a resolution of a tenth of the nearest-neighbour distance
already changes the polarity of 12 percent of points under the isotropic observer, so the
exploratory expectation that small budgets change nothing is already contradicted; recorded,
not graded. Grading the pilot's own rows with `d2_grade.py` at these tolerances holds every bar
the pilot can reach (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe_v1.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed (fresh seeds, unseen families, real corpora, scale cells), grade with
   `d2_grade.py results.json --tols tolerances.json`, commit `results.json` and `grade.json`
   as executed, enter the registry tests in `claims/transformations/OD.toml`.
