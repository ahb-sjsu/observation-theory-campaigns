# Monte Carlo

**id.** monte-carlo
**kind.** concept

## definition

Estimating a probability or an expectation as the fraction or average over many simulated runs, a sample proportion with standard error the square root of p(1 minus p) over N. A null model run many times is one. Primer S, equation S.21.

**Example.** 17 of 100 runs show the event, so the estimate is 0.17 with standard error the square root of 0.17 times 0.83 over 100, which is 0.038.

## equation

Book equation S.21.

    \hat p=\frac{\#\text{runs with the event}}{N},\qquad \operatorname{SE}(\hat p)=\sqrt{\frac{\hat p(1-\hat p)}{N}}.

## conditions

none

## ledger

none

## first stated

Primer S section S.11 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

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

pseudo-random-generator, null-model, standard-error, permutation-test

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
