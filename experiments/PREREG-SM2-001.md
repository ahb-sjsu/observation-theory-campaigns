# PREREG-SM2-001 — SM-2: OT-derived consumer-relative value beats hand-tuned fixed-priority (Q-RAM) scheduling at matched time

**Status:** DRAFT — calibration complete, READY TO SEAL. Harness frozen
(`code_hash` below), two disclosed calibration pilots run and recorded. Remaining
soft item: quote-verify the Kreucher and Q-RAM citations against the records
(see `SENSOR-MANAGEMENT-TRACK.md`). Seal = commit + `SEALS.md` row, "Authorized
by: A. H. Bond (session instruction)", then the single governed run at
`governed_seed`.

## Anchor discipline (read first)

Two things are prior art and are NOT claimed here. (a) Task/consumer-driven
scheduling beats information-driven scheduling on the decision metric — Kreucher,
Hero & Kastella, CDC 2005; that is SM-1's anchor, not SM-2's. (b) Adaptive /
cognitive scheduling beats fixed-revisit scheduling — known in cognitive radar
resource management. SM-2 claims NEITHER. Q-RAM (Rajkumar et al., RTSS 1997) and
threat-weighted multifunction-radar RRM leave one thing open: WHERE the task
priorities come from — they are hand-set (range, velocity, threat, fuzzy logic).
The SM-2 contribution is that the OT consumer-projection `P_C` — the SAME object
used in the estimation/DR/DB/LM tracks — DERIVES a scheduling value
`tr(P_C ΔΣ)/dwell` that, with no per-task tuning, matches or beats fixed
priorities tuned per-scenario with hindsight. Novelty is the DERIVATION (the
general object that generates the adaptive schedule), evidence for the OT
unification — not "adaptive beats fixed," and not superiority over an
adaptive/cognitive RRM scheduler (a stronger policy class that would itself need
a scheduling objective, which is exactly what `P_C` supplies).

## Claim under test

On the SM-2 dynamic-clutter aperture ensemble, at matched total time budget, OT
scheduling on the derived value `tr(P_C ΔΣ)/dwell` (no per-task tuning) achieves
a joint-success rate — trigger caught within the 30 ms reaction deadline AND
doorway occupancy called correctly — at least as high as the best fixed-priority
(Q-RAM-style) revisit tuning selected per-scenario from a grid with hindsight;
AND every single fixed tuning is individually brittle (at least one fails the
joint objective, and the fixed tunings trade trigger-timeliness against imaging
so no one tuning is best on both); the brittleness is the predicted intra-trial
time-varying-optimum mechanism (confirm the still occupant early, then guard the
trigger). On pass, class `[measured]`: the consumer-relative projection derives
the adaptive schedule that fixed priorities cannot reach, without hindsight.

## Design

Harness `matlab/sm2_aperture_qram.m`, governed mode, deterministic under
`rng(governed_seed)`. Tick-based matched-TIME budget: 0.5 ms tick, 400 ms budget
(800 ticks), 30 ms deadline (60 ticks). State evolves per tick; a chosen mode
occupies `dwell/tick` ticks and blocks the aperture (so a 10 ms long imaging
dwell costs 20 ticks). Common random numbers across policies (shared clutter
realization and measurement-noise draws per scenario), so the comparison is
exact. Scene ensemble per trial: 5 cells with random motion types
(empty/moving/still), doorway still-occupied w.p. 0.6 else empty, trigger jump
at a random tick, 2-state platform-motion clutter. Imaging is clutter-limited
(still occupant needs long dwell in low clutter; measurement noise `∝ 1/dwell`,
`×clutter` for still targets). Modes: image-cell-i short (1 ms) / long (10 ms),
listen-trigger (0.5 ms), DF (1 ms).

Policies: OT (`argmax` reduction in `tr(P_C Σ)` per unit dwell); three
representative hand-tuned fixed-priority revisit schedulers (trigger-heavy,
balanced, imaging-heavy); and a fair hindsight ORACLE = best-per-scenario over a
15-point grid of fixed revisit tunings (trigger-revisit × doorway-revisit).
Q-RAM scheduler = urgency `(ticks_since_service)/revisit_interval`, serve the
most-urgent task, doorway served with the long dwell.

Structural null (stated, not measured): on a HOMOGENEOUS ensemble (a single
scenario type), a single fixed tuning tuned to it matches OT — the OT advantage
comes from ensemble heterogeneity, and vanishes as the ensemble collapses to one
scenario.

## Disclosed calibration pilot (exploratory; re-run from the frozen harness before seal)

Seed 20260830, 400 MC, matched 400 ms, CRN across policies:

| Policy | joint OK | trig<30 ms | doorway correct |
|---|---|---|---|
| OT (derived, untuned) | 99.0% | 99.8% | 99.2% |
| Q-RAM trigger-heavy (fixed) | 94.8% | 97.8% | 97.0% |
| Q-RAM balanced (fixed) | 92.5% | 95.2% | 97.2% |
| Q-RAM imaging-heavy (fixed) | 77.2% | 79.2% | 97.0% |
| Q-RAM oracle (best of 15-grid, hindsight) | 95.2% | 97.0% | 98.2% |

Trigger-rate spread across the three fixed tunings: 97.8 → 79.2 = 18.6 pts (the
trade-off is real).

