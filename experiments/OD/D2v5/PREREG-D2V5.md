# PREREG D2v5: observer-relative hubness, the law with a tail variable measured on the neighbour distances

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V5.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v5 of the OD track, the
successor of D2v4 (sealed, INDETERMINATE).

## 1. Claim under test

D2v4 widened the discovery set to full-dimensional clouds at d = 256 and heavy tails, and its
law extrapolated to d = 512, fitted the real corpora within half its pilot error and beat every
earlier law; it missed the per-world limit on Student t with 4 degrees at d = 256 (3.52) and
Laplace at d = 192 (4.75), heavier tails at higher dimension than the set held. The record named
the reason: the feature family's only tail variable was the excess kurtosis of the observed
coordinates, which the observer's rotation drives toward the Gaussian value (Laplace at d = 192
read 0.04 under every observer) and which the search never chose. This gate registers the repair
the record named first: a tail variable measured where the hubness mechanism lives, on the
distribution of neighbour distances in the observed space, and, second, heavy tails placed at
the transfer dimensions in the discovery set.

Four scale-free tail variables join the pool, each computed from the k-nearest-neighbour
distances the instrument already finds: the ratio of the 99th to the 50th percentile of the
k-th neighbour distance (tail_knn) and of the first (tail_r1), the excess kurtosis of log r_k
(kurt_lrk), and the Hill log-excess of r_k over its upper 5 percent (hill_rk, the reciprocal of
the Hill tail index). Each enters with the family's transforms (identity, log, square root,
reciprocal; log(3 + x) for the kurtosis), and three products with the spectral and intrinsic
dimensions join the products list, 79 features in all. The family, the search and the target
are otherwise D2v4's.

(L) The law, discovered on this set and frozen, transfers without refitting to unseen families
(Student t with 4 degrees at d = 256, Laplace at d = 192, Student t with 2.5 degrees at d = 128,
a log-normal at d = 192, the cube and a Gaussian at d = 512, and D2v4's other unseen worlds), to
fresh real slices and to larger N including Laplace at N = 12000, and beats all five
competitors on the transfer groups. (X), (P), (B) as before.

## 2. World

Observers, k, N, budget cells as in D2v4. Training worlds: D2v4's 31 plus Student t with 4
degrees at d = 192 and Laplace at d = 128 (33 worlds). Held-out worlds: D2v4's 9 under unseen
observer spectra. Unseen families (run only): D2v4's 12 plus Student t with 2.5 degrees at
d = 128 and a log-normal at d = 192 (14 worlds). Real corpora (run only): fresh slices, both
Wikipedia slices from part 002 (offsets 0 and 500,000), SIFT base from offset 2,000,000, and
SIFT queries from offset 0; the query file holds 10,000 rows, so this window overlaps D2v2's by
3,000 rows and is the one slice that is not fresh. Scale cells (run only): D2v4's 6 plus Laplace
at d = 64 and N = 12000 (7 cells). 67 worlds; seeds 20261004 (probe), 20261005 (pilot), 20261006
(run).

## 3. Estimators

As in D2v4, with the tail variables of Section 1 in the pool and the frozen D2v4 law added to
the competitors and to the self-test. The self-test also checks that the tail variables order a
ball, a Gaussian and Student t with 3 degrees by tail weight, that they do not change under a
rescaling of the cloud, and that a rotated Laplace cloud at d = 128 reads a coordinate kurtosis
near zero while its neighbour-distance tail sits above the Gaussian's.

## 4. Errors and nulls

As in D2v4. REF is the frozen law's error pooled over every pilot row.

## 5. Bars (REF = 0.878 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled; L3
  real corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the competitors, pooled over the transfer groups: at most 0.8 times the nominal
  competitor's error, 0.8 times the D2 law's, 0.9 times the D2v2 law's, 0.95 times the D2v3
  law's and 0.95 times the D2v4 law's, and within each group at most each competitor's.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, X1 and P1 hold. Fail: pooled unseen error above 3 REF, or any competitor's
pooled error below the law's on the transfer groups, or X1 failing in more than half the
worlds. Otherwise INDETERMINATE.

## 6. What falsifies

A tail variable on the neighbour distances that the search does not choose, or a law that
chooses it and still misses the heavy-tailed worlds at d = 256 and 192, refutes the record's
diagnosis that the missing variable was the tail; a law that fits them and loses the real
corpora or the d = 512 clouds that D2v4 reached refutes the claim that the tail can be added
without cost. Any competitor beating the law on the transfer groups fails the gate.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2v4's self-test (PASS); the tail variables order the ball, the
Gaussian and Student t (tail_knn 1.04, 1.21, 4.71; hill_rk 0.006, 0.036, 0.357) and are
unchanged by a rescaling; a rotated Laplace cloud at d = 128 reads kurt_1d 0.07 against the
Gaussian's 0.00 while its tail_knn reads 1.16 against 1.09 and hill_rk 0.029 against 0.016;
the frozen D2v4 law applies with its published coefficients. PASS.

Probe (`probe.json`, `probe.log`, seed 20261004, Student t with 4 degrees at d = 192, Laplace
at d = 128, and the held-out Student t with 3 degrees at d = 96): every quantity exists. The
tail variables read the tail the coordinate kurtosis cannot: Laplace at d = 128 has kurt_1d
0.07 under every observer while tail_knn runs from 1.17 (isotropic reader) to 2.74 (exponent
2) and hill_rk from 0.031 to 0.263; Student t with 4 degrees at d = 192 has tail_knn 3.10 to
6.11 and hill_rk 0.277 to 0.479. The tail variables rise with the observer's exponent in every
world, as the reader compresses the cloud onto fewer directions, so they carry the observer
as well as the family; the products with the spectral dimension are in the pool for that.
Hubness skewness runs to 17.9 (t4) and 13.8 (Laplace) on the isotropic readers. Effective rank
2.3 to 4.1 against nulls of 12.0 to 23.9; hub-set overlap across orientations 0.33 to 0.48
against 0.15 to 0.26 across spectra.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20261005, 33 training and 9 held-out worlds,
2,700 law rows, Atlas 2026-09-09). The search over the declared family, with the four tail
variables and their transforms and products in the pool, froze the law

    skew = -2.8023 -0.5096 / cv_d +1.1905 log(id_twonn) +1.0670 sqrt(d_eff)

