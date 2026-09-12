# Bonferroni correction

**id.** bonferroni-correction
**kind.** concept

## definition

Dividing the significance threshold by the number of tests, which holds the family-wise error rate at or below the original threshold whatever the dependence among the tests, at the price of being conservative. Primer S, equation S.16.

**Example.** Forty tests at 0.05 become forty tests at 0.00125.

## equation

Book equation S.16.

    \Pr[\text{at least one false alarm}]\le m\,\alpha,\qquad \alpha_{\mathrm{Bonf}}=\frac{\alpha}{m}.

## conditions

none

## ledger

none

## first stated

Primer S section S.8 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer S, chapters 5, 8.

## related

family-wise-error-rate, multiple-comparisons

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
