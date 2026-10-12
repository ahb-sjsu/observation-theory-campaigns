# OP4 (DESIGN DRAFT): D6v3's spectral selector on D8's flow, the instrument or the system

Status: DESIGN DRAFT, 2026-10-12. Not a registration and not claim-bearing. Gate OP4 of the OP track
(`experiments/OPEN-PROBLEMS-TRACK.md`), the test that OP3's record suggests in its Section 5
(`experiments/OP/OP3/OP3-RECORD-DRAFT.md`). Nothing here is fixed until a probe has settled the items
marked PENDING by rules this draft states before the probe runs.

## 1. The question

D6v3 and D8 disagree, and they differ in three ways at once. D6v3 (sealed, PASS) chose sensors on
linear and Lorenz-96 systems by the spectrum of the exact window Gramian and needed fewer sensors
than the energy ranking. D8 (pilot, 7 of 8 cells) chose Fourier pairs for nudging forced
two-dimensional turbulence by READ, a ranking of single modes, and needed more pairs than BALL, the
ordering by scale, in every cell. OP3 could not say whether the split belongs to the instrument (a
Gramian spectrum searched over sets, against a diagonal ranking of modes) or to the system (linear
and low-dimensional, against turbulence, where the instability sits in the large scales near the
forcing).

OP4 takes D6v3's instrument to D8's flow and changes nothing else. It uses the same worlds, seeds,
test trajectories, nudging gain, synchronization rule and ladder as D8's pilot, and compares its
budget with BALL's and READ's cell by cell.
- If the spectral selector matches or beats BALL, the per-mode ranking was the weak link, and the
  read operator's spectrum can choose what a nudged copy of turbulence must read.
- If it also loses to BALL, scale is what this flow asks an observer to read, even of the instrument
  that won on linear systems. OT's selection results then stop at the linear and low-dimensional
  systems D6v3 covered.

Either outcome is worth recording, and the draft fixes now which reading each outcome gets.

## 2. Carrying the instrument across

| D6v3 on a linear system | OP4 on D8's flow |
|---|---|
| State $x' = Ax$ | Tangent dynamics along the training trajectory, $\delta' = DF(u(t))\,\delta$ (D8's `ftangent`) |
| Candidate sensor: a row $c_i$ | Candidate pair $k$: its real and imaginary Fourier coefficients |
| Window Gramian $W_S(T) = \int_0^T e^{A^T t} C_S^T C_S e^{A t}\,dt$ | Window Gramian on the leading tangent subspace, $W_S^U = \sum_j (C_S \Phi(t_j) U)^T (C_S \Phi(t_j) U)\,\Delta t$, summed over windows along the training trajectory |
| Identifiable count $d_{obs} = \#\{\lambda_i(W_S) > B^2/\rho^2\}$ | The same count on $W_S^U$ |
| Required count $m$, a ladder | The flow's finite-time unstable dimension $d_u$ over the window, measured on the training trajectory |
| Greedy on $d_{obs}$, ties by the $m$-th eigenvalue, exact search where checkable | The same greedy. No exact search, since the candidate pool has thousands of pairs |

The reduction that makes it computable. $U$ holds $m'$ orthonormal tangent directions at each
window's start, the leading Lyapunov vectors from a QR iteration along the spin-up (D8's
`lyapunov` machinery). Propagating them over the window gives $\Phi(t_j) U$, and each candidate
pair's rows $C_k \Phi(t_j) U$ are read off the propagated vectors' Fourier coefficients. All
candidates are scored at once, and every Gramian is $m' \times m'$. With $U$ spanning the whole
tangent space, $W_S^U$ is the full window Gramian, and the self-test checks that identity on a small
linear system, where OP4's selector must reproduce D6v3's.

From selection to D8's test. The greedy order is a ranking of pairs, GRAM. It is continued past
the count, after $d_{obs}$ reaches $d_u$, by the largest gain in the $m'$-th eigenvalue, so it fills D8's
ladder. GRAM enters D8's nudging protocol as one more graded observer, and its budget $m^*$ is
measured exactly as D8 measures READ's and BALL's. The count GRAM's greedy needs to reach $d_u$ is
recorded beside it, since it is the selector's own prediction of how many pairs suffice.

