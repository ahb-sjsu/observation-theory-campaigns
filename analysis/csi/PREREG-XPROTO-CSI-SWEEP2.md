# PREREG-XPROTO-CSI-SWEEP2 — the CSI age horizon at the true 0.10 budget (calibrated recompute)

**STATUS: UNSEALED.** FAMILY-CONSTRUCTED: 2026-08-26. Earliest compliant seal
**2026-08-27** (`csi_sweep2_check.py` codes the cooling-off). Graded seeds
{20260827, 20260828, 20260829}, disjoint from the pilots' {0,1,2} and the
calibration seed 999. Substrate = real Sionna 5G NR LDPC BLER curves + TDL-A
fading (`csi_sionna`, mode "nrsionna"), held CSI, empirical HARQ NACK rate.

## Why this cell exists (the correction it seals)

External review of the WCNC draft found that the age-horizon sweep behind the
claimed 0.177·Tcoh law (`csi_sweep.py`) measured its floors at a relaxed 0.15
threshold while the paper claimed the 0.10 target, and that its fresh baseline
(BLER ≈ 0.113) never met the budget in the first place. Both records are kept;
this cell recomputes the horizon honestly: calibrate the fresh baseline to the
budget first, then floor at the budget itself, censor rather than clamp.

## The claim

At the paper's own 0.10 budget, with the fresh baseline calibrated to genuinely
meet it, the age horizon collapses. The largest compliant report period is a few
TTI at 10 Hz Doppler and at most 2 TTI at 50 Hz and above. The
coherence-proportional law of the 0.15-threshold exploration does not survive:
the origin-fit slope falls well below the exploration's 0.177 and the fit is
weak, because there is almost no horizon left to scale. Operationally: periodic
reporting alone cannot protect a tight budget at any practical mobility, and the
HARQ-witnessed correction (OLLA) is mandatory rather than optional.

## Family F-CSI-SWEEP2 (constructed + piloted 2026-08-26)

`fam_csi_sweep2.py`: calibration first — the smallest backoff D_cal in 0.25 dB
steps for which the FRESH policy achieves BLER ≤ 0.09 at every Doppler on the
disclosed calibration seed 999 (pilot: D_cal = 0.5 dB). All policies then carry
D_cal. Per graded seed: f_D ∈ {10, 25, 50, 100, 200, 400} Hz, report periods
P ∈ {1, 2, 3, 4, 6, 8, 12, 16, 24, 32} TTI, 12 000 TTI per point, 1 dB report
noise. P*(f_D) = max{P : held-CSI BLER ≤ 0.10}; no compliant period → CENSORED,
never clamped. OLS through the origin of floor_ms on Clarke T_coh, non-censored
points only.

*Pilot trail (disclosed, kept): pilot 1 (coarse periods {1,2,4,8,16,32,64},
6 000 TTI, seeds {0,1,2}) — floors {10: 5, 25: 2, ≥50: 1}, instrument too coarse
at the collapsed scale and seed-2 fit unstable (R² = −1.77). Pilot 2 (this
family's grid, seeds {0,1,2}) — floors {10: 4/4/3, 25: 2/2/2, ≥50: 1}, no
censoring, fresh_worst 0.078–0.090, slopes 0.081–0.101, R² 0.25–0.74.*

## Bars (bind at seal; checked against the family record first)

- **B1 — the fresh baseline meets the budget.** Per seed: fresh BLER ≤ 0.10 at
  every Doppler (with the family's D_cal).
- **B2 — collapse at mobility.** Per seed: floor ≤ 2 TTI at every
  f_D ∈ {50, 100, 200, 400} Hz.
- **B3 — a handful of TTI at low mobility.** Per seed: 1 ≤ floor(10 Hz) ≤ 6 TTI
  (the 0.15-law would predict ≈ 7.5).
- **B4 — the proportional law does not survive.** Per seed: origin-fit slope
  ≤ 0.14 (exploration's was 0.177).

**Manipulation checks (bars too):**
- **MC1 — floors monotone.** Per seed: floors non-increasing in f_D.
- **MC2 — aging hurts.** Per seed, per Doppler: BLER(P=32) ≥ BLER(P=1) − 0.01.
- **MC3 — substrate + design constants.** mode "nrsionna", target 0.10,
  cal_margin 0.09, cal_seed 999, ntti 12000, D_cal ≤ 4.0 dB.
- **MC4 — no censoring.** Per seed: censored list empty (given B1, P = 1 must
  qualify; a censored Doppler signals a calibration inconsistency).

**Verdict:** any MC fail → VOID; all MCs + B1–B4 every seed → PASS; else FAIL,
kept. **Kills:** any censored Doppler, or floor(10 Hz) > 6 on any graded seed.

## Seal procedure

On 2026-08-27+: confirm `CSISWEEP2REP-family.json` PASSes `--check-family`,
reread, flip STATUS to SEALED, commit; on Atlas run `fam_csi_sweep2.py --seeds
20260827 20260828 20260829 --out CSISWEEP2REP-graded-raw.json` (sionna-venv,
CPU), pull, `csi_sweep2_check.py` → commit `XPROTO-CSI-SWEEP2-graded.json`, then
swap the graded floors into WCNC §IV and regenerate `age_horizon` (fig 3).

## Scope

The claim is the collapse of the horizon at the true budget and the death of
the proportional law there, not a new reporting scheme. The proportional
behaviour at relaxed thresholds is real and stays in the record as exploration.
Provenance: `csi_sweep.py` (superseded exploration), review round 2026-08-26,
`fam_csi_sweep2.py`, `csi_sweep2_check.py`.
