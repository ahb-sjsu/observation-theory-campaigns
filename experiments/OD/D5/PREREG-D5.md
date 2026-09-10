# PREREG D5: Burgers shock formation as the first singular test

Status: SEALED 2026-09-10 by the rename to `PREREG-D5.md`; blob hash recorded in
`experiments/DISCOVERY-TRACK.md` and the README status ledger. Gate D5 of the OD
track (`experiments/DISCOVERY-TRACK.md`), taken after D6 in the track's declared order.

## 1. Claim under test

The track's gate reads: approaching a shock, the observer-induced geometry of perturbations shows a
transition that converges as the resolution N grows and depends on the observation budget B
through a scaling collapse Phi(N, B, t) = N^beta F(B / B_c(t)), and the classical diagnostics do not
predict the shock time earlier. This registration fixes every term, and states in advance where
the declared claim cannot hold.

The world is the periodic Burgers equation u_t + u u_x = nu u_xx on [0, 2 pi), solved pseudo-spectrally
at resolution N with 2/3 dealiasing and RK4, from seeded initial conditions of three Fourier modes at
unit amplitude, for viscosities nu on a ladder that includes 0. For nu = 0 the shock time is exact,
t* = -1 / min u0', and the pre-shock solution follows from characteristics; the self-test checks the
solver against it. An observer of budget B is the spectral reader that keeps wavenumbers 1 to B.

The observational quantity. A fixed seeded set of r = 16 smooth perturbations (random Fourier
coefficients with amplitude 1/k on wavenumbers 1 to N/3, unit norm) is carried along the trajectory
from t = 0 by the tangent solver. At each sample and each budget B, the read fraction f_B(t) is the
mean over the set of |C_B delta|^2 / |delta|^2, the share of a perturbation's energy that the reader of
budget B still sees; the Gram matrix of the read images gives the observational geometry (its
effective dimension and shell thickness are recorded). The front wavenumber is the classical
inverse length B_c(t) = max |u_x| / max |u|. Two earlier estimators were tried at the probe and
rejected before any pilot: a fresh random sketch at each sample, whose growth rate was sketch
noise; and the windowed amplification of the fixed smooth set, which stayed within three percent
of one while the gradient grew tenfold, because the forming front is narrower than any smooth
direction and its effect lives at wavenumbers the short window does not reach. The read fraction
is the quantity D3v2 used, and it carries the transition: as the front steepens, the perturbation's
energy moves to wavenumbers beyond B, earlier and deeper for smaller B.

The classical diagnostics beside every sample: max |u_x|, its classical alarm (the first time it
exceeds three times its initial value), and the classical prediction of t* by linear extrapolation
of 1 / max |u_x| to zero, which for inviscid Burgers is exact before the shock (the probe returned
0.5144 against 0.5139). The observational alarm at budget B is the first time f_B falls below half
its initial value.

(E) The read fraction is nested in B and at most one, at every sample. (N) Convergence: at the same
initial condition and viscosity, the read fractions at N and 2N agree within TOL_N up to 0.9 t*.
(C) Collapse: with x = B / B_c(t) and y = f_B(t) / f_B(0), on samples after the front has begun to
steepen (B_c at least 1.2 times its initial value), the points of every world at a given viscosity
fall on one curve, the interquartile range of y in half-octave bins of x being at most TOL_C at the
median bin and 2 TOL_C at the worst; and the scaled collapse is tighter than the unscaled null
(x = B) by a factor of 0.8 at the median bin, so that the front wavenumber carries information.
(L) Lead: the earliest observational alarm across budgets precedes the classical alarm by at least
MARGIN_L on every run trajectory. (X) The negative control does not fire.

