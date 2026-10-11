# OP2 (DESIGN DRAFT): which modes a reduced model should carry explicitly, so that the rest needs the least memory

Status: DESIGN DRAFT, 2026-10-11. Not a registration and not claim-bearing. Gate OP2 of the OP track
(`experiments/OPEN-PROBLEMS-TRACK.md`). It becomes `PREREG-OP2-DRAFT.md` once its probe has fixed the
items marked PENDING, by the rules this draft states before the probe runs.

## 1. The open problem

The Mori–Zwanzig formalism writes the evolution of any chosen set of observables exactly, as a
Markov term, a memory integral over their past and orthogonal dynamics. A reduced model is cheap
when the memory is short. How long it is depends on what the model carries explicitly, and nobody
has a rule for choosing that.

The work nearest to OP2 is Tian, Lin, Anghel and Livescu (arXiv:2108.13288, 2021), who learn the
operators from data for isotropic turbulence. They use Mori's linear projection and the algorithm
of Lin and coauthors (arXiv:2101.05873), which recovers the Markov operator and every memory
kernel recursively from two-time correlations. They compare four hand-chosen sets of observables.
Their findings are the starting point here.
- Prediction errors depend strongly on the set. The set made of the terms of the filtered equations
  (the divergence of the velocity products and the pressure gradient) predicts over 50 percent
  better than the others.
- That same set shifts the dynamics from the memory kernel to the Markov term, and its memory
  kernel decays faster and more smoothly.
- The memory length grows with the filter scale and stays within several Kolmogorov times.
- They state the selection problem directly. Observables with smaller and shorter-correlated
  orthogonal dynamics are preferable, which "adds another layer of complexity in selecting
  observables". They choose kinds of observables by hand and do not choose which modes to keep.

Why the t-model works is still explained through renormalization (Stinis; Price and Stinis,
arXiv:1707.01955), and the memory length in MZ closures is fitted or set dynamically (Parish and
Duraisamy, arXiv:1611.03311; arXiv:1906.01411). A search on 2026-10-11 found no rule that chooses
which modes stay explicit so as to shorten the memory.

## 2. Why the read operator should bear on it

The memory term carries the influence of everything not carried explicitly on what is. To first
order that influence is the read of the unresolved modes by the consumer's tendency, $J_k x_k$ for
mode $k$, and READ ranks modes by its variance (OP1 Section 1; theory note, Proposition 4). Moving
the modes with the largest read into the explicit set removes the largest first-order sources of
memory. ENERGY moves the loudest modes, whether or not the consumer reads them. BALL moves the
nearest scales.

There is a reason to expect the effect to show in the memory rather than only in the one-step
error. A mode that is read strongly but varies slowly feeds the consumer the same signal for many
steps, and when it is left out, a memory kernel must reconstruct that signal from the consumer's
past. Carried explicitly, it costs nothing in memory. The draft tests whether that happens, and
whether READ finds such modes better than energy or scale.

## 3. The design

