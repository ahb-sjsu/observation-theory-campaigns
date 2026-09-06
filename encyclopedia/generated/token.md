# token

**id.** token
**kind.** concept

## definition

A piece of text, roughly a word, the unit a language model reads and writes. Chapter 0 section 0.11.

## equation

Book equation 0.22.

    \mathrm{PPL}=2^{H},\qquad H=-\frac1T\sum_{t=1}^{T}\log_2 p\big(w_t\mid w_{<t}\big).

Book equation 0.23.

    \operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_j e^{z_j}},\qquad \text{output}=\sum_i\operatorname{softmax}\!\Big(\frac{q\cdot k_i}{\sqrt{d}}\Big)_{\!i}\,v_i.

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

## ledger

none

## first stated

Chapter 0 section 0.11 of *Data Mining as Observation*, with the program's serving measurements in `geometric-observation/experiments/GO-kv-serving-flip-NOTES.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.6 | attempt one, six gates, 4 pass, K3 0.075 vs 0.15, K4 0.050 vs 0.10, arms 0.925, 0.925, 0.900, 0.850, recon ratio 1.000000, n 40, mechanism 15 to 36 times | `geometric-observation\experiments\GO-kv-serving-flip-NOTES.md:1-40`; `geometric-observation\prereg\GO-P-2026-056-kv-serving-flip.md:1-40`; `geometric-observation\results\GO-KV-serving-flip-7B.json` |
| chapter 13 section 13.6 | attempt two, broken proxy, control did not exist, identifier burned, 16 prompts, 1360 s | `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md:1-15`; `geometric-observation\results\GO13-kvaw-pilot-disclosed.json` |
| chapter 13 section 13.6 | attempt three, windows 1024, 256, 32, uncertainty 0.982 to 0.892, 5 of 6, 0.4375 with SE 0.070 at 5 percent keep vs 0.30, 97 percent eviction, oracle-miss 0.370 vs 0.25, V4 0.078 vs 0.0625, contrast 0.359 with SE 0.068, n 64, seed 20260812, 89 duty cycles | `geometric-observation\claims\LEDGER.md` row GO-2/GO-12/GO-13 operational; `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md`; `geometric-observation\results\GO13-kvaw2-governed.json` |

## failures and corrections

none

## conditions

- A piece of text, roughly a word, the unit a language model reads and writes. A model reads a sequence of tokens and outputs a probability for the next one, and perplexity is two to the power of the average bits per token, so it is at least one and equals the vocabulary size for a uniform guess.
- The key-value cache stores one key and one value per token per head, and a generation of 512 tokens under a wrong codebook was where the retracted degradation curve was measured. Token counts are the budget in every serving row of chapter 13.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Perplexity.lean`, theorems `bits_nonneg`, `one_le_perplexity`, `perplexity_uniform`, `perplexity_mono`, `bits_of_finding`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 4, 8, 11, 12, 13.

## related

perplexity, attention, kv-cache, rotary-position-embedding, teacher-forcing

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
