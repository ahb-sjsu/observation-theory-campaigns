# cuisine as a distribution and its flavor eigenvectors

**id.** cuisine-flavor-eigenvectors
**kind.** concept
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

A cuisine is a probability distribution over flavor space, estimated from a corpus of recipes and summarized by its mean and covariance $\Sigma_C$. The eigenvectors of $\Sigma_C$ are the cuisine's flavor eigenvectors, and $\lambda_k / \sum_j \lambda_j$ is the share of its flavor variation along axis k.

**Example.** With eigenvalues 6, 3 and 1 the first axis carries 6/10 = 60% of the variance and the first two carry 90%. The numbers are illustrative.

## equation

none

## conditions

- The distribution is a modeling axiom. The eigendecomposition of a symmetric positive-semidefinite covariance is tagged a theorem and is standard linear algebra.
- The named axes (richness for French, dashi for Japanese, chile and toast for Mexican) are a stylized reading. The volume says the axes depend on corpus and featurization, and that honest practice reports the loadings.
- The claim that five to ten components capture most within-cuisine variance is tagged empirical and stated without a printed spectrum.
- Authenticity is read as likelihood under the distribution, so a cuisine has no sharp edges.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, with no gastronomy instrument evaluated by the series' admission filter (xbse) and the nearest evaluated perceptual domains, aesthetics and music, rated inadmissible to medium. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each statement as a modeling axiom, empirical, a conjecture or a theorem.

## first stated

Chapter 9, [`geometric-gastronomy/chapters/ch09_the_eigenvalues_of_a_kitchen.md:24-24`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/dfbfdbb/chapters/ch09_the_eigenvalues_of_a_kitchen.md#L24-L24), with the eigendecomposition in Section 9.2, [`geometric-gastronomy/chapters/ch09_the_eigenvalues_of_a_kitchen.md:40-44`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/dfbfdbb/chapters/ch09_the_eigenvalues_of_a_kitchen.md#L40-L44). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch09_the_eigenvalues_of_a_kitchen.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Gastronomy*, Volume 12 of the Geometric Series.

## related

principal-component-analysis, covariance-matrix, eigenvalue-eigenvector, explained-variance, fusion-geodesic, culinary-convergence-conjecture

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
