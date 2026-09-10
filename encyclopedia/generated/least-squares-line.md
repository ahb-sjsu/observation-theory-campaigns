# least-squares line

**id.** least-squares-line
**kind.** concept

## definition

The straight line predicting one column from another that minimizes the sum of squared vertical errors, with slope the covariance over the variance of the predictor, passing through the two means, and accounting for r squared of the variance. Primer S, equation S.13.

**Example.** x = (1, 2, 3, 4, 5) and y = (2, 4, 5, 4, 5) give slope 0.6, intercept 2.2, and r squared 0.6.

## equation

Book equation S.13.

    \hat y=a+b\,x,\qquad b=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)},\qquad a=\bar y-b\,\bar x,\qquad r^{2}=\frac{\text{variance explained}}{\text{variance of }Y}.

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

*Data Mining as Observation* primer S, chapters 6.

## related

correlation, covariance, residual, explained-variance

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
