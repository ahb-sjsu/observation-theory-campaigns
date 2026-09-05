# distance concentration

**id.** distance-concentration
**kind.** concept

## definition

The narrowing of the spread of pairwise distances as dimension grows, read in the book as the reader running out of resolution. Chapter 3.

## equation

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.

## first stated

The classical result on nearest neighbours in high dimension, as TSK chapter 2 presents it, and chapter 3 section 3.4 of *Data Mining as Observation*, where it is read as the reader running out of resolution.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |
| chapter 4 section 4.2 | allocation report, gain over uniform, concentration caution below effective rank 2 | `turboquant-pro\turboquant_pro\read_allocation.py:244-307` |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- When a squared distance is a sum of independent coordinate contributions with a common mean and variance, its relative spread is the variance over the dimension times the squared mean, which falls with the dimension and tends to zero. The independence is the model's assumption.
- The book reads the narrowing as a property of the reader, the identity reader on all coordinates, and not of the data. A consumer that reads a low-dimensional subspace does not see it, which is why the effective rank and not the ambient dimension is the number that matters.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/DistanceConcentration.lean`, theorems `relSpread_eq`, `relSpread_antitone`, `relSpread_tendsto_zero`, `exists_dim_relSpread_lt`, at observation-data-mining 43ea852.

## used in

*Data Mining as Observation* chapters 3.

## related

hubness, effective-rank, read-subspace, rank-certificate

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 97b2015, theory-radar 37c4e6c, observation-data-mining 43ea852, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
