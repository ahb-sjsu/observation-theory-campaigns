# PREREG-XPROTO-PHY — the remaining PHY adaptation certificates: PMI, RI, TA

**STATUS: SEALED 2026-08-24.** FAMILY-CONSTRUCTED: 2026-08-23. Earliest compliant seal
**2026-08-24** (`phy_check.py` codes the cooling-off). The shakedown runs on a
self-contained parametric NR waterfall (mode="model": validation, not evidence,
as `fam_csi`'s sim is not); the sealed rung uses the real Sionna 5G NR LDPC
curves (mode="nrsionna") -- `phy_check.py` refuses to seal on "model". Graded
seeds {20260824, 20260825, 20260826}, disjoint from the shakedown's {0,1,2}.

**IP posture:** public methodology; completes the cellular PHY certificate
taxonomy. Nothing gated.

## The claim

Three more 5G adaptation certificates age and false-clear under their own
coherence process, each repaired by grading against the served-link outcome:

- **PMI (precoder).** The reported precoder (top eigen-direction) misaligns as
  the channel rotates -> beamforming-gain loss -> HARQ NACK. The MIMO-precoder
  sibling of XPROTO-BEAM.
- **RI (rank).** The reported rank ages; a stale-high rank transmits a spatial
  layer the current channel can no longer carry -> that layer collapses.
- **TA (uplink timing advance).** The UE's round-trip delay drifts with radial
  motion; a stale timing advance leaves a residual that, once it exceeds the
  cyclic prefix, causes inter-symbol interference -> UL decode failure. The
  taxonomy's **first uplink cell**.

Each: **naive** holds the periodic report; **witnessed** re-reports on K=2
consecutive failures (the deployed loop: PMI re-selection, RI down-rank, the TA
command loop); **fresh** re-reports every slot. The refresh floor is proportional
to each certificate's coherence process (angular, rank, timing).

## Family F-PHY (constructed + shaken down 2026-08-23)

Parametric NR waterfall (13-MCS, `0.5*erfc`), fixed MCS at operating SINR minus a
2 dB margin. PMI: precoder angle drifts 1200 deg/s, loss 0.3 dB/deg. RI: rank
random-walks in {1..4} at 270 flips/s, valid layers reliable, a stale-high layer
collapses (-12 dB). TA: delay drifts 20 us/s, TA cadence 200 ms, cyclic prefix
4.7 us, ISI penalty rising with residual then destroying the block past the CP.

## Bars (bind at seal; checked against the family record first)

Per cell (mode x seed). *Demonstrated (model): PMI naive ~0.36 / witnessed ~0.13;
RI ~0.28 / ~0.08; TA ~0.47 / ~0.055; fresh ~0 throughout.*

- **B1 -- certificate vacuity.** `naive_fc >= 0.25`.
- **B2 -- witness holds.** `witnessed_fc <= 0.15`.
- **B3 -- dominance.** `witnessed_fc <= naive_fc / 2`.

**Manipulation checks (bars too):**
- **MC1 -- aging is real.** `aging >= 0.05` (mode-agnostic floor: PMI mean
  gain-loss dB, RI rank-mismatch fraction, TA mean residual/CP).
- **MC2 -- fresh is sane.** `fresh_fc <= 0.15`.
- **MC3 -- non-degenerate.** `n_tti >= 5000`, `n_requotes >= 1`.

**Verdict:** any MC fail -> VOID; all MCs + B1-B3 on every cell -> PASS; else
FAIL, kept. **Kills:** any cell `naive_fc < 0.15` or `witnessed_fc > 0.25`.

## Seal procedure

On 2026-08-24+: port `fam_phy` decode to the real Sionna curves (mode
"nrsionna"), confirm the model record PASSes `--check-family`, reread, flip
STATUS to SEALED, commit; run on the NR substrate for seeds {20260824-26} ->
`PHYREP-graded-raw.json`, `phy_check.py` -> commit `XPROTO-PHY-graded.json`.

## Scope

Model-level shakedown; the sealed rung swaps the parametric waterfall for the
real Sionna LDPC curves and the abstract aging processes for TR38.901 CDL
(PMI/RI) and a real timing model (TA). PMI rhymes with the already-sealed BEAM
mechanism (angular precoder aging) in the MIMO-precoder domain; RI and TA are new
(discrete rank; uplink timing). Credited prior art: PMI/RI reporting + rank
adaptation, the NR TA command loop; OT's delta is the *measured, calibrated*
false-clear rate and the derivable refresh floor per certificate.

## Provenance

- Exploration: the 5G/6G applications discussion (completing the PHY certificate
  set beyond CQI/beam/CSI-feedback/RSRP).
- Family + grading: `fam_phy.py` (three modes) + `phy_check.py` (seal-guard +
  cooling-off + NR-only sealed grading + pre-seal record check).
