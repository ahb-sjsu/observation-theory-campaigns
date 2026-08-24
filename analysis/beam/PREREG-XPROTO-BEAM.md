# PREREG-XPROTO-BEAM — mmWave beam-aging cell (the taxonomy's FR2 entry)

**STATUS: SEALED 2026-08-23.** FAMILY-CONSTRUCTED: 2026-08-22. Earliest compliant
seal **2026-08-23** (`beam_check.py` enforces the cooling-off in code). The
**sealed graded run is on the real NR substrate** (mode="nrsionna_beam":
`fam_beam.py` on Atlas GPU — an exact λ/2 ULA array factor for the
beamforming gain vs misalignment, plus the real Sionna 5G NR LDPC BLER
curves for the block decode; see `../csi/SUBSTRATE.md`). Graded on seeds
{20260823, 20260824, 20260825}, disjoint from the shakedown's {0,1,2}. No
evidential weight until sealed and run on the NR substrate.

**IP posture:** public methodology (a cellular companion to the replication
survey + `draft-bond-ot80211-freshness`); nothing gated. Repo private for now.

## The claim

At FR2 the gNB serves the UE through a **narrow analog beam** chosen from
the UE's reported best-beam certificate (SSB/CSI-RS index, L1-RSRP). Under
**angular aging** (the dominant direction drifts faster than the beam-report
cadence — rotation, mobility), the certificate is a **false-clear**: the
reported beam was implicitly certified best, but by transmission time the
true direction has moved off it, the beamforming gain collapses (a narrow
beam has little angular tolerance), and the transmission fails (HARQ NACK).
Graded against HARQ ACK/NACK — the independent witness of whether the
consumer decoded — a stale periodic beam has a false-clear rate (BLER) far
above target, while a **HARQ-witnessed** policy (Beam-Failure Recovery, BFR:
re-select on K consecutive NACKs) holds BLER near target. The false-clear
rate is **consumer-relative**: set by the UE's own angular velocity /
coherence. This is the vacuity taxonomy's mmWave/FR2 cell, and the OT-14
refresh-floor law in the angular domain (max beam-report period ∝ angular
coherence time). **HARQ is the universal witness** (as in XPROTO-CSI).

## Family F-BEAM (constructed + shaken down 2026-08-22)

Certificate = reported best beam; consumer = the beamformed link; witness =
HARQ. A 16-element λ/2 ULA with a 24-beam codebook over ±60°; the received
SINR of beam *b* at true angle θ is `BASE + 10log10(|AF(θ;b)|²/N)` from the
**exact array factor** (aligned SINR = 10log10 N ≈ 12 dB). The true angle
drifts at ω = 300°/s (bounded, + AR jitter) — the aging process; the beam is
measured with 1° error at each report. MCS is **fixed** at the most
aggressive one supportable at (aligned SINR − 2 dB margin), to isolate the
*beam* certificate (not link adaptation) and keep the fresh-beam control
below target. Block decode uses the **real Sionna 5G NR
LDPC BLER curves** at the actual (misaligned) SINR. Three policies over the
SAME angular track: **naive** (periodic beam, held), **bfr** (periodic +
re-select on K=2 consecutive NACKs — the deployed HARQ-witnessed
correction), **fresh** (re-select every slot — the no-aging control).

## Bars (bind at seal; checked against the family record first)

- **B1 — beam certificate vacuity under aging.** Per seed:
  `naive_bler ≥ 0.25` (stale beam false-clears ≥ 2.5× the 0.10 target).
- **B2 — witness holds.** Per seed: `bfr_bler ≤ 0.15`.
- **B3 — dominance.** Per seed: `bfr_bler ≤ naive_bler / 2`.

**Manipulation checks (bars too):**
- **MC1 — misalignment is real.** `beam_loss_db ≥ 2.0` (mean beamforming-gain
  loss under the naive policy; if beams never drift off there is no story).
- **MC2 — link sane with a fresh beam.** `fresh_bler ≤ 0.15` (failures are
  attributable to aging, not a broken model).
- **MC3 — non-degenerate.** `n_slot ≥ 5000`, `beam_var ≥ 2` (the beam
  certificate is active, not pinned to one beam).

**Verdict rule:** any MC failure → VOID; all MCs + B1–B3 pass on every
graded seed → PASS; otherwise FAIL, kept as executed.

**Kills.** `naive_bler < 0.15` — no beam-aging vacuity in this regime
(claim refuted for this substrate); or `bfr_bler > 0.30` — BFR does not hold.

## Seal procedure

On 2026-08-23 or later: confirm `BEAMREP-family.json` (mode
"nrsionna_beam") PASSes `beam_check.py --check-family`, reread this prereg,
flip STATUS to `SEALED <date>`, commit. Then on Atlas GPU run `fam_beam.py
--seeds 20260823 20260824 20260825 --out BEAMREP-graded-raw.json`, pull it,
`beam_check.py` (seal-guarded) → commit `XPROTO-BEAM-graded.json` as executed.

## Scope

Analog beamforming at FR2, link level; an exact ULA array factor stands in
for the antenna pattern and real Sionna 5G LDPC for the decode. Angular
drift stands in for rotation/mobility. A Sionna CDL small-scale-fading
overlay, hybrid/digital beamforming, a real beam codebook (Type-I CSI), and
an over-the-air cell are later external-validity graduations. BFR is
credited prior art; OT's delta is the *measured, consumer-relative,
calibrated* beam false-clear rate and the *derivable* angular refresh floor.
Normative behavior is 3GPP's remit; this cell is measurement methodology.

## Provenance

- Exploration: the 5G/6G applicability discussion (HARQ-as-witness across
  adaptation certificates: CQI→MCS, **beam**, PMI, TA, handover).
- Physics: exact λ/2 ULA array factor (`fam_beam.array_gain`).
- Decode: real Sionna 5G NR LDPC BLER curves (`csi_sionna`, XPROTO-CSI).
- Grading: `beam_check.py` (seal-guard + coded cooling-off + NR-only sealed
  grading + pre-seal record check).
