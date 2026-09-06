# quantization

**id.** quantization
**kind.** concept

## definition

Replacing each number with one of a small set of allowed values so that it can be stored in a few bits. Chapter 0 section 0.11.

## equation

Book equation 0.13.

    D(b)=\sum_i s_i v_i\,4^{-b_i},\qquad b_i=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i v_i}{\theta}\Big),\qquad \sum_i b_i=B.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.
- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 7d91883.

## first stated

Chapter 0 section 0.11 and chapter 11 section 11.2 of *Data Mining as Observation*, with the program's quantizer table in `turboquant-pro/docs/KV_KEYS_FINDING.md:1-49`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 8 section 8.9 | 13.7 ROUGE-L, 0.25/4.19/9.60/13.7 at 64/128/256/512, re-validation negative 0.31 n=40, 26.64 under symmetric nf4, `_quant_nf4a_group` unchanged since `289bdfc` before `4f7baab` | `turboquant-pro\CLAIMS.md:63-81`; `turboquant-pro\benchmarks\kvquant_matrix\REVAL-2026-08-08.md` |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- Replacing each number with one of a small set of allowed values so that it can be stored in a few bits. A uniform quantizer with a given step has error at most half the step and zero error on a level, and halving the step halves the bound.
- Those are the identity reader's bounds. What a quantizer does to a consumer is the flip's question, and the key quantizer table of chapter 11 is the case in which the smaller reconstruction error was the worse code.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Quantization.lean`, theorems `error_le_half_step`, `quantize_level`, `half_step_bound`, `sq_error_le`, `finer_step`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 0, 2, 3, 4, 7, 8, 10, 11.

## related

bit, codebook, per-channel-quantizer, direction-only-quantizer, flip

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
