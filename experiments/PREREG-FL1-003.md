# PREREG-FL1-003 — FL-1, second successor: the two-hop law at 512 and 1,024 routers, deployment limit fixed

**Status:** SEALED (sealing commit and SHA-256 in `SEALS.md`), "Authorized by: A. H. Bond (session instruction)".
Successor to `PREREG-FL1-002` (sealed at 62c255d), which is VOID: its setup gates
passed, but both discriminating cells failed at deployment (`analysis/flooding/fl1-002/`, 24753bd). FL1-002 was
itself the successor of `PREREG-FL1-001`, VOID without data. Both stay sealed and unedited. This registration names
what it repairs.

## Why a second successor

FL1-002 ran on Atlas on 2026-11-22/23, in KVM guests under FRR's default timers. Its gap-step checks passed, and so
did its setup gates: the two 256-router calibration graphs came within 2.5 points of their calibration savings. The
512-router cells of degree 8 and 16 then failed before their first run.

The lab harness loads each router's configuration in turn (`vtysh -b`), with a 120 s limit. The routers configured
before it are already flooding, and at routers r507 (degree 8) and r359 (degree 16) the load took longer than the
limit. That is a limit of the harness, unrelated to the saving under test. By FL1-002's stopping rule the 1,024-router
cells did not run, and the law was not tested.

## What changes from FL1-002, and why

1. **The harness: topology-builders at 69220fe instead of FL1-001's tree.** The package differs from FL1-001's tree
   (`/tmp/tb-gap/src` on Atlas) in two places only, checked on 2026-11-23 with line endings ignored:
   - `measure.py`: loading a router's configuration gets its own limit of 1,800 s (`CONFIG_TIMEOUT`). Every other
     command keeps 120 s, and a deployment that finished within 120 s per load runs exactly as before.
   - `report.py`: labels for Topology Zoo graphs. Neither the labs nor the FL scripts use it.
2. **Test cells: 512 routers at degree 8 and 16, and 1,024 routers at degree 4, 8 and 16.** The 512-router
   degree-4 cell was graded in FL1-002 (10.5%, not discriminating) and does not run again. It is reported as
   secondary.
3. **The setup gate I3 is carried over, not run again.** FL1-002's I3 (PASS, logged 2026-11-22 22:15:18 UTC) was
   measured in this setup: the same guest, image, timers and windows. Its two 256-router deployments completed within
   the old limit, so the new limit leaves them unchanged. I4 applies, as before, to every record of every graded test
   cell.

Everything else is FL1-002's, and through it FL1-001's: the claim, the m-law, the d-law rival, the lockstep model,
the calibration table and summary (same sha256), the bar (8.557 points), the discriminating rule, gates G1, G2, I0,
I1, I2 and I4, the verdict rule, the setup (KVM guest, FRR's defaults, 60 s windows) and the five sealed scripts at
their hashes.

## Data seen before this draft (exploratory, not evidence for the verdict)

- **FL1-002's record:**
  - I3 (6.12% against 8.55%, and 12.51% against 14.53%).
  - The 512-router degree-4 cell: 10.5%, against the m-law's 7.0% and the d-law's 12.4%.
  - The two deployment failures. No run of either discriminating cell exists.
- **The 256-router degree-16 graph under FRR's defaults, in a guest** (topology-builders `results/operator-timers`,
  2026-11-22): 23.0% at m = 1.5025. The m-law gives 37.9%, 14.9 points above, outside the bar; the d-law gives
  74.7%. It was seen after FL1-002's seal and before this draft. It warns that G1 may fail where m is larger; it
  changes nothing here, since the law, calibration, bar and cells are FL1-001's.
- **topology-builders' other results of 2026-11-22** (operator timers at 64 routers, four Topology Zoo networks):
  public, and not used here.
- **1,024 routers:** nothing built or run.

## Design

- **Calibration, m-law, d-law, model, bar:** as FL1-001 (`fl1-calibration.csv`, `fl1-calibration.json`). Bar 8.557
  points; a cell is discriminating when its m-law and d-law predictions differ by at least 17.11 points.
