# alignment

**id.** alignment
**kind.** concept

## definition

The normalized overlap between a consumer's average read operator and the covariance of the data on the read subspace, written kappa, between zero and one. Near one the read subspace and the high-variance subspace coincide and no flip is possible. Chapter 4, equation 4.6.

## equation

Book equation 4.6.

    \kappa=\operatorname{tr}\big(\bar P_C\,\bar\Sigma_x\big)\in[0,1],\qquad \kappa\to1\ \text{is the coupling null (no flip)}.

## ledger

- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 7d91883.

## first stated

Volume 14, chapter 12, `geometric-observation/chapters/ch12_failure_taxonomy_and_kappa.md:56-82`, DOI 10.5281/zenodo.21776291, where the alignment law is a retrospective fit carried as exploratory with one prospective point.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.4 | alignment law, retrospective fit exploratory, one prospective point | `geometric-observation\chapters\ch12_failure_taxonomy_and_kappa.md:56-82` |
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |

## failures and corrections

none

## conditions

- Defined as the normalized overlap between the averaged read operator and the source covariance on the read subspace, between zero and one, and so a statement about one workload.
- The alignment law that relates it to the size of the flip is a retrospective fit with a single prospective point and is carried as exploratory, not as a theorem.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Alignment.lean`, theorems `overlap_sq_le`, `alignment_le_one`, `alignment_nonneg`, `alignment_eq_one_of_proportional`, `coupling_null`, at observation-data-mining 7aab08c.

## used in

*Data Mining as Observation* chapters 2, 4, 7, 11, 14.

## related

flip, read-distortion, coupling-null, water-filling

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 92c643b, theory-radar 37c4e6c, observation-data-mining 7aab08c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
