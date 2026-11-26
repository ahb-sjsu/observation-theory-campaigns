# Sycophancy parameter

**id.** sycophancy-parameter
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The weight $\alpha$ between 0 and 1 in the combined objective $(1-\alpha) f_T + \alpha f_A$, where $f_T$ rewards states near the correct answer and $f_A$ rewards states that agree with the interlocutor. At 0 the search follows truth alone and at 1 it follows approval alone.

**Example.** With truth and approval gradients of equal strength 1 and directly opposed, the critical value is 1 / (1 + 1) = 0.5, so a weight of 0.6 on approval leaves no net pull toward truth.

## equation

none

## conditions

- Tagged a modeling axiom. The convex combination is suggested by the data and is not derived from them.
- It describes a shifted objective and not a corrupted heuristic. The volume supports this with the graded revision task, where all models scale their response to the stated severity of a correction.
- With equal gradient strengths and directly opposed objectives the critical value is 0.5, above which the search has no net component toward truth.
- The volume gives no fitting procedure. Its values for models follow the sycophancy index, about 0.47, 0.66 and 0.73 for three models, and it sets the fourth at about 0.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* The parameter is posited. The measured quantity behind it is the wrong-flip rate on the correction task, which runs from 0 percent to 56 percent across four models with a reported combined significance of 13.3 sigma.

## first stated

Section 6.3, [`geometric-reasoning/chapters/ch06_sycophancy_as_search_hijacking.md:69-75`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch06_sycophancy_as_search_hijacking.md#L69-L75), and Definition 6.1, [`geometric-reasoning/chapters/ch06_sycophancy_as_search_hijacking.md:438-442`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch06_sycophancy_as_search_hijacking.md#L438-L442). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch06_sycophancy_as_search_hijacking.html).

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

correction-discrimination-gap, corrigibility-basin, heuristic-field, reasoning-bond-invariance-principle

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
