# PF-0 tolerance freeze — DRAFT for review

**Status:** draft, unsealed, exploratory. Numbers below were measured during the
2026-08-03/04 shakedown (commits 8ddd321..3d15e92) on Atlas (MATLAB R2026a,
Python 3.12.3 venv) and NRP (`python:3.12-slim` CPU Job, `ssu-atlas-ai`).
Sealing is a human action and has not happened.

## Measured instrument performance

| Witness | Configuration | Measured | Evidence |
|---|---|---|---|
| Branch counts across creation fold | analytic control, MATLAB + Python | 0 -> 1 -> 2 exact, signed count 0 at every slice | console run + pytest |
| Separation exponent vs 1/2 | analytic control, polyfit over 6 decades | error < 1e-12 | console run |
| Fold event location shift, MaxStep 0.01 -> 0.005 -> 0.0025 | ode45, RelTol 1e-10, AbsTol 1e-12, PF-2 toy | 7.0e-13 and 4.5e-13; fold count 12 at all three | console run |
| \|p_t\| at located events | same | <= 4.5e-13 | console run |
| Relative energy drift, adaptive | same | <= 1.4e-12 | console run |
| Relative energy drift, manifest rows | ode45, 4 scenarios | <= 1.1e-14 | results/matlab/*.json |
| dt halving on manifest (PF2-0003 vs 0004) | ode45 MaxStep 1e-3 vs 5e-4 | identical fold count and locations printed to 10 digits | results/matlab/*.json |
| Verlet vs ode45 event locations | dt 1e-3, PF2-0002 scenario | <= 2.4e-7 (consistent with O(dt^2)) | results/nrp-smoke.json vs results/matlab/PF2-0002.json |
| Relative energy drift, fixed step | Verlet dt 1e-3, single + 1000-member ensemble | 1.25e-7 single; <= 4.3e-9 ensemble | results/atlas-verlet.json, results/atlas-ensemble.json |
| Cross-substrate determinism | same scenario, Atlas venv vs NRP container | outcome_sha256 bit-identical | results/atlas-verlet.json vs results/nrp-smoke.json |
| Ensemble fold-count dispersion | 1000 perturbed ICs, PF-2 toy | all 1000 members: exactly 12 folds | results/atlas-ensemble.json |

## Proposed frozen tolerances

Roughly one order of magnitude of headroom over measured values. A claim-bearing
run that exceeds a bar invalidates the instrument for that run.

Adaptive path (ode45 or equivalent, RelTol 1e-10, AbsTol 1e-12, MaxStep <= 0.01):

- T1 fold event location shift under one MaxStep halving: < 1e-11
- T2 |p_t| at every located event: < 1e-11
- T3 relative energy drift over the full integration: < 1e-11
- T4 fold count under refinement: exact integer match, no tolerance
- T5 analytic controls: exact branch counts, signed count exactly 0,
  separation exponent error < 1e-10, no degenerate point classified as a fold

Fixed-step path (velocity Verlet, dt = 1e-3):

- T6 event location agreement with the adaptive reference: < 1e-6
- T7 relative energy drift: < 1e-6
- T8 fold count agreement with the adaptive reference: exact
- T9 same scenario on two substrates yields identical outcome_sha256
  when dependency versions match

Classifier constants (both languages, already identical): first-derivative
tolerance 1e-9, second-derivative tolerance 1e-8.

## Gaps that must close before sealing

1. **M0 double-fold control is not implemented.** The control table requires
   t(tau) = tau^3 - tau with both critical points found and correctly oriented.
   Neither the MATLAB nor the Python suite exercises it yet.
2. **N0 monotone null is not explicitly run.** Trivial, but the sealed net
   must include it as a stated pass.
3. **Evidence records do not capture numpy/scipy versions.** T9 is only
   meaningful if dependency versions are recorded; add them to the runtime
   block of `run_trial.py`.
4. **Classifier tolerances (1e-9 / 1e-8) are inherited, not derived.** Either
   justify them against measured event-location error or restate them as
   conventions in the prereg.

## Non-claims

Nothing above bears on physics. These are instrument-validation numbers for the
kinematic layer only. The 12-fold uniformity of the ensemble illustrates that
fold counts in the toy model are set by the dynamics and the initial-condition
measure, exactly as the campaign design expects for a negative control.
