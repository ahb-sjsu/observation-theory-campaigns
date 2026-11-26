# moral-economic boundary and boundary penalty

**id.** moral-economic-boundary
**kind.** concept
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

A threshold in the decision complex where the local decision regime changes discontinuously. Crossing boundary k adds a penalty $\beta_k$ to the edge weight on top of the Mahalanobis term, and the penalty may be infinite.

**Example.** The volume's grocery example. Buying for 50 dollars has weight $50^2/\sigma_1^2$, which is 1 when the monetary scale is 50, and stealing crosses the theft boundary with infinite penalty. The buy edge is the cheaper one.

**Known as, or related to prior art.** Tetlock's forbidden or taboo trade-offs, which the volume names as the infinite-penalty case.

## equation

none

## conditions

- The three regimes of the penalty, infinite, finite and zero, are tagged a modeling axiom.
- The volume says finite penalties are measurable as the compensation at which agents become willing to cross, after the taboo trade-off paradigm of Tetlock. It reports no such measurement of its own.
- The four named types are the theft, promise, sacred-value and market-norm against social-norm boundaries. The last changes the covariance matrix itself and not only a penalty.
- Chapter 16 leaves open whether infinite boundaries are topological features or only very high penalties.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls the volume a posited framework, speculative theory awaiting instruments, and says that no economics instrument has been evaluated by the series' admission filter and that none passes its gate. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation.

## first stated

Section 3.4 on boundary penalties and Definition 5, Section 3.5, [`geometric-economics/chapters/ch03_decision_manifold.md:152-166`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/chapters/ch03_decision_manifold.md#L152-L166), with the three penalty regimes in the technical appendix, [`geometric-economics/chapters/ch03_decision_manifold.md:399-404`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/chapters/ch03_decision_manifold.md#L399-L404). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch03_decision_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Economics*, Volume 4 of the Geometric Series.

## related

economic-decision-complex, geometric-decision-cost, economic-heuristic-truncation-theorem, economic-no-escape-conjecture, threshold

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