- **Test cells:**
  - 512 routers: `random-regular-n512-d8-s1.json` (sha256 9d36d1c6...02da778) and `random-regular-n512-d16-s1.json`
    (22a0e741...6141f54), the files of the 2026-11-21 queue (`tb-n512/topos512`). Discriminating: m-law 11.0%
    against d-law 35.3%, and 23.9% against 74.7%.
  - 1,024 routers, degree 4, 8 and 16, seed 1: built in the gap step by `topology-builders build random-regular
    --routers 1024 --degree d --seed 1` from the tree at 69220fe. Degree 8 and 16 are expected to discriminate
    (FL1-002's argument); the gap step's predictions decide.
- **Measurement, as FL1-002:**
  - Labs: `clab ... --hello-interval 3 --hello-multiplier 10 --lsp-gen-interval 30`, then
    `measure --backend netns --profile --links 3 --repeat 2 --max-wait 600 --window 60`.
  - Guest: one per lab through `run_vm.sh`, 16 vCPUs on CPUs 12-23,36-43. Guest RAM is 64 GiB at 512 routers and
    128 GiB at 1,024.
  - One lab at a time.
  - Caps: 8 h (512) and 12 h (1,024).
- **Order and stopping:**
  - Gap 0: checks.
  - 512 routers at degree 8, then 16.
  - Gap: if neither is graded, the queue stops and FL1-003 is VOID.
  - Gap: 1,024-router files built and predicted. Then degree 4, 8 and 16.
  - Gap: grading.
  - No reruns.
- **Gap steps**, logged in `/archive/experiments/tb-vm/fl1-003/` before each size's first LAB line:
  - The sha256 of the five scripts and the calibration table are checked.
  - The summary is recomputed from the table, byte-identical.
  - For 512 routers, the predictions are rewritten and must equal FL1-002's (sha256 40094c25...39f9) for these two
    files.
  - For 1,024 routers, the files are built and the predictions written, with their sha256 logged.

```yaml
id: PREREG-FL1-003
date: 2026-11-23
retrospective: false
status: sealed
supersedes: PREREG-FL1-002 (sealed 62c255d; VOID: both discriminating cells failed at deployment)
kind: size-transfer test of a one-statistic law (two-hop multiplicity) for the link-change LSP saving of IS-IS
      flood reduction (FRR PR 24128 at e263c441) on random regular graphs, against a degree-only rival, in KVM guests
      under FRR's default timers
harness: analysis/flooding/{fl_common,fl1_calibrate,fl1_predict,fl1_grade,fl1_setup_check}.py as sealed in
  PREREG-FL1-001 and PREREG-FL1-002
code_hash:
  fl_common.py: sha256:1847b8809b01ffc6c2920b09070e631940bf227d44d3fb26f78c39bfed32642b
  fl1_calibrate.py: sha256:fb45f6051a42b516f96ba01184bece8800852aa6b39499b2d0779a9b84bdddb6
  fl1_predict.py: sha256:b4dfc1771b716bfc7418b5652cf3ff0f953a7110ac78b3422e84f692543319c2
  fl1_grade.py: sha256:ad3ca4cf07ca351242dc9b6a3b8b24b17aff9e0da934b0dd59f5e29eb9b89fb0
  fl1_setup_check.py: sha256:312c6409743a7256eb39a2de9647727b0a3f2b90f6649e5b189ab7564de9db91
calibration: as PREREG-FL1-001 (table sha256:8695ea7e...1bcc, summary sha256:afc46bd8...7f96, 23 rows, bar_pct 8.5568)
substrate: topology-builders at 69220fe (its topology_builders package copied with file hashes to
  /archive/experiments/tb-vm/fl1-003/src before the first lab, for predictions and labs alike); FRR
  pr24128-e263c441 in image tb-colab-test:latest (sha256:e3c3479e...f3dc) from the guest's read-only images share;
  guest golden-flat.qcow2 of 2026-11-20; tools/overlay/run_vm.sh as at topology-builders 3bd633a
power: continuous gates; four cells expected discriminating (512 d8, d16; 1,024 d8, d16); the risk is deployment
  or convergence at 1,024 routers in 16 vCPUs, which voids, never fails
pilot: none new; FL1-002's run (its record, above)
setup_gates:
  I3 (setup): carried over from PREREG-FL1-002 (PASS, 2026-11-22 22:15:18 UTC: 256 routers degree 4 -2.43 points,
      degree 8 -2.02 points, bar 8.557)
  I4 (setup): every record of every graded test cell carries hello_interval 3, hello_multiplier 10,
      lsp_gen_interval 30 and window_s 60 (fl1_setup_check.py)
sealed_gates:
  G1 (physics): on every graded discriminating cell, |measured - m_law| <= bar
  G2 (physics): m-law mean absolute error < d-law mean absolute error over the graded discriminating cells
  discriminating: |m_law - d_law| >= 2 * bar (fixed by the predictions, before any test measurement)
  I0 (instrument): multiplicity recomputed equals the builder's recorded value (|diff| <= 1e-4) where recorded
  I1 (instrument): each test size's predictions and their sha256 are written by the gap step (its log in
      /archive/experiments/tb-vm/fl1-003/) before that size's first LAB line in the queue log, by the sealed scripts
      (sha256 checked), from the sealed table, with the summary recomputed byte-identical; at 512 routers the
      prediction values equal FL1-002's for the two test files
  I2 (instrument): each graded cell's records carry the sha256 of the predicted topology file
  on an I0-I2 or I4 failure no gate is interpreted; FL1-003 is VOID and reported
verdict: PASS iff I4 PASS, >= 2 discriminating cells graded, and G1 and G2 hold; FAIL iff I4 PASS, >= 2 graded, and
  G1 or G2 fails; VOID otherwise (a cell is VOID if any of its runs did not converge or a side has no link window)
clusters: one graph per cell; cells are the independent unit
stopping: fixed: the queued runs, two runs per variant; no reruns; a cell lost to memory, time or deployment is
  VOID; 1,024 not run if no discriminating 512 cell is graded
falsification: G1 fail -> the saving does not transfer across size through m alone at this bar; G2 fail -> degree
  predicts the larger networks at least as well as m; each is reported as the answer, at equal prominence
secondary (cannot rescue the verdict): model lockstep error per cell; non-discriminating cells (1,024 degree 4); the
  512-router degree-4 cell of FL1-002; the 256-router degree-16 lab under FRR's defaults; per-size errors
amendments: []
```

## Scope and non-claims

FL1-002's: random regular graphs, one seed per size, one FRR commit, one host, three links per run, two runs. The
test setup (guest, FRR's defaults, 60 s windows) differs from the calibration's, and I3 checked that difference at
256 routers only. No claim about other families, other timers, or that m causes the saving.

## Interpretation ceiling

On pass: for random regular graphs from 64 to 1,024 routers, the link-change LSP saving of this implementation,
under FRR's default timers, is predicted by the two-hop multiplicity alone, fitted under the study's timers. It is
predicted within 8.6 points, and better than by degree, on networks measured after the prediction was sealed. The
reading through Observation Theory would then have one sealed instance on this substrate. It would not establish the
law for other families, implementations, events or CPU, nor at 2,048 routers.
