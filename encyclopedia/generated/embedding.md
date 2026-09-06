# embedding

**id.** embedding
**kind.** concept

## definition

A vector assigned to an object, a word, a sentence, a node, a document, so that nearness in the vector space stands for a relation between the objects. Chapter 11.

## equation

Book equation 11.1.

    \cos\big(k,\hat k\big)=0.995\qquad\text{while}\qquad \mathrm{PPL}:\ 12.24\ \to\ 10643.

Book equation 11.2.

    \begin{gathered} r=\frac{d_{\mathrm{compressed}}}{d_{\mathrm{exact}}},\qquad \kappa_{\text{strict}}=\frac{\max r}{\min r},\qquad \tau\ \ge\ 1-2\hat\mu(\kappa_{\text{strict}}),\qquad \rho_S\ \ge\ 1-3\hat\mu(\kappa_{\text{strict}}), \\ \kappa_{97.5/2.5}=\frac{q_{97.5}(r)}{q_{2.5}(r)}\ \text{ gives the same two expressions as estimates, not floors.} \end{gathered}

## ledger

- NEG-2. Reconstruction cosine as a proxy for key quality. `[refuted]`. `geometric-observation/claims/LEDGER.md:95` at 7d91883.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 7d91883.

## first stated

Chapter 11 section 11.1 of *Data Mining as Observation*, with the program's embeddings in the legal-citation flip, the GloVe corpus of readscope, and the attention keys of the KV finding.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | cosine 0.995 and perplexity of order ten thousand, the recalibration negative | `geometric-observation\chapters\ch02_failure_of_observer_free_measurement.md:40-60`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 and NEG-4; `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 2 section 2.5 | cosine 0.995 and the softmax reader | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 4 section 4.5 | GloVe table, 73 percent at 64 components, 0.685 vs 0.862 and 0.866, 0.906 at matched bytes, 0.989 at 37 bytes, 768 to 256 keeps about 99 percent, the 95 percent rule | `turboquant-pro\benchmarks\RESULTS_glove.md:1-40` |
| chapter 8 section 8.2 | cosine 0.995, perplexity near 1e4 | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-2 |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 11 section 11.2 | fp16 12.24, values-only 13.12, PolarQuant K4 10643 and 0.095, per-channel uniform K4 14.91 and 0.062, per-channel NUQ K3 15.77 and 0.148, 2.4x and 670x, pre-rotary near 22000, 2 key heads serve 12 query heads | `turboquant-pro\docs\KV_KEYS_FINDING.md:1-49` |

## failures and corrections

- NEG-2, `[refuted]`. Reconstruction cosine as a proxy for key quality.

## conditions

- A vector assigned to an object so that nearness in the vector space stands for a relation between the objects. Objects with the same embedding are indistinguishable to every consumer of the embedding, so the embedding is a quotient, and a cosine reader takes a further quotient in which the nearest neighbour is unchanged when the query is rescaled, where a dot-product reader does not.
- What an embedding is worth to a consumer is the consumer's number. The keys that reconstructed at cosine 0.995 and raised the perplexity by three orders of magnitude are the case, and the rank certificate is the instrument that says which neighbour rankings a compressed embedding preserved.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Embedding.lean`, theorems `quotient`, `cosine_scale_free`, `nearest_scale_free`, `dot_not_scale_free`, at observation-data-mining 8d458b2.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 4, 8, 9, 10, 11, 12, 13, 14.

## related

encoder, dot-product, rank-certificate, hubness, flip

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 429cc9d, theory-radar 37c4e6c, observation-data-mining 8d458b2, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
