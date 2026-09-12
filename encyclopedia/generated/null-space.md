# null space

**id.** null-space
**kind.** concept

## definition

The set of vectors a matrix sends to zero, also called the kernel, the directions the matrix cannot see. Its dimension plus the rank is the number of columns. Primer L, equation L.7.

**Example.** Rows (1, 2) and (2, 4) send (2, -1) to zero, so the null space is the line of multiples of (2, -1), and 1 + 1 is the 2 columns.

## equation

Book equation L.7.

    \ker A=\{x:\ Ax=0\},\qquad \operatorname{rank}A+\dim\ker A=d.

## conditions

none

## ledger

none

## first stated

Primer L section L.4 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L.

## related

kernel, rank, quotient, column-space

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
