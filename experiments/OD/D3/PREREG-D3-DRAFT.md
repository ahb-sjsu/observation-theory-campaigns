# PREREG D3 (DRAFT, NOT SEALED): the observational predictability horizon

Status: draft. Nothing here is a registered claim until Section 8 is executed. Gate D3 of the
OD track (`experiments/DISCOVERY-TRACK.md`).

## 1. Claim under test

Section 6 of `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`.
An observer O = (C, G, B) measures a tangent perturbation delta(t), carried by the linearised
flow, in its own length d_C(delta) = sqrt(delta^T P_C delta). Over a window [t0, T] the
observational Lyapunov exponent is log(d_C(T) / d_C(t0)) / (T - t0), the classical one is the
same with the Euclidean length, and the horizon T_O(B) is the first time d_C exceeds B.
Proposition 1 of the article, in the form this gate can measure:

(E) Positive definite observer. If P has eigenvalues in [a, b] with a > 0 then, for every
perturbation and every window, the two exponents differ by at most log(b / a) / (2 (T - t0)),
since a |delta|^2 <= d_C^2 <= b |delta|^2 at both ends of the window. This is exact, and it
makes the two exponents agree in the limit.

(K) Observer with a kernel. The observational exponent is smaller than the classical one when
the perturbation's Euclidean growth is carried by kernel components growing faster than its
read components, equal in the limit when the read components grow at least as fast, and
transiently larger for a perturbation started inside a kernel the flow does not preserve,
since its read length starts at zero and must grow faster than its Euclidean length at first.
For a perturbation confined to an invariant kernel the observational length is zero at all
times and the exponent is undefined; the article's draft 0.2 said "can be zero" and is
corrected to "undefined" with this registration (Section 7).

(H) Horizon. T_O(B) is non-decreasing in B by definition. For a positive definite observer
it lies between the Euclidean horizons at B / sqrt(b) and B / sqrt(a); for a projection it is
never earlier than the Euclidean horizon, since d_C <= |delta|. At fixed B it depends on the
observer wherever the flow has no symmetry carrying one observer to the other, and it does not
where the flow has one.

## 2. World

Flows integrated by a fourth-order Runge-Kutta scheme on the state and the tangent vectors
together, step 0.002 for Lorenz-63 (sigma 10, rho 28, beta 8/3) and 0.005 for Lorenz-96
(N = 40, F = 8), lengths recorded every 0.01 up to T = 20. Starts on the attractor: one
trajectory spun up for 100 time units (50 for Lorenz-96) and sampled every 5 (2) units, 64
starts (32). Every observer has a constant diagonal read operator, so one tangent integration
per start and direction serves all observers of a world.

Worlds and observers. Lorenz-63: `full` (P = I), `aniso` (P = diag(1, 4, 1/4), b / a = 16),
`x_only` (P = diag(1, 0, 0)), `z_only` (P = diag(0, 0, 1)); directions: `random` (uniform on
the unit sphere), `kernel_x` (unit, in the kernel of `x_only`), `kernel_z`. World K: Lorenz-63
extended by one decoupled linear direction u' = mu u, with mu = 2 (`K_mu2`) and mu = 1/2
(`K_mu05`, the control); observers `full` and `core` (reads x, y, z and not u); direction
`core_plus_u`, a random unit vector in the Lorenz part of size sqrt(3) / 2 and u of size 1/2.
Lorenz-96: `full`, `aniso` (P alternating 1 and 4 over sites, b / a = 4), `sub` (sites 0 to
9), `sub2` (sites 10 to 19); directions `random`, `kernel_sub`. The window ladder is
T = 1, 2, 5, 10, 20 from t0 = 0 (t0 = 0.01, the first recorded time, for kernel starts, whose
read length is zero at t = 0); the budget ladder is B = 10, 100, 1000, 10000 for a unit initial perturbation.

The reference exponents (about 0.906 for Lorenz-63 and 1.7 for Lorenz-96 at these
parameters) are not bars; every bar compares exponents on the same trajectory and window.

## 3. Estimators

Window exponents and horizons read off the recorded lengths as defined in Section 1 (the
horizon is the first grid time at which the length exceeds B; unreached horizons are recorded
as infinite and excluded from medians). No fitting anywhere. The self-test (Section 7) checks
the integrator and the estimators on a linear flow with known exponents.

## 4. Errors and nulls

Exact bars are counted as violations over every row and window, with a numerical slack of
1e-9 on the inequalities and 1e-7 on the World K identity. Tolerance bars use the median over
the starts of a cell. The observer-dependence bar uses an exact paired sign test on the horizons of two
observers of the same rank reading the same start and perturbation, ties and unreached pairs
excluded.

## 5. Bars (tolerances FIXED FROM THE PILOT before sealing as declared multiples; Section 7)

Exact, zero violations:
- E1. For every positive definite observer, every row and every window,
  |lambda_O - lambda_cl| <= log(b / a) / (2 (T - t0)).
- KX. In World K the `core` reader's exponent equals the exponent of the perturbation's
  Lorenz part on every window, since the read operator selects exactly that part.
- H1. Horizons non-decreasing in B for every observer and row; the positive definite
  bracket; a projection's horizon never earlier than the Euclidean horizon.

With tolerances:
- E2. For `aniso` in both flows, `random` direction: the median of |lambda_O - lambda_cl| is
  non-increasing over the window ladder (5 percent for ties) and at T = 20 at most TOL_E2.
- K1. World K, mu = 2: in every start lambda_cl(20) - lambda_O(20) >= 0.5 and
  |lambda_cl(20) - 2| <= 0.15 (the classical exponent is mu up to log(1/2) / 20).
