# The variant probe: record

Status: RECORD, 2026-10-14. Not claim-bearing. This is the probe of `experiments/OP/SEALED-RUN-PLAN.md`
Section 4, run before the sealed run of D8 and OP4 (`experiments/OD/D8/PREREG-D8-RUN-DRAFT.md`). The
plan lets the probe set one thing, ESA's number of training samples. The variants' standing is
reported here and changes nothing in the sealed run.

## 1. What was run

Worlds and seeds: D8's two pilot worlds at $n = 96$, $\nu = 0.03$ and $\nu = 0.02$ (`p_nu030_n96`,
`p_nu020_n96`), on the pilot seeds, both test trajectories. That is 4 cells, and each cell is paired with
D8's recorded budgets for READ, BALL, ENSTROPHY and KE (`experiments/OD/D8/pilot.json`) and with
OP4's GRAM budget (`experiments/OP/OP4/`).

Arms probed by nudging: READ-KE, GRAM-UN and SV, one NRP Job per (arm, world, trajectory), 12 Jobs.
ESA was not nudged (Section 3). Each arm's ordering was computed once per world from the training
trajectory alone, on Atlas (`op_variants.py --part rank` and `--part gram`, cached in `cache/`), and
the nudging is D8's protocol unchanged (`nudge_record`, the same generator per record as D8's graded
arms, the observer and block tangents carried as in D8's pilot role). Results are in `pieces/`, one
JSON and one log per Job.

## 2. The orderings (training trajectory only)

READ recomputed by the variants code equals D8's recorded READ at all 256 positions on both worlds,
so every arm is compared with the same READ the pilot graded.

| | $\nu = 0.03$ | $\nu = 0.02$ |
|---|---|---|
| leading finite-time Lyapunov exponents | 0.0832, 0.0797, 0.0699, 0.0573, 0.0495, 0.0411, then $-0.0014$ | 0.2478 to 0.0016 (12 positive), then $-0.0054$ |
| $d_u$ (positive exponents) | 6 | 12 |
| $d_{un}$ (exponents above $-0.1\,\lambda_1$) | 9 | 13 |
| subspace $m'$ for GRAM-UN and SV | 24 | 32 |
| window $T_w = 1/\lambda_1$ | 12.0 | 4.0 |
| frac (rule met in every window) | 0.001 | 0.001 |
| pairs for GRAM-UN to reach $d_{un}$ | 3 | 5 |
| rank part, gram part on Atlas (s) | 712, 8717 | 918, 7253 |

Overlap of the top $k$ pairs of each ordering with another's:

| $k$ | READ-KE with READ | GRAM-UN with GRAM | SV with GRAM | SV with READ |
|---|---|---|---|---|
| 8 | 8, 7 | 5, 5 | 2, 0 | 1, 3 |
| 24 | 22, 22 | 20, 21 | 15, 16 | 9, 12 |
| 48 | 44, 46 | 46, 43 | 41, 40 | 33, 42 |
| 96 | 95, 94 | 90, 88 | 88, 86 | 89, 87 |

Each entry is $\nu = 0.03$, then $\nu = 0.02$. GRAM here is OP4's recorded ordering. The sub-block GRAM
the sealed run will use reproduces it at all 256 positions on $\nu = 0.03$, with the same frac and the
same count to $d_u$ (`cache_check/gram_p_nu030_n96_pilot.json`).

## 3. ESA's sample count (the one item the probe sets)

The rule: the smallest number of training samples at which the Spearman correlation of the two
halves' ESA scores over all candidate pairs is at least 0.9. On $\nu = 0.03$, $n = 96$
(`esa_stability.py`, logs `esa_stability_p_nu030_n96.log` and `esa_stability2_p_nu030_n96.log`):

| samples | 80 | 320 | 1280 | 2560 | 5120 |
|---|---|---|---|---|---|
| all-pairs Spearman | 0.373 | 0.728 | 0.878 | 0.886 | 0.890 |
| Spearman over the halves' top-64 union | $-0.199$ | $-0.178$ | 0.225 | 0.032 | 0.788 |
| halves' top 8 shared | 1 | 2 | 2 | 1 | 6 |

The rule was not met and was not changed. The owner dropped ESA from every sealed run (2026-10-14).
The top of the ranking began to settle only at 5120 samples, about 4 hours of one Atlas core at
$n = 96$.

## 4. Budgets

$m^*$ in each cell, on D8's ladder (4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256). The flags read
left to right along the ladder, 1 where the copy stays synchronized.

