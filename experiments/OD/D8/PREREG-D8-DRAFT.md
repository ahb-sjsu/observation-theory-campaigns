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
theorem therefore constrains none of the observers D8 compares, and it speaks only to BALL.

What the synchronization literature already settles (web search 2026-10-10, not a systematic
database review). Every study found nudges a low-pass ball of Fourier modes, $|k| \le k_a$, and
asks how large $k_a$ must be.
- In 3-D homogeneous turbulence the ball synchronizes the flow once $k_a\eta \approx 0.15$ to $0.2$.
  This is from Yoshida, Yamaguchi and Kaneda (2005), Lalescu, Meneveau and Eyink (Phys. Rev. Lett.
  110, 084102, 2013), and Clark Di Leoni, Mazzino and Biferale (Phys. Rev. X 10, 011023, 2020). The
  Phys. Rev. X paper allows an arbitrary nudged set in principle but tests only low-pass sets.
- In 2-D damped-driven turbulence the threshold sits near the forcing scale and far above the
  dissipation scale: $3 < k_a^* < 4$ for Kolmogorov flow at $k_f = 4$, $\alpha = 0.1$,
  $\nu = 10^{-3}$, with $k_a^*$ tracking $k_f$ for $k_f = 2$ to 6. The sign change of the conditional
  Lyapunov exponent identifies it (Inubushi and Caulfield, arXiv:2508.16920, 2025). That is D8's
  forcing and drag, so D8's BALL observer is the case they studied, at lower Reynolds number. The
  probe's BALL budgets (6 and 12 pairs on the two valid worlds, $|k| \le 2$ and 3) are consistent
  with them.
- The threshold coincides with the spectral peak of the leading conditional or Lyapunov vector (Li
  et al., J. Fluid Mech. 983, A1, 2024, and 1008, A27, 2025). Transverse Lyapunov exponents give the
  same picture (Inubushi, Saiki, Kobayashi and Goto, Phys. Rev. Lett. 131, 254001, 2023).
- Olson and Titi (J. Stat. Phys. 2003) showed that the number of determining modes and the rate of
  assimilation depend strongly on the length scales of the forcing.
- In a shell model, measuring two adjacent mesoscales synchronizes the larger scales under an
  ensemble Kalman filter (Fossella et al., arXiv:2507.15626, 2025). That is a different method and
  model.

Not found: any comparison of mode sets other than the low-pass ball for nudging. That includes
sets ranked by energy, enstrophy or sensitivity, and sets that leave out the large, low-amplitude
scales. Observability-Gramian sensor placement exists (for example Kang and Xu 2012), but for
variational estimation, not for choosing Fourier modes to nudge in turbulence. D8's comparison of
READ, ENSTROPHY and KE against BALL is therefore, as far as this search shows, not done before. Its
BALL arm is not new: it replicates Inubushi and Caulfield's observer on their flow family. A claim of
novelty in any write-up needs a database search (Scholar, Web of Science) first. Which modes to
observe for a given count is not settled by the classical theory or by this literature.

D7v3 (PASS) found that, for a filtered flow at a
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
$-\alpha\omega$ to stop condensation at the box scale. $F_0 = 1$, $\alpha = 0.1$ (fixed by the
probe).

Worlds. Two viscosities, $\nu_1 = 0.03$ and $\nu_2 = 0.02$, fixed by the owner on 2026-10-10 from
probe round 3 (Section 7). Each meets the criteria at $n = 96$. Each is chaotic: the largest
Lyapunov exponent was positive on the probe trajectory, +0.06 and +0.26. Each is resolved at the
coarser resolution of its ladder: the enstrophy spectrum at the dealiasing wavenumber is below
$10^{-6}$ of its peak, at $5\times10^{-10}$ and $1\times10^{-7}$. At $n = 64$ neither viscosity was
resolved, which is why the coarser resolution is 96. Resolutions: pilot $n = 96$ and $128$. The run
is at $n = 128$ and $192$ by the rule that its ladder is one step finer than the pilot's. That
ladder is PENDING the owner's decision on its cost: one $n = 192$ trajectory is estimated at the
order of 100 CPU-hours, and this is not measured. ($\nu_1 > \nu_2$ as before. $\nu_1 = 0.03$ is
the weakly chaotic world.)

