# matrix

**id.** matrix
**kind.** concept

## definition

A table of numbers with n rows and d columns that sends a vector to the linear combination of its columns with the vector's coordinates as the scalars. A data table with numeric columns is one. Primer L, equation L.5.

**Example.** Rows (2, 1) and (1, 3) send (1, 2) to 1 (2, 1) + 2 (1, 3) = (4, 7).

## equation

Book equation L.5.

    (Ax)_i=\sum_{j}A_{ij}x_j,\qquad Ax=x_1\,a_1+\cdots+x_d\,a_d\ \ \text{with } a_j \text{ the } j\text{th column}.

## conditions

none

## ledger

none

## first stated

Primer L section L.3 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primers L and S, chapters 0, 1, 4, 6, 7, 8, 9, 10, 12, 13.

## related

vector, transpose, inverse, rank, linear-combination

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
