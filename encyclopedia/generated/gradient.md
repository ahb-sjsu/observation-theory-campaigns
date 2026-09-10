# gradient

**id.** gradient
**kind.** concept

## definition

The vector of a function's partial derivatives, the direction of fastest increase, whose dot product with a small step is the first-order change in the function. The book calls the gradient of a consumer its sensitivity. Primer L, equations L.19 and L.20.

**Example.** f(x) = x1 squared + 3 x1 x2 has gradient (8, 3) at (1, 2), and a step of 0.01 along the first coordinate changes f by 0.0801.

## equation

Book equation L.19.

    \nabla f(x)=\Big(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_d}\Big),\qquad f(x+\delta)\approx f(x)+\nabla f(x)\cdot\delta.

Book equation L.20.

    \nabla(w\cdot x)=w,\qquad \nabla\|x\|^{2}=2x,\qquad \nabla\big(x^{\top}Ax\big)=2Ax,\qquad \nabla g(w\cdot x)=g'(w\cdot x)\,w.

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

*Data Mining as Observation* primer L, chapters 0, 4, 6, 7, 8, 11, 12, 14.

## related

sensitivity, partial-derivative, finite-difference, jacobian, read-operator

## see also

none

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
