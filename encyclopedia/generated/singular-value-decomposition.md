# singular value decomposition

**id.** singular-value-decomposition
**kind.** concept

## definition

Any matrix written as a sum of rank-one outer products ordered by size, with orthonormal vectors on both sides, the eigenvector idea for a matrix that is not square. Its right singular vectors are the eigenvectors of A transposed A, and for centered data they are the principal components. Primer L, equations L.16 and L.17.

**Example.** Rows (1, 1), (1, 0), and (0, 1) have A transposed A with rows (2, 1) and (1, 2), so the singular values are root 3 and 1.

## equation

Book equation L.16.

    A=\sum_{i=1}^{r}\sigma_i\,u_iv_i^{\top}=U\Sigma_{\!s}V^{\top},\qquad \sigma_1\ge\sigma_2\ge\cdots\ge\sigma_r>0,\qquad U^{\top}U=I,\ V^{\top}V=I.

## conditions

none

## ledger

none

## first stated

Primer L section L.8 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L, chapters 0.

## related

singular-value, principal-component-analysis, low-rank-approximation, latent-semantic-analysis, eigenvalue-eigenvector

## see also

Book equations stated beside the entry's terms, not defining it: L.17.

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
