# The conversion determinant — post-hoc study (2026-09-03, owner-directed)

**Question:** what determines per-unit conversion of headroom into graded gain
(measured 190%/101%/74%/9%/~0 within V2 alone)?
**Instruments:** `cr_ann_conversion_pm.py` → `prereg/conversion_pm.json`,
all 13 graded units of both sealed families. Post-hoc exploratory; both FAIL
verdicts stand untouched.

## Candidates tested

| candidate potential | Spearman | Pearson | slope | verdict |
|---|---|---|---|---|
| xbse reliability weights (V1 B3) | ≈0 | — | — | dead |
| H = D − A (classification headroom; both preregs) | 0.181 | — | — | dead |
| R_C − A (retrieval headroom, single split) | 0.352 | 0.834 | 1.11 | see below |
| Φ = 5-fold cross-fit (R_C − A) | **0.220** | **0.908** | 1.30 | see below |

Cross-fitting did NOT rescue the rank correlation (0.352 → 0.220); the
split-noise hypothesis for the residuals is refuted as the whole story. The
high Pearson is carried by the one large-Φ unit (care).

## The decomposition that explains everything

With the oracle ceiling ≈ 1 and k = 50 nearly global, the graded gain IS the
grading-split retrieval headroom under the frozen probe metric — close to
definitionally. So the scientific content of any conversion law is exactly:
**does calibration-measured retrieval headroom forecast grading-realized
retrieval headroom?** Measured over 13 units:

- **Magnitude scale: yes.** Pearson 0.9, slope 1.1–1.3 — Φ is the right
  quantity and roughly unit-calibrated.
- **Rank order among small effects: no.** The per-unit fold-SD of Φ is
  0.011–0.058, and 10 of 13 measured gains are smaller than 0.06: the effects
  of interest sit AT the instrument's noise floor (privacy_aita: Φ = +0.015 ±
  0.058 at n_cal = 460 — the SD is four times the prediction). Where Φ stands
  ~11σ from zero (care: 0.201 ± 0.018), the forecast works (measured 0.274).
- **Plus real generalization failure, beyond noise:** fairness_mhs
  (+0.042 ± 0.022 → +0.008) and societal_env (+0.029 ± 0.025 → −0.003)
  overpredict by more than their fold-SD; identity_attack underpredicts
  (+0.025 ± 0.014 → +0.057). Calibration-split probe-metric headroom does not
  fully transfer to the grading distribution for these corpora.

## Conclusion — and why NO V3 is drafted on this potential

The determinant is identified in kind — **gain is the probe metric's retrieval
headroom, Φ, at roughly unit slope** — but Φ is not forecastable from
calibration at these unit sizes for effects below ~0.06, which is where almost
all natural units live. A prereg barred on Spearman(Φ, gain) ≥ 0.6 would seal
a bar the construction data itself fails at 0.22; that would be manufacturing
a third FAIL, and the owner's "seal V3 tomorrow if the numbers hold"
conditional is therefore NOT met. No V3 is drafted.

**What a viable V3 would require (recorded for the owner, not drafted):**
- **Power rule:** qualify only units with Φ_xfit ≥ 3 × fold-SD(Φ) — in the
  current pool only care passes; a family needs several, so either
  (a) engineered large-Φ units (cross-topical attributes over
  topically-clustered corpora — the construction sweep's log_length is the
  template), or (b) calibration corpora ~10× larger to push the noise floor
  under the natural 0.01–0.05 effects.
- A shift diagnostic (calibration-vs-grading Φ stability) as a manipulation
  check, since noise is not the only failure mode.

**The alternative that needs no new seal:** the graded record now supports a
paper as-is — the dissociation exists (13/16 anisotropic units positive,
recall collapse universal, matched nulls hold), its magnitude equals the
consumer's retrieval headroom at unit slope, and that magnitude is
demonstrably not forecastable from the consumer's own calibration view at
natural corpus sizes. Two honest sealed FAILs are the evidence trail of that
last clause — arguably the most OT-flavored finding in the campaign: the
quantity is real, but this observer's calibration channel cannot see it in
advance.


## Addendum (owner challenge, 2026-09-03 late)

The owner challenged the "not forecastable" conclusion, and the challenge is
sustained on two points and partially on a third. (1) The gain IS measurable
in advance in principle: it is itself a retrieval statistic, and Phi is
exactly that pre-measurement on calibration data. The correct statement is a
RESOLUTION limit: at n_cal = 460-4,200 the pre-measurement's sampling noise
(0.011-0.058) is the size of most natural effects, so both sealed families
barred distinctions finer than the instrument could resolve. Forecastability
is a power question; noise shrinks as sqrt(n). (2) The paper's title and
closing overclaimed relative to this; corrected in the same-day commit.
(3) The "genuine calibration-to-grading shift beyond fold noise" claim above
is WEAKENED: calibration and grading are exchangeable random splits of one
corpus, so prediction-versus-outcome deviations are consistent with
two-sided sampling noise of both quantities; the largest single deviation
(fairness_mhs, ~1.5 sigma) does not establish shift. The study's candidate
rankings, tables, and the no-V3 decision are unaffected: sealing against a
bar finer than the instrument's resolution remains wrong regardless of
which framing explains the residuals.
