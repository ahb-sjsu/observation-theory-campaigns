# preregistration

**id.** preregistration
**kind.** instrument

## definition

Committing the hypothesis, the bar, and the analysis before the measurement is run, so that the record shows what was predicted. Chapter 8.

## equation

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- OT-7. The damage form, trace pairing, rank, and loading covariance are GL(d)-invariant under `P' = A⁻ᵀPA⁻¹`, while spectrum, effective rank, principal angles, and water-filling are O(d)-only — consumer-weighted damage is a geometric scalar, and P3's cliff cannot be bought down by reparameterization. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:30` at 7d91883.
- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.

## first stated

Chapter 8 section 8.8 of *Data Mining as Observation*, with the program's template `observation-theory-campaigns/experiments/PREREG-TEMPLATE.md:1-71` and Volume 14's protocol `geometric-observation/PROTOCOL.md:58-75`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.1 | the four tasks, the churn framing, the framing workshop | TSK chapter 1; instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:29-60` |
| chapter 1 section 1.3 | the four failure modes | `ECE_514-01_FA26_session-outlines.md:38` |
| chapter 1 section 1.6 | the course map | `ECE_514-01_FA26_session-outlines.md:29-332` |
| chapter 1 section 1.7 | the field guide, the decision test, the red flags | `ECE_514-01_FA26_session-outlines.md:39-46` |
| chapter 2 section 2.3 | MCAR, MAR, MNAR and the remedies, imputation before splitting | TSK 2e section 2.2; instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:64-72` |
| chapter 2 section 2.3 | the missing-data rule as a required preregistration field | `observation-theory-campaigns\experiments\PREREG-TEMPLATE.md:47-52` |
| chapter 5 section 5.3 | the transferable idea as a course learning outcome | instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:117-136` |
| chapter 7 section 7.6 | the preregistration fields | instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:157-176`; chapter 8 section 8.8 of this book |
| chapter 8 section 8.3 | anti-vacuity bar, quoted | `observation-theory-campaigns\experiments\PREREG-PF5-002.md:79-86` |
| chapter 8 section 8.8 | template fields | `observation-theory-campaigns\experiments\PREREG-TEMPLATE.md:1-71` |
| chapter 8 section 8.8 | declaration drafted 2026-08-17, sealed 2026-08-18, one count corrected, G2 | `geometric-observation\crucible\DECLARATION-V1.md:1-20`; `geometric-observation\crucible\OT-CRUCIBLE-4.md:31-35` |

## failures and corrections

- `observation-theory-campaigns/ERRATA.md:90-110` at f5585e7. ## E3. Two wrong bar values in the campaign notes **Found** 2026-08-07, same pass. Not a published error. `experiments/CAMPAIGN.md` twice described the PF4-006 entry-point and timestep clause as having a bar of 1e-10. The sealed declaration and the committed record both set that bar at 1e-8. The 1e-10 figure is the separate translation-covariance bar. The narrative was wrong and the verdict was not, since the clause failed at 1.3e-2 against either number. The same document described PREREG-PF4-009 as passing all six bars. The sealed document groups its requirements into six bars and the governed runner reports eight items, and the mapping between them was never declared. Both statements are now made explicitly. Corrected in place, since these are working notes rather than sealed documents or published records. ---

## conditions

- A preregistration commits the hypothesis, the bar, the analysis, and the missing-data rule before the measurement is run, so that the record shows what was predicted rather than what was found.
- Its bar must be anti-vacuous. A pass that any instrument would have produced, a threshold met by every reading, proves nothing, and the program's own first PF5 pass is the case.
- Multiple looks at the data need a corrected threshold, and a preregistration that names one look needs none.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Bonferroni.lean`, theorems `family_error_le`, `bonferroni`, `one_look`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

sealed, ledger-class, harness, certificate

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
