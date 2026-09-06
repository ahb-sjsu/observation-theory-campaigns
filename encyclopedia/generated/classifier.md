# classifier

**id.** classifier
**kind.** concept

## definition

A consumer that produces a score per row and turns it into a decision with a threshold. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 1.1.

    O=(C,\ G,\ B).

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 8c6986b.
- GO-B-whale (038). Sperm-whale coda dialect (DSWP/Sharma 2024), Clan classifier — cetacean communication; promotes the exploratory (A2) verdict to a sealed flip `[predicted]`. `geometric-observation/claims/LEDGER.md:120` at 8c6986b.

## first stated

Chapter 6 section 6.1 of *Data Mining as Observation*, with the classifier row of Volume 14's consumer table and the whale clan classifier of ledger row GO-B-whale.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |

## failures and corrections

none

## conditions

- A consumer that produces a score per row and turns it into a decision with a threshold. For a linear classifier the sensitivity is the link's slope times the weight direction, so the read operator is the workload mean of the squared slope times the outer product of the weights, sends every vector to a multiple of the weights, and reads nothing orthogonal to them.
- The score is affine, so chapter 0's exact quotient applies before the link. The whale clan classifier is the flip's classifier case, held-out AUROC 0.934 against 0.883 for a code that reconstructs twice as well.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Classifier.lean`, theorems `readOp_classifier`, `readOp_classifier_mulVec`, `readOp_classifier_orth`, `score_orth`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 14.

## related

consumer, read-operator, threshold, decision-boundary, margin

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
