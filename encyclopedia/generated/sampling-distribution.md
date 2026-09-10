# sampling distribution

**id.** sampling-distribution
**kind.** concept

## definition

The distribution of a statistic across repeated samples of the same size, whose standard deviation is the statistic's standard error. The bootstrap estimates it from one sample. Primer S, equation S.11.

**Example.** The mean of eight values with standard deviation 2 has a sampling distribution with spread 0.707.

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

standard-error, bootstrap, central-limit-theorem, confidence-interval

## see also

none

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
