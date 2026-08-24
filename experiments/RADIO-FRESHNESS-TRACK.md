# Radio-Freshness Track: 5G/6G PHY & RAN adaptation certificates

**Status:** re-homed 2026-08-24 from `network-governor`. Chip 🕒📡 RF. Freshness
program ([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). Substrate: **NVIDIA Sionna
1.2.2** (real 5G NR LDPC per TS 38.212, TR38.901 channels) on Atlas GPU 1.

## Question

Every 5G "adaptation certificate" — a UE/gNB report that certifies a transmission
decision (CQI→MCS, CSI→precoder, beam index, RSRP→serving cell, PMI/RI/TA) — **ages**
over the channel coherence time, is graded by the **HARQ ACK/NACK** (or the served
link outcome), and false-clears when acted on stale. The refresh floor scales with
coherence time (**OT-14 law:** floor ≈ 0.177·T_coh, R²=0.915). Consumer-relativity:
the reliability *target* is the read operator — the same CQI certificate is fine for
eMBB (1e-1) and vacuous for URLLC (1e-3).

## Cells

| Cell | Certificate → decision | Witness | naive → aware | Sealed |
|---|---|---|---|---|
| **XPROTO-CSI** (`analysis/csi`) | CQI → MCS | HARQ | 0.34–0.37 → 0.10 (OLLA) | ✅ 08-23 |
| **XPROTO-BEAM** (`analysis/beam`) | mmWave beam index | HARQ | 0.31 → 0.02 (BFR) | ✅ 08-23 |
| **XPROTO-AICSI** (`analysis/aicsi`) | neural-CSI recon (turboquant bridge) | precoder/HARQ | recon wins yet 0.28 → 0.13 | ✅ 08-23 |
| **XPROTO-HO** (`analysis/ho`) | RSRP → serving cell | RLF | 0.31–0.44 → 0.09–0.12 | ✅ 08-23 |
| **XPROTO-URLLC** (`analysis/urllc`) | reliability target (eMBB vs URLLC) | HARQ vs budget | ~0.11 → ~1e-5 (+diversity) | ✅ 08-24 |
| **XPROTO-PHY** (`analysis/phy`) | PMI / RI / TA | HARQ | 0.27–0.42 → 0.055–0.13 | ✅ 08-24 |
| **XPROTO-CCA** (`analysis/cca`) | 802.11 CCA | ADALM-Pluto Rx | ~0.30 → ~0.03 (RTS/CTS) | unsealed (SDR-gated) |

**OT-14 refresh-floor law** (`analysis/csi/CSI-refreshfloor.*`): the report period
holding false-clear at target scales linearly with coherence time; the optimal
linear predictor cannot beat the one-coherence-time wall (Gaussian fading → Wiener
optimal). The **RAN governor** (`analysis/ran`) is the reference O-RAN rApp core:
observe→measure false-clear→refresh at the floor→escalate (diversity / re-route).

## Shared tooling

`analysis/freshread` — the generalized `read_fresh` witness-gate (ZK/PG/Mongo
adapters), shared across the database-freshness and radio tracks.

## Seals

CSI/BEAM/AICSI/HO sealed in network-governor (`ng:fda9148`); **URLLC + PHY sealed
natively here 2026-08-24 on the real Sionna substrate** (URLLC PASS: eMBB ~0.11,
naive ≥30× URLLC budget, aware ~1e-5; PHY PASS: PMI/RI/TA all bars on the nrsionna
LDPC decode). Only **CCA** remains unsealed — SDR-gated (ADALM-Pluto hidden-node
bench). See SEALS.md.
