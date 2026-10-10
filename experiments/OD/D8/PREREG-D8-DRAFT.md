# PREREG D8 (DRAFT): which modes an observer must read for a two-dimensional flow to be determined by its observation

Status: DRAFT 2026-10-09, not claim-bearing, not sealed. Gate D8 of the OD track
(`experiments/DISCOVERY-TRACK.md`), a new claim registered after the track's declared order was
complete, and not a version of D7. Its theory is `notes/dynamical-read-operator.md` (draft 0.1),
Sections 5 and 6. Its bars and tolerance rules are to be fixed in code (`d8_grade.py`,
`d8_fix_tols.py`) before its pilot runs. Nothing below has been run. Every number marked
"probe" is set by the probe in Section 7 and recorded there before the seal.

D8 makes no claim about Navier–Stokes regularity. It is a two-dimensional problem in which the
answer to "are the discarded directions harmless" is known to be yes for enough observed modes, and
it asks only whether the observer theory chooses those modes better than the classical choices.

## 1. Claim under test

Background. Nudging a second solution toward the observed Fourier modes of a two-dimensional flow
(Azouani, Olson and Titi 2014) makes the two flows synchronize once enough modes are observed.
For the ball of lowest wavenumbers this is the determining-modes theorem (Foias and Prodi 1967),
and the counts the theory guarantees are far above what simulations need. Which modes to observe
for a given count is not settled by that theory. D7v3 (PASS) found that, for a filtered flow at a
single time, the discarded modes of largest read distortion (the resolved dynamics' sensitivity to
a mode times the mode's energy) close the resolved tendency better than the same number of
energy-ranked modes. The theory note's Proposition 4 shows that ranking is optimal for the linear
feedback under independent phases, and its Section 6 shows the dynamical read distortion
$\sigma_k^2\|N_u e_k\|^2$ minimizes the discarded error's nonlinear spreading rate at the first
instant of nudging. Neither statement says anything about synchronization at long times.

Claim. In forced two-dimensional turbulence, an observer that reads the $m$ Fourier modes of
largest dynamical read distortion, ranked on a training trajectory, synchronizes a nudged solution
with the reference on fresh trajectories at a smaller number of observed modes $m^*$ than both
classical observers, the $m$ lowest wavenumbers (BALL) and the $m$ modes of largest energy (ENERGY),
by a declared pooled margin, behind neither in any cell by more than a declared tolerance, with the
advantage the same at two resolutions within a declared tolerance.

## 2. World

Solver. D5's `NS2D` (vorticity form, pseudo-spectral, 2/3 dealiasing, RK4), subclassed in
`d8_sync.py` with Kolmogorov forcing $f_\omega = F_0 k_f \cos(k_f y)$ at $k_f = 4$ and linear drag
$-\alpha\omega$ to stop condensation at the box scale. $F_0 = 1$; $\alpha$ (probe).

Worlds. Two viscosities $\nu_1 > \nu_2$ (probe), each chosen so that the reference flow is chaotic
(largest Lyapunov exponent from `tangent_step` positive on every probe trajectory) and resolved at
the coarser resolution of its ladder (enstrophy spectrum at the dealiasing wavenumber below
$10^{-6}$ of its peak). Resolutions: pilot $n = 64$ and $96$; run $n = 96$ and $128$. Time step
(probe), scaled as $1/n$.

Trajectories. Each trajectory starts from a seeded random vorticity field on $|k| \le 8$, scaled to
a declared enstrophy, and is spun up for $T_{\rm spin}$ (probe) to a statistically stationary
state. Per world: one training trajectory, on which the rankings are computed over a window
$T_{\rm train}$ sampled every $\Delta_s$ (probe); and $K$ test trajectories (pilot $K = 2$, run
$K = 4$) on disjoint seeds, on which synchronization is measured. The same seeded low-mode field is
used at both resolutions of a ladder, so the two resolutions see the same physical initial
condition.

Seeds. Probe 20261071. Pilot training 20261072, pilot test 20261073. Run training 20261074, run
test 20261075. Checked unused in this repository and in geometric-evaluation-theory on
2026-10-09.

## 3. Observers and estimators

Candidates. Every dealiased Fourier mode with $k \neq 0$, one representative per $\pm k$ pair
(observing a pair means reading one complex coefficient). Each observer is a ranking of the
candidates, so its observed sets are nested in $m$.

- READ (the declared arm). Rank by the training-window mean of
  $d_k(t) = |\hat\omega_k(t)|^2 \cdot \tfrac12(\|N_{u(t)} e_k^{\rm re}\|^2 + \|N_{u(t)} e_k^{\rm im}\|^2)$,
  where $N_u$ is the nonlinear part of `tangent_rhs` (the viscous, drag and forcing terms excluded)
  and $e_k^{\rm re}, e_k^{\rm im}$ are the unit real and imaginary perturbations of the pair.
- ENERGY (classical control). Rank by the training-window mean of $|\hat\omega_k(t)|^2$, the
  amplitude factor READ uses and the quantity D7's energy closure ranked by
  (`experiments/OD/D7v3/d7_closure.py:116`), so READ and ENERGY differ by the sensitivity factor
  alone. The kinetic-energy ranking $|\hat\omega_k|^2 / |k|^2$ is computed and recorded (R1), not
  graded.
- BALL (classical control, the Foias–Prodi observer). Rank by $|k|$, ties broken by the angle of
  $k$ and then by index.
- SENS (recorded, not claimed, the analogue of D7's refuted arm). Rank by the training-window mean
  of the sensitivity factor alone.
- RANDOM (null). Five seeded permutations; $m^*$ reported as their median.

Nudging. $v_t = F(v) - \mu P_S(v - u)$ with $v(0) = 0$, $S$ the observer's top $m$ pairs,
$\mu = \mu_0$ (probe, with $\mu_0\,\Delta t \le 1$ for RK4 stability). $\mu_0 / 4$ is run on the pilot
and recorded, not graded.

Synchronization. $\delta(t) = \|\omega_v - \omega_u\| / \|\omega_u\|$. A cell (trajectory,
observer, $m$) is synchronized when $\delta(T_{\rm sync}) \le 10^{-4}$ and the least-squares slope
of $\log\delta$ over the last quarter of $[0, T_{\rm sync}]$ is negative. $T_{\rm sync}$ (probe).
The ladder is $m \in \{4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256\}$. $m^*$ is the smallest
ladder value at which this and every larger ladder value synchronize. A synchronized value below a
non-synchronized one is recorded as a non-monotone cell.

Theorem checks on the solver. At cutoffs $N \in \{4, 8\}$ on every training snapshot,
(a) the central-difference read of the resolved tendency at $q = 0$, which is exact for a quadratic
map up to rounding, on every discarded pair with $|k| > 2N$; (b) the ratio
$\|r_N(p, q)\| / (c_N(2\|p\|\,\|\Pi_{(N,2N]}q\| + \|q\|^2))$ in the velocity norm with the note's
$c_N$.

Estimated cost (to be measured on the probe). Nine rankings (four observers and five random draws)
times 13 ladder values times $K$ test trajectories nudged runs per world, each the length of
$T_{\rm sync}$, batched over $m$ in one array. The platform is decided at launch under the NRP
PREFLIGHT checklist (`C:\Users\abptl\.claude\projects\C--source-agi-hpc\memory\reference_nrp_job_policies.md`)
or on Atlas within its thermal cap. Nothing runs on the laptop.

## 4. Errors and nulls

The quantity graded is $m^*$ per (world, test trajectory, observer). The advantage of READ in a
cell is $a = \log_2(m^*_{\rm best} / m^*_{\rm READ})$, with $m^*_{\rm best} = \min(m^*_{\rm BALL}, m^*_{\rm ENERGY})$,
and the pooled advantage is the mean of $a$ over cells. One ladder step is about 0.5 to 0.6 in
these units. RANDOM is the null: a structured observer that does not beat it is not an observer.
A cell where BALL does not synchronize within the ladder has no $m^*_{\rm best}$ and is out of
scope (bar E2).

## 5. Bars (M1, TOL1 and TOL_N fixed from the pilot by the rules below; `tolerances.json`; Section 7)

- T1 (Proposition 2, exact). On every training snapshot and both cutoffs, the read of every pair
  with $|k| > 2N$ is at most $10^{-10}$ times the largest first-octave read. A miss is an error in
  the note or in the code and stops the gate before any claim is graded.
- T2 (Proposition 3). The ratio at most 1 on every snapshot. The ratio's distribution recorded,
  since it measures how loose the classical bound is.
- E1 (instrument). On every test trajectory, observing every pair synchronizes to
  $\delta(T_{\rm sync}) \le 10^{-10}$, and observing none leaves $\delta(T_{\rm sync}) \ge 0.3$.
- E2 (scope). BALL synchronizes within the ladder on every test trajectory, and every structured
  observer's $m^*$ is below RANDOM's in every cell.
- L1 (the claim). The pooled advantage at least M1, and no cell with $a < -$TOL1.
- N1 (resolution). For each viscosity, the pooled advantages at the run's two resolutions differ by
  at most TOL_N.

Rules. M1 = half the pilot's pooled advantage rounded down to 0.05, and at least 0.25 (half a ladder
step), so a pilot showing no advantage makes L1 a real bar and not an empty one. TOL1 = the pilot's
largest per-cell shortfall rounded up to the next ladder step, and at least one step. TOL_N = 1.5
times the pilot's change between its two resolutions rounded up to 0.05.

Records R1, not graded. SENS's $m^*$ and its advantage. The conditional Lyapunov exponent of the
discarded block $Q_S\,DF(u)\,Q_S$ at $m^*$ and at the ladder value below it, for every structured
observer, and the fraction of cells in which its sign agrees with synchronization (the classical
criterion of the note's Section 6). The overlap of READ's and ENERGY's top-$m$ sets at $m^*$, and the
shell histogram of READ's modes. Non-monotone cells. The $\mu_0/4$ pilot run. The initial spreading
rate of the note's Section 6 for each observer at each $m$, to see whether the instant the
proposition covers predicts the long-time result.

Pass: T1, T2, E1, E2, L1, N1. Fail: T1 (the gate stops and the note is corrected first), or the
pooled advantage below $-0.25$ (READ behind the better classical observer by half a ladder step),
or more than a quarter of in-scope cells with $a < -$TOL1. Otherwise INDETERMINATE.

## 6. What falsifies

An ENERGY or BALL observer that synchronizes at the same count as READ says the read distortion
adds nothing to the classical choices once the problem is dynamical, and D7v3's result is a
property of the single-time closure only. A READ advantage that SENS reproduces equally says the
energy factor is not needed in the dynamical problem (recorded, and a revision would change the
claim). An advantage that changes with resolution beyond TOL_N says it belongs to the grid and not
the flow. A T1 miss says Proposition 2 is false as stated or the solver is not the system the
note describes.

Anti-circularity (track Section 3). The rankings are computed on training trajectories with seeds
disjoint from the test trajectories. Both classical controls are computed beside READ, and the claim
is graded against the better of the two in each cell. The observer family is declared in
`claims/transformations/OD.toml` as `OD:sync-observer` before the seal.

## 7. Self-test, probe, pilot (before sealing)

Not yet run. Files to write: `d8_sync.py` (forced solver subclass, the four rankings, batched
nudging, theorem checks, `--selftest`), `d8_grade.py`, `d8_fix_tols.py`, `prereg_config.json`,
`d8_launch.sh`.

Self-test, to pass before the probe. The forcing balance at a fixed point of the laminar
Kolmogorov flow; the central-difference read equal to `tangent_rhs`'s nonlinear part on random
fields; T1 on random fields at $n = 32$; nudging with every mode observed contracting at rate
$\mu$; nudging with nothing observed leaving $\delta$ unchanged at $t = 0$.

Probe (seed 20261071). Fixes $\alpha$, $\nu_1$, $\nu_2$, $\Delta t$, $T_{\rm spin}$, $T_{\rm train}$,
$\Delta_s$, $\mu_0$ and $T_{\rm sync}$, records the Lyapunov exponents, the spectra at the
dealiasing wavenumber, whether $\delta$ is bimodal at $T_{\rm sync}$ (so that the $10^{-4}$ threshold
separates synchronized from unsynchronized cells), and the measured cost per nudged run.

Pilot (training 20261072, test 20261073, $n = 64$ and $96$, $K = 2$). Fixes M1, TOL1 and TOL_N by the
rules of Section 5 and records the pilot's own grade.

## 8. Sealing procedure

1. Write the code and pass the self-test. Probe on Atlas or NRP, record Section 7, commit
   `probe.json`. Pilot, fix the tolerances, record them, commit `pilot.json` and `tolerances.json`.
2. Declare `OD:sync-observer` in `claims/transformations/OD.toml`. Verify the references in the
   theory note against Crossref. Rename this file to `PREREG-D8.md`, commit, record its blob hash
   in the track document and the README status ledger.
3. Run on the run seeds, grade with `d8_grade.py results.json --tols tolerances.json`, commit
   `results.json` and `grade.json` as executed, enter the registry test.
