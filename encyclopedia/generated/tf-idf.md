# TF-IDF

**id.** tf-idf
**kind.** concept

## definition

A weighting of term counts by how rare the term is across the collection, so that a term in every document carries no weight. Equation 0.36.

## equation

Book equation 0.36.

    w_{t,d}=\mathrm{tf}_{t,d}\cdot\ln\frac{N}{\mathrm{df}_t},\qquad \mathrm{tf}_{t,d}=\frac{\text{count of }t\text{ in }d}{\text{length of }d},\qquad \mathrm{df}_t=\text{documents containing }t.

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

## ledger

- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 7d91883.

## first stated

Spärck Jones, a statistical interpretation of term specificity, 1972, as chapter 0 section 0.17 states it, with the program's frozen LSA baseline in ledger row GO-B-legal.

## measurements

none

## failures and corrections

none

## conditions

- A term's weight is its frequency in the document times the logarithm of the document count over the number containing it. A term in every document carries no weight, the weight is nonnegative and falls as the term spreads, and the frequency lies in the unit interval.
- It is a reader that reads rarity. The legal-citation flip used a frozen TF-IDF to SVD baseline trained on the training split only, and the flip tied while its magnitude overshot, which the ledger carries as partial.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/TFIDF.lean`, theorems `weight_everywhere`, `weight_nonneg`, `weight_antitone`, `tf_mem_unit`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 0, 12.

## related

bag-of-words, retrieval-augmented-pipeline, cross-corpus-gate, quotient

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
