# PREREG-XPROTO-QOT-GRAD — the reversal diagnostic run prospectively on the optical flip pair

**STATUS: DRAFT — FAMILY-CONSTRUCTED 2026-08-27, EARLIEST SEAL 2026-08-28** (cooling-off
rule: one full day between family construction and seal). Graded seeds {20260828,
20260829, 20260830}, disjoint from the calibration seeds {990..997} and the shakedown's
{0,1,2}. Substrate = fam_qot's GNPy GN-model GSNR over CORONET-CONUS (mode
"gnpy-coronet") through fam_qotflip's footprint fleets. The prospective half of the
formal core's reversal diagnostic (formal-core.tex Sec. 4, steps 3-6), on the sealed
XPROTO-QOT-FLIP pair, for the SIGMETRICS 2027 policy-reversal paper.

## Why this cell

The sealed flip records are retrospective: they measure the reversal after the fact.
The paper's anti-construction claim needs the prospective half: measure directional
sensitivities on calibration data, pass the exposure gate, REGISTER the predicted
signs and lambda*, then let fresh seeds confirm or refute the registration. This cell
is that registration. The registered numbers below are fixed by deterministic
calibration on the disclosed seeds; the graded run has no free parameters left.

## The claim

The directional exposure gate, evaluated on disclosed calibration seeds, licenses a
reversal prediction for the sealed footprint pair, and the registered signs and
lambda* band hold on fresh graded seeds. The aligned FEC control, pushed through the
same gate, does not license a reversal prediction. If the gate had abstained, the
abstention would have been the registered outcome; it did not abstain.

## Family F-QOT-GRAD (constructed + shaken down 2026-08-27)

`fam_qotgrad.py`. The sealed F-QOT-FLIP pair is reused exactly: policy A = margin
proportional to normalized reach, policy B = proportional to band-centrality + 0.05,
both normalized per seed to a 1.0 dB fleet-mean margin; K = 120 services/seed, R/P
footprint fleets as in PREREG-XPROTO-QOT-FLIP. Segment m(t) = m^B + t·d, d = m^A −
m^B, t in [0,1].

