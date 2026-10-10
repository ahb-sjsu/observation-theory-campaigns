# PREREG D8 (DRAFT): which modes an observer must read to synchronize a nudged copy of a two-dimensional flow

Status: DRAFT 2026-10-09, revision 2 (after an outside review the same day), not claim-bearing,
not sealed. Gate D8 of the OD track (`experiments/DISCOVERY-TRACK.md`), a new claim registered
after the track's declared order was complete, and not a version of D7. Its theory is
`notes/dynamical-read-operator.md` (draft 0.1), Sections 5 and 6. Its bars and tolerance rules are
to be fixed in code (`d8_grade.py`, `d8_fix_tols.py`) before its pilot runs. Nothing below has been
run except the self-test. Every number marked "probe" is set by the probe in Section 7 and recorded
there before the seal.

D8 makes no claim about Navier–Stokes regularity. It is a two-dimensional problem in which enough
observed modes are known to make the discarded directions harmless. It asks only whether the
observer theory chooses those modes better than the classical choices do. Its $m^*$ is a
finite-time synchronization budget measured on finite trajectories. It is not the mathematical
minimum number of determining modes, and nothing here estimates that number.

## 1. Claim under test

Background. Nudging a second solution toward the observed Fourier modes of a two-dimensional flow
(Azouani, Olson and Titi 2014) makes the two flows synchronize once enough modes are observed.
For the ball of lowest wavenumbers this is the determining-modes theorem (Foias and Prodi 1967),
and the counts the theory guarantees are far above what simulations need. For D8's own flows the
gap is measured. Jones and Titi (1993, Theorem 3.2) guarantee that the ball of about $2.7\,c_3\,G$
lowest Fourier pairs is determining, with Grashof number $G = |f|/\nu^2$ on the $2\pi$ box and
$c_3$ an Agmon-type constant the paper leaves unstated. At the probe's viscosities that ball
exceeds the 924-pair grid at $n = 64$ almost everywhere. Where BALL's budget has been measured,
the guarantee sits 80 to 7,500 times above it (theory note Section 6, table and caveats). The
theorem therefore constrains none of the observers D8 compares, and it speaks only to BALL. Which
modes to observe for a given count is not settled by that theory. D7v3 (PASS) found that, for a filtered flow at a
single time, the discarded modes of largest read distortion (the resolved dynamics' sensitivity to
a mode times the mode's squared vorticity amplitude) close the resolved tendency better than the
same number of modes ranked by amplitude alone. The theory note's Proposition 4 shows that ranking
is optimal for the linear feedback under independent phases, and its Section 6 shows the dynamical
read distortion $|\hat\omega_k|^2\|N_u e_k\|^2$ minimizes the discarded error's nonlinear spreading
rate at the first instant of nudging. Neither statement says anything about synchronization at
long times. Sensitivity measures the size of a response. Whether a ranking by response size yields
a stable observer is the empirical question.

Claim. In forced two-dimensional turbulence, an observer that reads the $m$ Fourier pairs of
largest dynamical read distortion, ranked on a training trajectory, reaches sustained
synchronization of a nudged solution with the reference on fresh trajectories at a smaller
finite-time budget $m^*$ than each of the three graded classical observers (the lowest
wavenumbers, BALL; the largest enstrophy contributions, ENSTROPHY; the largest kinetic energies,
KE), by a declared pooled margin, behind the best of them in no graded cell by more than one ladder
step, with the margin the same at two resolutions within a declared and capped tolerance.

## 2. World

Solver. D5's `NS2D` (vorticity form, pseudo-spectral, 2/3 dealiasing, RK4), subclassed in
`d8_sync.py` with Kolmogorov forcing $f_\omega = F_0 k_f \cos(k_f y)$ at $k_f = 4$ and linear drag
$-\alpha\omega$ to stop condensation at the box scale. $F_0 = 1$; $\alpha$ (probe).

Worlds. Two viscosities $\nu_1 > \nu_2$ (probe), each chosen so that the reference flow is chaotic
(largest Lyapunov exponent positive on every probe trajectory) and resolved at the coarser
resolution of its ladder (enstrophy spectrum at the dealiasing wavenumber below $10^{-6}$ of its
peak). Resolutions: pilot $n = 64$ and $96$; run $n = 96$ and $128$.

Time step. $\Delta t = \Delta t_0 \cdot 64 / n$ (probe). Scaling with $1/n$ does not by itself keep
explicit RK4 stable, since the linear stiffness grows as $\nu k_{\max}^2$, so the code checks each
world before any nudging run. It requires $(\nu k_{\max}^2 + \alpha + \mu)\Delta t \le 1$, inside
RK4's real-axis interval of about 2.78 with margin, and an advective CFL number
$\max|u|\,\Delta t / \Delta x \le 0.5$, taken as the maximum over the training window. A world that
fails is refused, recorded, and not graded, and the probe is repeated with a smaller step. The probe
also re-runs every graded observer at $\Delta t / 2$ (Section 7).

Trajectories. Each trajectory starts from a seeded random vorticity field on $|k| \le 8$, scaled to
a declared rms vorticity, and is spun up for $T_{\rm spin}$ (probe) to a statistically stationary
state. Per world: one training trajectory, on which the rankings are computed over a window
$T_{\rm train}$ sampled every $\Delta_s$ (probe); and $K$ test trajectories (pilot $K = 2$, run
$K = 4$) on disjoint seeds, on which synchronization is measured. The same seeded low-mode field is
used at both resolutions of a ladder, so the two resolutions see the same physical initial
condition.

Seeds. Probe 20261071. Pilot training 20261072, pilot test 20261073. Run training 20261074, run
test 20261075. Checked unused in this repository and in geometric-evaluation-theory on
2026-10-09.

Units. Spectral arrays are numpy `fft2` output, and math coefficients are `fft2` / $n^2$. The
$L^2$ norm is $\|f\|^2 = (2\pi)^2\sum_k|\hat f_k|^2$, and the velocity norm of a vorticity field is
$(2\pi)(\sum_k |\hat\omega_k|^2/|k|^2)^{1/2}$, which the self-test checks against physical space.
Both theorem checks use these definitions.

## 3. Observers and estimators

Candidates. Every dealiased Fourier mode with $k \neq 0$, one representative per $\pm k$ pair
(observing a pair means reading one complex coefficient). Each observer is a ranking of the
candidates, so its observed sets are nested in $m$.

- READ (the declared arm). Rank by the training-window mean of
  $d_k(t) = |\hat\omega_k(t)|^2 \cdot \tfrac12(\|N_{u(t)} e_k^{\rm re}\|^2 + \|N_{u(t)} e_k^{\rm im}\|^2)$,
  where $N_u$ is the nonlinear part of the tangent (the viscous, drag and forcing terms excluded)
  and $e_k^{\rm re}, e_k^{\rm im}$ are the unit real and imaginary perturbations of the pair.
- ENSTROPHY (graded control). Rank by the training-window mean of $|\hat\omega_k(t)|^2$. This is
  the pair's contribution to the enstrophy, not to the energy. It is READ's amplitude factor and the
  quantity D7's "energy" closure ranked by (`experiments/OD/D7v3/d7_closure.py:116`), so READ and
  ENSTROPHY differ by the sensitivity factor alone. (D7's records call this ranking "energy". That
  name is inexact and is not carried forward.)
- KE (graded control). Rank by the training-window mean of $|\hat\omega_k|^2 / |k|^2$, the pair's
  kinetic energy.
- BALL (graded control, the Foias–Prodi observer). Rank by $|k|$, ties broken by the angle of $k$
  and then by index.
- SENS (recorded only). Rank by the training-window mean of the sensitivity factor alone. It enters
  no bar.
- RANDOM (null). Five seeded permutations.

Nudging. $v_t = F(v) - \mu P_S(v - u)$ with $v(0) = 0$, $S$ the observer's top $m$ pairs, and
$\mu = \mu_0$ (probe, inside the stability condition of Section 2). On the pilot, $\mu_0/4$ is run on
the graded observers and recorded, not graded.

Sustained synchronization. $\delta(t) = \|\omega_v - \omega_u\| / \|\omega_u\|$. A cell (test
trajectory, observer, $m$) is synchronized when $\delta(t) \le 10^{-4}$ at every sample of the final
window $[T_{\rm sync} - T_{\rm hold}, T_{\rm sync}]$. Both $T_{\rm sync}$ and $T_{\rm hold}$ come
from the probe, with $T_{\rm hold}$ at least five times the inverse of the largest probe Lyapunov
exponent. An endpoint crossing therefore does not count, and an error that has reached rounding
level counts because it stays below threshold. The slope of $\log\delta$ over the window is
recorded and is not part of the rule. The ladder is
$m \in \{4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256\}$, with index $i(m) = 0, \dots, 12$.
$m^*$ is the smallest ladder value at which this and every larger ladder value synchronize. If the
largest value does not synchronize, the cell is censored and its index is set to 13, one step past
256. A synchronized value below a non-synchronized one is recorded as a non-monotone cell.

Stability diagnostics. Beside every cell, the code integrates a tangent vector under the
finite-gain observer's own linearized error equation, $\dot e = [DF(u(t)) - \mu P_S]\,e$, and
records its Lyapunov exponent. This is the local synchronization diagnostic for the observer
actually run. The exponent of the discarded block $Q_S\,DF(u)\,Q_S$, the $\mu \to \infty$ limit, is
recorded on the probe and the pilot only, since it misses the coupling between observed and
discarded error at finite $\mu$.

Theorem checks on the solver. At cutoffs $N \in \{4, 8\}$ on three training snapshots (the first,
the middle and the last of the window). (a) T1: the base state is set explicitly to $p = P_N u$, and
the central-difference read of the resolved tendency at $p$ is taken on every discarded pair with
$|k| > 2N$. This read is exact for the quadratic map up to rounding, and Proposition 2's band-limited
argument holds at $p$, not around the full snapshot. (b) T2: the ratio
$\|r_N(p, q)\| / (c_N(2\|p\|\,\|\Pi_{(N,2N]}q\| + \|q\|^2))$ in the velocity norm, with
$c_N = N\sqrt{K_N}/(2\pi)$ and $q = Q_N u$.

Estimated cost (to be measured on the probe). Ten rankings (READ, the three graded controls, SENS
and five random draws) times 13 ladder values times $K$ test trajectories, each the length of
$T_{\rm sync}$, batched over $m$, with one observer tangent per cell. The probe adds the block
tangent and the $\Delta t / 2$ reruns. The platform is decided at launch under the NRP PREFLIGHT
checklist (`C:\Users\abptl\.claude\projects\C--source-agi-hpc\memory\reference_nrp_job_policies.md`)
or on Atlas within its thermal cap. Nothing runs on the laptop.

## 4. Errors, nulls and the outcome of every case

Advantage. In a cell (world, test trajectory) let $i_{\rm best} = \min(i_{\rm BALL}, i_{\rm ENSTROPHY}, i_{\rm KE})$
over the three graded controls, censored values at 13. READ's advantage is
$a = i_{\rm best} - i_{\rm READ}$, in ladder steps. The pooled advantage is the mean of $a$ over
graded cells.

Every case has one outcome.

- READ synchronizes, and at least one graded control synchronizes: graded, with $a$ as defined.
- READ synchronizes, and all three graded controls are censored: graded, $a = 13 - i_{\rm READ}$.
  This is a lower bound on the true advantage and is recorded as such.
- READ is censored, and at least one graded control synchronizes: graded,
  $a = i_{\rm best} - 13 \le -1$, a shortfall.
- READ and all three graded controls are censored: uninformative, excluded from L1 and N1, and
  counted against scope (E2).
- RANDOM: the median index of its five draws, censored draws at 13. RANDOM is used only in E2,
  against the best graded control.
- SENS: recorded and never graded. Its censoring has no effect on any bar.
- A world refused by the stability guard: not graded, and the gate's verdict is INDETERMINATE unless
  the probe is repeated and the run re-registered before the seal.

## 5. Bars (M1 and TOL_N fixed from the pilot by the rules below, within fixed limits; `tolerances.json`; Section 7)

- T1 (Proposition 2, exact). On every checked training snapshot and both cutoffs, the read of every
  pair with $|k| > 2N$ is at most $10^{-10}$ times the largest first-octave read.
- T2 (Proposition 3). The ratio is at most 1 on every checked snapshot. Its distribution is
  recorded, since it measures how loose the classical bound is.
- E1 (instrument). On every test trajectory, observing every pair holds
  $\delta \le 10^{-10}$ over the final window, and observing none leaves $\delta(T_{\rm sync}) \ge 0.3$.
- E2 (scope). In each world at least three quarters of the test trajectories are graded cells.
  The best graded control's pooled mean index (the mean of $i_{
m best}$ over cells) is below
  RANDOM's pooled mean index. Scope depends on the classical observers alone, so neither READ nor
  SENS can move it. (Changed 2026-10-09 while writing the grader. The earlier form required every
  graded observer, READ included, to beat RANDOM. A READ no better than chance would then have
  read as out of scope, INDETERMINATE, where it should read as a failure of the claim.)
