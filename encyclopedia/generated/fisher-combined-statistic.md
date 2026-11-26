# Fisher-combined significance

**id.** fisher-combined-statistic
**kind.** instrument
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The statistic $-2 \sum_i \ln p_i$ over $k$ independent p-values, one per model. Under the null it follows a chi-squared distribution with $2k$ degrees of freedom. The volume converts the combined p-value to a sigma value with the standard normal quantile function and reports its headline results in this form.

**Example.** Two p-values of 0.01 give -2 times (ln 0.01 + ln 0.01) = 18.42, to be compared with a chi-squared distribution with 4 degrees of freedom.

**Known as, or related to prior art.** Fisher's method for combining independent p-values.

## equation

none

## conditions

- The method is tagged established mathematics and assumes independent tests. The volume grants that the five models share training methods and that four share a lineage.
- The volume calls the combined test anti-conservative under positive dependence, so the true significance is lower than reported.
- Each cell holds 5 to 25 evaluations, so the per-model p-values that enter the sum may be imprecise.
- A combined sigma value is a statement about the five tested models taken together. The volume limits it to transformer language models from two laboratories.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A standard statistical method. The five headline sigma values it produces are measured benchmark results whose independence assumption the volume itself says is imperfect.

## first stated

Section 12.6.1, [`geometric-reasoning/chapters/ch12_benchmarks_as_geometric_probes.md:340-344`](https://github.com/ahb-sjsu/geometric-reasoning/blob/b645f23/chapters/ch12_benchmarks_as_geometric_probes.md#L340-L344), and the technical appendix, [`geometric-reasoning/chapters/ch12_benchmarks_as_geometric_probes.md:483-495`](https://github.com/ahb-sjsu/geometric-reasoning/blob/b645f23/chapters/ch12_benchmarks_as_geometric_probes.md#L483-L495). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch12_benchmarks_as_geometric_probes.html).

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

p-value, null-hypothesis, multiple-comparisons, independence, reasoning-bond-invariance-principle

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
