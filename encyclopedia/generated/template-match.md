# template match

**id.** template-match
**kind.** instrument

## definition

Comparing a measured list of numbers, such as eigenvalue ratios, to a stored list for each candidate shape and picking the smallest distance between the logarithms. Equation 0.32.

## equation

Book equation 0.32.

    \operatorname{dist}(m,t)=\sqrt{\frac18\sum_{k=1}^{8}\big(\ln m_k-\ln t_k\big)^{2}}.

Book equation 9.3.

    \hat\mu=\frac{\bar s_{\mathrm{true}}-\bar s_{\mathrm{distr}}}{\sigma_{\mathrm{distr}}},\qquad \mu_{\mathrm{crit}}=\mathbb E\Big[\max_{N-1}\mathcal N(0,1)\Big],\qquad \rho=\frac{\hat\mu}{\mu_{\mathrm{crit}}},\qquad \rho=1\ \text{vacuous}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 7d91883.

## first stated

Volume 14, chapter 11, `geometric-observation/chapters/ch11_the_recognizer.md:1-95`, DOI 10.5281/zenodo.21776291, and the recognizer battery in the-angular-observer.

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
| chapter 9 section 9.2 | the battery, three new templates, frozen ratios, code hash, bars at least 10 of 12 and the dimension ordering, eccentricity scope | `the-angular-observer\PREREG_RECOGNIZER_BATTERY.md:1-80` |
| chapter 9 section 9.2 | 12 of 12, dimensions 1.81, 2.80, 1.74, angular Spearman ranges, eccentricity spreads, verdict confirmed, GO-P-2026-041 | `the-angular-observer\experiments\manifold-recovery\battery_result.json` |
| chapter 9 section 9.2 | causal set 0.57 with dimension 2.9 to 10.7, small world 0.45, control 0.01, rung 4 decay 0.747 to 0.679 below 0.75 | `the-angular-observer\README.md:99-109`; `wolfram-observer-bridge\rung4_scaledm_result.json`; `wolfram-observer-bridge\review-2.txt` |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |

## failures and corrections

none

## conditions

- Comparing a measured list of numbers, the eigenvalue ratios, to a stored list for each candidate shape and picking the smallest root-mean-square distance between the logarithms. The distance is zero between a list and itself, symmetric, and unchanged when both lists are scaled by the same factor, so the match reads shape and not size.
- The templates are frozen before the battery is run, with their code hash recorded, and the match can only name shapes in its template set, which is why the recognizer also certifies that none is present.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Recognizer.lean`, theorems `templateDist_self`, `templateDist_comm`, `templateDist_scale`, `templateDist_nonneg`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 0, 2, 8, 9, 14.

## related

recognizer, vacuity-threshold, intrinsic-dimension, laplacian

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
