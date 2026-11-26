# Legal Mahalanobis distance

**id.** legal-mahalanobis-distance
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

The distance between two cases is the square root of $\Delta v^T \Sigma^{-1} \Delta v$, where $\Delta v$ is the difference of their eight-dimensional attribute vectors and $\Sigma$ is the covariance matrix of the eight dimensions over the case corpus.

**Example.** In the volume's illustration every variance is 0.04, so a difference of 0.3 on one dimension contributes 0.09 / 0.04 = 2.25. Its eight contributions sum to 5.3125, and the square root gives a distance of about 2.30.

**Known as, or related to prior art.** Mahalanobis distance.

## equation

none

## conditions

- The covariance matrix must be positive definite. When it is diagonal the distance reduces to a Euclidean distance with each dimension weighted by the inverse of its variance.
- The front matter classes the Mahalanobis metric as a modeling axiom. The volume says the metric is calibrated from data and can be miscalibrated, for example by a biased corpus.
- Chapter 4 states that the calibration programme has not yet been executed on legal data. Chapter 16 lists metric calibration as its first open problem and says no calibration protocol, sensitivity bound or uncertainty procedure exists yet.
- The predicted off-diagonal entries, such as a positive covariance of statutory authority with remedial scope, are stated as falsifiable predictions. The volume reports no test of them.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 4, [`geometric-law/chapters/ch04_legal_metric.md:52-60`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch04_legal_metric.md#L52-L60). Online, [Geometric Law](https://erisml.org/geometric-law/ch04_legal_metric.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Law*, Volume 5 of the Geometric Series.

## related

mahalanobis-distance, covariance-matrix, eight-legal-dimensions, legal-edge-weight, calibration, positive-definite

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
