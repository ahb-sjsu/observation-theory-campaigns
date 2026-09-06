# chunk

**id.** chunk
**kind.** concept

## definition

A piece of a document, the unit a retrieval pipeline encodes and indexes. Chunking is a discrete stage with no Jacobian. Chapter 12.

## equation

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

Book equation 0.36.

    w_{t,d}=\mathrm{tf}_{t,d}\cdot\ln\frac{N}{\mathrm{df}_t},\qquad \mathrm{tf}_{t,d}=\frac{\text{count of }t\text{ in }d}{\text{length of }d},\qquad \mathrm{df}_t=\text{documents containing }t.

## ledger

- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 12 section 12.2 of *Data Mining as Observation*, with the pullback composition in `geometric-observation/chapters/ch06_mathematical_preliminaries.md:10-27`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 11 section 11.4 | R80 table, 25x probe depth, 92 percent own cell, one third cross-article, 0.53 matches same-article share, relative contrast discriminates nothing | `openvector-bench\results\R80_ANN.md:1-40`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 12 section 12.2 | pullback composition and the rank bound | `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27`; chapter 2 of this book |

## failures and corrections

none

## conditions

- A piece of a document, the unit a retrieval pipeline encodes and indexes. Chunking is a discrete stage with no Jacobian, and a stage that identifies two inputs identifies them for every stage after it, so what a chunker merges no later stage can separate.
- A chunk's vector is read by the index against a query vector, and the probe depth, cell, and cross-article share of the candidates are properties of the chunks and the query set together.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Pipeline.lean`, theorems `quotient_inherited`, `quotient_inherited_chain`, `rank_comp_le_first`, `rank_comp_le_second`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 12.

## related

retrieval-augmented-pipeline, jacobian, pipeline, encoder, inverted-file

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
