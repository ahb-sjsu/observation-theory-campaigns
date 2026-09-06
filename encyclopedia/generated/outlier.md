# outlier

**id.** outlier
**kind.** concept

## definition

A row the reader cannot place. The statistical detector calls a row an outlier when its distance from the mean in units of spread passes a threshold, and no more than one over the threshold squared of the weight can. Chapter 10.

## equation

Book equation 0.33.

    d_M(x)=\sqrt{(x-\mu)^{\top}\Sigma^{-1}(x-\mu)}.

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

Book equation 0.6.

    x_{\mathrm w}=\Sigma^{-1/2}(x-\mu),\qquad \Sigma^{-1/2}=\sum_i\lambda_i^{-1/2}\,v_i v_i^{\top}.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 0 section 0.16 and chapter 10 section 10.1 of *Data Mining as Observation*, after TSK chapter 9, with the hierarchical typing in `turboquant-pro/turboquant_pro/anatomy.py:98-170`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.1 | the four detector families | TSK 2e chapter 9 |
| chapter 10 section 10.3 | hierarchical typing, tails 0.95 and 0.85, prescriptions, two designs that died, correlation above 0.8 on an isotropic Gaussian | `turboquant-pro\turboquant_pro\anatomy.py:98-170` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- A row the reader cannot place. The statistical detector scores a row by its distance from the mean in units of spread, which is zero at the mean, unchanged when data, mean, and spread are rescaled and shifted together, and past a threshold t exactly when the row lies more than t spreads from the mean. By Chebyshev the weight of rows beyond t is at most the mean squared score over t squared.
- The four detector families read different coordinates, distance from the mean, distance to neighbours, density relative to neighbours, and cluster membership, and the observer's outliers, the anti-hubs, are the rows no detector of the data alone can see.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Outlier.lean`, theorems `zscore_mean`, `zscore_affine`, `outlier_iff`, `zscore_reflect`, `chebyshev`, at observation-data-mining f05f3e7.

`lean/DataMiningAsObservation/Mahalanobis.lean`, theorems `dM2_nonneg`, `dM2_mean`, `dM2_scale`, `dM2_eq_whitened`, `dM2_antitone_in_variance`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 2, 3, 10.

## related

mahalanobis-distance, anti-hub, abstention, whitening, density

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
