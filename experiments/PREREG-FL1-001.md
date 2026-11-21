# PREREG-FL1-001 — FL-1: the two-hop law transfers to 1,024 and 2,048 routers

**Status:** DRAFT, unsealed. Harness written (`analysis/flooding/`), calibration and the 512-router check run in
the queue's gap before the 512-router labs; bars PENDING that calibration (filled from
`fl1-calibration.json`, never chosen by hand). Seal = commit + `SEALS.md` row, "Authorized by: A. H. Bond (session
instruction)", before the first 1,024-router lab starts.

## Anchor discipline (read first)

That flood reduction saves more in denser networks is known (`FLOODING-TRACK.md`): the spanning-tree bound and the
"fan-out" heuristic both say so, and both make the saving a function of **degree**, independent of size. Two-hop
relay selection is old (MPR, OSPF-MDR). This registration claims none of that. It tests one sharper statement on
held-out sizes: for random regular graphs the saving is a function of the **two-hop multiplicity** m alone, so at a
fixed degree it falls with size as m falls, by an amount fitted on smaller networks and predicted before the larger
ones run. The contribution, if it passes, is a measured size-transfer law for a real implementation, and an
instance of the Observation Theory reading: the reflood decision reads two hops, so the saving factors through the
statistic of what two hops can see.

## Claim under test

For random regular graphs of 1,024 and 2,048 routers (degree 4, 8 and 16; seed 1), FRR pull request 24128 at
e263c441 saves, per link change, the share of LSPs that the **m-law** predicts from each graph's two-hop
multiplicity, within the bar, on every graded discriminating cell; and the m-law's mean absolute error over those
cells is below the **d-law**'s (the rival: the saving at the same degree in 64-router graphs, which is what a
size-independent, degree-only account predicts).

## Design

- **Calibration set** (seen; fitted): every random regular graph measured before the gap step, with its topology
  file matched by sha256 and every run converged: the 64-router density sweep (`random-regular-n64`, degree 3 to
  48), the degree-16 check in `families-n64`, the three seeds per degree of `seeds-n64`, the 128-router run
  (`random-regular-n128`) in Docker labs, and the 256-router run (`tb-n256`) in namespace labs.
  `fl1_calibrate.py` writes one row per graph and the knots of both laws.
- **m-law:** the isotonic (non-decreasing) least-squares fit of the saving on m over the calibration set, linear
  between knots, constant beyond them.
- **d-law (rival):** the same fit on degree over the 64-router calibration graphs only.
- **Model (secondary):** `topology_builders.flood_model` in lockstep, for the exact three links `measure` will take
  down (chosen from each file's sha256 and seed 1), averaged over their down and up changes.
- **Bar** (percentage points), by rule: `max(3 * sigma_seed, loso_max)`. `sigma_seed` is the largest standard
  deviation of the saving among calibration graphs of the same size and degree. `loso_max` is the largest absolute
  error of the m-law on one calibration size when fitted on the others. The law must transfer to new sizes at least
  as well as it did to the worst held-out size it was calibrated on.
- **Test cells:** the six topology files `topology-builders build random-regular --routers N --degree d --seed 1`,
  N in {1024, 2048}, d in {4, 8, 16}, as the queue scripts `tb-n1024/n1024.sh` and `tb-n2048/n2048.sh` build them.
  `fl1_predict.py` writes their predictions in the gap before each size's labs; the gap step's log carries the
  output's sha256 before that size's first `LAB` line.
- **Measurement:** as queued: `measure --backend netns --profile --links 3 --repeat 2 --max-wait 600`, one container
  per degree, routers on CPUs 12-23,36-43, one lab at a time, nothing else of ours on those CPUs during a lab.
- **512 routers:** predicted in the gap before its labs (hash in `tb-n512/n512.log`), so the prediction precedes
  the data, but the registration is not sealed by then. Reported beside the verdict, not graded.

## Disclosed calibration pilots

PENDING: the gap step after the 256-router run writes `fl1-calibration.{csv,json,txt}`,
`fl1-predictions-n512.{json,txt}`. Their numbers go here, verbatim, before the seal.

```yaml
id: PREREG-FL1-001
date: 2026-11-21
retrospective: false
status: draft
kind: size-transfer test of a one-statistic law (two-hop multiplicity) for the link-change LSP saving of IS-IS
      flood reduction (FRR PR 24128 at e263c441) on random regular graphs, against a degree-only rival
harness: analysis/flooding/{fl_common,fl1_calibrate,fl1_predict,fl1_grade}.py
code_hash: PENDING (sha256 of the four files at the sealing commit)
substrate: topology-builders 0.2.0 tree as uploaded to the gap step (commit PENDING); FRR pr24128-e263c441 in
  image tb-colab-test:latest
calibration: PENDING fl1-calibration.csv sha256 (rows, sigma_seed, loso_max, bar from fl1-calibration.json)
test_cells: random-regular, seed 1, routers {1024, 2048} x degree {4, 8, 16}
sealed_gates:
  G1: on every graded discriminating cell, |measured - m_law| <= bar
  G2: m-law mean absolute error < d-law mean absolute error over the graded discriminating cells
  discriminating: |m_law - d_law| >= 2 * bar (fixed by the predictions, before any test measurement)
  I0: integrity - multiplicity recomputed by fl_common equals the builder's recorded value (|diff| <= 1e-4) on
      every calibration graph that records one
  I1: integrity - each test size's predictions and their sha256 are written by the gap step (its log
      /archive/experiments/tb-colab/gap-hook-<UTC time>.log) before that size's first LAB line in its queue log,
      by the sealed fl1_predict.py, from the calibration whose sha256 is sealed below (the gap step refuses
      otherwise)
  I2: integrity - each graded cell's records carry the sha256 of the predicted topology file
  on I0-I2 failure no gate is interpreted; the run is VOID for FL1 and reported
verdict: PASS iff >= 2 discriminating cells graded and G1 and G2 hold; FAIL iff >= 2 graded and G1 or G2 fails;
  VOID otherwise (a cell is VOID if any of its runs did not converge or a side has no link window)
stopping: fixed: the queued runs, two runs per variant; no reruns; a cell lost to memory or time is VOID
falsification: G1 fail -> the saving does not transfer across size through m alone at this bar; G2 fail -> degree
  predicts the larger networks at least as well as m; either is reported as the answer, at equal prominence
secondary (cannot rescue the verdict): model lockstep error per cell; non-discriminating cells; the 512-router
  check; per-size errors
amendments: []
```

## Scope and non-claims

Random regular graphs only, one seed per size, one FRR commit, one host, the namespace backend for the test sizes
(the 64- and 128-router calibration ran in Docker labs, whose counts without flood reduction ran 5% to 15% above
namespace labs in `results/colab-sessions`; the 256-router calibration is in the test's own backend). Three links
per run, two runs. No claim about other families (flattened butterflies already show degree mattering at fixed
m = 2). No claim that m causes the saving: the claim is predictive sufficiency within this family.

## Interpretation ceiling

On pass: for random regular graphs from 64 to 2,048 routers, the link-change LSP saving of this implementation is
predicted by the two-hop multiplicity alone to within the bar, and better than by degree, on networks measured
after the prediction was sealed. It would license using m, not degree, to say where flood reduction pays in large
sparse networks. It would not establish the law for other families, other implementations, other events (router or
multi-link failures), or CPU.
