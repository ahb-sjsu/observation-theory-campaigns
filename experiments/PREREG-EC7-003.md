# PREREG-EC7-003 — EC-7 third seal: analytic effort matching

**SEALED at the commit ledgered in `SEALS.md`.** Third and, if the
instrument is finally right, decisive seal for Campaign 7. The governed run
executes ONCE after the sealing commit, on the governed seed below, and is
reported regardless of sign.

## Lineage — two registered misses, one instrument

- [`PREREG-EC7-001`](PREREG-EC7-001.md) (seed 20260828): predictions passed
  (K1 +8.3%, K2 1.037, K3 +7.7%); **FAIL** on absolute effort-target
  transfer (>30% drift, 2/20 systems, common-mode).
- [`PREREG-EC7-002`](PREREG-EC7-002.md) (seed 20260830): predictions passed
  again (K1 +9.4%, K2 1.026, K3 +8.6%); **FAIL** on the respecified
  cross-arm spread (0.322 vs 0.15, 1/20 systems, **arm-differential** —
  iso arms undershot effort ~35%, real comparison contamination, refuting
  v1's benign-common-mode reading).

Both misses were the SAME instrument failing: simulation-bisection effort
matching, whose calibration-to-heldout transfer error proved able to
contaminate the comparison. Neither miss touched the claims; both stay on
the record.

## The v3 instrument — analytic, transfer-error-free

The Kalman covariance recursion is control-independent, so the sensing
schedule and per-step gains are FIXED per (system, charge level), computed
once. Expected effort `E‖u_t‖² = tr(K Ξ_t Kᵀ)` then follows EXACTLY by
propagating the joint second moment of `z = (x, x̂)` through the identical
schedule (predict `F = [[A, −BK],[0, A−BK]]` plus process noise; per scalar
update `G = [[I,0],[kal hᵀ, I−kal hᵀ]]` plus `kal r kalᵀ` on the estimate
block). ρ is bisected against the ANALYTIC target — no noise bundle enters
the matching. **Calibration measures the instrument residual directly: the
cross-arm analytic spread is 1e-5** (bisection precision), so the held-out
spread gate now measures only CRN evaluation scatter of a genuinely common
expectation.

**All prediction bars inherited unchanged for the third time** (K1 ≥ 0.04,
K2 capture ≥ 0.60, K3 ≥ 0.00).

## One disclosed calibration pilot (v3 design)

**Pilot 1** (seed 20260831, n=8): K1 0.085, K2 0.916, K3 0.080 — all over
the inherited bars; **analytic cross-arm spread 0.00001** (the v1/v2 error
class is gone by construction and by measurement); held-out spread max
0.0439; stability, boundedness, controls clean. The spread band is frozen
at 0.10 — 2.3× the calibration max of a max-statistic that the governed
n=20 will draw more of, with the analytic residual at 1e-5 underneath it.

```yaml
id: PREREG-EC7-003
date: 2026-08-19
retrospective: false
kind: EC-7 third seal — consumer-derived LQG penalty at ANALYTICALLY matched
      control effort (joint second-moment propagation; zero transfer error)
supersedes: PREREG-EC7-002 (second registered miss; both misses stay on the record)
harness: python/ec7c_closedloop.py
code_hash: sha256:6ca1be7e025ffe3d0bf44c4aeb296ff4925fcec305ffb250dcdc2a7ce50480ad
governed_seed: 20260901
calibration_seed: 20260831
frozen_config:
  N_sys: 20
  bisect_iters: 20
  n_endpoint_bundles: 6   # hand-diag family selection only, never matching
  delta_k1: 0.04          # inherited (third time, unchanged)
  eps_k2: 0.40            # inherited (capture >= 0.60), unchanged
  delta_k3: 0.00          # inherited, unchanged
  spread_band: 0.10       # I2 (cal held-out max 0.0439; analytic residual 1e-5)
internal_calibration:
  pilot1: {K1: 0.085, K2: 0.916, K3: 0.080, heldout_spread_max: 0.0439,
           analytic_spread_max: 0.00001, stable: true, bounded: true,
           shuffled_gap: 0.062, anti_ok: true}
sealed_predictions:
  K1: oracle-penalty LQG beats iso-penalty LQG on the consumer endpoint at
      matched effort by >= 4% (inherited)
  K2: probe-charged blind penalty captures >= 60% of the oracle advantage
      (inherited)
  K3: full geometry at least ties the best hand-tuned diagonal (inherited;
      a tie is the operationally-unnecessary boundary, reported either way)
integrity: [spectral radius < 1 all loops, states bounded,
            I2 cross-arm held-out effort spread <= 0.10 per system;
            the analytic cross-arm spread is reported as the instrument
            residual and must remain ~0]
controls: [shuffled-vs-iso >= -0.02, anti loses to oracle and not better
           than iso (2% slack)]
stopping: fixed-n, single governed run
falsification: as EC7-001/-002 with the analytic instrument; an I2 fail now
  indicts CRN evaluation scatter itself and the campaign NARROWS (a third
  instrument iteration is not licensed by this seal). All reported at equal
  prominence.
amendments: []
```

## Scope and non-claims

As EC7-001. If this run passes, Campaign 7's claims are promoted at
`[predicted]` with the two-miss instrument history cited as consistent
context, never as evidence; if I2 fails even with a 1e-5 instrument
residual, the campaign narrows rather than iterating a fourth time.