Relation to the field. Empirical observability Gramians are the standard instrument for sensor
placement in nonlinear systems. Krener and Ide (Measures of unobservability, Proc. 48th IEEE CDC,
2009, 6401 to 6406) introduce the local observability Gramian and use it to place a sensor in the
flow of two point vortices. Singh and Hahn (DYCOPS 2004) and Serpas, Chu and Hahn (2013) place
sensors by empirical Gramians, and Kazma and coauthors (2023 and 2024) by submodular observability
measures. OP4's instrument is that family in D6v3's form, which counts directions
identifiable at a budget instead of maximizing a determinant or a trace. So OP4 is also a test of
whether the standard observability instrument, in its OT form, beats scale for nudging turbulence.
The novelty is narrow, and a database search comes before any claim of it.

## 3. Design

Worlds, seeds and trajectories: D8's pilot ($\nu \in \{0.03, 0.02\}$ at $n = 96$ and 128, training
seed 20261072, test seed 20261073, $K = 2$). D8's pilot budgets for BALL, READ, ENSTROPHY and KE come
from the same seeds and so are paired with GRAM cell by cell. Reusing them saves a full rerun of
the controls. One control is rerun in one cell to check that it reproduces, since D8's results are
seed-deterministic (D8's own smoke test found bit-identical budgets across a split).

GRAM's parameters, all PENDING the probe and fixed by the rule below.
- The window $T$ and the number of windows on the training trajectory.
- The subspace size $m'$, at least twice $d_u$.
- The threshold fraction $c = \text{frac} \times \lambda_{max}(W^U_{all})$, as D6 defines it.

The rule, fixed before the probe and blind to every budget. The parameters are chosen from the
training trajectory's Lyapunov spectrum and Gramian alone, never from any nudging result. $T$ is one
Lyapunov time $1/\lambda_1$, and $m'$ is the smallest multiple of 8 that is at least twice $d_u$. frac
is the largest of D6's $\{0.001, 0.01, 0.1\}$ at which the all-pairs Gramian identifies every one of
the $m'$ directions. GRAM's nudging budget is not looked at until the parameters are written down.

Bars, in D8's form and fixed from the pilot of OP4 by D8's rules: GRAM's ladder index against
BALL's, pooled over cells, with a margin and a per-cell tolerance in ladder steps. Also GRAM against
READ, recorded.

Reading the outcomes, fixed now.
- GRAM ahead of or level with BALL, pooled: "instrument". The per-mode ranking was the weak link.
- GRAM behind BALL and ahead of READ: "both". The spectrum helps, and scale still wins.
- GRAM behind BALL and not ahead of READ: "system". In this flow scale is what to read, for the
  instrument that won on linear systems as for the per-mode ranking.

## 4. Instrument checks before the probe

- With $U$ spanning the whole state of a small linear system, $W^U_S$ equals D6's Van Loan Gramian,
  and OP4's greedy returns D6v3's selection on one of D6's worlds.
- The propagated tangent vectors match central differences of D8's solver over the window (D8's
  tangent is exact for the quadratic map; the propagator is checked over a short window).
- On a synthetic system with a known unstable subspace, a pair set that observes it gives
  $d_{obs} = d_u$, and one that misses it gives less.
- GRAM with every pair observed reaches $d_{obs} = m'$.

Code and self-test (2026-10-12). `op4_gram.py` imports D8's solver, tangent, rankings and
`nudge_record` and D6v3's Gramian and greedy, and copies neither. It runs in two parts, so that the
eight cells can run in parallel. The `gram` part computes the instrument once per world and caches
the ordering, and the `nudge` part runs per test trajectory. `op4_config.json` holds the
instrument's settings ($m_0 = 24$ tangent vectors, QR every 1.0 time unit, 20 time units to align and 40 to
measure, 4 windows of 20 samples, $T_w$ clipped to $[1, 20]$). Self-test on Atlas, eleven checks, all PASS.
- OP4's greedy reproduces D6's on Lorenz-96 at $n = 10$, at four thresholds and counts, through full
  ten-sensor orderings. Where D6's set never reaches the count, OP4 reports it as not reached.
- The sampled Gramian of the propagated directions equals D6's Van Loan Gramian within
  $3.6 \times 10^{-5}$.
- On a system with a known unstable subspace, the pairs that observe it identify $d_u$ directions and
  the pairs that miss it identify none, and the greedy takes the first pairs first.
- The parameter rule is right on unordered exponents.
- The QR exponents of a diagonal system are exact.
- The propagated tangent equals the central difference of D8's solver over 0.5 time units within
  $3.2 \times 10^{-10}$.
