# residualization

**id.** residualization
**kind.** instrument

## definition

Removing from a column the least-squares multiple of another. The residual is orthogonal to the column removed. Chapter 8 section 8.6 and chapter 12 section 12.5.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 12.3.

    \text{validated}\iff \mathrm{AUROC}_{\text{cross}}-\max\big(\mathrm{AUROC}_{\text{untrained}},\ \mathrm{AUROC}_{\text{BoW}}\big)\ \ge\ 0.10.

Book equation 14.2.

    \mathrm{coverage\ difference}_c=\mathrm{AUROC}_c(\text{embedding})-\mathrm{AUROC}_c(\text{validated axes}),\qquad \text{floor}\approx0.08\ \text{to}\ 0.12.

## ledger

- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 8 section 8.6 and chapter 12 section 12.5 of *Data Mining as Observation*, with the bifactor readout in `xbse/docs/BIFACTOR_READOUT.md:14-100`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.6 | books 0.241 at 17 sigma, residual 0.093, R2 0.009, z 6.5, p 5.7e-11, 85 percent, fiction 0.131 on 2250 | `geometric-aesthetics\book\src\chapter-17-empirical-evidence-for-geometric-aesthetics.md:95-106` |
| chapter 12 section 12.5 | valence channel 0.856 plus or minus 0.008 on 51319 rows, P1 failed 4 of 11, the G-share table, 12 by 12 gate five own-axis six demoted, bimodal G row, 0.875 vs 0.811, display rule | `xbse\docs\BIFACTOR_READOUT.md:14-100` |
| chapter 14 section 14.8 | 0.241 to 0.093, 4998 books, 6.5 standard errors, one to two percent | `geometric-aesthetics\book\src\chapter-17-empirical-evidence-for-geometric-aesthetics.md:95-106` |

## failures and corrections

none

## conditions

- Removing from a column the least-squares multiple of another. The residual is orthogonal to the column removed, its squared length is the original less the squared dot product over the removed column's squared length, a column orthogonal to the removed one is unchanged, and a column residualized on itself vanishes.
- Whether named categories survive residualization on the general valence channel is chapter 12's test, and the book-length signal fell from 0.241 to a residual 0.093 at six and a half standard errors.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Residual.lean`, theorems `residual_orth`, `residual_sq`, `residual_of_orth`, `residual_self`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 8, 12, 14.

## related

correlation, orthogonal, confound, contraction, projection

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
