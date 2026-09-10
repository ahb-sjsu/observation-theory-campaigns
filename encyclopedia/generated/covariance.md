# covariance

**id.** covariance
**kind.** concept

## definition

The expectation of the product of two variables' deviations from their means, positive when they move together, the off-diagonal entry of the covariance matrix and the numerator of the correlation. Primer S, equation S.12.

**Example.** x = (1, 2, 3, 4, 5) and y = (2, 4, 5, 4, 5) have deviation products summing to 6, covariance 1.2 with n in the denominator.

## equation

Book equation S.12.

    \operatorname{Cov}(X,Y)=\mathbb E\big[(X-\mu_X)(Y-\mu_Y)\big],\qquad r=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}.

## conditions

none

## ledger

none

## first stated

Primer S section S.5 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primers L and S, chapters 0, 1, 2, 3, 4, 9, 10, 11, 12.

## related

covariance-matrix, correlation, variance, least-squares-line

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
