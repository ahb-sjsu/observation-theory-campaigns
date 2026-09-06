# margin

**id.** margin
**kind.** concept

## definition

How far a row's score sits from the threshold. Chapter 6.

## equation

Book equation 9.3.

    \hat\mu=\frac{\bar s_{\mathrm{true}}-\bar s_{\mathrm{distr}}}{\sigma_{\mathrm{distr}}},\qquad \mu_{\mathrm{crit}}=\mathbb E\Big[\max_{N-1}\mathcal N(0,1)\Big],\qquad \rho=\frac{\hat\mu}{\mu_{\mathrm{crit}}},\qquad \rho=1\ \text{vacuous}.

Book equation 11.2.

    \begin{gathered} r=\frac{d_{\mathrm{compressed}}}{d_{\mathrm{exact}}},\qquad \kappa_{\text{strict}}=\frac{\max r}{\min r},\qquad \tau\ \ge\ 1-2\hat\mu(\kappa_{\text{strict}}),\qquad \rho_S\ \ge\ 1-3\hat\mu(\kappa_{\text{strict}}), \\ \kappa_{97.5/2.5}=\frac{q_{97.5}(r)}{q_{2.5}(r)}\ \text{ gives the same two expressions as estimates, not floors.} \end{gathered}

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 7d91883.

## first stated

Chapter 6 section 6.1 of *Data Mining as Observation*, with the margin certificate of chapter 9 section 9.3 and the neighbour margins of chapter 11.

## measurements

none

## failures and corrections

none

## conditions

- How far a row's score sits from the threshold. A perturbation whose length times the weight length is smaller than the margin cannot move a linear classifier's score across the threshold, by Cauchy–Schwarz, and a step along the weights of exactly that size reaches the boundary.
- The margin is therefore a certificate on a decision, and chapter 9's margin certificate is the same idea with a noise model in place of a perturbation bound and a vacuity threshold derived from it.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Margin.lean`, theorems `score_add`, `decision_stable`, `tight_along_weights`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 0, 6, 7, 9, 11, 12, 14.

## related

classifier, decision-boundary, vacuity-threshold, rank-certificate, escalation

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
