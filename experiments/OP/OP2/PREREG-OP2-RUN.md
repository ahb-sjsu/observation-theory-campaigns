# PREREG OP2 RUN: the sealed run of OP2, with one declared variant

Status: SEALED 2026-10-18 by the rename of `PREREG-OP2-RUN-DRAFT.md` (drafted 2026-10-14) to
`PREREG-OP2-RUN.md`; blob hash recorded in `experiments/OPEN-PROBLEMS-TRACK.md` and the README status
ledger. The registration of OP2's sealed run, which the owner chose on 2026-10-13
(`experiments/OP/SEALED-RUN-PLAN.md`). OP2 (which modes a reduced model should carry explicitly, so that
the rest needs the least memory) was recorded at its pilot on 2026-10-12, unsealed, with a pilot grade of
FAIL. That record stands as it is, and this run is new evidence beside it. Section 9 lists what was done
before the seal.

## 1. What is incorporated by reference, and what changes

Unchanged, by reference to `PREREG-OP2-DRAFT.md`:
- Sections 1 and 2, the open problem and why the read operator should bear on it;
- Section 3, the design: OP1's world and trajectories; the observables (the consumer's coordinates,
  the $r$ pool pairs a ranking puts first and OP1's TEND observable on them, with a constant); Mori's
  projection and the correlation recursion; the rankings READ, ENERGY, BALL, SENS and RANDOM; the
  quantities per cell; the owner's decisions after the probe (the lag ladder capped by
  `lag_budget_ratio` 4, the fluctuation-dissipation check recorded and not graded);
- Section 4, the graded statistic (the memory share of the consumer block, chosen on the probe by the
  split-half rule), the bars E1, L1, L1E (fixed at $-0.01$ before the pilot), L2 and N1, the verdict
  rule and what falsifies;
- Section 5, the dependence on OP1.

What changes, each fixed before any run and blind to every result of READ on the run seeds:
- The worlds are OP1's run worlds, $n = 128$ and $192$ (`r_nu030_n128`, `r_nu030_n192`,
  `r_nu020_n128`, `r_nu020_n192` in `op2_config.json`), read from the trajectory files OP1's run
  writes. OP2 adds no simulation.
- The seed is the run seed 20261113, OP1's, with the same world offsets.
- The tolerances are the ones OP2's pilot fixed (`experiments/OP/OP2/tolerances.json`, committed at
  d2f087f): M1 = 0.01, TOL1 = 0.25, TOL_N = 0.05. Each sits at a limit of its rule.
- One secondary arm is added, READ-KE (Section 3), with its own test (Section 5). A second was
  declared, ESA, and dropped before the seal (Section 3).
- OP1's regime check removes OP2's worlds too (decided by the owner, 2026-10-14; Section 4).

A graded cell is one (world, $k_c$, $r$), as in the pilot: 4 worlds, 2 cutoffs and 5 budgets, so 40
cells, fewer if a world is removed.

## 2. Primary claim

At matched $r$, the modes READ makes explicit leave a smaller memory share in the consumer block than
the better of ENERGY's and BALL's, by OP2's bars E1, L1, L1E, L2 and N1 with the pilot's tolerances.
The grader is `op2_grade.py`, committed. The verdict rule is the draft's: PASS when every bar holds,
FAIL when the pooled advantage is at most zero at either cutoff, INDETERMINATE otherwise with the missed
bar named. The secondary arm cannot rescue the primary claim.

## 3. Secondary arm (declared before it is probed)

READ-KE, variant V3 of `SEALED-RUN-PLAN.md` Section 3, exactly as in OP1's run registration
(`experiments/OP/OP1/PREREG-OP1-RUN.md` Section 3): OP1's READ with the consumer's response
measured in the kinetic-energy norm, the mask and the amplitude factor unchanged. OP2 imports OP1's
rankings, so READ-KE's order is computed by OP1's code from the same training trajectory, and OP2 builds
its observables on it as it does for every ranking.

ESA, variant V2, was declared for OP2 and dropped from every sealed run by the owner on 2026-10-14
(`SEALED-RUN-PLAN.md` Section 4). It was never computed on OP2's data.

## 4. OP1's regime check and OP2's worlds

`SEALED-RUN-PLAN.md` Section 2 adds a regime check to OP1 (a world whose persistence error differs from
its pair's at the other resolution by more than a factor of 1.5 is reported and not graded) and is
silent on OP2. OP2 reads the same trajectories, so a world in another regime for OP1 is in another
regime for OP2. Decided by the owner on 2026-10-14, before any run (Section 9, item 1): OP2 inherits
the check, read as OP1's run registration Section 4 reads it. A world OP1's check removes is reported
and not graded in OP2 either, and OP2's N1 is not graded at that viscosity, since the check is about
the trajectory, not the gate. The alternative offered, grading every world with the check's outcome
recorded beside, was not taken.
The reading for a world with no partner is OP1's too (OP1 run registration, Section 4, confirmed by the
owner on 2026-10-18): the partner is graded and recorded as unchecked, and N1 is not graded at that
viscosity. A world with no OP2 result is treated the same way in OP2 (`op2_run_grade.py`).
OP2's pilot had no such failure: N1 held, and its worst cell was checked and stood as measured
(`PREREG-OP2-DRAFT.md` Section 6).

## 5. Bar for the secondary arm

