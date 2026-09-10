# permutation test

**id.** permutation-test
**kind.** concept

## definition

A test that computes the p-value by reassigning the labels under the null, every way or a few thousand random ways, and counting the fraction of statistics at least as extreme as the observed. It needs no assumption about the shape of the data, and the sample size fixes the smallest p-value it can give. Primer S, equation S.15.

**Example.** Groups (8, 9) and (4, 5) have six reassignments, two with a difference of at least 4 in size, so the two-sided p-value is one third.

## equation

Book equation S.15.

    p=\Pr\big[\,|T|\ge|t_{\mathrm{obs}}|\ \big|\ \text{null}\,\big]=\frac{\#\{\text{reassignments with } |T|\ge|t_{\mathrm{obs}}|\}}{\#\{\text{reassignments}\}}.

## conditions

none

## ledger

none

## first stated

Primer S section S.7 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer S, chapters 0, 7, 8, 9, 14.

## related

null-hypothesis, p-value, null-model, seed, type-i-type-ii-error

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
