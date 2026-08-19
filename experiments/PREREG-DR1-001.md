# PREREG-DR1-001 — DR-1: the directional-staleness crossover exhibit

**SEALED at the commit ledgered in `SEALS.md`.** The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign in the track document and README status ledger.

## Claim under test

The DR track's positive control (experiments/DYNAMIC-RELEVANCE-TRACK.md
§5, DR-1; Paper VIII §IX states the interface as an explicit conjecture):
age-based freshness and directional staleness S_C(θ) = g(θ)ᵀΣg(θ)
**provably disagree, at a point predictable in closed form before any
rollout**. Per random system: a plant with one slow low-noise mode and
one fast high-noise mode; an OLD scalar measurement of the slow mode
(age 20–40) versus a FRESH one of the fast mode (age 3–8). Age ranks the
fresh set better at every read direction, always. The sealed prediction
is that the realized consumer-loss ordering flips exactly once as the
read direction sweeps the quadrant, at the angle
tan²θ* = −D₁₁/D₂₂ (D = Σ_A − Σ_B) computed from propagated covariances
alone; that the older observation genuinely wins below θ*; and that the
entire effect vanishes for the isotropic consumer (the null that makes
direction the mechanism, not information volume).

This is the exhibit/positive-control campaign: it licenses the DR track's
vocabulary. It does NOT claim scheduling advantage (that is DR-3, its own
future seal, disciplined by the anchor that signal-aware sampling already
beats age-optimal — Sun–Polyanskiy–Uysal 2020).

## Design

Harness `python/dr1_crossover.py`, governed mode. 20 fresh random systems
from the generator frozen in the harness header (a_slow ∈ [0.995, 0.9995],
a_fast ∈ [0.90, 0.98], q_slow ∈ [2e-4, 1e-3], q_fast ∈ [1e-2, 5e-2],
ages 20–40 / 3–8, r = 0.01), n = 200,000 Monte-Carlo rollouts per arm per
system, θ-grid of 181 points on [0, π/2]. Exact-linear model: the MC leg
is an instrument check on the harness (errors are Gaussian with the
analytic covariance), so G4 is an integrity gate in the EC7-003 sense —
the analytic instrument's residual measured as its own diagnostic. Basis
note recorded in the harness: the mode frame is WLOG (common rotation of
plant, measurements, and consumer sweep is a change of basis with
identical numbers).

## Two disclosed calibration pilots

1. **Pilot 1** (2026-08-19, seed 20260819, single hand-built instance,
   `results/dr1-pilot1.json`): the exhibit exists in minimal 2-mode form;
   θ* predicted to 5.0e-4 rad of measured; residuals 0.19%/0.98%;
   isotropic null clean. Established the exhibit and the residual scale.
2. **Pilot 2** (2026-08-19, seed 20260820, 20 generator draws,
   `results/dr1-pilot2.json`): existence predicted 20/20, measured
   exactly-one-flip 20/20, gap median 0.70 / max 1.64 grid steps,
   residual max 0.0069, null flips 0, old-wins in all 20. Bars frozen
   below this performance with margin.

```yaml
id: PREREG-DR1-001
date: 2026-08-19
retrospective: false
kind: directional-staleness crossover exhibit (DR track positive control);
      random 2-mode systems, old-slow vs fresh-fast information sets,
      closed-form crossover prediction vs realized MC loss ordering
harness: python/dr1_crossover.py
code_hash: sha256:caeb9f4141982bb5a37228247ace8a8c5b26ad007401765934b160e1004c292a
governed_seed: 20260905
calibration_seeds: [20260819, 20260820]
frozen_config:
  n_sys: 20
  n_mc: 200000
  n_theta: 181
  r_meas: 0.01
  generator: {a_slow: [0.995, 0.9995], a_fast: [0.90, 0.98],
              q_slow: [2.0e-4, 1.0e-3], q_fast: [1.0e-2, 5.0e-2],
              age_old: [20, 40], age_fresh: [3, 8]}
sealed_gates:
  G1: existence — closed form predicts a crossover in >= 80% of systems
      (cal 100%)
  G2: measured — of predicted-crossover systems, >= 90% show exactly one
      sign change of the MC loss difference on the grid (cal 100%)
  G3: prediction accuracy — |theta*_pred - theta*_meas| median <= 1.5
      grid steps and max <= 4.0 grid steps over measured-crossover
      systems (cal 0.70 / 1.64)
  G4: instrument integrity — max relative analytic-vs-MC residual over
      all arms and systems <= 0.02 (cal 0.0069)
  G5: isotropic null — trace-consumer ordering flips in 0 of 20 systems
      (cal 0)
  G6: age is wrong below the crossing — the older observation's realized
      loss is lower on a nonempty part of the grid in EVERY
      measured-crossover system (cal all 20)
stopping: fixed-n, single governed run
falsification: G1/G2 fail -> the crossover does not exist robustly over
  the declared system class; the exhibit is a hand-tuned artifact and the
  DR track loses its positive control (reported as such). G3 fail -> the
  closed form does not predict the realized crossing; directional
  staleness is not preregisterable and DR-1's headline is FALSE. G4 fail
  -> instrument integrity broken, NO other gate is interpreted (EC-7
  discipline). G5 fail -> the effect survives without direction — the
  mechanism claim is wrong. G6 fail -> age never actually misranks;
  the track's motivating sentence is withdrawn. All reported at equal
  prominence.
amendments: []
```

## Scope and non-claims

Exhibit only: no scheduling policy, no matched-budget advantage claim, no
recovered-operator (probing) arm — those are DR-3 and later seals. The
consumer is a planted known direction; blind recovery is inherited from
the EC track and not re-litigated here. Exact-linear plant; nonlinear /
non-Gaussian staleness is open. Class on pass: `[predicted]` for the
existence-and-predictability of the crossover over the declared system
class.
