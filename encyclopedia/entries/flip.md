# the flip

**id.** flip
**kind.** result

## definition

Fix a bit budget and build two codes for the same data, one that minimizes reconstruction
error and one that preserves the consumer's read subspace. The flip is the outcome in which
the read-preserving code scores better on the consumer's task while reconstructing worse,
and a third code built to destroy the read subspace, the anti arm, scores worst. Either
inequality alone is unremarkable. Together they say that preservation is a property of the
code and consumer as a pair, not of the code.

## equation

With task score task(·), error second-moment matrix Σ_δ, read operator P_C, and the two
codes O (read-preserving) and R (reconstruction-optimal), at matched bits,

    task(O) > task(R)  and  tr Σ_δ^O > tr Σ_δ^R,  and  task(anti) < task(R).

The read distortion tr(P_C Σ_δ) is the quantity that predicts the ordering. Book equation
4.3 states the flip, equation 0.10 the read distortion, and equation 3.1 the two-dimensional
case with the reader at 15 degrees, where the two readings are 1 ∓ 0.35√3.

## ledger

- GO-2 negative half, at matched bits downstream preservation is not controlled by
  reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.
- GO-2 positive half, downstream preservation is controlled by tr(P_C Σ_δ). `[replicated]`.
  `geometric-observation/claims/LEDGER.md:64` at 7d91883.
- GO-B-AV163, D3, 038, the acoustic, seismic, and whale battery rows. `[demonstrated]`.
  `geometric-observation/claims/LEDGER.md` at 7d91883.
- GO-4, budget inversion under matched budget, three seeds. `geometric-observation/claims/LEDGER.md` row GO-4.
- NEG-16, steering KV quantization error into the attention read subspace on a deployed-class
  model and LongBench. `[refuted]` for the end-task claim at its registered effect sizes, with
  the behavioural co-primary `[demonstrated]`. `geometric-observation/claims/LEDGER.md:92` at 7d91883.

## first stated

Volume 14, chapter 8, "value", `geometric-observation/chapters/ch08_value.md:1-30` at 7d91883,
DOI 10.5281/zenodo.21776291. The two-dimensional case is the cover and equation 3.1 of
*Data Mining as Observation*.

## measurements

| Cell | Numbers | Source |
|---|---|---|
| transformer attention keys, audit-matched bits | reconstruction 0.0934 vs 0.0938, task 2.53 times apart, direct read distortion predicts 12 of 12, anti arm worst 21 times | `geometric-observation/claims/LEDGER.md` rows GO-2, at 7d91883 |
| retrieval, matched clean | reconstruction 0.0964, negative half 4.70, positive half 4.65, reconstruction alone 0.40 | same rows |
| acoustic battery | 148 of 201 flips, anti worst 201 of 201, 152 of 201 | `geometric-observation/chapters/ch08_value.md:40-70` |
| seismic battery | 13 of 17, 17 of 17, 13 of 17, the code that reconstructs the seismogram better points at the wrong epicentre | same |
| sperm-whale clan classifier, 8718 codas | held-out AUROC 0.934 read-preserving vs 0.883 reconstruction-optimal, which reconstructed twice as well, anti worst 300 of 300 | same, and `geometric-observation/claims/LEDGER.md` row 038 |
| whitened code on whale, three budgets | 0.83, 0.85, 0.97 vs 0.41, 0.80, 0.89 | `geometric-observation/chapters/ch08_value.md:84-97` |
| gradient compression | anti worst 300 of 300, flip only 27 percent, the coupling boundary case | `geometric-observation/chapters/ch08_value.md:108-116` |
| the battery's sealed prediction | a flip in at least two of three core prospective domains, met, held in at least five domains and all three physics | `geometric-observation/chapters/ch08_value.md:40-70` |

## failures and corrections

- The first registered test missed two of four bars. The apparent reversal was a matched-bits
  confound, an uncounted per-block codebook adding about 25 percent to one arm. NEG-4 to
  NEG-10 and the reconstruction-matched precondition that came out of them.
  `geometric-observation/chapters/ch16_honest_negatives.md`.
- A prospective attempt on an independent representation found no flip, because one arm
  reconstructed strictly better and dominated downstream. The precondition is that the arms be
  matched on reconstruction before a flip can be recognized as one. Book chapter 4 section 4.6.
- NEG-16, refuted at its registered effect sizes on a deployed-class model and task. The
  behavioural co-primary held. The end-task claim did not.
- The direct read distortion nailed the discriminating flip twelve of twelve and still
  misordered one middle pair whose per-token error had structure the trace does not see. Book
  chapter 4 section 4.6.

## conditions

- Matched bits, and reconstruction matched or reported, for every comparison of two codes.
- A read operator misaligned with where the signal has its energy. The alignment
  κ = tr(P̄_C Σ̄_x) of book equation 4.6 is the dial. Near one, the coupling null, the
  reconstruction-optimal code is also the read-preserving one and no flip is possible.
  `geometric-observation/chapters/ch12_failure_taxonomy_and_kappa.md:56-82`, the retrospective
  fit `[exploratory]` with one prospective point.
- The read operator P_C is the average of local linearizations. For a nonlinear consumer the
  ordering it predicts is the ordering on average over the data.

## machine checked

The two-dimensional diagonal case, equal traces, opposite rankings for the readers at 15 and
75 degrees, and the readings 0.394 and 1.606 to three decimals.
`observation-data-mining/lean/DataMiningAsObservation/Flip.lean`, theorems `flip`,
`four_to_one_flip`, `readings_15_to_three_decimals`, built 2026-09-03 against Mathlib v4.32.2,
no `sorry`. The twelve-domain flip is a measurement and is not a theorem.

## used in

- *Data Mining as Observation* chapters 1, 3, 4, 6, and 11, and the cover.
- Volume 14 chapters 8, 12, and 16.
- turboquant-pro, the consumer-aware compression and the rank certificate, DOI 10.5281/zenodo.20660087.
- readscope, which recovers the read operator the prediction needs, PyPI `readscope`.

## related

read-distortion, alignment, anti-arm, rank-certificate, coupling-null

## status

Hand-filled 2026-09-03 from geometric-observation at 7d91883 and observation-data-mining at
a0b20ff. Not yet generated.
