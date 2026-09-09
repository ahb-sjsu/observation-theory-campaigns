# PREREG D2v3: observer-relative hubness, the law with manifold worlds

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V3.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v3 of the OD track, the
successor of D2v2 (sealed, INDETERMINATE).

## 1. Claim under test

D2v2 froze a hubness law on seven full-dimensional synthetic families and it transferred to
eight further synthetic families and to SIFT descriptors, but not to Wikipedia embeddings,
whose TwoNN intrinsic dimension (8 to 20) sits far below their spectral dimension (up to 320)
and whose hubness is low. The intrinsic dimension was in the declared pool and the search
dropped it, because on full-dimensional discovery families it duplicates the spectral
dimension. This gate registers the repair the D2v2 record named: clouds on embedded manifolds
in the discovery families, so that the intrinsic dimension carries information the spectral
dimension does not.

(L) The law, as in D2v2, discovered on eleven families at once, the four manifold families
among them, and tested without refitting on families, corpora and sizes it was not discovered
on; it must beat the nominal-dimension formula, the frozen D2 law and the frozen D2v2 law on
the transfer groups. (X) latent rank, (P) polarity, (B) budget as in D2v2.

The probe (Section 7) confirmed the premise: the random Fourier embedding of an 8-dimensional
Gaussian in 128 dimensions reads at spectral dimension 54 and intrinsic dimension 12 with
skewness 0.24, which is the Wikipedia signature the D2v2 law could not learn.

## 2. World

Observers, k, N, budget cells as in D2v2. Training families, each at two or three of
d = 32, 64, 128: Gaussian at covariance exponents 0, 0.5, 1; cube; ball; Student t with 5
degrees of freedom; a four-centre mixture; and the manifolds: an m-dimensional Gaussian in a
random m-dimensional subspace with isotropic noise 0.01 (m = 4, 8, 16); a random smooth
nonlinear embedding of an m-dimensional Gaussian through 3d random Fourier features at
bandwidth 0.5 or 1.0 with a Gaussian readout and noise 0.01 (m = 4, 8, 16); a product of m
circles read through the first four harmonics of each angle in a random subspace, a curved
m-manifold of spectral dimension near 8m (m = 2, 4, 8); a two-dimensional swiss-roll sheet with
noise 0.005; 25 training worlds. Held-out worlds (ranking): Gaussian at exponent 0.25, Student
t with 3 degrees, ball at d 96, an eight-centre mixture, a 6-dimensional subspace at d 96, a
12-dimensional Fourier manifold at d 96 and bandwidth 0.75, a 3-circle torus at d 48, and a
noisier 8-dimensional subspace (noise 0.05), all under unseen observer spectra. Unseen families
(run only): Laplace, log-normal, the sphere, a two-scale mixture, Student t with 2.5 degrees, the
cube at d 256, a 12-dimensional subspace at d 256, a 6-dimensional Fourier manifold at d 256
with noise 0.02, a 24-dimensional Fourier manifold at d 128 and bandwidth 1.0, a 5-circle torus
with three harmonics and noise 0.002. Real corpora (run only, fresh slices): Wikipedia rows
900000 on of part 000 and 600000 on of part 001, SIFT base rows 900000 on, SIFT queries rows
5000 on. Scale cells (run only, two rotations per alpha): Gaussian and Student t at N = 16000,
an 8-dimensional Fourier manifold at N = 16000, Wikipedia at N = 12000, SIFT at N = 16000.

## 3. Estimators

As in D2v2: neighbour search, hubness statistics, polarity, the cross-observer matrix, the
spectral and shape variables, the 66-feature family in up to three terms under the identity
and log(1 + skew) transforms, ranked on held-out error and frozen at the pilot. Competitors: the
best nominal-dimension model, the frozen D2 law, the frozen D2v2 law. The self-test checks that
the manifold families read at TwoNN dimension far below the ambient one (TwoNN overestimates
curved manifolds at this sample size, so the curved families are held to 2.5 times their
intrinsic dimension and the flat one to 1.6; the sheet, whose density varies along the spiral,
only to a quarter of the ambient dimension).

