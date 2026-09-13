# Sensor-Management Track (SM)

**Status:** opened 2026-08-30, exploratory. Chip 🎚️ SM (a level slider, for
the allocation of one budget across channels; assigned 2026-09-13, this track
having opened without one). First seal SM-1 in draft
(`PREREG-SM1-001.md`). Sibling of the DR and EC tracks: the OT question here
is not *what to estimate* but *where to spend a shared sensor's scarce
budget*, when the downstream consumer cares about a low-dimensional function
of the state.

## The consumer

A multifunction phased aperture (the magnetar man-portable shield;
`C:\Users\abptl\Documents\personal\magnetar_polyfunctional_aperture.md`) is one
shared sensor/effector time-shared across tasks: image a scene cell, listen on
a trigger band (the Safety Ray counter-RCIED cue), sweep for device bearings.
The tactical decision cares overwhelmingly about two directions of the state,
is a radio trigger about to fire and is the doorway occupied, and barely about
a noisy peripheral cell or a device bearing.

## The OT claim

Standard sensor management spends each measurement to maximize total
information (minimize `tr Σ`, or maximize mutual information / minimize
`log det Σ`). OT says spend it on the uncertainty that matters to the decision:
minimize `tr(P_C Σ)`, `P_C` the consumer-relevance projection. The anchor
discipline (as in DR): information-greedy scheduling and fair round-robin are
the established baselines; beating a strawman is not the claim. The claim is
that consumer-relative scheduling beats *honest* info-greedy and round-robin on
the decision-critical outcomes at matched time budget, and does so with the
predicted structure: info-greedy fails specifically by neglecting the quiet,
low-uncertainty, decision-critical channel; and under realistic clutter the
still-occupant dwell cost breaks fair round-robin's reaction deadline while OT
balances both.

## Prior art (WebSearch 2026-08-30, citations verified — the bare result is NOT novel)

The finding "task/consumer-driven scheduling beats information-driven on the
decision metric" is **published prior art**. Verified records:

- **C. Kreucher, A. O. Hero, K. Kastella, "A Comparison of Task Driven and
  Information Driven Sensor Management for Target Tracking," 44th IEEE CDC-ECC
  2005** (info-theoretic methods special session; preprint on Hero's site;
  IEEE Xplore 1582788). Task-driven objective = expected localization risk;
  info-driven = Rényi/MI; task-driven wins on risk. **This is our result in
  general form and MUST be cited as its source.** Their weighting is a bespoke
  tracking-risk functional, NOT a geometric, derived, cross-domain relevance.
- **Q-RAM: R. Rajkumar, C. Lee, J. Lehoczky, D. Siewiorek, "A Resource
  Allocation Model for QoS Management," IEEE RTSS 1997** (+ "Practical
  Solutions…", RTSS 1998). Utility-max under resource constraints; **NP-hard**;
  radar application via the QoS-based RRM line. Priorities are **hand-set**
  (range, velocity, threat, fuzzy logic). Our `P_C` weighting IS a Q-RAM
  priority weighting; `tr(P_C Σ)`-greedy is covariance-based task-driven RRM
  (a worked example in the MATLAB Radar Toolbox).
- Threat-based allocation for cognitive radar networks (arXiv 2311.13906);
  FARRA (AFRL); goal-oriented / semantic-communication sensing ("beyond
  freshness to goal-oriented importance" — the same idea as OT, arriving from
  the AoI/communication side, parallel to the DR track).

## What we learn / how the contribution sharpens

1. Kreucher CAPS the "task beats info" claim; it is not ours. Never present it
   as new.
2. **Where OT genuinely adds:** Q-RAM and threat-weighted RRM HAND-SET the
   priorities; OT DERIVES them from consumer geometry (`tr(P_C ΔΣ)`). The
   defensible experiment is therefore **OT-derived priorities vs hand-tuned /
   heuristic Q-RAM priorities at matched budget** — NOT OT vs info-greedy. This
   is the SM-1 successor (SM-2), and the sharper result.
3. The problem is NP-hard: the greedy myopic scheduler is a FLOOR, never a
   method contribution. Any claim is about the OBJECTIVE, not the solver.
4. **Strongest lesson:** three communities (task-driven sensor management,
   Q-RAM radar RRM, goal-oriented/semantic communication) independently circle
   consumer-relative value. OT is the geometric formalization that unifies them
   AND the estimation/DR/DB/LM tracks. This is the Paper VIII framing.
5. The metric IS the consumer (GOSPA-vs-OSPA lesson): the reaction deadline and
   detection gate are the consumer's cost functional; state it plainly.

**Positioning.** SM-1 claims the quantified MEASUREMENT (the clutter regime
where info-greedy structurally misses the reaction deadline), crediting Kreucher
+ Q-RAM. SM-2 (designated) claims the DERIVATION (OT-supplied vs hand-tuned
priorities). The unification is Paper VIII; the integrated magnetar aperture is
a separate systems paper.

## Exploratory findings (2026-08-30, MATLAB on Atlas; NOT sealed)

Three model refinements, harnesses in `matlab/sm*_*.m`, results in the magnetar
findings note. The direction held and strengthened under each:

