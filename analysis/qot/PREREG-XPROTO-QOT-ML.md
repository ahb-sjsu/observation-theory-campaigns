# PREREG-XPROTO-QOT-ML — the ML-QoT objective is consumer-misaligned (OFC Result 2)

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-24. Earliest compliant seal
**2026-08-25** (`qotml_check.py` codes the cooling-off). Graded seeds {20260825,
20260826, 20260827}, disjoint from the shakedown's {0,1,2}. Substrate = GNPy
GN-model GSNR (`fam_qot`) + scikit-learn, run in the qot venv (numpy<2). Result 2
of the OFC paper, companion to PREREG-XPROTO-QOT.

## The claim

An ML-QoT estimator trained to minimize **average** GSNR error is optimizing a
reconstruction metric; the consumer — the FEC decoder — reads a **threshold**. Under
irreducible prediction uncertainty (unmeasured network state), the average-error
estimator therefore **false-clears at the FEC cliff** — a small over-prediction near
a modulation boundary flips a format decision — while a **consumer-aware**
(conservative lower-quantile) objective holds, at comparable delivered capacity. The
reconstruction-vs-consumer dissociation (the OT VALUE thesis; the XPROTO-AICSI
lesson) in machine-learning QoT.

## Family F-QOTML (constructed + shaken down 2026-08-24)

Features = provisioning-time (reference-loading) GSNR + (spectral position, reach,
deployed loading); the true deployed GSNR carries an **irreducible impairment**
(`HIDDEN_NOISE_DB = 0.8` dB, unmeasured state the estimator cannot predict) and is
the **witness**. Two `GradientBoostingRegressor` objectives: **mse** (squared error)
and **aware** (quantile, α=0.15). Each selects the highest modulation with required
GSNR ≤ prediction − 0.5 dB; a selection **false-clears** if its required GSNR
exceeds the true GSNR.

## Bars (bind at seal; checked against the family record first)

*Demonstrated (seeds {0,1,2}, CORONET-CONUS reaches): MAE mse ≈ 0.65 < aware ≈ 0.95
(mse wins recon); FC mse ≈ 0.03–0.04 vs aware ≈ 0.004–0.007 (aware wins consumer,
~8×); delivered bits/symbol ≈ 3.9 for both.*

- **B1 — the average-error estimator false-clears at the cliff.** Per seed:
  `fc_mse ≥ 0.03`.
- **B2 — the consumer-aware objective holds.** Per seed: `fc_aware ≤ 0.03`.
- **B3 — dominance.** Per seed: `fc_aware ≤ fc_mse / 2`.

**Manipulation checks (bars too):**
- **MC1 — the dissociation is real.** `mae_mse < mae_aware` (the MSE estimator
  genuinely wins reconstruction; the aware one is not simply better at everything).
- **MC2 — comparable capacity.** `bps_aware ≥ 0.90 · bps_mse` (the aware objective
  is not degenerate conservatism buying safety with throughput).
- **MC3 — non-degenerate.** `n_test ≥ 100`.

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL, kept.
**Kills:** `fc_mse < 0.01` (no cliff false-clear — task too easy / no irreducible
uncertainty) or `fc_aware > 0.05`.

## Seal procedure

On 2026-08-25+: confirm `QOTMLREP-family.json` PASSes `--check-family`, reread, flip
STATUS to SEALED, commit; in the qot venv run `fam_qotml.py --seeds 20260825 20260826
20260827 --out QOTMLREP-graded-raw.json`, `qotml_check.py` → commit
`XPROTO-QOT-ML-graded.json`.

## Scope

The irreducible-uncertainty term models the unmeasured state real ML-QoT faces; its
magnitude is a declared modeling choice. The consumer-aware objective here is a
conservative quantile; a decision-margin or cost-sensitive loss is an equivalent
route. GNPy GN model is the evidence rung; a fibre-testbed pre-FEC-BER witness is the
external-validity graduation. Credited prior art: ML-QoT regression/classification;
OT's delta is the *measured* reconstruction-vs-consumer false-clear dissociation and
the objective it implies.
