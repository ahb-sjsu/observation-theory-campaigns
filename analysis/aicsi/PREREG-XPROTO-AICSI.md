# PREREG-XPROTO-AICSI — neural CSI-feedback vacuity cell (the 6G / turboquant bridge)

**STATUS: SEALED 2026-08-23.**

> **ANNOTATION ADDED 2026-08-27 (not part of the sealed text). SCOPE CORRECTION, NOT A
> RETRACTION.** The v1 seal stands for what it tested. What it tested does **not**
> generalize to the substrate the DL-CSI-feedback community benchmarks on. In the
> AICSI-v2 shakedown (real 3GPP CDL-C channels + a CsiNet-class convolutional
> autoencoder), the NMSE-optimal codec reconstructs near-perfectly (NMSE ≈ 0.03) and its
> false-clear rate is **0.0 on all three seeds**; the pre-registered kill fired. The
> reconstruction-vs-consumer dissociation sealed here was substantially an artifact of an
> **under-powered MLP codec** (its own recon NMSE ≈ 0.67) on a **harder synthetic**
> clustered-ULA channel. The mismatch is real only in the lossy/high-rank regime, not at
> practical CSI-feedback operating points on CDL. Do not headline this cell. See
> [`PREREG-XPROTO-AICSI-V2.md`](PREREG-XPROTO-AICSI-V2.md) (REFUTED AT SHAKEDOWN, NOT
> SEALED, 2026-08-25, kept negative). §III-C of the WCNC 2027 paper is dropped as a
> result. Preregs sealed before 2026-08-25 that cite this cell are correct as of their
> sealing date and are left unchanged.

FAMILY-CONSTRUCTED: 2026-08-22. Earliest compliant
seal **2026-08-23** (`aicsi_check.py` enforces the cooling-off in code). The
**sealed graded run is on the real NR substrate** (mode="nrsionna_aicsi":
`aicsi.py` on Atlas GPU — learned CSI autoencoders + the real Sionna 5G NR
LDPC BLER curves for the consumer's decode). Graded on seeds {20260823,
20260824, 20260825}, disjoint from the shakedown's {0,1,2}. No evidential
weight until sealed and run on the NR substrate.

**IP posture:** public methodology; the **cellular twin of turboquant-pro's
public thesis** (consumer-relative distortion + witnessed certificate). This
cell is the OT-series bridge from Paper II (turboquant, ML-systems) into the
5G/6G domain. Nothing gated.

## The claim

In (6G-)AI-native CSI feedback, the UE compresses the measured channel with
a **learned codec**; the gNB reconstructs it and derives a **precoder**. The
codec is conventionally trained to minimize **reconstruction error (NMSE)** —
a certificate that says "the CSI was conveyed faithfully." But the consumer
(the precoder → the served link) reads the channel through a **low-dim
projection** (its dominant eigen-direction), not the Frobenius norm. So the
reconstruction certificate is a **false-clear**: a codec can *win the NMSE it
was trained on yet fail the consumer* — the precoder it induces is misaligned
and the transmission fails (HARQ NACK). Graded against HARQ ACK/NACK — the
independent witness of whether the consumer decoded — the NMSE-optimal codec
has a false-clear rate far above target, while a **consumer/witness-aware**
codec (trained on the achieved beamforming gain) holds. This is the
compression-domain, cellular twin of the replication-vacuity result and of
turboquant-pro's KV-keys finding ("compress by the metric the consumer reads,
not reconstruction"). **HARQ is the universal witness** (as across the cellular
cells).

## Family F-AICSI (constructed + shaken down 2026-08-22)

