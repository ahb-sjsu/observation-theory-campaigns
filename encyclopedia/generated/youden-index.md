# Youden index

**id.** youden-index
**kind.** instrument

## definition

True positive rate minus false positive rate at a threshold, whose maximum over thresholds is the pointwise ceiling that prunes the formula search. Chapter 5 section 5.4.

## equation

Book equation 5.4.

    \begin{gathered} F_1^{\max}\ \le\ \sup_{t\in[J,\,1]}\ \frac{2t\pi}{t\pi+\pi+(t-J)(1-\pi)},\qquad J=\max_{\tau}\big(\mathrm{TPR}-\mathrm{FPR}\big),\qquad \pi=\text{prevalence}, \\ J\le 2A-1\ \text{when the ROC curve is concave, and not in general.} \end{gathered}

Book equation 0.28.

    P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2PR}{P+R}.

Book equation 0.38.

    w=\max\big(0,\ 2\cdot\mathrm{AUROC}-1\big).

## ledger

none

## first stated

Youden, index for rating diagnostic tests, 1950, as chapter 5 section 5.4 of *Data Mining as Observation* reads it, with the pointwise ceiling in `theory-radar/paper/astar_paper.tex:94-110`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.4 | seven thresholds up to 0.75, eight datasets, 56 conditions, zero admissibility violations, reductions 70 to 99.1 percent | `theory-radar\paper\astar_paper.tex:170-200` |
| chapter 5 section 5.4 | learned pruning 88 to 99.6 percent with zero false negatives | `theory-radar\README.md:88-100` |
| chapter 6 section 6.3 | Monotone Invariance Theorem and its proof | `theory-radar\paper\theory_radar_paper.tex:290-304`; `theory-radar\paper\astar_paper.tex:94-110` |
| chapter 6 section 6.3 | 88 to 99.6 percent pruned with zero false negatives, fair protocol, 200 by 5 folds | `theory-radar\README.md:88-100` |

## failures and corrections

none

## conditions

- True positive rate minus false positive rate at a threshold, whose maximum over thresholds bounds the best F1 the score can reach at any threshold. The bound is exact for concave ROC curves and fails for a curve at AUROC 0.75.
- The pointwise ceiling on a node of the formula search is proved, and using it to prune the node's descendants is a heuristic that missed the optimum on two of five datasets in the rerun.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/YoudenF1.lean`, theorems `f1_eq`, `f1_le_of_youden`, `auroc_eq`, `youden_eq`, `youden_exceeds_auroc_form`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 5.

## related

roc-curve, auroc, f1, safe-pruning, formula-classifier

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
