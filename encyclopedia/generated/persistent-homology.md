# persistent homology

**id.** persistent-homology
**kind.** concept
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

Connect the points of a cloud that lie within a distance threshold, forming the Vietoris-Rips complex, and raise the threshold from zero. Each topological feature, a connected component or a loop, has a birth threshold and a death threshold, and its persistence is death minus birth.

**Example.** For three points on a line at 0, 1 and 3, three components are born at threshold 0. One dies at 1, when the first two points join, one dies at 2, when the third joins, and one never dies, so the persistences are 1 and 2.

**Known as, or related to prior art.** Persistent homology of topological data analysis, with the stability theorem of Cohen-Steiner, Edelsbrunner and Harer (2007).

## equation

none

## conditions

- Long persistence is read as structure and short persistence as noise. The volume calls this a heuristic, made formal by the stability theorem, under which a perturbation of the cloud by at most delta moves the persistence diagram by at most delta in bottleneck distance.
- One connected component never dies. It is excluded from summary statistics.
- Higher homology dimensions are expensive to compute and rarely interpretable. The volume says components and loops suffice for most applications.
- The contribution the volume claims for this layer in the bioacoustics case study is posited. The comparison of Section 20.9.4 has not been run.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The README's status note of 2026-07-14 calls this volume the series' metrology discipline, a method that is normative and not a finding. Its Section 21.8 (November 2026) classes each result as proved, posited, or measured on a recorded run, and the tables of Chapters 1, 8, 9, 11 and 12 are posited illustrations.

## first stated

Section 5.3.1, [`geometric-methods/chapters/chapter-05-topological-data-analysis.md:105-122`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-05-topological-data-analysis.md#L105-L122). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-05-topological-data-analysis.html).

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

graph, hierarchical-clustering, manifold, intrinsic-dimension

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
