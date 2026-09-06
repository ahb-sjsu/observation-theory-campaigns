# correlation

**id.** correlation
**kind.** concept

## definition

The cosine of two centred columns, between minus one and one, unchanged by shifting or rescaling either. Its distance lives on the quotient that discards shift and scale. Chapter 0 section 0.6.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

## ledger

- NEG-9. The projected-variance trace tr(P_C·Σ_δ) is a complete rank statistic for softmax-KL across all arms. `[refuted]`. `geometric-observation/claims/LEDGER.md:102` at 9f3829f.

## first stated

Pearson, 1895, as chapter 0 section 0.6 and chapter 3 section 3.1 of *Data Mining as Observation* read it, with the radius-against-degree correlation in `the-angular-observer/README.md:135-139`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.3 | radius against degree correlation 0.92 to 0.99 | `the-angular-observer\README.md:135-139` |
| chapter 6 section 6.4 | the uncorrected t stored as sigma, 251 and 15.84, nine wins to three, seven, eight, 3 wins 17 ties 11 losses on 31 datasets, the three-way inconsistency | `constraint-gap\review\FINDINGS.md:1-35`; `constraint-gap\README.md:57-76` |
| chapter 6 section 6.4 | five analyses negative, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md:1-45` |
| chapter 8 section 8.5 | 9/3/19 to 3/17/11, five negative analyses, 0.2 percent of floor, twelve times the band, learning-curve redesign | `constraint-gap\README.md:57-76`; `constraint-gap\review\REDESIGN.md` |

## failures and corrections

- NEG-9, `[refuted]`. The projected-variance trace tr(P_C·Σ_δ) is a complete rank statistic for softmax-KL across all arms.

## conditions

- The cosine of two centred columns. It lies between minus one and one, is one for a column against itself, is symmetric, and is unchanged by shifting or positively rescaling either column, so correlation distance lives on the quotient that discards shift and scale.
- Rank correlations read the order and discard the values, and a read distortion that correlates with a downstream ranking at 0.80 is a control and not a complete rank statistic, NEG-9.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Correlation.lean`, theorems `abs_corr_le_one`, `corr_self`, `cosine_comm`, `corr_comm`, `center_shift`, `center_smul`, `corr_shift`, `corr_smul`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

cosine, spearman-correlation, kendall-correlation, covariance-matrix, quotient

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
