# conditional probability

**id.** conditional-probability
**kind.** concept

## definition

The probability of A among the repetitions in which B occurred, the probability of both divided by the probability of B. Precision, recall, and calibration are each one. Primer S, equation S.2.

**Example.** Given that the first die shows three, the sum is seven only when the second shows four, probability one sixth.

## equation

Book equation S.2.

    \Pr[A\mid B]=\frac{\Pr[A\cap B]}{\Pr[B]},\qquad A,B\ \text{independent}\iff \Pr[A\cap B]=\Pr[A]\,\Pr[B].

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

*Data Mining as Observation* primer S.

## related

probability, independence, bayes-rule, precision-recall, calibration

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
