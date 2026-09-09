# PREREG D2v4: observer-relative hubness, the law with the discovery set widened to d = 256 and heavy tails

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V4.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v4 of the OD track, the
successor of D2v3 (sealed, INDETERMINATE).

## 1. Claim under test

D2v3 put manifold worlds into the discovery set and its law, with the intrinsic dimension as
its main term, fitted every real corpus within its own pilot error; it missed the per-world
limit on a full-dimensional cube at d = 256, where the TwoNN estimator reads 125 on 4,000
points and the law extrapolated beyond anything the set had shown it, and on heavy tails at
N = 16000. This gate registers the repair the D2v3 record named: full-dimensional clouds at
d = 256 and heavy-tailed clouds in the discovery families, the same feature family and search,
and the frozen D2, D2v2 and D2v3 laws as competitors.

(L) The law, discovered on the widened set and frozen, transfers without refitting to unseen
families (now including clouds at d = 512 and heavy tails at d = 256), to fresh real slices and
to larger N, and beats all four competitors on the transfer groups. (X), (P), (B) as before.

## 2. World

Observers, k, N, budget cells as in D2v3. Training worlds: D2v3's 25 with the cube at d = 256
moved in from the unseen group, plus Gaussian clouds at d = 256 (exponents 0 and 1), Student t
with 3 degrees of freedom at d = 64 and 128, and Laplace at d = 64 (31 worlds). Held-out worlds:
D2v3's, with Student t with 3 degrees moved to d = 96 and a Gaussian at exponent 0.5, d = 192
added (9 worlds), under unseen observer spectra. Unseen families (run only): log-normal, the
sphere, a two-scale mixture, Student t with 2.5 degrees at d = 32, a steep Gaussian, the three
unseen manifolds of D2v3, Laplace at d = 128 and 192, the cube and a Gaussian at d = 512, and
Student t with 4 degrees at d = 256 (12 worlds). Real corpora (run only): fresh slices of the
two Wikipedia parts, SIFT base and SIFT queries. Scale cells (run only): Gaussian, Student t with
5 and with 3 degrees, the Fourier manifold, Wikipedia and SIFT at N = 12000 to 16000.

## 3. Estimators

As in D2v3, with the frozen D2v3 law added to the competitors and to the self-test.

## 4. Errors and nulls

As in D2v3. REF is the frozen law's error pooled over every pilot row.

## 5. Bars (REF = 1.065 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled; L3
  real corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the competitors, pooled over the transfer groups: at most 0.8 times the nominal
  competitor's error, 0.8 times the D2 law's, 0.9 times the D2v2 law's and 0.95 times the D2v3
  law's, and within each group at most each competitor's.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, X1 and P1 hold. Fail: pooled unseen error above 3 REF, or any competitor's
pooled error below the law's on the transfer groups, or X1 failing in more than half the
worlds. Otherwise INDETERMINATE.

## 6. What falsifies

As in D2v3, with the D2v3 law as a competitor: a widened discovery set that does not improve
the transfer to full-dimensional clouds beyond the set or to heavy tails at scale, or that
costs the fit on real corpora that D2v3 achieved.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2v3's self-test (PASS) and the frozen D2v3 law applying with its
published coefficients. PASS.

Probe (`probe.json`, `probe.log`, seed 20261001, the cube at d = 256, Student t with 3 degrees at
d = 64, and a held-out Gaussian at d = 192): every quantity exists; the cube's cross-observer
matrix has effective rank 8.1 against a null of 23.9, the highest ratio of any full-dimensional
world so far, and the heavy-tailed cloud 2.5; hub-set overlap across orientations 0.23 to 0.45
against 0.06 to 0.28 across spectra.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20261002, 31 training and 9 held-out worlds,
2,556 law rows, Atlas 2026-09-09). The search over the same declared family froze the law

    log(1 + skew) = -1.0938 +0.1685 cv_r sqrt(d_eff) -0.0319 log(d_nom) log(k) +0.7014 log(id_twonn)

(features `cv_r_x_sqrt_d_eff`, `log_d_nom_x_log_k`, `log_id_twonn`, transform log1p), held-out
error 0.812, training error 1.097, pooled 1.065 = REF. The intrinsic dimension stays the main
term with the coefficient D2v3 found (0.70 against 0.75); the concentration term is now the
spread of the centroid distances times the root of the spectral dimension, and a small
nominal-dimension product enters with a negative sign, the first time any registration's law
has used the nominal dimension. REF is larger than D2v3's 0.747 because the training rows now
hold the hardest worlds: Laplace at d = 64, where no law of the family fits (the new law 3.86,
D2v2 2.88, D2v3 3.06, skewness up to 13.6), and Student t with 3 degrees at d = 128 (1.93,
skewness up to 15.7). On the worlds the widening was for, the cube at d = 256 (0.98 against the
D2v3 law's 2.56) and the Gaussian at d = 256 (1.03 against 2.72), the law fits where D2v3's did
not, and on the held-out heavy tails at d = 96 it errs by 1.03 where D2v3's law errs by 3.30.
Pooled over the pilot the competitors err by 2.62 (nominal), 2.72 (D2), 1.43 (D2v2) and 1.13
(D2v3). The nominal competitor,

    skew = -0.9877 +0.8221 log(d_nom) -0.1377 log(d_nom) log(k) +0.2548 log(k),

has held-out error 2.87. Effective-rank ratios run from 0.09 to 0.67, so FRAC_X = 0.90 by the
cap; the cube at d = 256 reads 0.34, the highest of any full-dimensional world. Hub-set overlap
across orientations exceeds the overlap across spectra in all 40 worlds. Budget sweep as
before. The pilot's own rows hold every bar the pilot can reach (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V4.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v4_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
