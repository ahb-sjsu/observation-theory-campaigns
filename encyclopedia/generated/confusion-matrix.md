# confusion matrix

**id.** confusion-matrix
**kind.** concept

## definition

The four counts a two-class classifier with a threshold produces on a test set, true and false positives and negatives, from which precision, recall, the false positive rate, and accuracy are read as conditional probabilities. Primer S, equation S.17.

**Example.** 30 true positives, 10 false positives, 20 false negatives, and 940 true negatives give precision 0.75, recall 0.6, and accuracy 0.97.

## equation

Book equation S.17.

    P=\Pr[\text{positive}\mid\text{predicted positive}]=\frac{TP}{TP+FP},\qquad R=\Pr[\text{predicted positive}\mid\text{positive}]=\frac{TP}{TP+FN}.

## conditions

none

## ledger

none

## first stated

Primer S section S.9 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer S, chapters 0, 5, 6, 8.

## related

precision-recall, accuracy, false-positive-rate, threshold

## see also

none

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
