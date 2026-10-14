# PREREG D8 RUN (DRAFT): the sealed run of D8 and OP4, with four declared variants

Status: DRAFT, 2026-10-13. Not sealed and not claim-bearing. The registration of the sealed run that
the owner chose on 2026-10-13 (`experiments/OP/SEALED-RUN-PLAN.md`). D8 (which modes a nudged copy of
forced two-dimensional turbulence must read) and OP4 (D6v3's window-Gramian selector on the same
task) share one run, since they share the worlds, the seeds, the nudging protocol and the controls.
D8 and OP4 were each recorded unsealed, at the pilot and at the confirmation. Those records stand as
they are, and this run is new evidence beside them. Section 9 lists what must be done before this
draft is renamed `PREREG-D8-RUN.md` and sealed.

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
- Four secondary arms are added (Section 3), with the correction for several arms of Section 5.

## 2. Primary claims (one per gate)

- D8 primary claim: READ synchronizes with a smaller budget than the best of BALL, ENSTROPHY and KE,
  by D8's bars L1 and N1 with the pilot's tolerances. The grader is `d8_grade.py`, committed.
- OP4 primary claim: GRAM is ahead of or level with BALL, pooled in ladder steps over the 32 cells
  ("instrument"). If it is behind BALL, the reading is "both" when GRAM is ahead of READ pooled and
  "system" otherwise. These readings are OP4's, fixed in its draft before its probe.

Neither primary claim can be rescued by a secondary arm.

## 3. Secondary arms (declared before any of them is probed)

The four variants of `SEALED-RUN-PLAN.md` Section 3, as coded in `experiments/OP/VARIANTS/op_variants.py`
(commit 364fa64):
- READ-KE: D8's READ with the response measured in the kinetic-energy norm. Its self-test checks that
  it equals READ in the enstrophy norm.
- ESA: full-covariance sensitivity, $\mathrm{ESA}_k = \|E_t[v_t\,\delta x_{k,t}]\|^2 / \mathrm{Var}(x_k)$ with
  $v_t = N_{w_t}(w_t - \bar w)$. Its self-test checks that it reduces to READ for independent modes. The
  number of training samples is PENDING (Section 9).
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
- READ-KE, ESA, GRAM-UN and SV (secondary).

Rankings and instruments are computed once per world, from that world's training trajectory, by
`op_variants.py --part rank` and `--part gram` and D8's training. They are cached, committed, and carried
into the nudging Jobs.

Each Job is one (world, trajectory, arm) in the exempt class on NRP. An arm whose estimated time at
$n = 192$ exceeds 16 hours is split by ladder halves, and its flags are merged before $m^*$ is taken
(tooling, Section 9). As in the pilot, the theorem checks T1 and T2 run on each world's training
trajectory, and the instrument checks of D8's E1 (nothing observed, everything observed) run once per
cell.

## 5. Bars for the secondary arms

A secondary arm beats a control only by a one-sided sign test over the 32 cells, ties dropped, with
Holm's correction across the four secondary arms at a family-wise level of 0.05. The control for this
test is BALL, the best control in every pilot cell. Each arm against READ, and against the best of the
three graded controls per cell, is reported beside it without a test.

At 32 untied cells, the strictest Holm threshold (0.0125) needs at least 23 cells ahead (one-sided
$p = 0.0100$), and the loosest (0.05) needs at least 22 ($p = 0.0251$). With fewer untied cells the
threshold is recomputed from the exact binomial. Margins in ladder steps are reported for every arm.

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
   fixed by the declared split-half rule, or the rule's failure is reported to the owner.
2. GRAM's leading-sub-block computation is added to `op_variants.py`, with a self-test check that it
   equals OP4's GRAM when $m'_{GRAM} = m'_{UN}$.
3. Ladder-half splitting and flag merging are added and tested (a merged split gives the unsplit $m^*$
   on a small world).
4. `nats_results.py` is committed, its stream ensured, and a round trip tested from an NRP Job.
5. `prereg_config.json` sets $K_{run} = 8$ and the run worlds. `OD:sync-observer` and the OP4 and
   variant families are entered in `claims/transformations/OD.toml` and `OP.toml`.
6. A smoke run of one cell of every arm on a small world through the whole pipeline (submit, save,
   collect, merge, grade).
7. This draft is renamed `PREREG-D8-RUN.md` in one commit, and its blob hash is recorded in the track
   documents and the README status ledger.
