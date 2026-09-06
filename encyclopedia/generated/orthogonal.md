# orthogonal

**id.** orthogonal
**kind.** concept

## definition

Of two vectors, having dot product zero. The squared length of a sum of orthogonal vectors is the sum of the squared lengths. Chapter 0 section 0.1.

## equation

Book equation 0.1.

    x\cdot y=\sum_{i=1}^{d}x_i y_i,\qquad \|x\|=\sqrt{x\cdot x},\qquad \cos\theta=\frac{x\cdot y}{\|x\|\,\|y\|}.

Book equation 0.3.

    \Sigma_{ij}=\mathbb E\big[(x_i-\mu_i)(x_j-\mu_j)\big],\qquad \operatorname{tr}\Sigma=\sum_{i}\Sigma_{ii}.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 9f3829f.

## first stated

Chapter 0 section 0.1 and section 0.2 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |

## failures and corrections

none

## conditions

- Of two vectors, having dot product zero. The relation is symmetric, survives rescaling, holds between any vector and zero, the squared length of a sum of orthogonal vectors is the sum of the squared lengths, and the residual of a projection is orthogonal to the direction projected on.
- A linear classifier's nuisance is everything orthogonal to its weight vector, and the eigenvectors of a symmetric matrix with distinct eigenvalues are orthogonal, so the read subspace and the nuisance split every row.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Orthogonal.lean`, theorems `orth_symm`, `pythagoras`, `orth_smul`, `orth_zero`, `residual_orth`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 6, 9, 11, 12.

## related

dot-product, projection, eigenvalue-eigenvector, nuisance, read-subspace

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