- L1 (the claim). The pooled advantage is at least M1, and no graded cell has $a < -1$.
- N1 (resolution). For each viscosity, the pooled advantages at the run's two resolutions differ by
  at most TOL_N.

Rules, with limits fixed now so a weak or variable pilot cannot loosen the claim. M1 is half the
pilot's pooled advantage, rounded down to 0.1 step, and never below 0.5 step. A pilot that shows no
advantage therefore leaves L1 a real bar. The per-cell tolerance is fixed at one ladder step and is
not taken from the pilot. TOL_N is 1.5 times the pilot's change in pooled advantage between its two
resolutions, rounded up to 0.1 step, then clamped to the interval [0.2, 0.5] step.

Verdict, total. Each case below names the outcome.

- T1 or T2 misses: FAIL of the note's proposition. The gate stops before any claim is graded, and
  the note is corrected first.
- E1 misses: INDETERMINATE (the instrument does not separate the extremes on this world). Recorded.
- E2 misses: INDETERMINATE (outside the scope the ladder can measure). Recorded.
- With T1, T2, E1 and E2 holding, three cases remain.
  - FAIL if the pooled advantage is at most $-0.5$ step, or if more than a quarter of graded cells
    have $a \le -2$.
  - PASS if L1 and N1 hold.
  - INDETERMINATE otherwise.

