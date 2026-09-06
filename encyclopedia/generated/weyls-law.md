# Weyl's law

**id.** weyls-law
**kind.** concept

## definition

The rule for how the number of eigenvalues below a value grows with that value, whose exponent reveals the dimension of the space. Equation 0.31.

## equation

Book equation 0.31.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}.

Book equation 9.2.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}\qquad\Rightarrow\qquad d=2\,\frac{d\log N}{d\log\lambda}.

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 8c6986b.

## first stated

Weyl, 1911, as chapter 0 section 0.15 of *Data Mining as Observation* states it, with the program's dimension reading in `geometric-observation/chapters/ch11_the_recognizer.md:1-95`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 9 section 9.2 | the recognizer's mechanism, low multiplets and angular distances, dimension before shape by Weyl's law, refusal, the growth gotcha | `geometric-observation\chapters\ch11_the_recognizer.md:1-95` |
| chapter 9 section 9.2 | 12 of 12, dimensions 1.81, 2.80, 1.74, angular Spearman ranges, eccentricity spreads, verdict confirmed, GO-P-2026-041 | `the-angular-observer\experiments\manifold-recovery\battery_result.json` |

## failures and corrections

none

## conditions

- The rule that the number of eigenvalues below a value grows like that value to the power of half the dimension, so the dimension is in the exponent and is read from the slope of the count against the value on log axes. Doubling the value multiplies the count by two to the half dimension.
- Chapter 9 reads a dataset's dimension from its spectrum before reading its shape, and the recognizer's battery recovered dimensions of 1.81, 2.80, and 1.74 on three sealed templates. The finer geometry is in the constant and the multiplets, not the exponent.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/IntrinsicDimension.lean`, theorems `log_weyl`, `dimension_from_slope`, `weyl_double`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 9.

## related

intrinsic-dimension, manifold, laplacian, multiplet, recognizer

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
