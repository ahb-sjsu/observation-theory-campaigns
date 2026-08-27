# PREREG-XPROTO-CSI-FLIP — the two-consumer verdict inversion (the Flip) in 5G NR link adaptation

**STATUS: SEALED 2026-08-27.** FAMILY-CONSTRUCTED: 2026-08-26. Earliest compliant seal
**2026-08-27** (`csiflip_check.py` codes the cooling-off). Graded seeds {20260827,
20260828, 20260829}, disjoint from the shakedown's {0,1,2}. Substrate = real Sionna
5G NR LDPC BLER curves + TDL-A fading (`csi_sionna`, mode "nrsionna"), held CSI,
empirical HARQ NACK rate. The radio twin of XPROTO-QOT-FLIP, for the WCNC 2027
paper; the optical and radio cells share one taxonomy story.

## The claim

Two margin policies with the same fleet-mean budget receive OPPOSITE verdicts from
two user fleets whose read operators are misaligned. The M-fleet (200 Hz Doppler,
12 dB mean SNR) fails through CSI aging, the time axis. The S-fleet (10 Hz, 7 dB)
fails through deep fades, the amplitude axis. Policy A allocates the 1.5 dB
fleet-mean margin by Doppler; policy B allocates the same total by SNR deficit. The
M-fleet does better under A, the S-fleet under B, and the fleet-mean NACK rate is
nearly tied, so the aggregate cannot order the pair for either fleet. As the
registered control, the SAME fleet read at two reliability thresholds (a +2 dB
shift of the required-SNR table) shows NO inversion under protect-low vs
protect-high margin policies: the coupling null of the failure taxonomy, since a
threshold shift leaves the read operators aligned. This also explains, within the
same paper, why the eMBB/URLLC axis (a threshold pair) shows dominance rather than
inversion.

## Family F-CSI-FLIP (constructed + shaken down 2026-08-26)

`fam_csiflip.py`: per seed, 12 users per fleet, per-user TDL-A traces (fleet fd and
mean SNR as above, distinct sub-seeds), 6000 TTI, 20-TTI held reports, 1 dB report
noise. Margins: m_A proportional to user Doppler, m_B proportional to
(12 - meanSNR)+0.05, both normalized to a fleet mean of exactly 1.5 dB. Per-fleet
FC = mean empirical NACK rate (real LDPC curve draws at the true SNR). Null: one
M-trace, required table shifted 0 / +2 dB, margins 3.0 vs 0.75 dB (protect-low vs
protect-high).

*Demonstrated (seeds {0,1,2}): flip TRUE on all seeds; gaps M: B-A = 0.13-0.14,
S: A-B = 0.10-0.11; fleet aggregate within 0.02; null_flip FALSE on all seeds.*

## Bars (bind at seal; checked against the family record first)

- **B1 — M-fleet prefers A, with margin.** Per seed: `fc_M_B - fc_M_A >= 0.08`.
- **B2 — S-fleet prefers B, with margin.** Per seed: `fc_S_A - fc_S_B >= 0.06`.
- **B3 — full inversion.** Per seed: `flip == true`.

**Manipulation checks (bars too):**
- **MC1 — the coupling null holds.** Per seed: `null_flip == false`.
- **MC2 — matched aggregate.** Per seed: `|mean_margin_A - mean_margin_B| <= 0.01`.
- **MC3 — non-degenerate.** Per seed: every fleet FC strictly inside (0,1).

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL,
kept. **Kills:** `flip == false` on any graded seed, or MC1 fails.

## Seal procedure

On 2026-08-27+: confirm `CSIFLIPREP-family.json` PASSes `--check-family`, reread,
flip STATUS to SEALED, commit; on Atlas run `fam_csiflip.py --seeds 20260827
20260828 20260829 --out CSIFLIPREP-graded-raw.json` (sionna-venv, CPU), pull,
`csiflip_check.py` → commit `XPROTO-CSI-FLIP-graded.json`.

## Scope

Policies are transparent margin allocations, not optimized schedulers; the claim is
the inversion, its size, and its taxonomy-predicted null, not allocator optimality.
WCNC use: a "one budget, two fleets, opposite verdicts" subsection plus the
paragraph that reframes the eMBB/URLLC threshold pair as the predicted null.
Provenance: the Flip (book Ch. 8/12; GO-2; GO-P-2026-088; XPROTO-QOT-FLIP),
`fam_csiflip.py`, `csiflip_check.py`.