Records R1, not graded. SENS's $m^*$ and its advantage computed as for READ. The observer Lyapunov
exponent at $m^*$ and at the ladder value below it for every graded observer, and the fraction of
cells in which its sign agrees with sustained synchronization, a direct test of whether READ's
response-size ranking produces a stable observer. The block exponent on the probe and the pilot,
and how often its sign disagrees with the observer exponent's. The overlap of READ's top-$m$ set with
each control's at $m^*$, and the shell histogram of READ's modes. Non-monotone cells. The $\mu_0/4$
pilot run. The initial spreading rate of the note's Section 6 for each observer at each $m$, to see
whether the instant the proposition covers predicts the long-time result.

## 6. What falsifies

A graded control that reaches the same budget as READ says the read distortion adds nothing to the
classical choices once the problem is dynamical, and that D7v3's result belongs to the single-time
closure only. A READ advantage that SENS reproduces equally says the amplitude factor is not needed
in the dynamical problem. That is recorded, and a revision would change the claim. An advantage that
changes with resolution beyond TOL_N says it belongs to the grid and not the flow. A T1 miss says
Proposition 2 is false as stated, or the solver is not the system the note describes. A READ
advantage whose observer exponents do not track synchronization says the budget was reached for
reasons the stability diagnostic does not see. That is recorded, and it does not change the verdict.

