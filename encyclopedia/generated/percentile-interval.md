# percentile interval

**id.** percentile-interval
**kind.** concept

## definition

The bootstrap interval that takes the 2.5th and 97.5th percentiles of a statistic recomputed on a few thousand resamples. It works for statistics with no standard error formula, a median, an AUROC, a rank correlation. Primer S section S.6.

**Example.** Two thousand bootstrap means of 2, 4, 4, 4, 5, 5, 7, 9, sorted, have their 50th and 1950th values as the interval.

## equation

none

## conditions

none

## ledger

none

## first stated

Primer S section S.6 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

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

bootstrap, confidence-interval, percentile, paired

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
