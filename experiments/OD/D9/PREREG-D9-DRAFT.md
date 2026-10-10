# PREREG D9 (DRAFT): the barrier, where any observer-theory estimate meant for regularity must fail

Status: DRAFT 2026-10-10, not claim-bearing, not sealed. Code `d9_barrier.py` written, self-test PASS on Atlas at 2d004ec. Gate D9 of the OD track
(`experiments/DISCOVERY-TRACK.md`), registered after the track's declared order was complete. It
answers the test named in `notes/dynamical-read-operator.md` Section 7: any dynamical bound the
program proposes is run on a dyadic model known to blow up, and it must fail there.

D9 makes no claim about the Navier–Stokes equations, and no claim that Observation Theory does
anything. It is an instrument. It sorts candidate estimates into those that could bear on
regularity and those that cannot. It is built on a model where both blow-up and regularity are
theorems. D9 is a standing gate: a candidate estimate goes through it before any text calls that
estimate relevant to regularity.

## 1. Why a barrier, and why this model

The theory note's Propositions 2 to 4 use only the energy cancellation, Fourier triad support and
the energy inequality. Tao's averaged equation keeps the cancellation and the harmonic-analysis
estimates, a weakened form of the locality, and still blows up (note Section 7, checked against
arXiv:1402.0290v3 eq. 1.12). So statements of that kind alone cannot prove regularity. That
argument is an analogy, since Tao's operator lives on R^3. D9 replaces it with a measurement on a
model where the dichotomy is proved.

The model is the viscous dyadic model of Katz and Pavlović (2005), in the form studied by
Cheskidov (2008, Trans. Amer. Math. Soc. 360, 5101–5120; read against arXiv:math/0601074v2,
equation 1.1):

$$\frac{d}{dt}u_n + \nu\lambda^{2\alpha n}u_n - \lambda^n u_{n-1}^2 + \lambda^{n+1}u_n u_{n+1} = g_n,
\qquad n \ge 1,\quad u_0 = 0,$$

with $\lambda > 1$, viscosity $\nu \ge 0$ and dissipation degree $\alpha > 0$. Here
$(B(u,u))_n = -\lambda^n u_{n-1}^2 + \lambda^{n+1}u_n u_{n+1}$ satisfies $\sum_n u_n(B(u,u))_n = 0$,
the same energy cancellation as Navier–Stokes. The results D9 relies on, all from that paper, are:

- Theorem 4.2. Nonnegative initial data stay nonnegative, and the energy inequality holds from
  every time.
- Theorem 5.3, blow-up. For $\alpha < 1/3$ and $u_n(0) \ge 0$, for every $\varepsilon > 0$ there is
  an $M(\varepsilon)$ such that $\|u(t)\|^3_{1/3+\varepsilon}$ is not locally integrable on
  $[0, \infty)$ whenever $\|u(0)\|_\varepsilon > M(\varepsilon)$. Here
  $\|u\|_\gamma = (\sum_n \lambda^{2\gamma n}u_n^2)^{1/2}$.
- Global regularity for $\alpha \ge 1/2$ (abstract and Section 4). Local regularity holds for
  $\alpha > 1/3$.
- At $\alpha = 2/5$ the model has the same sharp nonlinear estimates as the 3-D Navier–Stokes
  equations (Section 1). That value lies in the gap $1/3 \le \alpha < 1/2$, where the paper
  proves neither blow-up nor global regularity.

So the model gives, by theorem, one world that blows up and one that is regular, with the same
cancellation and the same algebraic form. A candidate estimate that holds in both cannot by itself
separate blow-up from regularity.

## 2. Worlds

- $\lambda = 2$, $\nu = 1$, $g = 0$ (unforced).
- B (blow-up by Theorem 5.3): $\alpha = 1/4$.
- R (regular by the global-regularity theorem): $\alpha = 3/5$.
- G (the Navier–Stokes-like value in the open gap, $\alpha = 2/5$): RECORDED ONLY, never graded.
  D9 says nothing about it. A truncated simulation cannot settle an open problem of the model, and
  no text may cite D9 as evidence about it.

Truncation. The paper's own Galerkin scheme (eq. 4.2). Shells $n \le J$ are kept, the last shell
drops its $\lambda^{J+1}u_J u_{J+1}$ term, and energy is conserved by the nonlinearity exactly. The
ladder is $J \in \{16, 24, 32, 40\}$ (probe), with the top value set by what the integrator
resolves in double precision, since $\lambda^{2\alpha J}$ and $\lambda^{J}$ span many decades.