Anti-circularity (track Section 3). The rankings are computed on training trajectories with seeds
disjoint from the test trajectories. Three classical controls are computed beside READ, and the
claim is graded against the best of the three in each cell. The observer family is declared in
`claims/transformations/OD.toml` as `OD:sync-observer` before the seal.

## 7. Self-test, probe, pilot (before sealing)

Written 2026-10-09: `d8_sync.py`, `prereg_config.json` (probe candidates), `d8_launch.sh`,
`d8_grade.py` and `d8_fix_tols.py`. Each of the last two has its own `--selftest` on synthetic
results. The grader's self-test exercises every outcome of Section 4 and every verdict branch of
Section 5. The fixer's self-test exercises M1's floor, TOL_N's floor and TOL_N's cap.

Self-test (`d8_sync.py --selftest`, 17 checks at $n = 32$; PASS on Atlas 2026-10-09 at 775d7ed).
- The laminar Kolmogorov flow is a fixed point of the forced solver.
- Batched evaluation equals evaluation one field at a time.
- The central-difference read equals the nonlinear tangent.
- The spectral velocity norm equals the physical one.
- Proposition 1's triad feeds the mode $(1, 0)$.
- T1 and T2 hold at two cutoffs on a broadband random field.
- The nudging contribution to the error tendency is exactly $-\mu P_S e$, and the reference is
  untouched.
