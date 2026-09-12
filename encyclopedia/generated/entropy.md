# entropy

**id.** entropy
**kind.** concept

## definition

The expected surprise of a distribution, the bits needed per outcome under the best code, at most the log base two of the number of outcomes. Primer S, equation S.19.

**Example.** A fair die has entropy log2 of 6, about 2.585 bits, and (0.5, 0.25, 0.25) has 1.5 bits.

## equation

Book equation S.19.

    H(p)=-\sum_i p_i\log_2 p_i.

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

surprise, cross-entropy, kl-divergence, perplexity, bit

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
