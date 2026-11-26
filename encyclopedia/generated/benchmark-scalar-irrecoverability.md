# Scalar Irrecoverability Theorem for benchmark profiles

**id.** benchmark-scalar-irrecoverability
**kind.** result
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

If the performance profiles of a set of models are mutually Pareto-non-dominated, so that each model beats each other on some dimension and loses on another, then every weighted-sum score with non-negative weights ranks some model below another that it beats on a subset of at least two dimensions.

**Example.** On the volume's two metacognition scores, (0.700, 0.350) averages 0.525 and (0.094, 0.723) averages 0.409, so the average ranks the first model higher although the second is better on the second score.

**Known as, or related to prior art.** The fact that a partial order of Pareto-incomparable points has no order-preserving map to a line that reflects every coordinate. The volume attributes the theorem to Geometric Methods, Chapter 1.

## equation

none

## conditions

- The hypothesis is that no profile dominates another. Where one model is at least as good on every dimension, a monotone score can respect the ordering.
- Tagged a conditional theorem. The proof's step to a subset of size two is not general and appeals to the measured profiles of the five models.
- The volume states it in three forms. Section 13.6 speaks of any composite score, Theorem 13.1 of weighted sums, and Theorem A10.1 of strictly monotone functions that would preserve the ordering on every axis.
- It concerns loss of ordering information between incomparable profiles. It does not say that a score chosen for a stated application is wrong for that application.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A conditional theorem with a proof that leans on the benchmark data for one step. The crossing profiles it is applied to are measurements on five models.

## first stated

Theorem 13.1, [`geometric-reasoning/chapters/ch13_five_convergent_measurements.md:449-457`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch13_five_convergent_measurements.md#L449-L457), stated informally in Section 13.6, [`geometric-reasoning/chapters/ch13_five_convergent_measurements.md:280-282`](https://github.com/ahb-sjsu/geometric-reasoning/blob/881f075/chapters/ch13_five_convergent_measurements.md#L280-L282). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch13_five_convergent_measurements.html).

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

pareto-dominance, model-robustness-profile, metacognitive-plane, aggregation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
