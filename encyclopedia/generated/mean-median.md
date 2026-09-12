# mean, median

**id.** mean-median
**kind.** concept

## definition

The mean of a sample is its average and the median its middle value once sorted. One wild value moves the mean and leaves the median, which is why the book reports a median where one value can be wild. Primer S, equation S.9.

**Example.** 2, 4, 4, 4, 5, 5, 7, 9 has mean 5 and median 4.5, and with the 9 changed to 90 the mean is 15.125 while the median stays 4.5.

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

*Data Mining as Observation* primer S, chapters 2, 4, 6, 7, 11, 13.

## related

expectation, percentile, standard-deviation, skewness

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
