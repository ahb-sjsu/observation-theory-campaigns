# Asymmetric edge weight (legal)

**id.** legal-edge-weight
**kind.** concept
**volume.** Geometric Law, Volume 5 of the Geometric Series

## definition

The weight of a directed edge from case $i$ to case $j$ is the quadratic form $\Delta v^T \Sigma^{-1} \Delta v$, plus a penalty $\beta$ for each regime boundary crossed, plus a hierarchical cost. That cost is 0 from a higher court to a lower one, a positive constant $\eta$ at the same level, and infinite from lower to higher.

**Example.** In the volume's illustration the edge from McDonnell Douglas (Supreme Court) to a district case has quadratic form 5.3125, no boundary crossing and hierarchical cost 0, so its weight is 5.3125 + 0 + 0 = 5.3125. The reverse edge has infinite weight.

## equation

none

## conditions

- The weight is asymmetric, so it is a cost function for shortest paths on a directed graph and not a metric. The volume states that only the doctrinal term taken alone is a metric.
- The formula uses the quadratic form without the square root, although the chapter labels that term the Mahalanobis distance. The worked example adds the squared value to the other two terms.
- The boundary penalties are to be estimated from the observed cost of crossing jurisdictional, doctrinal, statutory and constitutional boundaries. The volume gives no estimated values.
- Chapter 15 gives a different operational weight, a cross-validated mix of a citation-type term, an attribute-distance term and an outcome term.

Conditions are curated in `volumes/geometric-law.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic status of 2026-07-14 calls the volume a posited framework with one instrumented corner. That corner is the legal text embedding LeBSE, validated in the xbse admission filter on US case law with labels from the CourtListener citation graph, and the README says this covers structure preservation in legal text embeddings and not the book's broader jurisprudential claims, which remain posited theory at licensed strength.

## first stated

Chapter 4, [`geometric-law/chapters/ch04_legal_metric.md:114-155`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch04_legal_metric.md#L114-L155), with the appendix form at [`geometric-law/chapters/ch04_legal_metric.md:408-412`](https://github.com/ahb-sjsu/geometric-law/blob/1021d65/chapters/ch04_legal_metric.md#L408-L412). Online, [Geometric Law](https://erisml.org/geometric-law/ch04_legal_metric.html).

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

legal-mahalanobis-distance, judicial-complex, legal-friction, precedential-weight-deformation, metric

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
