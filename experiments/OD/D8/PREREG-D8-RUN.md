# PREREG D8 RUN: the sealed run of D8 and OP4, with four declared variants

Status: SEALED 2026-10-19 by the rename of `PREREG-D8-RUN-DRAFT.md` (drafted 2026-10-13) to
`PREREG-D8-RUN.md`; blob hash recorded in `experiments/DISCOVERY-TRACK.md`,
`experiments/OPEN-PROBLEMS-TRACK.md` and the README status ledger. The registration of the sealed run that
the owner chose on 2026-10-13 (`experiments/OP/SEALED-RUN-PLAN.md`). D8 (which modes a nudged copy of
forced two-dimensional turbulence must read) and OP4 (D6v3's window-Gramian selector on the same
task) share one run, since they share the worlds, the seeds, the nudging protocol and the controls.
D8 and OP4 were each recorded unsealed, at the pilot and at the confirmation. Those records stand as
they are, and this run is new evidence beside them. Section 9 lists what was done before the seal.

## 1. What is incorporated by reference, and what changes

Unchanged, by reference to `PREREG-D8-DRAFT.md`:
- Section 1, the claim and the background;
- Section 2, the world (forced two-dimensional turbulence, Kolmogorov forcing at $k_f = 4$, drag
  $\alpha = 0.1$, $\nu \in \{0.03, 0.02\}$);
- Section 3, the observers READ, BALL, ENSTROPHY and KE (graded), SENS and RANDOM (recorded), the
  nudging protocol and the synchronization rule;
- Sections 4 to 6, the errors, the bars and what falsifies.

Unchanged, by reference to `experiments/OP/OP4/OP4-DESIGN-DRAFT.md` Sections 2 and 3: GRAM and the
readings "instrument", "both" and "system".

What changes, each fixed before any run and blind to every result of READ:
- The resolutions are the run ladder of D8's draft Section 2, $n = 128$ and $192$ (worlds
  `r_nu030_n128`, `r_nu030_n192`, `r_nu020_n128`, `r_nu020_n192`).
- The seeds are the run seeds, training 20261074 and test 20261075, so no run trajectory was seen by a
  probe or a pilot.
- There are $K = 8$ test trajectories per world, in place of the draft's 4 (owner, 2026-10-13). That
  gives 32 run cells.
- The tolerances are the ones D8's pilot fixed (`experiments/OD/D8/tolerances.json`, committed at
  2390ea0): M1 = 0.5 ladder step, TOL1 = 1 step, TOL_N = 0.5 step.
- GRAM's subspace rule states its cap: $m'$ = the smallest multiple of 8 at least $2 d_u$, at most
  $m_0 = 32$. In the confirmation the cap was 24, not stated, and it bound on one world.
- Three secondary arms are added (Section 3), with the correction for several arms of Section 5. A
  fourth was declared, ESA, and dropped before the seal when its declared stability rule failed
  (Section 3).

## 2. Primary claims (one per gate)

- D8 primary claim: READ synchronizes with a smaller budget than the best of BALL, ENSTROPHY and KE,
  by D8's bars L1 and N1 with the pilot's tolerances. The grader is `d8_grade.py`, committed.
- OP4 primary claim: GRAM is ahead of or level with BALL, pooled in ladder steps over the 32 cells
  ("instrument"). If it is behind BALL, the reading is "both" when GRAM is ahead of READ pooled and
  "system" otherwise. These readings are OP4's, fixed in its draft before its probe.

Neither primary claim can be rescued by a secondary arm.

## 3. Secondary arms (declared before any of them is probed)

The four variants of `SEALED-RUN-PLAN.md` Section 3, as coded in `experiments/OP/VARIANTS/op_variants.py`
(commit 364fa64). Three are sealed arms (READ-KE, GRAM-UN and SV), and ESA is recorded as dropped:
- READ-KE: D8's READ with the response measured in the kinetic-energy norm. Its self-test checks that
  it equals READ in the enstrophy norm.
