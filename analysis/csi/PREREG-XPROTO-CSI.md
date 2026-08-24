# PREREG-XPROTO-CSI — 5G/6G CSI-aging cell (the taxonomy's first cellular entry)

**STATUS: SEALED 2026-08-23.** FAMILY-CONSTRUCTED: 2026-08-22. Earliest compliant
seal **2026-08-23** (`csi_check.py` enforces the cooling-off in code). The
**sealed graded run is on a real 5G NR PHY substrate** (mode="nrsionna":
`csi_sionna.py` on Atlas GPU, NVIDIA Sionna — real 5G LDPC decode + 3GPP
TR38.901 TDL channel; see `SUBSTRATE.md`). srsRAN/OAI RFsim is an accepted
system-level alternative (mode="rfsim"). The synthetic fading simulator
(`fam_csi.py --sim`) validates the grading CODE and calibrates the bars but
is **not evidence about real 5G** — `csi_check.py` refuses to seal on sim
data. Graded on seeds {20260823, 20260824, 20260825}, disjoint from the
sim validation's {0,1,2}. No evidential weight until sealed and run on the
NR substrate.

**IP posture:** public methodology (companion to the replication survey +
`draft-bond-ot80211-freshness`); nothing gated. Repo private for now.

## The claim

A UE's CQI report is a certificate — the gNB selects an MCS from it to
hit a target BLER (10%). Under CSI **aging** (the channel decorrelates
faster than the report cadence — mobility, Doppler), the certificate is a
**false-clear**: the CQI-chosen MCS was implicitly certified supportable,
but the transmission on the aged channel fails (HARQ NACK). Graded against
HARQ ACK/NACK — the independent witness of whether the consumer decoded —
raw fixed-cadence CQI has a false-clear rate (BLER) far above target,
while a **HARQ-witnessed** policy (outer-loop link adaptation, OLLA) holds
BLER at target. The false-clear rate is **consumer-relative**: it is set
by the UE's own Doppler / coherence time. This is the vacuity taxonomy's
first cellular cell (routing / DB / PHY-802.11 already covered), and the
OT-14 refresh-floor law at the 5G/6G air interface.

**HARQ is the universal witness** for 5G/6G adaptation certificates
(CQI→MCS here; CSI→precoder, beam, TA elsewhere) — nearly every one can
be graded against ACK/NACK, which is exactly what this cell does.

## Family F-CSI (constructed + shaken down 2026-08-22)

Sim substrate (`fam_csi.py --sim`): a correlated-fading SINR trace (AR(1),
coherence time 0.423/f_d, Clarke) at f_d = 200 Hz (high mobility), mean
SINR 12 dB, σ 4 dB; CQI reported every 20 TTIs with 1 dB noise; a 15-level
MCS table (per-MCS SINR-for-50%-BLER), MCS chosen to target 10% BLER; HARQ
ACK/NACK drawn from the BLER at the *actual aged* SINR. Three policies over
the SAME channel: **naive** (raw CQI), **olla** (CQI + HARQ-driven SINR
offset; equilibrium at target BLER), **fresh** (CQI every TTI — the
no-aging control). The seed draws the channel + noise.

## Bars (bind at seal; checked against the family record first)

Calibrated on the sim (naive BLER ≈ 0.30, olla ≈ 0.10, fresh ≈ 0.07) and
validated against the committed RFsim `CSIREP-family.json`
(`csi_check.py --check-family`) before the seal.

- **B1 — CQI vacuity under aging.** Per seed: `naive_bler ≥ 0.25` (raw
  CQI false-clears ≥ 2.5× the 0.10 target).
- **B2 — witness holds.** Per seed: `olla_bler ≤ 0.15` (HARQ-witnessed
  policy keeps BLER near target).
- **B3 — dominance.** Per seed: `olla_bler ≤ naive_bler / 2`.

**Manipulation checks (bars too):**
- **MC1 — aging is real.** `cqi_err_db ≥ 2.0` (mean |reported − realized
  SINR| — a genuine aging regime; if the channel is static there is no
  story). *(In RFsim, derive from the logged SINR/CQI vs realized; if not
  logged, MC1 is asserted by the configured f_d × report period.)*
- **MC2 — link adaptation sane with fresh CSI.** `fresh_bler ≤ 0.15`
  (fresh CQI hits target — failures are attributable to aging, not a
  broken model).
- **MC3 — non-degenerate.** `n_tti ≥ 5000`, `mcs_var ≥ 2` (the MCS
  certificate is active, not pinned).

**Verdict rule:** any MC failure → VOID; all MCs + B1–B3 pass on every
graded seed → PASS; otherwise FAIL, kept as executed.

**Kills.** `naive_bler < 0.15` on the graded seeds — no aging vacuity in
this regime (the CQI certificate is adequate; claim refuted for this
substrate); or `olla_bler > 0.30` — the witnessed policy does not hold.

## Seal procedure

On 2026-08-23 or later: confirm the family record (`CSIREP-family.json`,
mode="nrsionna") still PASSes `csi_check.py --check-family`, reread this
prereg, flip STATUS to `SEALED <date>`, commit. Then on Atlas GPU run
`csi_sionna.py --seeds 20260823 20260824 20260825 --out CSIREP-graded-raw.json`,
pull it, `csi_check.py` (seal-guarded; grades the graded-raw NR record) →
commit `XPROTO-CSI-graded.json` as executed.

## Scope

The sealed substrate is real 5G NR PHY at the **link level** (NVIDIA
Sionna: real 5G LDPC decode + 3GPP TR38.901 TDL channel + Doppler; HARQ
ACK/NACK via the 3GPP link-to-system method over real LDPC-measured BLER
curves), no SDR hardware. It stands in for real mobility; a system-level
stack (srsRAN/OAI, real scheduler), full per-block decoding, and an
over-the-air / channel-emulator cell are later external-validity
graduations. The `fam_csi.py` and `nr_link.py` runs are code / modeled-
decoder rungs, not the sealed evidence. OLLA is credited prior art (a deployed HARQ-witnessed correction);
OT's delta is the *measured, consumer-relative, calibrated* false-clear
rate and the *derivable* refresh floor (max report period for BLER ≤
target ∝ coherence time), reported as a Doppler sweep. Normative
air-interface behavior is **3GPP's** remit; this cell is measurement
methodology. Prior art (OLLA, CSI aging, AI-based CSI feedback) positioned
in the replication survey / the 6G exploration note.

## Provenance

- Exploration: the 5G/6G applicability discussion (HARQ-as-witness,
  refresh floors, slice/beam/cell-free parallels; turboquant-pro→CSI
  compression bridge).
- Grading + simulator: `fam_csi.py`; sim validation `CSI-SIM-validation.json`
  (seeds {0,1,2}) — no evidential weight.
- Substrate + log schema: `SUBSTRATE.md`.
- Graded runner: `csi_check.py` (seal-guard + coded cooling-off +
  RFsim-only sealed grading + pre-seal record check).
