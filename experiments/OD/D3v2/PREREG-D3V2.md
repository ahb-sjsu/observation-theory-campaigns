# PREREG D3v2: the horizon offset law

Status: SEALED 2026-09-09 by the rename to `PREREG-D3V2.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D3v2 of the OD track, the
successor of D3.

## 1. Claim under test

D3 (sealed, INDETERMINATE) found that an observer reading one coordinate of Lorenz-63 reaches
every budget later than the full reader, or than another coordinate's reader, for the same
perturbation, and that the paired significance of that dependence faded along the budget
ladder although its size did not. D3v2 registers the law behind the size.

Once a tangent perturbation delta(t) has aligned with the leading Lyapunov vector v_1(x(t)),
an observer O with read operator P_O measures it as d_O(t) = |delta(t)| f_O(x(t)) with the read
fraction f_O(x) = sqrt(v_1(x)^T P_O v_1(x)), and the full reader (P = I) as |delta(t)|. Write
L(t) = log |delta(t)| and g_O(t) = log f_O(x(t)). The horizon of O at budget B is the first time
L + g_O exceeds log B and the full reader's the first time L does, so the offset
T_O(B) - T_full(B) is the extra time the growth needs to close the deficit -g_O at the moment
of crossing. Because g_O fluctuates with the state on the fast timescale of the flow while L
grows at the exponent, the crossing happens where the deficit is small, and the mean of g_O is
not the law: the probe of 2026-09-09 (Section 7) found the constant-fraction prediction
-E[g_O] / lambda_1 wrong by factors of two to eight for the coordinate readers. The law is the
first passage itself, computed on one independent long trajectory carrying the aligned tangent
vector, with L and g_O recorded on the fine grid:

    Delta_O(B) = E_s[ inf{t >= s : L(t) - L(s) + g_O(t) >= log B}
                      - inf{t >= s : L(t) - L(s) >= log B} ],

the mean over start times s along that trajectory. Nothing from the horizon runs enters; the
long trajectory is integrated separately with its own transient, and the horizon runs start
from random unit perturbations at fresh points of the attractor. The law is observer-relative
in the track's sense: it assigns every observer a horizon offset from the process of its read
fraction along the flow's leading direction; it is zero for the full reader, equal for
observers a symmetry of the flow relates, negative for an observer whose metric exceeds the
Euclidean one on the leading direction, and for a positive definite observer it lies inside
the D3 bracket, since g_O is between log sqrt(a) and log sqrt(b). The constant-fraction value
-E[g_O] / lambda_1 is recorded beside it as the refuted approximation.

## 2. World

The D3 world, Lorenz-63 (step 0.002, 128 starts) and Lorenz-96 at N = 40 (step 0.005, 64
starts), lengths recorded every 0.01 up to T = 20, random unit perturbations, budget ladder
10, 100, 1000, 10000, with the observer family widened. Lorenz-63: `full`, `aniso`
(diag(1, 4, 1/4)), `x_only`, `y_only`, `z_only`, `u1` (the rank-one reader along
(1, 1, 1) / sqrt 3), `u2` (along (1, -1, 0) / sqrt 2), `xy_plane`. Lorenz-96: `full`, `aniso`
(alternating 1, 4), `sub` (sites 0 to 9), `sub2` (sites 10 to 19), `site0`. The independent
long trajectory: one tangent vector renormalised every 0.5 time units over 2000 time units
(600 for Lorenz-96) after a transient of 50 (30), with the accumulated log growth L and every
observer's g_O recorded every 0.01, giving lambda_1 from the growth and Delta_O(B) from the
first passages over start times every 0.5 units, each budget of the ladder separately; first
passages sit on the 0.01 grid, so predictions carry a quantization of that size. Starts for the horizon runs are sampled from a separate spun-up
trajectory with the seed of the role.

## 3. Estimators

Horizons as in D3 (first grid time the length exceeds B; unreached recorded as infinite and
the pair excluded). The measured offset of observer O at budget B is the mean over starts of
T_O(B) - T_full(B) over pairs reached under both, with its standard error. The prediction is
Delta_O from the long trajectory. No fitting.

## 4. Errors and nulls

The offset law is tested at the two largest budgets, 1000 and 10000, where the perturbation
has aligned. The error is the absolute difference between the measured mean offset and
Delta_O(B) at the same budget. The symmetry control is the pair `sub`, `sub2` of Lorenz-96, whose Delta must agree
on the long trajectory and whose measured offsets must agree on the runs.

## 5. Bars (TOL_O1 = 0.259, TOL_O2 = 0.490, TOL_O4 = 0.137 fixed from the pilot; `tolerances.json`; Section 7)

Exact, zero violations (inherited from D3, on the widened family):
- E1. The positive definite window bound for `full` and `aniso`.
- H1. Horizons non-decreasing in B; the positive definite bracket; a projection's horizon
  never earlier than the Euclidean horizon.

With tolerances:
- O1, the offset law. For every observer other than `full`, in both flows, at B = 1000 and
  B = 10000, |mean offset - Delta_O(B)| <= TOL_O1 = 0.259.
- O2, convergence. For every such observer, |mean offset(10000) - mean offset(1000)| <= TOL_O2 = 0.490.
- O3, sign and order. For every such observer at both budgets the sign of the mean offset is
  the sign of Delta_O(B), and the observers of Lorenz-63 ordered by measured offset at
  B = 10000 are ordered as by Delta_O(10000) (Spearman correlation at least 0.9 over the seven
  observers).
- O4, symmetry. In Lorenz-96, |Delta_sub(B) - Delta_sub2(B)| <= TOL_O4 on the long trajectory
  at both budgets and |mean offset(sub) - mean offset(sub2)| <= TOL_O4 = 0.137 at both budgets.
- O5, bracket. For `aniso` at both budgets the mean offset lies in
  [-log sqrt(b) / lambda_1, -log sqrt(a) / lambda_1] and so does Delta_aniso(B).

Tolerance rule. TOL_O1 is 1.5 times the largest error over observers and the two budgets in
the pilot, rounded up to three decimals; TOL_O2 and TOL_O4 likewise from the pilot's largest
values, each with a floor of 0.05 time units.

Pass: every bar holds. Fail: any violation of E1 or H1; or the sign of the mean offset
opposite to the sign of Delta_O(10000) for any observer whose |Delta_O(10000)| exceeds 0.1
(the law is wrong in direction). Otherwise INDETERMINATE.

## 6. What falsifies

A measured offset that differs from the first-passage prediction by more than the tolerance
at the largest budgets, an offset that keeps changing with the budget, an observer whose horizon is
earlier where the law says later, an ordering of observers that the law does not reproduce,
symmetric observers with unequal offsets, or an anisotropic offset outside the D3 bracket.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09): D3's self-test on matrix read operators (PASS), and the offset law
on the linear flow x' = diag(1, 0, -1) x, whose leading vector is e_1, for a rank-one reader
along (cos 0.7, sin 0.7, 0): lambda_1 recovered as 1.0000, the predicted offset 0.2680 against
the exact -log cos 0.7 = 0.2681, the measured horizon offset at B = 10000 0.2700. PASS.

Probe, first launch (`probe_v1.json`, `probe_v1.log`, seed 20260921, 2026-09-09 15:30 UTC, the
constant-fraction law). Lorenz-63, lambda_1 = 0.9049 over 3,900 renormalisation points. The
constant-fraction prediction -E[log f_O] / lambda_1 was 1.33 for `x_only`, 0.95 for `y_only`,
0.80 for `z_only`, 0.80 for `u1`, 1.88 for `u2`, 0.51 for `xy_plane` and -0.18 for `aniso`; the
measured mean offsets at B = 10000 were 0.84, 0.12, 0.09, 0.21, 0.71, 0.09 and -0.63 (standard
errors 0.01 to 0.12), wrong by factors of two to eight for the coordinate readers and with the
order of `x_only` and `u2` reversed. The mean of log f_O is dominated by the moments when the
leading vector is nearly orthogonal to the reader, which a first passage barely feels. The law
was restated as the first passage on the long trajectory before any pilot (Section 1), the
Lorenz-96 Jacobian was vectorised, and the probe was relaunched.

Probe (`probe.json`, `probe.log`, seed 20260921, 15:38 to 15:52 UTC, the first-passage law).
Lorenz-63, lambda_1 = 0.9049 over 195,000 grid points; Lorenz-96, lambda_1 = 1.6815 over
57,000. Predictions at B = 10000 against measured mean offsets (standard error): `aniso` -0.54
against -0.63 (0.12), `x_only` 1.01 against 0.84 (0.10), `y_only` 0.22 against 0.12 (0.02),
`z_only` 0.13 against 0.09 (0.01), `u1` 0.31 against 0.21 (0.05), `u2` 0.87 against 0.71 (0.10),
`xy_plane` 0.16 against 0.09 (0.02); in Lorenz-96 `aniso` -0.28 against -0.27 (0.02), `sub` 0.70
against 0.75 (0.08), `sub2` 0.67 against 0.71 (0.07), `site0` 1.47 against 1.50 (0.09). At
B = 1000 the errors are 0.02 to 0.16. Every sign agrees, the Lorenz-63 order agrees, the
symmetric pair `sub`, `sub2` differ by 0.07 in prediction and at most 0.11 in measurement, and
the `aniso` offsets and predictions lie inside the bracket. The largest error over the two
graded budgets is 0.163 (`site0`, B = 1000), so the pilot is expected to fix TOL_O1 near 0.25.

Pilot (`pilot.json`, `pilot.log`, seed 20260922, Atlas 2026-09-09 15:45 to 15:51 UTC, 192
rows). Lorenz-63, lambda_1 = 0.8998; Lorenz-96, lambda_1 = 1.7328, each from its own long
trajectory. Exact bars: no violation. Predictions against measured mean offsets at B = 10000
(standard error): `aniso` -0.60 against -0.49 (0.08), `x_only` 1.00 against 1.16 (0.13),
`y_only` 0.22 against 0.16 (0.04), `z_only` 0.13 against 0.13 (0.03), `u1` 0.31 against 0.29
(0.06), `u2` 0.84 against 1.01 (0.12), `xy_plane` 0.17 against 0.14 (0.04); Lorenz-96 `aniso`
-0.28 against -0.27 (0.02), `sub` 0.66 against 0.70 (0.08), `sub2` 0.67 against 0.60 (0.06),
`site0` 1.46 against 1.36 (0.08). The largest error over the two graded budgets is 0.172
(`u2`, B = 10000), so TOL_O1 = 0.259; the largest change of a measured offset between the two
budgets is 0.327 (`u2`), so TOL_O2 = 0.490; the symmetric pair differs by 0.023 in prediction
and at most 0.091 in measurement, so TOL_O4 = 0.137. Every sign agrees, the Lorenz-63 order agrees
exactly (Spearman 1.0), and the `aniso` offsets and predictions lie inside the bracket. The
pilot passes every bar at these tolerances (`pilot_grade.json`). The constant-fraction values,
recorded beside the law, are wrong by up to 1.0 time units on the same rows.

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; record them in Section 7; fix the tolerances in
   Section 5 and write them to `tolerances.json`; commit `probe_v1.json`, `probe.json` and
   `pilot.json`. Done.
2. Rename this file to `PREREG-D3V2.md`, commit, record its blob hash in the track document
   and the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d3v2_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
