# expectation

**id.** expectation
**kind.** concept

## definition

The average of a random variable's values weighted by their probabilities, its long-run average over repetitions, also called the mean. It is linear whether or not the variables are independent. Primer S, equations S.4 and S.5.

**Example.** A fair die has expectation (1 + 2 + 3 + 4 + 5 + 6)/6 = 3.5.

## equation

Book equation S.4.

    \mathbb E[X]=\sum_x x\,\Pr[X=x],\qquad \operatorname{Var}(X)=\mathbb E\big[(X-\mu)^{2}\big]=\mathbb E[X^{2}]-\mu^{2},\qquad \sigma=\sqrt{\operatorname{Var}(X)}.

Book equation S.5.

    \mathbb E[aX+bY]=a\,\mathbb E[X]+b\,\mathbb E[Y],\qquad \operatorname{Var}(aX+b)=a^{2}\operatorname{Var}(X),\qquad \operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)\ \text{if independent}.

## conditions

none

## ledger

none

## first stated

Primer S section S.2 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer S, chapters 9.

## related

random-variable, variance, mean-median, law-of-large-numbers

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
