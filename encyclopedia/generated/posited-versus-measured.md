# posited versus measured

**id.** posited-versus-measured
**kind.** concept

## definition

The division of every claim in a report into those asserted by design and those backed by an artifact. Chapter 14.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 7d91883.
- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 7d91883.

## first stated

The epistemic banners of the four posited volumes, `geometric-ai/README.md`, `geometric-cognition/README.md`, `geometric-reasoning/README.md`, `geometric-education/README.md`, and chapter 14 section 14.8 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 14 section 14.8 | registry rules, V4 proved in Lean and verified 2026-08-17 at commit ea7ee82, D4 posited with the drift list, reliability weight as one formula one source, 8 of 9 | `erisml-lib\docs\CONCEPT_REGISTRY.md:1-160` |
| chapter 14 section 14.8 | the four posited volumes | `geometric-ai\README.md`; `geometric-cognition\README.md`; `geometric-reasoning\README.md`; `geometric-education\README.md` epistemic banners |

## failures and corrections

none

## conditions

- Every claim in a report is either posited, asserted by design with no artifact behind it, or measured, backed by a committed artifact the reader can open. The division is stated at the top of the report and not inferred from the prose.
- A posited claim carries no ledger class above exploratory, and it stays there until a sealed measurement moves it. The ledger rule that says so is the one machine-checked in the book.
- Four volumes of the program are posited in their entirety and say so on their first page. Their claims are cited only as proposals.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Ledger.lean`, theorems `step_none`, `step_miss_le`, `step_pass_ge`, `step_miss_refuted`, `exploratory_stays`, at observation-data-mining abac866.

## used in

*Data Mining as Observation* chapters 14.

## related

ledger-class, preregistration, sealed, reliability-weight

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 6f08896, theory-radar 37c4e6c, observation-data-mining abac866, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
