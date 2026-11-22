# PREREG-FL1-001 — FL-1: the two-hop law transfers to 1,024 and 2,048 routers

**Status:** SEALED (sealing commit and SHA-256 in `SEALS.md`), "Authorized by: A. H. Bond (session instruction)".
Calibration complete from a logged pilot (the Atlas queue's gap step, 2026-11-21 23:45-23:47 UTC); one pilot-caught
defect in the bar rule fixed before the seal and itemized below. Test sizes run after the sealing commit.

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
  (`random-regular-n128`) in Docker labs, and the 256-router run (`tb-n256`) in namespace labs. 23 graphs
  (`analysis/flooding/calibration/fl1-calibration.csv`).
- **m-law:** the isotonic (non-decreasing) least-squares fit of the saving on m over the calibration set, linear
  between knots, constant beyond them (`fl1-calibration.json`, `m_law_knots`).
- **d-law (rival):** the same fit on degree over the 64-router calibration graphs only (`d_law_knots`).
- **Model (secondary):** `topology_builders.flood_model` in lockstep, for the exact three links `measure` will take
  down (chosen from each file's sha256 and seed 1), averaged over their down and up changes.
- **Bar** (percentage points), by rule: `max(3 * sigma_seed, loso_max)`. `sigma_seed` is the largest standard
  deviation of the saving among calibration graphs of the same size and degree. `loso_max` is the largest absolute
  error of the m-law on one calibration size when fitted on the other sizes, counting only held-out graphs whose m
  lies inside the range the fit was made on (the test predicts inside the calibrated range; an extrapolation error
  measures the extrapolation, not the transfer). The law must transfer to new sizes at least as well as it did
  between the sizes it was calibrated on.
- **Test cells:** the six topology files `topology-builders build random-regular --routers N --degree d --seed 1`,
  N in {1024, 2048}, d in {4, 8, 16}, as the queue scripts `tb-n1024/n1024.sh` and `tb-n2048/n2048.sh` build them.
  In the gap before each size's labs, the gap step checks the sealed scripts' and calibration's sha256, recomputes
  the calibration summary from the sealed table (it must be byte-identical), and runs `fl1_predict.py`; its log
  carries the predictions' sha256 before that size's first `LAB` line.
- **Measurement:** as queued: `measure --backend netns --profile --links 3 --repeat 2 --max-wait 600`, one container
  per degree, routers on CPUs 12-23,36-43, one lab at a time, nothing else of ours on those CPUs during a lab; a
  watchdog stops a lab at 6 h (1,024) or 8 h (2,048) and keeps the runs it finished.
- **512 routers:** predicted in the gap before its labs (23:47 UTC, hash below), so the prediction precedes the data,
  but before this seal. Reported beside the verdict with the sealed bar, not graded.

## Disclosed calibration pilot (verbatim from the gap step; full files in `analysis/flooding/calibration/`)

Calibration rows (`fl1-calibration-original-rule.txt`; saving = link-change LSP saving, both variants converged):

| Routers | Degree | Seed | m | Saving |
|---:|---:|---:|---:|---:|
| 64 | 3 | 1 | 1.0105 | 7.0% |
| 64 | 4 | 1, 1, 2, 3 | 1.0368, 1.0368, 1.0776, 1.0645 | 11.8%, 9.2%, 14.8%, 13.9% |
| 64 | 6 | 1 | 1.1753 | 22.7% |
| 64 | 8 | 1, 1, 2, 3 | 1.4239, 1.4239, 1.3995, 1.4038 | 36.5%, 35.8%, 35.0%, 33.7% |
| 64 | 12 | 1 | 2.3483 | 58.8% |
| 64 | 16 | 1, 1, 1, 2, 3 | 3.9384 (x3), 3.9286, 3.9686 | 75.1%, 74.1%, 75.0%, 75.0%, 74.3% |
| 64 | 24 | 1 | 9.0553 | 90.5% |
| 64 | 32 | 1 | 16.3014 | 94.1% |
| 128 | 4, 8, 16 | 1 | 1.0271, 1.1784, 2.1516 | 8.1%, 19.5%, 52.8% |
| 256 | 4, 8 | 1 | 1.0119, 1.0885 | 8.5%, 14.5% |

Left out by rule (a run did not converge): 64 routers degree 48 (seed 1) and degree 32 (seeds-n64, seeds 1-3), and
256 routers degree 16 (flood reduction off overloaded the 20 CPUs: load about 790 for the lab's 4 h 50 min).

- `I0`: multiplicity recomputed here against the builder's recorded value on the 2 calibration files that record
  one: max |diff| 1.9e-5 (builder rounds to 4 decimals; gate 1e-4). PASS.
- `sigma_seed` = 2.487 points (64 routers, degree 4; degree 8: 1.183; degree 16: 0.451).
- **Pilot-caught defect (itemized, §5.1):** the drafted rule took `loso_max` over every held-out graph. Holding out
  64 routers fits the law on 128 and 256 routers (m up to 2.15) and predicts 64-router graphs at m up to 16.3 by
  extrapolation: `loso_max` 41.32, bar 41.32 points (`fl1-calibration-original-rule.json`). With that bar no test
  cell could be discriminating (2 x bar = 82.6 points exceeds every m-law vs d-law gap), so the test would be VOID by
  construction. Revised rule (above): held-out graphs inside the fitted m range only; 9 of the 64-router graphs fall
  outside (degree 3 below; degree 12, 16, 24 and 32 above), none of the 128- or 256-router graphs. Result: `loso_max` = 8.557
  (64 routers held out; mean 4.45), 2.03 (128), 1.18 (256). **Bar = max(3 x 2.487, 8.557) = 8.557 points**; a cell
  is discriminating when its m-law and d-law predictions differ by at least 17.11 points. The revision tightens the
  bar; it was not chosen to make the test pass.
- Margin (§5.1, continuous gate): the bar is 1.0x the largest in-range transfer error seen in calibration and 3.4x
  the largest seed standard deviation; the mean in-range transfer errors (1.2 to 4.4 points) sit 1.9x to 7x inside
  it.
- 512-router predictions (`fl1-predictions-n512.json`, sha256 75cefbb9...02e36, written 23:47 UTC before the labs;
  the file records the drafted bar, the knots are the same): degree 4, m 1.0086: m-law 7.0%, d-law 12.4%, model 2.5%
  (not discriminating); degree 8, m 1.0415: m-law 11.0%, d-law 35.3%, model 5.4% (discriminating, gap 24.3);
  degree 16, m 1.2256: m-law 23.9%, d-law 74.7%, model 20.0% (discriminating, gap 50.8).

```yaml
id: PREREG-FL1-001
date: 2026-11-22
retrospective: false
status: sealed
kind: size-transfer test of a one-statistic law (two-hop multiplicity) for the link-change LSP saving of IS-IS
      flood reduction (FRR PR 24128 at e263c441) on random regular graphs, against a degree-only rival
harness: analysis/flooding/{fl_common,fl1_calibrate,fl1_predict,fl1_grade}.py at commit b219af2
code_hash:
  fl_common.py: sha256:1847b8809b01ffc6c2920b09070e631940bf227d44d3fb26f78c39bfed32642b
  fl1_calibrate.py: sha256:fb45f6051a42b516f96ba01184bece8800852aa6b39499b2d0779a9b84bdddb6
  fl1_predict.py: sha256:b4dfc1771b716bfc7418b5652cf3ff0f953a7110ac78b3422e84f692543319c2
  fl1_grade.py: sha256:ad3ca4cf07ca351242dc9b6a3b8b24b17aff9e0da934b0dd59f5e29eb9b89fb0
calibration:
  table: analysis/flooding/calibration/fl1-calibration.csv sha256:8695ea7eec75a40e3f09c2e3eaefce9aa4869c40d22ba8f8734312d4a1031bcc
  summary: analysis/flooding/calibration/fl1-calibration.json sha256:afc46bd811bbe766a270d7507fc898f61e0007b9ad98bedff4d9e8dc54c07f96
  rows: 23
  sigma_seed_pct: 2.4872
  loso_max_pct: 8.5568
  bar_pct: 8.5568
substrate: topology-builders 0.2.0 tree (with the report fix of 2026-11-21) in /tmp/tb-gap/src; FRR
  pr24128-e263c441 in image tb-colab-test:latest; random-regular generator unchanged since v0.2.0
power: continuous gates; bar sized by rule from the calibration (above), margin printed above
pilot: the gap step of 2026-11-21 23:45-23:47 UTC (logged; outputs committed at b219af2); one rule change itemized
test_cells: random-regular, seed 1, routers {1024, 2048} x degree {4, 8, 16}
sealed_gates:
  G1 (physics): on every graded discriminating cell, |measured - m_law| <= bar
  G2 (physics): m-law mean absolute error < d-law mean absolute error over the graded discriminating cells
  discriminating: |m_law - d_law| >= 2 * bar (fixed by the predictions, before any test measurement)
  I0 (instrument): multiplicity recomputed equals the builder's recorded value (|diff| <= 1e-4) where recorded
      (pilot: PASS, 1.9e-5)
  I1 (instrument): each test size's predictions and their sha256 are written by the gap step (its log
      /archive/experiments/tb-colab/gap-hook-<UTC time>.log) before that size's first LAB line in its queue log, by
      the sealed scripts (sha256 checked), from the sealed table, with the summary recomputed byte-identical
  I2 (instrument): each graded cell's records carry the sha256 of the predicted topology file
  on an I0-I2 failure no gate is interpreted; the size is VOID for FL1 and reported
verdict: PASS iff >= 2 discriminating cells graded and G1 and G2 hold; FAIL iff >= 2 graded and G1 or G2 fails;
  VOID otherwise (a cell is VOID if any of its runs did not converge or a side has no link window)
clusters: one graph per cell; cells are the independent unit
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
namespace labs in topology-builders `results/colab-sessions`; the 256-router calibration is in the test's own
backend). Three links per run, two runs. No claim about other families (flattened butterflies already show degree
mattering at fixed m = 2). No claim that m causes the saving: the claim is predictive sufficiency within this
family. The calibration already hints at a residual size effect (64-router graphs near m = 1.4 save up to 8.6 points
more than the law fitted on larger sizes predicts); the bar is sized to it, and the test reports it.

## Interpretation ceiling

On pass: for random regular graphs from 64 to 2,048 routers, the link-change LSP saving of this implementation is
predicted by the two-hop multiplicity alone to within 8.6 points, and better than by degree, on networks measured
after the prediction was sealed. It would license using m, not degree, to say where flood reduction pays in large
sparse networks. It would not establish the law for other families, other implementations, other events (router or
multi-link failures), or CPU.