**Second disclosed pilot** (seed 20260901, frozen harness, 400 MC):

| Policy | joint OK | trig<30 ms | doorway correct |
|---|---|---|---|
| OT (derived, untuned) | 99.0% | 100.0% | 99.0% |
| Q-RAM trigger-heavy (fixed) | 96.2% | 98.0% | 98.0% |
| Q-RAM balanced (fixed) | 93.8% | 95.5% | 97.8% |
| Q-RAM imaging-heavy (fixed) | 75.0% | 76.8% | 97.8% |
| Q-RAM oracle (best of 15-grid, hindsight) | 95.5% | 97.0% | 98.2% |

Both draws agree: OT joint 99.0%/99.0% beats the hindsight grid oracle
95.2%/95.5% (G1 margin +3.8/+3.5 pts); imaging-heavy is brittle 77.2%/75.0%
(G2); trigger-rate spread 18.6/21.2 pts (G3). All gates hold across both draws
with margin; bars are set below the two-draw minimums.

```yaml
id: PREREG-SM2-001
date: 2026-08-30
retrospective: false
status: ready-to-seal
kind: OT-derived consumer-relative value vs hand-tuned fixed-priority
      (Q-RAM-style) revisit scheduling at matched time (SM-2); dynamic-clutter
      aperture ensemble, CRN across policies, joint reaction-deadline +
      still-occupant objective
harness: matlab/sm2_aperture_qram.m (seed-parameterized; default 20260830)
code_hash: sha256:c3f0775dc75a3912f139afc6479faecdfa7cd676dd03c5933881a059145cadaf
imports_sealed: none (self-contained)
governed_seed: 20261202
calibration_seeds: [20260830, 20260901]
frozen_config:
  tick_ms: 0.5
  budget_ms: 400
  deadline_ms: 30
  n_mc: 400
  scene: {doorway_still_prob: 0.6, motion_types: [empty, moving, still]}
  clutter_states: [1, 4]
  dwell_ms: {short: 1, long: 10, listen: 0.5, df: 1}
  P_C_weights: {trigger: 6, doorway: 4, other_cell: 0.1, device: 0.3}
  occ_gate: {mean: 0.5, var: 0.08}
  display_tunings_rev_ticks:
    trigger_heavy: [6, 60, 40, 80]
    balanced:      [20, 40, 40, 60]
    imaging_heavy: [50, 24, 30, 80]
  oracle_grid: {trigger_rev: [6,12,20,30,50], doorway_rev: [24,40,60],
                cell_rev: 40, df_rev: 70}
sealed_gates:
  G1: primary - OT joint-success minus hindsight grid-oracle joint-success
      >= -0.01 (OT matches or beats the best fixed tuning selected per
      scenario with hindsight; pilot +0.038)
  G2: brittleness - min joint-success over the three display tunings
      <= 0.85 (no single fixed tuning is safe to deploy; pilot 0.772)
  G3: trade-off - trigger-within-deadline spread across the three display
      tunings >= 0.10 (fixed tunings genuinely trade trigger vs imaging;
      pilot 0.186)
  I1: integrity - all policies run to the same total time budget within
      1 tick; on failure NO comparison gate is interpreted
  I2: integrity - CRN identity: OT and Q-RAM see the same per-scenario
      clutter + noise draws; verified by construction, asserted at run
  I3: integrity - half-sample split of G1 agrees to <= 0.03
stopping: fixed-n, single governed run after the sealing commit
falsification: G1 fail -> the derived value does NOT recover hindsight-tuned
  fixed scheduling; consumer geometry is not sufficient to schedule without
  tuning; reported as the boundary answer regardless of sign. G2 fail ->
  fixed tunings are NOT brittle here (one tuning suffices); the "derivation
  matters" motivation collapses. G3 fail -> no real trigger/imaging
  trade-off; the intra-trial time-varying-optimum mechanism is wrong.
  I1/I2/I3 fail -> instrument integrity broken, no comparison claimed
  (EC-7 discipline). All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Linear-Gaussian; clutter as a 2-state platform-motion process modulating imaging
noise (not a full range-Doppler cancellation sim); myopic per-decision OT greedy.
The comparison is OT vs HAND-TUNED FIXED priorities ONLY. No claim over adaptive
/ cognitive RRM (a stronger policy class); the point is that OT SUPPLIES the
objective such a scheduler would need, from the consumer geometry. No optimality
claim for OT (it is a myopic rate-normalized heuristic). No claim that consumer-
relative scheduling, or adaptive-beats-fixed, is novel — see the anchor. The
`P_C` weights encode the consumer/decision cost (the objective specification),
not a scheduler tuning; that is the asymmetry with Q-RAM, which needs BOTH the
cost AND a per-task priority tuning.

## Interpretation ceiling

On pass: in this idealized heterogeneous ensemble, the OT consumer-projection
derives an aperture schedule that matches or beats fixed priorities tuned per
scenario with hindsight, without per-task tuning — evidence that the same `P_C`
object generalizes from estimation/DR/DB/LM to sensor management (the Paper VIII
unification). This does NOT establish fielded performance, nor superiority over
an adaptive/cognitive RRM scheduler, nor that the myopic OT rule is optimal.
