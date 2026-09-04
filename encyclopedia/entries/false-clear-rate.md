# false-clear rate

**id.** false-clear-rate
**kind.** concept

## definition

A certificate is a claim, made at a time, that something is safe to act on. A witness is an
independent measurement of whether the claim was true. The false-clear rate is the fraction
of the decisions the certificate cleared in which the witness said otherwise. It is
conditional on clearing and is reported beside the certificate's coverage, the fraction of
decisions it clears, because a certificate that clears nothing has a false-clear rate of zero
and no use. A certificate whose false-clear rate exceeds the target it claims is vacuous for
that consumer. The rate is a property of the certificate and the consumer together, read
through the consumer's read operator, not of the certificate alone.

## equation

    FC = Pr[ W refutes | C_t clears ],   coverage = Pr[ C_t clears ].

The joint rate, cleared and wrong over all decisions, is the product of the two. A naive
certificate clears everything, so its coverage is one and its joint and conditional rates
coincide. Book equation 0.26, restated as equation 13.1 with the drift term
d_O(Δ) = tr(P_C Σ_drift(Δ)).

## ledger

- The freshness program is the operational, measurement side of the theory and reads
  tr(P_C Σ) in freshness rather than allocation.
  `observation-theory-campaigns/experiments/FRESHNESS-PROGRAM.md:1-30` at edd1f25.
- Volume 14 chapter 19 carries the definition and the two properties inherited from the
  allocation theory, consumer relativity and measurability wherever a witness exists.
  `geometric-observation/chapters/ch19_the_certificate_that_ages.md:61-76` at 7d91883.

## first stated

Volume 14 chapter 19, "the certificate that ages", and the freshness program's umbrella
document, re-homed into observation-theory-campaigns on 2026-08-24 from the network-governor
program.

## measurements

| Cell | Certificate, witness | Naive to witnessed | Source |
|---|---|---|---|
| XPROTO-PG, Postgres with delayed apply | replica fresh, WAL position | about 0.50 to about 0.06 | `observation-theory-campaigns/experiments/DATABASE-FRESHNESS-TRACK.md:23` at edd1f25 |
| XPROTO-MG, MongoDB delayed secondary | replica fresh, oplog timestamp | about 0.47 to about 0.03 | same file, line 24 |
| XPROTO-PGX, production Postgres under network lag | replica fresh, WAL position and the statements footprint | about 0.47 to about 0.02 | same file, line 25 |
| XPROTO-ZK, ZooKeeper 3.9 ensemble | zxid, sync | hot reader 0.99, cold reader 0.01, witnessed 0.0 | same file, line 27 |
| XPROTO-CSI, channel quality to modulation | HARQ | 0.34 to 0.37, then 0.10 | `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:25` at edd1f25 |
| XPROTO-BEAM, mmWave beam index | HARQ | 0.31 to 0.02 | same file, line 26 |
| XPROTO-AICSI, neural channel reconstruction | precoder and HARQ | reconstruction wins, yet 0.28 to 0.13 only under the witness | same file, line 27, scope-corrected 2026-08-25 |
| XPROTO-HO, handover by signal strength | radio-link failure | 0.31 to 0.44, then 0.09 to 0.12 | same file, line 28 |
| XPROTO-PHY, precoding, rank, timing | HARQ | 0.27 to 0.42, then 0.055 to 0.13 | same file, line 30 |
| routing quiescence, BGP, IS-IS, OSPF | second collector | 0.351, 0.184, 0.083 | `observation-theory-campaigns/experiments/ROUTING-TELEMETRY-TRACK.md:130-150` |
| XPROTO-LLM, a benchmark score as a certificate for deployment slices | true accuracy per slice | benchmark 0.909 against target 0.8, naive policy false-clears 0.333 of thirty slices, aware policy 0.033, deployment mean 0.736, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns/experiments/LLM-EVAL-TRACK.md:1-50` |

The ZooKeeper row is the clearest statement that the rate belongs to the pair. The same
replica read by a hot reader and a cold reader gives 0.99 and 0.01, and an aggregate over
both describes neither.

## failures and corrections

- The refresh-floor law. An unsealed exploration fit a floor of about 0.177 times the
  coherence time with R² 0.915, measured at a relaxed 0.15 threshold against the 0.10
  target, with a fresh baseline that never met the budget. Refuted. The record is kept and
  not cited. `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:41-50`,
  `observation-theory-campaigns/analysis/csi/CSI-refreshfloor.json:2,111-114`. Its sealed
  replacement calibrated the baseline first and found floors of a few milliseconds at 10 Hz
  and one transmission interval at 50 Hz and above, `analysis/csi/PREREG-XPROTO-CSI-SWEEP2.md:1-60`,
  sealed 1d3de4a. Volume 14's book outline still cites the refuted law, an open item.
- XPROTO-AICSI scope correction, 2026-08-25. The reconstruction-versus-consumer dissociation
  does not survive the community-standard substrate. On real 3GPP CDL-C with a CsiNet-class
  codec the reconstruction-optimal codec reconstructs near-perfectly and false-clears 0.0.
  The v1 seal stands for what it tested. `observation-theory-campaigns/experiments/RADIO-FRESHNESS-TRACK.md:33-39`.
- Definition corrected 2026-09-03. Volume 14 and the book had written the joint probability
  Pr[clears ∧ refutes]. Both now state the conditional rate with coverage beside it, which is
  the form every measured cell already reported. geometric-observation 7d91883,
  observation-data-mining a0b20ff.

## conditions

- A witness must exist. Where none exists the rate is not measurable and the certificate is
  unassessed, not safe.
- The rate is per consumer. A report gives it per read operator, or per slice, group, or
  footprint, and never as one aggregate that a hot reader and a cold reader would both
  disown.
- Coverage is reported with it. A witnessed certificate clears fewer decisions than a naive
  one, and the two numbers are read together.

## machine checked

none

## used in

- *Data Mining as Observation* chapters 0, 12, 13, and 14, and the deployment report template.
- Volume 14 chapters 19 and 20.
- Papers of the freshness program, published by DOI as listed in the campaigns README.

## related

certificate, witness, coverage, coherence-time, refresh-floor, min-over-strata

## status

Hand-filled 2026-09-03 from observation-theory-campaigns at edd1f25, geometric-observation at
7d91883, and observation-data-mining at a0b20ff. Not yet generated.
