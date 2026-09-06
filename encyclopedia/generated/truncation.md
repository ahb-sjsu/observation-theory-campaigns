# truncation

**id.** truncation
**kind.** instrument

## definition

Keeping the first k components of a spectrum and dropping the rest, a bet that the consumer reads the top of the spectrum. Chapter 4 section 4.5.

## equation

Book equation 4.2.

    D(b)=\sum_i s_i\sigma_i^{2}\,2^{-2b_i},\qquad s_i=v_i^{\top}P_C\,v_i,\qquad b_i^{\star}=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i\sigma_i^{2}}{\theta}\Big),\qquad \sum_i b_i^{\star}=B,

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## ledger

- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 9f3829f.

## first stated

Chapter 4 section 4.5 of *Data Mining as Observation*, with the truncation claim in `turboquant-pro/CLAIMS.md:28-49` and the GloVe table in `turboquant-pro/benchmarks/RESULTS_glove.md:1-40`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.5 | GloVe table, 73 percent at 64 components, 0.685 vs 0.862 and 0.866, 0.906 at matched bytes, 0.989 at 37 bytes, 768 to 256 keeps about 99 percent, the 95 percent rule | `turboquant-pro\benchmarks\RESULTS_glove.md:1-40` |
| chapter 4 section 4.5 | truncation claim reproducible, loses on compact sets | `turboquant-pro\CLAIMS.md:28-49` |
| chapter 11 section 11.5 | 9.6x at recall 0.999 CI-gated on GloVe 1.18M; 32x at 0.9993 on private 199k LaBSE, ties OPQ, beats RaBitQ, 20x build; 27.7x and 114x reported; PCA truncation loses on compact sets; 20x at 199k and 4x at 1M over OPQ; RaBitQ builds in under a second | `turboquant-pro\CLAIMS.md:28-49` |

## failures and corrections

none

## conditions

- Keeping the first k components of a spectrum and dropping the rest. The variance kept grows with k and reaches one at full rank, and the error is the sum of the dropped eigenvalues, so truncation is a bet that the consumer reads the top of the spectrum.
- Truncation to 64 components kept 73 percent of GloVe's variance and lost 0.685 against 0.862 downstream, is reproducible, and loses on compact sets.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PCA.lean`, theorems `varAlong_basis`, `varAlong_le`, `varAlong_ge`, `dropped_eq`, `dropped_nonneg`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/ExplainedVariance.lean`, theorems `explained_mem_unit`, `explained_mono`, `explained_full`, `retained_identity`, `retained_example`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 4, 11.

## related

principal-component-analysis, explained-variance, budget, spectrum, concentrated

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
