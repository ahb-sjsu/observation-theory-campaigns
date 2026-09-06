# ROC curve

**id.** roc-curve
**kind.** instrument

## definition

The path of true positive rate against false positive rate as the threshold sweeps, whose area is the AUROC. Chapter 5 section 5.4.

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

Chapter 5 section 5.4 of *Data Mining as Observation*, with the Youden ceiling and its correction to concave curves in `theory-radar/paper/astar_paper.tex:94-110`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.4 | seven thresholds up to 0.75, eight datasets, 56 conditions, zero admissibility violations, reductions 70 to 99.1 percent | `theory-radar\paper\astar_paper.tex:170-200` |
| chapter 6 section 6.3 | Monotone Invariance Theorem and its proof | `theory-radar\paper\theory_radar_paper.tex:290-304`; `theory-radar\paper\astar_paper.tex:94-110` |

## failures and corrections

none

## conditions

- The path of true positive rate against false positive rate as the threshold sweeps. Its area is the AUROC, which lies in the unit interval, is one half for a constant score, is one for a perfect ranking, and is unchanged by any strictly increasing transform of the score.
- The bound from AUROC to the best F1 through the Youden index holds for concave curves and not for every curve, with the counterexample at AUROC 0.75, and the book corrects the source on that point.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Auroc.lean`, theorems `pair_nonneg`, `auroc_nonneg`, `auroc_le_one`, `auroc_perfect`, `auroc_reversed`, `auroc_chance`, `auroc_monotone_invariant`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/YoudenF1.lean`, theorems `f1_eq`, `f1_le_of_youden`, `auroc_eq`, `youden_eq`, `youden_exceeds_auroc_form`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 5, 6, 7, 8, 11, 12, 13, 14.

## related

auroc, youden-index, threshold, precision-recall, f1

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
