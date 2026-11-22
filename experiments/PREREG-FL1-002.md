# PREREG-FL1-002 — FL-1, successor: the two-hop law transfers to 512 and 1,024 routers, measured in KVM guests

**Status:** SEALED (sealing commit and SHA-256 in `SEALS.md`), "Authorized by: A. H. Bond (session instruction)".
Successor to `PREREG-FL1-001` (sealed at 061a41e), which is VOID without data: none of its test labs ran. It
stays sealed and unedited; this registration names what it repairs.

## Why a successor

FL1-001's test labs were the 1,024- and 2,048-router random regular graphs on the namespace backend directly on the
Atlas host. They never started. The 512-router labs queued before them ran that way on 2026-11-22. The first, degree 4
with flood reduction off, never converged at bring-up and drove the host's load to about 1,560. A netlink request
from systemd-networkd for the uplink's route then timed out, and the uplink failed. Since then every lab on Atlas runs
in a KVM guest with its own kernel and no network device (topology-builders `tools/overlay/run_vm.sh`, commit
70de788). FL1-001's sealed setup can no longer be run, so its sizes cannot be graded as sealed.

## What changes, and why

1. **Setup: a KVM guest.** 16 vCPUs on CPUs 12-23,36-43, one guest at a time. Inside it, the namespace backend in the
   same container image as before (tb-colab-test, FRR pr24128-e263c441). The host's 20 CPUs are no longer the lab's.
2. **Timers: FRR's defaults.** Hello 3 s x 10 and lsp-gen-interval 30, with 60 s windows, instead of the study's
   hello 1 s x 3, lsp-gen-interval 2 and 30 s windows. Under the study's timers, two labs near these sizes did not
   converge without flood reduction on this hardware: the 512-router degree-4 lab (above) and the 256-router
   degree-16 lab (load about 790 on the host for 4 h 50 min; in a guest on 2026-11-22, no run finished in an hour).
   The heavier test cells under those timers are untried. A test whose cells cannot converge is VOID by
   construction. FRR's defaults are what an operator runs.
3. **Sizes: 512 and 1,024 routers.** 512 is the size the FL1-001 queue predicted but did not grade. 2,048 is dropped:
   at the 256-router labs' 35 to 48 MiB per router, its degree-16 labs would need over 100 GiB in a guest, and its
   runs would take days on 16 vCPUs. That is an estimate; I have not tried.
4. **New setup gates, I3 and I4** (`analysis/flooding/fl1_setup_check.py`). Before any test cell runs, the two
   256-router calibration graphs (degree 4 and 8) are measured again in the test setup. They are the only
   calibration graphs measured on the namespace backend, and their savings (8.5% and 14.5%) sit in the range the
   test cells are predicted in. Each must reproduce its calibration saving within the bar (I3). Every record of every
   run must carry the test setup's timers and window (I4). The law is calibrated in one setup and tested in another;
   these gates check that the change of setup does not move the saving by more than the bar. On an I3 or I4 failure,
   no test cell is interpreted.

Unchanged from FL1-001: the claim, the m-law, the d-law rival and the lockstep model. The calibration table and
summary are reused byte for byte, at the same sha256, and so is the bar (8.557 points). Also unchanged: the
discriminating rule, gates G1, G2, I0 and I2, the verdict rule and the four sealed scripts at their sealed hashes.
FL1-001's anchor discipline applies as written.

## Data seen before this draft (exploratory, not evidence for the verdict)

- **512 routers.** The predictions (`calibration/fl1-predictions-n512.json`, sha256 75cefbb9...02e36) were written
  at 2026-11-21 23:47 UTC, before any 512-router lab. Only the degree-4 lab started afterwards, on the host, under
  the study's timers. Its flood-reduction-off run sent 39.3 million LSPs at bring-up without converging and was
  stopped. No link window and no saving was observed at 512 routers. Degree 8 and 16 never ran.
- **1,024 routers:** nothing built or run.
- **64-router labs in a guest** (topology-builders ops block, 2026-11-22), the same files under both timer sets.
  Link-change saving, study timers against FRR's defaults: random regular degree 16 (a calibration graph) 72.55%
  against 73.06%; butterfly 4x4x4 69.06% against 67.60%; leaf-spine 48 x 16 93.18% against 93.31%; random regular
  degree 32 93.63% against 93.69%. Every run converged. These were seen before the timers were chosen (change 2).
  The setup check's pilot is on the first of them, against its calibration value of 74.61%: -1.55 points (defaults)
  and -2.06 (study timers), I3 PASS. It is a test of the code on seen data, not the gate.
