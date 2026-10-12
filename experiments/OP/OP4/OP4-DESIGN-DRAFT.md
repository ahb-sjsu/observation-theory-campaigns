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
