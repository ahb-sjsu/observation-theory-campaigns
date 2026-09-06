# score

**id.** score
**kind.** concept

## definition

The number a classifier produces per row before a threshold turns it into a decision. Chapter 6.

## equation

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

Book equation 6.2.

    \begin{gathered} \max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(g(f(X)),\tau\big)\big],\,y\Big)=\max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(f(X),\tau\big)\big],\,y\Big) \\ \text{for every strictly monotone } g. \end{gathered}

## ledger

none

## first stated

Chapter 6 section 6.1 of *Data Mining as Observation*, with the program's threshold sweeps in theory-radar.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.4 | Monotone Invariance and AUROC invariance theorems, the AUROC to F1 bound via the Youden index, stated in the source for every ROC curve and corrected in the book to concave curves, with the counterexample at AUROC 0.75 and F1 0.857 | `theory-radar\paper\astar_paper.tex:94-170`; `theory-radar\paper\theory_radar_paper.tex:290-304` |
| chapter 6 section 6.3 | Monotone Invariance Theorem and its proof | `theory-radar\paper\theory_radar_paper.tex:290-304`; `theory-radar\paper\astar_paper.tex:94-110` |

## failures and corrections

none

## conditions

- The number a classifier produces per row before a threshold turns it into a decision. Every decision at every threshold is a function of the scores' ordering, so a strictly increasing recalibration of the scores with the matching recalibration of the threshold changes no decision.
- What a recalibration can change is calibration, which is why the reliability weight reads the ordering and the expected calibration error reads the values, and neither stands in for the other.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Threshold.lean`, theorems `predicted_anti`, `tp_anti`, `fp_anti`, `decision_comp`, `predicted_extremes`, at observation-data-mining 8d30d9d.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

classifier, threshold, monotone-invariance, calibration, reliability-weight

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 425c17a, theory-radar 37c4e6c, observation-data-mining 8d30d9d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