What this registration says about (L) before the run: for inviscid Burgers the classical
extrapolation is exact, so no observational quantity can lead a classical prediction of t*; the
lead is measured against the classical alarm, a threshold on the gradient, and at the probe the
read fraction did not cross its alarm threshold before the shock at any budget (its smallest value
was 0.54 to 0.57 of its initial value at B = 2) while the classical alarm fired at 0.36. (L) is kept as
declared because it is the track's clause, and it is expected to fail; a failure of (L) alone is
INDETERMINATE, as the bars say. The first singular test is then what (N), (C) and (X) say about the
observer-relative transition, and that is what the record will carry.

The exponent beta of the declared form is not registered: at the probe the read fractions at N =
256 and 512 agreed to a few hundredths until the front approached the grid, so the N dependence is
a convergence, not a power, and Phi(N, B, t) = F(B / B_c(t)) with beta = 0 is the form under test.

## 2. World

Pilot (seed 20261026): four seeded initial conditions at N = 128 and 256 and nu in {0, 0.005}, sixteen
trajectories, and one two-dimensional control at 48 squared. Run (seed 20261027): four fresh
initial conditions at N = 256 and 512 and nu in {0, 0.005, 0.02}, twenty-four trajectories, and two
controls at 64 squared. Trajectories run to 0.95 t*, sampled every 0.02; time step 0.002 at N = 256,
scaled with N. Budgets B in {2, 4, 8, 16, 32, 64} where B is at most N/3. The control is decaying
two-dimensional Navier-Stokes in vorticity form (pseudo-spectral, 2/3 dealiasing, RK4, nu = 0.001)
from a seeded smooth field of four low modes at amplitude 4, run four time units, with the same
carried-perturbation estimator (r = 8) and spectral budgets B in {2, 4, 8, 16}. Probe seed 20261025.

## 3. Estimators

`d5_burgers.py`. Self-test: the inviscid solver against characteristics at t*/2 (errors at the
1e-6 floor of the reference at N = 128, 256, 512); the classical extrapolation recovering t* to
0.1 percent; the tangent step against a finite difference of the nonlinear step (5e-9); nested
read fractions; the two-dimensional solver conserving energy and enstrophy at nu = 0 (1e-6) and its
tangent against a finite difference (1e-13).

## 4. Errors and nulls

The quantities are deterministic given the seeds. The null for the collapse is the unscaled
variable x = B. Tolerances are fixed from the pilot by the rules of Section 5.

## 5. Bars (TOL_N = 0.21 and TOL_C = 0.13 fixed from the pilot; MARGIN_L = 0.02 declared; `tolerances.json`; Section 7)

- E1, exact: read fractions nested in B and at most one at every sample of every world.
- N1: for every pair (N, 2N) at the same initial condition and viscosity, the largest difference in
  read fraction over shared budgets and t at most 0.9 t* is at most TOL_N (1.5 times the pilot's
  largest, rounded up to 0.01).
- C1: at every viscosity, the scaled collapse's median bin IQR is at most TOL_C (1.5 times the
  pilot's largest median, rounded up to 0.01) and its worst bin at most 2 TOL_C.
- C2: at every viscosity, the scaled collapse's median bin IQR is at most 0.8 times the unscaled
  null's.
- L1: on every run trajectory the earliest observational alarm precedes the classical alarm, and
  the median lead is at least MARGIN_L = 0.02 (one sample interval).
- X1: no observational alarm on any control at any budget.

Pass: E1, N1, C1, C2, L1, X1. Fail: a resolution difference above 3 TOL_N; a scaled collapse median
IQR above 3 TOL_C; the controls firing in more than half their budget cells. Otherwise
INDETERMINATE.

## 6. What falsifies

A transition that disappears with N (N1 fails by its fail clause) says the observational signature
is a discretisation artefact. A collapse no tighter than the unscaled null (C2 fails) says the
front wavenumber is not the scale that organises what a budgeted reader sees, and the signature is
not observer-relative in the declared sense. A control that fires says the signature is not about
singularity formation. (L) failing says, as the registration expects, that a budgeted reader's
view of a forming shock trails the gradient it cannot resolve, and that the classical diagnostic
keeps its lead.

