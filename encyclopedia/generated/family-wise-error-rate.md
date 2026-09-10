# family-wise error rate

**id.** family-wise-error-rate
**kind.** concept

## definition

The probability of at least one false alarm across a set of tests, at most the number of tests times the per-test threshold by the union bound. Primer S, equation S.16.

**Example.** Forty tests at 0.05 have family-wise error rate 1 minus 0.95 to the fortieth, about 0.87.

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

*Data Mining as Observation* primer S, chapters 8.

## related

bonferroni-correction, multiple-comparisons, p-value

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