Time step. $\Delta t = \Delta t_0 \cdot 64 / n$, with $\Delta t_0 = 0.005$, fixed by the probe
(step refinement passed on every collected probe world). Scaling with $1/n$ does not by itself keep
explicit RK4 stable, since the linear stiffness grows as $\nu k_{\max}^2$, so the code checks each
world before any nudging run. It requires $(\nu k_{\max}^2 + \alpha + \mu)\Delta t \le 1$, inside
RK4's real-axis interval of about 2.78 with margin, and an advective CFL number
$\max|u|\,\Delta t / \Delta x \le 0.5$, taken as the maximum over the training window. A world that
fails is refused, recorded, and not graded, and the probe is repeated with a smaller step. The probe
also re-runs every graded observer at $\Delta t / 2$ (Section 7).

Trajectories. Each trajectory starts from a seeded random vorticity field on $|k| \le 8$, scaled to
a declared rms vorticity, and is spun up for $T_{\rm spin} = 100$ to a statistically stationary
state. Per world: one training trajectory, on which the rankings are computed over a window
$T_{\rm train} = 20$ sampled every $\Delta_s = 1$ (all fixed by the probe); and $K$ test trajectories (pilot $K = 2$, run
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
$\mu = \mu_0 = 50$ (fixed by the probe, inside the stability condition of Section 2). On the pilot, $\mu_0/4$ is run on
the graded observers and recorded, not graded.

Sustained synchronization. $\delta(t) = \|\omega_v - \omega_u\| / \|\omega_u\|$. A cell (test
trajectory, observer, $m$) is synchronized when $\delta(t) \le 10^{-4}$ at every sample of the final
window $[T_{\rm sync} - T_{\rm hold}, T_{\rm sync}]$, with $T_{\rm sync} = 100$ and
$T_{\rm hold} = 10$. Both were fixed by the owner on 2026-10-10 from probe round 3, on the separation
of $\delta$: at $T_{\rm sync} = 100$, 3 of 52 graded cells per valid world fell between $10^{-6}$
and $10^{-2}$, against 45 of 260 at $T_{\rm sync} = 50$. $T_{\rm hold} = 10$ satisfies the rule
that it be at least five times the inverse of the largest probe Lyapunov exponent
($5/0.54 \approx 9.3$). Recorded: it is shorter than five inverse exponents of the weakly chaotic
world $\nu_1$ ($5/0.06 \approx 83$). The rule was written against the largest exponent and is
applied as written. An endpoint crossing therefore does not count, and an error that has reached rounding
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

Probe rounds 1 and 2 (COMPLETE 2026-10-10; collected as `probe_round1.json`, `probe_round2.json`
and one `probe_<world>.json` and `.log` per world, in `experiments/OD/D8/` on Atlas). Nothing here
grades the claim, and no bar or rule of Sections 1 to 5 has been changed. Each probe world was one
NRP Job (namespace ssu-atlas-ai, CPU only, exempt class 1 CPU / 2Gi, `submit_d8_nrp.py`), at
$n = 64$ with one test trajectory ($K = 1$). Every other parameter was as in `prereg_config.json`
($\alpha = 0.1$, $\Delta t_0 = 0.005$, $T_{\rm spin} = 100$, $T_{\rm train} = 20$, $\Delta_s = 1$,
$\mu_0 = 50$, $T_{\rm sync} = 50$, $T_{\rm hold} = 10$, block exponent on). The code was identical in
both rounds (d8_sync.py sha256 e274c0db...), and the in-pod self-test passed on every Job.

- Round 1 (code at a76cf15, submitted 2026-10-10 05:04 UTC): $\nu = 0.004$ and $0.002$.
- Round 2 (config at ece9ab1, submitted 05:10 UTC): $\nu = 0.01, 0.02, 0.03, 0.05$. It was added
  after round 1 failed the resolution bar.
- Lost to a node failure: the $\nu = 0.01$ and $0.02$ Jobs ran on nautilus-ext-gpu01.fullerton.edu.
  The node went NotReady at about 06:21 UTC and then carried a taint the pods do not tolerate, and
  both Jobs ended Failed (BackoffLimitExceeded, backoff_limit 0). This was not a utilization stop:
  the events show NodeNotReady, and the pods were in the exempt class. Their training numbers and
  the $m^*$ values logged during the run survive. Their result blocks do not. They have not been
  resubmitted.

Training phase, all six worlds.

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
the stability guard.

Nudging phase, test trajectory 0 (ladder index in parentheses, censored = 13). The last column is
the largest Lyapunov exponent of the reference trajectory, so a positive value means chaotic.

| $\nu$ | resolved | READ | BALL | ENSTROPHY | KE | READ's advantage over the best control | Lyapunov | Job |
|---|---|---|---|---|---|---|---|---|
| 0.002 | no | 32 (6) | 32 (6) | 64 (8) | 32 (6) | 0 | +0.54 | complete |
| 0.004 | no | 24 (5) | 24 (5) | 48 (7) | 24 (5) | 0 | +0.44 | complete |
| 0.01 | no | 24 (5) | 16 (4) | 64 (8) | 24 (5) | -1 | lost | failed, node |
| 0.02 | no | 24 (5) | 12 (3) | 96 (9) | 32 (6) | -2 | lost | failed, node |
| 0.03 | no (narrowly) | 48 (7) | 12 (3) | 96 (9) | 32 (6) | -4 | +0.06 | complete |
| 0.05 | yes | 256 (12) | 6 (1) | 128 (10) | 96 (9) | -11 | -0.05 | complete |

What the probe settles, on the four collected worlds:

- No world at $n = 64$ satisfies Section 2's criteria. The flows are chaotic up to $\nu = 0.03$ but
  unresolved. They are resolved only at $\nu = 0.05$, where the reference Lyapunov exponent is
  negative. The exponent falls from +0.54 at 0.002 to +0.06 at 0.03 and -0.05 at 0.05. So $\nu_1$
  and $\nu_2$ cannot be fixed at $n = 64$.
- Step refinement passes on all four worlds: every graded observer's $m^*$ at $\Delta t/2$ equals
  its $m^*$ at $\Delta t$.
- The instrument extremes behave on all four. With nothing observed, $\delta(T_{\rm sync}) \ge 0.98$.
  With everything observed, $\delta \le 3.7\times10^{-17}$ over the final window.
- RANDOM (all five draws on every world) and SENS never synchronize within the ladder.
- Footprint: peak RSS 118.7 to 119.7 MiB, mean cores 0.998 to 1.000. Wall time per world for one
  test trajectory is 3.2 to 3.8 h on the chaotic worlds and 1.7 h at $\nu = 0.05$.

What the probe finds against the instrument:

- The $10^{-4}$ threshold does not separate cleanly. Across the 260 graded and SENS cells,
  $\delta(T_{\rm sync})$ is not bimodal. 45 cells lie between $10^{-6}$ and $10^{-2}$, and 29 lie
  in $[10^{-4}, 10^{-3})$, right above the threshold. Most of the cluster is the slowly decaying
  observers of $\nu = 0.05$ ($\delta = 2.8\times10^{-4}$ and still falling) and of $\nu = 0.03$. A
  slow decay is therefore read as no synchronization. Changing the window or the rule is a
  legitimate change before the pilot. It must be decided on that separation criterion across every
  observer and world, not on its effect on READ. It is not decided here. Round 3 runs a longer
  window (below) so that the rule can be evaluated at both lengths from the same runs.
- The finite-gain observer exponent's sign agrees with sustained synchronization in 192 of 260
  cells (74 percent).

What the probe shows about the claim. These are recorded and not graded: one trajectory per world,
on worlds that fail the world criteria. READ is never ahead of the best classical control. On the
two strongly chaotic worlds it ties BALL and KE, and READ's and BALL's $\delta(T_{\rm sync})$
profiles over the ladder are nearly the same. On the weakly chaotic and non-chaotic worlds BALL
leads by 4 and 11 steps. READ leads ENSTROPHY, its own amplitude factor and the contrast D7v3
passed on, by two to four steps on every unresolved world.

The $\nu = 0.05$ world in detail (`probe_pr_nu050_n64.json`). READ's $m^* = 256$ is slow
synchronization read through a finite window. For every $m$ from 6 to 96, READ's error at
$T_{\rm sync}$ is $2.8\times10^{-4}$, still falling at about 0.026 decades per unit time, with
observer exponents near -0.09. KE and ENSTROPHY show the same plateau. READ's first picks are
forcing-scale modes: (2,0), (0,4), (2,±4), (2,±1), (4,±4). It does not read the $|k| = 1$ modes
(1,0), (0,1) and (1,±1) early, because their amplitude is small. BALL reads those first and
contracts about 2.5 times faster (exponent about -0.22; error $2.8\times10^{-10}$ at $m = 8$). On
this one non-chaotic world, the modes whose observation makes the error contract fast are the
slow, weakly damped large scales, and neither amplitude nor sensitivity ranks them first. That is
an observation and not a result. With nothing observed the error ends at 0.98, so a copy started
from $v = 0$ settles away from the reference. Whether that is another attractor or a very slow
approach is not determined.

Probe round 3 (submitted 2026-10-10 12:36 to 12:39 UTC, at 5a87626; results below). The aim is
chaotic and resolved worlds at a coarser resolution of $n = 96$.

- Worlds: $\nu \in \{0.01, 0.02, 0.03\}$ at $n = 96$, one test trajectory each, same seeds
  (probe 20261071). These are the viscosities rounds 1 and 2 found chaotic, at a resolution where
  the tail should clear the bar.
- $T_{\rm sync} = 100$ with $T_{\rm hold} = 10$. $\delta(t)$ for $t \le 50$ does not depend on the
  window length, so the same runs give the rule's answer at $T_{\rm sync} = 50$ and 100.
- The block exponent is off, since rounds 1 and 2 recorded it on four worlds.
- Each world is split into three NRP Jobs: the instrument and the four graded observers; SENS and
  RANDOM; and the $\Delta t/2$ reruns. That keeps every Job to a few hours and limits what one node
  failure can take.
- Set up at bc2f1de: `d8_sync.py --parts` with per-world overrides, and `submit_d8_nrp.py --split`
  (nine Jobs, exempt class, `timeout 16h`). Logs are read only from Jobs that succeeded, since a dead
  node makes `kubectl logs` hang. The submitter's dry run passed every preflight guard. A smoke test on
  Atlas (n = 32, short times) ran one world whole and then as three parts merged by the submitter's
  `merge_parts`. It found the same observers, bit-identical $m^*$ and $\delta(T_{\rm sync})$ for every
  observer, the same $\Delta t/2$ and instrument results, and identical rankings across parts.

Round 3 results (recorded 2026-10-10; collected per world as `probe_pr3_nu{010,020,030}_n96.json`
on Atlas, merged by the submitter from the parts that succeeded).

| $\nu$ ($n = 96$) | enstrophy tail, train / test (bar $10^{-6}$) | Lyapunov | world criteria | READ | BALL | ENSTROPHY | KE | READ's advantage over the best control |
|---|---|---|---|---|---|---|---|---|
| 0.01 | 2.8e-5 / 6.4e-6 | +0.41 | fails (unresolved) | 16 (4) | 12 (3) | 64 (8) | 16 (4) | -1 |
| 0.02 | 1.3e-7 / 3.2e-8 | +0.26 | PASSES both | 32 (6) | 12 (3) | 48 (7) | 24 (5) | -3 |
| 0.03 | 4.5e-10 / 7.9e-10 | +0.06 | PASSES both | 16 (4) | 6 (1) | 48 (7) | 32 (6) | -3 |

$m^*$ is at $T_{\rm sync} = 100$, ladder index in parentheses.

- Two worlds meet Section 2's criteria: $\nu = 0.02$ and $0.03$ at $n = 96$. The probe can now
  propose $\nu_2 = 0.02$ and $\nu_1 = 0.03$ with $n = 96$ as the coarser resolution. That is for the
  owner to confirm, and it is not fixed here.
- Theorem checks and stability hold on all three worlds: T1 at $8\times10^{-16}$ to
  $1.0\times10^{-15}$, T2 at most 0.030, linear stiffness at most 0.37, training CFL at most 0.19.
- The instrument extremes behave on all three. With nothing observed, $\delta(T_{\rm sync})$ is
  1.74 to 2.58. With everything observed, $\delta \le 4.6\times10^{-17}$ over the final window.
- Step refinement passes on both valid worlds: every graded observer's $m^*$ at $\Delta t/2$ equals
  its $m^*$ at $\Delta t$. The $\nu = 0.01$ $\Delta t/2$ part is still running.
- The longer window separates the outcomes, the criterion this round was set up to test. At
  $T_{\rm sync} = 100$, only 3 of the 52 graded cells on each valid world lie between $10^{-6}$ and
  $10^{-2}$. The rest are below $10^{-12}$ or clearly above $10^{-2}$. At $T_{\rm sync} = 50$
  (rounds 1 and 2, all worlds) the count was 45 of 260. The same runs read at $T_{\rm sync} = 50$
  give larger budgets for most observers: on $\nu = 0.03$, READ 48, BALL 12, ENSTROPHY 96, KE 32.
  So the probe supports $T_{\rm sync} = 100$, $T_{\rm hold} = 10$, chosen on separation. Every
  observer except KE gets a smaller budget under it, READ included. That is for the owner to
  confirm, and it is not fixed here.
- The finite-gain observer exponent is negative at every graded observer's $m^*$ on both valid
  worlds (-0.12 to -0.18).
- Footprint: about 220 MiB and one core per part. The core and $\Delta t/2$ parts took 2.4 to 3.0 h
  each.
- Lost to a node failure: the $\nu = 0.02$ SENS and RANDOM part (NodeNotReady, then a failed mount
  and pod kill on the dying node; Failed, BackoffLimitExceeded). Nothing graded depends on it. It
  has not been resubmitted. The $\nu = 0.03$ SENS and RANDOM part and the $\nu = 0.01$ $\Delta t/2$
  and SENS/RANDOM parts are still running.

What the valid worlds show about the claim, recorded and not graded: one trajectory each. READ is
three ladder steps behind BALL on both. It is ahead of ENSTROPHY, its own amplitude factor, by one
to three steps. BALL synchronizes at $|k| \le 3$ ($\nu = 0.02$) and $|k| \le 2$ ($\nu = 0.03$),
inside the forcing scale, consistent with Inubushi and Caulfield (background, Section 1). On every
world the probe has measured (nine worlds over three rounds), READ has never been ahead of the best
classical control.

Consequence to decide before the pilot. If the coarser resolution of the ladder becomes 96,
Section 2's ladders move up: the pilot to $n = 96$ and 128, and the run to 128 and 192. From the
measured cost at $n = 64$ (about 3.5 h per chaotic trajectory) and a per-step cost scaling of
roughly $n^2\log n$, with steps scaling as $n$, one trajectory at $n = 192$ would take on the order
of 100 h on one CPU. That is an estimate, not a measurement. It is the case for a lower
resolution bar, or for splitting each trajectory's observers across Jobs. That is the owner's
decision, and it is not taken here.

What this does not do. It does not grade the claim. The probe exists to fix parameters. Its worlds
carry one trajectory each, and only two of its nine worlds meet the world criteria. The claim, the bars and the tolerance rules of Sections 1 to 5
are unchanged. The instrument may change before the pilot, through the world choice, the
resolution bar or the synchronization window, but only on the probe's own criteria (chaos,
resolution, separation of $\delta$, step refinement) and with every change recorded here. Changing
the claim or the bars in response to how READ fared would be fitting the registration to its own
probe, and is not done.

