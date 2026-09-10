# cross-entropy

**id.** cross-entropy
**kind.** concept

## definition

The expected bits per outcome when outcomes drawn from p are coded as if from a model q. Its excess over the entropy is the KL divergence, and perplexity is two to the power of the cross-entropy per token. Primer S, equation S.20.

**Example.** Coding (0.5, 0.25, 0.25) with the uniform model costs log2 of 3, about 1.585 bits, 0.085 more than its entropy.

## equation

Book equation S.20.

    H(p,q)=-\sum_i p_i\log_2 q_i,\qquad \mathrm{KL}(p\,\|\,q)=H(p,q)-H(p)=\sum_i p_i\log_2\frac{p_i}{q_i}\ \ge0.

## conditions

none

## ledger

none

## first stated

Primer S section S.10 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix C covers it at length.

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

entropy, kl-divergence, perplexity, likelihood

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
