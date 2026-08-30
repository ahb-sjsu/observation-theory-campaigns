# PREREG-SM1-001 — SM-1: consumer-relative aperture scheduling beats information-greedy at matched time

**Status:** DRAFT — calibration complete, READY TO SEAL. Harness frozen
(`code_hash` below), two disclosed calibration pilots run and recorded,
prior-art anchored. Seal = commit + `SEALS.md` row, "Authorized by: A. H. Bond
(session instruction)", then the single governed run at `governed_seed`.

## Anchor discipline (read first)

This is NOT a claim that consumer-relative scheduling is a new idea. Task-driven
/ decision-focused sensor management and threat/priority-weighted multifunction
radar resource management are established (see `SENSOR-MANAGEMENT-TRACK.md`
prior-art recon; quote-verify before seal). Weighting the covariance by a
relevance matrix and scheduling on `tr(P_C Σ)` is a covariance-based resource
management approach. The sealed contribution is a **measurement**: on a realistic
multifunction aperture in a clutter-limited regime where the decision-critical
channel is *low-uncertainty*, honest information-greedy scheduling
**structurally** neglects that channel and misses a counter-RCIED reaction
deadline, while consumer-relative (OT) scheduling meets it at matched time; and
the OT framework unifies this with the estimation/DR/DB consumer tracks. Novelty
is the quantified conjunction + the unification, not "OT is best."

## Claim under test

On the SM-1 dynamic-clutter aperture model, at matched total time budget, OT
consumer-relative scheduling (`min tr(P_C Σ_post)`) beats BOTH honest
information-greedy scheduling (trace-greedy `min tr Σ_post` and MI/log-det-greedy
`min log det Σ_post`) AND fair round-robin on the two decision-critical
outcomes — trigger detection within a 30 ms reaction deadline, and stationary
doorway-occupant detection — and does so with the predicted STRUCTURE:
(a) MI-greedy structurally never attends the low-uncertainty trigger channel
(near-total deadline miss); (b) under the clutter dwell-tension, fair
round-robin fails the reaction deadline while OT meets it; (c) OT alone clears
both outcomes at the lowest decision cost. On pass, class `[measured]`: on this
model, consumer-relevance is the load-bearing scheduling variable for the
reaction deadline.

## Design

Harness `matlab/sm1_aperture_clutter.m` (governed mode; deterministic under
`rng(governed_seed)`). Linear-Gaussian sensor management, one aperture
allocation per frame at matched TIME budget. State = 5 scene-cell occupancy
latents (persistent; doorway = decision-relevant) + trigger channel (rare jump
= a command sent) + 2 device bearings. Modes: image-cell-i short (1 ms) / long
(10 ms), listen-trigger (0.5 ms), DF (1 ms). Through-wall imaging is
clutter-limited: a moving/empty cell separates in Doppler (cheap), a still
occupant is buried in the clutter residue (needs long dwell), platform motion is
a 2-state process raising the clutter floor. Scheduler plans with a known-clutter
worst-case (still-target) noise model and receives the true motion-dependent
noise on measuring. Consumer relevance `P_C = diag`, trigger 6×, doorway 4×.

Structural null (stated, not measured): for an isotropic consumer `P_C = I`, OT
scheduling IS trace-greedy — the advantage vanishes identically by construction.

## Disclosed calibration pilots (exploratory; to be re-run from the frozen harness)

Exploratory MATLAB run, seed 20260830, 500 MC, 240 frames, 30 ms deadline:

| Policy | decJ | trig<30 ms | trig miss | still-occ det | door FA |
|---|---|---|---|---|---|
| OT | 0.627 | 95.8% | 4.0% | 100% | 2.1% |
| Trace-greedy | 0.853 | 86.2% | 13.8% | 95.0% | 0.0% |
| Round-robin | 1.159 | 36.0% | 22.8% | 100% | 5.4% |
| MI / log-det | 5.389 | 0.0% | 100% | 0.0% | 0.0% |

Two disclosed modeling fixes during the pilot (both in the record): empty-room
occupancy prior (an initial coin-flip prior gave 48% false alarms); persistent
occupancy latent (an initial diffusing state let "empty" cells drift to look
occupied). The schedule and decision cost are covariance-driven and did not
depend on either fix; only the detection metric did.

**Second disclosed pilot** (seed 20260901, frozen harness, 500 MC):