- **256 routers, degree 16, FRR's defaults, in a guest** (ops block, started 11:48 UTC): running as this is
  drafted. A status line showed its first run's bring-up: flood reduction off, 3.97 million LSPs, converged. Its link
  windows have not been looked at, and will not be before the seal. It is neither a calibration graph nor a test
  cell.

## Design

- **Calibration, m-law, d-law, model, bar:** as FL1-001 (`fl1-calibration.csv`, `fl1-calibration.json`); bar 8.557
  points; a cell is discriminating when its m-law and d-law predictions differ by at least 17.11 points.
- **Setup gate I3:** `random-regular-n256-d4-s1.json` (sha256 1a290891...8fffac) and `random-regular-n256-d8-s1.json`
  (c2def38b...a6a7f3), the files of the calibration rows, measured in the test setup. `fl1_setup_check.py` compares
  each saving with its calibration value (8.5457% and 14.5293%). PASS iff both are graded and within the bar.
- **Test cells:** random regular, seed 1, N in {512, 1024} x degree {4, 8, 16}.
  - The 512-router files are those of the 2026-11-21 queue (`tb-n512/topos512`; sha256 in the 512 predictions file).
  - The 1,024-router files are built in the gap step with `topology-builders build random-regular --routers 1024
    --degree d --seed 1`, from FL1-001's tree (see `substrate`), which the labs run too.
  - From the 512 predictions with this bar, degree 8 (m-law 11.0%, d-law 35.3%) and degree 16 (23.9% against 74.7%)
    are discriminating, and degree 4 (7.0% against 12.4%) is not.
  - At 1,024 routers, m is expected to be below 512's at each degree, since in random regular graphs two routers
    two hops apart share fewer neighbors as the graph grows. The m-law never decreases as m rises, so each 1,024
    prediction would be at most the 512 one, while the d-law stays at 12.4%, 35.3% and 74.7%. Degree 8 and 16 would
    then discriminate by at least 24 and 51 points. The gap step's predictions decide.
- **Measurement:**
  - Labs: `clab ... --hello-interval 3 --hello-multiplier 10 --lsp-gen-interval 30`, then
    `measure --backend netns --profile --links 3 --repeat 2 --max-wait 600 --window 60`.
  - Guest: one per lab, through `run_vm.sh` (topology-builders 3bd633a) and its `jobs/netns`, 16 vCPUs. Guest RAM is
    64 GiB at 256 and 512 routers and 128 GiB at 1,024.
  - One lab at a time, and nothing else of ours runs on Atlas during a lab.
  - Caps: 5 h (256), 8 h (512), 12 h (1,024). A capped lab keeps the runs it finished, since records are appended as
    each run ends.
  - Worst case 70 h for the eight labs.
- **Order and stopping:**
  - The two I3 labs come first, then the gap step's I3 and I4 check.
  - Then 512 routers (degree 4, 8, 16), then 1,024 (degree 4, 8, 16).
  - On I3 or I4 not PASS, the queue stops; no test cell runs, and FL1-002 is VOID.
  - If neither discriminating 512-router cell is graded, 1,024 is not run (its labs are heavier), and FL1-002 is
    VOID.
  - No reruns.
- **Gap step** (logged, in `/archive/experiments/tb-vm/fl1-002/`), before each size's first LAB line:
  - Check the sha256 of the five scripts and of the calibration table.
  - Recompute the summary from the table; it must be byte-identical to the sealed one.
  - For 1,024 routers only, build the three topology files.
  - Run `fl1_predict.py`, and log the predictions' sha256.
  - For 512 routers, the recomputed m-law, d-law and model values must equal those in `fl1-predictions-n512.json`
    (only its recorded bar differs).

