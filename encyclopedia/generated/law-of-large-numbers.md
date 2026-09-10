# law of large numbers

**id.** law-of-large-numbers
**kind.** concept

## definition

The sample mean settles toward the expectation as the sample grows, its standard error falling with the square root of n, so that halving the error takes four times the data. Primer S, equation S.11.

**Example.** A standard error of 0.707 at n = 8 becomes 0.354 at n = 32.

## equation

Book equation S.11.

    \operatorname{SE}(\bar x)=\frac{\sigma}{\sqrt n},\qquad \frac{\bar x-\mu}{\sigma/\sqrt n}\ \approx\ \text{normal with mean } 0 \text{ and variance } 1.

## conditions

none

## ledger

none

## first stated

Primer S section S.4 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

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

expectation, standard-error, central-limit-theorem, monte-carlo

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