| Policy | decJ | trig<30 ms | trig miss | still-occ det | door FA |
|---|---|---|---|---|---|
| OT | 0.629 | 94.6% | 5.2% | 99.7% | 1.1% |
| Trace-greedy | 0.850 | 89.8% | 9.8% | 96.9% | 0.0% |
| Round-robin | 1.161 | 38.6% | 20.8% | 100% | 5.0% |
| MI / log-det | 5.389 | 0.0% | 100% | 0.0% | 0.0% |

Across-draw reading (the load-bearing bars): the structural gates are robust —
MI structurally misses (0%/0%), round-robin fails the deadline under clutter
(36%/39%), OT clears both outcomes both draws. G1 (OT-over-trace margin) is the
NARROW one: +9.6 pts (pilot 1) and +4.8 pts (pilot 2); trace-greedy is a
stronger honest baseline than pilot 1 suggested, so the G1 bar is set BELOW the
two-draw minimum (+0.03 < +0.048) per the 088 lesson, and G1 is a SUPPORTING
gate — the structural core is G4 (info-max misses entirely) and G5 (fair
scheduling fails under clutter).

```yaml
id: PREREG-SM1-001
date: 2026-08-30
retrospective: false
status: ready-to-seal
kind: consumer-relative vs information-greedy vs round-robin aperture
      sensor scheduling at matched time budget (SM-1); dynamic-clutter
      through-wall model with a counter-RCIED reaction deadline
harness: matlab/sm1_aperture_clutter.m (seed-parameterized; default 20260830)
code_hash: sha256:717e3b63aeefb0962d950fd540e594f2e0431f29b7a6bff6526e657fd6f23e52
governed_seed: 20261201
calibration_seeds: [20260830, 20260901]
frozen_config:
  n_mc: 500
  t_frames: 240
  deadline_ms: 30
  clutter_states: [1, 4]
  clutter_switch_prob: 0.03
  dwell_ms: {short: 1, long: 10, listen: 0.5, df: 1}
  P_C_weights: {trigger: 6, doorway: 4, other_cell: 0.1, device: 0.3}
  occ_gate: {mean: 0.5, var: 0.08}
sealed_gates:
  G1: SUPPORTING - OT trigger-within-deadline rate minus best info-greedy
      (trace) rate >= +0.03 (pilots +0.096 / +0.048; bar set below the
      two-draw minimum per the 088 lesson; the structural core is G4+G5)
  G2: OT still-occupant detection >= 0.95 AND door false-alarm <= 0.05
      (pilot 1.00 / 0.021)
  G3: OT decision cost strictly below every baseline (pilot 0.627 < 0.853)
  G4: structure - MI/log-det trigger-within-deadline <= 0.20, i.e. info
      maximization structurally neglects the critical channel (pilot 0.00)
  G5: structure - round-robin trigger-within-deadline at least 0.30
      below OT, i.e. the clutter dwell-tension breaks fair scheduling
      (pilot 0.36 vs 0.958)
  I1: integrity - max cross-policy total-time spread <= 0.02 relative;
      on failure NO comparison gate is interpreted (EC-7 discipline)
  I2: integrity - half-sample split of G1 agrees to <= 0.03; as I1
stopping: fixed-n, single governed run after the sealing commit
falsification: G1 fail -> consumer-relevance does not beat honest
  info-greedy at matched time on this model; P_C is a feature, not a
  scheduling policy; reported as the boundary answer regardless of sign.
  G4 fail -> info maximization does NOT structurally neglect the critical
  channel here; the mechanism story is wrong. G5 fail -> the clutter
  dwell-tension does not break fair scheduling; the round-robin result
  was model-specific. I1/I2 fail -> instrument integrity broken, no
  comparison claimed. All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Linear-Gaussian (the regime where `tr(P_C Σ)` is exact, hence friendliest to
OT). Clutter modeled as a 2-state platform-motion process modulating imaging
noise — a reasonable abstraction of the Doppler-residue mechanism, NOT a full
range-Doppler cancellation simulation. Single trigger event and single still
occupant per run. Myopic (one-step) schedulers only; no optimality claim for any
policy, all are matched-budget heuristics. No operational or fielded-performance
claim. No claim that consumer-relative scheduling is novel as a concept — see
the anchor.

## Interpretation ceiling

The strongest supportable conclusion on pass: in this idealized clutter-limited
multifunction-aperture model, consumer-relevance is the load-bearing variable
for meeting a counter-RCIED reaction deadline, and information-greedy scheduling
structurally cannot, which motivates an OT supervisor in the real scheduler.
This does NOT establish fielded performance, nor superiority over a
threat-weighted radar-resource-management scheduler tuned by hand (that
comparison is future work; the OT contribution is the principled, cross-domain
consumer-relative objective, not a claim of beating every hand-tuned heuristic).
