# PREREG-XPROTO-AICSI-V2 — neural CSI-feedback vacuity on the community-standard substrate

**STATUS: REFUTED AT SHAKEDOWN — NOT SEALED (2026-08-25).** The pre-registered kill
condition fired: on the real 3GPP CDL-C substrate with a CsiNet-class codec, the
NMSE-optimal codec has `nmse_false_clear = 0.0` on all three shakedown seeds — well
below the kill threshold of 0.15. The claim (reconstruction-vs-consumer dissociation)
**does not reproduce on this substrate**; the cell is recorded as a kept negative and
is **not sealed**. See "Shakedown result" below. FAMILY-CONSTRUCTED: 2026-08-25.

*(Original registration text preserved below for the record.)* Graded seeds
{20260826, 20260827, 20260828} were reserved but **not run** (no seal). Substrate =
mode `nrsionna_cdl_csinet`: `aicsi_v2.py` on Atlas — a CsiNet-class convolutional
autoencoder over real 3GPP CDL-C channels (Sionna 1.2 `tr38901`) + the real Sionna 5G
NR LDPC BLER curves.

## Shakedown result — REFUTED (kept negative)

Seeds {0,1,2}, real CDL-C + CsiNet-conv AE (`AICSIV2REP-family.json`):

| seed | NMSE codec: recon / FC / gain | aware codec: recon / FC / gain |
|---|---|---|
| 0 | 0.034 / **0.0** / 0.975 | 1.20 / 0.026 / 0.797 |
| 1 | 0.033 / **0.0** / 0.976 | 1.33 / 0.030 / 0.801 |
| 2 | 0.040 / **0.0** / 0.971 | 1.25 / 0.021 / 0.811 |

**Interpretation (honest).** On a standard low-rank, frequency-correlated CDL-C channel
a CsiNet-class codec reconstructs the CSI almost perfectly at a practical compression
ratio (NMSE ≈ 0.03), so the induced MRT precoder is near-optimal (gain ≈ 0.97) and the
reconstruction objective **does not** false-clear. The consumer-aware codec is strictly
worse on every axis. The v1 XPROTO-AICSI dissociation (sealed 2026-08-23) was therefore
substantially an artifact of an **under-powered codec** (an MLP that itself only reached
recon NMSE ≈ 0.67) on a **harder synthetic** channel with competing singular directions;
it does **not** survive the substrate the DL-CSI-feedback community benchmarks on.

**Consequence.** The reconstruction-vs-consumer objective mismatch is real only in the
lossy/high-rank regime, not at practical CSI-feedback operating points on CDL. It is
**not** a WCNC headline; §III-C of the WCNC paper is dropped. A systematic
compression-ratio / channel-rank sweep — characterising the boundary where the mismatch
appears, reported with its non-appearance at practical CR — is the honest future cell
(its own prereg), not a rushed reseal. The v1 seal stands for what it tested; this is a
scope correction, not a retraction.

---

*Original registration (pre-shakedown), preserved:*

**Why v2.** The sealed XPROTO-AICSI (2026-08-23) demonstrated the reconstruction-vs-
consumer dissociation on a *synthetic* clustered-ULA channel with an *MLP* autoencoder
— a valid proof-of-concept whose own scope named "a real CsiNet-class architecture" and
3GPP channels as later rungs. This cell discharges those rungs so the WCNC result stands
on the substrate the DL-CSI-feedback community benchmarks on. **v2 does not supersede or
re-open v1's seal**; it is a separate, higher-fidelity registration.

**IP posture:** public methodology; the cellular twin of turboquant-pro's public thesis.
Nothing gated. **Venue:** IEEE WCNC 2027 (§III-C).

## The claim

A learned CSI-feedback codec compresses the measured channel to a small bottleneck
(feedback-bit proxy); the gNB reconstructs it and derives a **precoder**. Trained to
minimise **reconstruction NMSE**, the codec optimises a Frobenius-norm certificate — but
the consumer (the per-subcarrier MRT precoder → the served link) reads the channel
through its **dominant eigen-direction**, not the Frobenius norm. So the reconstruction
certificate **false-clears**: the NMSE-optimal codec wins the metric it was trained on
yet induces a misaligned precoder whose transmission fails the FEC decoder. Witnessed by
the real Sionna 5G NR LDPC BLER, the NMSE-optimal codec has a false-clear rate far above
target, while a **consumer-aware** codec (trained on achieved beamforming gain) holds —
at comparable or better delivered gain. The compression-domain, cellular twin of the
replication-vacuity / KV-keys result.

