# output metric

**id.** output-metric
**kind.** concept

## definition

The rule by which a consumer's mistakes are scored, the second element of an observer. Chapter 1.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 9f3829f.
- GO-2 (pos. half: consumer-projected covariance *controls*). Downstream preservation is controlled by the error covariance projected on the consumer's read subspace, tr(P_C·Σ_δ). `[replicated]`. `geometric-observation/claims/LEDGER.md:64` at 9f3829f.

## first stated

Chapter 1 section 1.2 of *Data Mining as Observation*, with the flip's verdict inversion in `geometric-observation/chapters/ch08_value.md:1-30`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.2 | traces 2.0, diagonals 0.3 and 1.7, consumers at 15 and 75 degrees, distortion 0.39 vs 1.61, 4.1 to one, computed not drawn | `observation-theory\assets\make_flip_figure.py:4-24,107-119` |
| chapter 4 section 4.3 | the flip definition, flip versus (A2) verdict | `geometric-observation\chapters\ch08_value.md:1-30,100-108` |
| chapter 4 section 4.3 | GO-2 0.0934 vs 0.0938, 2.53 times, 12 of 12, anti 21 times; retrieval 0.0964, negative 4.70 and positive 4.65, recon 0.40 | `geometric-observation\claims\LEDGER.md` rows GO-2 negative and positive halves |

## failures and corrections

none

## conditions

- The rule by which a consumer's mistakes are scored, the second element of an observer. A consumer and its negation have the same read operator and reverse every comparison, so the read operator alone does not fix the observer, and two cost matrices score the same pair of classifiers in opposite orders, so naming the output metric is naming what a downstream mistake is.
- A dataset-level loss, accuracy, F1, a rank correlation, or dollars lost is not a local geometry on the score and cannot be inserted into the read-operator formula. Each interestingness measure of chapter 5 and each fairness metric of chapter 14 is an output metric, right for some consumer and wrong for others.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/OutputMetric.lean`, theorems `neg_reverses`, `readOp_of_neg`, `cost_flips`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 5, 6, 8, 9, 11, 14.

## related

observer, consumer, read-operator, budget, flip-the

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