- ESA: full-covariance sensitivity, $\mathrm{ESA}_k = \|E_t[v_t\,\delta x_{k,t}]\|^2 / \mathrm{Var}(x_k)$ with
  $v_t = N_{w_t}(w_t - \bar w)$. Its self-test checks that it reduces to READ for independent modes.
  DROPPED before the seal (owner, 2026-10-14). `SEALED-RUN-PLAN.md` Section 4 lets the probe set one
  thing, ESA's number of training samples, as the smallest count at which the Spearman correlation of
  the two halves' scores over all candidate pairs is at least 0.9. On the probe world $\nu = 0.03$,
  $n = 96$ (`experiments/OP/VARIANTS/esa_stability.py`, logs `esa_stability_p_nu030_n96.log` and
  `esa_stability2_p_nu030_n96.log`) it was 0.373 at 80 samples, 0.728 at 320, 0.878 at 1280, 0.886 at
  2560 and 0.890 at 5120, gaining about 0.004 per doubling. The rule was not met and was not changed.
  At 5120 the top of the ranking had begun to settle (6 of the halves' top 8 pairs shared, Spearman
  0.788 over the union of their top 64), which is recorded and changes nothing. ESA's ranking was never
  nudged, so no budget of ESA was seen.
- GRAM-UN: GRAM with the required count $d_{un} = \#\{\lambda_i > -0.1\,\lambda_1\}$, the unstable and
  neutral manifold (Trevisan, D'Isidoro and Talagrand 2010).
- SV: singular-vector targeting in the leading tangent subspace (Buizza and Montani 1999).

GRAM itself is computed from the same tangent run as GRAM-UN. Its subspace is the leading $m'_{GRAM}$
directions of GRAM-UN's, and Gram–Schmidt keeps that order, so its blocks are the leading sub-blocks
of GRAM-UN's. This is to be added to `op_variants.py` with a self-test check (Section 9).

## 4. Cells, Jobs and the nudging budget

A cell is one (world, test trajectory). The run has 4 worlds and 8 trajectories, so 32 cells. Each arm's
budget in each cell is $m^*$ by D8's rule, on D8's ladder. Arms in every cell:
- READ, BALL, ENSTROPHY and KE (graded);
- SENS and five RANDOM draws (recorded);
- GRAM (OP4 primary);
- READ-KE, GRAM-UN and SV (secondary).

Rankings and instruments are computed once per world, from that world's training trajectory, by
`op_variants.py --part rank` and `--part gram` and D8's training. They are cached, committed, and carried
into the nudging Jobs.

The run worlds' caches were computed on Atlas from 2026-10-14 to 2026-10-15 and committed on 2026-10-17
(commit 3564ef0, `experiments/OP/VARIANTS/cache/rank_<world>_run.json` and `gram_<world>_run.json`): eight
processes, one per (part, world), run at the same time, each single-threaded (98 to 99% of one core by
`/usr/bin/time -v`), at nice 10, under a thermal guard that would have paused them above 80 C and never did,
and every one exited 0. Wall time and peak RSS:
- rank: `r_nu030_n128` 1.24 h and 334 MiB, `r_nu030_n192` 4.97 h and 629 MiB, `r_nu020_n128` 1.06 h and
  334 MiB, `r_nu020_n192` 6.56 h and 629 MiB;
- gram: `r_nu030_n128` 6.65 h and 166 MiB, `r_nu030_n192` 16.20 h and 331 MiB, `r_nu020_n128` 7.56 h and
  395 MiB, `r_nu020_n192` 21.14 h and 917 MiB.

The Gramian selector's threshold rule was met on every world ($d_u$ = 6, 6, 13 and 12 in the order above).
The gram part at $\nu = 0.02$, $n = 192$ took longer on Atlas than the 20 h bound of a run Job.
The rank caches also hold an ESA ordering, which
`op_variants.py` computes with the others. ESA was dropped before the seal (Section 3), and the run role of
`submit_variants_nrp.py` has no ESA arm, so that ordering travels inside the cache file and is never nudged.

Each Job is one (world, trajectory, arm) in the exempt class on NRP. An arm whose estimated time at
$n = 192$ exceeds 16 hours is split by ladder halves, and its flags are merged before $m^*$ is taken
(tooling, Section 9). As in the pilot, the theorem checks T1 and T2 run on each world's training
trajectory, and the instrument checks of D8's E1 (nothing observed, everything observed) run once per
cell.

## 5. Bars for the secondary arms

A secondary arm beats a control only by a one-sided sign test over the 32 cells, ties dropped, with
Holm's correction across the three secondary arms at a family-wise level of 0.05. The control for this
test is BALL, the best control in every pilot cell. Each arm against READ, and against the best of the
three graded controls per cell, is reported beside it without a test.

At 32 untied cells, Holm's thresholds are 0.0167, 0.025 and 0.05. The first two need at least 23 cells
ahead (one-sided $p = 0.0100$; 22 gives 0.0251), and the third needs at least 22 ($p = 0.0251$; 21 gives
0.0551). With fewer untied cells the thresholds are recomputed from the exact binomial. Margins in
ladder steps are reported for every arm. (Recomputed 2026-10-14 for three arms when ESA was dropped;
with four, the strictest threshold was 0.0125 and needed the same 23.)

## 6. What each outcome would mean

- If READ fails D8's bars and GRAM reads "system", the pilots' findings stand as sealed verdicts.
- A secondary arm that beats BALL under Section 5 is a positive result about choosing what a nudged
  turbulent copy must read. It is reported as found by declared search over four arms, not as a
  primary claim.
- If no secondary arm beats BALL, the "system" reading is tested against the strongest variants the
  literature supplies, and it holds.

## 7. Errors and nulls

As in D8's draft Section 4. A Job that fails or times out is resubmitted once with the same seeds, and
both attempts are recorded. A cell missing an arm after one resubmission is reported and dropped from
that arm's test, with the test's threshold recomputed. A world refused by the stability guard is
reported and not graded.

## 8. Platform and transport

NRP, exempt-class CPU Jobs (1 CPU, 2 GiB), with no sleep, bounded by `timeout`, submitted through
nats-bursting with fresh names, and passing each submitter's preflight. Results travel in the Job log
and are saved the moment each Job succeeds. They also travel over NATS through
`experiments/OD/D8/nats_results.py` into the hub's `OD_RESULTS` stream, so that no result depends on
a node's log (three of D8's pilot logs were lost).