World and data. OP1's world, its cached probe trajectories and, later, its pilot and run
trajectories (D8's forced turbulence, $\nu \in \{0.03, 0.02\}$, sampled every 0.5). Using OP1's
data means OP2 needs no new simulation for its probe and that the two gates share their worlds.
Whether the sample interval of 0.5 is fine enough for the memory is checked on the probe
(PENDING; Tian and coauthors found the kernel's shape insensitive to the interval once
normalized, and an optimal interval for each horizon).

Observables. For each cutoff $k_c$, ranking $R$ and budget $r$: the consumer's coordinates, the $r$
pool pairs ranked first by $R$, and the TEND observable on them (OP1's lift, the consumer's
tendency on the chosen pairs), with a constant. TEND is included because OP1's probe and Tian and
coauthors' set 4 both found that the equation's own terms move the dynamics into the Markov term.
Without it, the memory would be measuring the linear dictionary's inability to represent products,
not the modes left out.

Operators. Mori's projection with the time-average inner product, as in Lin and coauthors and in
Tian and coauthors: two-time correlations $C(n) = \langle g((n + i)\Delta)\, g(i\Delta)^T \rangle_i$,
the Markov operator $\Omega^{(0)} = C(1) C(0)^{-1}$, and the kernels recursively from
$C(n + 1) = \sum_{l=0}^{n} \Omega^{(l)} C(n - l)$. A ridge term on $C(0)$ is fixed on the probe (PENDING).

Rankings. READ, ENERGY, BALL, SENS and RANDOM exactly as in OP1, computed on the training
trajectory. Records: NONE (the consumer and its TEND alone) and the per-mode quantities.

Quantities per cell (world, $k_c$, ranking, $r$).
- $E_L$, the consumer's forecast error at the declared horizons of the best linear predictor with
  $L$ lags, $g(n + 1) \approx \sum_{l=0}^{L} A_l\, g(n - l)$ fitted by least squares (the Wiener
  projection of Lin and Lu, J. Comput. Phys. 2021), for $L \in \{0, 1, 2, 4, 8, 16\}$. $E_0$ is the
  Markov forecast, OP1's quantity under TEND. The forecast of the truncated generalized Langevin
  equation with the orthogonal dynamics set to zero (Tian and coauthors, eq. 36) is recorded beside
  it as $E^{gle}_L$. It is not the graded forecast, because Mori's orthogonal dynamics are orthogonal
  only to the observables at the initial time and not to their later history, so dropping them does
  not give the best predictor. The self-test shows the difference on a system with a known optimum.
- $L^*$, the smallest $L$ whose error is within a declared fraction of $\min_L E_L$, the memory the
  model needs.
- $\tau_{90}$ and $\tau_{int}$ of the consumer block of the kernel, as defined by Tian and coauthors
  (the delay at which its norm falls to 10 percent of its first value, and the integral of the norm
  over its first value).
- The memory share, $\sum_{l \ge 1} \|\Omega^{(l)}_{CC}\| / \|\Omega^{(0)}_{CC}\|$.

The claim, in the form it will be registered. At matched $r$, the modes READ makes explicit leave a
consumer memory that is shorter (smaller $\tau_{90}$) than the memory left by ENERGY's or BALL's,
and the best forecast with memory, $\min_L E_L$, is no worse. Which of $\tau_{90}$, $L^*$ and the
memory share is the graded statistic is chosen on the probe by one rule fixed here and blind to
READ. The rule picks the statistic that agrees best between the two halves of each probe training
trajectory, pooled over every ranking, which is a reliability criterion that never looks at READ's
standing.

Controls and nulls. ENERGY and BALL are graded controls and RANDOM is the null, as in OP1. A
statistic on which RANDOM is as good as the structured rankings measures nothing about the choice,
so the draft will require each structured ranking to beat RANDOM pooled (the E1 form of OP1).

Instrument checks before the probe.
- On a linear system whose consumer is driven by a hidden autoregressive variable, the extracted
  kernel equals the analytic one. Carrying the hidden variable explicitly removes the memory
  exactly. This is OP2's claim in miniature, where it must hold by construction.
- The generalized fluctuation–dissipation relation for Mori's projection,
  $\Omega^{(l)} C(-\Delta) = -\langle W_{l+1} W_1^T \rangle$ (Lin and coauthors; verified by Tian and
  coauthors), holds on the flow data within a declared tolerance. This checks the extraction on
  real data, independently of any ranking.
- With $L = 0$ the forecast equals OP1's TEND forecast up to the difference between a ridge
  regression and $C(1) C(0)^{-1}$.

Self-test (`op2_mz.py --selftest`, Atlas, 2026-10-11), seven checks, all PASS. A consumer $x$ is
driven by a hidden autoregressive $y$ ($x' = 0.5 x + 0.8 y$, $y' = 0.9 y + \eta$, 200,000 samples).
- From the exact correlations, the consumer alone has memory (kernel norm 0.054 summed over eight
  lags), and carrying $y$ explicitly removes it ($4.9 \times 10^{-15}$).
- Kernels learned from the data match the exact ones within $2 \times 10^{-4}$. With $y$ explicit
  the Markov operator is the true transition within 0.0017. The recursion reproduces the
  correlations exactly, and the fluctuation–dissipation relation holds on the data within
  $10^{-4}$.
- The predictor with one lag reaches the analytic optimum for the consumer alone (0.2346 against
  0.2334, the Markov predictor 0.2617). With $y$ carried, the consumer is forecast exactly
  ($2 \times 10^{-6}$).
- The memory statistics and $L^*$ are right on a constructed kernel sequence.

Two first versions of checks failed, and both failures were mine, not the code's. A threshold for
"the consumer alone has memory" was a guess (0.3 against a true 0.054) and was replaced by the exact
correlations. A check that expected the truncated generalized Langevin forecast to reach the optimum
was wrong in principle, for the reason given above, and led to the Wiener predictor becoming the
graded forecast.

## 4. What would make OP2 a negative result, stated now

READ's explicit set leaving as long a memory as ENERGY's or BALL's, pooled. Or a statistic that
cannot separate the structured rankings from RANDOM, in which case OP2 reports that the memory of
this consumer does not depend on which modes are explicit at these budgets. Either outcome is
recorded as it falls.

## 5. Dependence on OP1

OP2 uses OP1's code for the world, the split, the rankings and TEND, and OP1's trajectories. If
OP1's lift rule (OP1 draft, Section 7) excludes TEND, OP2 is redesigned before its probe, since
its observables assume TEND. OP2 does not wait for OP1's verdict, because the two claims are
distinct. OP1 asks about the Markov forecast and OP2 about the memory that remains.

## 6. Next steps

1. Done: `op2_mz.py`, importing OP1's module (the correlation recursion, the lag predictor, the
   generalized Langevin forecast as a record, the memory statistics and the checks above).
2. Done: the self-test on Atlas. Next, a probe on OP1's cached probe trajectories (no new
   simulation), after OP1's lift rule is applied to its round 2.
3. Fix the PENDING items by the rules above, then write `PREREG-OP2-DRAFT.md` with bars in the form
   of OP1's (E1, L1, L2 over lifts replaced by the two cutoffs, N1).