## Family F-AICSI-V2 (constructed + shaken down 2026-08-25)

Real **3GPP CDL-C** MIMO channels (Sionna 1.2 `tr38901`), UE Nr=2 × gNB Nt=16 dual-pol,
32 subcarriers (30 kHz SCS, 3.5 GHz, 100 ns DS), per-sample power-normalised. Two
autoencoders share a **CsiNet-class convolutional architecture** (Conv2D encoder → dense
bottleneck B=32 → dense + Conv2D decoder with residual refine) on the (Nt × Nsub × 2Nr)
CSI image: **nmse** (loss = ‖H−Ĥ‖²/‖H‖²) and **aware** (loss = mean −log(mean-subcarrier
achieved-gain / optimal-gain)). Consumer = per-subcarrier MRT (top right singular vector
via power iteration); witness SINR = operating_SINR + 10log₁₀(gain fraction); BLER from
the **real Sionna 5G NR LDPC curves** (`csi_sionna`). A **perfect-CSI** control (gain
fraction = 1) shows the link is sane.

## Bars (bind at seal; checked against the family record first)

*Calibrated on the shakedown (seeds {0,1,2}) with margin — placed where the robust
effect lives, not at round numbers. Values inserted from the shakedown record before the
seal act; the seal commit fixes them.*

- **B1 — reconstruction certificate vacuity.** Per seed: `nmse_false_clear ≥ <B1>`
  (the NMSE-optimal codec false-clears at the consumer).
- **B2 — witness holds.** Per seed: `aware_false_clear ≤ <B2>`.
- **B3 — dominance.** Per seed: `aware_false_clear ≤ nmse_false_clear / <B3>`.

**Manipulation checks (bars too):**
- **MC1 — the paradox is real.** `nmse_recon_aware − nmse_recon_nmse ≥ <MC1>` (the NMSE
  codec genuinely *wins reconstruction*; otherwise there is no vacuity, just a worse codec).
- **MC2 — link sane with perfect CSI.** `perfect_false_clear ≤ 0.15`.
- **MC3 — the mechanism holds.** `aware_gain_frac ≥ nmse_gain_frac` (the aware codec
  aligns the precoder better) **and** `nmse_recon_nmse ≤ 0.90` (the NMSE codec learned).

**Verdict:** any MC failure → VOID; all MCs + B1–B3 on every graded seed → PASS;
otherwise FAIL, kept. **Kills:** `nmse_false_clear < 0.15` (no vacuity on this substrate —
claim refuted) or `aware_false_clear > <kill>` (the consumer-aware codec does not hold).

## Seal procedure

On 2026-08-26+: confirm `AICSIV2REP-family.json` (mode `nrsionna_cdl_csinet`) PASSes
`aicsi_v2_check.py --check-family`, reread this prereg, flip STATUS to `SEALED <date>`,
commit. Then on Atlas run `aicsi_v2.py --seeds 20260826 20260827 20260828 --out
AICSIV2REP-graded-raw.json`, pull it, `aicsi_v2_check.py` (seal-guarded) → commit
`XPROTO-AICSI-V2-graded.json`.

## Scope

Link-level, learned CSI feedback on real 3GPP CDL-C; a continuous B-dim bottleneck stands
in for the quantised/entropy-coded feedback budget (a quantised codec, Type-II CSI, and
per-sample HARQ over full PDSCH decoding remain later rungs). Conv autoencoder is a
CsiNet-class architecture; MRT on the top singular vector is the precoder (multi-layer
eigen-beamforming is a later rung). OT's delta is the *measured, consumer-relative,
calibrated* false-clear rate of a reconstruction certificate and the *witnessed*
alternative. Ran on CPU (a cuDNN execution fault blocks Conv2D on the GV100/TF build);
identical results on any device — the substrate is the channel + the decoder, not the
trainer.

## Provenance

- Exploration: XPROTO-AICSI v1 scope (declared CsiNet/3GPP rungs) + the WCNC 2027 paper.
- Experiment: `aicsi_v2.py` (CsiNet-conv AE + CDL channels + power-iteration precoder).
- Decode: real Sionna 5G NR LDPC BLER curves (`csi_sionna`, XPROTO-CSI).
- Grading: `aicsi_v2_check.py` (seal-guard + coded cooling-off + NR-substrate-only sealed
  grading + pre-seal record check).
