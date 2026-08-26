# PREREG-XPROTO-QOT-FLIP — the two-consumer verdict inversion (the Flip) in optical QoT

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-26. Earliest compliant seal
**2026-08-27** (`qotflip_check.py` codes the cooling-off). Graded seeds {20260827,
20260828, 20260829}, disjoint from the shakedown's {0,1,2}. Substrate = fam_qot's
GNPy GN-model GSNR over CORONET-CONUS (mode "gnpy-coronet"). The optical instance of
the program's signature experiment (GO-2 codes; GO-P-2026-088 sensor schedules), for
the OFC 2027 digital-twin paper.

## The claim

Two margin policies with the same fleet-mean margin budget receive OPPOSITE verdicts
from two consumer classes whose read operators are misaligned, and the fleet
aggregate cannot order the pair correctly for either class. Policy A allocates
margin by reach; policy B allocates the same total by band-centrality. The R-fleet
(long-reach, band-edge services, penalty dominated by span count) does better under
A; the P-fleet (short-reach, band-centre services, penalty dominated by NLI
position) does better under B. Full verdict inversion. As a registered control, the
same protocol on two FEC classes (SD/HD threshold shift, SAME read projection)
produces NO flip: the coupling null of the failure taxonomy (book Ch. 12), since a
scalar threshold shift leaves the read operators aligned.

## Disclosed pilot (design iteration before this registration; no sealed bar existed)

Pilot 1 (2026-08-26, seeds {0,1,2}): the first construction used only the two FEC
classes with margin bumps shaped in provisioning-GSNR. The flip was ABSENT on all
seeds (policy B dominated both classes). This is the taxonomy's predicted coupling
null, so the construction was retained as the registered CONTROL and the flip
construction was moved to the misaligned footprint axes above. No bars existed
before this registration; the pilot is disclosed here, not hidden.

## Family F-QOT-FLIP (constructed + shaken down 2026-08-26)

`fam_qotflip.py`: K=120 services/seed. Footprint fleets: R = top-half reaches at
band-edge positions (p in [0,0.15] or [0.85,1]); P = bottom-half reaches at centre
positions (p in [0.35,0.65]); interleaved. Policies: m_A proportional to normalized
reach; m_B proportional to band-centrality + 0.05; both normalized per seed to a
fleet-mean margin of exactly 1.0 dB. Estimates carry 0.3 dB monitoring noise.
Provisioning = 6-ch band; deployed = full 76-ch C-band. FC per class = fraction of
services whose selected format (estimate + class margin vs required-GSNR table)
fails the deployed GSNR. FEC control: interleaved SD/HD fleet (required table
shifted by -/+1.5 dB), margin bumps protect-low vs protect-high in provisioning
GSNR, same 1.0 dB fleet mean.

*Demonstrated (seeds {0,1,2}): footprint flip TRUE on all seeds with gaps
fp_R: B-A = 0.25-0.42; fp_P: A-B = 0.15-0.20. FEC flip FALSE on all seeds.*

## Bars (bind at seal; checked against the family record first)

- **B1 — R-fleet prefers A, with margin.** Per seed:
  `fp_fc_R_B - fp_fc_R_A >= 0.15`.
- **B2 — P-fleet prefers B, with margin.** Per seed:
  `fp_fc_P_A - fp_fc_P_B >= 0.10`.
- **B3 — full inversion.** Per seed: `fp_flip == true`.

**Manipulation checks (bars too):**
- **MC1 — the coupling null holds.** Per seed: `fec_flip == false` (the taxonomy's
  predicted absence with aligned read operators; if the FEC construction flips, the
  mechanism story is wrong and the cell is VOID).
- **MC2 — matched aggregate.** Per seed:
  `|fp_mean_margin_A - fp_mean_margin_B| <= 0.001` (the aggregate cannot separate
  the policies by budget).
- **MC3 — non-degenerate.** Per seed: every fp false-clear strictly inside (0,1).

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL,
kept. **Kills:** `fp_flip == false` on any graded seed (the inversion does not
replicate) or MC1 fails (the null flips).

## Seal procedure

On 2026-08-27+: confirm `QOTFLIPREP-family.json` PASSes `--check-family`, reread,
flip STATUS to SEALED, commit; run `fam_qotflip.py --seeds 20260827 20260828
20260829 --out QOTFLIPREP-graded-raw.json` in the qot venv, `qotflip_check.py` →
commit `XPROTO-QOT-FLIP-graded.json`.

## Scope

The GN model is the substrate; policies are transparent margin allocations, not
optimized schedulers. The claim is the inversion and its taxonomy-predicted null,
not policy optimality. OFC use: the twin paper's consumer-relativity section; the
sealed numbers replace the shakedown's before submission. Provenance: the Flip
(book Ch. 8/12; GO-2; GO-P-2026-088), `fam_qotflip.py`, `qotflip_check.py`.
