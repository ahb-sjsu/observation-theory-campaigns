# covariance matrix

**id.** covariance-matrix
**kind.** concept

## definition

The matrix of pairwise covariances of a set of rows, whose trace is the total variance. Equation 0.3.

## equation

Book equation 0.3.

    \Sigma_{ij}=\mathbb E\big[(x_i-\mu_i)(x_j-\mu_j)\big],\qquad \operatorname{tr}\Sigma=\sum_{i}\Sigma_{ii}.

Book equation 0.4.

    \operatorname{Var}(u\cdot x)=u^{\top}\Sigma\,u.

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 7d91883.
- OT-2. Loading is a covariance, not a distance: reading error under a change of measure is priced by ε·‖E[h·A]‖ — predicted from the base measure alone — and a full-magnitude shift orthogonal to the operator's variation does nothing. `[predicted]`. `geometric-observation/claims/LEDGER.md:33` at 7d91883.

## first stated

Chapter 0 section 0.2 of *Data Mining as Observation*, paired with the read operator in chapter 4, and Volume 14 chapter 5, `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.2 | read subspace small, operator local, pullback composition, rank cannot increase | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:7-48`; `geometric-observation\chapters\ch06_mathematical_preliminaries.md:10-27` |
| chapter 2 section 2.2 | read distortion controls but is not a complete rank statistic, twelve of twelve, one middle pair misordered, NEG-9 | `geometric-observation\chapters\ch05_the_read_metric_and_the_quotient.md:49-75` |
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 4 section 4.2 | allocation report, gain over uniform, concentration caution below effective rank 2 | `turboquant-pro\turboquant_pro\read_allocation.py:244-307` |

## failures and corrections

none

## conditions

- The weighted average of the centred rows' outer products, the same construction as the read operator with the centred row in place of the sensitivity. Its quadratic form along a unit direction is the variance of the projection onto it, its trace is the total variance, and it is positive semidefinite.
- Chapter 4 pairs it with the read operator in one basis. Where the two are proportional there is no flip, and where they are not the water-filling allocation reads both.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Covariance.lean`, theorems `var_eq_quad`, `trace_eq_total`, `quad_nonneg`, `cov_symm`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 9, 10, 11, 12.

## related

read-operator, whitening, water-filling, alignment, explained-variance

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
