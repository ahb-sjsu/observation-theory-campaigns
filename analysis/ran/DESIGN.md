# An Observation-Theory Freshness Governor for the O-RAN RIC

*Design + standardization note, 2026-08-23. The RAN embodiment of the
network-governor thesis: every 5G/6G adaptation certificate ages and can
false-clear; grade it against its witness, refresh it at the coherence floor,
price it to the consumer. This note gives the architecture, the O-RAN mapping,
a deployable MVP, and the standards path.*

## 1. The observation

The deployed 5G loops -- outer-loop link adaptation (OLLA), beam-failure
recovery (BFR), radio-link monitoring (RLM), the HARQ and timing-advance loops,
rank/precoder adaptation -- are *already* witnessed corrections. But they are
**fragmented** (a separate hand-tuned loop per certificate), **uncalibrated**
(no loop reports its own false-clear rate), and **not consumer-relative** (a
single CQI serves an eMBB and a URLLC flow with the same aggressiveness). The
governor is the common layer beneath them: one place that measures the
false-clear rate and the refresh floor of every certificate, per consumer, and
governs the loops accordingly.

Certificates and their witnesses (all measurable today):

| certificate | decision | witness | ages with | cell |
|---|---|---|---|---|
| CQI | MCS | HARQ ACK/NACK | Doppler / T_coh | XPROTO-CSI (sealed) |
| beam index / L1-RSRP | beam | HARQ / beam-failure | angular coherence | XPROTO-BEAM |
| CSI feedback | precoder | HARQ / achieved SINR | codec trained on NMSE | XPROTO-AICSI |
| RSRP report | serving cell | post-HO RLF | shadowing + fade | XPROTO-HO |
| reliability target | MCS + mechanism | HARQ vs the slice budget | (per-consumer) | XPROTO-URLLC |
| PMI / RI / TA | precoder / rank / UL timing | HARQ / UL decode | angular / rank / delay | XPROTO-PHY |

## 2. Where it lives: the O-RAN RIC

Not in the inner MAC/PHY loops -- in the RAN Intelligent Controller, the
standardized home for cross-loop intelligence.

- **non-RT RIC (rApp, > 1 s):** the governor proper. Ingests the certificate and
  witness streams over **E2 / E2SM-KPM**; computes per-consumer false-clear and
  T_coh -> refresh floor; sets **A1 policy**.
- **near-RT RIC (xApp, 10 ms - 1 s):** enacts it via **E2SM-RC** -- tunes report
  cadence, OLLA target, BFR/RLM/TA thresholds, diversity order, per UE/slice.

The rApp is **deployable today on existing E2SM-KPM measurements with no standard
change** -- the false-clear rate is simply not a first-class KPI in any RAN, so
surfacing it is a pure observability win before any control action.

## 3. What the governor does (observe -> measure -> govern -> certify)

1. **Observe** -- certificate value + witness outcome per UE / slice / beam.
2. **Measure** -- the sealed-cell metrics live: consumer-relative false-clear
   (rolling) and coherence time -> refresh floor (k * T_coh).
3. **Govern** -- refresh each certificate at its floor *for that consumer's
   target*; withhold aggressive decisions when the witness says the certificate
   is vacuous (the "don't false-clear" guard); choose the *mechanism*, not just
   the parameter (URLLC lesson: below a coherence time, margin alone fails --
   switch on diversity).
4. **Certify** -- emit a calibrated, witnessed reliability certificate per served
   flow, carrying its measured false-clear rate. This is the SLA-grade artifact
   URLLC and network slicing need and lack today.

`governor.ran` (see `ran_governor.py`) is the reference: a `RanGovernor` running
a `FalseClearMeter` + `RefreshFloorEstimator` per (certificate, consumer),
emitting a `GovernanceDecision` (report period, mechanism, certified false-clear).
It is the RAN generalization of `governor.sealed` / `governor.detector`.

## 4. What is deployable now vs. worth standardizing

- **Now (rApp, no standard change):** false-clear as a first-class KPI;
  slice-aware refresh-floor tuning; the calibrated per-flow certificate as an
  rApp output. Overhead-aware: the floor is a *minimum* report rate, traded
  against uplink signalling and UE battery -- the governor optimizes above it.
- **Standard extensions (E2SM / 6G-native):** witness-first reporting (a
  consumer declares the freshness it needs and receives a *certified* answer --
  the freshread/ZooKeeper lesson, alongside CQI/CSI); consumer-relative
  reporting (the reliability target + resource footprint as the read operator
  P_C); the refresh floor as a published bound.

## 5. 6G-native

- Certify learned components on the **witness, not reconstruction** (AICSI:
  train/gate CSI codecs on HARQ, not NMSE).
- **Cap prediction at the coherence time** (the prediction-wall result): an
  AI-native scheduler must not over-report reliability past T_coh -- for a
  Gaussian fading process the Wiener predictor is optimal and blind beyond T_coh.
- **Gate instantaneous CSI feedback on RTT < T_coh** (NTN): the governor decides
  per link whether closed-loop CSI is viable, else statistical/predictive CSI or
  diversity.
- **Cell-free / RIS:** "which AP or RIS config serves me" is nearest-*certified*
  routing (the geo-fleet cell) at the RAN.

## 6. Standardization path (layered; lead where the concept is domain-general)

The RAN core is 3GPP + O-RAN, not IEEE; 3GPP is company-driven. Match each layer
to its body and use IEEE-SA where the concept is general.

- **IEEE-SA Industry Connections activity + whitepaper** on *consumer-relative,
  witnessed freshness/reliability certification* -- domain-general (Wi-Fi /
  cellular / routing / DB), low barrier to **initiate and chair** as a Senior
  Member; incubates toward an IEEE **Recommended Practice** (a measurement RP is
  IEEE-native and dodges the 3GPP turf problem). Strong co-sign target: a
  distributed-systems / networking name (e.g., a ZooKeeper-lineage collaborator).
- **IEEE 802.11** -- the Wi-Fi instance (the OT-governed 802.11 freshness draft);
  direct participation via SA membership.
- **O-RAN Alliance** -- WG1 use case, WG2 rApp/A1, WG3 E2SM; + **OSC** as an open
  reference rApp (this module). Academic membership via the institution.
- **3GPP** -- PHY/slicing specifics, via an O-RAN->3GPP liaison or a study-item
  pitch through a member org (longest path; do not lead with it).
- **IEEE Future Networks / INGR** -- a "freshness governance" roadmap section
  (high influence, low barrier).
- **Publish first** (IEEE journals/confs, already in flight) for priority/citation.

**Sequence:** publish -> open reference rApp -> IEEE IC whitepaper (consensus) ->
formal PARs / O-RAN contributions. **First step:** an IEEE-SA IC whitepaper you
initiate + an O-RAN WG1 use-case submission.

## 7. Honest boundaries

The governor **unifies and calibrates; it does not replace** the inner loops.
Near-term value is an observability KPI (false-clear) and slice-aware tuning, not
a revolution. Standardization is slow -- the rApp path is real now; E2SM / 6G
extensions are years. And the refresh floor always trades against signalling
overhead; that trade-off is the governor's real job, not a solved problem.
