# explained variance

**id.** explained-variance
**kind.** concept

## definition

The fraction of total variance retained by a set of principal components, the identity reader's criterion for a reduction. Chapter 4.

## equation

Book equation 4.1.

    d_O=\operatorname{tr}(P_C\,M_\delta)\qquad\text{against}\qquad \operatorname{tr}M_\delta=d_O\big|_{P_C=I}.

Book equation 0.7.

    r_{\mathrm{eff}}=\frac{\big(\sum_i\lambda_i\big)^{2}}{\sum_i\lambda_i^{2}}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 8c6986b.

## first stated

TSK appendix B on principal component analysis, as chapter 4 section 4.1 of *Data Mining as Observation* reads it, the identity reader's criterion for a reduction, with the program's spectrum record in `gtc-prototype/docs/SPECTRUM_FINDINGS.md:10-18`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |
| chapter 14 section 14.3 | floor 0.08 to 0.12, balanced resample 3001 items, identity attack 0.237 with interval 0.20 to 0.28 on 289, sexual 0.204, threat 0.093 retracted, first pass 18 positives, 87.7 and 1.4 percent | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:20-64` |
| chapter 14 section 14.3 | contraction 0.779 to 0.863, 77 of 1600, 4.8 percent, 0.872 to 0.863, weight 2.69 | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:66-99` |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |
| chapter 14 section 14.7 | 51 percent moderated at 80 and 95 percent precision on the balanced set | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:84-88` |

## failures and corrections

none

## conditions

- The fraction of total variance the first k components carry. It lies in the unit interval, cannot fall as k grows, and reaches one at the full dimension. With unit sensitivities it is the fraction a consumer retains, which is why it is the identity reader's criterion.
- A consumer that reads other directions retains a different fraction. With variances 9 and 1 and a consumer reading only the second direction, keeping the first component explains nine tenths of the variance and none of what the consumer reads, which is the flip in its smallest form.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ExplainedVariance.lean`, theorems `explained_mem_unit`, `explained_mono`, `explained_full`, `retained_identity`, `retained_example`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 4, 8.

## related

identity-reader, flip, effective-rank, water-filling

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