## 4. Errors and nulls

As in D2v2. REF is the frozen law's error pooled over every pilot row.

## 5. Bars (REF = 0.747 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled; L3
  real corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the competitors: pooled over the unseen, real and scale groups the law's error is
  at most 0.8 times the nominal competitor's, 0.8 times the frozen D2 law's and 0.9 times the
  frozen D2v2 law's, and within each of those groups at most each competitor's.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, X1 and P1 hold. Fail: pooled unseen error above 3 REF, or any competitor's
pooled error below the law's on the transfer groups, or X1 failing in more than half the
worlds. Otherwise INDETERMINATE.

## 6. What falsifies

As in D2v2, with the frozen D2v2 law added as a competitor: in particular, a law that still
fails on Wikipedia with the intrinsic dimension available and informative on the discovery set.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2v2's self-test (PASS) and the manifold check: at d = 64 and
N = 3000 the 8-dimensional subspace reads TwoNN 10.6 with spectral dimension 8.0; the
8-dimensional Fourier manifold 12.1 with spectral dimension 33; the 4-circle torus with four
harmonics 8.2 with spectral dimension 32; the sheet 7.1 with spectral dimension 2.5. Two
earlier versions of the manifold families were rejected by this self-test before any probe:
noise 0.05 buried the sheet's neighbour structure (TwoNN 33 at m = 2), and the torus read
linearly had spectral dimension equal to its intrinsic one, which is not the case the gate
needs. PASS after the revisions.

Probe (`probe.json`, `probe.log`, seed 20260927, a 4-dimensional subspace at d 64, an
8-dimensional Fourier manifold at d 128, and a held-out 6-dimensional subspace at d 96): the
Fourier manifold reads spectral dimension 54 and TwoNN 12 under the isotropic observer with
skewness 0.24 and Poisson excess 1.2, the Wikipedia signature; the subspaces read spectral and
intrinsic dimension together near m and skewness near zero; the cross-observer matrix has
effective rank 2 to 3 against nulls of 12 to 24; hub-set overlap 0.20 to 0.26 across
orientations against 0.04 to 0.09 across spectra.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20260928, 25 training and 8 held-out worlds,
2,088 law rows, Atlas 2026-09-09). The search over the same declared family as D2v2 froze the law

    log(1 + skew) = -1.4629 -0.0132 / cv_knn +0.7475 log(id_twonn) +0.0686 sqrt(d_eff)

(features `inv_cv_knn`, `log_id_twonn`, `sqrt_d_eff`, transform log1p), held-out error 0.481,
training error 0.781, pooled 0.747 = REF. With the manifold worlds in the discovery set the
search chose the intrinsic dimension as its main term, the concentration of the k-th neighbour
distance and the root of the spectral dimension beside it; on the same rows the frozen D2v2 law
errs by 1.40 pooled and by 1.5 to 2.3 on every manifold world, the frozen D2 law by 2.26 and
the nominal-dimension competitor,

    skew = 4.4244 -0.0006 N -0.0426 log(d_nom) log(k)

by 2.19. Per world the law's error runs from 0.19 to 2.22, the largest on Student t at d = 128
(skewness up to 18.7) and the ball at d = 64 (1.32, where the nominal competitor at 1.54 and
the D2v2 law at 0.99 bracket it); on the manifold worlds 0.19 to 0.63. Effective-rank ratios run
from 0.09 to 0.67 (the ball at d = 96), so FRAC_X = 0.90 by the cap. Hub-set overlap across
orientations exceeds the overlap across spectra in all 33 worlds (0.13 to 0.48 against 0.02 to
0.30). Budget sweep as in D2v2. The pilot's own rows hold every bar the pilot can reach
(`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V3.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v3_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
