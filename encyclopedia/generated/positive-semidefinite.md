# positive semidefinite

**id.** positive-semidefinite
**kind.** concept

## definition

Of a symmetric matrix, having every quadratic form nonnegative, as the read operator and the covariance are. Chapter 0 section 0.3.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

Book equation 0.3.

    \Sigma_{ij}=\mathbb E\big[(x_i-\mu_i)(x_j-\mu_j)\big],\qquad \operatorname{tr}\Sigma=\sum_{i}\Sigma_{ii}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.

## first stated

Chapter 0 section 0.3 and section 0.5 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |

## failures and corrections

none

## conditions

- Of a symmetric matrix, having every quadratic form nonnegative. A sum of such matrices is one, a nonnegative multiple is one, an outer product of a vector with itself is one, the read operator is one whenever the weights are nonnegative, and the diagonal entries are nonnegative.
- The local metric on a consumer's output is positive semidefinite and exists only where the output metric has a local quadratic representation, and every eigenvalue of a positive semidefinite matrix is nonnegative.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PositiveSemidefinite.lean`, theorems `psd_add`, `psd_smul`, `psd_outer`, `psd_readOp`, `psd_diag_nonneg`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 2.

## related

read-operator, covariance-matrix, outer-product, eigenvalue-eigenvector, metric

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
