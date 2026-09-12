# Bayes' rule

**id.** bayes-rule
**kind.** concept

## definition

The probability of a cause given an observation, equal to the probability of the observation given the cause times the base rate, divided by the overall probability of the observation. Precision is Bayes' rule with a classifier as the test. Primer S, equation S.3.

**Example.** Base rate one percent, detection ninety percent, false report five percent, so a positive report means the condition with probability 0.009 over 0.0585, about 0.154.

## equation

Book equation S.3.

    \Pr[A\mid B]=\frac{\Pr[B\mid A]\,\Pr[A]}{\Pr[B]},\qquad \Pr[B]=\Pr[B\mid A]\Pr[A]+\Pr[B\mid A^{c}]\Pr[A^{c}].

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

*Data Mining as Observation* primer S, chapters 6, 7.

## related

conditional-probability, base-rate, precision-recall, naive-bayes

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
