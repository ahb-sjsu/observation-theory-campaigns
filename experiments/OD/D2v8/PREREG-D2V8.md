# PREREG D2v8: observer-relative hubness, the excess law with full-dimensional worlds at d = 384 to 512 in the discovery set

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V8.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v8 of the OD track, the
successor of D2v7 (sealed, INDETERMINATE).

## 1. Claim under test

D2v7 changed the target of the hubness law to the log Poisson hub excess and, on D2v6's
world, held the heavy tails at d = 256, the Gaussian at d = 512, the real corpora and the
heavy tails at N = 16000 at once; it missed the cube at d = 512 by a factor of 2.3, the one
full-dimensional world beyond its training dimensions, and its record named the coverage
repair. D2v6 showed that coverage does not help the skewness family, whose errors moved
between the heavy tails and the clouds. This gate asks whether coverage helps the excess
family, whose errors did not: full-dimensional clouds at d = 384 and 512 join the training
worlds, the uniform cube and an isotropic Gaussian at d = 384, the cube and a Gaussian with
covariance exponent 0.5 at d = 512, so that an unseen cube at d = 448 and an unseen ball at
d = 384 are bracketed in dimension; the isotropic Gaussian at d = 512 stays unseen, one
exponent away from a training world; and a cube at d = 640 sits one step beyond the set.

Target, errors, pool, search and bars are D2v7's. The frozen D2v7 law predicts the same
quantity and is carried as a third competitor at 0.95, beside the nominal-only law and the
chance level at 0.8.

(L) The law, discovered on this set and frozen, transfers without refitting to the bracketed
full-dimensional worlds, to the cube one step beyond, to D2v7's other unseen families, to
fresh real slices and to larger N, and beats all three competitors on the transfer groups.
(X), (P), (B) as before.

## 2. World

D2v7's worlds with four training worlds added (41 training, 9 held-out), the unseen cube
moved from d = 512 to 448 and two unseen worlds added (17 unseen), 4 real slices (fresh: both
Wikipedia slices from part 003 at offsets 0 and 500,000, SIFT base from 8,000,000, SIFT
queries from 6,000, the last overlapping earlier gates' windows), 8 scale cells (the
Wikipedia cell from part 004 at 300,000). 79 worlds; seeds 20261013 (probe), 20261014
(pilot), 20261015 (run).

## 3. Estimators

As in D2v7, with the frozen D2v7 law added to the competitors and to the self-test.

## 4. Errors and nulls

As in D2v7: root-mean-square differences in log excess; REF the frozen law's error pooled
over every pilot row.

## 5. Bars (REF = 0.365 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled; L3
  real corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the competitors, pooled over the transfer groups: at most 0.8 times the nominal
  competitor's error, 0.8 times the chance level's and 0.95 times the D2v7 law's, and within
  each group at most each competitor's.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, X1 and P1 hold. Fail: pooled unseen error above 3 REF, or any competitor's
pooled error below the law's on the transfer groups, or X1 failing in more than half the
worlds. Otherwise INDETERMINATE.

## 6. What falsifies

The claim is that the excess family, unlike the skewness family, takes coverage without
paying for it elsewhere. It is refuted if a law discovered with the clouds at d = 384 and 512
in the set holds them and loses the heavy tails, the real corpora or the scale cells that
D2v7 held, which is D2v6's outcome in the new target; or if the D2v7 law, frozen without
those worlds, is the better predictor pooled on the transfer groups, which is D2v6's fail
clause. It is confirmed in the useful sense if the bracketed cube at d = 448 and ball at
d = 384 fit inside the per-world limit and everything D2v7 held still holds. The cube at
d = 640, one step beyond the set, says whether the law extrapolates in dimension under this
target as D2v4's did under the skewness.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2v7's self-test (PASS) and the frozen D2v7 law applying with
its published coefficients. PASS.

Probe (`probe.json`, `probe.log`, seed 20261013, the cube at d = 384, the Gaussian with
exponent 0.5 at d = 512, and the unseen cube at d = 448): every quantity exists. The excess
on the new worlds runs from 1.0 under the steepest readers to 18 to 21 under the isotropic
ones, the same range as the clouds at d = 256, so the coverage adds dimension and not target
range; the TwoNN intrinsic dimension reads 157 (cube at 384), 143 (Gaussian at 512) and 169
(cube at 448) under the isotropic reader against spectral dimensions of 350, 261 and 403, the
regime beyond d = 256 where D2v7's law over-predicted the cube. Effective rank 7.0 to 9.2
against nulls of 23.9, ratios of 0.29 to 0.38, the highest of any full-dimensional worlds in
the track and well below the cap; hub-set overlap across orientations 0.21 to 0.25 against
0.05 to 0.08 across spectra.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20261014, 41 training and 9 held-out worlds,
3,276 law rows, Atlas 2026-09-09). The search over the declared family froze the law

    log(excess) = -0.9502 -0.0099 / hill_rk +0.2190 log(d_eff) +0.3664 sqrt(id_twonn)

(features `inv_hill_rk`, `log_d_eff`, `sqrt_id_twonn`, identity transform), held-out error 0.266,
training error 0.375, pooled 0.365 = REF, a factor of 1.44. Three things are recorded before the
run. First, the search chose a neighbour-distance tail variable for the first time in the
track: the reciprocal of the Hill log-excess of the k-th neighbour distance replaces D2v7's
concentration term, with the spectral and intrinsic dimensions kept; D2v5 put the variable in
the pool and every search since declined it, and it enters now that the training rows hold
clouds at d = 384 to 512, where the neighbour-distance tail separates a light-tailed
full-dimensional cloud from a heavy-tailed one at the same dimensions. Second, the frozen
D2v7 law errs by 0.332 pooled over the same pilot rows, less than the new law's 0.365, though
the new law leads held-out (0.266 against 0.250 the other way; the held-out worlds are
D2v7's own). On the worlds the coverage was for, the new law is the better fit in sample
(cube at d = 384 0.58 against 0.68, cube at d = 512 0.66 against 0.83, the Gaussian at d = 512
0.51 against 0.61, the Gaussian at d = 384 0.33 against 0.39); on the heavy tails it is the
worse (Student t with 3 degrees at d = 256 0.37 against 0.22, at d = 128 0.44 against 0.28)
and on the balls (0.55 and 1.05 against 0.29 and 0.67). Third, therefore, the excess family
shows the trade-off D2v6 found in the skewness family, milder by a factor of about three in
log excess but of the same sign: coverage of the clouds beyond d = 256 moves error onto the
heavy tails. Section 6's first clause is in play at the pilot, and the run decides it on the
transfer groups; the sharp bar is L5 against the D2v7 law at 0.95, which the pooled pilot
rows already fail. The nominal competitor,

    log(excess) = -21.85 +200.78 / d_nom +5.808 log(d_nom) -0.5930 sqrt(d_nom),

has held-out error 0.863. Effective-rank ratios run from 0.09 to 0.68 (the held-out ball at
d = 96; the clouds at d = 384 to 512 read 0.29 to 0.38), so FRAC_X = 0.90 by the cap. Hub-set
overlap across orientations exceeds the overlap across spectra in all 50 worlds. Budget sweep
as before. The pilot's own rows hold every bar the pilot can reach (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V8.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v8_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