1. **Abstract single-run + κ-sweep** (`sm0_aperture_sched.m`,
   `sm0_aperture_sweep.m`): OT best on trigger latency at every κ; info-greedy
   degrades to 100% miss when irrelevant states are noisy; round-robin robust
   but mediocre.
2. **Realistic aperture** (`sm1_aperture_realistic.m`): real 12-element 1.5 GHz
   ULA beam patterns, link-budget SNR, time-resource, 30 ms reaction deadline.
   OT hits the deadline 95%; MI-greedy misses 100% (real beams make scene cells
   independent, so it always finds something more "informative" than the
   trigger). The link budget also showed through-wall is SNR-rich (100+ dB), so
   this is an attention/timing problem, not a noise problem.
3. **Dynamic clutter** (`sm1_aperture_clutter.m`, the SM-1 pilot): still
   occupants need long dwell in low clutter; platform motion raises the floor.
   OT is the only policy to do both hard jobs (100% still-occupant detection AND
   96% trigger deadline); the clutter dwell-tension breaks round-robin's
   deadline (36%). Two modeling fixes on the record (empty-room prior, persistent
   occupancy latent).

## Registry

| ID | Claim | Status |
|---|---|---|
| SM-1 | consumer-relative aperture scheduling beats info-greedy + round-robin on decision-critical outcomes at matched time | **SEALED @5ffade8; governed 20261201 ALL PASS → [measured]** |
| SM-2 | OT-DERIVED consumer-relative value beats HAND-TUNED fixed-priority (Q-RAM) scheduling, incl. a hindsight grid oracle, at matched time | **SEALED @5ffade8; governed 20261202 ALL PASS → [measured]** |

### Governed runs (once, after the sealing commit; reported regardless of sign)

**SM-1 governed** (seed 20261201, 500 MC): OT decJ 0.626, trig<30 ms 95.2%,
still-occ 99.7%, FA 0.5%; trace 86.6%, round-robin 37.8%, MI 0.0%. Gates:
G1 +8.6 pts (bar +3) ✓; G2 99.7%/0.5% (bars ≥95%/≤5%) ✓; G3 0.626 < all ✓;
G4 MI 0.0% (bar ≤20%) ✓; G5 round-robin 57.4 pts below OT (bar ≥30) ✓.
**ALL PASS.** The measurement holds: info-greedy structurally misses the
reaction deadline, round-robin fails it under clutter, OT meets it and detects
the still occupant.

**SM-2 governed** (seed 20261202, 400 MC): OT joint 98.8%, trig 99.8%, doorway
99.0%; grid oracle 94.5%; img-heavy 73.8% (trig 75.5%); trig-heavy 95.0%.
Gates: G1 OT − oracle = +4.3 pts (bar ≥ −1) ✓; G2 min fixed 73.8% (bar ≤85%) ✓;
G3 trig-rate spread 21.7 pts (bar ≥10) ✓; I1/I2 by construction ✓. **ALL PASS.**
The derivation holds: OT-derived value beats the hindsight-tuned fixed oracle
and every fixed tuning, without per-task tuning.

Both governed runs corroborate the two-pilot calibration. Next: fold the SM
track into Paper VIII as the sensor-management consumer, with Kreucher + Q-RAM
credited and the goal-oriented-communication bridge noted.

### SM-2 pilot (2026-08-30, `matlab/sm2_aperture_qram.m`, 400 MC, matched 400 ms)

Joint success = trigger caught within 30 ms AND doorway occupancy called
correctly, across a varied scene ensemble (motion types, trigger timing,
2-state clutter), common random numbers across policies.

| Policy | joint OK | trig<30 ms | doorway correct |
|---|---|---|---|
| OT (derived, no per-task tuning) | **99.0%** | 99.8% | 99.2% |
| Q-RAM trigger-heavy (fixed) | 94.8% | 97.8% | 97.0% |
| Q-RAM balanced (fixed) | 92.5% | 95.2% | 97.2% |
| Q-RAM imaging-heavy (fixed) | 77.2% | 79.2% | 97.0% |
| Q-RAM oracle (best of 15-point grid, hindsight) | 95.2% | 97.0% | 98.2% |

**Finding:** each single fixed tuning is brittle (imaging-heavy fails the
trigger deadline; trigger-heavy under-serves imaging), and OT beats even the
hindsight grid oracle. **Mechanism:** the optimal schedule is time-varying
within a trial (confirm the still occupant early, then guard the trigger); a
fixed revisit interval cannot do that, but OT derives it from `tr(P_C ΔΣ)/dwell`
with no per-task tuning. **Scope (honest):** this is OT vs HAND-TUNED FIXED
priorities. It is NOT a claim over adaptive/cognitive RRM — which is a stronger
policy class but needs a scheduling objective, exactly what OT supplies from the
consumer geometry. So SM-2's contribution is the DERIVATION (the object that
generates the adaptive schedule), evidence for the unification, not "adaptive
beats fixed" (known). A proper SM-2 prereg is TODO before any claim.

## Related

`DYNAMIC-RELEVANCE-TRACK.md` (DR; directional-beats-isotropic sibling),
`ESTIMATION-CONTROL-TRACK.md` (EC; smart-sensor scheduling idealization),
Paper VIII (fold SM in as a new consumer track on pass).
