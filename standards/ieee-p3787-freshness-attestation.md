# Freshness and Validity Attestation for Policy-Carrying Data Objects

### A proposed contribution to IEEE P3787 (Secure Data Encapsulation)

**DRAFT v0.1, 2026-08-27. Owner reviews and submits. Not submitted by the assistant.**

Proposed contributor: Andrew H. Bond, Senior Member IEEE, IEEE SA member.
Department of Computer Engineering, San José State University.

---

## 1. Why this project

IEEE P3787, "Secure Data Encapsulation: Policy-Carrying Data Objects,
Enforcement Interfaces, and Conformance Requirements," has an approved PAR
(NesCom, October 2025, running to December 2029) under the Computer
Society. Its scope covers a machine-readable policy-carrying metadata
format cryptographically bound to a data payload, and the interfaces for
creation, binding, transfer, storage, usage-control enforcement,
audit and attestation, revocation, and destruction, with conformance
requirements for producers, consumers, enforcement points, validators,
auditors, and registries.

The PAR is recent, so the draft is being written now. A contribution at
this stage can add a metadata class rather than argue against finished
text.

## 2. The gap

A policy-carrying object as scoped can state **who** may use a payload,
**under what conditions**, and **until when**. Three properties that
production systems depend on are not expressible:

1. **Validity is consumer-relative, and expiry is not.** A wall-clock
   time-to-live is a single number attached to the object. The freshness a
   party actually experiences depends on which part of the underlying
   state that party reads. Two consumers holding the identical object at
   the identical instant can be in opposite validity states. This is
   measured, not conjectural: on the same replica of a coordination
   service at the same instant, a reader whose working set is hot is
   stale on roughly 99% of reads while a reader whose working set is
   cold is stale on roughly 1%. A single per-object expiry cannot be
   correct for both.

2. **Attestation is intactness, not correctness-in-use.** An enforcement
   point can verify that the metadata is bound to the payload and
   unaltered. It cannot verify that the assertion the metadata carries
   was true when acted upon. The distinction has a measurable cost: an
   assertion that is inferred from a proxy rather than graded against an
   independent measurement of the outcome it predicts can clear decisions
   that fail. Across independently sealed measurements, proxy-based
   assertions cleared unsafe decisions at rates from 0.18 to 0.50
   depending on the substrate, against nominal targets orders of
   magnitude lower.

3. **Decay is unsignalled revocation.** P3787 treats revocation as an
   explicit act by an authorized party. An object whose asserted
   condition has decayed past the consumer's tolerance is, operationally,
   revoked, but nothing in the system says so. Enforcement points
   evaluate policy at binding time and at transfer time; nothing requires
   re-evaluation of validity at use time against the consumer that is
   using it.

These three are one gap: the encapsulation format has no place to say what
makes the payload still *good for this reader now*, and no interface
obligation to check it.

## 3. Proposed contribution

We propose a **validity attestation** class in the policy-carrying
metadata, with four defined terms and one conformance obligation. The
terms are domain-general and carry no cryptographic-suite or
implementation mandate, consistent with the project's technology-agnostic
scope.

**3.1 Consumer class and read operator.** A consumer class declares which
projection of the underlying state the consumer depends on. Where the
state error has second moment `Σ`, the distortion the consumer
experiences is, to second order, `tr(P_C · Σ)`, with `P_C` the consumer's
read operator. The conventional case, in which validity is computed
against the whole state or a benchmark, is `P_C = I`. The metadata
carries validity constraints indexed by consumer class rather than a
single scalar expiry.

**3.2 Witness.** The independent measurement, native to the substrate,
against which the object's assertion can be graded: a write-ahead-log
sequence number, an acknowledgement or negative acknowledgement, a
monitor feed, a realized outcome. The metadata names the witness that
grades its assertion. An assertion with no named witness is declared
**inferred** and is distinguishable, in the format, from one that is
**witnessed**.

**3.3 False-clear rate.** The rate at which the object's assertion clears
a use whose witnessed outcome violates the consumer's target. This is the
proposed reportable conformance metric for a validity attestation. An
attestation whose false-clear rate for a consumer class exceeds the
target it asserts is **vacuous** for that class, and the format should be
able to express the measured rate and the conditions under which it was
measured.

**3.4 Refresh floor.** The maximum renewal interval that holds the
false-clear rate at target, derived from the decorrelation timescale of
the certified condition rather than set by convention, and measured at
the target the assertion actually claims. In a cellular physical-layer
substrate with controlled coherence time, the admissible report period at
a 0.10 block-error budget collapsed to four to six transmission intervals
at 10 Hz Doppler, two to three at 25 Hz, and a single interval at 50 Hz
and above, across three sealed seeds.

That substrate also supplies the cautionary case for why the format must
carry measurement conditions. An earlier exploration on the same
substrate appeared to show the admissible period scaling cleanly with
coherence time, but it had measured its floors at a relaxed threshold
while reporting against the tighter target. Recomputed at the asserted
target, with the fresh baseline first calibrated to meet that target, no
proportional law survives. A refresh floor is meaningful only alongside
the target and calibration it was measured under, which is precisely why
the metadata carries the floor, its target, and its derivation basis
rather than the floor alone.

**3.5 Conformance obligation.** An enforcement point claiming conformance
to the validity attestation class re-evaluates validity **at use time,
against the requesting consumer class**, not solely at binding or
transfer. Where an object's validity has lapsed for that class, the
enforcement point treats the object as revoked for that use and records
the event on the audit interface.

## 4. Where this attaches in the P3787 functional model

