# Bernoulli, binomial

**id.** bernoulli-binomial
**kind.** concept

## definition

A Bernoulli variable is one with probability p and zero otherwise, with mean p and variance p(1 minus p). A binomial variable counts the ones among n independent Bernoulli trials, with mean np. Primer S, equation S.6.

**Example.** Ten fair coin flips show exactly seven heads with probability 120 over 1024, about 0.117.

## equation

Book equation S.6.

    \Pr[X=k]=\binom{n}{k}p^{k}(1-p)^{n-k},\qquad \binom{n}{k}=\frac{n!}{k!\,(n-k)!},\qquad \mathbb E[X]=np.

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

*Data Mining as Observation* primer S.

## related

poisson-distribution, expectation, monte-carlo

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
