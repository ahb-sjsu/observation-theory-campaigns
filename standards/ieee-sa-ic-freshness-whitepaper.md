# Consumer-Relative, Witnessed Freshness and Reliability Certification
### A Cross-Domain Measurement Methodology

**IEEE Standards Association — Industry Connections Whitepaper (DRAFT v0.1, 2026-08-23)**

Proposed IC activity lead: Andrew H. Bond, Senior Member, IEEE — Department of
Computer Engineering, San José State University.

*This draft is written to seed an IEEE-SA Industry Connections (IC) activity. IC
activities and their whitepapers are pre-standardization; participation is open
to any interested party, IEEE membership not required. Nothing here is normative.*

---

## Executive summary

Networked and distributed systems constantly issue **certificates of freshness or
reliability**: a Wi-Fi clear-channel assessment ("the medium is idle"), a
cellular channel-quality report ("this rate is supportable"), a database
bounded-staleness read ("this replica is fresh enough"), a routing
convergence signal ("the network has settled"), a risk number ("this book is
within limits"). Each asserts that a decision is safe. Each can be **wrong in a
way the issuer cannot see** — because it ignores *what the specific consumer
reads*, and because it is *inferred* rather than *graded against an independent
measurement*.

This whitepaper proposes a single, domain-general way to state and **measure**
such claims: a certificate should be (1) **consumer-relative** — evaluated
through the read operator of the actual consumer; (2) **witnessed** — graded
against an independent measurement of the true outcome; and (3) refreshed within
its **coherence floor** — the timescale over which the certified condition
decorrelates. The central metric is the **false-clear rate**: how often a
certificate says "safe" when the witnessed outcome is not. Across five domains we
find naive certificates that false-clear at rates far above the target they
purport to guarantee, and witnessed alternatives that hold at target.

We propose an IC activity to develop this into an IEEE **Recommended Practice**
for freshness/reliability certification and its measurement, with per-domain
profiles, complementing (not duplicating) 3GPP, O-RAN, IEEE 802, and IETF work.

---

## 1. Motivation

Reliability and freshness guarantees are pervasive and load-bearing, yet they are
almost always **asserted, not measured**. A lag threshold, a convergence timer, a
confidence interval, a Value-at-Risk — each is trusted operationally, but its
**error rate is rarely a first-class, reported quantity**, and it is rarely
evaluated relative to the specific consumer that depends on it. When such a
certificate is wrong, the failure is silent until the witnessed outcome (a
collision, a decode failure, a stale read, an outage, a loss) reveals it.

Three structural gaps recur across domains:

- **Consumer-blindness.** A single certificate serves heterogeneous consumers as
  if they were identical. The freshness a consumer *feels* depends on what it
  reads; a certificate computed for the average, the benchmark, or the aggregate
  can be adequate for one consumer and catastrophic for another *at the same
  instant*.
- **No witness.** The certificate is inferred from a proxy (silence, a lag bound,
  a reconstruction error, an explained-variance figure) rather than graded
  against an independent measurement of the outcome it predicts.
- **No refresh floor.** The cadence at which a certificate must be renewed is set
  by convention, not derived from the coherence time of the condition it
  certifies; too-slow renewal makes the certificate stale-on-use.

These are not domain quirks; they are the same three gaps. A common methodology
is therefore both possible and useful.

---

## 2. The core concept

**Certificate.** A report that induces a decision intended to satisfy a target
(a medium-idle assessment → transmit; a CQI → a modulation and coding scheme; a
lag bound → serve a read; a convergence signal → trust routes; a risk number →
hold a position).

**Consumer and read operator.** The consumer is the entity that acts on the
certificate, with a metric on its own outcome. Its **read operator** `P_C`
encodes *which part of the underlying state it actually feels*. The distortion a
consumer experiences from an error with second moment `Σ` is, to second order,

> `d_C = tr(P_C · Σ)`

— the error read through the consumer. Ordinary "average" or "reconstruction"
metrics are the special case `P_C = I`. Two consumers with different `P_C`
experience different reliability from the identical underlying state; portfolio
risk `wᵀΣw = tr(w wᵀ Σ)` is exactly this form, with the portfolio as `P_C`.

**Witness.** An independent measurement of the true outcome, native to the
substrate: a receiver-side collision indicator, a hybrid-ARQ ACK/NACK, a
write-ahead-log sequence number, a routing-monitor feed or dataplane probe, a
realized return. A certificate is **witnessed** when it is graded against the
witness rather than inferred.

**False-clear rate.** The rate at which the certificate clears a decision whose
witnessed outcome violates the consumer's target. This is the proposed
first-class metric. A certificate whose false-clear rate exceeds the target it
claims to guarantee is **vacuous** for that consumer.

**Refresh floor.** The maximum renewal interval that keeps the false-clear rate
at target is proportional to the **coherence time** of the certified condition
(its de-correlation timescale). Certificates must be refreshed within this floor;
prediction cannot extend the horizon beyond one coherence time when the
underlying process is memoryless past it.

---

## 3. Evidence base (cross-domain, measured)

The following are representative measurements under the pre-registered discipline
of Section 4. "naive" is the conventional certificate; "witnessed" is the
consumer-relative, witnessed alternative. Status is marked honestly.

| Domain | Certificate → decision | Witness | naive false-clear | witnessed | status |
|---|---|---|---|---|---|
| Interdomain routing | quiescence (60 s silence) → converged | monitor / dataplane | 0.351 (BGP), 0.184 (IS-IS), 0.083 (OSPF) | posterior detector, 30–120 s band | sealed |
| Distributed data (SQL/NoSQL) | replica-lag → serve read | WAL LSN / oplog ts | ≈0.50 (two-sided) | ≈0.02–0.06 (footprint cert) | sealed |
| Coordination (ZooKeeper) | local read → serve | zxid | 0.99 (hot) vs 0.01 (cold), same replica | ≈0 (sync/watermark) | pre-registered |
| Cellular 5G NR (real PHY) | CQI → MCS | HARQ ACK/NACK | 0.34–0.37 | 0.10 (outer-loop) | sealed |
| Cellular 5G NR | reliability target (eMBB vs URLLC) | HARQ vs slice budget | ≈100× budget (URLLC on an eMBB cert) | ≈1e-4 (consumer-aware + diversity) | pre-registered |
| Finance (illustrative) | risk model (99% variance) → "within limits" | realized returns | VaR breached 48% (nominal 1%) | ≈nominal (consumer-aware) | illustrative |

Two cross-cutting results:

- **Consumer-relativity is stark.** On the *same* ZooKeeper follower at the same
  instant, a hot-footprint reader is 99% stale while a cold-footprint reader is
  1% stale — a 99× difference from *what the reader reads*, not the replica. A
  risk model explaining 99% of market variance rates a book near-riskless while
  its consumer-relative risk is thousands of times larger.
- **A refresh-floor law.** On a real 5G NR physical layer, the maximum report
  period holding false-clear at target scales linearly with coherence time
  (measured slope ≈ 0.177, R² ≈ 0.92); and the optimal linear predictor cannot
  extend the usable horizon past one coherence time (information-theoretic for a
  Gaussian fading process).

The point is not any single number; it is that **one grammar — certificate,
consumer read operator, witness, false-clear rate, refresh floor — recurs across
independent domains**, and that the false-clear rate is measurable wherever a
witness exists.

---

## 4. The proposed measurement methodology

To make a reliability claim falsifiable rather than asserted, we propose a
**sealed pre-registration** discipline, which the Recommended Practice would
codify:

1. **Bars before runs.** Numeric pass/fail thresholds (including the target the
   certificate claims) are committed in a pre-registration *before* the graded
   measurement.
2. **Witness requirement.** The certificate is graded against an independent
   witness, named in the pre-registration; inference-only claims are out of
   scope for certification.
3. **Consumer read operator.** The consumer(s) and their read operators / targets
   are declared; the false-clear rate is reported per consumer.
4. **Manipulation checks.** Checks that the effect is real (the condition
   genuinely ages; a fresh certificate is sane; the certificate is exercised) are
   themselves bars — any failure voids the result.
5. **Cooling-off and disjoint evaluation.** A structural delay between
   construction and sealing, and evaluation on data/seeds disjoint from
   calibration, both enforced in code.
6. **Kept failures.** A failing graded run is recorded as executed; the
   methodology has no escape hatch.

This is deliberately domain-general: it standardizes *how a freshness/reliability
claim is stated and measured*, not the protocol behavior of any one system.

---

## 5. Relationship to existing standards

This activity is **complementary and non-duplicative**:

- **IEEE 802 (e.g., 802.11).** The medium-access freshness instance (clear-channel
  assessment vs a receiver-side witness) is a natural first profile; coordinates
  with 802.11 working groups and a companion IETF measurement draft.
- **3GPP / O-RAN.** Cellular certificates (CQI, CSI, beam, RSRP/handover,
  PMI/RI/TA, reliability target) are 3GPP/O-RAN's normative remit. The proposed
  RP contributes *measurement and certification methodology* (the false-clear
  KPI, the refresh floor), realizable as an O-RAN RIC rApp on existing
  measurements, and offered to O-RAN/3GPP by liaison rather than duplicated.
- **IETF.** Measurement-methodology alignment (e.g., performance-metric
  registries) and the routing/dataplane instances.
- **Distributed systems / databases.** No single normative body; the RP offers a
  vendor-neutral certification others can adopt.

The RP's value is the **cross-domain common core** plus thin per-domain profiles,
which no single existing body owns.

---

## 6. Proposed IC activity and path forward

**Activity.** An IEEE-SA Industry Connections activity, "Freshness and Reliability
Certification" (working title), open to operators, vendors, cloud/database
providers, academics, and standards liaisons.

**Deliverables.** (a) this whitepaper, expanded with contributed evidence; (b) a
reference open-source measurement harness and certificate-governor (a RAN RIC
rApp reference exists); (c) a draft **Recommended Practice** scope and PAR.

**Path.** IC Activity Initiation via ICCom → whitepaper + workshops to build
consensus → a Project Authorization Request for an IEEE **Recommended Practice**
(a measurement/methodology RP, sponsored by an appropriate IEEE society/standards
committee, approved by NesCom) → per-domain profiles. Publishing peer-reviewed
results in parallel establishes the technical basis.

**Why an IC activity first.** The concept is new and cross-cutting; IC is the
low-barrier vehicle to establish shared definitions (false-clear rate, witness,
read operator, refresh floor) and gather multi-party evidence before committing a
PAR — and it is open to non-members, widening participation.

---

## 7. Call to participation

We invite participants from radio access (3GPP/O-RAN), Wi-Fi (IEEE 802.11),
distributed data and coordination systems, interdomain routing, and quantitative
finance to contribute domain evidence, review the definitions, and co-develop the
per-domain profiles. Contributors interested in the measurement harness,
reference governor, or co-authoring the Recommended Practice scope are especially
welcome.

---

## References (indicative)

1. A. H. Bond, "Observation Theory: Geometry, Distortion, and Reliability as
   Properties of Observation," submitted to IEEE Trans. Information Theory, 2026.
2. A. H. Bond, applied-instance papers (radio-access, distributed databases,
   coordination services), 2026; sealed pre-registrations and reference code,
   https://github.com/ahb-sjsu/geometric-observation .
3. S. Kaul, R. Yates, M. Gruteser, "Real-Time Status: How Often Should One
   Update?," IEEE INFOCOM, 2012.
4. P. Bailis et al., "Probabilistically Bounded Staleness for Practical Partial
   Quorums," Proc. VLDB Endowment, 2012.
5. P. Hunt, M. Konar, F. Junqueira, B. Reed, "ZooKeeper: Wait-Free Coordination
   for Internet-Scale Systems," USENIX ATC, 2010.
6. O-RAN Alliance, Working Group specifications (non-RT/near-RT RIC, E2SM).
7. IEEE-SA Industry Connections process (ICCom) and Standards Development
   (PAR/NesCom) documentation.
