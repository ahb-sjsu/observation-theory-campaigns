# Value metric

**id.** value-metric
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

The symmetric positive-definite 9 by 9 matrix g(v) that prices an infinitesimal value change as $ds^2 = g_{\mu\nu}(v) dv^\mu dv^\nu$. The cost of a trajectory is the integral of ds along it, and the value geodesic between two states is the trajectory of least cost.

**Example.** In the Mahalanobis form with covariance diag(4, 1), the change (2, 1) costs 2 times 2 over 4 plus 1 times 1 over 1, which is 2. With the identity in place of the covariance the same change costs 5.

**Known as, or related to prior art.** A Riemannian metric, approximated locally by the Mahalanobis metric.

## equation

none

## conditions

- The metric depends on position and on the population. Whether a deployed system uses one metric or one per population is called a governance decision, not a mathematical one.
- The approximation of the metric by the inverse covariance matrix of the value dimensions is exact only for a flat manifold with a constant metric. The volume uses it for local computations and says it breaks down globally.
- Chapter 20 lists as open question 1 whether the metric can be estimated from human preference data at the precision alignment engineering needs. The metric components printed in Chapter 16 belong to the fictional ARIA-G narrative.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Definition 4.1, Section 4.3, [`geometric-ai/manuscript/part_ii/ch04_value_manifold.md:118-128`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch04_value_manifold.md#L118-L128), with the Mahalanobis approximation at [`geometric-ai/manuscript/part_ii/ch04_value_manifold.md:138-146`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_ii/ch04_value_manifold.md#L138-L146). Online, [Geometric AI](https://erisml.org/geometric-ai/ch04_value_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric AI*, Volume 11 of the Geometric Series.

## related

mahalanobis-distance, metric, geodesic-distance, value-manifold, geometric-rlhf

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
