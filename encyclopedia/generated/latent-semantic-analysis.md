# latent semantic analysis

**id.** latent-semantic-analysis
**kind.** instrument

## definition

The singular value decomposition of the TF-IDF matrix with the top components kept, which is principal components on documents. Chapter 12.

## equation

Book equation 0.36.

    w_{t,d}=\mathrm{tf}_{t,d}\cdot\ln\frac{N}{\mathrm{df}_t},\qquad \mathrm{tf}_{t,d}=\frac{\text{count of }t\text{ in }d}{\text{length of }d},\qquad \mathrm{df}_t=\text{documents containing }t.

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

## ledger

- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Deerwester, Dumais, Furnas, Landauer, and Harshman, indexing by latent semantic analysis, 1990, as chapter 12 section 12.1 of *Data Mining as Observation* reads it, with the program's frozen embedding in `geometric-observation/chapters/ch10_the_blind_probe.md:100-118`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.3 | 041 non-oracle, frozen LSA TF-IDF to SVD 100 train-only, AUROC 0.975 vs 0.910, flip tied, magnitude overshot, partial | `geometric-observation\chapters\ch10_the_blind_probe.md:100-118`; `geometric-observation\claims\LEDGER.md` row GO-B-blind 041 |

## failures and corrections

none

## conditions

- The singular value decomposition of the TF-IDF matrix with the top components kept, which is principal components on documents. The fraction of variance kept grows with the components kept and reaches one at full rank, and the components dropped cost the sum of their eigenvalues.
- It is the identity reader on term-document variance, and the components it keeps are the directions of largest variance whether or not the consumer reads them. The non-oracle test fit a frozen embedding of 100 components on the training split only and recovered the reader blind.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PCA.lean`, theorems `varAlong_basis`, `varAlong_le`, `varAlong_ge`, `dropped_eq`, `dropped_nonneg`, at observation-data-mining f05f3e7.

`lean/DataMiningAsObservation/ExplainedVariance.lean`, theorems `explained_mem_unit`, `explained_mono`, `explained_full`, `retained_identity`, `retained_example`, at observation-data-mining f05f3e7.

`lean/DataMiningAsObservation/TFIDF.lean`, theorems `weight_everywhere`, `weight_nonneg`, `weight_antitone`, `tf_mem_unit`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 12.

## related

tf-idf, principal-component-analysis, explained-variance, bag-of-words, blind-probe

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
