# low-rank approximation

**id.** low-rank-approximation
**kind.** concept

## definition

The best approximation of a matrix by one of rank k in total squared error keeps the first k terms of its singular value decomposition, and the error is the sum of the squared singular values dropped, the Eckart and Young theorem. It is the identity reader's best approximation, and chapter 4 is about consumers for which it is not the best. Primer L, equation L.18.

**Example.** Keeping only the root 3 term of the three by two example leaves squared error 1, one quarter of the total.

## equation

Book equation L.18.

    \|A\|_F^{2}=\sum_{i,j}A_{ij}^{2}=\sum_i\sigma_i^{2},\qquad \min_{\operatorname{rank}B\le k}\|A-B\|_F^{2}=\sum_{i>k}\sigma_i^{2}.

## conditions

none

## ledger

none

## first stated

Primer L section L.8 of *Data Mining as Observation*, added in draft 0.3 (2026-09-09) for the ECE 514 readers whose first courses are far behind. The idea is standard and TSK Appendix A covers it at length.

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Data Mining as Observation* primer L, chapters 6, 11.

## related

singular-value-decomposition, truncation, explained-variance, flip, identity-reader

## see also

none

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