MIMO channels H (Nr=2 × Nt=16) with angular structure (4 clusters → competing
singular directions). Two autoencoders share the architecture + a B=9
bottleneck (the feedback-bit proxy): **nmse** (loss = ‖H−Ĥ‖²/‖H‖²,
reconstruction) and **aware** (loss = mean −log(‖H·w(Ĥ)‖²/‖H·w(H)‖²), the
consumer's SINR deficit; the tail-sensitive form). w(·) = top right singular
vector (power iteration) = the MRT precoder. The consumer's achieved SINR =
operating_SINR + 10log10(gain fraction); HARQ ACK/NACK / BLER from the
**real Sionna 5G NR LDPC curves**. A **perfect-CSI** control (gain fraction
= 1) shows the link is sane.

## Bars (bind at seal; checked against the family record first)

Cell-specific thresholds (this is a reconstruction-vs-consumer cell, not a
temporal-freshness monitor), calibrated on the shakedown with margin.
*Demonstrated on seeds {0,1,2}: nmse_fc ≈ 0.28–0.31, aware_fc ≈ 0.12–0.17,
recon nmse ≈ 0.67 vs aware ≈ 1.14–1.20.*

- **B1 — reconstruction certificate vacuity.** Per seed:
  `nmse_false_clear ≥ 0.22` (the NMSE-optimal codec false-clears at the
  consumer).
- **B2 — witness holds.** Per seed: `aware_false_clear ≤ 0.18` (the
  consumer-aware codec holds well below the NMSE codec).
- **B3 — dominance.** Per seed: `aware_false_clear ≤ nmse_false_clear / 1.7`.

**Manipulation checks (bars too):**
- **MC1 — the paradox is real.** `nmse_recon_aware − nmse_recon_nmse ≥ 0.20`
  (the NMSE codec genuinely *wins reconstruction* — otherwise there is no
  vacuity, just a worse codec). This is the crux of the cell.
- **MC2 — link sane with perfect CSI.** `perfect_false_clear ≤ 0.15`
  (failures are attributable to the feedback, not a broken link).
- **MC3 — non-degenerate.** `nmse_recon_nmse ≤ 0.90` (the NMSE codec
  actually learned to reconstruct) **and** `aware_gain_frac ≥ nmse_gain_frac`
  (the aware codec genuinely aligns the precoder better — the mechanism).

**Verdict rule:** any MC failure → VOID; all MCs + B1–B3 pass on every graded
seed → PASS; otherwise FAIL, kept as executed.

**Kills.** `nmse_false_clear < 0.15` — no reconstruction vacuity (the NMSE
codec serves the consumer fine; claim refuted for this substrate); or
`aware_false_clear > 0.22` — the consumer-aware codec does not hold.

## Seal procedure

On 2026-08-23 or later: confirm `AICSIREP-family.json` (mode
"nrsionna_aicsi") PASSes `aicsi_check.py --check-family`, reread this prereg,
flip STATUS to `SEALED <date>`, commit. Then on Atlas GPU run `aicsi.py
--seeds 20260823 20260824 20260825 --out AICSIREP-graded-raw.json`, pull it,
`aicsi_check.py` (seal-guarded) → commit `XPROTO-AICSI-graded.json` as executed.

## Scope

Link-level, learned CSI feedback; a continuous B-dim bottleneck stands in for
the feedback-bit budget (a quantized/entropy-coded codec, a real CsiNet-class
architecture, Type-II CSI, and per-sample HARQ over full PDSCH decoding are
later fidelity/external-validity rungs). The precoder is MRT on the top
singular vector; multi-layer/eigen-beamforming is a later rung. The claim is
positioned against turboquant-pro (Paper II) and the AI-native-CSI literature
in the replication survey / the 6G exploration note. OT's delta is the
*measured, consumer-relative, calibrated* false-clear rate of a reconstruction
certificate and the *witnessed* alternative.

## Provenance

- Exploration: the 5G/6G applicability discussion (turboquant→CSI-compression
  bridge; consumer-relative distortion `tr(P_C·Σ)`).
- Experiment + physics: `aicsi.py` (autoencoders + power-iteration precoder).
- Decode: real Sionna 5G NR LDPC BLER curves (`csi_sionna`, XPROTO-CSI).
- Grading: `aicsi_check.py` (seal-guard + coded cooling-off + NR-only sealed
  grading + pre-seal record check).
