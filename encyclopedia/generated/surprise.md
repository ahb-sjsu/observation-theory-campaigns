# surprise

**id.** surprise
**kind.** concept

## definition

Minus the log base two of an outcome's probability, its information in bits. Certainty carries none, a fair coin's outcome one bit, and one chance in eight three. Primer S, equation S.19.

**Example.** An outcome with probability one eighth carries 3 bits.

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

*Data Mining as Observation* primer S, chapters 5.

## related

entropy, bit

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
