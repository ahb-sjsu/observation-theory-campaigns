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

- **EC-5 (ALL PASS 6/6, governed seed 20260824) — the first native seal in
  this repository** ([`PREREG-EC5-001`](PREREG-EC5-001.md), sealed
  `d77dbd9`; harness [`python/ec5_fso_consumer.py`](../python/ec5_fso_consumer.py),
  sha256 `315c5fa9…65e8d`). A physics-based FSO link consumer (Gaussian
  far-field + fiber rolloff over a hidden state→physical map), black box,
  probed with the paper §VI **belief-averaged smoothed metric**: the
  physical-loss ordering of trace-matched schedules is predicted by
  `tr(P̄_C Σ̄)` **before the run** in **94.1%** of 17 pairs (gate ≥ 80%/8);
  the charged aligned schedule beats the best agnostic by **12.5%** mean
  coupling loss (gate ≥ 4%); blind capture of the lavish reference
  **89.8%** (gate ≥ 70%). Three disclosed pilots (anti-control respecified
  to its load-bearing form from the per-policy diagnostic). The prereg
  seals the **narrowed prior-art posture** from the SPIE-targeted sweep:
  static-budget flow-down (JPL IPN 42-161, 2005), coupling-surface
  probing-for-control (nutation/SPGD), and covariance scheduling without
  FSO (Al Ahdab et al., ICML 2025) are the named nearest neighbors; the
  loose "nobody derives estimator requirements from the link" claim is
  conceded false. Scope: physics-based SIMULATED consumer — a step toward,
  not the arrival at, hardware.

- **EC-6 (ALL PASS 6/6, governed seed 20260826)** —
  ([`PREREG-EC6-001`](PREREG-EC6-001.md), sealed `e773056`; harness
  [`python/ec6_multiconsumer.py`](../python/ec6_multiconsumer.py)). **The
  multi-consumer tax exists and has the predicted angular shape**: for
  consumer pairs at controlled principal angles, the egalitarian
  best-shared-over-utopia ratio runs **1.000 / 1.037 / 1.123 / 1.149** at
  0°/30°/60°/90° — sharing exactly free when geometries coincide, a
  **14.9% tax at orthogonality** (gates: ≤1.05 at 0°, rise ≥0.05, ≥1.05 at
  90°); consumer-aware sharing beats agnostic sharing by 12.5% pooled on
  worst-of-two (gate 5%). Exploratory, reported not claimed: scalarized
  joint scheduling dominates time-sharing at every angle at this budget
  (72/80 cells). The two-observer coding theorem motivated, and was not
  imported as, the result. Two disclosed pilots.
- **EC-7 (FAIL — integrity gate, governed seed 20260828; no comparison
  claimed)** — ([`PREREG-EC7-001`](PREREG-EC7-001.md), sealed `e773056`;
  harness [`python/ec7_closedloop.py`](../python/ec7_closedloop.py)). The
  sealed predictions all passed numerically (K1 oracle-penalty vs
  iso-penalty +8.3%; K2 blind capture 1.037 — the recovered penalty beat
  the oracle pooled; K3 +7.7% vs the best hand-tuned diagonal), stability
  and boundedness passed, controls passed — **but the effort-matching
  integrity gate failed**: realized held-out efforts strayed >30% from the
  common target in 2 of 20 systems (6 arm-cells, all **common-mode** — all
  four arms drifting together, so within-system comparisons stayed
  effort-consistent; the 3-bundle matching shortcut under-powers
  per-system target transfer). Per the sealed falsification clause, **no
  comparison is claimed**, and the numerically-passing predictions are
  NOT promoted. The miss stays on the record; the successor seal
  (EC7-002: more matching bundles, and the integrity gate respecified to
  cross-arm effort spread — the fair-comparison quantity — rather than
  absolute target transfer) is the designated rehabilitation, not yet
  sealed.

- **EC7-002 (FAIL — integrity again, governed seed 20260830; no comparison
  claimed)** — ([`PREREG-EC7-002`](PREREG-EC7-002.md), sealed `3f953c4`;
  harness [`python/ec7b_closedloop.py`](../python/ec7b_closedloop.py)).
  The rehabilitation's predictions passed a second time (K1 +9.4%, K2
  capture 1.026, K3 +8.6%; every loop stable) but the respecified
  **cross-arm spread gate failed**: 0.322 vs the 0.15 band, in exactly
  **1 of 20 systems — and arm-differential this time** (oracle/blind
  efforts ≈ 0.85 near the 0.946 target while iso/hand-diag undershot to
  ≈ 0.62), so the consumer-aligned arms held an effort advantage there.
  This REFINES the v1 story: the ρ-bisection instrument's failure mode is
  not benignly common-mode — it can contaminate the comparison, which is
  precisely what the integrity gate exists to catch. Two consecutive
  instrument misses; the EC-7 claims remain **unclaimed** despite passing
  numerically in both runs. Designated successor **EC7-003**: replace
  simulation-bisection effort matching with **analytic matching** —
  expected `‖u‖²` computed exactly from the closed-loop Lyapunov
  equations, deterministic, no calibration-to-heldout transfer error at
  all (the instrument that should have been built first).

## Open

- **EC7-003** — analytic (Lyapunov) effort matching; the third and, if the
  instrument is finally right, decisive seal for Campaign 7.
- EC-5 hardware endpoint (real link; own future seal); harder cliffs (BER
  waterfalls, deep fades).
- m > 2 consumers, asymmetric priorities, layered/refined descriptions
  (EC-6 follow-on).