(features `inv_cv_d`, `log_id_twonn`, `sqrt_d_eff`, identity transform), held-out error 0.709,
training error 0.899, pooled 0.878 = REF. The search did not choose a tail variable. That is the
first outcome Section 6 names, and it is recorded before the run rather than after: the best
model of the family that contains a neighbour-distance tail variable (`tail_check.json`, an
annotation and not a bar) is skew = -1.684 +3.246 / tail_r1 +1.478 sqrt(d_eff) -0.716 / cv_d with
held-out error 0.752 against the frozen law's 0.709 and pooled error 0.974 against 0.878, and it is
worse than the frozen law on five of the eight heavy-tailed pilot worlds (Student t with 4
degrees at d = 192: 2.18 against 1.73). Within a linear family of at most three terms, the tail
of the neighbour distances adds nothing the concentration and dimension terms do not already
carry; the probe showed why, the tail variables rise with the observer's exponent in every
world, so they measure the reader as much as the family. The frozen law is D2v3's form (the
intrinsic dimension, the spectral dimension and a concentration term) refitted with heavy
tails at the transfer dimensions in the training rows: its coefficient on log(id_twonn) is
1.19 against D2v3's 0.75 under the log1p transform, and it returns to the untransformed
target. On the pilot rows it beats every competitor pooled (nominal 2.67, D2 2.64, D2v2 1.56,
D2v3 0.932, D2v4 1.21 against 0.878), the margin over the D2v3 law being 6 percent, inside the
0.95 that L5 demands on the transfer groups. On the heavy-tailed training worlds it errs by
1.73 (Student t with 4 degrees at d = 192) and 2.32 (Laplace at d = 128), in sample, against
the D2v4 law's 1.55 and 3.59. The nominal competitor,

    skew = 28.182 -0.1653 d_nom -17.943 log(d_nom) +7.294 sqrt(d_nom),

has held-out error 2.38. Effective-rank ratios run from 0.09 to 0.68 (the held-out ball at
d = 96), so FRAC_X = 0.90 by the cap. Hub-set overlap across orientations exceeds the overlap
across spectra in all 42 worlds. Budget sweep as before. The pilot's own rows hold every bar
the pilot can reach (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V5.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v5_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
