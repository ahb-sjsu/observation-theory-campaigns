# coupling null

**id.** coupling-null
**kind.** concept

## definition

The case, alignment near one, in which the read subspace and the high-variance subspace coincide and the reconstruction-optimal code is also the read-preserving one. The flip's stated boundary. Chapter 4.

## equation

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

## ledger

- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 7d91883.
- GO-B-optim-D4 (034 · D4). Optimization — gradient compression, curvature (Hessian) read operator, on a REAL model (logistic regression); optional stretch `[predicted]`. `geometric-observation/claims/LEDGER.md:122` at 7d91883.

## first stated

Volume 14, chapter 8, `geometric-observation/chapters/ch08_value.md:108-116`, the gradient-compression case, and chapter 12 for the alignment dial, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.4 | gradient compression anti 300 of 300, flip 27 percent, coupling boundary | `geometric-observation\chapters\ch08_value.md:108-116` |
| chapter 4 section 4.4 | alignment law, retrospective fit exploratory, one prospective point | `geometric-observation\chapters\ch12_failure_taxonomy_and_kappa.md:56-82` |
| chapter 7 section 7.2 | real logistic model, exact Hessian, anti 300 of 300, flip 82 of 300, coupling diagnosis, bound not refutation | `geometric-observation\claims\LEDGER.md` row GO-B-optim-D4 |

## failures and corrections

none

## conditions

- The coupling null is the case in which the read subspace and the high-variance subspace coincide, alignment near one, so that the reconstruction-optimal code is also the read-preserving one and no flip is possible.
- It is the flip's stated boundary, and a comparison that finds no flip there has confirmed the boundary rather than refuted the flip.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Alignment.lean`, theorems `overlap_sq_le`, `alignment_le_one`, `alignment_nonneg`, `alignment_eq_one_of_proportional`, `coupling_null`, at observation-data-mining 49fcb16.

## used in

*Data Mining as Observation* chapters 4.

## related

alignment, flip, read-distortion

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 27b21e4, theory-radar 37c4e6c, observation-data-mining 49fcb16, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
