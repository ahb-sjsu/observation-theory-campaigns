# direction-only quantizer

**id.** direction-only-quantizer
**kind.** instrument

## definition

A quantizer that stores each vector's length exactly and rounds its direction. Chapter 11.

## equation

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.
- GO-B-LOCATA. Real microphone-array recordings (LOCATA), DOA consumer — held-out confirmation with the PolarQuant compressor `[predicted]`. `geometric-observation/claims/LEDGER.md:117` at 9f3829f.

## first stated

Chapter 11 section 11.2 of *Data Mining as Observation*, with PolarQuant in `turboquant-pro/docs/KV_KEYS_FINDING.md:1-49` and the LOCATA comparison of the ledger.

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

- A quantizer that stores each vector's length exactly and rounds its direction to a unit codeword. The quantized vector keeps the original's length, its cosine with any query is the codeword's cosine, and its score against a query is the length times the query's dot product with the codeword, so the score error is the length times the query's dot product with the direction error.
- A key's cosine with its own quantized form can be near one while its score against a query moves by a multiple of its length, which is why keys at cosine 0.995 raised the perplexity by three orders of magnitude.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DirectionQuantizer.lean`, theorems `length_preserved`, `score_eq`, `score_error`, `cosine_eq`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 11.

## related

quantization, dot-product, kv-cache, attention, flip

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
