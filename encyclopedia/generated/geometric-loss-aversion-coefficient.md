# geometric loss-aversion coefficient

**id.** geometric-loss-aversion-coefficient
**kind.** result
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

The ratio of the edge weight of a loss to the edge weight of an equal gain, $\lambda = w_- / w_+$. A gain is taken to move the state on $d_1$ alone while a loss also moves it on rights, fairness, social and identity dimensions, so the ratio exceeds one and grows with the number and intensity of dimensions activated.

**Example.** The volume's Remark 35. A loss that activates four further dimensions at half a standard deviation each gives $1 + 4 \times 0.25 = 2.0$, against 1.0 for a loss that moves $d_1$ alone.

**Known as, or related to prior art.** Loss aversion in the prospect theory of Kahneman and Tversky, where the coefficient is a fixed parameter near 2.25.

## equation

none

## conditions

- The theorem is given with an argument that posits which dimensions a loss activates. The activations are not measured.
- Section 4.2 takes the ratio of edge weights, which are squared distances. Section 4.10 and the technical appendix take the ratio of Finsler lengths, which is the square root of that ratio. Section 4.10 states the relation, and the volume does not settle which of the two is compared with 2.25.
- The volume states its falsifiers. A coefficient that is constant across conditions, or one that varies but not monotonically with the count of activated dimensions, would show the derivation wrong.
- The chapter says the value 2.25 should be derivable from a fitted Sigma and calls that fitting an empirical programme.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* An argument from posited activations, tagged in parts as conditional theorem and as empirical prediction. Section 4.2 calls it a derivation, while the chapter opening says the chapter reads loss aversion as a property of the metric and that sealed tests of reduced-form geometric models against cumulative prospect theory have so far favored prospect theory (Geometric Ethics, Section 20.8). The chapter cites the eris-econ calibration for a range of 1.0 to 3.53 and calls it an in-sample calibration, not a held-out test. The README of 2026-07-14 says no economics instrument has passed the series' admission filter.

## first stated

Theorem 34, Section 4.2, [`geometric-economics/chapters/ch04_economic_metric.md:68-99`](https://github.com/ahb-sjsu/geometric-economics/blob/a4483e7/chapters/ch04_economic_metric.md#L68-L99). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch04_economic_metric.html).

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

economic-metric-tensor, economic-finsler-metric, metric-feature-versus-heuristic-error, economic-decision-dimensions

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
