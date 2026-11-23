# PREREG-FL1-003: outcome — VOID

`experiments/PREREG-FL1-003.md`, sealed at 8f5a8e6. It was run on Atlas from 2026-11-23 02:56 to 18:21 UTC, in KVM
guests under FRR's default timers, with topology-builders 69220fe (configuration loads limited to 1,800 s).
**Verdict: VOID.** Both discriminating 512-router cells deployed this time, but neither could be graded. By the
sealed stopping rule, the 1,024-router cells were not run. The law was not tested.

## What ran

| Step | Result |
|---|---|
| Gap 0 | 8 sealed files and the summary byte-identical; package hash 6342187e (69220fe), `CONFIG_TIMEOUT` present (`gap-0.log`) |
| Gap 2 | Predictions for the two 512-router files: sha256 a8cbb584...9f40; values equal FL1-002's (`gap-2.log`) |
| 512, degree 8 | Deployed. 2 of 4 runs finished before the 8 h limit (exit 124). Flood reduction off: converged at bring-up (14.6 million LSPs), but the quiet and most link windows did not settle (88,000 to 390,000 LSPs each). Flood reduction on: never converged, sending 35 to 41 million LSPs in every window. VOID: a run did not converge |
| 512, degree 16 | Deployed. The guest ran out of memory: its console logs 235 `isisd` processes killed by the kernel (about 176 MB each; 512 routers need about 90 GB against the guest's 64 GiB). One run recorded (flood reduction off, 410 million LSPs at bring-up, not converged), then `measure` stopped on a reporting error (below). VOID |
| Gap 3 | Discriminating cells graded: 0; FL1_VERDICT VOID; 1,024 not run (`gap-3.log`, `queue.log`) |

I4 holds on the three records (all in the test setup). The `-16657.8%` that the grade script prints for degree 8 is
the ratio of a non-converged storm to a converged run, not a saving.

## What this says about the test, and what it does not

The two discriminating cells failed for capacity, not for the law. At 512 routers and these densities, a guest of 16
vCPUs and 64 GiB on this host cannot hold the experiment:

- At degree 8 the network with flood reduction on stormed. Without it, the network converged but stayed busy.
- At degree 16 the routers did not fit in memory.

The 1,024-router cells would need more of both.

The degree-8 storm is a lead in its own right: flood reduction on, a network that converges without it never did.
This is one run on a CPU-starved machine. It is not established, and needs repeating with more CPU before it is
reported as a property of the implementation.

The reporting error: `measure` writes each record before printing its one-line summary. When a quiet window has no
CPU reading (routers dead), the summary line raised `KeyError: 'cpu_ms'` and the job ended. The record was already
written; nothing was lost.

## Files

| File | What it is |
|---|---|
| `queue.log`, `gap-0.log`, `gap-2.log`, `gap-3.log` | The queue's log and its gap steps |
| `fl1-003-predictions-n512.json` | The predictions written in gap 2 |
| `fl13-n512-d8.jsonl.gz` | The two finished runs of the degree-8 cell |
| `fl13-n512-d16.jsonl.gz` | The one run of the degree-16 cell |
| `fl13-n512-d8-*.log`, `fl13-n512-d16-*.log` | The guests' job logs and the runner's logs |

To regrade, from `analysis/flooding`:

```
python fl1_grade.py fl1-003/fl1-003-predictions-n512.json -- fl1-003/fl13-n512-d8.jsonl.gz fl1-003/fl13-n512-d16.jsonl.gz
python fl1_setup_check.py calibration/fl1-calibration.csv calibration/fl1-calibration.json -- fl1-003/fl13-n512-d8.jsonl.gz fl1-003/fl13-n512-d16.jsonl.gz
```
