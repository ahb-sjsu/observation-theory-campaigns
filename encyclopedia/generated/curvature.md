# curvature

**id.** curvature
**kind.** concept

## definition

The second derivative of a consumer, which the finite difference of equation 0.8 does not read and which sets the error of the linear model at a step. Chapter 0 section 0.5 and chapter 7 section 7.2.

## equation

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## ledger

- GO-B-optim-D4 (034 · D4). Optimization — gradient compression, curvature (Hessian) read operator, on a REAL model (logistic regression); optional stretch `[predicted]`. `geometric-observation/claims/LEDGER.md:122` at 9f3829f.

## first stated

Chapter 0 section 0.5 and chapter 7 section 7.2 of *Data Mining as Observation*, with the curvature reader's flip in `geometric-observation/claims/LEDGER.md` row GO-B-optim-D4.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 7 section 7.2 | second-order leaf values, logistic curvature | ESL 2e 10.9 to 10.13; XGBoost introduction to boosted trees |
| chapter 7 section 7.2 | real logistic model, exact Hessian, anti 300 of 300, flip 82 of 300, coupling diagnosis, bound not refutation | `geometric-observation\claims\LEDGER.md` row GO-B-optim-D4 |

## failures and corrections

none

## conditions

- The second derivative of a consumer, which the finite difference of equation 0.8 does not read. For a quadratic the second difference recovers it exactly at every step, the error of the linear model at a step is the curvature times the step squared, and the gradient at the two ends of a step differs by the curvature times the step. An affine consumer has none.
- The reader of a gradient is the optimizer, and its read operator is the loss curvature, which chapter 4's flip was measured against on a real logistic model with its exact Hessian, anti three hundred of three hundred and the flip in 82 of 300.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Curvature.lean`, theorems `second_quad`, `second_affine`, `linear_error`, `gradient_change`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 7.

## related

hessian, finite-difference, sensitivity, boosting, read-operator

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
