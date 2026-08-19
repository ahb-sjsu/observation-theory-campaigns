# 🎯 EC — Estimation & Control track

**Question in one line.** Does a downstream consumer's read geometry
`P_C = JᵀGJ`, recovered from the consumer itself by query-only probing and
composed with a Kalman covariance as `tr(P_C Σ)`, allocate estimation and
communication resources better than reconstruction-based allocation — at
matched budgets that include the cost of probing?

This is the estimation-and-control face of Observation Theory: the paper is
**Paper VIII** of the geometric series
([`ot-estimation-control.tex`](https://github.com/ahb-sjsu/geometric-observation/blob/master/paper/ot-estimation-control.tex),
in `geometric-observation`), organized as three interfaces — estimator
geometry (state-dependent `P_C(x)` moves the optimum off the posterior
mean), resource value (`tr(P_C ΔΣ)`), and dynamic relevance (`S_C(Δ)`,
conjectural). The boundary results (weighted posterior-mean invariance;
the rank-one value-of-observation identity) are machine-checked in
Lean 4/Mathlib in `geometric-observation/lean/`.

## Provenance — migration from geometric-observation, 2026-08-19

Campaigns EC-2/3/4 were designed, sealed, and run in the
`geometric-observation` repository under its GO-P-2026 prediction registry,
then migrated here (session instruction, 2026-08-19) when the campaigns
outgrew that repository's paper-evidence scope. **The binding registration
timestamps are the ORIGINAL sealing commits in `geometric-observation`**,
listed below and permanently verifiable there; the files here are
byte-identical copies (the harness SHA-256s below equal the `code_hash`
fields inside the sealed preregs). `geometric-observation`'s registry
accounting retains rows 087–089 marked as migrated, so its no-file-drawer
argument is unbroken.

| Campaign | Prereg (here) | Original seal (geometric-observation) | Harness (here) | Harness SHA-256 |
|---|---|---|---|---|
| EC-3 flagship: blind recovery → scheduling | [`GO-P-2026-087`](GO-P-2026-087-blind-recovery-scheduling.md) | `63a6f56` (2026-08-18) | [`python/blind_scheduling.py`](../python/blind_scheduling.py) | `c71f47a8…f76b08` |
| EC-2: the consumer-relative flip in sensing | [`GO-P-2026-088`](GO-P-2026-088-consumer-flip-sensing.md) | `705f068` + amendment `7e68dba` (2026-08-19) | [`python/consumer_flip_sensing.py`](../python/consumer_flip_sensing.py) | `c80c0644…c0e62e9` |
| EC-4: operational event triggering | [`GO-P-2026-089`](GO-P-2026-089-operational-trigger.md) | `705f068` (2026-08-19) | [`python/operational_trigger.py`](../python/operational_trigger.py) | `004192a6…c590ec` |

## What the track has established (all single sealed governed runs, class `[predicted]`)

- **EC-3 (ALL PASS 5/5, governed seed 20260819).** The conjunction the
  prior-art sweep left open, in its first instantiation: query-only
  finite-difference recovery of `P̂_C`, composed with the Kalman covariance,
  schedules sensors that improve the held-out consumer at matched budgets
  **with probe cost charged** — capturing **94.6%** of the known analytic
  optimum's gain on the positive-control arm (gate ≥ 75%: recover/match,
  not beat), winning **+16.3%** over the best consumer-agnostic policy on
  black-box consumers (gate ≥ 8%), with trace-matched ordering carried by
  the composition in **86.9%** of 61 pairs (gate ≥ 65%). Five disclosed
  calibration pilots (transient-loaded charging, prior-inconsistent x₀,
  noise-dominated comparisons → common random numbers, per-use charging).
- **EC-2 (ALL PASS 6/6, governed seed 20260821).** The
  reconstruction-matched flip transfers from codes to **sensor schedules**:
  full two-consumer verdict inversion in **100%** of trace-matched systems
  (gate ≥ 80%), `tr(P_i Σ̄)` predicts the ordering in **100%** of cells
  (gate ≥ 85%), mean relative consumer gap **31.8%** (gate ≥ 10%). Two
  gates passed exactly at their bars (noted, not hidden). One dated
  amendment: governed invocation 1 completed its measurement and crashed in
  JSON serialization; evidence logs committed
  (`results/GO88-governed-invocation1-*.log`); invocation 2 reproduced
  invocation 1 line-for-line, as the amendment required.
- **EC-4 (ALL PASS 6/6, governed seed 20260822).** Signal-aware operational
  triggering (`eᵀP_C e > τ` on the realized gap) beats periodic/isotropic
  triggers by **20.0% / 33.3%** at matched realized transmission budgets
  (gate ≥ 10% both arms); the probe-charged blind trigger captures
  **86.9%** of the true-operator advantage (gate ≥ 75%). Pilot 1 is a
  **registered null finding**: covariance-only threshold triggers collapse
  to quasi-periodic schedules — direction matters to WHEN only through the
  realized error, so the operational trigger must be signal- or
  belief-aware.

Verification: `python python/verify_ec_gates.py` re-derives every gate and
the EC-3 headline metrics from the committed result JSONs (no re-run; the
sealed seeds make the runs deterministic).

## Open

- **EC-5 — physical consumer** (free-space-optical link geometry pulled
  back into the navigation estimator; the belief-averaged read operator is
  load-bearing because the endpoints are threshold-like). A SPIE-targeted
  prior-art pass on the pointing-acquisition-tracking literature gates any
  gap assertion. Next to be sealed, in this repository under this track.
- EC-6 multi-consumer state service; EC-7 closed-loop control — per the
  paper's campaign section.