## 9. Before sealing (each item done and recorded before the rename)

1. The variant probe (`SEALED-RUN-PLAN.md` Section 4) completes, and ESA's number of training samples is
   fixed by the declared split-half rule, or the rule's failure is reported to the owner. ESA's part
   done 2026-10-14: the rule failed (0.890 at 5120 samples, Section 3), it was reported, and the owner
   dropped ESA from the sealed arms. The probe's 12 nudging cells for READ-KE, GRAM-UN and SV are
   complete and recorded in `experiments/OP/VARIANTS/PROBE-RECORD.md` (results in `pieces/`). They
   set nothing.
2. GRAM's leading-sub-block computation is added to `op_variants.py`, with a self-test check that it
   equals OP4's GRAM when $m'_{GRAM} = m'_{UN}$. Done 2026-10-14: self-test checks 9 and 10 (commit
   09d0d27), and on the probe world $\nu = 0.03$, $n = 96$ the sub-block GRAM reproduces OP4's recorded
   ordering at all 256 positions, with the same frac (0.001) and count to $d_u$ (2)
   (`experiments/OP/VARIANTS/cache_check/gram_p_nu030_n96_pilot.json`).
3. Ladder-half splitting and flag merging are added and tested (a merged split gives the unsplit $m^*$
   on a small world). Done 2026-10-14: `d8_sync.py` self-test check 14, and `test_ladder_split.py` on
   an $n = 64$ test world, PASS (`ladder_split_test.json`): BALL $m^* = 6$ and READ $m^* = 48$ (flags
   `0001100111111`, non-monotone, the change across the halves' boundary) are equal whole and merged,
   with every delta series and tangent exponent identical.
4. The cost at $n = 192$ is measured, not estimated (added by the owner, 2026-10-14). One run-shaped Job
   (`submit_d8_nrp.py --role timing`: the lower ladder half, 7 of 13 rungs, of READ with the observer
   tangent, on the timing world `t_nu020_n192` with its own seeds) runs on NRP, and its wall time and
   peak memory are recorded. The Job structure of item 3 is confirmed or revised from that measurement.
   Measured 2026-10-14 (`timing_n192_read_h0.json` and `.log`, Job `d8-timing-t-nu020-n192-t0-read-h0` on
   `k8s-haosu-11`, submitted 02:09 UTC, seen succeeded at 10:49): wall 30958 s (8.6 h) on one core (mean 1.00 cores), peak RSS 760 MiB.
   Of that, training (repeated in every Job) took 7263 s (2.0 h) and the 7 rungs of the lower half 23695 s
   (6.6 h, about 0.94 h per rung). The self-test passed in the pod, and the stability guard passed (CFL 0.115,
   at most 0.145 in training). Derived from this one Job, assuming equal cost per rung, not measured: the
   upper half (6 rungs) about 7.7 h, and a graded observer unsplit about 14 h. Both are inside the 20 h
   bound, and the unsplit estimate is under the 16 h at which Section 4 splits an arm. The Job ran on the
   node where the probe's cells ran two to three times slower than D8's pilot (`PROBE-RECORD.md` Section 5),
   so the times may be high. Memory is 37% of the 2 GiB class. Decided by the owner from this measurement
   (2026-10-14): the $n = 192$ graded and variant arms run in ladder halves, as in item 3 and Section 4
   (`halves_min_n` 192 in both submitters).
5. `nats_results.py` is committed, its stream ensured, and a round trip tested from an NRP Job. Done
   2026-10-14: committed in 338dfdc; the `OD_RESULTS` stream (subjects `od.results.>`) created on the
   Atlas hub; `test_nats_roundtrip.py` PASS locally and from the NRP Job `d8-nats-roundtrip`, which sent
   a 2.24 MB seeded payload through the in-cluster leaf in 3 acknowledged chunks; the copy collected on
   Atlas matched both the pod's sha256 and the one computed from the seed (`nats_roundtrip_test.json`).
   Wired 2026-10-14: the run role of `submit_d8_nrp.py` and of `submit_variants_nrp.py` ships
   `nats_results.py` (sha256 asserted) and nats-py 2.14.0, and publishes each result file, bounded by
   `timeout 10m`, to `od.results.d8.run.<Job name>` or `od.results.opv.run.<Job name>` before the log
   block; a failed publish is logged (`NATS-PUBLISH-EXIT`) and does not fail the Job. The preflight refuses a
   run Job without the bounded publish or without `NATS_URL`. Collecting a result from the stream when its log
   is lost is part of the smoke run, item 7.
6. `prereg_config.json` sets $K_{run} = 8$ and the run worlds. `OD:sync-observer` and the OP4 and
   variant families are entered in `claims/transformations/OD.toml` and `OP.toml`. Done 2026-10-14:
   $K_{run} = 8$ in `prereg_config.json` (commit 76808f8, the run worlds were already there);
   `OD:sync-observer` in `OD.toml`, and `OP:gram-observer` and `OP:sync-variants` in a new `OP.toml`,
   with no test rows until the run's verdict.
7. A smoke run of one cell of every arm on a small world through the whole pipeline (submit, save,
   collect, merge, grade). Built 2026-10-14: the smoke world `s_nu030_n64` ($\nu = 0.03$, $n = 64$, its own
   seeds 20261092 and 20261093, $K = 1$) and a `smoke` role in both submitters that is the run role with
   `halves_min_n` lowered to 64, so every graded observer and every variant arm goes through the ladder-half
   split and merge (15 D8 Jobs and 8 variant Jobs). The run's grader for OP4's reading and the secondary arms,
   `d8_run_grade.py`, is added beside `d8_grade.py` (which grades D8's gate and is imported unchanged), with a
   self-test of the sign test and Holm thresholds of Section 5 and of OP4's three readings.
   `smoke_check.py` then checks, for every Job, that the result in its log and the copy in `OD_RESULTS` are
   byte-identical, that D8's collection from the stream alone equals the one from the logs, and that the
   collected files grade, and writes `smoke_record.json`. Done 2026-10-14, PASS (commit 71e0e62): the 15
   D8 Jobs and 8 variant Jobs all succeeded on NRP at the first submission, on 9 or more nodes, in 437 to
   1025 s each (peak RSS of the D8 Jobs about 120 MiB, one core); every one published its result to
   `OD_RESULTS`, and the stream copy equals the log copy byte for byte in all 23; the halves joined with
   $m^*$ on the merged flags, D8's collection from the stream alone (logs disabled) equals the one from the
   logs, and both graders ran. The smoke cell's budgets, which settle nothing (one cell at $n = 64$ on its
   own seeds): BALL 6, KE 12, READ 16, ENSTROPHY 48, SENS and every RANDOM draw censored; GRAM 64,
   READ-KE 12, GRAM-UN 64, SV 48. The graders' labels read "SMOKE GRADE, NOT A VERDICT" throughout. The
   variant Jobs record no footprint (peak RSS), unlike D8's; their $n = 192$ memory rests on D8's
   measurement of the same nudging code (item 4).
8. This draft is renamed `PREREG-D8-RUN.md` in one commit, and its blob hash is recorded in the track
   documents and the README status ledger. Done by this commit.
