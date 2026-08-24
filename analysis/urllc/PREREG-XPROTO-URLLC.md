# PREREG-XPROTO-URLLC — reliability-target consumer-relativity (5G URLLC vs eMBB)

**STATUS: SEALED 2026-08-24.** FAMILY-CONSTRUCTED: 2026-08-23. Earliest compliant seal
**2026-08-24** (`urllc_check.py` codes the cooling-off). Sealed graded run on the
real NR substrate (mode="nrsionna": `fam_urllc.py` on Atlas -- real Sionna 5G NR
LDPC waterfall fits + TDL fading). Graded seeds {20260824, 20260825, 20260826},
disjoint from the shakedown's {0,1,2}.

**IP posture:** public methodology; the cellular case where the read operator is
the reliability target itself. Nothing gated.

## The claim

The consumer's **reliability target is its read operator**. The same CQI report
and the same channel serve an **eMBB** consumer (target BLER 1e-1) and a
**URLLC** consumer (target 1e-3 here, a measurable proxy for the real 1e-5). A
**one-size certificate** calibrated to eMBB selects an aggressive MCS delivering
~1e-1 reliability -- adequate for eMBB, but a **false-clear** for URLLC, whose
budget it exceeds by >= 100x. A **consumer-aware** certificate selects the MCS
for each consumer's own target (URLLC with a robustness margin) and holds each at
its budget. The vacuity is purely consumer-relative: the *same* certificate is
adequate for one consumer and catastrophic for another, on the identical channel.

## Family F-URLLC (constructed + shaken down 2026-08-23)

Mean achieved BLER over a fresh-CSI TDL-fading trace, read directly off the real
Sionna 5G NR LDPC curves (`cs.bler_at`); CQI carries 1 dB measurement noise.
Policies: **eMBB** MCS (highest at target 1e-1), **URLLC-naive** (the eMBB MCS,
reused by the URLLC consumer), **URLLC-aware** (a conservative MCS, 4 dB backoff
below the eMBB pick, **plus K=3-branch frequency/spatial diversity** -- fail iff
all branches fail). Fresh CSI isolates the reliability-target axis (aging is
XPROTO-CSI). **A load-bearing honest finding:** MCS margin *alone* cannot reach
URLLC reliability on a Rayleigh channel -- the deep-fade outage floor (~4%)
dominates regardless of margin; URLLC reliability requires diversity, which is
why the aware policy carries it. The eMBB naive value (~0.11) is resolved
directly; the URLLC-aware value (~1e-4) is resolved by the diversity product.

## Bars (bind at seal; checked against the family record first)

- **B1 -- one-size cert vacuous for URLLC.** Per seed: `achieved_urllc_naive >=
  30 * urllc_target` (the eMBB cert delivers >= 30x URLLC's budget).
- **B2 -- consumer-aware holds.** Per seed: `achieved_urllc_aware <= 1e-3`.
- **B3 -- dominance.** Per seed: `achieved_urllc_aware <= achieved_urllc_naive / 30`.

**Manipulation checks (bars too):**
- **MC1 -- the SAME cert serves eMBB fine.** `achieved_embb <= 0.15` (<= 1.5x
  the eMBB target) -- the certificate is not broken, it is consumer-relative.
- **MC2 -- the consumers genuinely differ.** `mcs_margin >= 1.0` (eMBB uses a
  higher MCS than URLLC at their respective targets).
- **MC3 -- non-degenerate.** `n_tti >= 5000`, `mcs_var >= 2`.

**Verdict:** any MC fail -> VOID; all MCs + B1-B3 every seed -> PASS; else FAIL,
kept. **Kills:** `achieved_urllc_naive < 3*urllc_target`, or `achieved_urllc_aware
> 1e-2`.

## Seal procedure

On 2026-08-24+: confirm `URLLCREP-family.json` PASSes `--check-family`, reread,
flip STATUS to SEALED, commit; on Atlas run `fam_urllc.py --seeds 20260824
20260825 20260826 --out URLLCREP-graded-raw.json`, pull, `urllc_check.py` ->
commit `XPROTO-URLLC-graded.json`.

## Scope

Fresh CSI + link-level BLER curves at 400 blocks/point (resolution ~2.5e-3); the
single-branch URLLC tail below that floor is unresolved, so the aware value relies
on the diversity product of resolved per-branch BLERs -- the sealed rung would
measure the per-branch tail directly (more blocks / importance sampling), which
only sharpens the effect. URLLC's real 1e-5 target makes the naive false-clear
ratio ~10^4, not ~10^2. Diversity is modeled as K independent fading branches
(idealized frequency/spatial diversity); real HARQ/repetition diversity is
correlated and a later graduation. The delta is the *measured, consumer-relative*
reliability-target vacuity and the demonstration that the fix is a different
*mechanism* (diversity), not merely a more conservative certificate.

## Provenance

- Exploration: the 5G/6G applications discussion (URLLC vs eMBB as the purest
  consumer-relativity -- the target is the read operator).
- Family + grading: `fam_urllc.py` (fits the XPROTO-CSI Sionna curves);
  `urllc_check.py` (seal-guard + cooling-off + NR-only sealed grading).
