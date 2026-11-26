# economic metric (inverse covariance as metric tensor)

**id.** economic-metric-tensor
**kind.** concept
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

In the continuous limit of the decision complex the cost of a small displacement is $ds^2 = g_{ij}\,da^i\,da^j$ with the metric tensor g equal to the inverse of the nine by nine dimensional covariance matrix Sigma. Cost is counted in standard deviations of behavioral expectation, so unusual displacements are costly.

**Example.** With a diagonal covariance each dimension adds its squared change over its variance. In the volume's illustration a 100 dollar expense at monetary scale 50 adds $100^2/50^2 = 4.0$ and a fairness change of 0.6 at scale 0.8 adds 0.5625, for 4.5625 on those two dimensions.

**Known as, or related to prior art.** The Mahalanobis distance of 1936, read as a Riemannian metric.

## equation

none

## conditions

- Taking the inverse covariance as the metric tensor is tagged a modeling axiom.
- Sigma is symmetric positive semidefinite with at most 45 free parameters and is to be estimated from a calibration sample before prediction. The distance is a proper metric only when Sigma is positive definite and a pseudometric otherwise.
- Chapter 16 calls the calibration partial and lists as open whether Sigma can be estimated from large observational data, whether it is stable in time and whether it is universal or culture specific.
- The symmetric quadratic form cannot express the asymmetry between gains and losses. Section 4.10 replaces it with a Finsler metric for that purpose.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* Modeling axiom in the volume's tags. The repository's registered test prereg-coupling-v1, which predicted that one shared metric couples risk and social preferences as a rank-one factor, was scored on the Global Preferences Survey and falsified on that proxy. The same-subject angle test that the scorecard names as decisive is unrun. The preface and Section 16.1 report the failed test.

## first stated

Section 4.1, [`geometric-economics/chapters/ch04_economic_metric.md:40-50`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/chapters/ch04_economic_metric.md#L40-L50), after Definition 4 of Chapter 3, [`geometric-economics/chapters/ch03_decision_manifold.md:129-133`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/chapters/ch03_decision_manifold.md#L129-L133). The registered test named in the standing is scored in [`geometric-economics/experiments/RESULTS_coupling_scorecard.md:8-14`](https://github.com/ahb-sjsu/geometric-economics/blob/0382d57/experiments/RESULTS_coupling_scorecard.md#L8-L14). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch04_economic_metric.html).

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

geometric-decision-cost, mahalanobis-distance, covariance-matrix, economic-finsler-metric, economic-singularity, geometric-evaluation-theory

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
