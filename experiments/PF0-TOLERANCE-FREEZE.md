# PF-0 tolerance freeze

**Status:** SEALED.

**Registration ID:** PF0-FREEZE-001

**Date sealed:** 2026-08-04

**Seal hash:** SHA-256 of this file's git blob at the sealing commit, recorded
in `experiments/SEALS.md`. Any edit to this file after the sealing commit
voids the seal and requires a new registration ID.

**Authorization:** sealed on the project owner's explicit instruction after
review of the draft and the gap-closure record.

Numbers below were measured during the 2026-08-03/04 shakedown (commits
8ddd321..d542851) on Atlas (MATLAB R2026a, Python 3.12.3 venv, numpy 2.5.1,
scipy 1.18.0) and NRP (`python:3.12-slim` CPU Job, namespace `ssu-atlas-ai`).
Every stated measured bound was recomputed from the committed evidence records
immediately before sealing; bounds are rounded up from measurements, never
down.

## Measured instrument performance

| Witness | Configuration | Measured | Evidence |
|---|---|---|---|
| Branch counts across creation fold | analytic control, MATLAB + Python | 0 -> 1 -> 2 exact, signed count 0 at every slice | console run + pytest |
| Separation exponent vs 1/2 | analytic control, polyfit over 6 decades | error < 1e-12 | console run (printed 0.500000000000 at 12 decimals; assert bar 1e-10) |
| Fold event location shift, MaxStep 0.01 -> 0.005 -> 0.0025 | ode45, RelTol 1e-10, AbsTol 1e-12, PF-2 toy | <= 7.0e-13 per halving; fold count 12 at all three | console run |
| \|p_t\| at located events | same | <= 4.6e-13 | console run |
| Relative energy drift, adaptive | same | <= 1.5e-12 | console run |
| Relative energy drift, manifest rows | ode45, 4 scenarios | <= 1.2e-14 | results/matlab/*.json |
| dt halving on manifest (PF2-0003 vs 0004) | ode45 MaxStep 1e-3 vs 5e-4 | identical fold count and locations printed to 10 digits | results/matlab/*.json |
| Verlet vs ode45, all 12 fold events | dt 1e-3, tau in [0,40], PF2-0002 scenario | max \|dtau\| = 1.7e-6 at the last event, growing roughly as dt^2 * tau; max \|dt\| = 1.9e-7; max \|dx\| = 3.4e-7 | results/nrp-smoke.json vs results/matlab/PF2-0002.json |
| Relative energy drift, fixed step | Verlet dt 1e-3, single + 1000-member ensemble | <= 1.3e-7 single; <= 4.3e-9 ensemble | results/atlas-verlet.json, results/atlas-ensemble.json |
| Cross-substrate determinism | same scenario, Atlas venv vs NRP container | scenario_sha256 and outcome_sha256 bit-identical | results/atlas-verlet.json, results/atlas-verlet-r2.json vs results/nrp-smoke.json |
| Ensemble fold-count dispersion | 1000 perturbed ICs, PF-2 toy | all 1000 members: exactly 12 folds | results/atlas-ensemble.json |
| N0 monotone null | polynomial instrument, both languages | 1 branch, orientation +1, 0 critical points at every slice | run_p0_instrument_net + pytest |
| P0/P1 generic slices vs quadratic reference | polynomial instrument vs branch_count / analytic_fold_branches | tau agreement < 1e-12, orientations identical | run_p0_instrument_net + pytest |
| D0 degenerate cubic | polynomial instrument | one critical point, classified degenerate, never a fold | run_p0_instrument_net + pytest |
| M0 double fold t = tau^3 - tau | polynomial instrument, both languages | band counts 1-3-3-3-1, signed count +1 at every slice, both folds at +/-1/sqrt(3) with correct types | run_p0_instrument_net + pytest |
| M0 cross-language branch locations | MATLAB vs Python, slice t = 0.2 | max difference <= 4.5e-16 | console runs |
| First-derivative residual at polynomial critical points | MATLAB, M0 control | <= 5.6e-16 | console run |

## Frozen tolerances

Each bar sits at least a factor of five above its measured value; most sit one
to seven decades above. A claim-bearing run that exceeds a bar invalidates the
instrument for that run. The bars may not be moved while this seal stands.

Adaptive path (ode45 or equivalent, RelTol 1e-10, AbsTol 1e-12, MaxStep <= 0.01):

- T1 fold event location shift under one MaxStep halving: < 1e-11
- T2 |p_t| at every located event: < 1e-11
- T3 relative energy drift over the full integration: < 1e-11
- T4 fold count under refinement: exact integer match, no tolerance
- T5 analytic controls (full N0/P0/P1/D0/M0 net): exact branch counts, signed
  count exactly as the map degree requires, separation exponent error < 1e-10,
  no degenerate point classified as a fold, non-generic slices refused

Fixed-step path (velocity Verlet, dt = 1e-3, valid for tau_max <= 40):

- T6 fold event tau agreement with the adaptive reference: < 1e-5 over the
  full range. The disagreement scales roughly as dt^2 * tau; any change of dt
  or tau_max beyond this domain voids T6 and forces a re-freeze.
- T7 relative energy drift: < 1e-6
- T8 fold count agreement with the adaptive reference: exact
- T9 same scenario on two substrates yields identical scenario_sha256 and
  outcome_sha256 when recorded dependency versions match

## Classifier constants, derived

The classifier is invoked only at located critical points, never at arbitrary
samples; the polynomial instrument refuses slices whose preimage falls within
the derivative floor of a critical point, so no regular point reaches it.

- **first_tol = 1e-9 (frozen).** Measured first-derivative residual at located
  events: <= 4.6e-13 on the adaptive path, <= 5.6e-16 at polynomial critical
  points. The tolerance sits a factor of at least 2e3 above the worst
  residual, so no true critical point can be misread as regular.
- **second_tol = 1e-8 (frozen).** Across all 71 fold events in the committed
  evidence the smallest |d^2 t / d tau^2| is 0.208; the analytic controls give
  2 (P0), 2*sqrt(3) (M0), and exactly 0 (D0). The tolerance sits a factor of
  2e7 below the smallest genuine fold curvature and at least 7 decades above
  the measured degenerate residual, so folds and degenerate points cannot
  swap.

Any claim-bearing model whose fold curvatures approach 1e-5 in the campaign
units invalidates this derivation and forces a re-freeze before use.

## Gap closure record (2026-08-04, commits 779f1c0..d542851)

1. **M0 double-fold control: closed.** Generic polynomial instrument
   (`pf.poly_branches` / `polynomial_time_branches`,
   `pf.poly_critical_points` / `polynomial_critical_points`) implemented in
   both languages; band structure, signed invariant, both fold locations and
   types verified, cross-language agreement <= 4.5e-16. Non-generic slices
   are refused by contract rather than counted.
2. **N0 monotone null: closed.** Explicit pass in both suites.
3. **Dependency versions: closed.** `run_trial.py` records numpy and scipy
   versions under `runtime.dependencies`; `gpu_ensemble.py` records
   `backend_version`. T9 re-verified under the new format against the
   original NRP record.
4. **Classifier tolerances: closed.** Derived above from measured margins and
   restated as frozen constants with an explicit invalidation condition.

Two instrument defects were found and fixed before sealing, and are preserved
here per the evidence discipline:

- `roots()` reports a repeated derivative root once per multiplicity, so the
  D0 cubic initially yielded its single degenerate critical point twice.
  Critical-point clusters within 1e-8 now collapse to their mean (commit
  1a0c65a). The Python D0 test caught this before the MATLAB net ran.
- The first draft of this document stated the Verlet-vs-ode45 event agreement
  as <= 2.4e-7 from the first three events only. The full 12-event
  recomputation gives 1.7e-6 at the last event because the fixed-step error
  grows with tau. The draft's proposed T6 bar of 1e-6 would have failed its
  own first application; T6 above is set from the full-range measurement with
  an explicit validity domain. Three other measured bounds in the first draft
  were rounded below their measurements and are corrected here (4.5e-13 ->
  4.6e-13, 1.4e-12 -> 1.5e-12, 1.1e-14 -> 1.2e-14).

## Non-claims

Nothing above bears on physics. These are instrument-validation numbers for
the kinematic layer only. The 12-fold uniformity of the ensemble illustrates
that fold counts in the toy model are set by the dynamics and the
initial-condition measure, exactly as the campaign design expects for a
negative control.
