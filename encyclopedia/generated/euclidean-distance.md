# Euclidean distance

**id.** euclidean-distance
**kind.** concept

## definition

The straight-line distance between two vectors, which reads every coordinate at the scale it arrives in. Chapter 3.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 4.1.

    d_O=\operatorname{tr}(P_C\,M_\delta)\qquad\text{against}\qquad \operatorname{tr}M_\delta=d_O\big|_{P_C=I}.

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 7d91883.

## first stated

Chapter 3 section 3.2 of *Data Mining as Observation*, where a distance is a choice of what to ignore.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- The straight-line distance between two vectors, whose square is the identity reader's quadratic form on the difference, so it reads every coordinate at the scale it arrives in. It is symmetric and zero exactly between a row and itself.
- Rescaling one coordinate changes which of two rows is nearer. A choice of scale is a choice of reader, and reconstruction error, the Euclidean distance between a row and its code, is the identity reader's number and not the consumer's.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/EuclideanDistance.lean`, theorems `distSq_eq_quad_one`, `distSq_comm`, `distSq_eq_zero_iff`, `ranking_flips`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 6, 10, 11, 12.

## related

identity-reader, dot-product, mahalanobis-distance, distance-concentration

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
