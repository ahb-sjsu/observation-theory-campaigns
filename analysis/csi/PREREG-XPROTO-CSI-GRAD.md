# PREREG-XPROTO-CSI-GRAD — the reversal diagnostic run prospectively on the radio flip pair

**STATUS: DRAFT — FAMILY-CONSTRUCTED 2026-08-27, EARLIEST SEAL 2026-08-28** (cooling-off
rule: one full day between family construction and seal). Graded seeds {20260828,
20260829, 20260830}, disjoint from the calibration seeds {990..994} and the shakedown's
{0,1,2}. Substrate = real Sionna 5G NR LDPC BLER curves + TDL-A fading (`csi_sionna`,
mode "nrsionna") through fam_csiflip's fleets. The radio twin of XPROTO-QOT-GRAD: one
diagnostic, two substrates, for the SIGMETRICS 2027 policy-reversal paper.

## Why this cell

The sealed flip records are retrospective. The paper's anti-construction claim needs
the prospective half of the formal core's diagnostic (formal-core.tex Sec. 4, steps
3-6): measure the directional sensitivities on calibration seeds, pass the exposure
gate, REGISTER signs and lambda*, then grade on fresh seeds. This cell is the radio
registration. The registered numbers are deterministic functions of the disclosed
calibration seeds; the graded run has no free parameters left.

## The claim

The directional exposure gate, evaluated on disclosed calibration seeds, licenses a
reversal prediction for the sealed Doppler/deficit pair, and the registered signs and
lambda* band hold on fresh graded seeds. The aligned threshold-pair control, pushed
through the same gate, licenses only a SAME-SIGN prediction (no reversal), the
taxonomy's expected behavior for aligned reads on this substrate.

## Family F-CSI-GRAD (constructed + shaken down 2026-08-27)

`fam_csigrad.py`. The sealed F-CSI-FLIP pair is reused exactly: 12 users per fleet
(M: 200 Hz Doppler, 12 dB mean SNR; S: 10 Hz, 7 dB), per-user TDL-A traces with the
flip family's sub-seeds, 6000 TTI, 20-TTI held reports, 1 dB report noise; policy A =
margin proportional to Doppler, policy B = proportional to SNR deficit + 0.05, both
normalized to a 1.5 dB fleet mean. Segment m(t) = m^B + t·d, d = m^A − m^B.

Calibration (all constants declared):
- Stencil t in {0, 1/4, 1/2, 3/4, 1}, h = 1/4. Per-class risk at each t = mean
  empirical HARQ NACK rate over the fleet, with the per-user random streams seeded
  exactly as the sealed flip evaluation (seed·7+i), so all stencil points share
  common random numbers and differences isolate the margin effect. No extra noise
  redraws are needed (72000 TTI-draws per fleet per point).
- Calibration seeds {990, 991, 992, 993, 994}, disclosed here (5 seeds, not the
  QOT cell's 8: one radio calibration seed costs ~7 s against the QOT cell's
  milliseconds, and the radio spread is an order of magnitude tighter).
- g_c = (f_c(3/4) − f_c(1/4)) / (2h); in the t-parameterization this IS the
  directional derivative ∇R_c(m̄)ᵀd (chain rule); no further ||d|| normalization.
- Curvature witness sec_c = (f_c(1/4) − 2f_c(1/2) + f_c(3/4)) / h²; floor term
  M_c = |mean_seed(sec_c)| + 2·SE_seed(sec_c) (the declared inflation is the 2·SE
  noise allowance; same estimator as F-QOT-GRAD, adopted after the disclosed QOT
  pilot showed a max-based floor double-charges sampling noise).
- Gate (formal-core Eq. 10): both ratios |mean g_c| / (z·SE_c + M_c/4) > 1 with
  z = 2. Both > 1 → REGISTER; either ≤ 1 → ABSTAIN (a legitimate registered
  outcome).
- lambda* estimator (declared): lambda* = ḡ_S/(ḡ_S − ḡ_M) from the MEAN calibration
  directional derivatives (formal-core step 5; endpoint deltas recorded alongside).
  Band = registered lambda* ± max(2·spread, 0.05); the 0.05 floor bites here
  because the calibration spread is 0.0062.

