# session deck

**id.** session-deck
**kind.** reference

## definition

The lecture deck of ECE 514, cited by line range from the instructor's session outlines, which are not public. Chapter 1 section 1.6.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

## ledger

none

## first stated

Chapter 1 section 1.6 of *Data Mining as Observation*, citing the instructor's working documents, `ECE_514-01_FA26_session-outlines.md`, which are not public.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.1 | the four tasks, the churn framing, the framing workshop | TSK chapter 1; instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:29-60` |
| chapter 1 section 1.3 | the four failure modes | `ECE_514-01_FA26_session-outlines.md:38` |
| chapter 1 section 1.6 | the course map | `ECE_514-01_FA26_session-outlines.md:29-332` |
| chapter 1 section 1.7 | the field guide, the decision test, the red flags | `ECE_514-01_FA26_session-outlines.md:39-46` |
| chapter 2 section 2.3 | MCAR, MAR, MNAR and the remedies, imputation before splitting | TSK 2e section 2.2; instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:64-72` |
| chapter 5 section 5.3 | the transferable idea as a course learning outcome | instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:117-136` |
| chapter 7 section 7.6 | the preregistration fields | instructor working documents, not public [@bond2026course], `ECE_514-01_FA26_session-outlines.md:157-176`; chapter 8 section 8.8 of this book |

## failures and corrections

none

## conditions

- The lecture deck of the course the book accompanies, ECE 514, cited by line range from the instructor's session outlines. A row that names it names a file and lines like every other source, and a changed digest would prove a changed deck.
- The deck is not public. The book quotes what it says and marks each such row as instructor working documents, and the reader who wants the deck asks the instructor.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Seal.lean`, theorems `changed_of_hash_ne`, `hash_eq_of_eq`, `exists_collision`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14.

## related

sources-table, commit-hash, harness, preregistration

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