- The observer tangent equals the derivative of the nudged tendency, and the block tangent is
  $Q_S\,DF\,Q_S$.
- Nudging with nothing observed reproduces the free solver from zero, which is an identity of the
  code and not a property of the dynamics.
- The stability guard reports the declared quantities and refuses a step outside RK4's interval.
- The rankings are permutations, BALL starts on $|k| = 1$, and the masks are Hermitian-symmetric.
- The initial field is the same physical field at two resolutions.
- The sustained rule rejects an endpoint crossing and an oscillation, and $m^*$ is as defined.

Synchronization of the complete system is not a self-test item. It is bar E1 on the real worlds.
The first version of the self-test (passed on Atlas 2026-10-09 at 91788eb) also asserted that
observing every mode contracts the error at least at rate $\mu/2$. That is not an identity of the
dynamics, and it was removed in this revision.

Probe (seed 20261071). It fixes $\alpha$, $\nu_1$, $\nu_2$, $\Delta t_0$, $T_{\rm spin}$,
$T_{\rm train}$, $\Delta_s$, $\mu_0$, $T_{\rm sync}$ and $T_{\rm hold}$. It records the Lyapunov
exponents, the spectra at the dealiasing wavenumber, the stability numbers, the measured cost per
nudged run, and whether $\delta$ separates cleanly at the $10^{-4}$ threshold. Its step-refinement
check: every graded observer's $m^*$ at $\Delta t/2$ must equal its $m^*$ at $\Delta t$ on every probe
trajectory. Otherwise $\Delta t_0$ is halved and the probe is repeated.

Probe record so far (INCOMPLETE, written 2026-10-10 while the Jobs run; nothing here fixes a
parameter or changes a bar). Each probe world is one NRP Job (namespace ssu-atlas-ai, CPU only,
exempt class 1 CPU / 2Gi, `submit_d8_nrp.py`), $n = 64$, one test trajectory ($K = 1$), every other
parameter as in `prereg_config.json` ($\alpha = 0.1$, $\Delta t_0 = 0.005$, $T_{\rm spin} = 100$,
$T_{\rm train} = 20$, $\Delta_s = 1$, $\mu_0 = 50$, $T_{\rm sync} = 50$, $T_{\rm hold} = 10$). The
code is identical in both rounds (d8_sync.py sha256 e274c0db...). In-pod self-test PASS on every Job.

