# Mahalanobis distance

**id.** mahalanobis-distance
**kind.** concept

## definition

The Euclidean distance of a row from the mean after whitening. Equation 0.33.

## equation

Book equation 0.33.

    d_M(x)=\sqrt{(x-\mu)^{\top}\Sigma^{-1}(x-\mu)}.

Book equation 10.1.

    z(x)=\frac{x-\mu}{\sigma},\qquad d_M(x)^{2}=(x-\mu)^{\top}\Sigma^{-1}(x-\mu)=\sum_i\frac{(v_i\cdot(x-\mu))^{2}}{\lambda_i}.

## ledger

none

## first stated

Mahalanobis, on the generalised distance in statistics, 1936, as chapter 0 section 0.16 states it, and chapter 10 section 10.1 of *Data Mining as Observation*, where the statistical detector is the identity reader on whitened data.

## measurements

none

## failures and corrections

none

## conditions

- The Euclidean distance of a row from the mean after whitening. In the eigenbasis its square is the sum of the squared centred coordinates over the eigenvalues, nonnegative, zero at the mean, unchanged when data and covariance are rescaled together, and a deviation along a direction of larger variance counts for less.
- The detector that scores by it treats every whitened direction equally, so it is the identity reader on whitened data, and a consumer that reads a subspace calls different rows outliers.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Mahalanobis.lean`, theorems `dM2_nonneg`, `dM2_mean`, `dM2_scale`, `dM2_eq_whitened`, `dM2_antitone_in_variance`, at observation-data-mining 2b00d80.

## used in

*Data Mining as Observation* chapters 0, 10.

## related

whitening, identity-reader, hubness, abstention

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns e448a13, theory-radar 37c4e6c, observation-data-mining 2b00d80, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
