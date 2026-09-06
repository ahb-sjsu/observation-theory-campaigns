# cosine

**id.** cosine
**kind.** concept

## definition

The dot product divided by the product of the two lengths, between minus one and one, unchanged by rescaling either vector. Its distance is the angle. Equation 0.1.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 0 section 0.1 of *Data Mining as Observation*, equation 0.1, with the program's cosine-against-consumer negative in `turboquant-pro/docs/KV_KEYS_FINDING.md:1-49`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 12 section 12.3 | uncompressed 0.79, centred 0.84 | `geometric-observation\claims\LEDGER.md` row GO-B-legal |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- The dot product divided by the product of the two lengths. By Cauchy and Schwarz it lies between minus one and one, a vector has cosine one with itself, rescaling either vector by a positive factor does not change it, and it is the dot product of the two row-normalized vectors, so its distance is the angle on the quotient that discards length.
- A reconstruction cosine of 0.995 sat beside a consumer's perplexity of ten thousand, so the cosine is never an acceptance metric for a code, and on a spectral embedding the cosine is the right similarity because the length has converged to degree noise.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Cosine.lean`, theorems `abs_dot_le`, `cosine_le_one`, `neg_one_le_cosine`, `cosine_self`, `cosine_smul`, `cosine_eq_dot_rowNormalize`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 5, 6, 8, 10, 11, 12.

## related

dot-product, euclidean-distance, spectral-embedding, quotient, identity-reader

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