- K1c. World K, mu = 1/2: in every start |lambda_cl(20) - lambda_O(20)| <= TOL_K1c.
- K2. Kernel starts (`kernel_x` under `x_only`, `kernel_z` under `z_only`, `kernel_sub`
  under `sub`): the fraction of starts with lambda_O > lambda_cl on the first window (t0 to
  T = 1) is at least FRAC_K2, and the median |lambda_O - lambda_cl| at T = 20 is at most
  TOL_K2.
- K3. `random` direction under every projection observer: the median |lambda_O - lambda_cl|
  is non-increasing over the window ladder and at T = 20 at most TOL_K3.
- H2. Lorenz-63, `random` direction, `x_only` against `z_only`: at every B whose median
  horizon is reached under both, the exact two-sided paired sign test on the horizons of the
  same start and perturbation (ties and unreached pairs excluded) gives p at most 0.01. Lorenz-96, `sub`
  against `sub2`, which the flow's translation symmetry relates: p at least 0.05 at every such
  B (a symmetry control that a real observer dependence must not fake).

Tolerance rule. Each TOL is 1.5 times the pilot's value of the same statistic, rounded up to
three decimals, with a floor of 0.02 on TOL_K1c; FRAC_K2 is 0.8 times the pilot's fraction,
rounded down to two decimals, with a floor of 0.5. (D1 fixed a tolerance at the pilot's own
maximum and missed it by 0.003 on the run; a declared multiple is the rule from here.)

Pass: every bar holds. Fail: any violation of E1, KX or H1 (a theorem, or the code, is wrong),
or K1's gap failing in more than half the starts (the kernel case of Proposition 1 is wrong).
Otherwise INDETERMINATE.

## 6. What falsifies

A positive definite observer whose window exponent leaves the bound; a kernel observer that
reads a decoupled fast direction it was declared not to read; a kernel-started perturbation
whose read length does not grow faster than its Euclidean length at first; a horizon that
decreases in B, leaves its bracket, or precedes the Euclidean one under a projection; horizons
that do not depend on the observer in Lorenz-63, or that do in Lorenz-96 across a symmetry.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-09, `--selftest`): a linear flow x' = diag(1, 0, -1) x. A generic
direction: classical exponent 0.890 on T = 5 (limit 1), anisotropic observer 0.973, difference
0.083 within the bound 0.277; the decaying direction read through x_3 gives -1.000 both ways;
a generic direction read through x_3 gives -1.000 against the classical 0.890 (the smaller
case); read through x_1 gives 1.000000 exactly (the read component); horizons monotone,
bracketed and never earlier for the projection at B = 2, 10, 50. PASS.

A first probe launch crashed in World K: the observer named `core` shared a key with the
integrator's internal record of the Lorenz-part length, so that record was appended twice;
internal keys renamed, self-test rerun, probe relaunched (`probe_crash.log` kept).

Probe (`probe.json`, seed 20260915, Atlas 2026-09-09 14:43 to 14:47 UTC, 384 rows, kernel
starts at t0 = 0.1). Events exist in every cell, no horizon unreached at any B. E1: the worst
ratio of |lambda_O - lambda_cl| to its bound over the positive definite observers was 0.93, so
the bound holds and is nearly attained. E2: `aniso` medians of |lambda_O - lambda_cl| fall from
0.306 at T = 1 to 0.019 at T = 20 (Lorenz-63) and from 0.133 to 0.005 (Lorenz-96). K1: in every
start of World K at mu = 2 the classical exponent at T = 20 is 1.965 (its prediction
2 + log(1/2) / 20 = 1.965) and the observational exponent 0.80 to 1.38 below it; KX exact to
machine precision. K1c: at mu = 1/2 the two exponents differ by at most 0.007 in every start.
K2: with t0 = 0.1 the kernel-start transient was already over on the window [0.1, 1] in half the
`kernel_x` starts (fraction larger 0.45, median excess -0.013), while `kernel_z` gave 0.62 and
+0.18 and `kernel_sub` 0.94 and +1.33; the read fraction of a kernel-started perturbation grows
from zero and, for the x reader, peaks before 0.1. Before the pilot t0 was set to 0.01, the
first recorded time, so that the window begins while the read fraction is still small; the
transient is a statement about small t0. K3: `random` under every projection converges,
|lambda_O - lambda_cl| medians at T = 20 of 0.028 (`x_only`), 0.024 (`z_only`), 0.043 (`sub`),
0.035 (`sub2`), non-increasing along the ladder. H1: no violation. H2: the observer reading x
reaches every budget later than the one reading z on the same perturbation (median horizons
2.39 against 1.61 at B = 10, 10.2 against 8.9 at B = 10000), x later in 71 to 92 percent of
pairs; a permutation test on the difference of medians gave p = 0.067 at B = 100 where the paired
sign test gives 0.0013, so the registered statistic is the exact paired sign test, which uses
the design (the same perturbation read twice). In Lorenz-96 the sign test between `sub` and
`sub2` gives p = 0.38 to 1.0 and fractions 0.41 to 0.50, the symmetry control.

Pilot (`pilot.json`, seed 20260916): TO BE RECORDED, with every TOL and FRAC of Section 5.

Article correction, made with this registration: Proposition 1's clause "can be zero for a
perturbation whose growth stays in the kernel" becomes "is undefined for a perturbation
confined to an invariant kernel, whose observational length is zero at all times", and the
"smaller" clause is stated with its condition, that the kernel components grow faster than the
read ones. Recorded in the article as draft 0.3 and in the ledger as a `[revised]` row.

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; record them in Section 7; fix the tolerances in
   Section 5 and write them to `tolerances.json`; commit `probe.json` and `pilot.json`.
2. Rename this file to `PREREG-D3.md`, commit, record its blob hash in the track document and
   the README status ledger.
3. Run on the run seed, grade with `d3_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
