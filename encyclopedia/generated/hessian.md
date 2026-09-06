# Hessian

**id.** hessian
**kind.** concept

## definition

The matrix of second derivatives of a score, whose off-diagonal entries are the interactions. Naive Bayes has a diagonal one. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

## ledger

- GO-B-optim-D4 (034 · D4). Optimization — gradient compression, curvature (Hessian) read operator, on a REAL model (logistic regression); optional stretch `[predicted]`. `geometric-observation/claims/LEDGER.md:122` at 9f3829f.

## first stated

Chapter 6 section 6.1 and chapter 7 section 7.2 of *Data Mining as Observation*, with the exact Hessian of a real logistic model in `geometric-observation/claims/LEDGER.md` row GO-B-optim-D4.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 7 section 7.2 | second-order leaf values, logistic curvature | ESL 2e 10.9 to 10.13; XGBoost introduction to boosted trees |
| chapter 7 section 7.2 | real logistic model, exact Hessian, anti 300 of 300, flip 82 of 300, coupling diagnosis, bound not refutation | `geometric-observation\claims\LEDGER.md` row GO-B-optim-D4 |

## failures and corrections

none

## conditions

- The matrix of second derivatives of a score, whose off-diagonal entries are the interactions. The second difference recovers a quadratic's curvature exactly, and a score that is additive across features, naive Bayes, has a diagonal Hessian because one feature's contribution is the same whatever the others are.
- The read operator is not the Hessian. Two features' sensitivities can rise and fall together across rows even when neither changes the other's effect, so a diagonal Hessian does not give a diagonal read operator.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Curvature.lean`, theorems `second_quad`, `second_affine`, `linear_error`, `gradient_change`, at observation-data-mining f05f3e7.

`lean/DataMiningAsObservation/NaiveBayes.lean`, theorems `log_likelihood_sum`, `log_odds_sum`, `contribution_independent`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 6, 7, 14.

## related

curvature, naive-bayes, boosting, read-operator, jacobian

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
