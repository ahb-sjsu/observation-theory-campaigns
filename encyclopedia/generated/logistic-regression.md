# logistic regression

**id.** logistic-regression
**kind.** instrument

## definition

A linear classifier whose score is the sigmoid of a weighted sum, strictly between zero and one, above one half exactly on one side of the hyperplane. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.28.

    P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2PR}{P+R}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 9f3829f.
- GO-B-optim-D4 (034 · D4). Optimization — gradient compression, curvature (Hessian) read operator, on a REAL model (logistic regression); optional stretch `[predicted]`. `geometric-observation/claims/LEDGER.md:122` at 9f3829f.

## first stated

Cox, the regression analysis of binary sequences, 1958, as chapter 6 section 6.1 of *Data Mining as Observation* reads it, with the real logistic model's Hessian in `geometric-observation/claims/LEDGER.md` row GO-B-optim-D4.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.1 | the classifier row of the consumer table, the output metric makes a different observer | `geometric-observation\chapters\ch04_the_observer_triple.md:60-135` |
| chapter 7 section 7.2 | real logistic model, exact Hessian, anti 300 of 300, flip 82 of 300, coupling diagnosis, bound not refutation | `geometric-observation\claims\LEDGER.md` row GO-B-optim-D4 |

## failures and corrections

none

## conditions

- A linear classifier whose score is the sigmoid of a weighted sum. The sigmoid lies strictly between zero and one, is one half at zero, is symmetric about one half, and is strictly increasing, so the decision at threshold one half is the sign of the weighted sum and the decision boundary is the hyperplane.
- Its score moves only along its weight vector, so its read subspace is one direction and its nuisance is everything orthogonal, and its read operator is the outer product of the weight vector with itself scaled by how steep the sigmoid is at each row.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Logistic.lean`, theorems `sigmoid_pos`, `sigmoid_lt_one`, `sigmoid_zero`, `sigmoid_neg`, `sigmoid_strictMono`, `decision_iff`, `decision_linear`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 6, 7, 11, 12.

## related

classifier, decision-boundary, threshold, read-subspace, hessian

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
