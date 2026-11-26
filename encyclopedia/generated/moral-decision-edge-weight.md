# Mahalanobis edge weight with boundary penalties

**id.** moral-decision-edge-weight
**kind.** concept
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

The weight of an action from state i to state j on the moral decision complex. It is the squared Mahalanobis distance of the attribute change under the 9 by 9 moral covariance, plus a penalty for each moral boundary the action crosses, $w = \Delta a^T \Sigma^{-1} \Delta a + \sum_k \beta_k 1[k]$.

**Example.** With the identity as covariance and a change of 1 on one dimension and 2 on another, the first term is 1 + 4 = 5. Crossing one boundary with penalty 3 gives a weight of 8, and a boundary with infinite penalty gives an infinite weight. The numbers are illustrative.

**Known as, or related to prior art.** Squared Mahalanobis distance with additive penalty terms.

## equation

none

## conditions

- Evidence status of the metric (Section 8.10a, added in v1.28). The covariance is a modeling choice with no evidence so far. No measurement in the volume shows that a metric, set by hand or learned, predicts moral judgements better than the boundary penalties alone, and the one registered test was void.
- Penalties follow the boundary type. A threshold has a finite penalty, a phase transition a large finite one, and an absorbing or sacred-value boundary an infinite one, so no finite-cost path crosses it.
- For the limit to Riemannian arc length each edge is weighted by the square root of the quadratic form. The sum of the squared forms along a refining path tends to zero.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Tagged Formal Definition in the text. The v1.28 change notes state that the ledger has no claim for Definition 8.13 or for the metric's predictive value.

## first stated

Definition 8.13, Section 8.10a, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1270-1285`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1270-L1285), with the penalties classified at [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1318-1333`](https://github.com/ahb-sjsu/geometric-ethics/blob/cf2325e/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1318-L1333). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Ethics*, Volume 2 of the Geometric Series.

## related

moral-decision-complex, moral-metric-evidence-status, mahalanobis-distance, covariance-matrix, geometric-decision-cost, moral-phase-transition

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