READ-KE beats the control only by a one-sided sign test over the graded cells, ties dropped, at level
0.05 with no correction, since OP2 has one secondary arm (`SEALED-RUN-PLAN.md` Section 5). Lower memory
share is better. The control in each cell is the better (lower) of ENERGY's and BALL's shares there, as
in the primary claim (decided by the owner, 2026-10-14, as in OP1). The threshold is the exact binomial on
the untied cells. At 40 untied cells, $p \le 0.05$ needs at least 26 ahead ($p = 0.0403$; 25 gives
0.0769). READ-KE's pooled advantage, its advantage against READ cell by cell and its best error with
memory against the control's (L1E's form) are reported beside the test.

The cells share trajectories: each world's 10 cells come from one training and one test trajectory. The
sign test treats them as independent, so its $p$ is nominal. This is recorded, not corrected.

## 6. What each outcome would mean

- If READ fails OP2's bars and READ-KE does not beat the control, the pilot's finding stands as a sealed
  verdict: the modes READ makes explicit leave less memory than ENERGY's and no less than BALL's, and
  ranking by the read is not the rule for choosing them.
- If READ-KE beats the control under Section 5, that is a positive result about the norm in which the
  read is measured, reported as found by a declared single variant, not as the primary claim.

## 7. Errors and nulls

As in OP2's draft. A world whose trajectory file is missing after OP1's resubmission is reported and not
graded, and the bars that need it are reported as not graded. A singular correlation matrix or a
non-finite share enters the record with its cell and is not graded, and the count of such cells is
reported.

## 8. Platform

Atlas, as in the pilot (`SEALED-RUN-PLAN.md` Section 6): OP2 reads OP1's run trajectory files and runs one
core per world in a screen session. The pilot took about 10 minutes per world once its trajectory file
landed. OP2's observables are pool coordinates, the same physical modes at every resolution, so its cost
does not grow with $n$. No NRP Job is needed.

## 9. Before sealing (each item done and recorded before the rename)

1. The owner settles the open readings: whether OP1's regime check removes OP2's worlds (Section 4),
   and the control for READ-KE's test (Section 5). Done 2026-10-14: the owner accepted the proposed
   readings, now written into Sections 4 and 5. The reading for a world with no partner (Section 4) was
   confirmed by the owner on 2026-10-18.
2. READ-KE reaches OP2 through OP1's rankings (OP1 run registration, Section 9, item 2), and
   `op2_mz.py`'s self-test checks that every ranking OP1 returns, READ-KE included, gets its cells.
   Done 2026-10-14 (da9f80b).
3. READ-KE is probed with OP1's probe (`SEALED-RUN-PLAN.md` Section 4), on the probe trajectory files
   OP1's READ-KE probe rewrites with the kinetic-energy sensitivities (OP1 run registration, Section 9,
   item 3), and recorded. The probe sets nothing.
   Done 2026-10-15 (Atlas; `probe_ke_pr_nu020_n96.json` and `probe_ke_pr_nu030_n96.json` with their
   logs). Every memory share of READ, ENERGY and BALL equals `probe_*.json`'s. In the 20 cells READ-KE's
   memory share is below the better of ENERGY's and BALL's in 7 and above it in 13; READ's is below in
   6 and above in 14; READ-KE against READ is 8 below, 6 above, 6 tied. About 3 minutes per world.
   Recorded; it sets nothing.
4. The run's grader, `op2_run_grade.py`, applies the owner's reading of Section 4 and the sign test of
   Section 5 and calls `op2_grade.py` unchanged. A self-test covers the binomial thresholds and the world
   removal. Any role but the run is labelled "NOT A VERDICT". Done 2026-10-16 (c9d33f9).
5. OP2 runs on the smoke world's trajectory file as part of OP1's smoke run (OP1 run registration,
   Section 9, item 7).
   Done 2026-10-18 on Atlas, on one core (`nice -n 10 timeout 2h op2_mz.py --config op2_config.json
   --seed-role smoke --world s_nu030_n64 --traj-dir ../OP1/traj --read-ke --out smoke.json`), on the
   trajectory file collected from OP1's smoke Job (sha256 beginning 2fb8c153). It exited 0 after 3 min
   40 s, with peak RSS 125 MiB (`smoke.json`, `smoke.log`). Graded by `op2_run_grade.py` with OP1's smoke
   result (`smoke_grade.json`), labelled "SMOKE GRADE, NOT A VERDICT". The regime check is OP1's ("pair
   incomplete: not checked, graded"), and all 10 cells were graded. E1 failed (pooled shares 2.26, 2.08
   and 2.11 for READ, ENERGY and BALL, against 1.75 for random), L1 failed (pooled advantage -0.148, 8 of
   10 cells behind), and L1E and L2 failed. N1 reads `holds: false` with no cells: `op2_grade.py`, called
   unchanged, has no one-resolution note as OP1's grader has, so with one resolution this is N1 not
   gradable, not an N1 failure. READ-KE was below the control in 3 of 10 cells, with 9 needed (one-sided
   p 0.945). As in OP1's smoke run, these grades test the pipeline only.
6. OP2's family and READ-KE's are entered in `claims/transformations/OP.toml`. Done 2026-10-16:
   `OP:mz-explicit-modes` and `OP:mz-read-ke`, with no test rows until the run's verdict.
7. This draft is renamed `PREREG-OP2-RUN.md` in one commit, and its blob hash is recorded in the track
   documents and the README status ledger. Done by this commit.