- The pair readings sum to half the full Gram matrix of the propagated vectors, since each pair
  stands for $\pm k$, within $10^{-16}$.
- Every direction is identified with every pair observed.

Two first versions of checks failed and were mine. The D6-equivalence check first compared only a
two-sensor selection, and was strengthened. Its reached-count condition then demanded a count
where D6's own set never reaches one, and was corrected to compare with D6's outcome.

Smoke run (Atlas, an unresolved world at $n = 48$ with short times, both parts and a BALL recheck,
about 3.5 minutes in all). It found one bug in the code. Over a short measuring time the QR exponents
do not come out ordered, and the code took the first as $\lambda_1$. The draft defines $\lambda_1$ as the
leading exponent, so the code now sorts, and a self-test check covers it. After the fix the rule gave
$\lambda_1 = 0.109$, $T_w = 9.2$, $d_u = 3$, $m' = 8$ and frac 0.01, met in every window. The count was reached
after 2 pairs, and GRAM's first twelve pairs lay at $|k|$ from 3.0 to 5.1, near the forcing shell. The
world is unresolved and too short to mean anything about synchronization; it shows only that the
pipeline runs.

Probe (owner's decision of 2026-10-12: one world, $\nu = 0.03$, $n = 96$, D8's pilot seeds, both test
trajectories and a BALL recheck on trajectory 0). Atlas, screen `op4-probe`, code at a547af8, started
15:30 UTC. The Gramian phase finished after 6362 s, cached as `gram/p_nu030_n96_pilot.json` (sha256
dfc74612...). Its parameters came from the registered rule, before any nudging ran.
- Lyapunov spectrum from the QR iteration (24 vectors, 20 time units to align, 40 to measure). Six
  exponents are positive (0.083, 0.080, 0.070, 0.057, 0.050, 0.041). The next four are near zero
  ($-0.001$, $-0.004$, $-0.006$, $-0.018$), and the rest are clearly negative, down to $-0.35$. D8's probe
  measured a leading exponent of $+0.06$ for this viscosity with one vector, and the finite-time
  values differ by window.
- The rule's parameters: $\lambda_1 = 0.083$, so $T_w = 12.0$; $d_u = 6$, so $m' = 16$. frac = 0.001, the
  smallest of the three, and the all-pairs Gramian identifies all 16 directions in every window
  only at that fraction. The thresholds by window are 0.129 to 0.262. The leading finite-time exponents
  by window are 0.08 to 0.14.
- The count $d_u = 6$ is reached in every window after 2 pairs, so from the third pair on GRAM's order is
  set by the tie-break, the smallest eigenvalue of the 16-direction Gramian.
- GRAM's first twelve pairs lie at $|k| = 2.83$ to $4.47$, around the forcing shell ($k_f = 4$): (2, 3), (4, 0),
  (3, 0), (3, 2), (3, $-2$), (3, $-1$), (3, $-3$), (1, $-3$), (1, $-4$), (2, $-3$), (4, 2), (2, 2). No $|k| = 1$ pair is
  among its first 32. Only 2 of its first 24 lie within BALL's 8-pair synchronizing set ($|k| \le \sqrt 5$),
  at positions 20 and 21.

What the Gramian phase shows before any nudging result, recorded and not acted on. The instrument
ranks pairs near the forcing scale first, as READ did. The large scales that BALL takes first come
late. A hypothesis for why, which this probe does not test: the rule counts only the positive
exponents ($d_u = 6$) as the directions to identify, while four more are near zero. Over $T_{sync} = 100$ an
error along a near-neutral direction barely decays, so synchronization may need those directions
observed as well. If they sit at the large scales, a rule that counts them would move those scales
forward. Changing the rule now would be fitting it to this probe. Any such rule is a new
registration, declared before a fresh probe.

## 5. Cost and platform

The Gramian needs $m'$ tangent propagations per window, over a few windows of the training
trajectory, which is small against one nudging record. The nudging record for GRAM costs what one
graded observer costs in D8: about 2.5 hours per cell at $n = 96$ and 4 to 11 hours at $n = 128$,
depending on the node. That is eight cells. By the owner's instruction for this campaign, it runs
on Atlas, one core per cell, unless the owner chooses NRP as D8 used.

## 6. What waits

D8's eighth pilot cell, so that GRAM is compared with complete controls. Then the code
(`op4_gram.py`, importing D8's solver, tangent and nudging machinery), its self-test on Atlas, and a
probe on one D8 world to fix the PENDING parameters by the rule above.
