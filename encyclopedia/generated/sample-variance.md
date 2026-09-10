# sample variance

**id.** sample-variance
**kind.** concept

## definition

The average squared deviation from the sample mean with n minus 1 in the denominator, because the sample mean sits closer to its own sample than the true mean does and the deviations come out a little small. Primer S, equation S.9.

**Example.** The deviations of 2, 4, 4, 4, 5, 5, 7, 9 from 5 have squares summing to 32, so the sample variance is 32 over 7, about 4.571.

## equation

Book equation S.9.

    \bar x=\frac1n\sum_i x_i,\qquad s^{2}=\frac{1}{n-1}\sum_i(x_i-\bar x)^{2}.

## conditions

none

## ledger

none

## first stated

Primer S section S.4 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

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

variance, standard-deviation, estimator

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
