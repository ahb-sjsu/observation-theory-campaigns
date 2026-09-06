# decision boundary

**id.** decision-boundary
**kind.** concept

## definition

The set of inputs whose score equals the threshold. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 6.2.

    \begin{gathered} \max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(g(f(X)),\tau\big)\big],\,y\Big)=\max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(f(X),\tau\big)\big],\,y\Big) \\ \text{for every strictly monotone } g. \end{gathered}

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 8c6986b.

## first stated

Chapter 6 section 6.1 of *Data Mining as Observation*, where the classifier's read direction and its threshold meet.

## measurements

none

## failures and corrections

none

## conditions

- The set of inputs whose score equals the threshold. For a linear classifier it is an affine hyperplane. Moving orthogonally to the weights never crosses it, moving along the weights crosses it exactly once, and every boundary point has the same projection on the weights.
- The boundary is where the read direction and the threshold meet and nothing else about the input enters it, which is the classifier's nuisance drawn as a picture.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DecisionBoundary.lean`, theorems `orth_stays`, `cross_once`, `same_projection`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0.

## related

classifier, threshold, margin, nuisance

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
