# P3787 contribution — 10-minute working group presentation

**Outline for slides. DRAFT v0.1, 2026-08-27. Owner presents.**

Companion to `ieee-p3787-freshness-attestation.md` (the written
contribution) and `ieee-sa-ic-freshness-whitepaper.md` (background).

Ten minutes is roughly nine slides plus a backup pile. The ask on the
last slide is the point of the talk; everything before it exists to make
that ask answerable.

---

## Slide 1 — Title

**Freshness and Validity Attestation for Policy-Carrying Data Objects**

Andrew H. Bond, San José State University. Contribution to P3787.

*Say:* who I am in one sentence, and that the proposal is one metadata
class plus one conformance obligation, not a redesign.

---

## Slide 2 — Where this sits in the scope

Three columns from the PAR scope, with a question mark under the middle:

| Who may use it | Is it still good? | Was it altered? |
|---|---|---|
| usage control, authorization | **(no home today)** | binding, attestation |

*Say:* P3787 answers columns one and three well. The proposal is about
the middle column. Validity is orthogonal to authorization: a party can
be fully authorized and the payload still useless to it.

---

## Slide 3 — The hook (one number)

Same coordination-service replica. Same instant. Two readers.

- Reader with a **hot** working set: stale on roughly **99%** of reads
- Reader with a **cold** working set: stale on roughly **1%**

*Say:* nothing about the replica differs between these two readers. What
differs is what each one reads. A single per-object expiry is wrong for
one of them by two orders of magnitude. This is the whole argument in one
slide; everything else is consequence.

---

## Slide 4 — Three gaps, stated as format problems

1. **Validity is consumer-relative; expiry is a scalar.** One number
   attached to the object cannot be right for heterogeneous readers.
2. **Attestation proves intactness, not correctness-in-use.** An
   enforcement point verifies the binding, not the truth of the
   assertion at the moment of use.
3. **Decay is unsignalled revocation.** Revocation is scoped as an
   explicit act. An object whose condition has decayed is operationally
   revoked and nothing says so.

*Say:* these are one gap seen three ways. There is no field to carry what
makes the payload still good for this reader now, and no obligation to
check it.

---

## Slide 5 — What "wrong" costs, measured

Rate at which a conventional assertion cleared a use whose independently
witnessed outcome failed:

| Substrate | Conventional assertion | False-clear | Witnessed alternative |
|---|---|---|---|
| Interdomain routing (BGP) | quiescence implies converged | 0.351 | posterior detector |
| Interdomain routing (IS-IS) | same | 0.184 | same |
| Replicated database | replica lag under threshold | ~0.50 | ~0.02 to 0.06 |
| Cellular physical layer | channel report implies rate | 0.34 to 0.37 | 0.10 |

*Say:* each produced under sealed pre-registration, thresholds committed
before the graded run, failing runs kept. Statuses stated as recorded.
The point is not any single number. It is that the same failure mode
appears in unrelated substrates, and that it is measurable wherever an
independent witness exists.

---

## Slide 6 — Proposed: a validity attestation class

Four terms in the metadata:

- **Consumer class and read operator.** Which projection of the state the
  reader depends on. Distortion experienced is `tr(P_C · Σ)` to second
  order; the conventional whole-state case is `P_C = I`. Validity
  constraints are indexed by consumer class, not a scalar expiry.
- **Witness.** The independent, substrate-native measurement that grades
  the assertion (log sequence number, acknowledgement, monitor feed,
  realized outcome). Assertions with no named witness are marked
  **inferred** and are distinguishable in the format from **witnessed**.
- **False-clear rate.** The reportable conformance metric, per consumer
  class, with the conditions under which it was measured.
- **Refresh floor.** Maximum renewal interval holding false-clear at
  target, derived from the decorrelation timescale rather than convention.

One conformance obligation:

> An enforcement point re-evaluates validity **at use time, against the
> requesting consumer class**, not solely at binding or transfer. A lapse
> is treated as revocation for that use and recorded on the audit
> interface.

*Say:* technology and algorithm agnostic, consistent with the PAR. No
cryptographic suite, no serialization, no protocol behavior.

---

## Slide 7 — Where it attaches

| P3787 element | Addition |
|---|---|
| Metadata format | Validity attestation block |
| Usage-control enforcement | Use-time re-evaluation per consumer class |
| Audit and attestation | Witnessed vs inferred; false-clear rate; lapse events |
| Revocation | Validity lapse as an implicit, separately auditable state |
| Conformance | Per-consumer-class reporting; inferred assertions declared |
| Registries | Witness types per substrate profile (thin) |

*Say:* this is deliberately small. Six touch points, one new block.

---

## Slide 8 — It already runs

`turboquant-pro`: MIT licence, on PyPI, archived with a DOI. Ships the
consumer-relative quantity as a gated number and a distribution-free
certificate that a third party who did not produce it can re-verify.

Also from that work: a compression reaching 0.995 cosine similarity on
transformer key vectors degraded the downstream task metric by orders of
magnitude. The proxy certified a payload that was unusable for the reader.

*Say:* offered to the group as an interoperability example for the class,
not as a candidate for normative reference.

---

## Slide 9 — What I am not proposing, and the ask

Not proposing: a cryptographic suite, a serialization, protocol behavior
for any substrate, or any change to the existing usage-control semantics.
Per-domain profiles belong to the bodies that own those substrates.

**Ask the group three questions:**

1. Is validity in scope for P3787 as the group reads the PAR, or is it
   adjacent work for someone else?
2. If in scope, does it belong in the metadata format clause, the
   enforcement clause, or its own?
3. What would the group want to see next: draft normative text, a
   worked profile for one substrate, or evidence for more substrates?

*Say:* I am asking the group to route this, not to adopt it today.

---

## Backup slides (hold, do not present)

- **B1.** The refresh-floor measurement: admissible report period scaled
  linearly with coherence time, slope approximately 0.177, R² approximately
  0.92; no predictor extended the horizon past one coherence time.
- **B2.** The sealed pre-registration discipline in six lines (bars before
  runs, named witness, declared consumer, manipulation checks as bars,
  cooling-off and disjoint evaluation, kept failures).
- **B3.** Why authorization and validity are orthogonal, with the
  authorized-but-stale case worked through.
- **B4.** The information-theoretic account: a description adequate for
  one reader is provably not adequate for another, and the gap is exactly
  computable in the Gaussian case (T-IT submission, 2026).
- **B5.** Full cross-domain evidence table from the whitepaper, with
  statuses and the cells where the effect did not appear.

---

## Presenter notes

- Lead with slide 3. If the group only remembers one thing, it should be
  99 versus 1 on the same replica.
- Do not oversell the thermodynamic or information-theoretic framing in
  this room. It is background, and it invites a scope argument that costs
  time without advancing the ask.
- Statuses are stated as recorded. If asked about a cell that did not
  replicate, say so plainly and offer the record.
- The patent policy call happens before or during the meeting. Have the
  institutional disclosure position settled before presenting, not
  discovered live.
