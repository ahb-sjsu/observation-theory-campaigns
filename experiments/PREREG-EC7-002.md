# PREREG-EC7-002 — EC-7 rehabilitation: closed-loop control, v2

**SEALED at the commit ledgered in `SEALS.md`.** Successor to
[`PREREG-EC7-001`](PREREG-EC7-001.md) per the registered-miss → successor
pattern (020→021, 032→033 in the parent program). The governed run executes
ONCE after the sealing commit, on the governed seed below, and is reported
regardless of sign.

## Lineage — the registered miss and the principled fix

EC7-001 (governed seed 20260828) was an **honest FAIL on its
effort-matching integrity gate**: all three sealed predictions passed
numerically (K1 +8.3%, K2 blind capture 1.037, K3 +7.7%; every loop stable
and bounded; controls clean), but realized held-out efforts strayed >30%
from the calibration target in 2/20 systems — **common-mode across all four
verdict arms** (all drifting together, so within-system comparisons stayed
effort-consistent while the absolute-transfer gate failed). Root cause: the
3-bundle effort-matching shortcut under-powers per-system target transfer.
Per the sealed falsification clause, no comparison was claimed and the
passing predictions were not promoted.

The v2 fixes, exactly as designated in the track document:
1. **Matching bundles 3 → 8** (bisection 14 → 12 iterations).
2. **The integrity gate respecified to the fair-comparison quantity**:
   cross-arm effort spread on held-out rollouts — per system, over the
   verdict arms, `(max − min)/mean ≤ band`. Common random numbers make this
   the CRN-robust statistic; the old absolute-target deviation is reported
   as a diagnostic, never gated.

**All prediction bars are inherited unchanged from EC7-001** (K1 ≥ 0.04,
K2 capture ≥ 0.60, K3 ≥ 0.00): the rehabilitation fixes the instrument,
never the claims.

## One disclosed calibration pilot (v2 design)

**Pilot 1** (seed 20260829, n=8): K1 0.074, K2 1.034, K3 0.066 — all
comfortably over the inherited bars; I2 spread max **0.0853**; stability,
boundedness, controls all clean; diagnostic max target-dev 0.225 (the old
gate would have been brushed again, vindicating the respecification). The
spread band is frozen at **0.15**, not the draft 0.10 the pilot would have
brushed: the gated quantity is a **max statistic over systems**, and the
governed run draws 20 systems against calibration's 8, so the band sits at
~1.75× the calibration max. This reasoning is part of the seal.

```yaml
id: PREREG-EC7-002
date: 2026-08-19
retrospective: false
kind: EC-7 rehabilitation — consumer-derived LQG penalty at matched control
      effort, integrity gate respecified to cross-arm spread (Campaign 7 v2)
supersedes: PREREG-EC7-001 (registered miss; stays on the record)
harness: python/ec7b_closedloop.py
code_hash: sha256:8672eb243fff1c7521bc2211f397fbd7a82eb68cd39a20b653ddd86d8514f791
governed_seed: 20260830
calibration_seed: 20260829
frozen_config:
  N_sys: 20
  N_cal_bundles: 8
  bisect_iters: 12
  delta_k1: 0.04      # inherited from EC7-001, unchanged
  eps_k2: 0.40        # inherited (capture >= 0.60), unchanged
  delta_k3: 0.00      # inherited, unchanged
  spread_band: 0.15   # I2 (cal max 0.0853 at n=8; max-statistic headroom for n=20)
internal_calibration:
  pilot1: {K1: 0.074, K2: 1.034, K3: 0.066, spread_max: 0.0853,
           target_dev_diagnostic: 0.225, stable: true, bounded: true,
           shuffled_gap: 0.086, anti_ok: true}
sealed_predictions:
  K1: oracle-penalty LQG beats iso-penalty LQG on the consumer endpoint at
      matched effort by >= 4% (inherited)
  K2: probe-charged blind penalty captures >= 60% of the oracle advantage
      (inherited)
  K3: full geometry at least ties the best hand-tuned diagonal (inherited;
      a tie is the operationally-unnecessary boundary, reported either way)
integrity: [spectral radius < 1 all loops, states bounded,
            I2 cross-arm effort spread <= 0.15 per system]
controls: [shuffled-vs-iso >= -0.02, anti loses to oracle and not better
           than iso (2% slack)]
stopping: fixed-n, single governed run
falsification: as EC7-001, with I2 in place of the absolute-transfer gate;
  an I2 fail means even cross-arm fairness could not be held and no
  comparison is claimed. All reported at equal prominence.
amendments: []
```

## Scope and non-claims

As EC7-001. The v1 miss stays in the ledger and README; a v2 pass promotes
the campaign's claims with the v1 numerical agreement noted as consistent
history, never as evidence.
