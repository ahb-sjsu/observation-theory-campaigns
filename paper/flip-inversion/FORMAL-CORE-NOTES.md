# FORMAL-CORE-NOTES — status of the formal core (2026-08-27)

Companion to `formal-core.tex` (future Sections 2–3 of the SIGMETRICS 2027
policy-reversal paper) and `flip_theorem_checks.py` (7/7 checks PASS).

## Proved at full rigor

- **Prop 1 (exact directional form).** Mean value theorem; exact, unmeasurable.
- **Lemma 1 (midpoint bound).** |ΔR_c − ∇R_c(m̄)ᵀd| ≤ (L_c/4)‖d‖². The
  constant is **1/4, not 1/8** (the per-side Taylor bound is L/8 per
  half-step; the worst case adds; the V-derivative instance attains L‖d‖²/4
  exactly, refuting 1/8). On quadratic risks the midpoint estimate is exact
  (error 0), so near-tightness is exhibited on the piecewise-quadratic
  instance, not on a quadratic; T1 verifies both, plus the bound on random
  quadratic / Gaussian-shortfall / sinusoid families.
- **Prop 2 (predictive criterion).** Sign transfer under the directional
  margin, hence reversal from opposite-sign midpoint directional derivatives.
- **Exposure gate (owner correction applied, directional + normalized):**
  E_c(d) = |∇R_c(m̄)ᵀd| > z·SE_c + (L_c/4)‖d‖² for both classes
  (equivalently both exposure ratios > 1; directional refinement M_c/4
  allowed). Magnitude-only exposure appears nowhere.
- **Prop 3 (mixture crossover).** Exact; λ* = ΔR_2/(ΔR_2 − ΔR_1); sign
  change in (0,1) iff reversal; corollary: no mixture-free scalar ranking.

## Constructed and verified numerically (illustrated, not theorems about the studied systems)

- **Prop 4(a)** reversal with an identical read operator (crossing
  Gaussians; gate PASSES it, ratios 4.27 / 3.37).
- **Prop 4(b1)** misaligned reads, large gradient norms, gradients orthogonal
  to d: ΔR ≡ 0, E_c(d) = 0, gate abstains.
- **Prop 4(b2)** misaligned reads ~4σ from threshold: same-sign negligible
  deltas, exposure below floor by 10³–10⁴.
- Scope is held at sufficiency throughout: misalignment + exposure is a
  sufficient, empirically predictive mechanism in the studied systems, never
  stated as necessary.

## Worked instances (graded records, retrospective half only)

Per-seed λ* (weight on class 1 = R resp. M): QOT 0.382 / 0.412 / 0.422;
CSI 0.426 / 0.432 / 0.429. Even-mixture fleet signs consistent with
λ = 1/2 > λ* on all six cells; aligned controls (fec, null) same-sign on
every seed. All recomputed by T5/T6 from the raw graded JSONs.

## What remains for the paper (NEW sealed work per OUTLINE.md)

- **Gradient-prediction cells** (diagnostic steps 3–5 prospectively: measure
  ĝ_c and SE_c on calibration seeds, register signs + λ* through the gate,
  then grade). This document supplies the registered predictions' formal
  basis; the existing graded records predate the gradient registration.
- **Cost-matched variants** (resource equivalence in C = capacity/goodput,
  not nominal dB; Eq. (1) is the exact criterion to match against).
- **Phase-diagram cells** (reach × spectral position; Doppler × mean SNR).
- Baselines (uniform, max-min), goodput-primary verdicts, POMACS format,
  anonymization. All family → shakedown → prereg → cooled seal → graded.

## Build

```
cd paper\flip-inversion
C:\Users\abptl\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe formal-core.tex   (run twice)
python flip_theorem_checks.py   (must print 7/7 PASS)
```

Current build: 8 pages, zero undefined references. Bibliography entries
carry `% verify` marks where records were not fully confirmed (FAMS 2023
authors; Simpson/Athey vol/pages).
