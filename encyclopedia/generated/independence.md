# independence

**id.** independence
**kind.** concept

## definition

Two events are independent when knowing one changes nothing about the other, so that the probability of both is the product. Independent variables have variances that add, and tests on overlapping data are not independent. Primer S, equation S.2.

**Example.** The first die showing three and the sum being seven have joint probability 1/36, the product of 1/6 and 1/6, so they are independent.

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

*Data Mining as Observation* primers L and S, chapters 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

conditional-probability, variance, multiple-comparisons

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