```yaml
id: PREREG-FL1-002
date: 2026-11-22
retrospective: false
status: sealed
supersedes: PREREG-FL1-001 (sealed 061a41e; VOID without data, its test labs never ran)
kind: size-transfer test of a one-statistic law (two-hop multiplicity) for the link-change LSP saving of IS-IS
      flood reduction (FRR PR 24128 at e263c441) on random regular graphs, against a degree-only rival, in KVM guests
      under FRR's default timers
harness: analysis/flooding/{fl_common,fl1_calibrate,fl1_predict,fl1_grade}.py as sealed in PREREG-FL1-001, plus
  fl1_setup_check.py (new)
code_hash:
  fl_common.py: sha256:1847b8809b01ffc6c2920b09070e631940bf227d44d3fb26f78c39bfed32642b
  fl1_calibrate.py: sha256:fb45f6051a42b516f96ba01184bece8800852aa6b39499b2d0779a9b84bdddb6
  fl1_predict.py: sha256:b4dfc1771b716bfc7418b5652cf3ff0f953a7110ac78b3422e84f692543319c2
  fl1_grade.py: sha256:ad3ca4cf07ca351242dc9b6a3b8b24b17aff9e0da934b0dd59f5e29eb9b89fb0
  fl1_setup_check.py: sha256:312c6409743a7256eb39a2de9647727b0a3f2b90f6649e5b189ab7564de9db91
calibration: as PREREG-FL1-001 (table sha256:8695ea7e...1bcc, summary sha256:afc46bd8...7f96, 23 rows, bar_pct 8.5568)
substrate: the topology-builders tree of PREREG-FL1-001 (/tmp/tb-gap/src), copied with its file hashes to
  /archive/experiments/tb-vm/fl1-002/src before the first lab, for the predictions and the labs alike (the ops
  block's tree /tmp/tb-final/src differs from it only in docstrings, help strings and the report's labels: checked
  2026-11-22 with line endings ignored); FRR pr24128-e263c441 in image tb-colab-test:latest
  (sha256:e3c3479e...f3dc), loaded in the guest from the read-only images share; guest golden-flat.qcow2 of
  2026-11-20; tools/overlay/run_vm.sh at topology-builders 3bd633a
power: continuous gates; four cells expected discriminating (512 d8, d16 known; 1,024 d8, d16 expected); the risk is
  convergence at 1,024 routers in 16 vCPUs, which voids, never fails
pilot: fl1_setup_check.py on the 64-router calibration graph's two guest labs (above); the 512 predictions of
  2026-11-21; no other pilot
setup_gates:
  I3 (setup): the 256-router calibration graphs of degree 4 and 8, measured in the test setup after the seal and
      before any test cell, each within the bar of its calibration saving (fl1_setup_check.py)
  I4 (setup): every record of the I3 labs and of every graded test cell carries hello_interval 3, hello_multiplier
      10, lsp_gen_interval 30 and window_s 60 (fl1_setup_check.py)
sealed_gates:
  G1 (physics): on every graded discriminating cell, |measured - m_law| <= bar
  G2 (physics): m-law mean absolute error < d-law mean absolute error over the graded discriminating cells
  discriminating: |m_law - d_law| >= 2 * bar (fixed by the predictions, before any test measurement)
  I0 (instrument): multiplicity recomputed equals the builder's recorded value (|diff| <= 1e-4) where recorded
  I1 (instrument): each test size's predictions and their sha256 are written by the gap step (its log in
      /archive/experiments/tb-vm/fl1-002/) before that size's first LAB line in the queue log, by the sealed scripts
      (sha256 checked), from the sealed table, with the summary recomputed byte-identical; at 512 routers the
      prediction values equal fl1-predictions-n512.json's
  I2 (instrument): each graded cell's records carry the sha256 of the predicted topology file
  on an I0-I4 failure no gate is interpreted; FL1-002 is VOID and reported
verdict: PASS iff I3 and I4 PASS, >= 2 discriminating cells graded, and G1 and G2 hold; FAIL iff I3 and I4 PASS,
  >= 2 graded, and G1 or G2 fails; VOID otherwise (a cell is VOID if any of its runs did not converge or a side has
  no link window)
clusters: one graph per cell; cells are the independent unit
stopping: fixed: the queued runs, two runs per variant; no reruns; a cell lost to memory or time is VOID; 1,024 not
  run if no discriminating 512 cell is graded
falsification: G1 fail -> the saving does not transfer across size through m alone at this bar; G2 fail -> degree
  predicts the larger networks at least as well as m; I3 fail -> the test setup moves the saving by more than the
  bar, and the law cannot be tested in it; each is reported as the answer, at equal prominence
secondary (cannot rescue the verdict): model lockstep error per cell; non-discriminating cells; per-size errors;
  the 256-router degree-16 lab under FRR's defaults (ops block)
amendments: []
```

## Scope and non-claims

The scope is FL1-001's: random regular graphs, one seed per size, one FRR commit, one host, three links per run, two
runs. It narrows further: the test setup (guest, FRR's default timers, 60 s windows) differs from the calibration's
(the host; Docker labs at 64 and 128 routers, namespace labs at 256; the study's timers; 30 s windows). I3 checks that
difference at 256 routers only, and the 64-router comparison above is exploratory. No claim about other families,
about timers other than these two sets, or that m causes the saving.

## Interpretation ceiling

On pass: for random regular graphs from 64 to 1,024 routers, the link-change LSP saving of this implementation, under
FRR's default timers, is predicted by the two-hop multiplicity alone, fitted under the study's timers. It is
predicted within 8.6 points, and better than by degree, on networks measured after the prediction was sealed. The
reading through Observation Theory would then have one sealed instance on this substrate: the reflood decision reads
two hops, and the saving factors through the statistic of what two hops can see. It would not establish the law for
other families, implementations, events (router or multi-link failures) or CPU, nor at 2,048 routers.
