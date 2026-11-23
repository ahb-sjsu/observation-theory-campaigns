# PREREG-FL1-002: outcome — VOID

`experiments/PREREG-FL1-002.md`, sealed at 62c255d. It was run on Atlas from 2026-11-22 20:43 to 2026-11-23 00:45
UTC, in KVM guests under FRR's default timers. **Verdict: VOID.** Neither discriminating cell (512 routers, degree 8
and 16) could be graded, because both failed at deployment. By the sealed stopping rule, the 1,024-router cells were
not run. The setup gates passed. The law was not tested.

## What ran

| Step | Result |
|---|---|
| Gap 0 | 8 sealed files and the calibration summary byte-identical (`gap-0.log`) |
| I3 labs | 256 routers, degree 4 and 8: 4 runs each, all converged |
| Gap 1 | I4 PASS (8 records, all in the test setup); I3 PASS: degree 4 6.12% against the calibration's 8.55% (-2.43 points), degree 8 12.51% against 14.53% (-2.02); bar 8.56 (`gap-1.log`) |
| Gap 2 | Predictions for 512 routers written before their labs: sha256 40094c25...39f9; values equal those of 2026-11-21 (`gap-2.log`) |
| 512, degree 4 | 4 runs, converged; measured 10.5% (m-law 7.0%, d-law 12.4%); not discriminating |
| 512, degree 8 | VOID: deployment failed, no run (`fl1-n512-d8-job.log`) |
| 512, degree 16 | VOID: deployment failed, no run (`fl1-n512-d16-job.log`) |
| Gap 3 | Discriminating cells graded: 0; FL1_VERDICT VOID; 1,024 not run (`gap-3.log`, `queue.log`) |

## Why the two cells failed

The lab harness starts every router's daemons, then loads each router's configuration in turn (`vtysh -b`) with a
120 s limit. Routers configured earlier are already flooding. At 512 routers on 16 vCPUs, the load of router r507
(degree 8) and of r359 (degree 16) exceeded the limit, and `measure` stopped before the first run. This is a limit
of the harness, independent of what was to be measured. The cells are VOID by the registration's rule: "a cell lost
to memory or time is VOID; no reruns".

topology-builders a68e77b gives that one call a 30-minute limit. A successor registration names that change.

## Seen after the seal (secondary, cannot change the verdict)

- 512 routers, degree 4: 10.5%, against the m-law's 7.0% and the d-law's 12.4% (above).
- 256 routers, degree 16, FRR's defaults, in a guest (topology-builders ops block, `results/operator-timers`):
  measured 23.0% at m = 1.5025. The m-law gives 37.9%, 14.9 points above and outside the bar; the d-law gives 74.7%.

## Files

| File | What it is |
|---|---|
| `queue.log`, `queue-1.log` | The test queue's log, and its first start, aborted before any lab by the ISP outage's STOP |
| `gap-0.log` to `gap-3.log` | The gap steps' output |
| `fl1-002-predictions-n512.json` | The predictions written in gap 2 |
| `fl1-n256-d4.jsonl.gz`, `fl1-n256-d8.jsonl.gz` | The I3 records |
| `fl1-n512-d4.jsonl.gz` | The one graded test cell's records |
| `fl1-n512-d8-*.log`, `fl1-n512-d16-*.log` | The guests' job logs, with the timeout, and the runner's logs |

To regrade, from `analysis/flooding`:

```
python fl1_setup_check.py calibration/fl1-calibration.csv calibration/fl1-calibration.json \
    1a2908911122d79cf5173f42cdee12122b85a036a98b9119aaec2550988fffac \
    c2def38b865218ce25cffd57389824e3a774195c02f08b8f9506c1b648a6a7f3 -- fl1-002/fl1-n256-d4.jsonl.gz fl1-002/fl1-n256-d8.jsonl.gz
python fl1_grade.py fl1-002/fl1-002-predictions-n512.json -- fl1-002/fl1-n512-d4.jsonl.gz
```
