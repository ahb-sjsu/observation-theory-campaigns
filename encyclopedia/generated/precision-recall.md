# precision, recall

**id.** precision-recall
**kind.** concept

## definition

The fraction of predicted positives that are truly positive, and the fraction of true positives that were predicted. Equation 0.28.

## equation

Book equation 0.28.

    P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F_1=\frac{2PR}{P+R}.

Book equation 6.2.

    \begin{gathered} \max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(g(f(X)),\tau\big)\big],\,y\Big)=\max_{\tau,\ \mathrm{dir}}F_1\!\Big(\mathbf 1\big[\mathrm{dir}\big(f(X),\tau\big)\big],\,y\Big) \\ \text{for every strictly monotone } g. \end{gathered}

## ledger

none

## first stated

Chapter 0 section 0.14 of *Data Mining as Observation*, with the program's precision targets in `gtc-prototype/docs/SPECTRUM_FINDINGS.md:84-88`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 14 section 14.7 | 51 percent moderated at 80 and 95 percent precision on the balanced set | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:84-88` |

## failures and corrections

none

## conditions

- The fraction of predicted positives that are truly positive, and the fraction of true positives that were predicted, both in the unit interval. F1 is their harmonic mean, between the smaller of the two and their arithmetic mean, equal to both when they agree, and zero when either is zero.
- In counts F1 is twice the true positives over twice the true positives plus the false positives and false negatives, the form the Youden ceiling bounds.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PrecisionRecall.lean`, theorems `precision_mem_unit`, `recall_mem_unit`, `f1_le_mean`, `min_le_f1`, `f1_self`, `f1_zero`, `f1_counts`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 1, 4, 6, 8, 9, 10, 11, 12, 14.

## related

f1, threshold, recall-at-k, youden-f1-bound

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
