# Poisson distribution

**id.** poisson-distribution
**kind.** concept

## definition

The distribution of a count of rare events, the limit of the binomial when n is large and p small with np held at mu, with mean and variance both mu. It is the null under which retrieval slots are handed out at random, and the Poisson ceiling is its tail. Primer S, equation S.7.

**Example.** With mean 0.1 the probability of a count of three or more is 0.000155, which times fifty thousand points is 7.7.

## equation

Book equation S.7.

    \Pr[X=k]=e^{-\mu}\frac{\mu^{k}}{k!},\qquad \mathbb E[X]=\operatorname{Var}(X)=\mu.

## conditions

none

## ledger

none

## first stated

Primer S section S.3 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer S, chapters 0, 3, 5.

## related

poisson-ceiling, bernoulli-binomial, null-model, hub

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