## 7. Self-test, probe, pilot (before sealing)

Self-test (Atlas 2026-09-10): PASS, seven checks, after two estimator revisions recorded in
Section 1.

Probe (`probe.json`, `probe.log`, seed 20261025, one initial condition inviscid at N = 256 and 512,
viscous at N = 256 with nu = 0.01, and a control at 48 squared). Every quantity exists. Inviscid at
N = 256: the read fraction at B = 2 falls from 0.65 to 0.37 and at B = 64 from 0.996 to 0.94 as the
front wavenumber rises from 2.0 to 20.9 and the gradient grows 10.8-fold; at N = 512 the same
initial condition reads 0.66 to 0.35 and 0.99 to 0.91 with the front at 25.9 and the gradient
13.3-fold, the two resolutions agreeing to 0.02 at t = 0.36 and parting to 0.06 at t = 0.48 where
the front approaches the coarser grid. Viscous at nu = 0.01: the read fractions first rise (0.81 to
0.85 at B = 4 by t = 0.12, diffusion smoothing the carried perturbations) and then fall (0.69 at
0.48), the front reaching 11.2. The classical extrapolation returned 0.5144 against t* = 0.5139
inviscid and 0.529 viscous; the classical alarm fired at 0.36 and 0.38; no observational alarm
fired before 0.95 t* at any budget. The control's read fractions moved by at most 0.06 over two
time units with its gradient growing one percent, too quiet to test anything, so the run's
controls use a fourfold stronger field over four time units, declared here before the pilot.

Pilot (`pilot.json`, `pilot.log`, `tolerances.json`, seed 20261026, sixteen Burgers trajectories and one
control at 48 squared, Atlas 2026-09-10). Every quantity exists on every trajectory. Resolution:
the eight pairs (N = 128 against 256, same initial condition and viscosity) differ by 0.03 to 0.14 in
read fraction up to 0.9 t*, the largest on the two initial conditions whose fronts are sharpest at
N = 128, so TOL_N = 0.21 by the rule; the run compares N = 256 against 512, where the probe read
0.06. Collapse: at nu = 0 the scaled collapse (x = B / B_c(t)) has a median bin IQR of 0.080 over
14 half-octave bins and 1,144 points against 0.139 for the unscaled null; at nu = 0.005, 0.028
against 0.087; so the front wavenumber organises what a budgeted reader sees, by factors of 0.58
and 0.32 against the null, and TOL_C = 0.13 by the rule. Alarms: the classical alarm fired on every
trajectory at 0.62 to 0.82 of t*; the observational alarm fired on one trajectory only (initial
condition 13 at N = 256, nu = 0, at B = 2 and 4, at 0.86 and 0.90 against the classical 0.72), later
than the classical alarm, so L1 fails on the pilot rows as Section 1 expected. The control, with
the fourfold field over four time units, moved its gradient by 0.1 percent and fired the
observational alarm at B = 2 at t = 0.5, its lowest two modes losing half their share of the
carried perturbations as the two-dimensional flow moved energy across scales; X1, declared as no
alarm at any budget, fails on the pilot's control at the smallest budget and holds at B = 4, 8 and
16. X1 is kept as declared; the pilot says the B = 2 reader's alarm is not specific to a forming
shock, and the run's two controls will say whether that is the rule. E1, N1, C1 and C2 hold on
the pilot rows under the fixed tolerances (`pilot_grade.json`, INDETERMINATE by L1 and X1).

## 8. Sealing procedure

1. Self-test, probe and pilot on Atlas; fix the tolerances; record them in Sections 5 and 7;
   commit `probe.json`, `pilot.json`, `tolerances.json`. Done.
2. Rename this file to `PREREG-D5.md`, commit, record its blob hash in the track document and
   the README status ledger. Done by this commit.
3. Run on the run seed, grade with `d5_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry tests in
   `claims/transformations/OD.toml`.
