# communication metric

**id.** communication-metric
**kind.** concept
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

A Riemannian metric on the communication manifold written in three by three block form. The diagonal blocks are the metrics on signal, pragmatics and content, and the off-diagonal blocks carry the correlations between factors. With the off-diagonal blocks zero it reduces to $d^2 = \alpha_S d_S^2 + \alpha_P d_P^2 + \alpha_C d_C^2$ with positive weights.

**Example.** With all three weights equal to 1 and factor distances of 3 in signal, 0 in pragmatics and 4 in content, the block-diagonal distance is the square root of 9 + 0 + 16, which is 5.

## equation

none

## conditions

- The metric tensor is symmetric and positive definite. The chapter calls the block-diagonal form an approximation.
- The blocks are proposed, not fitted. The chapter suggests the log-Euclidean distance between spectral covariance matrices for acoustic signals, an embedding distance for content, and the Poincare ball distance for hierarchical content.
- No values of the weights or of the off-diagonal blocks are given.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. It says that no communication-domain instrument has been evaluated by the series' admission filter (xbse), that none currently passes its gate, and that the claims are theory at licensed strength and not validated measurement.

## first stated

Definition 3.2, [`geometric-communication/manuscript/part_i/ch03_communication_manifold.md:137-143`](https://github.com/ahb-sjsu/geometric-communication/blob/217c957/manuscript/part_i/ch03_communication_manifold.md#L137-L143), with the block-diagonal form at [`geometric-communication/manuscript/part_i/ch03_communication_manifold.md:129-133`](https://github.com/ahb-sjsu/geometric-communication/blob/217c957/manuscript/part_i/ch03_communication_manifold.md#L129-L133). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch03_communication_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

communication-manifold, metric, log-euclidean-distance, communication-distance-patterns, positive-definite

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
