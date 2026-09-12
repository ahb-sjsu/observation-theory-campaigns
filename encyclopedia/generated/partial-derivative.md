# partial derivative

**id.** partial-derivative
**kind.** concept

## definition

The rate of change of a function of a vector when one coordinate moves and the others stay fixed. The gradient collects them. Primer L, equation L.19.

**Example.** For f(x) = x1 squared + 3 x1 x2 the partial derivatives are 2 x1 + 3 x2 and 3 x1.

## equation

Book equation L.19.

    \nabla f(x)=\Big(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_d}\Big),\qquad f(x+\delta)\approx f(x)+\nabla f(x)\cdot\delta.

## conditions

none

## ledger

none

## first stated

Primer L section L.9 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L, chapters 0.

## related

gradient, finite-difference

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