| P3787 element | Addition |
|---|---|
| Policy-carrying metadata format | Validity attestation block: consumer classes, witness identifier, measured false-clear rate and conditions, refresh floor and derivation basis |
| Usage-control enforcement | Use-time re-evaluation against the requesting consumer class |
| Audit and attestation | Witnessed versus inferred distinction; false-clear rate as a reportable quantity; lapse events |
| Revocation | Validity lapse as an implicit revocation state, distinct from explicit revocation and separately auditable |
| Conformance requirements | Per-consumer-class reporting; declaration of inferred assertions as such |
| Registries | Registry of witness types per substrate profile (thin, per-domain) |

Nothing here mandates a cryptographic suite, a serialization, or an
implementation, and nothing displaces the project's existing security
model. The addition is a metadata class plus one enforcement obligation.

## 5. Evidence offered

The following are public and can be cited or contributed without
restriction.

- **A public reference implementation of a consumer-relative witnessed
  certificate.** `turboquant-pro` (MIT, PyPI, Zenodo DOI) ships
  `tr(P_C · Σ)` as a gated number and a distribution-free rank
  certificate with third-party re-verification (`certify` and `verify`,
  re-hashable by a party that did not produce it). This is the proposed
  concept already reduced to running, independently checkable code.
- **A measured failure of proxy-based validity.** In the same codebase,
  a compression achieving 0.995 cosine similarity on transformer key
  vectors degraded downstream perplexity to order 10⁴. The proxy
  certified a payload that was unusable for the consumer that read it.
  This is the compression-domain twin of the replication result below.
- **Cross-domain sealed measurements** of false-clear rates for
  conventional versus witnessed assertions, in interdomain routing
  (0.351 for BGP and 0.184 for IS-IS under a quiescence assertion),
  replicated databases (approximately 0.50 for a lag-threshold assertion
  against approximately 0.02 to 0.06 for a consumer-relative witnessed
  one), and a cellular physical layer (0.34 to 0.37 against 0.10). Each
  was produced under a sealed pre-registration: numeric pass and fail
  thresholds committed before the graded run, manipulation checks as
  bars, evaluation on data disjoint from calibration, and failing runs
  recorded rather than discarded.
- **A pre-standardization whitepaper** developing the common core across
  five domains, drafted for an IEEE-SA Industry Connections activity and
  available to the working group as input.

Statuses are stated as recorded: sealed where sealed, pre-registered
where pre-registered. Cells in which the effect did not appear are
recorded as such in the source material and are available on request.

## 6. What this contribution does not propose

- No cryptographic suite, key-management scheme, or serialization.
- No protocol behavior for any specific substrate. The per-domain
  profiles are thin and belong to the bodies that own those substrates
  (3GPP and O-RAN for cellular, IEEE 802 for wireless local area
  networks, IETF for measurement registries).
- No claim that freshness subsumes the project's existing usage-control
  or access-control semantics. Validity is orthogonal to authorization: a
  party may be authorized and the payload still invalid for it.
- No replacement of expiry. Wall-clock expiry remains correct where the
  certified condition does not decay in a consumer-dependent way; the
  proposal adds expressiveness where it does.

## 7. Disclosure and intellectual property

Everything cited in Section 5 is already public, under permissive
licence, or archived with a DOI. One item is deliberately excluded from
this contribution pending institutional review: the
replication-specific mechanism of a private database administration
utility. Because a sibling public project already ships the general
consumer-relative witnessed certificate, that utility's distinguishing
novelty rests on the replication mechanism specifically, which is the
subject of an SJSU intellectual property review. It is not required for
this contribution and is not disclosed here.

Contributions to an IEEE working group are governed by the IEEE SA
patent policy and the project's own contribution terms. The owner should
confirm SJSU's position on institutional ownership before submitting
material beyond what is already public.

## 8. Suggested next actions (owner)

1. Open the P3787 project page and confirm whether the working group is
   accepting participants and when it meets. The PAR is recent, so the
   likely posture is a call for participation rather than a ballot.
2. Join the working group roster as an individual participant (IEEE SA
   membership already held).
3. Submit Sections 2 through 4 of this document as a contribution to the
   drafting discussion, with the whitepaper attached as background.
4. Offer the public reference implementation as an interoperability
   example for the validity attestation class.
5. If the working group takes the class, the per-domain profile work
   becomes the natural home for the routing and radio evidence, and the
   Industry Connections activity becomes optional rather than the
   primary path.

---

## References

1. IEEE P3787, "Secure Data Encapsulation: Policy-Carrying Data Objects,
   Enforcement Interfaces, and Conformance Requirements" (PAR approved
   October 2025). https://standards.ieee.org/ieee/3787/12288/
2. A. H. Bond, "Consumer-Relative, Witnessed Freshness and Reliability
   Certification: A Cross-Domain Measurement Methodology," IEEE-SA
   Industry Connections whitepaper draft, 2026.
   (`standards/ieee-sa-ic-freshness-whitepaper.md`)
3. `turboquant-pro`, MIT licence, https://github.com/ahb-sjsu/turboquant-pro
   (PyPI; Zenodo DOI). Consumer-relative compression with a
   distribution-free, third-party-verifiable rank certificate.
4. A. H. Bond, "Tradeoffs Between Rate and Conditional Content with
   Encoder-Observed Context," manuscript, 2026. The information-theoretic
   account of why a description adequate for one reader is not adequate
   for another.
5. Sealed pre-registrations and reference code,
   https://github.com/ahb-sjsu/geometric-observation and
   https://github.com/ahb-sjsu/observation-theory-campaigns
