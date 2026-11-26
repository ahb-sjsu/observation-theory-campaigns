# Scalar Irrecoverability Theorem

**id.** scalar-irrecoverability
**kind.** result
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

A linear scalar summary $\phi(v) = w^\top v$ of an evaluation vector with n components, n at least 2, has a null space of dimension n minus 1. Vectors with the same summary can differ by any amount in their components, so the summary alone neither reconstructs the vector nor bounds its components.

**Example.** With weights (1, 1) the vectors (0, 10) and (10, 0) both have summary 10 and differ by 10 in each component. For the volume's evaluation on 5 dimensions the null space has dimension 4.

## equation

none

## conditions

- The summary is linear with a nonzero weight vector. The unbounded difference in every component needs at least two nonzero weights. With exactly one nonzero weight that component is determined by the summary and the others are free.
- For a continuous summary that is not linear the theorem says only that each interior value has an uncountable preimage, so the summary is not injective.
- The ultimatum-game vectors that illustrate it in Chapter 1 are posited.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Proved in writing in Appendix C. Parts (iii) and (iv) were restated or reproved in the November 2026 review, and there is no machine-checked proof.

## first stated

Section 1.1.1, [`geometric-methods/chapters/chapter-01-why-geometry.md:16-24`](https://github.com/ahb-sjsu/geometric-methods/blob/d910c92/chapters/chapter-01-why-geometry.md#L16-L24), and as Theorem C.1 in Appendix C, [`geometric-methods/chapters/appendix-c-proofs.md:13-23`](https://github.com/ahb-sjsu/geometric-methods/blob/d910c92/chapters/appendix-c-proofs.md#L13-L23). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-01-why-geometry.html).

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

null-space, projection, pareto-dominance, kernel

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
