# PREREG D7: the minimal observational geometry that closes a turbulent flow

Status: SEALED 2026-09-10 by the rename to `PREREG-D7.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D7 of the OD
track (`experiments/DISCOVERY-TRACK.md`), the last gate of the track's declared order, taken after D5,
whose two-dimensional solver and tangent it uses.

## 1. Claim under test

The track's gate reads: for a filtered flow, with large-eddy filtering as the consumer and the filter
scale as the budget, the read operator of the resolved dynamics with respect to the unresolved state
has a spectrum whose leading part carries the information a closure needs, so that a closure built on
the leading eigen-directions predicts the resolved flow within a declared tolerance and a closure
built on the same number of energy-ranked directions does not.

The world is decaying two-dimensional turbulence in vorticity form, pseudo-spectral with 2/3
dealiasing and RK4, at resolution n, from a seeded random field with spectrum k^3 exp(-(k / 6)^2) at
amplitude 5, sampled at t = 1 and t = 2. The consumer is the spectral cutoff at k_c, the resolved
state being the vorticity modes with |k| at most k_c; the budget is k_c, on {8, 16}. The subfilter
state is the dealiased remainder, parametrised by one real and one imaginary coefficient per
conjugate pair. The resolved tendency T(w_bar + w') is the nonlinear term of the vorticity equation
on the resolved modes; the subgrid contribution is T(w_bar + w') - T(w_bar).

The read operator by the blind probe. The resolved tendency is called on the solver with each
subfilter coefficient perturbed in turn (central differences at a step of 1e-6 of the field's
largest coefficient), which gives the sensitivity J of the resolved tendency to every subfilter
coefficient; the read operator of the resolved dynamics with respect to the subfilter state is
P = J^T J, its eigen-directions the right singular vectors of J, its rank at most twice the resolved
count. The self-test checks J x against the tangent solver's action to 1e-7.

Closures at matched rank r. A closure keeps r directions of the subfilter state and drops the rest;
its error is |T(w_bar + Pi_r w') - T(w_bar + w')| over |T(w_bar + w') - T(w_bar)|, one for no closure
and zero for exact. Four closures: the eigen-direction closure, the projection of the true subfilter
state onto the leading r eigen-directions of P, which is the gate's declared arm; the read-energy
closure, the r subfilter modes of largest sensitivity-weighted energy, the diagonal of P times the
squared coefficient, which is the read distortion the resolved consumer experiences from each mode
(the encyclopedia's read distortion, mode by mode); the energy closure, the r modes of largest
energy, the classical control; and random modes, the median over eight draws. Ranks 16, 32, 64
and 128, and the read operator's full rank, where the eigen-direction closure reproduces the linear
part of the subgrid term exactly and its residual is the part quadratic in the subfilter state.

Why two observational arms. The self-test, on a random field before any turbulence, showed the
energy ranking beating the eigen-direction closure at every low rank (0.94 against 0.98 at rank 2,
0.73 against 0.79 at rank 8) while the eigen-direction closure at full rank left a residual of
0.05 with 76 percent of the subfilter energy. The reason is in the theory the gate is built on:
the consumer's loss from a subfilter mode is its sensitivity times its amplitude, and the leading
eigen-directions rank by sensitivity alone. The read-energy closure ranks by the product and is
the arm the read-distortion definition names; it was added before the probe and is registered
beside the declared arm, not instead of it.

(E) Structure beats random: every closure's error at most the random median's, every cell. (L1)
The declared arm: the eigen-direction closure's error below the energy closure's by a margin M1
in every cell at ranks 16 and above. (L2) The read-energy closure's error below the energy
closure's by a pooled margin M2 at every rank 16 and above, and behind it in no cell by more than
TOL2. (N) Convergence: the read-energy closure's pooled advantage changes by at most TOL_N between
the run's two resolutions. (Q) Record: the eigen-direction closure's residual at full rank.

## 2. World

Pilot (seed 20261029): two seeded fields at n = 64 and 96, two snapshots, two cutoffs, sixteen
cells. Run (seed 20261030): three fresh fields at n = 96 and 128, two snapshots, two cutoffs,
twenty-four cells. Viscosity 0.0005, time step 0.002 at n = 64 scaled with n. Probe seed 20261028.

## 3. Estimators

`d7_closure.py`, importing the two-dimensional solver and tangent from D5. Self-test: the blind
probe's J x against the tangent solver (1.3e-7); the conjugate-pair parametrisation's round trip;
the full-rank eigen-direction closure below one with its energy fraction at most one; the
zero-rank closure at error one; and the rank ladder printed.

## 4. Errors and nulls

Deterministic given the seeds. The null is the random closure; the classical control is the
energy closure. Tolerances are fixed from the pilot by the rules of Section 5.

## 5. Bars (M1 = 0, M2 = 0.01, TOL2 = 0.13, TOL_N = 0.03 fixed from the pilot; `tolerances.json`; Section 7)

- E1: every closure's error at most the random median's, every cell and rank.
- L1: the eigen-direction closure's relative advantage over the energy closure at least M1 in every
  cell at ranks 16 and above (M1 = half the pilot's median advantage, rounded down to 0.01, at
  least 0).
- L2: the read-energy closure's relative advantage over the energy closure, pooled over cells, at
  least M2 at every rank 16 and above (M2 = half the pilot's pooled advantage, rounded down to 0.01,
  at least 0), and at least -TOL2 in every cell (TOL2 = 1.25 times the pilot's largest shortfall,
  rounded up to 0.01).
- N1: the pooled read-energy advantage at the run's two resolutions differs by at most TOL_N (1.5
  times the pilot's change between its two resolutions, rounded up to 0.01).
- Q1: the full-rank residual, reported.

Pass: E1, L1, L2, N1. Fail: E1 failing (a structured closure worse than random); the read-energy
closure behind the energy closure pooled at every rank. Otherwise INDETERMINATE.

## 6. What falsifies

The declared claim, L1, is falsified by the energy closure closing as well as or better than the
eigen-direction closure, which the self-test and the probe both show at low rank; the run says
whether it holds anywhere at the ranks declared. The theory-faithful claim, L2, is falsified by
the energy closure matching the read-energy closure, which would mean the consumer's sensitivity
adds nothing to the amplitude in choosing what to keep. N1 failing says the margin is a
resolution artefact. Q1 is not a bar: it records how much of the subgrid term is beyond any
linear read.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS, after one defect found and fixed, the probe's columns
ordered by mode with real and imaginary parts interleaved while the subfilter vector is ordered
with all real parts first; the self-test's comparison with the tangent solver caught it at a
relative error of 1.1 and reads 1.3e-7 after the fix.

Probe (`probe.json`, `probe.log`, seed 20261028, one field at n = 64 and 96, t = 1 and 2,
k_c = 8 and 16, ranks 4 to 128). Every quantity exists. The subgrid contribution is 0.74 to 0.83 of
the resolved tendency at k_c = 8 and 0.28 to 0.46 at k_c = 16; the read operator's effective rank
is about 130 at k_c = 8 and 360 at k_c = 16 at either resolution. The declared arm loses to the
energy closure in most cells at every rank (at k_c = 8, t = 1, n = 64: 0.97 against 0.89 at rank 4
and 0.22 against 0.19 at rank 128; the one exception n = 96, t = 1, k_c = 8 at ranks 4 to 8). The
read-energy closure ties or beats the energy closure in most cells, by up to 0.09 at k_c = 16 and
rank 128 (0.37 against 0.46) and by less at low rank, and is behind it in a few (n = 96, t = 2,
k_c = 8: 0.87 against 0.83 at rank 8). The random closure sits at 0.91 to 1.00. The eight cells took
5 to 58 seconds.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261029, two fields at n = 64 and 96,
sixteen cells, 64 rank cells at ranks 16 and above, Atlas 2026-09-10). The declared arm is behind
the energy closure in 53 of the 64 rank cells, by a median of 12 percent and up to 38 percent, so
M1 = 0 by the rule (half a negative median, floored at zero), and L1 will hold on the run only if
the eigen-direction closure is at least as good as the energy closure in every cell, which the
pilot says it is not. The read-energy closure is ahead of the energy closure pooled by 3.6
percent (4.4 at n = 64, 2.9 at n = 96), behind it in some cells by up to 9.6 percent (the k_c = 8
cells at rank 32 and 64, where the two rankings pick nearly the same modes), and ahead by up to
22 percent (k_c = 16 at rank 128, 0.375 against 0.444 and 0.403 against 0.462); so M2 = 0.01,
TOL2 = 0.13 and TOL_N = 0.03 by the rules. The full-rank residual of the eigen-direction closure
is 0.05 to 0.09 at k_c = 8, where the read operator's rank (twice the resolved count, about 200
to 400) is below the subfilter dimension and the quadratic part of the subgrid term is what a
linear read cannot see, and 0.000 at k_c = 16, where the rank reaches the subfilter dimension and
the closure is exact. The random closure sits at 0.82 to 1.00. The pilot's own cells give
INDETERMINATE under the fixed tolerances, by L1 (`pilot_grade.json`).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7;
   commit `probe.json`, `pilot.json`, `tolerances.json`. Done.
2. Rename this file to `PREREG-D7.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d7_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
