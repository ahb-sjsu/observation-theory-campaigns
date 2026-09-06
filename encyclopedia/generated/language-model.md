# language model

**id.** language-model
**kind.** concept

## definition

A model that reads a sequence of tokens and outputs a probability for the next one, scored by perplexity. Chapter 0 section 0.11.

## equation

Book equation 0.22.

    \mathrm{PPL}=2^{H},\qquad H=-\frac1T\sum_{t=1}^{T}\log_2 p\big(w_t\mid w_{<t}\big).

Book equation 0.23.

    \operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_j e^{z_j}},\qquad \text{output}=\sum_i\operatorname{softmax}\!\Big(\frac{q\cdot k_i}{\sqrt{d}}\Big)_{\!i}\,v_i.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- NEG-16 (KV serving, end-task). *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task. `[refuted]`. `geometric-observation/claims/LEDGER.md:92` at 9f3829f.
- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.

## first stated

Chapter 0 section 0.11 of *Data Mining as Observation*, with the serving measurements in `geometric-observation/experiments/GO-kv-serving-flip-NOTES.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 13 section 13.6 | attempt one, six gates, 4 pass, K3 0.075 vs 0.15, K4 0.050 vs 0.10, arms 0.925, 0.925, 0.900, 0.850, recon ratio 1.000000, n 40, mechanism 15 to 36 times | `geometric-observation\experiments\GO-kv-serving-flip-NOTES.md:1-40`; `geometric-observation\prereg\GO-P-2026-056-kv-serving-flip.md:1-40`; `geometric-observation\results\GO-KV-serving-flip-7B.json` |
| chapter 13 section 13.6 | attempt two, broken proxy, control did not exist, identifier burned, 16 prompts, 1360 s | `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md:1-15`; `geometric-observation\results\GO13-kvaw-pilot-disclosed.json` |
| chapter 13 section 13.6 | attempt three, windows 1024, 256, 32, uncertainty 0.982 to 0.892, 5 of 6, 0.4375 with SE 0.070 at 5 percent keep vs 0.30, 97 percent eviction, oracle-miss 0.370 vs 0.25, V4 0.078 vs 0.0625, contrast 0.359 with SE 0.068, n 64, seed 20260812, 89 duty cycles | `geometric-observation\claims\LEDGER.md` row GO-2/GO-12/GO-13 operational; `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md`; `geometric-observation\results\GO13-kvaw2-governed.json` |

## failures and corrections

- NEG-16 (KV serving, end-task), `[refuted]`. *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task.
- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- A model that reads a sequence of tokens and outputs a probability for the next one. Its perplexity is two to the power of the average bits per token, at least one and equal to the vocabulary size for a uniform guess, and its attention weights are a softmax, positive and summing to one.
- A seven-billion-parameter model served passage retrieval over contexts of fourteen thousand tokens across three registered attempts, and a key quantizer with reconstruction cosine 0.995 broke it to a perplexity near ten thousand.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Perplexity.lean`, theorems `bits_nonneg`, `one_le_perplexity`, `perplexity_uniform`, `perplexity_mono`, `bits_of_finding`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Softmax.lean`, theorems `denom_pos`, `softmax_pos`, `softmax_sum`, `softmax_shift`, `softmax_lt_iff`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 4, 6, 8, 11, 12, 13.

## related

token, perplexity, attention, kv-cache, softmax

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
