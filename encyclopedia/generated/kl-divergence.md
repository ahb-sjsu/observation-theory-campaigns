# KL divergence

**id.** kl-divergence
**kind.** concept

## definition

A measure of how far one probability distribution is from another, zero when they are identical. Equation 0.24.

## equation

Book equation 0.24.

    \mathrm{KL}(p\,\|\,q)=\sum_i p_i\ln\frac{p_i}{q_i}\ \ge 0.

Book equation 0.22.

    \mathrm{PPL}=2^{H},\qquad H=-\frac1T\sum_{t=1}^{T}\log_2 p\big(w_t\mid w_{<t}\big).

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.

## first stated

Kullback and Leibler, on information and sufficiency, 1951, as chapter 0 section 0.11 states it beside perplexity, with the program's case in `turboquant-pro/docs/KV_KEYS_FINDING.md:1-49`.

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

- The expected log ratio of two distributions' masses under the first. It is nonnegative by Gibbs' inequality, zero when the distributions agree, and not symmetric, so the direction of the comparison is part of the claim.
- The book's use is through perplexity. A reconstruction at cosine 0.995 raised the perplexity by three orders of magnitude, which is the case that reconstruction error is not the consumer's error.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/KL.lean`, theorems `kl_nonneg`, `kl_self`, `kl_not_symm`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 1, 8, 11.

## related

identity-reader, read-distortion, calibration, flip

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
