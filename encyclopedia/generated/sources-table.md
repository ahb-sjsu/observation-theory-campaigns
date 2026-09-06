# sources table

**id.** sources-table
**kind.** instrument

## definition

The table at the end of every chapter naming, for each number, the repository, file, and line range it came from. Chapter 0 section 0.21.

## equation

Book equation 8.1.

    O_{\mathrm{harness}}=\big(C_{\mathrm{score}},\ G_{\mathrm{metric}},\ B=\text{folds}\times\text{samples}\times\text{seeds}\big).

## ledger

none

## first stated

Chapter 0 section 0.21 of *Data Mining as Observation*, with the program's claims ledger that the same discipline enforces in `turboquant-pro/CLAIMS.md:1-27`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 11 section 11.5 | CI fails when CLAIMS.md and claims.yaml disagree | `turboquant-pro\CLAIMS.md:1-27`; `turboquant-pro\tests\test_claims_ledger.py` |

## failures and corrections

none

## conditions

- The table at the end of every chapter naming, for each number, the repository, file, and line range it came from, so that no number in the book has to be taken on trust. A row that names a commit hash binds the number to one state of the file, since a changed digest proves a changed file.
- The table is a citation and not a proof. The book's checker verifies that every cited path exists, and the encyclopedia's checker verifies the numbers of its hand-filled entries against the generated ones, but the numbers themselves are the records' and the reader who wants them opens the file.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

commit-hash, sealed, ledger-class, preregistration, certificate

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 8c6986b, observation-theory-campaigns 553a902, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
