# log-Euclidean distance

**id.** log-euclidean-distance
**kind.** concept
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

The distance between two symmetric positive definite matrices is the Frobenius norm of the difference of their matrix logarithms, $d_{LE}(S_1, S_2) = \|\log S_1 - \log S_2\|_F$. The logarithm is taken on the eigenvalues.

**Example.** The logarithm of the identity is the zero matrix and the logarithm of diag(e, e) is diag(1, 1), so their distance is the square root of 2, about 1.414.

**Known as, or related to prior art.** The log-Euclidean metric of Arsigny et al. (2006).

## equation

none

## conditions

- Both matrices are symmetric positive definite, so every eigenvalue is strictly positive and its logarithm exists. The printed code clamps eigenvalues at 1e-10.
- It is a proper metric, because the logarithm maps the positive definite matrices one to one onto the symmetric matrices, where the Frobenius norm is a metric.
- The Frechet mean under this distance has a closed form, the exponential of the weighted average of the logarithms. Under the affine-invariant metric the mean needs an iterative algorithm.
- The contribution the volume claims for this layer in the bioacoustics case study is posited. The comparison of Section 20.9.4 has not been run.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* A definition. Its metric property is stated with a proof sketch as Proposition 4.1 and proved in writing as Theorem C.4 of Appendix C, with no machine-checked proof.

## first stated

Definition 4.2 and Proposition 4.1, [`geometric-methods/chapters/chapter-04-spd-manifolds.md:45-55`](https://github.com/ahb-sjsu/geometric-methods/blob/d910c92/chapters/chapter-04-spd-manifolds.md#L45-L55). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-04-spd-manifolds.html).

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

positive-definite, frobenius-norm, covariance-matrix, log-cholesky-parameterization, mahalanobis-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
