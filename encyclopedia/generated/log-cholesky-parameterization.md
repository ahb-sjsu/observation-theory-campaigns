# log-diagonal Cholesky parameterization

**id.** log-cholesky-parameterization
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Write a symmetric positive definite matrix as L times its transpose, with L lower triangular, and store the diagonal of L as logarithms. The n(n+1)/2 stored numbers are unconstrained, and any real values give a symmetric positive definite matrix.

**Example.** For a 2 by 2 matrix, log-diagonal entries of 0 and 0 with an off-diagonal entry of 1 give L with rows (1, 0) and (1, 1), and the product has rows (1, 1) and (1, 2), with determinant 1. A 9 by 9 matrix needs 36 + 9 = 45 numbers.

**Known as, or related to prior art.** The Cholesky factorization with a log-transformed diagonal.

## equation

none

## conditions

- The map from the parameters to the positive definite matrices is smooth, onto, and has a smooth inverse, the Cholesky decomposition followed by the logarithm of the diagonal.
- Setting every parameter to zero gives the identity matrix, the volume's starting point for optimization.
- When the training signal is too limited to fit a full matrix, Section 15.8 restricts the factor to its n diagonal numbers, which gives a diagonal matrix.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The surjection is Theorem C.5 of Appendix C with its Corollary C.5.1, proved in writing. No machine-checked proof.

## first stated

Section 15.3.1, [`geometric-methods/chapters/chapter-15-cholesky-parameterization.md:66-75`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-15-cholesky-parameterization.md#L66-L75), with the complete map in Section 15.3.3, [`geometric-methods/chapters/chapter-15-cholesky-parameterization.md:97-106`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-15-cholesky-parameterization.md#L97-L106). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-15-cholesky-parameterization.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

positive-definite, symmetric-matrix, log-euclidean-distance, mahalanobis-distance, covariance-matrix

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