- Round 1 (code at a76cf15, submitted 2026-10-10 05:04 UTC): $\nu = 0.004$ and $0.002$.
- Round 2 (config at ece9ab1, submitted 05:10 UTC): $\nu = 0.01, 0.02, 0.03, 0.05$. It was added
  after round 1 failed the resolution bar.

Training phase, all six worlds complete.

| $\nu$ | enstrophy tail at $k_{\rm dealias}$ (bar $10^{-6}$) | resolved | linear stiffness | CFL max (train) | T1 max | T2 max |
|---|---|---|---|---|---|---|
| 0.002 | 1.40e-2 | no | 0.26 | 0.21 | 6.1e-16 | 0.024 |
| 0.004 | 6.30e-3 | no | 0.27 | 0.24 | 5.5e-16 | 0.022 |
| 0.01 | 6.83e-4 | no | 0.29 | 0.18 | 6.6e-16 | 0.024 |
| 0.02 | 3.12e-5 | no | 0.34 | 0.13 | 5.3e-16 | 0.026 |
| 0.03 | 1.47e-6 | no (by a factor of 1.5) | 0.38 | 0.09 | 5.6e-16 | 0.031 |
| 0.05 | 3.00e-9 | yes | 0.47 | 0.05 | 4.7e-16 | 0.034 |

Proposition 2 (T1) holds at rounding level on every checked snapshot. Proposition 3's ratio (T2)
stays at most 0.034, so the classical bound is loose by a factor of about 30. Every world passes
the stability guard. Only $\nu = 0.05$ passes the resolution bar at $n = 64$. The CFL number falls
steadily with $\nu$, so whether the resolved flows are still chaotic is open until the Lyapunov
exponents are collected.

Nudging phase, test trajectory 0. These are the $m^*$ values logged so far (ladder index in
parentheses, censored = 13). "-" means not yet logged. Updated 2026-10-10 after the $\nu = 0.05$
Job completed and was collected.

| $\nu$ | resolved | READ | BALL | ENSTROPHY | KE | READ's advantage over the best control | Job |
|---|---|---|---|---|---|---|---|
| 0.002 | no | 32 (6) | 32 (6) | 64 (8) | 32 (6) | 0 | running |
| 0.004 | no | 24 (5) | - | 48 (7) | 24 (5) | 0 so far (BALL pending) | running |
| 0.01 | no | 24 (5) | 16 (4) | 64 (8) | 24 (5) | -1 | failed, node lost |
| 0.02 | no | 24 (5) | 12 (3) | 96 (9) | 32 (6) | -2 | failed, node lost |
| 0.03 | no (narrowly) | 48 (7) | 12 (3) | 96 (9) | 32 (6) | -4 | running |
| 0.05 | yes | 256 (12) | 6 (1) | 128 (10) | 96 (9) | -11 | complete, collected |

Lost Jobs. The $\nu = 0.01$ and $0.02$ Jobs ran on one NRP node, nautilus-ext-gpu01.fullerton.edu.
It went NotReady at about 06:21 UTC on 2026-10-10 and then carried a taint the pods do not
tolerate. Both Jobs ended Failed (BackoffLimitExceeded, backoff_limit 0). This was a node failure,
not a utilization stop: the events show NodeNotReady, and the pods were in the exempt class. Their
$m^*$ values above were logged during the run and survive. Their result blocks did not, so their
Lyapunov exponents, $\delta(t)$ curves, RANDOM, SENS, the $\Delta t/2$ reruns and their footprints
are lost. They have not been resubmitted.

What the record shows, with one trajectory per world. Five worlds have all four graded observers.
In none of them is READ ahead of the best control: its advantage is 0, -1, -2, -4 and -11 steps.
BALL is the best control, or tied for it, in all five. READ leads ENSTROPHY, its own amplitude
factor and the contrast D7v3 passed on, by two to four steps on every unresolved world. KE ties
READ or beats it on every world where it has reported.

