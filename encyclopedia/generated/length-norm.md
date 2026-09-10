# length, norm

**id.** length-norm
**kind.** concept

## definition

The square root of the sum of a vector's squared coordinates, Pythagoras in d dimensions, which is also the square root of the vector's dot product with itself. Primer L, equations L.2 and L.3.

**Example.** (1, 2, 2) has length the square root of 1 + 4 + 4, which is 3.

## equation

Book equation L.2.

    \|x\|=\sqrt{x_1^{2}+\cdots+x_d^{2}},\qquad u=\frac{x}{\|x\|},\qquad \|u\|=1.

Book equation L.3.

    x\cdot y=x^{\top}y=\sum_{i=1}^{d}x_i y_i,\qquad x\cdot x=\|x\|^{2}.

## conditions

none

## ledger

none

## first stated

Primer L section L.1 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primers L and S, chapters 0, 1, 2, 3, 4, 6, 10, 11, 12, 13.

## related

unit-vector, dot-product, euclidean-distance, frobenius-norm

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining a0db6a8; the commit of every record is listed in the encyclopedia's provenance.
