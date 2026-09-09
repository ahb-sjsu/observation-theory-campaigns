# PREREG D2v6: observer-relative hubness, the law with heavy tails placed at the transfer dimensions

Status: SEALED 2026-09-09 by the rename to `PREREG-D2V6.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D2v6 of the OD track, the
successor of D2v5 (sealed, INDETERMINATE).

## 1. Claim under test

D2v4's record named two repairs for its misses on heavy tails at higher dimension than its
discovery set held. D2v5 registered the first, a tail variable measured on the neighbour
distances, and its search declined the variable: within a linear family of at most three terms
the tail of the neighbour distances added nothing the concentration and dimension terms did
not carry. This gate registers the second: the heavy tails are placed in the discovery set at
the dimensions the transfer asks about, so that every unseen heavy-tailed world sits between
training worlds in tail weight or in dimension rather than beyond them.

Student t with 3 and with 5 degrees at d = 256 join the training worlds and bracket the
unseen Student t with 4 degrees at d = 256 in tail weight. Laplace at d = 192 and at d = 256
join and bracket an unseen Laplace at d = 224 in dimension. An unseen Student t with 6 degrees
at d = 192 sits between the training t with 5 degrees at d = 128 and t with 4 degrees at
d = 192. The pool, the search and the target are D2v5's, tail variables included; the
search decides again whether it wants them now that the training rows hold the worlds that
were missed.

(L) The law, discovered on this set and frozen, transfers without refitting to the bracketed
heavy-tailed worlds, to D2v5's other unseen families, to fresh real slices and to larger N,
and beats all six competitors on the transfer groups. (X), (P), (B) as before.

## 2. World

Observers, k, N, budget cells as in D2v5. Training worlds: D2v5's 33 plus Student t with 3
and with 5 degrees at d = 256 and Laplace at d = 192 and 256 (37 worlds). Held-out worlds:
D2v5's 9 under unseen observer spectra. Unseen families (run only): D2v5's 14 with the Laplace
moved from d = 192 to d = 224, plus Student t with 6 degrees at d = 192 (15 worlds). Real
corpora (run only): fresh slices, both Wikipedia slices from part 002 beyond the D2v5 windows
(offsets 250,000 and 750,000), SIFT base from offset 4,000,000, SIFT queries from offset 2,000
(the query file holds 10,000 rows; this window overlaps earlier gates' windows and is the one
slice that is not fresh). Scale cells (run only): D2v5's 7 plus Student t with 4 degrees at
d = 128 and N = 12000 (8 cells). 73 worlds; seeds 20261007 (probe), 20261008 (pilot),
20261009 (run).

## 3. Estimators

As in D2v5, with the frozen D2v5 law added to the competitors and to the self-test.

## 4. Errors and nulls

As in D2v5. REF is the frozen law's error pooled over every pilot row.

## 5. Bars (REF = 1.453 and FRAC_X = 0.90 fixed from the pilot; `tolerances.json`; Section 7)

- L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled; L3
  real corpora within 3 REF each; L4 scale cells within 2 REF each.
- L5, against the competitors, pooled over the transfer groups: at most 0.8 times the nominal
  competitor's error, 0.8 times the D2 law's, 0.9 times the D2v2 law's, and 0.95 times each of
  the D2v3, D2v4 and D2v5 laws', and within each group at most each competitor's.
- X1 effective-rank ratio at most FRAC_X in every world (1.5 times the pilot's largest ratio,
  rounded up to two decimals, at most 0.9); P1 hub-set overlap across orientations above that
  across spectra in every world; B1 budget reported.

Pass: L1 to L5, X1 and P1 hold. Fail: pooled unseen error above 3 REF, or any competitor's
pooled error below the law's on the transfer groups, or X1 failing in more than half the
worlds. Otherwise INDETERMINATE.

## 6. What falsifies

A law discovered with the heavy tails bracketed in the training set that still misses the
bracketed unseen worlds refutes the claim that the misses were a matter of coverage; a law that
reaches them and loses the real corpora, the d = 512 clouds or the manifolds refutes the claim
that coverage can be bought without cost. A search that fits the bracketed training worlds in
sample no better than D2v5's law did (1.73 and 2.32 on Student t with 4 degrees at d = 192 and
Laplace at d = 128) says the family, not the set, is the limit. Any competitor beating the law
on the transfer groups fails the gate.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D2v5's self-test (PASS) and the frozen D2v5 law applying with
its published coefficients. PASS.

Probe (`probe.json`, `probe.log`, seed 20261007, Student t with 3 degrees at d = 256, Laplace
at d = 192, and the unseen Student t with 4 degrees at d = 256): every quantity exists. The
bracketing holds in the variables the law reads: under the isotropic reader the training
Student t with 3 degrees at d = 256 has tail_knn 4.53, hill_rk 0.38 and skewness 16.3, the
unseen t with 4 degrees 2.94, 0.24 and 14.6, and the training Laplace at d = 192 1.13, 0.024
and 12.8, so the unseen world sits between its training neighbours in tail weight and in the
target. Skewness runs to 20.4 (t with 3 degrees) and 20.1 (t with 4 degrees) across observers,
the largest targets of the track. Effective rank 3.0 to 4.9 against nulls of 23.9; hub-set
overlap across orientations 0.32 to 0.45 against 0.13 to 0.22 across spectra.

Pilot (`pilot.json`, `pilot.log`, `law.json`, seed 20261008, 37 training and 9 held-out worlds,
2,988 law rows, Atlas 2026-09-09). The search over the declared family froze the law

    log(1 + skew) = -0.3994 -0.0130 / cv_knn -0.0371 log(d_nom) log(k) +0.3583 sqrt(id_twonn)

(features `inv_cv_knn`, `log_d_nom_x_log_k`, `sqrt_id_twonn`, transform log1p), held-out error
0.939, training error 1.504, pooled 1.453 = REF. The search again chose no tail variable. Three
things are recorded before the run. First, the frozen law is the first of the track whose
pooled pilot error exceeds a competitor's: the frozen D2v5 law errs by 1.189 and the D2v3 law by
1.274 over the same rows, against 1.453; the search ranks by held-out error, where the new law
is best (0.939 against 0.962 and 1.077), and the training rows, which now hold the hardest
worlds of any registration, are where it loses. Second, the bracketing worlds in sample: the
law fits Laplace at d = 192 and 256 (0.64, 1.19) where the D2v5 law reads 0.83 and 2.07, and
misses Student t with 3 degrees at d = 256 by 5.41 and with 5 degrees by 2.34 where the D2v5
law reads 1.42 and 1.48; the target skewness on those worlds reaches 18, and on Student t with
4 degrees at d = 192 reaches 24, the largest of the track. Third, therefore, the third clause
of Section 6 applies at the pilot: the family fits the bracketed training worlds in sample no
better than a law frozen without them, so the limit is the family and not the coverage of the
set. The gate is sealed and run as registered, because the transfer bars are the test of
whether coverage bought anything on the unseen bracketed worlds; but REF is 1.65 times
D2v5's, the per-world limits of L2 and L4 widen with it, and the sharp bar of this gate is L5
against the D2v5 law at 0.95 on the transfer groups. The nominal competitor,

    skew = -21.98 +224.78 / d_nom +4.074 log(d_nom) -0.4966 log(k / N),

has held-out error 2.72. Effective-rank ratios run from 0.09 to 0.67 (the held-out ball at
d = 96), so FRAC_X = 0.90 by the cap. Hub-set overlap across orientations exceeds the overlap
across spectra in all 46 worlds. Budget sweep as before. The pilot's own rows hold every bar
the pilot can reach (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; freeze `law.json`; record them in Section 7 and the
   tolerances in Section 5; commit `probe.json`, `pilot.json`, `law.json`. Done.
2. Rename this file to `PREREG-D2V6.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d2v6_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
