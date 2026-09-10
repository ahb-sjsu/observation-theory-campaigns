# base rate

**id.** base-rate
**kind.** concept

## definition

How common a cause or class is before any observation, the prior that Bayes' rule multiplies by. A classifier's precision falls with it, and accuracy is fooled by it. Primer S, equations S.3 and S.17.

**Example.** With five percent positives, the classifier that calls every row negative has accuracy 0.95.

## equation

Book equation S.3.

    \Pr[A\mid B]=\frac{\Pr[B\mid A]\,\Pr[A]}{\Pr[B]},\qquad \Pr[B]=\Pr[B\mid A]\Pr[A]+\Pr[B\mid A^{c}]\Pr[A^{c}].

Book equation S.17.

    P=\Pr[\text{positive}\mid\text{predicted positive}]=\frac{TP}{TP+FP},\qquad R=\Pr[\text{predicted positive}\mid\text{positive}]=\frac{TP}{TP+FN}.

## conditions

none

## ledger

none

## first stated

Primer S section S.1 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer S, chapters 0, 5, 14.

## related

bayes-rule, precision-recall, accuracy, calibration

## see also

none

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
