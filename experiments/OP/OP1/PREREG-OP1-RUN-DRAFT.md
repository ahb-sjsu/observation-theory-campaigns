# PREREG OP1 RUN (DRAFT): the sealed run of OP1, with one declared variant

Status: DRAFT, 2026-10-14. Not sealed and not claim-bearing. The registration of OP1's sealed run, which
the owner chose on 2026-10-13 (`experiments/OP/SEALED-RUN-PLAN.md`). OP1 (on which coordinates a
consumer's Koopman dictionary should be built) was recorded at its pilot on 2026-10-12, unsealed, with a
pilot grade of FAIL. That record stands as it is, and this run is new evidence beside it. Section 9 lists
what must be done before this draft is renamed `PREREG-OP1-RUN.md` and sealed.

## 1. What is incorporated by reference, and what changes

Unchanged, by reference to `PREREG-OP1-DRAFT.md`:
- Section 1, the claim and the background;
- Section 2, the world (D8's forced two-dimensional turbulence, $\nu \in \{0.03, 0.02\}$, consumer
  cutoffs $k_c \in \{3, 5\}$, pool $k_c < |k| \le 12$, one training and one test trajectory per world);
- Section 3, the rankings READ (claim), ENERGY and BALL (graded controls), SENS (recorded) and RANDOM
  (null), the references POD, GREEDY, NONE and PERSIST, the lifts, the ridge $10^{-6}$, the horizons
  $\{1, 2, 4\}$ samples, the error and the ladder $r \in \{2, 4, 8, 16, 32\}$;
- Section 4, errors and nulls;
- Sections 5 and 6, the bars E1, L1, L2 and N1, the verdict rule and what falsifies;
- Section 7's owner decisions: graded lifts RFF and TEND, LIN recorded and not graded.

What changes, each fixed before any run and blind to every result of READ on the run seeds:
- The worlds are the run ladder of OP1's draft Section 2, $n = 128$ and $192$ (worlds `r_nu030_n128`,
  `r_nu030_n192`, `r_nu020_n128`, `r_nu020_n192` in `prereg_config.json`).
- The seed is the run seed 20261113, with the run worlds' offsets (21 at $\nu = 0.03$, 22 at
  $\nu = 0.02$), so no run trajectory was seen by the probe or the pilot.
- The tolerances are the ones OP1's pilot fixed (`experiments/OP/OP1/tolerances.json`, committed at
  321cb46): M1 = 0.01, TOL1 = 0.25, TOL_N = 0.05. Each sits at a limit of its rule.
- A regime check on every world (Section 4), from `SEALED-RUN-PLAN.md` Section 2.
- One secondary arm is added, READ-KE (Section 3), with its own test (Section 5). A second was
  declared, ESA, and dropped before the seal (Section 3).

A graded cell is one (world, $k_c$, graded lift, $r$), as in the pilot: 4 worlds, 2 cutoffs, 2 lifts
and 5 budgets, so 80 cells, fewer if the regime check removes a world.

## 2. Primary claim

READ's pooled advantage over the better of ENERGY and BALL, cell by cell, meets OP1's bars E1, L1, L2
and N1 with the pilot's tolerances. The grader is `op1_grade.py`, committed, with the regime check of
Section 4 applied before it. The verdict rule is the draft's: PASS when every bar holds, FAIL when the
pooled advantage is at most zero in either graded lift, INDETERMINATE otherwise with the missed bar
named. The secondary arm cannot rescue the primary claim.

## 3. Secondary arm (declared before it is probed)

READ-KE, variant V3 of `SEALED-RUN-PLAN.md` Section 3. It keeps OP1's READ exactly, its amplitude factor
$|w_k - \bar w_k|^2$, its averaging over the sensitivity times and the consumer's mask $P_C$, and changes
only the norm in which the consumer's response is measured, from the enstrophy norm (vorticity) to the
kinetic-energy norm:
$$\mathrm{READ\text{-}KE}_k = E_t\big[s^{\mathrm{KE}}_k(t)\,|w_k(t) - \bar w_k|^2\big], \qquad
s^{\mathrm{KE}}_k = \tfrac12\big(\|P_C N_w e_{re}\|^2_{\mathrm{KE}} + \|P_C N_w e_{im}\|^2_{\mathrm{KE}}\big).$$
With the enstrophy norm in place of the kinetic-energy norm, READ-KE equals READ, and that reduction is
a self-test check (Section 9). It is not a ranking by the mode's own kinetic energy. OP1's ENERGY
ranks by the mode's own vorticity variance and has no read.

ESA, variant V2, was declared for OP1 and dropped from every sealed run by the owner on 2026-10-14,
when its declared stability rule failed on D8's probe world (`SEALED-RUN-PLAN.md` Section 4). It was
never computed on OP1's data.

## 4. The regime check

From `SEALED-RUN-PLAN.md` Section 2, fixed there before any run from one case (the pilot's
$\nu = 0.03$, $n = 128$ world, persistence error 0.177 against 0.351 at $n = 96$). It looks only at
the persistence forecast, never at a ranking.

