# PREREG-FL2-001 — FL-2: the quiet-window reference ages within a run

**Status:** SEALED (sealing commit and SHA-256 in `SEALS.md`), "Authorized by: A. H. Bond (session instruction)".
Pilot complete (the Atlas queue's gap step, 2026-11-21 23:47 UTC, on 208 profiled runs). **The pilot predicts this
registration's gates FAIL on the test host**: the effect appears on Colab and not on Atlas, where the test runs. It is
sealed in that direction on purpose (the DB-3 lesson: seal the prediction you actually hold, in either direction).

## Anchor discipline (read first)

Baseline drift is an old problem of measurement, and interleaving reference measurements is standard experimental
design; RFC 6413 asks benchmarks of link-state convergence to account for variance without fixing how. This
registration claims nothing general. It measures one harness: topology-builders `measure` subtracts a single quiet
window, taken once after bring-up, from every event window of a run, and its CPU savings already repeat less well
than its LSP savings (`results/seeds-n64`, `results/colab-sessions`). The question is whether that single reference
**ages**: whether its error grows with the time since it was taken, as retained side information does in the
Observation Theory staleness results (Paper V's staleness-work complement, Paper VIII's dynamic relevance), or
whether it is fixed noise that a longer quiet window would cure.

## Claim under test

Across the runs of the 1,024- and 2,048-router labs, the hello handler's net-of-quiet CPU is larger in a run's
last link-down window than in its first, in more runs than chance: D = e_last - e_first > 0, one-sided sign test,
where e_j = |net-of-quiet CPU of `send_hello_cb`| in the j-th link-down window, summed over the routers; and the
mean of e_last is at least r_min times the mean of e_first.

`send_hello_cb` sends one hello per interface per second whatever the event, so its net figure should be zero up to
noise; its size measures how far the host's background has moved since the reference. Under a fixed-noise
reference, E|e_j| is the same for every j and the sign test sits at chance; under an aging reference it grows with j.

## Design

- **Pilot (seen):** every profiled run in topology-builders `results/` and the 256-router run, written by the gap
  step to `analysis/flooding/calibration/fl2-pilot.txt` (verbatim below).
- **Test (unseen):** every run of the 1,024- and 2,048-router labs (Atlas, namespace backend, 20 pinned CPUs) with
  at least two link-down windows carrying per-handler figures: three links per run, so three link-down windows,
  minutes apart. Up to 24 runs (2 sizes x 3 degrees x 2 variants x 2 repeats).
- **Unit and clustering (PROTOCOL §5):** the run is the independent unit for the primary test, because the
  hypothesis is within-run and each run takes its own reference. Clustered by lab (size x degree), the direction is
  reported as a gate of consistency (G3); the claim needs both.
- **Secondary:** link-up windows (a link coming up changes the hello work at its two ends); the same statistic per
  size, per degree and per variant.

## Disclosed calibration pilot (verbatim, `fl2-pilot.txt`)

```
link-down windows: e_j = |net send_hello_cb|, ms summed over the routers
  seeds-n64              runs  80  D>0  46  D<0  34  sign-test p 0.109  mean e by window 26, 28, 31 ms  last/first 1.17
  n128                   runs  12  D>0   3  D<0   9  sign-test p 0.981  mean e by window 26, 44, 28 ms  last/first 1.09
  fat-tree               runs  20  D>0  10  D<0  10  sign-test p 0.588  mean e by window 13, 12, 13 ms  last/first 0.99
  nfly                   runs  16  D>0   5  D<0  11  sign-test p 0.962  mean e by window 5, 4, 3 ms  last/first 0.70
  colab-sessions         runs  56  D>0  40  D<0  16  sign-test p 0.000921  mean e by window 37, 50, 60 ms  last/first 1.49
  atlas-colab-links      runs  12  D>0   8  D<0   4  sign-test p 0.194  mean e by window 13, 13, 18 ms  last/first 1.36
  n256                   runs  12  D>0   6  D<0   6  sign-test p 0.613  mean e by window 149, 126, 236 ms  last/first 1.58
  POOLED                 runs 208  D>0 118  D<0  90  sign-test p 0.0305  mean e by window 33, 36, 44 ms  last/first 1.37
```

(Link-up windows: pooled 117 of 208, p 0.041, last/first 1.13; full table in the file.)

Reading: the pooled effect is carried by Colab (40 of 56 runs, p 0.0009, ratio 1.49), a shared cloud host. On Atlas,
the test host, the six datasets together give 78 of 152 runs with D > 0 (51%), with mixed ratios (0.70 to 1.58).

- **Bars.** G1: one-sided sign test p <= 0.05 at the realized number of untied test runs (exact binomial). G2: r_min
  = 1.38, set from the only pilot showing the effect (Colab, 1.49) with the house margin: 1 + (1.49 - 1) / 1.3.
- **Power (§5.1, exact binomial at the gate):** at 24 runs G1 needs D > 0 in at least 17 (p 0.032). If the true rate
  of D > 0 is Colab's 0.714, G1 passes with probability 0.62; at 0.80, 0.91; at the Atlas pilot rate 0.513, 0.04. At
  20 runs (a lab lost): 15 needed; 0.47 / 0.80 / 0.03. **Below 80% power at the Colab effect: a miss is reported as
  "effect below the bar, unresolvable at this n", never as absence.**
- **Sealed expectation:** FAIL (the Atlas pilot rate gives G1 about a 4% chance). A PASS would mean the reference ages
  on Atlas too at this size, which the pilot did not show.

```yaml
id: PREREG-FL2-001
date: 2026-11-22
retrospective: false
status: sealed
kind: within-run aging of a single quiet-window CPU reference in a network-emulation harness (topology-builders
      measure, --profile), read through a handler whose work does not depend on the event
harness: analysis/flooding/{fl_common,fl2_baseline_age}.py at commit b219af2
code_hash:
  fl_common.py: sha256:1847b8809b01ffc6c2920b09070e631940bf227d44d3fb26f78c39bfed32642b
  fl2_baseline_age.py: sha256:cd63b9fd72530e5175bce175502e68849bab963cc5e0878619b87806e001c080
handler: send_hello_cb
pilot: the gap step of 2026-11-21 23:47 UTC, 208 profiled runs (analysis/flooding/calibration/fl2-pilot.txt,
  sha256:f190d32420796f089c396d17243f3381fe5d7e4c8ee2de96a96ca86e67c36127)
power: exact binomial at the gate; 0.62 at the Colab pilot rate (24 runs); 0.04 at the Atlas pilot rate
sealed_gates:
  G1 (physics): one-sided sign test of D > 0 over the untied test runs, p <= 0.05
  G2 (physics): mean(e_last) / mean(e_first) >= 1.38 over the test runs
  G3 (physics, clustering): in at least all but one of the graded labs (size x degree), the median D is > 0
  I1 (instrument): every test run's link-down windows carry per-handler figures including send_hello_cb
  I2 (instrument): every test run's quiet window is satisfied (no LSP sent, no router's LSPs changed)
  a run failing I1 or I2 is left out and counted; if fewer than 12 runs remain, VOID
verdict: PASS iff G1, G2 and G3; FAIL otherwise, unless VOID
expected: FAIL (Atlas pilot); a FAIL is reported as "effect below the bar, unresolvable at this n" for G1
stopping: fixed: the queued runs; no reruns
falsification: G1, G2 or G3 fail -> the single reference does not measurably age within a run on Atlas at this n;
  the Colab pilot's aging is then a property of the shared cloud host, and an interleaved reference matters there;
  reported at equal prominence with the pass case
secondary (cannot rescue the verdict): link-up windows; per-size, per-degree and per-variant splits; the effect on
  the net isisd CPU of a link change
amendments: []
```

## Scope and non-claims

One harness, one test host (Atlas, routers on 20 pinned CPUs, other load as recorded in each queue's
`hostload.log`), the namespace backend, three link-down windows per run. A pass says the reference ages on this host
over a few minutes; it does not say why (other jobs, thermal state, the routers' own timers), and it says nothing
about FRR or flood reduction. A fail does not show the CPU savings are sound; only that their noise on this host is
not mostly age.

## Interpretation ceiling

On pass: in this harness, one quiet window per run is a stale reference on Atlas as well as on Colab, and a
reference taken before each event (or a model of the drift) is needed before single-run CPU savings can be read.
On the expected fail: the aging seen on Colab does not appear on a dedicated workstation at this n, and the remedy it
suggests (interleaved references) is for shared cloud hosts. Nothing beyond the harness and hosts.
