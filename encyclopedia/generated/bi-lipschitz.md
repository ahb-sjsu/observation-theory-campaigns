# bi-Lipschitz

**id.** bi-lipschitz
**kind.** concept

## definition

Of a map between two spaces, neither stretching nor shrinking any distance by more than a fixed factor. Equation 0.21.

## equation

Book equation 0.21.

    \frac1K\,d(x,y)\ \le\ d'\big(f(x),f(y)\big)\ \le\ K\,d(x,y)\qquad\text{for all }x,y.

## ledger

- NEG-16 (KV serving, end-task). *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task. `[refuted]`. `geometric-observation/claims/LEDGER.md:92` at 7d91883.
- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 7d91883.
- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 7d91883.
- NEG-10. (prospective) The consumer-driven reconstruction-blind flip appears on any independent representation, e.g. embedding retrieval. `[refuted]`. `geometric-observation/claims/LEDGER.md:103` at 7d91883.
- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.
- NEG-12. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction. `[refuted]`. `geometric-observation/claims/LEDGER.md:105` at 7d91883.
- NEG-13 → resolved. (GO-P-2026-026, prospective, real LLM) Appendix-E's omission floor is a rate-irreducible downstream wall on trained Llama read operators. `[missed]`. `geometric-observation/claims/LEDGER.md:106` at 7d91883.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.

## first stated

Chapter 0 section 0.10 of *Data Mining as Observation*, with the refuted uniform bi-Lipschitz claim for the commute filter in Volume 14's honest negatives, ledger row NEG-1.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 3 section 3.3 | row normalization is the projection onto the read subspace of the geodesic-rank consumer | `geometric-observation\chapters\ch09_legibility.md:31-41`; `geometric-observation\chapters\ch03_historical_precursors.md:98-110` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |

## failures and corrections

- NEG-16 (KV serving, end-task), `[refuted]`. *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task.
- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.
- NEG-10, `[refuted]`. (prospective) The consumer-driven reconstruction-blind flip appears on any independent representation, e.g. embedding retrieval.
- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.
- NEG-12, `[refuted]`. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction.
- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- A map is bi-Lipschitz with factor K when it neither stretches nor shrinks any distance by more than K. The factor is at least one, compositions multiply the factors, and the map preserves a nearest neighbour whenever the runner-up is more than K squared times as far, the rank certificate's per-pair fact.
- It does not preserve every ordering, so it is not rank-faithful, and the program's fixed-scale uniform bi-Lipschitz claim for the commute filter is refuted and carried in the ledger.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/BiLipschitz.lean`, theorems `one_le_factor`, `within_comp`, `nn_preserved`, `not_rank_faithful`, at observation-data-mining 81ea18c.

## used in

*Data Mining as Observation* chapters 0, 3.

## related

rank-faithful, rank-certificate, recognizer, quotient

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 1aa8775, theory-radar 37c4e6c, observation-data-mining 81ea18c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
