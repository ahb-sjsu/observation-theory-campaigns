# drift

**id.** drift
**kind.** concept

## definition

A change over time in what a consumer reads or in the data it reads. Chapter 8 tests a drift claim against its null and finds half of it was noise.

## equation

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

Book equation 0.10.

    d_O=\operatorname{tr}(P_C\,M_\delta)=\mathbb E\!\left[\delta^{\top}P_C\,\delta\right],\qquad M_\delta=\mathbb E\!\left[\delta\delta^{\top}\right],\qquad P_C=I\ \Rightarrow\ d_O=\operatorname{tr}M_\delta.

## ledger

- OT-4. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it. `[refuted]`. `geometric-observation/claims/LEDGER.md:36` at 7d91883.
- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 7d91883.

## first stated

Volume 14, chapter 19, `geometric-observation/chapters/ch19_the_certificate_that_ages.md`, DOI 10.5281/zenodo.21776291, and the operator-drift record in readscope, `readscope/calibration/records/c11c-operator-drift.json`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.4 | C-11c paired null, rank 2 positional 0.385 vs null 0.572, 0.615 vs 0.224, 14 of 16 cells, scope 16 cells one 3B model 192 positions | `readscope\SPEC.md:806-857`; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.9 | drift at rank one 0.667 vs null 0.933, sixteen cells | `readscope\CALIBRATION.md:600-660` F-24; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.9 | C-12 four bars, 40 documents, 512 tokens, 13.4 point difference, teacher forcing removes it, negative 0.015 vs 0.005, Spearman negative 0.13 at p 0.45, sign test p 0.42, verdict FAIL, feedback compounding | `readscope\calibration\records\c12-longgen-drift-sym.json`; `readscope\calibration\DECLARATION-C12.md` at commit `90e2ce2`; `readscope\SPEC.md:806-825` |
| chapter 13 section 13.2 | the grammar, certificate, witness, refresh floor, false-clear rate, vacuity, the witness table | `geometric-observation\chapters\ch19_the_certificate_that_ages.md:1-95`; `observation-theory-campaigns\experiments\FRESHNESS-PROGRAM.md:1-40` |

## failures and corrections

- OT-4, `[refuted]`. Operator drift predicts a real long-generation degradation and a derived refresh intervention moves it.

## conditions

- A drift is a change over time in what a consumer reads or in the data it reads, and its damage is the read distortion of the drift, so it is consumer-relative. The same drift is read as its full squared size by one consumer and as nothing by another, and a drift confined to the nuisance is read as zero however large.
- The operator-drift claim was tested against a paired null and half of it was noise. The rank-one drift held in fourteen of sixteen cells on one model, and the refresh intervention derived from it was refuted, which the ledger carries.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Drift.lean`, theorems `damage_rank_one`, `same_drift_two_consumers`, `damage_eq_zero_of_nuisance`, `damage_nonneg`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 2, 8, 11, 13, 14.

## related

coherence-time, freshness, certificate, read-distortion

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
