# isotropic

**id.** isotropic
**kind.** concept

## definition

Of a covariance, having the same variance in every direction. Chapter 0.

## equation

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.

## first stated

Chapter 0 section 0.3 and chapter 3 section 3.2 of *Data Mining as Observation*, with the isotropic-Gaussian control of chapter 10.

## measurements

none

## failures and corrections

none

## conditions

- An isotropic covariance has the same variance in every direction, so every unit reader reads it the same and no flip is possible. An anisotropic one has different variances in different directions, and two unit readers can read it differently.
- The flip needs anisotropy. Two codes with the variances exchanged are read the same by every reader exactly when the two variances agree, which is the boundary the coupling null names from the other side.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Isotropy.lean`, theorems `isotropic_reads_same`, `isotropic_no_flip`, `anisotropic_readers_differ`, `flip_iff_anisotropic`, at observation-data-mining 51c193c.

## used in

*Data Mining as Observation* chapters 0, 2, 3, 4, 7, 9, 10, 11, 12.

## related

flip, coupling-null, covariance-matrix, alignment

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f206f90, theory-radar 37c4e6c, observation-data-mining 51c193c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
