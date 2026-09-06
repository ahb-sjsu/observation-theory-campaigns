# declaration

**id.** declaration
**kind.** instrument

## definition

A sealed statement of what a study will count, drop, or treat as a failure, written before the run. Chapter 8 section 8.8.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

Book equation 8.3.

    \Pr[\text{at least one of } m\text{ null tests passes}]=1-(1-\alpha)^{m},\qquad \alpha_{\mathrm{Bonferroni}}=\frac{\alpha}{m}.

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 9f3829f.

## first stated

Chapter 8 section 8.8 of *Data Mining as Observation*, with the sealed declaration in `geometric-observation/crucible/DECLARATION-V1.md:1-20`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | the missing-data rule as a required preregistration field | `observation-theory-campaigns\experiments\PREREG-TEMPLATE.md:47-52` |
| chapter 8 section 8.8 | declaration drafted 2026-08-17, sealed 2026-08-18, one count corrected, G2 | `geometric-observation\crucible\DECLARATION-V1.md:1-20`; `geometric-observation\crucible\OT-CRUCIBLE-4.md:31-35` |

## failures and corrections

none

## conditions

- A statement of what a study will count, drop, or treat as a failure, sealed before the run. A changed digest would prove a changed declaration, and a declaration drafted on one day and sealed the next is the record's normal shape.
- The declaration for the fourth crucible was drafted 2026-08-17, sealed 2026-08-18, and had one count corrected, and the missing-data rule is a required declared field.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 2, 7, 8, 10, 11, 12.

## related

registered, sealed, preregistration, missingness, commit-hash

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
