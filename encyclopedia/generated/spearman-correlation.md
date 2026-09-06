# Spearman correlation

**id.** spearman-correlation
**kind.** concept

## definition

The ordinary correlation between two lists of ranks. Equation 0.14.

## equation

Book equation 0.14.

    \rho_S=1-\frac{6\sum_i d_i^{2}}{n(n^{2}-1)},\qquad d_i=\text{difference of the two ranks of item } i.

Book equation 11.2.

    \begin{gathered} r=\frac{d_{\mathrm{compressed}}}{d_{\mathrm{exact}}},\qquad \kappa_{\text{strict}}=\frac{\max r}{\min r},\qquad \tau\ \ge\ 1-2\hat\mu(\kappa_{\text{strict}}),\qquad \rho_S\ \ge\ 1-3\hat\mu(\kappa_{\text{strict}}), \\ \kappa_{97.5/2.5}=\frac{q_{97.5}(r)}{q_{2.5}(r)}\ \text{ gives the same two expressions as estimates, not floors.} \end{gathered}

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 9f3829f.
- NEG-8. The Var-ratio tang_qproj is a ≥0.9-Spearman rank proxy for softmax-KL under every consumer. `[refuted]`. `geometric-observation/claims/LEDGER.md:101` at 9f3829f.

## first stated

Spearman, the proof and measurement of association between two things, 1904, as chapter 0 section 0.9 states it, and the rank statistic of the recognizer battery in the-angular-observer and of the rank certificate in readscope.

## measurements

none

## failures and corrections

- NEG-8, `[refuted]`. The Var-ratio tang_qproj is a ≥0.9-Spearman rank proxy for softmax-KL under every consumer.

## conditions

- The ordinary correlation between two lists of ranks, one minus six times the sum of squared rank differences over n(n² − 1). It is at most one, one when the rankings agree, and minus one for three items in opposite orders, and since ranks depend on the ordering alone a strictly increasing transform of either score leaves it unchanged.
- A high Spearman between a proxy and a consumer's loss is not a certificate. The variance-ratio proxy with Spearman above 0.9 is a refuted ledger row, and the rank certificate's floor on Spearman is the strict setting's guarantee, not a measured correlation.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Spearman.lean`, theorems `rho_le_one`, `rho_identical`, `rho_reversed_three`, `rank_comp`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 7, 9, 11.

## related

kendall-correlation, rank-certificate, recognizer, monotone-invariance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
