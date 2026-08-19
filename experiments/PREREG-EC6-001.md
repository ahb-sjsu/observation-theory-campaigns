# PREREG-EC6-001 — EC-6: multi-consumer state service (OT-EC Campaign 6)

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

Campaign 6 of the OT-EC paper (Paper VIII §XI): when can one sensor
schedule serve two consumers, and when does their operational geometry
force a **multi-consumer tax**? Two planted rank-3 linear consumers whose
read subspaces sit at a controlled principal angle φ ∈ {0°, 30°, 60°, 90°}
(all three principal angles equal φ by construction; same within-subspace
weights, so the angle is the only contrast). The two-observer coding
theorem motivates the shape (nesting → free sharing; incompatibility →
tax) but is **not imported as a result** — per the paper's own scope rule,
the campaign measures whether the dynamic analogue exists.

The tax at angle φ is the egalitarian service ratio
`tax(φ) = W_best-shared / W_utopia`, with `W = max(loss_1, loss_2)`,
`W_utopia = max(loss_1(ded-1), loss_2(ded-2))` — each consumer's outcome
with the WHOLE budget to itself, infeasible for both at once, so the ratio
prices the sharing.

## Design

Machinery from the sealed `blind_scheduling.py` (unmodified). Random stable
LTI (d=12), 30-sensor pool, k=3, T=60, Kalman filter, common random numbers.
Per system, the SAME pair-construction randomness at every angle (only φ
varies). Policies at one matched budget: `joint` (greedy on the scalarized
(P₁+P₂)/2), `split` (time-sharing: odd steps on P₁, even on P₂),
`dedicated-1/2` (utopia references), `iso`, `random`. No probing (planted
consumers; recovery was Campaign 3's question).

## Two disclosed calibration pilots (design fixes only; no sealed bar existed)

1. **Pilot 1** (tax 1.000/1.019/1.062/1.095 monotone — the predicted shape
   at first light — but two mis-specified checks): (a) M4 as a per-cell
   win fraction (0.844) is brittle near ties; respecified as the pooled
   mean relative W improvement, the stable form used throughout the EC
   campaigns; (b) the dedicated-sanity control assumed greedy dominance
   (dedicated-greedy ≥ joint-greedy per cell), which is not a theorem —
   greedy is suboptimal and can be beaten on its own consumer; respecified
   pooled.
2. **Pilot 2** (identical tax curve; M4 pooled 0.126; both controls True):
   corrected design confirmed; frozen.

```yaml
id: PREREG-EC6-001
date: 2026-08-19
retrospective: false
kind: multi-consumer tax vs read-subspace angle (Campaign 6, OT-EC paper);
      planted consumer pairs at controlled principal angles, no recovery
harness: python/ec6_multiconsumer.py
code_hash: sha256:af1ff6b921a2e098b8c7f74d92e322f38e45387f28a727a292e680a07835c5a3
governed_seed: 20260826
calibration_seed: 20260825
frozen_config:
  N_sys: 20
  angles_deg: [0, 30, 60, 90]
  m1_band: 0.05     # M1 gate: tax(0) <= 1.05 (cal 1.0000 exactly)
  m2_gap: 0.05      # M2 gate: tax(90)-tax(0) >= 0.05 (cal 0.0950)
  m3_tax: 0.05      # M3 gate: tax(90) >= 1.05 (cal 1.0950)
  m4_impr: 0.05     # M4 gate: pooled rel W improvement of best-shared
                    #          over iso >= 0.05 (cal 0.126)
internal_calibration:
  pilot2: {tax: {0: 1.0000, 30: 1.0193, 60: 1.0618, 90: 1.0950},
           M4_pooled: 0.126, M4_frac: 0.844,
           joint_vs_split_wins: {0: 8, 30: 6, 60: 7, 90: 8},
           ded_sane_pooled: true, random_worst: true}
sealed_predictions:
  M1: sharing near-free when aligned — tax(0) <= 1.05
  M2: the tax rises with angle — tax(90) - tax(0) >= 0.05
  M3: a genuine tax at orthogonality — tax(90) >= 1.05
  M4: consumer-aware sharing beats agnostic sharing — pooled mean relative
      W improvement of best-shared over iso >= 0.05
exploratory_not_gated: the joint-vs-split crossover by angle (the
  observable where a dynamic analogue of observer complementarity would
  show; calibration shows scalarization dominating time-sharing at every
  angle at this budget — reported, not claimed)
controls: [dedicated-utopia sane pooled per consumer, random worst on W]
stopping: fixed-n, single governed run
falsification: M1 fail -> sharing costs even when geometries coincide (the
  tax is not geometric). M2/M3 fail -> no dynamic analogue of observer
  incompatibility at these angles — the coding-theorem intuition does NOT
  transfer to schedules, reported as the campaign's answer. M4 fail ->
  consumer-aware sharing adds nothing over agnostic sharing. All reported
  at equal prominence.
amendments: []
```

## Scope and non-claims

Two consumers, equal weights, symmetric budgets, egalitarian endpoint;
m > 2 consumers, asymmetric weights/priorities, and layered/refined state
descriptions (the successive-refinement analogue proper) are follow-on. No
optimality claim for greedy; no claim that the coding-theorem nesting
condition governs the dynamic tax — only that a tax with the predicted
angular shape exists.
