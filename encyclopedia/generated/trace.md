# trace

**id.** trace
**kind.** concept

## definition

The sum of a matrix's diagonal, which for a covariance is the total variance. Equation 0.3.

## equation

Book equation 0.3.

    \Sigma_{ij}=\mathbb E\big[(x_i-\mu_i)(x_j-\mu_j)\big],\qquad \operatorname{tr}\Sigma=\sum_{i}\Sigma_{ii}.

Book equation 0.10.

    d_O=\operatorname{tr}(P_C\,M_\delta)=\mathbb E\!\left[\delta^{\top}P_C\,\delta\right],\qquad M_\delta=\mathbb E\!\left[\delta\delta^{\top}\right],\qquad P_C=I\ \Rightarrow\ d_O=\operatorname{tr}M_\delta.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.
- OT-2. Loading is a covariance, not a distance: reading error under a change of measure is priced by ε·‖E[h·A]‖ — predicted from the base measure alone — and a full-magnitude shift orthogonal to the operator's variation does nothing. `[predicted]`. `geometric-observation/claims/LEDGER.md:33` at 9f3829f.

## first stated

Chapter 0 section 0.2 of *Data Mining as Observation*, with the trace pairing of Volume 14's invariance row OT-7.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |

## failures and corrections

none

## conditions

- The sum of a matrix's diagonal. It is linear, the trace of the identity is the dimension, the trace of an outer product is the vector's squared length, the trace of a product does not depend on the order, and the trace of a read operator times a rank-one error is the read distortion of that error.
- For a covariance the trace is the total variance, and the trace pairing of a read operator with a second moment is the invariant the ledger's row OT-7 names, unchanged by a change of basis where the spectrum and effective rank are not.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Trace.lean`, theorems `trace_add`, `trace_smul`, `trace_one`, `trace_vecMulVec`, `trace_mul_comm`, `trace_read`, `trace_identity_read`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 4, 13.

## related

covariance-matrix, read-distortion, identity-reader, effective-rank

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