Graded evaluation: per graded seed, endpoints m^B and m^A; this is draw-for-draw
the sealed F-CSI-FLIP evaluation, so graded cells at overlapping seeds must
reproduce the sealed record's fc values exactly (a built-in substrate guard).

## Registered calibration outcome (deterministic on the disclosed seeds; pilot-derived, disclosed)

All numbers printed by `fam_csigrad.py --calibrate` and stored in
`CSIGRADREP-calibration.json`:

- ḡ_M = −0.13896, SE_M = 0.00097, M_M = 0.05595, floor_M = 0.01592, ratio_M = 8.728.
- ḡ_S = +0.09798, SE_S = 0.00131, M_S = 0.16343, floor_S = 0.04347, ratio_S = 2.254.
- **Gate: REGISTER.** Predicted signs: ΔR_M < 0, ΔR_S > 0 (reversal predicted).
- **Registered lambda* = 0.4135**, calibration spread 0.0062, band halfwidth
  max(2·0.0062, 0.05) = 0.05, **band [0.3635, 0.4635]**.
- Control (one M-trace at required-SNR shifts 0/+2 dB, protect-low 3.0 dB vs
  protect-high 0.75 dB scalar margins, through the same gate): ratios 2.026 / 3.960,
  LICENSED with SAME signs (ḡ_t1 = −0.0993, ḡ_t2 = −0.0760; more margin helps both
  thresholds). MC4 holds on the license-same-sign branch: aligned reads license a
  common-direction prediction, not a reversal.

## Bars (bind at seal; graded on {20260828, 20260829, 20260830})

- **B1 — signs.** Per seed: sign(ΔR_M) = −1 and sign(ΔR_S) = +1 (the registered
  signs).
- **B2 — lambda* band.** Per seed: lambda* in [0.3635, 0.4635].

**Manipulation checks (bars too):**
- **MC1 — sane evaluation.** Per graded seed: all four fleet NACK rates strictly
  inside (0,1). (At calibration: every stencil risk strictly inside (0,1); held.)
- **MC2 — the policies differ.** Per graded seed: RMS(d) ≥ 0.5 dB.
- **MC3 — calibration stability.** At registration: SE_c ≤ 0.5·|ḡ_c| for both
  classes (held: 0.007 and 0.013 relative).
- **MC4 — the aligned control does not falsely license.** At registration: the
  threshold-pair control through the same gate must not license an opposite-sign
  prediction (held: licensed, same sign).

**Verdict:** any MC fail → VOID; B1 + B2 every graded seed → PASS; else FAIL, kept.
**Kills:** a graded sign flip against the registration on any seed, or graded
lambda* outside the band on any seed.

## Shakedown (2026-08-27, seeds {0,1,2} as graded stand-ins; NEVER quoted in papers)

`CSIGRADREP-shakedown.json`: sign_match TRUE and lambda* in band on all three seeds
(lambda* 0.4342 / 0.4263 / 0.4383); shakedown verdict PASS. Runtime on Atlas CPU
(TF intra-op capped at 16 threads): calibration 39.3 s total (~7.3 s per seed),
graded stand-in 11.1 s (~3.7 s per seed), cached LDPC curves. Shakedown numbers
stand in for nothing beyond code correctness.

## Seal procedure

On 2026-08-28+: reread this prereg, confirm `CSIGRADREP-calibration.json`
reproduces the registered numbers (`fam_csigrad.py --calibrate` is deterministic),
flip STATUS to SEALED, commit; on Atlas run `fam_csigrad.py --graded --seeds
20260828 20260829 20260830` (sionna-venv, CPU), pull; write `csigrad_check.py`
(coded cooling-off + substrate guard, house pattern) and commit
`XPROTO-CSI-GRAD-graded.json`.

## Scope

The claim is that the diagnostic's registration-then-grade loop closes on the radio
substrate, and that the aligned control licenses only a same-sign prediction. It is
not a claim that the gate licenses every reversal (formal-core Prop. 5), nor about
allocator optimality. Provenance: formal-core.tex (Def. 4, Prop. 2, Eq. 10,
diagnostic box), XPROTO-CSI-FLIP (sealed pair), XPROTO-QOT-GRAD (optical twin,
disclosed floor pilot), `fam_csigrad.py`.
