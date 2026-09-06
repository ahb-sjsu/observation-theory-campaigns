# paired

**id.** paired
**kind.** instrument

## definition

Of a comparison, made on the same rows or seeds for both arms. Pairing helps exactly when the two arms covary. Chapter 0 section 0.9.

## equation

Book equation 0.18.

    \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2},\qquad \frac{\widehat{\operatorname{Var}}_{\mathrm{NB}}}{\hat\sigma^{2}/J}=1+J\,\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}.

Book equation 8.2.

    \begin{gathered} \widehat{\operatorname{Var}}_{\mathrm{NB}}=\Big(\frac1J+\frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}\Big)\hat\sigma^{2}, \\ J=1000,\ \frac{n_{\mathrm{test}}}{n_{\mathrm{train}}}=\frac14\ \Rightarrow\ 1+250=251,\ \ \sqrt{251}=15.84. \end{gathered}

Book equation 0.29.

    \mathrm{ECE}=\sum_b\frac{n_b}{n}\,\big|\bar s_b-\bar y_b\big|.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.
- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 9f3829f.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 9f3829f.

## first stated

Chapter 0 section 0.9 and chapter 8 section 8.4 of *Data Mining as Observation*, with the paired null in `readscope/SPEC.md:806-857`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.4 | C-11c paired null, rank 2 positional 0.385 vs null 0.572, 0.615 vs 0.224, 14 of 16 cells, scope 16 cells one 3B model 192 positions | `readscope\SPEC.md:806-857`; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.8 | 0.765 to 0.971 with interval 0.190 to 0.223, 0.545 to 0.562 with interval 0.004 to 0.031, v1 0.340 with interval negative 0.214 to negative 0.081, anisotropy 0.570 to 0.259 | `lebse\README.md:40-75`; `lebse\PAPER.md:1-15,60-66`; `lebse\MODEL_CARD.md:48-52` |
| chapter 12 section 12.4 | 0.765 to 0.971, 0.545 to 0.562, v1 0.340, cosine 0.570 to 0.259 | `lebse\README.md:40-75`; `lebse\PAPER.md:1-15,60-66` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- Of a comparison, made on the same rows or the same seeds for both arms, so that the difference is scored row by row. The variance of the difference is the sum of the variances less twice the covariance, so pairing helps exactly when the two arms covary.
- The paired null at rank two read 0.385 against 0.572 on fourteen of sixteen cells, and the encoder comparisons carry a paired bootstrap interval on each relation.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bootstrap.lean`, theorems `mean_sub`, `var_sub`, `paired_lt_iff`, `cov_comm`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 4, 6, 8, 11, 12.

## related

bootstrap, confidence-interval, seed, standard-error, control

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