The plan's sentence is: a world whose persistence error differs from its pair's at the other
resolution by more than a factor of 1.5 is reported and not graded. It left three readings open, and
the owner decided them on 2026-10-14, before any run (Section 9, item 1):
- The quantity: PERSIST's graded value $E$ (the mean over the horizons of $\min(e_h, 2)$), averaged
  over the two cutoffs, one number per world. The check fails at a viscosity when the larger of its two
  worlds' numbers exceeds 1.5 times the smaller.
- Which world is removed: both worlds of that viscosity are reported and not graded. The ratio is
  symmetric, and nothing in the check says which of the two is the odd one.
- What it does to N1: N1 is not graded at a viscosity whose pair failed the check. If both viscosities
  fail, OP1 is reported as unable to test its claim on the run worlds.

## 5. Bar for the secondary arm

READ-KE beats the control only by a one-sided sign test over the graded cells, ties dropped, at level
0.05 with no correction, since OP1 has one secondary arm (`SEALED-RUN-PLAN.md` Section 5). The control
in each cell is the better of ENERGY and BALL there, as in the primary claim (decided by the owner,
2026-10-14; the plan says "a control" and names none for OP1). A cell where READ-KE ties the control
is dropped from the count, and the threshold is the exact binomial on the untied cells. At 80 untied
cells, $p \le 0.05$ needs at least 48 ahead ($p = 0.0465$; 47 gives 0.0728). READ-KE's pooled advantage,
and its advantage against READ cell by cell, are reported beside the test.

The cells share trajectories: each world's 20 cells come from one training and one test trajectory. The
sign test treats them as independent, so its $p$ is nominal. This is recorded, not corrected.

## 6. What each outcome would mean

- If READ fails OP1's bars and READ-KE does not beat the control, the pilot's finding stands as a sealed
  verdict: ranking by the consumer's read does not choose a Koopman dictionary better than energy or
  scale in this world.
- If READ-KE beats the control under Section 5, that is a positive result about the norm in which the
  read is measured, reported as found by a declared single variant, not as the primary claim.

## 7. Errors and nulls

As in OP1's draft Section 4. A Job that fails or times out is resubmitted once with the same seed, and
both attempts are recorded. A world missing after one resubmission is reported and not graded, and the
bars that need it (N1 at that viscosity) are reported as not graded. A world refused by the stability
guard is reported and not graded.

## 8. Platform and transport

Each run world is one Job on NRP (`SEALED-RUN-PLAN.md` Section 6), in the exempt class (1 CPU, 2 GiB),
with no sleep, bounded by `timeout`, submitted through nats-bursting with a fresh name, and passing the
submitter's preflight on a measured footprint. The result and the world's trajectory file
(`traj/`, which OP2 reads) travel in the Job log and over NATS through
`experiments/OD/D8/nats_results.py` into `OD_RESULTS`. The pilot ran each world on one Atlas core in
about 4.5 to 5.5 hours, the $n = 128$ worlds longest (OP1's draft Section 7), and recorded no peak
memory. The time and memory at $n = 192$ are not measured (Section 9, item 4).

## 9. Before sealing (each item done and recorded before the rename)

1. The owner settles the open readings: the regime check's quantity, which world it removes and its
   effect on N1 (Section 4), and the control for READ-KE's test (Section 5). Done 2026-10-14: the owner
   accepted the proposed readings, now written into Sections 4 and 5.
2. READ-KE is added to `op1_edmd.py`'s rankings, with a self-test check that it equals READ in the
   enstrophy norm, and a check that its kinetic-energy sensitivity equals a central difference of the
   consumer's tendency measured in that norm.
3. READ-KE is probed on OP1's probe worlds and seeds (`SEALED-RUN-PLAN.md` Section 4) and recorded.
   The probe sets nothing. The cached probe trajectories cannot serve alone: they hold only the pairs
   $|k| \le 12$ and the enstrophy-norm sensitivities, and the kinetic-energy sensitivity needs the
   whole field. So each probe world is simulated again (`op1_edmd.py --read-ke`), and the new record
   must equal the cached one exactly before it is used (corrected 2026-10-14).
4. The cost at $n = 192$ is measured, not estimated: one run-shaped Job on a timing world with its own
   seeds, recording wall time and peak memory. Its result fixes the Job bound, and whether a world
   must be split (for example the simulation and the scoring as separate Jobs), before any run Job.
5. A submitter for OP1's run (`submit_op1_nrp.py`) with the preflight of D8's: exempt class, a
   measured footprint, the bounded NATS publish of the result and of the trajectory file, a dirty-tree
   check, and the dry run.
6. The run's grader, `op1_run_grade.py`, applies the regime check and the sign test of Section 5 and
   calls `op1_grade.py` unchanged. A self-test covers the check's three readings and the binomial
   thresholds. Any role but the run is labelled "NOT A VERDICT".
7. A smoke run of one small world through the whole pipeline (submit, save, collect from the stream,
   grade), on its own seeds, followed by OP2's run on that world's trajectory file.
8. OP1's family and READ-KE's are entered in `claims/transformations/OP.toml`.
9. This draft is renamed `PREREG-OP1-RUN.md` in one commit, and its blob hash is recorded in the track
   documents and the README status ledger.
