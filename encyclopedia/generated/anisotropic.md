# anisotropic

**id.** anisotropic
**kind.** concept

## definition

Of a covariance, having different variances in different directions. Chapter 0.

## equation

Book equation 0.5.

    \Sigma\,v_i=\lambda_i v_i,\qquad \Sigma=\sum_{i=1}^{d}\lambda_i\,v_i v_i^{\top},\qquad v_i\cdot v_j=0\ (i\ne j).

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

## ledger

- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 9f3829f.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 9f3829f.

## first stated

Chapter 0 section 0.4 of *Data Mining as Observation*, with the program's centring measurement in `geometric-observation/claims/LEDGER.md` row GO-B-legal and the anisotropy channel in `lebse/README.md:40-75`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 11 section 11.8 | 0.765 to 0.971 with interval 0.190 to 0.223, 0.545 to 0.562 with interval 0.004 to 0.031, v1 0.340 with interval negative 0.214 to negative 0.081, anisotropy 0.570 to 0.259 | `lebse\README.md:40-75`; `lebse\PAPER.md:1-15,60-66`; `lebse\MODEL_CARD.md:48-52` |
| chapter 12 section 12.3 | uncompressed 0.79, centred 0.84 | `geometric-observation\claims\LEDGER.md` row GO-B-legal |
| chapter 12 section 12.4 | 0.765 to 0.971, 0.545 to 0.562, v1 0.340, cosine 0.570 to 0.259 | `lebse\README.md:40-75`; `lebse\PAPER.md:1-15,60-66` |

## failures and corrections

none

## conditions

- Of a covariance, having different variances in different directions, which is to say unequal eigenvalues. Two readers at different angles to an anisotropic covariance read different variances, and the flip between two codes exists exactly when the covariance is anisotropic along the directions that separate them.
- Centring an embedding raised a ranker from 0.79 to 0.84 on the legal corpus, which is the condition under which a learned quotient and a variance quotient disagree most, and an isotropic control collapses the flip.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Isotropy.lean`, theorems `isotropic_reads_same`, `isotropic_no_flip`, `anisotropic_readers_differ`, `flip_iff_anisotropic`, at observation-data-mining f05f3e7.

## used in

*Data Mining as Observation* chapters 0, 3, 9, 11, 12.

## related

isotropic, covariance-matrix, spectrum, whitening, flip-the

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 398fb98, theory-radar 37c4e6c, observation-data-mining f05f3e7, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
