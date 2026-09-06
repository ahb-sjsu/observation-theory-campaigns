# spectrum

**id.** spectrum
**kind.** concept

## definition

The list of a matrix's eigenvalues. Chapter 0 section 0.4.

## equation

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

Book equation 9.2.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}\qquad\Rightarrow\qquad d=2\,\frac{d\log N}{d\log\lambda}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 8c6986b.
- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 8c6986b.

## first stated

Chapter 0 section 0.4 of *Data Mining as Observation*, with the program's spectrum records in readscope, `readscope/readscope/spectrum.py:35-70`, and the recognizer battery.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |
| chapter 14 section 14.3 | floor 0.08 to 0.12, balanced resample 3001 items, identity attack 0.237 with interval 0.20 to 0.28 on 289, sexual 0.204, threat 0.093 retracted, first pass 18 positives, 87.7 and 1.4 percent | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:20-64` |
| chapter 14 section 14.3 | contraction 0.779 to 0.863, 77 of 1600, 4.8 percent, 0.872 to 0.863, weight 2.69 | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:66-99` |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |
| chapter 14 section 14.7 | 51 percent moderated at 80 and 95 percent precision on the balanced set | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:84-88` |

## failures and corrections

none

## conditions

- The list of a matrix's eigenvalues. Its effective rank, the square of its sum over the sum of its squares, lies between one and the dimension, is the dimension for a flat spectrum, and is one for a single eigenvalue.
- The spectrum is not invariant under a change of basis of the input where the trace pairing and the rank are, and the Laplacian's spectrum is what the recognizer reads for dimension and shape.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/EffectiveRank.lean`, theorems `sq_sum_le`, `effRank_le`, `sum_sq_le_sq_sum`, `one_le_effRank`, `effRank_const`, `effRank_single`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 9, 11, 14.

## related

eigenvalue-eigenvector, effective-rank, recognizer, laplacian, isotropic

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
