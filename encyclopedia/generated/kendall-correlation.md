# Kendall correlation

**id.** kendall-correlation
**kind.** concept

## definition

The fraction of item pairs two rankings order the same way, minus the fraction they order differently. Equation 0.15.

## equation

Book equation 0.15.

    \tau=\frac{\#\{\text{concordant pairs}\}-\#\{\text{discordant pairs}\}}{n(n-1)/2}.

Book equation 11.2.

    \begin{gathered} r=\frac{d_{\mathrm{compressed}}}{d_{\mathrm{exact}}},\qquad \kappa_{\text{strict}}=\frac{\max r}{\min r},\qquad \tau\ \ge\ 1-2\hat\mu(\kappa_{\text{strict}}),\qquad \rho_S\ \ge\ 1-3\hat\mu(\kappa_{\text{strict}}), \\ \kappa_{97.5/2.5}=\frac{q_{97.5}(r)}{q_{2.5}(r)}\ \text{ gives the same two expressions as estimates, not floors.} \end{gathered}

## ledger

- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 8c6986b.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 8c6986b.

## first stated

Kendall, a new measure of rank correlation, 1938, as chapter 0 section 0.9 states it, and the rank certificate's statistic in readscope and openvector-bench.

## measurements

none

## failures and corrections

none

## conditions

- The fraction of item pairs two rankings order the same way minus the fraction they order differently. It lies between minus one and one, it is one when no pair disagrees, and since it depends only on the orderings a strictly increasing transform of either score leaves it unchanged.
- It is the rank-agreement statistic the rank certificate bounds from below, and a floor on it is a floor on the consumer's rankings, not on any distance.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Kendall.lean`, theorems `not_both`, `card_add_le`, `tau_mem`, `concordant_comp`, `discordant_comp`, `tau_comp`, `discordant_self`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 8, 11.

## related

rank-certificate, rank-faithful, monotone-invariance, recall-at-k

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
