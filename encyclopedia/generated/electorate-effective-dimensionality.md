# Effective dimensionality of an electorate

**id.** electorate-effective-dimensionality
**kind.** instrument
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

The number of eigenvalues of the electorate's six-by-six covariance matrix, taken from the largest down, needed to reach 85 percent of the total variance. One dominant eigenvalue means the left-right axis is a good approximation, and evenly spread eigenvalues mean it is a poor one.

**Example.** The volume's District 7 eigenvalues are 3.2, 2.8, 1.9, 1.5, 1.0 and 0.6, which sum to 11.0. The first three reach 7.9, or 72 percent, and the first four reach 9.4, or 85 percent, so the effective dimensionality is 4.

## equation

none

## conditions

- The inputs are standardized scores on the six dimensions from the 26-item instrument of Appendix C. The appendix recommends at least 500 voters, and 2,000 or more for the off-diagonal covariance terms.
- The 85 percent cut is the protocol's convention.
- The eigenvalues printed for the American electorate are given as approximate, and those for District 7 belong to a fictional district. Neither is a recorded measurement.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a political-argument instrument is plausible but has not been built or gated. District 7, the source of nearly every number in the volume, is a fictional district, and Chapter 18 says precise estimation of the manifold needs larger and richer datasets than currently exist.

## first stated

Appendix C.2, [`geometric-politics/manuscript/appendices/appendix_c_voting.md:67-71`](https://github.com/ahb-sjsu/geometric-politics/blob/436c5b5/manuscript/appendices/appendix_c_voting.md#L67-L71), with the reading of the eigenvalues in Chapter 4, [`geometric-politics/manuscript/part_ii/ch04_preference_manifold.md:100-100`](https://github.com/ahb-sjsu/geometric-politics/blob/436c5b5/manuscript/part_ii/ch04_preference_manifold.md#L100-L100). Online, [Geometric Politics](https://erisml.org/geometric-politics/appendix_c_voting.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Politics*, Volume 10 of the Geometric Series.

## related

covariance-matrix, eigenvalue-eigenvector, principal-component-analysis, explained-variance, political-preference-manifold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
