# ledger class

**id.** ledger-class
**kind.** concept

## definition

One of six labels every headline claim carries, proved, demonstrated, replicated, predicted, exploratory, or refuted, defined in the evidence ledger of Volume 14. Chapter 1.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 7d91883.
- GO-2 (neg. half: not reconstruction). At matched bits, downstream preservation is not controlled by reconstruction error. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:63` at 7d91883.
- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 7d91883.

## first stated

Volume 14, `geometric-observation/PROTOCOL.md:58-75` and `geometric-observation/OBSERVATION.md:43-45`, DOI 10.5281/zenodo.21776291, with the ledger itself at `geometric-observation/claims/LEDGER.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.5 | the six classes and the ledger rule | `geometric-observation\PROTOCOL.md:58-75`; `geometric-observation\OBSERVATION.md:43-45` |
| chapter 8 section 8.3 | OT-11 void, strata 0.81 to 0.87 | `geometric-observation\claims\LEDGER.md:48` |
| chapter 8 section 8.8 | sixteen standing negatives | `geometric-observation\claims\LEDGER.md` NEG-1 to NEG-16 |
| chapter 8 section 8.10 | the six classes | `geometric-observation\PROTOCOL.md:58-75` |
| chapter 11 section 11.5 | CI fails when CLAIMS.md and claims.yaml disagree | `turboquant-pro\CLAIMS.md:1-27`; `turboquant-pro\tests\test_claims_ledger.py` |

## failures and corrections

none

## conditions

- Every headline claim carries one of six labels, proved, demonstrated, replicated, predicted, exploratory, or refuted. A claim's class can only rise by a sealed pass on held-out data and only fall by a sealed miss, and a refuted claim is reported at the prominence of a pass.
- A number produced without a sealed bar is exploratory whatever its size. It may motivate a claim and may not carry one.
- The authority for a claim's class is the ledger, and a chapter or an encyclopedia entry that disagrees with it is rebuilt.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

none

## used in

*Data Mining as Observation* chapters 8, 11.

## related

preregistration, sealed, certificate, false-clear-rate

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 2a2e053, theory-radar 37c4e6c, observation-data-mining 22aa258, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
