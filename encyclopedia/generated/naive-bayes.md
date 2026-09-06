# naive Bayes

**id.** naive-bayes
**kind.** instrument

## definition

A classifier that multiplies one-dimensional likelihoods and adds their logs, so that each feature's contribution is the same whatever the others are and it cannot read an interaction. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

## ledger

none

## first stated

Chapter 6 section 6.1 of *Data Mining as Observation*, after TSK chapter 4.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.1 | the classifier row of the consumer table, the output metric makes a different observer | `geometric-observation\chapters\ch04_the_observer_triple.md:60-135` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |

## failures and corrections

none

## conditions

- A classifier that multiplies one-dimensional likelihoods and adds their logs. The log of the product is the sum of the logs, the log odds add across features, and one feature's contribution is the same whatever the others are, so the score has no interaction terms and its Hessian is diagonal.
- What naive Bayes cannot read is the interaction, which is a limit of the model class rather than a direction in its kernel, and its read operator is still not diagonal in general because two sensitivities can rise and fall together across rows.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NaiveBayes.lean`, theorems `log_likelihood_sum`, `log_odds_sum`, `contribution_independent`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 6.

## related

classifier, hessian, confidence, logistic-regression

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
