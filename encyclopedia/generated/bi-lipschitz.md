# bi-Lipschitz

**id.** bi-lipschitz
**kind.** concept

## definition

Of a map between two spaces, neither stretching nor shrinking any distance by more than a fixed factor. Equation 0.21.

## equation

Book equation 0.21.

    \frac1K\,d(x,y)\ \le\ d'\big(f(x),f(y)\big)\ \le\ K\,d(x,y)\qquad\text{for all }x,y.

## ledger

- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 9f3829f.

## first stated

Chapter 0 section 0.10 of *Data Mining as Observation*, with the refuted uniform bi-Lipschitz claim for the commute filter in Volume 14's honest negatives, ledger row NEG-1.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 3 section 3.3 | row normalization is the projection onto the read subspace of the geodesic-rank consumer | `geometric-observation\chapters\ch09_legibility.md:31-41`; `geometric-observation\chapters\ch03_historical_precursors.md:98-110` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.

## conditions

- A map is bi-Lipschitz with factor K when it neither stretches nor shrinks any distance by more than K. The factor is at least one, compositions multiply the factors, and the map preserves a nearest neighbour whenever the runner-up is more than K squared times as far, the rank certificate's per-pair fact.
- It does not preserve every ordering, so it is not rank-faithful, and the program's fixed-scale uniform bi-Lipschitz claim for the commute filter is refuted and carried in the ledger.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/BiLipschitz.lean`, theorems `one_le_factor`, `within_comp`, `nn_preserved`, `not_rank_faithful`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 3.

## related

rank-faithful, rank-certificate, recognizer, quotient

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