Initial data. Nonnegative and concentrated at the first shell: $u_1(0) = A$, $u_n(0) = 0$ for
$n > 1$. Theorem 5.3 guarantees blow-up only above an unstated $M(\varepsilon)$. The amplitude $A$
is therefore raised on a ladder in the probe until the positive control separates (bar I1), and the
same $A$ is then used in every world. If no amplitude on the ladder separates, D9 is INDETERMINATE
and the threshold is recorded as above the ladder.

Integrator. Stiff, implicit and adaptive (Radau, tight tolerances, from scipy). Accuracy is
checked by halving both tolerances, and the energy balance
$|u(t)|^2 + 2\nu\int\|u\|^2_\alpha = |u(0)|^2$ is checked to a declared relative error on every run.

Seeds. Only the RANDOM observer in candidate C2 draws random numbers. Probe 20261091, pilot
20261092, run 20261093, spare 20261094. All checked unused in this repository and in
geometric-evaluation-theory on 2026-10-10. (20261086 is used by D2v7.)

## 3. Candidates and how each is classified

A candidate is a functional $\Phi(J)$ of the truncated solution over a fixed horizon $[0, T]$.
Each candidate is classified from its behaviour along the $J$ ladder in worlds B and R.

- BOUNDED in a world. The increments $|\Phi(J_{i+1}) - \Phi(J_i)|$ shrink along the ladder by at
  least a declared factor per step, and the top value is within a declared tolerance of the
  extrapolated limit.
- DIVERGING in a world. $\Phi$ grows by at least a declared factor $D$ over the ladder, and the
  increments do not shrink.
- Otherwise UNSETTLED at this ladder.

The four classes are:

| class | in R | in B | reading |
|---|---|---|---|
| PASSES THE BARRIER | bounded | diverging | could bear on regularity; still not a proof |
| TRANSPARENT | bounded | bounded | holds where blow-up is a theorem, so cannot by itself give regularity |
| FALSE | diverging | either | fails where regularity is a theorem, so is not a valid estimate |
| UNSETTLED | otherwise | otherwise | the ladder cannot decide |

Entered at draft 0.1:

- C0, the positive control. $\Phi_0(J) = \int_0^T \|u^J(t)\|^3_{1/3+\varepsilon}\,dt$ with
  $\varepsilon = 0.05$. It must PASS by the two theorems. If it does not, the instrument cannot see
  a separation known to exist, and nothing else is graded.
- C1, the negative control: the note's Proposition 3 in dyadic form. For the observer that keeps
  shells $n \le N$, the feedback from the discarded shells is $r_N = -\lambda^{N+1}u_N u_{N+1}e_N$,
  since the coupling is nearest-neighbour, which is the exact dyadic counterpart of Proposition 2's
  octave. So $|r_N| \le \lambda^{N+1}(u_N^2 + u_{N+1}^2)/2 \le \lambda^{N+1}|u|^2 \le \lambda^{N+1}|u(0)|^2$ by the energy inequality, in
  both worlds and at every $J$. $\Phi_1(J) = \sup_{t \le T}|r_N(t)|/(\lambda^{N+1}|u(0)|^2)$ at
  $N = 6$ is bounded by 1, by theorem, in both worlds. So C1 is TRANSPARENT by construction, and a
  different class is a numerical error. It is entered to show on a model that provably blows up
  that the program's own Proposition 3 cannot tell the two worlds apart. That is the note's
  Section 7 claim, measured.
- C2, D8's observers carried to the dyadic model. $\Phi_2(J)$ is the finite-time synchronization
  budget (in shells) of a nudged copy for each D8 observer: BALL (the lowest shells), READ (shells
  ranked by the training mean of $u_n^2$ times the sensitivity of the tendency to shell $n$),
  ENSTROPHY and KE analogues, and RANDOM. Each uses D8's sustained synchronization rule. In world B
  the window must end before the blow-up time the probe measures, or the comparison is with a
  solution that has left every finite-$J$ approximation. No prediction is registered. The class of
  each observer's budget is the record.
- C3, a harmless-budget candidate in the spirit of Cheskidov and Shvydkoy's dissipation wavenumber
  (2014). $Q(t)$ is the smallest shell above which every shell's local Reynolds number
  $\mathrm{Re}_p = \lambda^p|u_p|/(\nu\lambda^{2\alpha p})$ is below $c_0$. That is, the shell's
  nonlinear turnover rate is below $c_0$ times its viscous rate. This is the dyadic analogue of their
  condition $2^{-p}\|u_p\|_\infty < c_0\nu$. Then $\Lambda(t) = \lambda^{Q(t)}$ and
  $\Phi_3^{(q)}(J) = \int_0^T\Lambda^q\,dt$ for $q \in \{1, 2, 5/2, 3\}$. Cheskidov and Shvydkoy's
  exponents ($L^{5/2}$ sufficient, $L^1$ for every Leray–Hopf solution) are for the Navier–Stokes
  equations, not this model. So no exponent is claimed, and the class of each $q$ is recorded. $c_0$
  is declared (probe) and not tuned per world. (Revised 2026-10-10, before any probe. The first
  definition compared a shell's nonlinear exchange with its dissipation. In the dissipation range
  those are nearly equal by the shell's own energy balance. A smoke run at $J \le 10$ on Atlas then
  gave $Q = J$, the top shell, in both worlds at every $J$, so C3 diverged by construction and its
  class said nothing about the flow.)

