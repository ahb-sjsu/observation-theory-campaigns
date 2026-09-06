# percentile

**id.** percentile
**kind.** concept

## definition

The value below which a given fraction of the rows fall. The fraction at or below a value is nondecreasing in the value. Chapter 11 section 11.3.

## equation

Book equation 11.2.

    \begin{gathered} r=\frac{d_{\mathrm{compressed}}}{d_{\mathrm{exact}}},\qquad \kappa_{\text{strict}}=\frac{\max r}{\min r},\qquad \tau\ \ge\ 1-2\hat\mu(\kappa_{\text{strict}}),\qquad \rho_S\ \ge\ 1-3\hat\mu(\kappa_{\text{strict}}), \\ \kappa_{97.5/2.5}=\frac{q_{97.5}(r)}{q_{2.5}(r)}\ \text{ gives the same two expressions as estimates, not floors.} \end{gathered}

Book equation 0.35.

    \mathrm{RH}=\sum_i\max\!\Big(0,\ \frac{N_i}{\sum_j N_j}-\frac1n\Big).

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

## ledger

- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 9f3829f.

## first stated

Chapter 11 section 11.3 of *Data Mining as Observation*, with the percentile setting of the rank certificate in `turboquant-pro/turboquant_pro`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 10 section 10.2 | anti-hubs as where compressed indexes fail first, aggregate recall barely moves | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 10 section 10.3 | hierarchical typing, tails 0.95 and 0.85, prescriptions, two designs that died, correlation above 0.8 on an isotropic Gaussian | `turboquant-pro\turboquant_pro\anatomy.py:98-170` |
| chapter 11 section 11.2 | the calibration-time probe and the streaming monitor | `turboquant-pro\turboquant_pro\a2_probe.py:315-438`; `turboquant-pro\tests\test_a2_probe.py` |
| chapter 11 section 11.6 | anti-hub recall, p05, hub-rank correlation, hub-set overlap, the build gate | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The value below which a given fraction of the rows fall. The fraction at or below a value is nonnegative, at most one, nondecreasing in the value, one at or above the largest row and zero below the smallest, and an upper percentile over a lower one is at least one.
- The rank certificate's percentile setting reads the 97.5 over 2.5 percentile ratio as a robust estimate where the strict setting reads the max over min, and the anti-hub gate reads the fifth percentile of recall.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Percentile.lean`, theorems `cdf_nonneg`, `cdf_le_one`, `cdf_mono`, `cdf_of_all`, `cdf_of_none`, `ratio_ge_one`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 3, 10, 11.

## related

rank-certificate, anti-hub-recall, skewness, threshold, robin-hood-index

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
