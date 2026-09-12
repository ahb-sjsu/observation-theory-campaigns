# singular value

**id.** singular-value
**kind.** concept

## definition

The size of one rank-one term of the singular value decomposition, the square root of an eigenvalue of A transposed A. The count of nonzero ones is the rank, and their squares sum to the squared Frobenius norm. Primer L, equations L.17 and L.18.

**Example.** Rows (1, 2) and (2, 4) have singular values 5 and 0, so the rank is one.

## equation

Book equation L.17.

    A^{\top}A\,v_i=\sigma_i^{2}\,v_i,\qquad u_i=\frac{Av_i}{\sigma_i},\qquad \Sigma=\frac{A^{\top}A}{n}\ \text{for centered } A.

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

*Data Mining as Observation* primer L, chapters 0, 9.

## related

singular-value-decomposition, rank, frobenius-norm, spectrum

## see also

none

## status

Generated 2026-09-12 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
