# read distortion

**id.** read-distortion
**kind.** concept

## definition

The error as a consumer experiences it, the trace of the read operator times the error's second-moment matrix, which is its covariance when the error is centered. For the identity reader it is mean squared error. Equation 0.10.

## equation

Book equation 0.10.

    d_O=\operatorname{tr}(P_C\,M_\delta)=\mathbb E\!\left[\delta^{\top}P_C\,\delta\right],\qquad M_\delta=\mathbb E\!\left[\delta\delta^{\top}\right],\qquad P_C=I\ \Rightarrow\ d_O=\operatorname{tr}M_\delta.

Book equation 1.2.

    d_O=\operatorname{tr}(P_C\,M_\delta),\qquad \big(d_O=\operatorname{tr}M_\delta\ \text{ for every admissible } M_\delta\big)\ \Longleftrightarrow\ P_C=I.

Book equation 4.1.

    d_O=\operatorname{tr}(P_C\,M_\delta)\qquad\text{against}\qquad \operatorname{tr}M_\delta=d_O\big|_{P_C=I}.

## ledger

- GO-2 (pos. half: consumer-projected covariance *controls*). Downstream preservation is controlled by the error covariance projected on the consumer's read subspace, tr(P_C·Σ_δ). `[replicated]`. `geometric-observation/claims/LEDGER.md:64` at 7d91883.

## first stated

Volume 14, chapter 5, `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:49-75`, DOI 10.5281/zenodo.21776291, and chapter 2 of the same volume for the failure of observer-free measurement.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.4 | the flip sealed in twelve domains and three physics, held in at least five domains and all three | `geometric-observation\chapters\ch08_value.md:40-70`; `geometric-observation\claims\LEDGER.md` rows GO-2, GO-B-AV163, D3, 038 |
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 4 section 4.3 | GO-2 0.0934 vs 0.0938, 2.53 times, 12 of 12, anti 21 times; retrieval 0.0964, negative 4.70 and positive 4.65, recon 0.40 | `geometric-observation\claims\LEDGER.md` rows GO-2 negative and positive halves |

## failures and corrections

none

## conditions

- Exact, with no centering, for a fixed read operator, which is the affine case. For a nonlinear consumer whose error depends on the row it is a first-order factorized surrogate, exact when the local operator and the error's outer product are uncorrelated across rows.
- The second-moment matrix of the error, not its covariance, unless the error is centered by construction.
- The trace of the second moment is the mean squared vector norm, which is the dimension times the per-coordinate mean squared error.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ReadDistortion.lean`, theorems `read_distortion`, `identity_reader`, `quad_one`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 1, 2, 4.

## related

flip, alignment, identity-reader, quotient

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