The $\nu = 0.05$ world, collected (`probe_pr_nu050_n64.json`). The earlier note recorded two
candidate explanations for READ's $m^* = 256$. The data decide between them as follows.

- The flow is not chaotic. The reference trajectory's largest Lyapunov exponent is -0.053, which
  fails Section 2's world criterion (positive on every probe trajectory). So $\nu = 0.05$ at
  $n = 64$ is resolved but outside D8's scope. It is not a world the claim can be graded on.
- READ's 256 is slow synchronization read through a finite window, explanation (b). For every
  $m$ from 6 to 96, READ's error at $T_{\rm sync} = 50$ is $2.8\times10^{-4}$. It is still falling
  steadily, at about 0.026 decades per unit time over the hold window, and every one of these
  cells has a negative finite-gain observer exponent (about -0.09). The copy is synchronizing,
  slowly, and has not stayed below $10^{-4}$ through the final window. KE and ENSTROPHY show the
  same plateau.
- The plateau and its rate match an observer that leaves the largest scales unread. READ's first
  picks are forcing-scale modes, (2,0), (0,4), (2,±4), (2,±1), (4,±4) and so on, and KE's are
  similar. Neither reads the $|k| = 1$ modes (1,0), (0,1) and (1,±1) early, because their
  amplitude is small. BALL reads those first. Its observer exponent is about -0.22, against READ's
  -0.09, and its error at $m = 8$ is $2.8\times10^{-10}$. With the large scales unread, the error
  decays at about the flow's own rate (reference exponent -0.053). On this one non-chaotic world,
  the modes whose observation makes the error contract fast are the slow, weakly damped large
  scales, and neither amplitude nor sensitivity ranks them first. That is an observation and not
  a result.
- Explanation (a) is half supported. With nothing observed, the error ends at 0.98, so a copy
  started from $v = 0$ does not reach the reference on its own. The Lyapunov exponent is negative,
  so that copy has settled somewhere else. Whether that is another attractor or a very slow
  approach is not determined from this run.

Probe questions answered by this world:
- Step refinement passes: every graded observer's $m^*$ is the same at $\Delta t/2$.
- The instrument extremes behave: with nothing observed the error ends at 0.98, and with everything
  observed it stays at most $1.4\times10^{-17}$ over the final window.
- RANDOM (all five draws) and SENS never synchronize.
- Footprint: peak RSS 119 MiB, 0.998 mean cores, 5,960 s wall time on one CPU.
- The $10^{-4}$ threshold does NOT separate cleanly here. Errors cluster at $2.8\times10^{-4}$, and
  a slow decay reads as no synchronization.

A longer $T_{\rm sync}$, or a rule on the decay rate, is a legitimate change before the pilot,
since this is what the probe was registered to find. It must be decided on the instrument
criterion across every observer and world: does $\delta$ at $T_{\rm sync}$ come out bimodal? It
must not be decided on which choice favours READ. It is not decided here.

What this does not do. It does not grade the claim. The probe exists to fix parameters, and its
worlds are mostly outside the resolution bar. The claim, the bars and the tolerance rules of
Sections 1 to 5 are unchanged. Revising them in response to these numbers before the probe is
complete and recorded would be fitting the registration to its own probe, and is not done here.

Pilot (training 20261072, test 20261073, $n = 64$ and $96$, $K = 2$). It fixes M1 and TOL_N by the
rules of Section 5, within their limits, and records the pilot's own grade.

## 8. Sealing procedure

1. Write the code and pass the self-test. Probe on Atlas or NRP, record Section 7, commit
   `probe.json`. Pilot, fix the tolerances, record them, commit `pilot.json` and `tolerances.json`.
2. Declare `OD:sync-observer` in `claims/transformations/OD.toml`. Verify the references in the
   theory note against Crossref. Rename this file to `PREREG-D8.md`, commit, record its blob hash
   in the track document and the README status ledger.
3. Run on the run seeds, grade with `d8_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test.
