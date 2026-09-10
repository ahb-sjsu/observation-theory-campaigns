# residual

**id.** residual
**kind.** concept

## definition

What is left of a vector after its projection is subtracted, orthogonal to the direction projected onto. In a regression, the vertical distance from a point to the fitted line. Primer L, equation L.9.

**Example.** Projecting (2, 3) onto (0.6, 0.8) leaves the residual (-0.16, 0.12), whose dot product with the direction is zero.

## equation

Book equation L.9.

    \operatorname{proj}_u(x)=(u\cdot x)\,u=\big(uu^{\top}\big)x,\qquad \big(x-\operatorname{proj}_u(x)\big)\cdot u=0.

## conditions

none

## ledger

none

## first stated

Primer L section L.5 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L, chapters 8, 12, 14.

## related

projection, orthogonal, least-squares-line

## see also

none

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
