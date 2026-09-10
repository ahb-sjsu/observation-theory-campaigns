# determinant

**id.** determinant
**kind.** concept

## definition

For a two by two matrix, ad minus bc, the number whose vanishing means the columns are dependent and no inverse exists. For a symmetric matrix it is the product of the eigenvalues. Primer L, equation L.6.

**Example.** Rows (1, 2) and (2, 4) give 4 - 4 = 0, so the matrix has no inverse.

## equation

Book equation L.6.

    A=\begin{pmatrix}a&b\\ c&d\end{pmatrix},\qquad \det A=ad-bc,\qquad A^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\ -c&a\end{pmatrix}.

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

*Data Mining as Observation* primer L, chapters 2.

## related

inverse, rank, eigenvalue-eigenvector, linear-independence

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
