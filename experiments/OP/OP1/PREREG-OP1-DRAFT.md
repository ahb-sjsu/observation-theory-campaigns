# PREREG OP1 (DRAFT): on which coordinates a consumer's Koopman dictionary should be built

Status: DRAFT, not sealed, not claim-bearing. Gate OP1 of the OP track
(`experiments/OPEN-PROBLEMS-TRACK.md`). Bars are fixed in code (`op1_grade.py`, `op1_fix_tols.py`,
to be written before the pilot) and their tolerances from the pilot by the rules of Section 5.
Section 7 records the self-test, the smoke run and the probe.

## 1. Claim under test

A consumer reads the large scales of a forced two-dimensional flow, the Fourier pairs with
$|k| \le k_c$, and forecasts them with extended dynamic mode decomposition (EDMD). Its dictionary
holds its own coordinates and the coordinates of $r$ further pairs drawn from a pool. The claim is
that ranking the pool by read distortion for the consumer (READ) gives a lower multi-step forecast
error than ranking it by energy (ENERGY) or by scale (BALL), at matched $r$, under a linear and
under a nonlinear lift, and that the advantage is stable in resolution.

Why READ. The consumer's increment over one sample is, to first order, the sample time times its
tendency $T_C(w)$. Around the training mean, pair $k$ contributes $J_k (x_k - \bar x_k)$ to it, with
$J_k$ the derivative of $T_C$ along the pair. Under random phases the variance this adds is
$|J_k|^2 \mathrm{Var}(x_k)$, which is READ (theory note, Proposition 4). So READ orders the pool by
each pair's first-order share of the consumer's next increment. ENERGY keeps the factor
$\mathrm{Var}(x_k)$ and drops the read. BALL keeps neither and orders by scale. The open part is
whether a first-order, one-step argument survives a nonlinear lift and forecasts iterated over
many samples, which is what EDMD is for.

Background. Choosing the dictionary is one of the most significant open problems of EDMD
(Colbrook, arXiv:2312.00137). Learned dictionaries (Li et al., arXiv:1707.00225), sparsity-promoting
selection of Koopman-invariant subspaces (Pan, Arnold and Duraisamy, J. Fluid Mech.) and residual
checks of a dictionary (Colbrook and Townsend, arXiv:2205.09779) choose observables by fit to
data. Peitz et al. (arXiv:2307.15325) treat Koopman models from partial observations and note that
EDMD need not approximate the Koopman operator when observables are chosen carelessly. A search on
2026-10-11 found no selection of observables by the consumer's sensitivity. The nearest results in
this repository point both ways. D7v3 (PASS) found read distortion ahead of energy for a closure of
the same kind of flow. D8's pilot finds it behind the best simple control for synchronizing a nudged
copy.

## 2. World

D8's forced two-dimensional turbulence, imported from `experiments/OD/D8/d8_sync.py`, not copied:
vorticity form, pseudo-spectral, 2/3 dealiasing, RK4, Kolmogorov forcing $F_0 k_f \cos(k_f y)$ with
$k_f = 4$, $F_0 = 1$, linear drag $\alpha = 0.1$, the explicit-RK4 stability guard. Viscosities
$\nu \in \{0.03, 0.02\}$, the two worlds D8's probe found chaotic and resolved at $n = 96$
(Lyapunov exponents $+0.06$ and $+0.26$). Time step $0.005 \cdot 64 / n$.

Per world, one training and one independent test trajectory, each from its own seeded initial field
spun up for $T_{spin} = 100$. Training length $T_{train} = 1000$, test length $T_{test} = 400$,
sampled every $0.5$. Consumer sensitivities every $10$ time units of the training run.

Consumer cutoffs $k_c \in \{3, 5\}$. At $k_c = 3$ the forcing pairs lie in the pool. At $k_c = 5$
they belong to the consumer. Pool: the pairs with $k_c < |k| \le 12$, the same physical modes at every
resolution, so a change of $n$ changes the simulation and not the question.

Resolution ladder: probe $n = 96$; pilot $n = 96$ and $128$; run $n = 128$ and $192$, as in D8.
Seeds: probe 20261111, pilot 20261112, run 20261113, with per-world offsets in
`prereg_config.json`.

## 3. Rankings, dictionaries and the error

Rankings of the pool, all computed on the training trajectory.

