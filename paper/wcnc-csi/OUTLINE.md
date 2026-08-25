# IEEE WCNC 2027 paper — the consumer-relative CSI certificate

**Working title:** *One CSI Report Cannot Serve Every Consumer: The
Consumer-Relative False-Clear Rate in 5G/6G Link Adaptation.*

**Author:** A. H. Bond (SJSU). **Venue:** IEEE WCNC 2027, Panama; PHY / signal-processing
track. **Length:** IEEE conference, ~6 pp double-column. **Deadline: 15 September 2026**
(accept 15 Jan 2027; camera-ready 8 Feb 2027) — ~3 weeks out, before OFC's 2026-10-20.

> **UPDATE 2026-08-25 — §III-C dropped.** The AICSI-v2 shakedown (CsiNet-class codec on
> real 3GPP CDL-C, Atlas) **refuted** the reconstruction-vs-consumer dissociation on the
> standard substrate: the NMSE codec reconstructs near-perfectly (NMSE ≈ 0.03) and
> false-clears **0.0** on all seeds (pre-registered kill fired). The v1 effect was an
> artifact of an under-powered MLP codec on a synthetic channel. The paper now stands on
> **two rock-solid real-Sionna results** (§III-A, §III-B). See
> `analysis/aicsi/PREREG-XPROTO-AICSI-V2.md` (REFUTED, kept negative).

## Thesis

A CSI report is a **certificate** — "the channel is good enough to send at rate X." It
is not read by "the channel"; it is read by a **consumer** — a scheduler with a
reliability target, a decoder at a moment in time. The certificate **false-clears**
(says "send" when the transmission will fail) *relative to that consumer*. We make the
false-clear rate a first-class, measured KPI on real 5G NR (Sionna LDPC decoding) and
show the CSI certificate is consumer-relative along **two axes** — the reliability
target and the refresh horizon. The witnessed corrections that hold each axis (OLLA;
a refresh) already exist; OT's contribution is the *measured, consumer-relative
false-clear rate* that says when each is needed and how much it buys.

## Why two axes, not three (rigor note)

A third candidate axis — the *training objective* of a learned CSI-feedback codec
(reconstruction NMSE vs the consumer's beam gain) — was tested rigorously and **did not
survive**. On real 3GPP CDL-C channels a CsiNet-class codec reconstructs the CSI well
enough that the reconstruction objective is *also* consumer-optimal (false-clear 0.0);
the dissociation seen in the earlier synthetic/MLP cell was a substrate artifact
(`PREREG-XPROTO-AICSI-V2.md`, REFUTED). We report only what survives the substrate the
community benchmarks on. Both surviving results stand on **real Sionna 5G NR BLER with
no learned model** — the strongest possible footing for a WCNC PHY submission.

## Structure

**§I Introduction.** The CSI report as a certificate; the consumer, not the channel,
reads it; false-clear as the missing KPI. Two axes preview.

**§II Method.** Real 5G NR link: Sionna LDPC BLER curves are the witness (HARQ decode).
Certificate = MCS/precoder selected from the CSI report; consumer = the served link's
decode. Pre-registered bars, disjoint graded seeds, content-hashed seals (cite the
campaigns repo + SEALS ledger). One paragraph per substrate.

**§III-A — Consumer-relativity in the reliability target (LEAD).** *XPROTO-URLLC,
SEALED+GRADED PASS.* The **identical** CSI certificate that meets an eMBB target
(BLER 0.10; achieved 0.112) false-clears a URLLC target (0.001) by ~**110×** (achieved
0.112); a target-aware policy reaches **1.7e-5**. Same radio state, opposite verdict by
consumer. → **Fig. 1** (bar: achieved BLER vs target, eMBB vs URLLC-naive vs URLLC-aware,
log-y). The cleanest, most defensible result; URLLC is a marquee WCNC topic.

**§III-B — Consumer-relativity in the refresh horizon.** *XPROTO-CSI + the OT-14 law,
SEALED+GRADED PASS.* At f_D = 200 Hz, stale CSI drives BLER to 0.37 vs the 0.10 target;
OLLA (the deployed witness) holds it at 0.10. Sweeping Doppler, the refresh floor obeys
**≈ 0.177·T_coh** (R² = 0.915): re-report before the channel decorrelates by that
fraction, not on a fixed period. → **Fig. 2** (refresh-floor law across f_D).

**§III-C — DROPPED.** The learned-codec objective-misalignment did not survive the
CsiNet-on-CDL substrate upgrade (refuted; see the update box at top). Optionally, a
single honest sentence in §IV notes that the reconstruction/consumer objective gap
appears only in the lossy/high-rank regime, not at practical CSI-feedback operating
points — but it carries **no figure and no headline**.

**§IV Related work.** DL CSI feedback trained on NMSE/cosine (CsiNet lineage);
outdated-CSI / CSI aging; OLLA; URLLC link adaptation. OT's delta: the *measured,
consumer-relative false-clear rate* unifying reliability-target and refresh-horizon
relativity; the refresh-floor law.

**§V Discussion.** Sionna link-level is the evidence rung; OTA / srsRAN testbed is the
graduation. The consumer-relative false-clear methodology is domain-general (optical
QoT, DB replication, grid) but the results here stand on the 5G-NR CSI certificate
alone. Future work: a systematic compression-ratio / channel-rank sweep to map the
boundary where a learned codec's reconstruction objective *does* begin to cost the
consumer (its own pre-registered cell — reported with its non-appearance at practical
CR, not cherry-picked).

## What is already sealed (write from the record — no new seal needed to submit)

| Act | Cell | Seal | Graded (real Sionna) |
|---|---|---|---|
| III-A | XPROTO-URLLC | 6375ebd, 2026-08-24 | eMBB 0.112 vs URLLC-naive 0.112 (target 0.001) vs aware 1.7e-5 → PASS |
| III-B | XPROTO-CSI + OT-14 | ng:fda9148, 2026-08-23 | naive 0.37 / OLLA 0.10 / fresh 0.12; floor ≈0.177·T_coh, R²=0.915 → PASS |
| — | ~~XPROTO-AICSI (v1)~~ | sealed but **not used** | v1 dissociation refuted on standard CDL (AICSI-v2, kept negative) — excluded |

Two sealed real-Sionna results carry the paper. The `build/aicsi_dissociation.{pdf,png}`
figure is **retired** (its claim did not survive v2). AICSI-v2 is recorded as a kept
negative, not sealed.

## Reuse from OFC

The ML dissociation figure, the false-clear-as-KPI framing, the "credit the deployed
witness, sell the measurement" positioning, and the sealed-prereg methodology all
transfer directly from the OFC ML-QoT paper. §III-C is the CSI twin of that paper's §3.1.
Keep the two papers' *substrates* distinct (optical QoT vs 5G-NR CSI) — same grammar,
venue-appropriate instances, no text reuse.
