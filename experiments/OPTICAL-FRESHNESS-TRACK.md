# Optical-Freshness Track: QoT-certificate vacuity in optical networks

**Status:** constructed 2026-08-24. Chip 🕒🔦 OPT. Freshness program
([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). Substrate: **GNPy** (oopt-gnpy),
the optical-networking-standard GN-model QoT engine — the *Sionna of optical*.
Cell **XPROTO-QOT** UNSEALED (shakedown PASS; seal ≥ 2026-08-25). Targets **OFC
2027** (deadline 2026-10-20).

## Question

**Optical margins are the price of an un-witnessed, un-refreshed freshness
certificate.** A pre-provisioning **QoT (GSNR) estimate** → modulation choice is a
certificate. It is computed under the *reference* channel loading; as neighbours
are added, nonlinear interference grows and the real GSNR drops, so the
certificate **false-clears** (the provisioned format fails its FEC threshold).
The false-clear is **consumer-relative** — it depends on the lightpath's footprint
(spectral position + reach) — so a blanket margin is right for one lightpath and
catastrophic for another. Witness = the coherent receiver's **pre-FEC BER**.

## Cell

**XPROTO-QOT** (`analysis/qot`, GNPy over **CORONET-CONUS** transparent routes):
naive certificate (GSNR under reference loading) false-clears **~50%** of lightpaths
when the band fills (loading penalty ~2.6 dB); the false-clears are
footprint-dependent (fc_spread ~0.50); a consumer-aware certificate holds at **0**.
Result 2 (F-QOTML): an average-error ML-QoT estimator wins reconstruction (MAE 0.65
vs 0.95) yet false-clears ~8× at the FEC cliff (0.04 vs 0.005) at equal capacity. Bars B1 naive_fc≥0.25 / B2 aware_fc≤0.10
/ B3 dominance + MC1 real loading penalty / MC2 footprint-relativity / MC3
non-degenerate. Sealed rung = GNPy; external-validity graduation = pre-FEC BER on a
fibre testbed / field trace + the EGN/split-step reference.

## Why it lands at OFC

Margin reduction is the field's biggest capacity lever; the OT delta is the
**measured, consumer-relative, footprint-witnessed false-clear rate** as a
first-class number (not a blanket margin) + the **refresh floor** from add/drop
churn. Fits the networks/systems track (co-sponsored IEEE ComSoc + Photonics +
Optica). Credited prior art: ML-QoT, physical-layer-aware RSA, the GN/EGN model.
The AICSI/KV-keys twin also applies: an ML-QoT estimator minimising *average* OSNR
error false-clears at the FEC cliff, where the consumer reads a threshold.

## Refresh-floor follow-on (declared)

The OT-14 law in optical: re-validate the QoT certificate within the loading-change
coherence time (add/drop-driven), i.e. re-certify faster than the band fills.
