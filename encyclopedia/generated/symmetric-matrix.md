# symmetric matrix

**id.** symmetric-matrix
**kind.** concept

## definition

A square matrix equal to its own transpose. Its eigenvalues are real, its eigenvectors can be chosen orthonormal, and it is the sum of its eigenvalues times the outer products of its eigenvectors. Almost every matrix in the book is one. Primer L, equation L.14.

**Example.** The matrix with rows (2, 1) and (1, 2) is symmetric, and the one with rows (2, 1) and (0, 2) is not.

## equation

Book equation L.14.

    A=\sum_{i=1}^{d}\lambda_i\,v_iv_i^{\top}=V\Lambda V^{\top},\qquad V^{\top}V=I,\qquad \Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_d).

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

*Data Mining as Observation* primers L and S, chapters 0, 3, 4, 5, 9, 10.

## related

transpose, eigenvalue-eigenvector, spectral-decomposition, covariance-matrix

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
