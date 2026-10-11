# PREREG OP2 (DRAFT): which modes a reduced model should carry explicitly, so that the rest needs the least memory

Status: DRAFT, not sealed, not claim-bearing. Gate OP2 of the OP track
(`experiments/OPEN-PROBLEMS-TRACK.md`). Written 2026-10-11 as `OP2-DESIGN-DRAFT.md` and renamed after
its probe, when the owner sent OP2 to a pilot. Sections 1 to 3 are the design as it stood before
the probe, with the probe's record at the end of Section 3. Section 4 holds the bars, Section 6 the
pilot. The grader and the tolerance rules (`op2_grade.py`) were written before the pilot runs.

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

Probe (Atlas, 2026-10-11, code at 274d27c, OP1's cached probe trajectories at $\nu = 0.02$ and
$0.03$, $n = 96$; both worlds clean, about 6 minutes each).

READ-blind results first.
- The statistic-choice rule. $\tau_{90}$ is degenerate: it equals 8.0, the 16-lag ceiling, in all
  200 half-records, so the kernel's consumer block has not fallen to 10 percent within 8 time
  units at this sample spacing. Split-half agreement over every cell and ranking: $\tau_{int}$
  Spearman 0.908; the memory share 0.985. The rule picks the memory share.
- The fluctuation–dissipation relation on the flow data is off by 10 to 16 percent (maximum over
  cells at lags 1 to 3), against $10^{-4}$ on the synthetic test. That is consistent with finite
  samples (2000 against 56 to 192 observables). No tolerance had been declared, so it is recorded
  and not graded.
- The lag predictor overfits at long memory. At $k_c = 5$ its error passes the climatology by
  $L = 8$ (1.08 for NONE at $\nu = 0.02$), with up to 3264 lag features against 2001 samples. At
  $k_c = 3$ the minimum sits at $L = 2$ to 4. So $L^*$ and $\min_L E_L$ are set by the sample budget
  where the dictionary is large, and the ladder needs a cap tied to it before any registration. The
  memory share comes from the correlation recursion, not from the lag regression, and is not
  affected.
- Memory matters for this consumer. At $\nu = 0.03$, $k_c = 3$ the best error with memory is 0.114
  for READ's $r = 2$ dictionary, against about 0.30 for OP1's Markov TEND forecast of the same cell.

READ's standing, read after the rule (probe, not a verdict). On the memory share, against the
better of ENERGY and BALL in each cell, the pooled advantage is $-2.8$ percent, with READ behind in 14
of 20 cells. Pooled shares are READ 0.533, ENERGY 0.574, BALL 0.524 and RANDOM's median 0.640. So
READ leaves clearly less memory than ENERGY, every structured ranking beats RANDOM, and the
ordering by scale leaves slightly less than READ. On the best error with memory, READ is level
($-0.5$ percent pooled). This is the pattern of D8, where BALL was also the best control, and not
that of OP1's TEND cells at $\nu = 0.03$, $k_c = 3$, where READ led.

Owner decisions (2026-10-11, after the probe). The lag ladder is capped by the sample budget. The
lag predictor's $d(L + 1)$ features may not exceed $N/4$, with $N$ the training samples; $L = 0$ is
always fitted (`lag_budget_ratio` 4 in `op2_config.json`). With 2000 samples this allows $L$ up to 4
for 56 observables, up to 2 for 160 and only 1 for 224, so at $k_c = 5$ and large $r$ the forecast
can use one lag of memory at most. The memory share, the graded statistic, comes from the
correlation recursion and is not affected. No tolerance was set for the fluctuation–dissipation
check, so it stays a recorded check and is not graded. OP2 goes to a pilot.

## 4. Bars, outcomes and what falsifies

A graded cell is one (world, $k_c$, $r$). The statistic is the memory share $s$ of the consumer
block, chosen on the probe by the split-half rule. Lower is better. READ's advantage in a cell is
$a = (s_{ctrl} - s_{READ}) / s_{ctrl}$, with $s_{ctrl}$ the lower of ENERGY's and BALL's shares there.

- E1, the instrument. Pooled over cells, READ, ENERGY and BALL each leave a smaller share than the
  RANDOM median, so that the share measures something about the choice.
- L1, the claim. The pooled advantage is at least M1, and no cell's advantage is below $-$TOL1.
- L1E, the forecast is not given up for it. READ's best error with memory is no worse than the
  better control's, pooled: $(E_{ctrl} - E_{READ}) / E_{ctrl} \ge -0.01$, with $E$ the minimum over the
  fitted lags. The limit 0.01 is fixed here, before the pilot, and is not taken from it.
- L2, the observer family. L1's pooled condition holds at each cutoff separately ($k_c = 3$, with
  the forcing pairs in the pool, and $k_c = 5$, with them in the consumer).
- N1, convergence. Per viscosity, the pooled advantage changes by at most TOL_N between the two
  resolutions.
- Records. SENS's share, $\tau_{int}$, $L^*$, every $E_L$ and $E^{gle}_L$, the fitted lags, the
  fluctuation–dissipation mismatches and the consumer block's kernel norms.

M1, TOL1 and TOL_N are fixed from the pilot by OP1's rules and limits, written into
`op2_grade.py` before the pilot runs: M1 is half the pilot's pooled advantage, rounded down to
0.005, within $[0.01, 0.10]$; TOL1 is 1.25 times the worst cell shortfall, rounded up to 0.01, within
$[0.05, 0.25]$; TOL_N is 1.5 times the largest change between the resolutions, rounded up to 0.005,
within $[0.01, 0.05]$.

PASS when every bar holds. FAIL when the pooled advantage is at most zero at either cutoff.
INDETERMINATE otherwise, with the missed bar named. A pilot like the probe, where BALL leaves
slightly less memory than READ, would fix M1 at its floor of 0.01, and the run would then need READ
ahead of the better control by at least 1 percent pooled to pass.

## 5. Dependence on OP1

OP2 uses OP1's code for the world, the split, the rankings and TEND, and OP1's trajectories. If
OP1's lift rule (OP1 draft, Section 7) excludes TEND, OP2 is redesigned before its probe, since
its observables assume TEND. OP2 does not wait for OP1's verdict, because the two claims are
distinct. OP1 asks about the Markov forecast and OP2 about the memory that remains.

## 6. Pilot and sealing

Pilot. OP1's pilot worlds and seeds ($\nu \in \{0.03, 0.02\}$ at $n = 96$ and 128, seed 20261112),
read from the trajectories OP1's pilot caches in `experiments/OP/OP1/traj/`, so OP2 adds no
simulation. Each OP2 pilot world starts when OP1's pilot has written that world's trajectory file.
Self-tests at the pilot's code: `op2_mz.py` eight checks (the eighth being the lag cap), and
`op2_grade.py` five, all PASS on Atlas, 2026-10-11.

Sealing. After the pilot, `op2_grade.py --fix-tols` writes `tolerances.json`, this draft takes the
pilot's record and is renamed `PREREG-OP2.md` in one commit, and the observer families go into
`claims/transformations/OP.toml` before that commit. The run uses OP1's run trajectories and the
sealed code. Its grade is whatever the sealed grader prints.
