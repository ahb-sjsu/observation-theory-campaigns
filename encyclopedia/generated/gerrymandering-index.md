# Gerrymandering index

**id.** gerrymandering-index
**kind.** instrument
**volume.** Geometric Politics, Volume 10 of the Geometric Series

## definition

For a districting of $n$ voters, $GI$ is the average manifold distance from each voter to the Frechet mean of that voter's district. The Gerrymandering Surgery Theorem calls a map a gerrymander when its index exceeds the expected index of random compact, contiguous, population-equal maps.

**Example.** Four voters sit at 0, 1, 10 and 11 on a line. Districts {0, 1} and {10, 11} have means 0.5 and 10.5, and every voter is 0.5 from the mean, so the index is 0.5. Districts {0, 10} and {1, 11} have means 5 and 6, every voter is 5 away, and the index is 5.

**Known as, or related to prior art.** It sits beside the efficiency gap, which the volume treats as a one-dimensional test, and the ensemble method of computational redistricting.

## equation

none

## conditions

- It needs each voter's six-dimensional position and an ensemble of random valid maps. Appendix C uses 10,000 maps and treats a rank above the 95th percentile as evidence of manifold gerrymandering.
- Theorem 5 is stated as a criterion and the chapter gives no proof of it.
- A dimension-specific index can be high while the overall index is ordinary. The Map C example of an algorithmic map shows this on the trust and identity dimensions.
- The index values for the three District 7 maps are illustrative.

Conditions are curated in `volumes/geometric-politics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a political-argument instrument is plausible but has not been built or gated. District 7, the source of nearly every number in the volume, is a fictional district, and Chapter 18 says precise estimation of the manifold needs larger and richer datasets than currently exist.

## first stated

Definition 4 and Theorem 5 of Chapter 9, [`geometric-politics/manuscript/part_iii/ch09_gerrymandering.md:36-46`](https://github.com/ahb-sjsu/geometric-politics/blob/436c5b5/manuscript/part_iii/ch09_gerrymandering.md#L36-L46). Online, [Geometric Politics](https://erisml.org/geometric-politics/ch09_gerrymandering.html).

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

political-frechet-mean, manifold-community-of-interest, political-bond-index, mahalanobis-distance, monte-carlo

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