## 4. Bars

- I1 (instrument). C0 PASSES THE BARRIER at the declared amplitude.
- I2 (numerics). In every run, halving both tolerances changes every graded $\Phi$ by less than a
  declared relative amount, and the energy balance closes to a declared relative error.
- N1 (negative control). C1 is TRANSPARENT.

Verdict.
- PASS: I1, I2 and N1 hold. The classes of C2 and C3 are then the gate's result and are entered in
  `claims/transformations/OD.toml` as barrier classifications.
- INDETERMINATE: I1 misses (the ladder or amplitude cannot see the known blow-up), or I2 misses.
- FAIL: N1 misses with I2 holding. That would contradict a theorem of the model on a numerically
  sound run, so the code or the derivation in Section 3 is wrong and is corrected before anything
  else.

No result of D9 is a claim that a candidate proves anything. PASSES THE BARRIER is necessary for
an estimate to bear on regularity, not sufficient.

## 5. What falsifies, and what D9 cannot do

A positive control that does not separate the worlds says the truncation ladder cannot see blow-up
in this model. The gate then says nothing, and a finer ladder or a different instrument is needed.
A negative control that is not transparent says the code is wrong, since its boundedness is a
theorem. A D8 observer whose budget is TRANSPARENT says that observer's finite-time budget is blind
to the singularity, however well it ranks modes in a regular flow. That would be a statement about
the limits of D8's result and not about D8's claim.

What D9 cannot do. It cannot certify a candidate as a regularity criterion. It cannot say anything
about $\alpha = 2/5$ or about the Navier–Stokes equations. It tests candidates against one dyadic
model. A candidate could separate this model's worlds by exploiting the nearest-neighbour cascade,
a structure the Navier–Stokes equations do not have. A wider barrier, Tao's averaged operator or
other shell models, is a later registration.

## 6. Self-test, probe, pilot (before sealing)

Self-test (`d9_barrier.py --selftest`, 15 checks, PASS on Atlas 2026-10-10 at 2d004ec). Beyond the list below it also checks the analytic Jacobian against a finite difference, the energy balance with dissipation, C1 <= 1/2 on a dissipative run, both nudging extremes, and the harmless-shell function on two constructed fields. The list: the energy cancellation $\sum u_n B_n = 0$ exactly on random vectors. The
truncation (4.2) conserves energy at $\nu = 0$. Nonnegativity is preserved from nonnegative data
(Theorem 4.2). C1's identity $r_N = -\lambda^{N+1}u_N u_{N+1}e_N$ is checked against a finite
difference. The classification rule is checked on constructed sequences.

The self-test now has 16 checks and passes on Atlas at 31a77a3. Two checks were added for the C3
redefinition.

Smoke runs, before any probe, on Atlas, with $J \in \{6, 8, 10\}$, $T = 0.2$ and $A = 100$, B and R
worlds, graded end to end. Not claim-bearing.
- First run (ca25c38). The pipeline works from integration through the grader. Halving the
  tolerances changes the graded functionals by at most $7\times10^{-11}$, and the energy balance
  closes to $6\times10^{-11}$. C1 is about 0.16 in both worlds and classes TRANSPARENT. C0 diverges
  in B, and in R it is UNSETTLED at this ladder, so the smoke grade is I1 INDETERMINATE, as expected
  at $J \le 10$. C3 as first defined gave $Q = J$ at every $J$ in both worlds, a defect of the
  definition, which was then revised (Section 3). It cost 9 min, almost all of it C2.
- Second run (a02bf21, C2 off). With the revised C3 at $q = 1$, R is 4.0, 7.7, 12.0 and B is 12.7,
  50, 201. B sits at the ceiling $\lambda^J T$ that energy piled at the top shell would give, and R
  is far below it, so the candidate is no longer degenerate. Its higher $q$ are dominated by the
  initial transient at this horizon and are for the probe to judge.