| Name | Definition | Role |
|---|---|---|
| READ | $E_t[s_k(t)\,|w_k(t) - \bar w_k|^2]$, with $s_k = (|P_C N_w e_{re}|^2 + |P_C N_w e_{im}|^2)/2$ the sensitivity of the consumer's tendency to a unit perturbation of pair $k$ | claim |
| ENERGY | training variance of $w_k$ | graded control |
| BALL | $|k|$ ascending, ties by index | graded control |
| SENS | $E_t[s_k]$ | recorded |
| RANDOM | 6 seeded permutations, median error | null |

References, recorded and not graded: POD (the leading $2r$ principal components of the pool's
training coordinates, the same real dimension in another basis); GREEDY (forward selection of pairs
on a validation split of the training record, 75 percent fit and 25 percent scored, linear lift
only, the data-fitted selector); NONE (the consumer's coordinates alone); PERSIST (the forecast
$\hat p(t+h) = p(t)$).

Dictionary. $z$ is the standardized vector of the consumer's coordinates and the selected
coordinates (real and imaginary parts, training mean and deviation). Lift LIN is $[1, z]$, DMD with
augmentation. Lift RFF is $[1, z, \sqrt{2/D}\cos(zW + b)]$ with $D = 256$ random Fourier features of
a Gaussian kernel of length scale $\sqrt{\dim z}$, $W$ and $b$ seeded by $\dim z$, so every ranking
at the same $r$ sees the same draw. $K$ is fitted by ridge regression of $\psi(t+1)$ on $\psi(t)$,
with the ridge $10^{-6}\,\mathrm{tr}(G)/\dim\psi$ (PENDING the probe).

Forecast and error. From $\psi$ at each test start (every second sample), $K$ is iterated without
re-lifting, and the consumer's coordinates are read off the iterate. At horizon $h$ the error is
$e_h = (\sum |\hat p - p|^2 / \sum |p - \bar p|^2)^{1/2}$ over the starts, in math units, with
$\bar p$ the training mean. Zero is exact and one is the climatology. A cell's value is
$E = \mathrm{mean}_h \min(e_h, 2)$ over the declared horizons, $h \in \{1, 4, 16\}$ samples
(PENDING the probe). The ladder of $r$ is $\{2, 4, 8, 16, 32\}$.

A graded cell is one (world, $k_c$, lift, $r$). Per cell, the advantage of READ is
$a = (E_{ctrl} - E_{READ}) / E_{ctrl}$ with $E_{ctrl} = \min(E_{ENERGY}, E_{BALL})$, the better
control in that cell.

## 4. Errors, nulls and the outcome of every case

A diverged forecast (a non-finite error) enters at the cap and is counted in the record. A world
refused by the stability guard is reported and not graded. If READ and a control choose the same
pairs at some $r$, the cell's advantage is zero by construction. The overlap of READ's top $r$ with
each control's is recorded for every cell, so a tie can be read as agreement rather than as a
measured equality.

## 5. Bars (numbers PENDING the pilot)

- E1, the instrument. Pooled over cells, each of READ, ENERGY and BALL below the RANDOM median; and
  the best of them at the top of the ladder below NONE, so that adding coordinates helps at all.
- L1, the claim. The pooled advantage of READ at least M1, and no cell's advantage below $-$TOL1.
- L2, the observer family. L1's pooled condition holds in each lift separately.
- N1, convergence. The pooled advantage changes by at most TOL_N between the two resolutions.
- Records. GREEDY, POD, SENS, PERSIST and NONE errors; overlaps; spectral radii of $K$; divergence
  counts; per-horizon errors.

M1, TOL1 and TOL_N are fixed from the pilot by rules written into `op1_fix_tols.py` before the
pilot runs, within limits fixed in this draft before the probe ends (to be written).

PASS when every bar holds. FAIL when the pooled advantage of READ is at most zero in either lift.
INDETERMINATE otherwise, with the missed bar named.

## 6. What falsifies

READ no better than the better of ENERGY and BALL, pooled, in either lift. A margin that holds at
$n = 128$ and not at $n = 192$. A result that only the linear lift shows is not the claim.

## 7. Self-test, smoke run and probe

Self-test (`op1_edmd.py --selftest`, Atlas, 2026-10-11), nine checks, all PASS:
- A synthetic consumer driven by a quiet rotating pair it reads, beside a pair of noise forty times
  louder that it does not read. READ ranks the read pair first and ENERGY the loud one. The
  dictionary with the read pair forecasts exactly at every horizon ($E = 4.6 \times 10^{-9}$), and
  the loud pair gains nothing over the consumer alone (0.805 against 0.804). Greedy picks the read
  pair.
