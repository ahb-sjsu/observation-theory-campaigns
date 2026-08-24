# Freshness Program: the witnessed-certificate axis (consolidated home)

**Status:** umbrella doc for the consumer-relative **witnessed freshness
certificate** program, re-homed into this repo on 2026-08-24 from the concurrent
`network-governor` program. Chip 🕒 FRESH. This dissolves the former
`DATABASE-TRACK.md` §0 coordination boundary (which had ceded freshness to
`network-governor`); the two OT programs are now one repo.

## The grammar (one thesis, many domains)

A **certificate** asserts a decision is safe (a replica is fresh enough, a rate is
supportable, a device is calibrated, a quote is live, the network has converged).
It is (1) **consumer-relative** — evaluated through the read operator `P_C` of the
actual consumer, not an aggregate; (2) **witnessed** — graded against an
independent measurement of the true outcome; (3) refreshed within its **coherence
floor**. The reported metric is the **false-clear rate**: how often "safe" is
wrong. A naive certificate whose false-clear rate exceeds the target it claims is
**vacuous** for that consumer. This is the operational, measurement side of OT,
complementary to the repo's other axes (precision/encoding, alignment tax,
estimation-control, …) which read `tr(P_C·Σ)` in allocation rather than freshness.

## Tracks (freshness program)

| Track | Domain | Cells |
|---|---|---|
| [ROUTING-TELEMETRY](ROUTING-TELEMETRY-TRACK.md) | interdomain routing | BGP/IS-IS/OSPF quiescence, RPKI staleness, BMP witness, D8 dataplane join |
| [DATABASE-FRESHNESS](DATABASE-FRESHNESS-TRACK.md) | replication / coordination | XPROTO-PG, -MG, -PGX, -GEO, -ZK |
| [RADIO-FRESHNESS](RADIO-FRESHNESS-TRACK.md) | 5G/6G PHY + RAN | XPROTO-CSI, -BEAM, -AICSI, -HO, -URLLC, -PHY, -CCA |
| [QUANTUM-COMPUTING](QUANTUM-COMPUTING-TRACK.md) | quantum devices | XPROTO-QUANTUM (calibration/backend-selection) |
| [MARKETS-FRESHNESS](MARKETS-FRESHNESS-TRACK.md) | market microstructure | XPROTO-QUOTE, portfolio tr(P·Σ) |
| [OPTICAL-FRESHNESS](OPTICAL-FRESHNESS-TRACK.md) | optical networks | XPROTO-QOT (QoT-certificate vacuity, GNPy) |
| [GRID-FRESHNESS](GRID-FRESHNESS-TRACK.md) | power systems | XPROTO-GRID (state-estimation staleness, pandapower) |

## Seal provenance across the re-home (binding)

Cells sealed in `network-governor` keep their **original registration IDs**
(`XPROTO-*`) and their original sealing acts. Their `SEALS.md` rows here cite the
**original network-governor sealing commit** and the **SHA-256 of the sealed file
content at that commit**, so the seal remains verifiable against network-governor's
history (`git -C network-governor show <commit>:<path> | sha256sum`). Re-homing
relocates files; it does **not** re-seal. Post-re-home cells seal natively here.

See [MIGRATION.md](MIGRATION.md) for the file-level manifest and status.
