# economic gauge violation tensor and Bond Index

**id.** economic-gauge-violation-tensor
**kind.** instrument
**volume.** Geometric Economics, Volume 4 of the Geometric Series

## definition

For a heuristic h, transformations i and states j, the entry $V_{ij}$ is h of the transformed state minus h of the state. An invariant heuristic has every entry zero, and the Frobenius norm of V is the total violation. The Bond Index of Chapter 4 is the same difference in absolute value divided by h of the state.

**Example.** A heuristic that scores a wage offer 100 in annual terms and 110 in monthly terms has an entry of 10 for that transformation and state, and a Bond Index of 10 / 100 = 0.10.

## equation

none

## conditions

- The transformations must be meaning preserving. Under Remark 45 a nonzero entry can be a pseudo-violation that reflects real economic content.
- Proposition 42 gives the composition rule. The violation of a composed transformation is the sum of the violations along the chain.
- The chapter describes a measurement protocol, the same states shown under each transformation to the same or matched subjects. It reports published experiments by others and no measurement of the tensor itself.

Conditions are curated in `volumes/geometric-economics.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls the volume a posited framework, speculative theory awaiting instruments, and says that no economics instrument has been evaluated by the series' admission filter and that none passes its gate. Its claims are to be read as theory at licensed strength and not as validated measurement, and the chapters tag each claim as established mathematics, empirical, modeling axiom, conditional theorem or speculation.

## first stated

Definition 41, Section 8.7, [`geometric-economics/chapters/ch08_gauge_invariance.md:256-264`](https://github.com/ahb-sjsu/geometric-economics/blob/ab7b319/chapters/ch08_gauge_invariance.md#L256-L264), with the Bond Index in Section 4.4, [`geometric-economics/chapters/ch04_economic_metric.md:160-164`](https://github.com/ahb-sjsu/geometric-economics/blob/ab7b319/chapters/ch04_economic_metric.md#L160-L164). Online, [Geometric Economics](https://erisml.org/geometric-economics/ch08_gauge_invariance.html).

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

economic-bond-invariance-principle, metric-feature-versus-heuristic-error, market-pathology-taxonomy, frobenius-norm

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
