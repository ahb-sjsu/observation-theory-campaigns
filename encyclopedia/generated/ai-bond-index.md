# Bond Index for AI

**id.** ai-bond-index
**kind.** instrument
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

The expected excess geodesic deviation of a system's trajectory on the value manifold over the value-aligned geodesic, reported as nine components, one per value dimension. The total is the square root of the sum of the squared components. Stratified by user population or averaged over time it gives a fairness audit and a drift monitor.

**Example.** Components of 0.03 on welfare and 0.04 on dignity, with the other seven at 0, give a total of the square root of 0.0009 + 0.0016, which is 0.05. Deviations of 0.1, 0.2 and 0.3 over three interactions give a running value of 0.6 / 3, which is 0.2.

## equation

none

## conditions

- The value-aligned geodesic is not observable. The volume approximates it by expert evaluation, by consensus of evaluators, by treating a gauge-invariant output as aligned, or by a trained evaluation model.
- The total is a scalar, and the volume says the Scalar Irrecoverability Theorem applies to it. The component vector is kept for diagnosis.
- The thresholds of the green, yellow and red alert zones are parameters set by governance for each deployment. The volume gives no values.
- Every Bond Index number in the volume belongs to the fictional ARIA and ARIA-G. The README says no alignment instrument has been evaluated.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* A posited instrument defined as a geodesic deviation. A note of 2026-11-26 in Section 9.8 says it is of the kind that Geometric Ethics calls the clinical Bond Index, and that this is a different quantity from the Bond Index of Geometric Ethics, the mean change of an evaluation under declared re-descriptions. No measured value of it is reported.

## first stated

Definition 9.1, Section 9.1, [`geometric-ai/manuscript/part_iii/ch09_bond_index_ai.md:26-36`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_iii/ch09_bond_index_ai.md#L26-L36), with the total at [`geometric-ai/manuscript/part_iii/ch09_bond_index_ai.md:50-56`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_iii/ch09_bond_index_ai.md#L50-L56), the stratified form at [`geometric-ai/manuscript/part_iii/ch09_bond_index_ai.md:58-66`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_iii/ch09_bond_index_ai.md#L58-L66) and the running form at [`geometric-ai/manuscript/part_iii/ch09_bond_index_ai.md:76-88`](https://github.com/ahb-sjsu/geometric-ai/blob/a628e38/manuscript/part_iii/ch09_bond_index_ai.md#L76-L88). Online, [Geometric AI](https://erisml.org/geometric-ai/ch09_bond_index_ai.html).

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

bond-index, legal-bond-index, reasoning-geodesic-deviation, alignment-gauge-violation-tensor, drift, stratification

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
