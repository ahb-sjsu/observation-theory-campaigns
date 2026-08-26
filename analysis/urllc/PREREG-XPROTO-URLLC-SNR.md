# PREREG-XPROTO-URLLC-SNR — SNR-robustness of the reliability-target consumer-relativity

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-25. Earliest compliant seal
**2026-08-26** (`urllc_snr_check.py` codes the cooling-off). Graded seeds {20260826,
20260827, 20260828}, disjoint from the shakedown's {0,1,2}. Substrate = real Sionna 5G NR
LDPC curves + TDL-A fading (`csi_sionna`), fresh CSI. Robustness companion to the sealed
XPROTO-URLLC (answers the reviewer's single-mean-SNR concern).

## The claim

AMC selects the MCS to ride the eMBB BLER target at every SNR, so the URLLC-naive
false-clear multiple (the same certificate read against $10^{-3}$) is **large across the
whole operating range**, not an artifact of one mean SNR. At **cell edge** the lowest MCS
cannot meet the eMBB target, so even the eMBB certificate false-clears (the SNR-relativity
predicted by review). A target-aware certificate (conservative MCS + $K{=}3$ diversity)
holds URLLC across the operating range.

## Family F-URLLC-SNR (constructed + shaken down 2026-08-25)

`fam_urllc_snr.py`: mean SNR swept over $\{3,6,9,12,15,18,21\}$\,dB (cell edge to centre)
by additive offset on the TDL-A fading trace; at each point the eMBB / URLLC-naive /
URLLC-aware achieved BLER is measured against $\beta_{\rm eMBB}{=}10^{-1}$,
$\beta_{\rm URLLC}{=}10^{-3}$. URLLC-aware = $4$\,dB backoff + $K{=}3$ independent branches.

*Demonstrated (seeds {0,1,2}): URLLC-naive stays $\ge 0.055$ (\,$\ge 55\times$ target) at
every SNR $\ge 9$\,dB; at $3$\,dB eMBB itself reaches $\approx 0.32$; URLLC-aware
$\le 5.7\!\times\!10^{-4}$ for SNR $\ge 9$\,dB.*

## Bars (bind at seal; checked against the family record first)

- **B1 — target-relativity persists across the operating range.** Per seed:
  $\min_{M\in\{9,12,15,18\}}\texttt{urllc\_naive}(M) \ge 0.05$ (the URLLC false-clear is
  $\ge 50\times$ its target at every in-range SNR).
- **B2 — witness holds across the operating range.** Per seed:
  $\max_{M\in\{9,12,15,18\}}\texttt{urllc\_aware}(M) \le 10^{-3}$.
- **B3 — gap never closes at cell centre.** Per seed:
  $\texttt{urllc\_naive}(21) \ge 0.03$ (even where the MCS saturates at 64-QAM, the
  URLLC false-clear stays $\ge 30\times$ its target).

**Manipulation checks (bars too):**
- **MC1 — cell-edge eMBB breakdown is real.** Per seed: $\texttt{embb}(3)\ge 0.15$ (the
  eMBB certificate itself false-clears at cell edge $> 1.5\times$ its target).
- **MC2 — sane at cell centre.** Per seed: $\texttt{embb}(15)\le 0.15$ and
  $\texttt{embb}(18)\le 0.15$ (not a universal breakdown; AMC works in range).
- **MC3 — non-degenerate.** $\ge 5$ SNR points swept.

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL, kept.
**Kills:** $\texttt{urllc\_naive}(12) < 0.02$ (no in-range target gap) or
$\texttt{embb}(3) < 0.11$ (no cell-edge breakdown — the SNR-relativity absent).

## Seal procedure

On 2026-08-26+: confirm `URLLCSNRREP-family.json` PASSes `--check-family`, reread, flip
STATUS to SEALED, commit; on Atlas run `fam_urllc_snr.py --seeds 20260826 20260827
20260828 --out URLLCSNRREP-graded-raw.json`, pull, `urllc_snr_check.py` → commit
`XPROTO-URLLC-SNR-graded.json`.

## Scope

Same substrate/limits as XPROTO-URLLC (one TDL-A profile, 64-QAM MCS set); adds the mean-
SNR axis (cell edge to centre). OT's delta: the *measured, consumer-relative false-clear
rate* shown SNR-invariant in the operating range plus the cell-edge breakdown of the eMBB
certificate. Provenance: reviewer comment (c); `fam_urllc_snr.py` + `urllc_snr_check.py`.
