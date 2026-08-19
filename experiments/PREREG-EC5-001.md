# PREREG-EC5-001 — EC-5: physical-model FSO consumer (OT-EC Campaign 5)

**SEALED at the commit ledgered in `SEALS.md`.** First EC campaign sealed
natively in this repository (EC-2/3/4 migrated with their original
geometric-observation seals; see `ESTIMATION-CONTROL-TRACK.md`). The governed
run executes ONCE after the sealing commit, on the governed seed below, and
is reported regardless of sign in the track document and README status
ledger.

## Claim under test

Campaign 5 of the OT-EC paper (`geometric-observation`, Paper VIII §XI):
a consumer whose geometry is a **physics-based free-space-optical link
model** — Gaussian far-field + fiber-coupling rolloff over a hidden
state→physical map mixing attitude and range-scaled transverse position —
treated strictly as a black box, can be probed with the paper §VI
**belief-averaged smoothed operational metric** (finite perturbations at
half a belief standard deviation; never a point Hessian, because the
endpoint is threshold-like), and the recovered `P̄_C`:

- **E1 (the paper's registered key test).** Among sensor schedules matched
  on time-average `tr Σ`, the ordering of the PHYSICAL endpoint (mean
  coupling loss when pointing with the estimate) is predicted by
  `tr(P̄_C Σ̄)` — and because the covariance path is deterministic, the
  prediction precedes the loss measurement by construction ("predict the
  ordering before the run").
- **E2.** The `P̄_C`-aligned schedule, probe cost charged, beats the best
  consumer-agnostic schedule on coupling loss at matched budgets.
- **E3.** The charged blind schedule captures most of an uncharged
  lavish-probe (8×) reference schedule's advantage — the recover/match
  discipline; no analytic optimum exists for the nonlinear link, which is
  the point.

The endpoint is external: coupling loss and outage fraction come from the
link physics, so OT cannot win by optimizing its own surrogate.

## Prior-art posture (SPIE-targeted sweep, 2026-08-19, run pre-seal)

The Campaign-5 gap assertion is used ONLY in its narrowed form, per the
sweep verdict: prior art derives estimator requirements from communication
needs as **static scalar pointing budgets** (canonically Lee–Ortiz–Alexander,
JPL IPN 42-161, 2005 — star-tracker rate and gyro grade flowed down from a
200–300 nrad budget), probes the coupling surface **for control** (nutation
/ SPGD fine-steering loops), and schedules sensors against covariance
objectives **without any link application** (Al Ahdab–Leth–Tan, ICML 2025).
No found work derives estimator design or sensor/update scheduling from the
link's **sensitivity geometry** (Jacobian/Hessian of coupling/BER vs state)
or composes a probed structure with the Kalman covariance — the three
ingredients exist separately; the composition appears open. The loose claim
"nobody derives estimator requirements from the link" is **conceded as
false** and must not be used. SPIE full texts were inspected at
title/abstract level (paywall); this residual is disclosed.

## Design

Machinery imported from the migrated, sealed `blind_scheduling.py`
(unmodified; its sha256 equals GO-P-2026-087's `code_hash`). Random stable
LTI (d=12), 30-sensor pool, k=3, T=60, Kalman filter, common random numbers.
Consumer: per-system hidden orthonormal map; physical coords 0,1 = attitude
tip/tilt (gain 0.8–1.2), 3,4 = transverse position (gain 0.15–0.35); beam
scale `theta0` set per system at the belief-typical offset (operating point
at the Gaussian shoulder, coupling ≈ e⁻¹). Policies: `align` (charged),
`lavish` (8× probes, uncharged reference), `iso`, `logdet`, `random`,
`shuffled` (charged), `anti` (charged). Probe charge as GO-087 (per-use,
spread steps).

## Three disclosed calibration pilots (design fixes only; no sealed bar existed)

1. **Pilot 1** (E1 1.000/7 pairs, E2 0.088, E3 0.813, shuffled +0.021, but
   anti-control False): all headline metrics healthy at first light; the
   anti control failed as specified.
2. **Pilot 2** (identical metrics; per-policy diagnostic added): pooled
   means align 0.177 < iso 0.199 < anti 0.212 < logdet 0.216 < shuffled
   0.220 < random 0.263 — the anti arm IS worse than align and iso; the
   "failure" was requiring anti to also exceed logdet, which is merely a
   weak agnostic arm, never a meaningful bound (the GO-088 lesson
   recurring). Also removed a dead duplicate logdet policy entry.
3. **Pilot 3** (control respecified): anti must lose to align at EQUAL
   probe charge AND not beat iso (2% slack). Validated arithmetically on
   pilot-2's seed-deterministic pooled numbers (0.2118 > 0.1769;
   0.2118 ≥ 0.1948). Design frozen; E2 floor set at 0.04, conservative
   against the 0.088 calibration value's modest headroom.

```yaml
id: PREREG-EC5-001
date: 2026-08-19
retrospective: false
kind: physical-model FSO consumer — belief-averaged recovery -> scheduling,
      reconstruction-matched physical prediction (OT-EC Campaign 5, first
      native EC seal in observation-theory-campaigns)
harness: python/ec5_fso_consumer.py
code_hash: sha256:315c5fa9ffedfaf4433924bec0575d8f6add15bd40f4da1c5e43181508e65e8d
governed_seed: 20260824
calibration_seed: 20260823
frozen_config:
  N_sys: 20
  N_probe: 40
  lavish_factor: 8
  lambda_p: 0.002
  eta_outage: 0.10
  trace_tol: 0.10
  q_pred: 0.80        # E1 gate (cal 1.000 over 7 pairs)
  min_pairs: 8        # E1 integrity gate
  delta_e2: 0.04      # E2 gate (cal 0.088)
  eps_e3: 0.30        # E3 gate: capture >= 0.70 (cal 0.813)
internal_calibration:
  pilot2: {E1: 1.000, E1_pairs: 7, E2: 0.088, E3: 0.813, shuffled_gap: 0.021,
           pooled: {align: 0.1769, lavish: 0.1719, iso: 0.1988,
                    logdet: 0.2156, shuffled: 0.2200, anti: 0.2118,
                    random: 0.2629}}
sealed_predictions:
  E1: physical-loss ordering predicted by tr(Pbar Sigma_bar) in >= 80% of
      trace-matched schedule pairs, with >= 8 pooled pairs
  E2: charged aligned schedule beats best consumer-agnostic schedule by
      >= 4% mean relative coupling loss
  E3: charged blind schedule captures >= 70% of the lavish reference's
      pooled advantage over iso
controls: [shuffled-vs-iso >= -0.02, anti loses to align at equal charge
           AND does not beat iso (2% slack)]
secondary: outage fraction reported, not gated
stopping: fixed-n, single governed run
falsification: E1 fail -> the composition does not carry physical ordering
  through a threshold-like consumer — belief-relative OT's first physical
  test fails. E2 fail -> recovered geometry adds nothing over agnostic
  scheduling on a physical endpoint. E3 fail -> the probe budget, not the
  geometry, is doing the work. All reported at equal prominence.
amendments: []
```

## Scope and non-claims

Physics-based SIMULATED consumer — a step toward, not the arrival at, the
hardware endpoint (real link hardware remains future work and would get its
own seal). Smooth Gaussian rolloff with an outage threshold reported as
secondary; harder cliffs (BER waterfalls, deep fades) are follow-on. No
optimality claim for greedy selection. The narrowed prior-art posture above
is part of what this document seals.