Pilot (training 20261072, test 20261073, $\nu \in \{0.03, 0.02\}$ at $n = 96$ and $128$, $K = 2$;
changed 2026-10-10 from $n = 64$ and 96 when the probe moved the coarser resolution to 96).
Submission path set up at b140c2e, not yet submitted. There are 24 NRP Jobs, one per (world, test
trajectory, part): the instrument and graded observers, SENS and RANDOM, and the $\mu_0/4$ reruns.
All are in the exempt class with `timeout 20h`. The core part at $n = 128$ is estimated at about
12 h, and the whole pilot at about 100 CPU-hours, scaled from round 3 and not measured. From this
change on, the observer and block tangents are carried for the graded observers only, since the
records use only theirs. A smoke test on Atlas ($n = 32$, $K = 2$) ran a world whole and then as six
per-trajectory, per-part pieces merged by the submitter. It gave bit-identical $\delta$ for every
observer, identical $\mu_0/4$ records and instrument fields, and tangents on the graded observers
only. The submitter's dry run passed every preflight guard. Submitted 2026-10-10, 17:54 to
18:03 UTC: all 24 accepted and fresh.

One part was lost and rerun. The Job `d8-pilot-p-nu020-n96-t0-others` (SENS and RANDOM, $\nu = 0.02$,
$n = 96$, trajectory 0) succeeded on cph-blade15.humboldt.edu, but its container log could not be
retrieved on two attempts ("unable to retrieve container logs"). The result block travels only in
the log, so it was lost. On the owner's instruction (2026-10-11) the finished Job was deleted and
the part resubmitted alone with `--only`. It used the same `d8_sync.py` (sha256 1bac5458...) and
config (e1c98524...) as the other 23, at 01:51 UTC. Its seeds are fixed, so it reproduces the lost
result. Lesson for the run: results should not travel only through Job logs. It fixes M1 and TOL_N by the
rules of Section 5, within their limits, and records the pilot's own grade.

## 8. Sealing procedure

1. Write the code and pass the self-test. Probe on Atlas or NRP, record Section 7, commit
   `probe.json`. Pilot, fix the tolerances, record them, commit `pilot.json` and `tolerances.json`.
2. Declare `OD:sync-observer` in `claims/transformations/OD.toml`. Verify the references in the
   theory note against Crossref. Rename this file to `PREREG-D8.md`, commit, record its blob hash
   in the track document and the README status ledger.
3. Run on the run seeds, grade with `d8_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test.
