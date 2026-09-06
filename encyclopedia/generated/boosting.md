# boosting

**id.** boosting
**kind.** instrument

## definition

Fitting a sequence of weak scorers, each on the rows the previous ones got wrong, and summing them. Its step size is positive exactly when the weak scorer beats chance, and the reweighting makes the last scorer's weighted error one half. Chapter 7.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

## ledger

- GO-B-optim-D4 (034 · D4). Optimization — gradient compression, curvature (Hessian) read operator, on a REAL model (logistic regression); optional stretch `[predicted]`. `geometric-observation/claims/LEDGER.md:122` at 9f3829f.

## first stated

Freund and Schapire, a decision-theoretic generalization of on-line learning, 1997, as chapter 7 section 7.1 of *Data Mining as Observation* reads it, with the curvature reader in `geometric-observation/claims/LEDGER.md` row GO-B-optim-D4.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.3 | the five-dataset table, breast cancer 0.955 to 0.963, the pattern, DOI 10.5281/zenodo.20660206 | `theory-radar\README.md:100-140` |
| chapter 7 section 7.1 | bagging variance, out-of-bag estimation, random forests, importances, AdaBoost | Hastie, Tibshirani, Friedman, ESL 2e chapters 15 and 10.1; TSK 2e 4.10 |
| chapter 7 section 7.2 | second-order leaf values, logistic curvature | ESL 2e 10.9 to 10.13; XGBoost introduction to boosted trees |
| chapter 7 section 7.2 | real logistic model, exact Hessian, anti 300 of 300, flip 82 of 300, coupling diagnosis, bound not refutation | `geometric-observation\claims\LEDGER.md` row GO-B-optim-D4 |
| chapter 7 section 7.3 | the five-dataset outcomes | `theory-radar\README.md:100-140` |

## failures and corrections

none

## conditions

- Fitting a sequence of weak scorers, each on the rows the previous ones got wrong, and summing them with a step size set by the weighted error. The step size is positive exactly when the weak scorer beats chance, and after the rows are reweighted the weighted error of the scorer just fitted is one half, so the next scorer must find something new.
- Gradient boosting reads the loss through its curvature, so the optimizer is a consumer whose read operator is the Hessian, and on the author's five-dataset benchmark the ensemble wins when the boundary needs many features and a formula wins when it needs few.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Boosting.lean`, theorems `alpha_pos_iff`, `alpha_half`, `reweighted_error_half`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 1, 6, 7, 8.

## related

ensemble, curvature, decision-tree, formula-classifier, importance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
