# dot product

**id.** dot-product
**kind.** concept

## definition

The sum of the coordinatewise products of two vectors. Equation 0.1.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 7d91883.

## first stated

Chapter 0 section 0.1 and chapter 3 section 3.2 of *Data Mining as Observation*, with the program's cosine-versus-consumer case in `turboquant-pro/docs/KV_KEYS_FINDING.md:1-49`.

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

- The sum of the coordinatewise products of two vectors, symmetric and bilinear. The cosine, the dot product over the two lengths, lies between minus one and one by Cauchy–Schwarz and is unchanged when either vector is scaled by a positive factor, while the dot product scales with the vector.
- A cosine reader has declared length a nuisance and a dot-product reader has not, which is the reader difference of chapter 3, and cosine 0.995 between keys and their reconstruction said nothing about the softmax that read them.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DotProduct.lean`, theorems `self_nonneg`, `dot_comm`, `dot_sq_le`, `cosine_mem`, `dot_smul`, `cosine_smul`, at observation-data-mining 416c9a3.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 8, 11, 12.

## related

projection, euclidean-distance, quotient, nuisance

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 994ee12, theory-radar 37c4e6c, observation-data-mining 416c9a3, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
