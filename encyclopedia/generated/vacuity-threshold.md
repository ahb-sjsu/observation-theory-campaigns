# vacuity threshold

**id.** vacuity-threshold
**kind.** result

## definition

The value of a certificate's statistic below which the certificate is uninformative, derived from the problem rather than tuned to the data. Chapter 9.

## equation

Book equation 9.3.

    \hat\mu=\frac{\bar s_{\mathrm{true}}-\bar s_{\mathrm{distr}}}{\sigma_{\mathrm{distr}}},\qquad \mu_{\mathrm{crit}}=\mathbb E\Big[\max_{N-1}\mathcal N(0,1)\Big],\qquad \rho=\frac{\hat\mu}{\mu_{\mathrm{crit}}},\qquad \rho=1\ \text{vacuous}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 7d91883.

## first stated

Volume 14, the GO-3 registration and its notes, `geometric-observation/experiments/GO3-certificate-vacuity-v3-NOTES.md:1-60`, DOI 10.5281/zenodo.21776291, and chapter 9 section 9.3 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 9 section 9.3 | the margin certificate, mu crit as the expected maximum of N minus 1 standard normals, rho, death at 0.948 within 6 percent, Spearman 0.991 vs 0.873, fourteen corpora, six gates, the v1 to v3 path, the standing correction | `geometric-observation\experiments\GO3-certificate-vacuity-v3-NOTES.md:1-60`; `geometric-observation\claims\LEDGER.md` row GO-3 |

## failures and corrections

none

## conditions

- The threshold is derived from the problem, the expected maximum of the distractors' margins, and is not tuned to the data.
- A certificate at or below the threshold proves nothing about the object. It has not shown that no structure exists, only that this test could not certify one at this resolution.
- Tested under seal on retrieval, which is recognition with one candidate per query, and the transition has a finite width.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Vacuity.lean`, theorems `maxOver_mono`, `rho_eq_one_iff`, `rho_lt_one_of_lt`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 8, 9.

## related

certificate, rank-certificate, recognizer

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