| cell | READ | BALL | ENSTROPHY | KE | GRAM | READ-KE | GRAM-UN | SV |
|---|---|---|---|---|---|---|---|---|
| $\nu = 0.03$, t0 | 24 | **8** | 48 | 24 | 48 | 48 | 48 | 32 |
| $\nu = 0.03$, t1 | 48 | **8** | 48 | 32 | 48 | 48 | 48 | 32 |
| $\nu = 0.02$, t0 | 16 | **12** | 64 | 24 | 96 | 16 | 96 | 64 |
| $\nu = 0.02$, t1 | 16 | **12** | 48 | 24 | 96 | 16 | 96 | 48 |

| arm | flags, the four cells in order |
|---|---|
| READ-KE | `0000010111111`, `0000010111111`, `0000111111111`, `0000111111111` |
| GRAM-UN | `0000000111111`, `0000000111111`, `0000000001111`, `0000000001111` |
| SV | `0000001111111`, `0000001111111`, `0000000011111`, `0000000111111` |

Margins in ladder steps (positive means the arm needs more):

| arm | against BALL | against READ | against GRAM |
|---|---|---|---|
| READ-KE | +5, +5, +1, +1 | +2, 0, 0, 0 | 0, 0, $-5$, $-5$ |
| GRAM-UN | +5, +5, +6, +6 | +2, 0, +5, +5 | 0, 0, 0, 0 |
| SV | +4, +4, +5, +4 | +1, $-1$, +4, +3 | $-1$, $-1$, $-1$, $-2$ |

BALL is the best graded control in every cell, so the column against BALL is also the column against the
best control.

What the probe shows, stated as observations on 4 cells and not as tests:
- No arm reaches BALL in any cell. The smallest gap is READ-KE's single step on $\nu = 0.02$.
- READ-KE behaves as READ. It is level with READ in 3 cells and 2 steps behind in one. On $\nu = 0.03$ its
  flags are non-monotone in both cells (synchronized at 24, not at 32), the pattern READ shows in t1.
  Its top 48 pairs share 44 and 46 with READ's.
- GRAM-UN behaves as GRAM. Its budget and every flag equal GRAM's in all 4 cells, and its top 48 pairs
  share 46 and 43 with GRAM's, so counting the near-neutral exponents changes the ordering too little
  to move a budget.
- SV is the only arm ahead of GRAM, by one or two steps in every cell, and it is ahead of READ in one
  cell. It stays four or five steps behind BALL.

These observations are on the pilot seeds, the seeds the pilot and OP4 already graded, at $n = 96$ only.
They are the reason the arms are run sealed, and they settle nothing.

## 5. Platform record

All 12 Jobs ran in NRP's exempt class (1 CPU, 2 GiB), each shipping its code and caches pinned by
sha256.
- First submission (01:19 to 01:23 UTC, commit 09d0d27): all 12 Jobs died at container start, "exec
  /bin/bash: argument list too long". The command carried about 200 KB of base64, over Linux's 128 KiB
  limit for one argument. Fixed in 116da28 by gzip before base64 (about 73 KB) and a preflight veto above
  120 KB.
- Second submission (01:25 to 01:29 UTC, 116da28): 3 Jobs failed within one second on node
  `k8s-haosu-23.sdsc.optiputer.net`, their logs jumping from the file checks to the result marker. The
  cause was not found. The 9 on `k8s-haosu-11` ran. The 3 were deleted after checking each had failed
  and resubmitted from the same commit at 01:32 to 01:33. They ran on `cph-dgx-node8.humboldt.edu` and
  `k8s-chase-ci-10.calit2.optiputer.net`.
- Atlas was unreachable from the laptop for part of the night, so the watcher could not save results
  as they landed. Ten were saved by hand from the Job logs at 05:18 UTC, the other two by the watcher.
  No result was lost.

Time per cell (13 rungs with both tangents) was 7686 to 13921 s. The three cells off `k8s-haosu-11`
took 7686, 10840 and 10931 s, and the nine on it took 8484 to 13921 s. D8's pilot ran its core part
at $n = 96$ (the instrument and four graded observers, with the same tangents) in one Job in 15151 to
20096 s, so at most 1.1 to 1.4 hours per observer, and these cells ran two to three times slower. Nine of them shared one node, and the cause was not
investigated. The $n = 192$ timing Job of `PREREG-D8-RUN-DRAFT.md` Section 9 item 4 also runs on
`k8s-haosu-11`, so its time may carry the same slowdown.
