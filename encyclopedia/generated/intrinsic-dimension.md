# intrinsic dimension

**id.** intrinsic-dimension
**kind.** concept

## definition

The number of directions a dataset actually varies along, whatever the number of its coordinates. Chapter 0 section 0.10.

## equation

Book equation 0.31.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}.

Book equation 9.2.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}\qquad\Rightarrow\qquad d=2\,\frac{d\log N}{d\log\lambda}.

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 7d91883.

## first stated

Weyl's law, 1911, as chapter 0 section 0.15 states it, applied in the recognizer of Volume 14 chapter 11, `geometric-observation/chapters/ch11_the_recognizer.md:1-95`, and chapter 9 section 9.2 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 3 section 3.3 | radius against degree correlation 0.92 to 0.99 | `the-angular-observer\README.md:135-139` |
| chapter 3 section 3.3 | angle 0.92 flat in m, magnitude 0.03, full 0.75 decaying | `wolfram-observer-bridge\theorem.md:1-20`; `the-angular-observer\theorem.md:187-224` |
| chapter 3 section 3.3 | substrate table | `the-angular-observer\README.md:99-109` |
| chapter 3 section 3.3 | proven versus conjectured ledger, d at least 3, d equals 2 borderline, fixed-m conditional theorem, heat filter uniform, commute metric form false, Green-kernel rank limit for d at most 3, obstruction at d equals 4 | `the-angular-observer\theorem.md:84-107,147-224`; `the-angular-observer\README.md:150-185` |
| chapter 3 section 3.3 | the self-refuted v0.8 claim, NEG-1 | `the-angular-observer\README.md:170-175`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-1 |
| chapter 3 section 3.3 | hyperbolic rejected, curvature negative 0.98 to negative 0.14, trend 1.09 minus 0.157 d across 20 manifolds and 5 families | `the-angular-observer\README.md:111-147,183-185` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 9 section 9.2 | the recognizer's mechanism, low multiplets and angular distances, dimension before shape by Weyl's law, refusal, the growth gotcha | `geometric-observation\chapters\ch11_the_recognizer.md:1-95` |
| chapter 9 section 9.2 | the battery, three new templates, frozen ratios, code hash, bars at least 10 of 12 and the dimension ordering, eccentricity scope | `the-angular-observer\PREREG_RECOGNIZER_BATTERY.md:1-80` |
| chapter 9 section 9.2 | 12 of 12, dimensions 1.81, 2.80, 1.74, angular Spearman ranges, eccentricity spreads, verdict confirmed, GO-P-2026-041 | `the-angular-observer\experiments\manifold-recovery\battery_result.json` |
| chapter 9 section 9.2 | causal set 0.57 with dimension 2.9 to 10.7, small world 0.45, control 0.01, rung 4 decay 0.747 to 0.679 below 0.75 | `the-angular-observer\README.md:99-109`; `wolfram-observer-bridge\rung4_scaledm_result.json`; `wolfram-observer-bridge\review-2.txt` |
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 14 section 14.3 | floor 0.08 to 0.12, balanced resample 3001 items, identity attack 0.237 with interval 0.20 to 0.28 on 289, sexual 0.204, threat 0.093 retracted, first pass 18 positives, 87.7 and 1.4 percent | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:20-64` |
| chapter 14 section 14.3 | contraction 0.779 to 0.863, 77 of 1600, 4.8 percent, 0.872 to 0.863, weight 2.69 | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:66-99` |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |
| chapter 14 section 14.7 | 51 percent moderated at 80 and 95 percent precision on the balanced set | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:84-88` |

## failures and corrections

none

## conditions

- The intrinsic dimension is the number of directions a dataset varies along, whatever its coordinate count. Under Weyl's law the count of eigenvalues below a level grows like the level to half the dimension, so the dimension is twice the slope of log count against log level between any two levels, whatever the constant.
- Dimension emerges before shape. The recognizer reports it with confidence before it names a manifold, and the law is an asymptotic statement about manifolds that a finite sample approximates.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/IntrinsicDimension.lean`, theorems `log_weyl`, `dimension_from_slope`, `weyl_double`, at observation-data-mining 95ef425.

## used in

*Data Mining as Observation* chapters 0, 3, 8, 9, 11.

## related

recognizer, effective-rank, distance-concentration, vacuity-threshold

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns ff35d5b, theory-radar 37c4e6c, observation-data-mining 95ef425, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
