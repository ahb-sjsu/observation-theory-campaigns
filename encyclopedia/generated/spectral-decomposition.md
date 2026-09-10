# spectral decomposition

**id.** spectral-decomposition
**kind.** concept

## definition

A symmetric matrix written as the sum of its eigenvalues times the outer products of its orthonormal eigenvectors. Powers, inverses, and square roots act on the eigenvalues alone, and the quadratic form becomes a weighted sum of squared coordinates in the eigenvector basis. Primer L, equations L.14 and L.15.

**Example.** Rows (2, 1) and (1, 2) equal 3 times the matrix with every entry one half plus 1 times the matrix with rows (1/2, -1/2) and (-1/2, 1/2).

## equation

Book equation L.14.

    A=\sum_{i=1}^{d}\lambda_i\,v_iv_i^{\top}=V\Lambda V^{\top},\qquad V^{\top}V=I,\qquad \Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_d).

## conditions

none

## ledger

none

## first stated

Primer L section L.7 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

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

eigenvalue-eigenvector, outer-product, whitening, spectrum, symmetric-matrix

## see also

Book equations stated beside the entry's terms, not defining it: L.15.

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
