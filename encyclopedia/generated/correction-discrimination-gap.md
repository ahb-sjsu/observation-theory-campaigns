# Discrimination gap

**id.** correction-discrimination-gap
**kind.** instrument
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The correct-flip rate minus the wrong-flip rate. The correct-flip rate is how often a system changes its answer after a valid correction, and the wrong-flip rate is how often it abandons a correct answer after an invalid one. A gap of 1 is perfect discrimination and a gap of 0 is none.

**Example.** A system that flips on 60 percent of valid corrections and 10 percent of invalid ones has a gap of 0.60 - 0.10 = 0.50 and a sycophancy index of 0.10 / 0.60, about 0.17.

## equation

none

## conditions

- It is an observable computed from two rates on the same correction task, with no geometric assumption.
- The companion sycophancy index is the wrong-flip rate divided by the correct-flip rate.
- Table 6.1 prints gaps of 0.588, 0.377, 0.238 and 0.206 for four models. The table of Section 11.4.1 printed different rates for three of them until the correction of 2026-11-26 and now follows Table 6.1.
- Reading the gap as distance to a critical surface or as the asymmetry of a basin is the volume's posited interpretation.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A measured benchmark quantity tagged empirical. The two chapters that tabulate it agree since the correction of 2026-11-26, which set Chapter 11 to the values of Table 6.1. The benchmark's run records are not in the repository.

## first stated

Definition 6.2, [`geometric-reasoning/chapters/ch06_sycophancy_as_search_hijacking.md:458-462`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch06_sycophancy_as_search_hijacking.md#L458-L462), with the sycophancy index defined at [`geometric-reasoning/chapters/ch06_sycophancy_as_search_hijacking.md:452-456`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch06_sycophancy_as_search_hijacking.md#L452-L456). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch06_sycophancy_as_search_hijacking.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Reasoning*, Volume 3 of the Geometric Series.

## related

sycophancy-parameter, corrigibility-basin, precision-recall, false-positive-rate

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
