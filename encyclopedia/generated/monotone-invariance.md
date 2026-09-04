# Monotone Invariance Theorem

**id.** monotone-invariance
**kind.** result

## definition

A strictly monotone transform of a score cannot change its optimal thresholded F1 or its AUROC, because both depend only on the ranking. Equation 6.2.

## equation

Book equation 6.2.

    \begin{gathered} \max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(g(f(X)),\tau\big)\big],\,y\Big)=\max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(f(X),\tau\big)\big],\,y\Big) \\ \text{for every strictly monotone } g. \end{gathered}

## ledger

none

## first stated

theory-radar, `theory-radar/paper/theory_radar_paper.tex:290-304` and `theory-radar/paper/astar_paper.tex:94-110`, DOI 10.5281/zenodo.20660206, and chapter 6 section 6.3 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 5 section 5.4 | Monotone Invariance and AUROC invariance theorems, the AUROC to F1 bound via the Youden index, stated in the source for every ROC curve and corrected in the book to concave curves, with the counterexample at AUROC 0.75 and F1 0.857 | `theory-radar\paper\astar_paper.tex:94-170`; `theory-radar\paper\theory_radar_paper.tex:290-304` |
| chapter 6 section 6.3 | Monotone Invariance Theorem and its proof | `theory-radar\paper\theory_radar_paper.tex:290-304`; `theory-radar\paper\astar_paper.tex:94-110` |

## failures and corrections

none

## conditions

- A strictly monotone transform of a score leaves AUROC, defined pairwise with ties counted one half, and optimal thresholded F1, defined by sweeping the threshold over every score value in both directions, unchanged, because both depend only on the ranking.
- The theorem licenses pruning every monotone unary node of a formula search with zero loss. It says nothing about non-monotone transforms, which can change both quantities.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/MonotoneInvariance.lean`, theorems `aurocNum_comp`, `auroc_comp`, `predicted_comp`, `predictedBelow_comp`, `sweptF1_comp`, `sweptF1Below_comp`, `optF1_comp`, at observation-data-mining 7aab08c.

## used in

*Data Mining as Observation* chapters 0, 5, 6, 12.

## related

formula-search, safe-pruning, youden-f1-bound

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 92c643b, theory-radar 37c4e6c, observation-data-mining 7aab08c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
