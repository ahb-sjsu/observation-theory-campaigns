# multiplet

**id.** multiplet
**kind.** concept

## definition

A group of eigenvalues that are equal or nearly so, whose pattern names the shape a dataset lies on. Chapter 9.

## equation

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 0.31.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}.

Book equation 9.2.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}\qquad\Rightarrow\qquad d=2\,\frac{d\log N}{d\log\lambda}.

## ledger

none

## first stated

Chapter 0 section 0.15 and chapter 9 section 9.2 of *Data Mining as Observation*, with the program's recognizer in `geometric-observation/chapters/ch11_the_recognizer.md:1-95`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 9 section 9.2 | the recognizer's mechanism, low multiplets and angular distances, dimension before shape by Weyl's law, refusal, the growth gotcha | `geometric-observation\chapters\ch11_the_recognizer.md:1-95` |
| chapter 9 section 9.2 | the battery, three new templates, frozen ratios, code hash, bars at least 10 of 12 and the dimension ordering, eccentricity scope | `the-angular-observer\PREREG_RECOGNIZER_BATTERY.md:1-80` |
| chapter 9 section 9.2 | 12 of 12, dimensions 1.81, 2.80, 1.74, angular Spearman ranges, eccentricity spreads, verdict confirmed, GO-P-2026-041 | `the-angular-observer\experiments\manifold-recovery\battery_result.json` |

## failures and corrections

none

## conditions

- A group of eigenvalues that are equal or nearly so, whose pattern names the shape a dataset lies on. The cycle's Laplacian eigenvalue at k equals the one at n minus k, so every eigenvalue of the discrete circle other than the constant mode and, for even n, the alternating mode appears twice.
- Symmetric shapes produce multiplets, the sphere in groups of three, five, seven, and a product of shapes has the product of their patterns. The recognizer reads the pattern of the lowest eigenvalues against stored templates and refuses when none matches.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Multiplet.lean`, theorems `cycleEig_zero`, `cycleEig_nonneg`, `cycleEig_le_four`, `cycleEig_pair`, `pair_distinct`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 9.

## related

laplacian, recognizer, manifold, weyls-law, eigenvalue-eigenvector

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