- Linear EDMD forecasts a linear system exactly ($1.9 \times 10^{-12}$).
- The error scale is 0 for the truth and 1 for the climatology.
- Random Fourier features are deterministic per dimension and approximate the Gaussian kernel
  (0.306 against 0.313 at $D = 4096$).
- On the flow, the consumer sensitivity equals the central difference of the consumer's tendency
  ($2.0 \times 10^{-13}$ relative to the largest). A first version of this check divided by each
  pair's own sensitivity and failed on a pair the consumer cannot read
  ($10^{-37}$ against rounding of $3 \times 10^{-31}$). The check was changed to the honest scale,
  not the code.
- The split partitions the pairs, the coordinates read back the field, the rankings are
  permutations, and the NONE and POD dictionaries have the declared dimensions.

Smoke run (Atlas, $\nu = 0.03$, $n = 48$, $T_{train} = 80$, pool $|k| \le 8$, $r \in \{2, 4\}$). Every
path ran. It showed three things that changed the code before the probe. numpy's BLAS ran about 16
threads unasked (142 CPU-minutes in 9 wall-minutes), so every run now pins one thread. Greedy on
the RFF lift dominated the cost, so greedy runs on the linear lift only. And every arm's error was
above the climatology even at one step, with 160 training samples against up to 93 features and a
ridge of $10^{-6}$. The smoke run is too short to say whether that is overfitting or a
non-stationary record, so the probe saves its trajectories and the ridge and the horizons are
fixed on the probe before the pilot. A persistence forecast was added as a recorded baseline.

Probe (Atlas, screen sessions `op1-pr_nu020_n96` and `op1-pr_nu030_n96`, started 2026-10-11, one
core each, trajectories cached in `traj/`). Probe round 1, the $\nu = 0.03$ world (training and test
spectrum tails $1.4 \times 10^{-9}$ and $2.7 \times 10^{-10}$, resolved).

What round 1 showed, per horizon. Under the linear lift, adding pool coordinates changes nothing.
The consumer alone forecasts at 0.154 at one step ($k_c = 3$) and the best arm at $r = 32$ at 0.149.
Even GREEDY, which is fitted on the training data, gains nothing. The reason is structural. The
consumer's tendency is a sum of products of pairs, and a dictionary linear in the coordinates
cannot represent a product, so no choice of linear coordinates can carry it. RFF is worse than the
consumer alone at every horizon (0.22 to 0.29 at one step), since 256 random features of a kernel
in 28 to 104 dimensions overfit 2000 samples. At $h = 16$ (8 time units) every arm is at or above
the climatology, so that horizon carries no information about the choice. The persistence forecast
is 0.17 at one step, so EDMD beats it only narrowly.

Change registered before round 2 is run (2026-10-11). A third lift, TEND, adds one vector
observable to the linear dictionary, the consumer's tendency evaluated on the consumer's and the
selected pairs alone, $T_C(P_{C \cup S} w)$, computed exactly from the coordinates on an alias-free
grid. It is D7's closure object placed inside a Koopman dictionary. It holds every triad among the
chosen pairs in the combination the equation uses, at the cost of $2 n_c$ extra columns. The
horizons become $h \in \{1, 2, 4\}$ samples (0.5, 1 and 2 time units).

Rule for which lifts are graded, fixed before round 2 and blind to READ. A lift is graded only if
augmentation can help under it at all. That means the best error over every arm computed under the
lift (READ, ENERGY, BALL, SENS, the RANDOM draws, POD and GREEDY where run), at the top of the
ladder, pooled over the probe's worlds and cutoffs, is at least 5 percent below the consumer alone
(NONE). A lift that fails the rule is reported and not graded, because a choice of coordinates
cannot be tested where no coordinates help. READ's standing against the controls plays no part in
the rule. If no lift passes it, OP1 is reported as unable to test its claim in this world.

## 8. Sealing procedure

After the pilot: `op1_fix_tols.py` writes `tolerances.json`; this draft is completed with the
pilot's record and renamed `PREREG-OP1.md` in one commit, whose blob hash goes into the track
document and the README status ledger; the observer families go into `claims/transformations/OP.toml`
before that commit. The run uses the run seeds and the sealed code, and its grade is whatever the
sealed grader prints.
