# quadratic form

**id.** quadratic-form
**kind.** concept

## definition

The number x transposed A x that a symmetric matrix assigns to a vector, a sum of the entries times pairs of coordinates. Along a unit direction the covariance's quadratic form is a variance and the read operator's is a read distortion. Primer L, equation L.11.

**Example.** For rows (2, 1) and (1, 2) at x = (1, 1), A x = (3, 3) and the form is 6.

## equation

Book equation L.11.

    x^{\top}Ax=\sum_{i,j}A_{ij}\,x_i x_j.

## conditions

none

## ledger

none

## first stated

Primer L section L.6 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L, chapters 0, 3.

## related

positive-semidefinite, covariance-matrix, read-distortion, variance, positive-definite

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
