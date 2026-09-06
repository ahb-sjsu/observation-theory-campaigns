# attention

**id.** attention
**kind.** concept

## definition

The operation inside a language model that lets each token look at earlier ones by comparing its query to their keys and averaging their values. Chapter 0 section 0.11.

## equation

Book equation 0.23.

    \operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_j e^{z_j}},\qquad \text{output}=\sum_i\operatorname{softmax}\!\Big(\frac{q\cdot k_i}{\sqrt{d}}\Big)_{\!i}\,v_i.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

- GO-2/GO-12/GO-13 operational (KV serving, 077). Consumer-relative access width measured on a production serving stack (Qwen2.5-7B KV-cache eviction, matched budget): task quality tracks measured predictive uncertainty u about the consumer's future reads, not nominal scorer width — the 32-query snapshot beats the 1024-query scorer +0.4375±0.070 at 5% keep (bar 0.30) and survives 97% eviction with zero drop, while wide-window scoring is statistically indistinguishable from random eviction at extreme budgets; the recency-hoarding starvation signature replicated across three disjoint prompt sets (oracle-miss gap 0.370 vs bar 0.25). The novel equal-uncertainty analytic-equality control (degradation-titrated, constructible by design) REFUTED its own equality prediction on the pre-registered branch: with calibration health 4×–130× inside gates, equal scalar u did NOT give equal quality (V4 +0.078 vs 0.0625 tolerance; the pre-registered ρ=0.03 contrast firmed to +0.359±0.068, 5.3 SE) — equal scalar uncertainty is insufficient, error structure matters, consistent with GO-13 Theorem 1's own r≥2 scoping of equal-q universality (a scalar-context privilege). Successor arc: 056 honest miss → 075 ID burned on a disclosed design failure → 077 sealed and split-verdict. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:81` at 9f3829f.
- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 9f3829f.

## first stated

Chapter 0 section 0.11 and chapter 11 section 11.1 of *Data Mining as Observation*, with the program's head-level measurements in `turboquant-pro/docs/KV_KEYS_FINDING.md:1-49` and the serving-stack ledger row.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 11 section 11.2 | the calibration-time probe and the streaming monitor | `turboquant-pro\turboquant_pro\a2_probe.py:315-438`; `turboquant-pro\tests\test_a2_probe.py` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- A head weights each earlier token's value by the softmax of its query-key score and sums. For scalar values the output lies between the smallest and largest value, and the head reads the keys only through their scores against the query, so a key change the query does not read leaves the output unchanged however large it is.
- That is the head's read subspace, a few query-weighted directions of each key, and the reason a key reconstruction at cosine 0.995 raised the perplexity by three orders of magnitude.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Attention.lean`, theorems `output_le_max`, `min_le_output`, `output_congr`, `output_nuisance`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 8, 11, 13.

## related

softmax, read-subspace, nuisance, flip

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
