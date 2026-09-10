# linear combination

**id.** linear-combination
**kind.** concept

## definition

A sum of scalar multiples of vectors. A matrix sends a vector to the linear combination of its columns with the vector's coordinates as the scalars. Primer L, equations L.1 and L.5.

**Example.** 2(1, 2) + (3, -1) = (5, 3).

## equation

Book equation L.1.

    x+y=(x_1+y_1,\dots,x_d+y_d),\qquad c\,x=(c\,x_1,\dots,c\,x_d).

Book equation L.5.

    (Ax)_i=\sum_{j}A_{ij}x_j,\qquad Ax=x_1\,a_1+\cdots+x_d\,a_d\ \ \text{with } a_j \text{ the } j\text{th column}.

## conditions

none

## ledger

none

## first stated

Primer L section L.1 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L.

## related

span, basis, matrix, vector

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