Calibration (all constants declared):
- Stencil t in {0, 1/4, 1/2, 3/4, 1}, h = 1/4. Per-class risk at each t is the mean
  false-clear over N_NOISE_REP = 20 monitoring-noise redraws (sigma 0.3 dB, common
  draws across t; this family's own noise stream, offset 5000 — it does not reuse the
  flip family's stream).
- Calibration seeds {990, 991, 992, 993, 994, 995, 996, 997}, disclosed here.
- g_c = (f_c(3/4) − f_c(1/4)) / (2h). In the t-parameterization the chain rule gives
  f_c'(t) = ∇R_c(m(t))ᵀd, so this symmetric difference IS the directional derivative
  ∇R_c(m̄)ᵀd of formal-core Def. 4; no further ||d|| normalization is applied.
- Curvature witness sec_c = (f_c(1/4) − 2f_c(1/2) + f_c(3/4)) / h², an estimate of
  dᵀ∇²R_c d. Floor term M_c = |mean_seed(sec_c)| + 2·SE_seed(sec_c) (the declared
  inflation is the 2·SE noise allowance), used as the directional refinement M_c/4.
- Gate (formal-core Eq. 10): both ratios |mean g_c| / (z·SE_c + M_c/4) > 1 with
  z = 2, SE_c the across-seed standard error of g_c. Both ratios > 1 → REGISTER;
  either ≤ 1 → ABSTAIN (recorded as the registered outcome, no prediction).
- lambda* estimator (declared): lambda* = ḡ_P/(ḡ_P − ḡ_R) from the MEAN calibration
  directional derivatives — the formal core's step-5 estimator, chosen because the
  registration is a statement about the derivatives the gate licensed, not about the
  endpoint deltas (which are recorded alongside for comparison). Band = registered
  lambda* ± max(2·spread, 0.05), spread = across-seed std of per-seed lambda_g;
  the 0.05 floor keeps the band honest when the calibration spread is accidentally
  small.

Graded evaluation: per graded seed, endpoints m^B and m^A with a single
monitoring-noise draw (stream offset 5000), per-class deltas, signs, and lambda* =
ΔR_P/(ΔR_P − ΔR_R).

## Disclosed pilots (design iteration before this registration; no sealed bar existed)

Pilot 1 (2026-08-27, calibration seeds {990..997}): the first floor construction used
M_c = 3·max_seed|sec_c|. The single-seed second differences are dominated by
Monte Carlo sampling noise (spread ~0.3, sign flips across seeds), so this floor
charges the sampling noise twice (once in z·SE_c, once in M_c) and the gate ABSTAINED
with ratios 0.586 / 0.721 on a pair whose graded reversal is already sealed and
robust. The estimator was replaced by the mean + 2·SE witness above BEFORE any seal.
The pilot is disclosed here, not hidden; both floors are deterministic functions of
the same calibration data.

## Registered calibration outcome (deterministic on the disclosed seeds; pilot-derived, disclosed)

All numbers printed by `fam_qotgrad.py --calibrate` and stored in
`QOTGRADREP-calibration.json`:

- ḡ_R = −0.38354, SE_R = 0.03232, M_R = 0.55373, floor_R = 0.20308, ratio_R = 1.889.
- ḡ_P = +0.25125, SE_P = 0.01920, M_P = 0.22723, floor_P = 0.09521, ratio_P = 2.639.
- **Gate: REGISTER.** Predicted signs: ΔR_R < 0, ΔR_P > 0 (reversal predicted).
- **Registered lambda* = 0.3958**, calibration spread 0.0789, band halfwidth
  max(2·0.0789, 0.05) = 0.1579, **band [0.2379, 0.5537]**.
- Control (FEC SD/HD through the same gate): ratios 1.461 / 0.100, not licensed, no
  opposite signs. MC4 holds.

## Bars (bind at seal; graded on {20260828, 20260829, 20260830})

- **B1 — signs.** Per seed: sign(ΔR_R) = −1 and sign(ΔR_P) = +1 (the registered
  signs).
- **B2 — lambda* band.** Per seed: lambda* in [0.2379, 0.5537].

**Manipulation checks (bars too):**
- **MC1 — sane evaluation.** Per graded seed: all four class false-clears strictly
  inside (0,1). (At calibration: every stencil risk strictly inside (0,1); held.)
- **MC2 — the policies differ.** Per graded seed: RMS(d) ≥ 0.1 dB.
- **MC3 — calibration stability.** At registration: SE_c ≤ 0.5·|ḡ_c| for both
  classes (held: 0.084 and 0.076 relative).
- **MC4 — the aligned control does not falsely license.** At registration: the FEC
  pair through the same gate must not license an opposite-sign prediction (held:
  ABSTAIN, same-sign means).

**Verdict:** any MC fail → VOID; B1 + B2 every graded seed → PASS; else FAIL, kept.
**Kills:** a graded sign flip against the registration on any seed, or graded
lambda* outside the band on any seed.

## Shakedown (2026-08-27, seeds {0,1,2} as graded stand-ins; NEVER quoted in papers)

`QOTGRADREP-shakedown.json`: sign_match TRUE and lambda* in band on all three seeds
(lambda* 0.3438 / 0.3103 / 0.3529); shakedown verdict PASS. Runtime: calibration
~1 s + GNPy comb precompute ~1 s; graded stand-in <1 s (combs cached in-process).
Shakedown numbers stand in for nothing beyond code correctness.

## Seal procedure

On 2026-08-28+: reread this prereg, confirm `QOTGRADREP-calibration.json` reproduces
the registered numbers above (`fam_qotgrad.py --calibrate` is deterministic), flip
STATUS to SEALED, commit; run `fam_qotgrad.py --graded --seeds 20260828 20260829
20260830` in the qot venv; write the check script `qotgrad_check.py` (coded
cooling-off + substrate guard, house pattern) and commit
`XPROTO-QOT-GRAD-graded.json`.

## Scope

The claim is that the diagnostic's registration-then-grade loop closes on this
substrate: licensed predictions hold, the aligned control does not falsely license.
It is not a claim that the gate licenses every reversal (formal-core Prop. 5 shows
both failure directions) nor that the floor constants are optimal. Provenance:
formal-core.tex (Def. 4, Prop. 2, Eq. 10, diagnostic box), XPROTO-QOT-FLIP (sealed
pair), `fam_qotgrad.py`.
