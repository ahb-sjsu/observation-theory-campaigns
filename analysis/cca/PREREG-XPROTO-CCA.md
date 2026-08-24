# PREREG-XPROTO-CCA — 802.11 CCA false-clear cell (the taxonomy's first PHY entry)

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-21. The earliest
compliant seal is **2026-08-22** (`cca_check.py` enforces the cooling-off
in code). The **sealed graded run is on HARDWARE** (mode="hw", the RF
bench of `HARDWARE.md`); the synthetic simulator (`fam_cca.py --sim`)
validates the grading CODE and calibrates the bars but is **not evidence
about 802.11** — `cca_check.py` refuses to seal on sim data. Graded on
bench runs {20260822, 20260823, 20260824}, disjoint from the sim
validation's {0, 1, 2}. No evidential weight until sealed and run on the
bench.

**IP posture:** public methodology (companion to
`draft-bond-ot80211-freshness`); nothing gated — SDR Wi-Fi measurement,
not the replication-certificate mechanism. Repo private for now per the
owner's stance.

## The claim

On a controlled 802.11 hidden-node topology, the transmitter's Clear
Channel Assessment (CCA) — "medium idle → transmit" — is **vacuous for
the receiver**: it reports clear at the transmitter while the receiver
collides with a station the transmitter cannot sense. Graded against an
independent Pluto witness co-located with the receiver, CCA-alone has a
false-clear rate meaningfully above zero, and an **RTS/CTS-witnessed**
assessment (the CTS silences the hidden node when it can hear the
receiver) reduces that rate by a multiple. This is the vacuity taxonomy's
first PHY cell (sealed so far: BGP 0.351 / IS-IS 0.184 / OSPF 0.083 /
BMP / PG lab + production / MongoDB), and the consumer-relativity claim
measured at the 802.11 MAC/PHY boundary.

## Substrate (constructed 2026-08-21; sealed run on the bench)

Conducted hidden-node triangle (see `HARDWARE.md`): transmitter **A** and
receiver **Rx** as SDR 802.11 (`gr-ieee802-11`, so A's CCA decision is
observable), hidden interferer **C**, and an **ADALM-Pluto witness W**
RX-only at the Rx port. Attenuators set the topology: A↔C coupling below
A's CCA threshold (A cannot sense C) while C→Rx collides and A→Rx passes.
Cabled + attenuated (no over-the-air emission) for reproducibility and to
avoid regulatory exposure; OTA is a later external-validity cell.

Each seed is a bench run with a seeded C on/off schedule; the run is
executed twice, **CCA-alone** and **RTS/CTS-enabled**, both graded against
the same witness. Grading (`fam_cca.grade_condition`): a false-clear is a
CCA-clear transmission where Rx decode failed AND the witness shows
concurrent C energy at Rx; losses without concurrent energy are link/SNR
losses, not false-clears.

## Bars (bind at seal; checked against the HARDWARE family record first)

Bars calibrated on the synthetic model (`fam_cca --sim`: fc_cca ≈ 0.30,
fc_rtscts ≈ 0.03 across seeds) and validated against the committed
hardware `CCAREP-family.json` (`cca_check.py --check-family`) before the
seal; a bar the bench record cannot pass does not get sealed.

- **B1 — CCA vacuity.** Per seed: `fc_cca ≥ 0.15` — bare CCA is
  meaningfully vacuous in the hidden-node regime.
- **B2 — witness helps.** Per seed: `fc_rtscts ≤ 0.05`.
- **B3 — dominance.** Per seed: `fc_cca ≥ 3 × fc_rtscts`.

**Manipulation checks (bars too):**
- **MC1 — hidden realized.** During C's transmissions, A's CCA reports
  clear ≥ 0.80 (A genuinely cannot sense C).
- **MC2 — interferer reaches the consumer.** The witness detects C energy
  at Rx in ≥ 0.80 of A frames overlapping a C burst.
- **MC3 — non-degenerate + link sane.** ≥ 1000 CCA-clear A-frames, ≥ 200
  with concurrent C energy, AND clean-link decode ≥ 0.90 (failures are
  attributable to collision, not a broken link).
- **MC4 — witness alignment.** Cross-correlation timing residual between
  the witness capture and A's frame schedule ≤ one OFDM symbol (≈ 4 µs).

**Verdict rule:** any MC failure → VOID (instrument, not claim); all MCs
pass and all bars pass on every graded bench run → PASS; otherwise FAIL,
kept as executed.

**Kills.** `fc_cca < 0.05` on the graded runs — the bench did not achieve
a hidden-node regime (topology failure; refuted for this substrate,
reported); or `fc_rtscts ≥ fc_cca` — RTS/CTS does not help here
(reported).

## Seal procedure

On 2026-08-22 or later, with the bench assembled: run the hardware
shakedown → commit `CCAREP-family.json`; `cca_check.py --check-family`
(must PASS); reread this prereg; flip STATUS to `SEALED <date>`; commit;
run `cca_check.py` (mode="hw", graded bench runs); commit
`XPROTO-CCA-graded.json` as executed.

## Scope

The sealed cell is a **conducted** bench: attenuators stand in for the
hidden-node geometry, and the workload is SDR 802.11 at low-mid MCS on
2.4 GHz. A PASS earns the PHY false-clear finding and the RTS/CTS
reduction on this bench — the first measured number for the RFC's
otherwise-illustrative example — not a production-deployment claim. An
over-the-air hidden-node cell at compliant power is the external-validity
graduation. The simulator is code validation only.

## Provenance

- Scoping: `../../../geometric-observation/docs/cca-cell-scoping.md` and
  `draft-bond-ot80211-freshness`.
- Grading + simulator: `fam_cca.py`; sim validation `CCA-SIM-validation.json`
  (seeds {0,1,2}) — code validation, no evidential weight.
- Hardware harness + log schema: `HARDWARE.md`.
- Graded runner: `cca_check.py` (seal-guard + coded cooling-off +
  hw-only sealed grading + pre-seal record check).
