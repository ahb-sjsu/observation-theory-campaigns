# inverse

**id.** inverse
**kind.** concept

## definition

The matrix that undoes a square matrix, so that the inverse times A times x is x. It exists exactly when the columns are independent, which for a two by two matrix means ad minus bc is not zero, and for a symmetric matrix it inverts each eigenvalue. Primer L, equations L.6 and L.15.

**Example.** The matrix with rows (2, 1) and (1, 3) has determinant 5 and inverse with rows (3, -1)/5 and (-1, 2)/5.

## equation

Book equation L.6.

    A=\begin{pmatrix}a&b\\ c&d\end{pmatrix},\qquad \det A=ad-bc,\qquad A^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\ -c&a\end{pmatrix}.

Book equation L.15.

    x^{\top}Ax=\sum_i\lambda_i\,(v_i\cdot x)^{2},\qquad A^{-1}=\sum_i\lambda_i^{-1}v_iv_i^{\top},\qquad A^{1/2}=\sum_i\lambda_i^{1/2}v_iv_i^{\top}.

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

*Data Mining as Observation* primer L, chapters 0, 2, 3, 4, 10, 11.

## related

determinant, rank, eigenvalue-eigenvector, matrix

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
