# PREREG-FL2-001 — FL-2: the quiet-window reference ages within a run

**Status:** DRAFT, unsealed. Harness written (`analysis/flooding/fl2_baseline_age.py`); pilot runs in the queue's
gap before the 512-router labs on every profiled run so far; bars PENDING that pilot (power before bars). Seal =
commit + `SEALS.md` row, "Authorized by: A. H. Bond (session instruction)", before the first 1,024-router lab
starts.

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
where e_j = |net-of-quiet CPU of `send_hello_cb`| in the j-th link-down window, summed over the routers.

`send_hello_cb` sends one hello per interface per second whatever the event, so its net figure should be zero up to
noise; its size measures how far the host's background has moved since the reference. Under a fixed-noise
reference, E|e_j| is the same for every j and the sign test sits at chance; under an aging reference it grows with j.

## Design

- **Pilot (seen):** every profiled run in `results/` (`seeds-n64`, `random-regular-n128`, `fat-tree`, `nfly`,
  `colab-sessions` and its Atlas run with the Colab links) and the 256-router run, per dataset and pooled, written
  by the gap step to `fl2-pilot.txt`. The bars below are set from it, before the seal.
- **Test (unseen):** every run of the 1,024- and 2,048-router labs with at least two link-down windows carrying
  per-handler figures. Run as queued: three links per run, so three link-down windows, the last about 3 minutes
  after the first.
- **Secondary:** link-up windows (a link coming up changes the hello work at its two ends, so they are secondary);
  the same statistic per size, per degree and per variant; the ratio mean(e_last) / mean(e_first).

## Disclosed calibration pilot

PENDING: `fl2-pilot.txt` from the gap step, verbatim, before the seal.

```yaml
id: PREREG-FL2-001
date: 2026-11-21
retrospective: false
status: draft
kind: within-run aging of a single quiet-window CPU reference in a network-emulation harness (topology-builders
      measure, --profile), read through a handler whose work does not depend on the event
harness: analysis/flooding/{fl_common,fl2_baseline_age}.py
code_hash: PENDING (sha256 of the two files at the sealing commit)
handler: send_hello_cb
sealed_gates:
  G1: one-sided sign test of D > 0 over the test runs, p <= alpha (alpha PENDING PILOT; 0.05 unless the pilot
      shows the test cannot reach it at the expected run count)
  G2: mean(e_last) / mean(e_first) >= r_min over the test runs (r_min PENDING PILOT)
  I1: integrity - every test run's link windows carry per-handler figures, and send_hello_cb appears in all of them
  I2: integrity - the quiet window of every test run is satisfied (no LSP sent, no router's LSPs changed)
  on I1-I2 failure for a run, that run is left out and counted; if fewer than 12 runs remain, VOID
verdict: PASS iff G1 and G2; FAIL otherwise, unless VOID
stopping: fixed: the queued runs; no reruns
falsification: G1 or G2 fail -> the single reference does not measurably age within a run on this host; its error
  is fixed noise, and a longer quiet window, not an interleaved one, is the remedy; reported at equal prominence
secondary (cannot rescue the verdict): link-up windows; per-size, per-degree and per-variant splits; the effect on
  the net isisd CPU of a link change
amendments: []
```

## Scope and non-claims

One harness, one host (Atlas, routers on 20 pinned CPUs, other load as recorded in each queue's `hostload.log`), the
namespace backend, three link-down windows per run. A pass says the reference ages on this host over a few
minutes; it does not say why (other jobs, thermal state, the routers' own timers), and it says nothing about FRR or
flood reduction. A fail does not show the CPU savings are sound; only that their noise is not mostly age.

## Interpretation ceiling

On pass: in this harness, one quiet window per run is a stale reference for the windows that follow it, and a
reference taken before each event (or a model of the drift) is needed before single-run CPU savings can be read;
that is the measurement change it would license. Nothing beyond the harness and host.