Probe record (PARTIAL, 2026-10-10). Amplitudes 10 and 100 are complete. The R world at
amplitude 1000 is still running, and nothing is fixed until it finishes and the amplitude is
chosen. There were six NRP Jobs, one per world (`submit_d9_nrp.py`, code at 23d0992, exempt class
1 CPU / 2Gi, `timeout 12h`), submitted 13:02 to 13:04 UTC. The config was `prereg_config.json`'s
probe candidates: $J \in \{16, 24, 32, 40\}$, $T = 1$, $\varepsilon = 0.05$, $N = 6$, $c_0 = 1$,
$\mu = 50$, $T_{\rm sync} = 1$, $T_{\rm hold} = 0.2$. Collected as `probe_pr_{B,R}_A{10,100}.json`
and `probe.json` on Atlas. Each amplitude pair was graded with `d9_barrier.py`'s own `grade`, with
the probe worlds renamed to R and B. That is a probe grade and not a verdict.

Instrument, the same at both amplitudes. The probe grade is PASS at both.
- I1. C0 PASSES THE BARRIER. In R it is the same at every $J$ (257 at $A = 10$; $1.26\times10^5$
  at $A = 100$). In B it grows about eight to ten times per 8 shells: $4.56\times10^4$ to
  $2.48\times10^7$ at $A = 10$, and $2.35\times10^8$ to $2.20\times10^{11}$ at $A = 100$.
- I2. Halving both tolerances changes the graded functionals by at most $1.7\times10^{-11}$. The
  energy balance closes to $1.0\times10^{-10}$.
- N1. C1 is TRANSPARENT: constant in $J$ in both worlds (R 0.0046 and 0.0386, B 0.0365 and 0.043,
  at $A = 10$ and 100), under its bound of 1/2. This is the theory note's Section 7 claim measured
  on a model that provably blows up: the program's own Proposition 3 does not tell the two worlds
  apart.

Candidates, the same classes at both amplitudes. These are recorded; the probe grades nothing.

| candidate | R along $J$ | B along $J$ | class |
|---|---|---|---|
| C3, every $q \in \{1, 2, 5/2, 3\}$ | constant | grows by many decades | PASSES THE BARRIER |
| C2 BALL | 1 shell | 1 shell | TRANSPARENT |
| C2 KE | 1 shell | 1 shell | TRANSPARENT |
| C2 READ | 1 ($A = 10$), 12 ($A = 100$) | 16, 24, 32, 40 (every shell) | UNSETTLED |
| C2 ENSTROPHY | 7, 14 | every shell | UNSETTLED |
| C2 SENS | 8, 15 | every shell | UNSETTLED |

What the classes say.
- BALL and KE synchronize the whole system from the lowest shell alone, in both worlds. This fits
  the model's one-way cascade: Cheskidov notes the lack of backward energy transfer for
  nonnegative data. So a D8-type synchronization budget is blind to the singularity.
- READ, ENSTROPHY and SENS need every shell in B. Their budget therefore tracks the truncation,
  growing linearly from 16 to 40. That is 2.5 times over the ladder, below the declared factor
  $D = 4$, so the rule leaves them UNSETTLED and not DIVERGING. A longer ladder would decide them,
  but linear growth with $J$ means only that every shell has to be read. It does not detect blow-up
  in any useful sense.
- C3 passes. It is the dyadic analogue of Cheskidov and Shvydkoy's dissipation wavenumber, a
  classical regularity criterion. Its passing shows that the barrier recognises a real criterion.
  It is not an Observation Theory result: by the track's anti-circularity contract, a classical
  quantity reproducing a result does not count for the theory.

Cost, from the Jobs' start and completion times: B at $A = 10$, 100, 1000 took 70.6, 36.2 and
119.9 min. R at $A = 10$ and 100 took 25.9 and 63.3 min. R at $A = 1000$ is still running after
2 h. At $J = 16$, R at $A = 1000$ looked blow-up-like (harmless shell at the top, READ needing every
shell), probably an initial transient. Whether it settles as $J$ grows decides whether
$A = 1000$ separates the worlds.

Open for the owner before the pilot: the amplitude. Both 10 and 100 separate the worlds cleanly
in C0 and give the same classes.

Probe (seed 20261091). It fixes the $J$ ladder's top, the amplitude $A$, the horizon $T$, $c_0$,
the tolerances, $D$ and the shrink factor. It records the blow-up time of world B as the time at
which $\|u^J\|_{1/3+\varepsilon}$ peaks at the top truncation, and the cost.

Pilot (seed 20261092). It runs the full candidate set at a reduced ladder and fixes nothing
further. The bars carry no pilot-derived tolerance, because every tolerance is a numerical-accuracy
quantity fixed by the probe.

## 7. Sealing procedure

1. Write the code and its self-test. Probe and pilot on NRP (exempt class; the systems have at most
   40 ODEs), and record Section 6.
2. Declare `OD:barrier` in `claims/transformations/OD.toml`. Rename this file to `PREREG-D9.md`,
   commit, and record its blob hash in the track document and the README status ledger.
3. Run, grade, and commit `results.json` and `grade.json` as executed.
