# coverage

**id.** coverage
**kind.** concept

## definition

The fraction of decisions a certificate clears, reported beside its false-clear rate, since a certificate that clears nothing has a false-clear rate of zero and no use. Equation 0.26.

## equation

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

## ledger

none

## first stated

*Data Mining as Observation*, chapter 0 section 0.13 and chapter 13, introduced on 2026-09-03 when the false-clear rate was restated as a conditional rate, and Volume 14 chapter 19 at geometric-observation 7d91883.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 12 section 12.6 | XPROTO-LLM, benchmark 0.909, 0.920, 0.909, thirty slices, target 0.8, naive 0.333, aware 0.033, spread 0.380, deployment mean 0.736, six bars on three seeds, sealed 2026-08-25 at b61f7f1 | `observation-theory-campaigns\experiments\LLM-EVAL-TRACK.md:1-50`; `observation-theory-campaigns\analysis\llm\XPROTO-LLM-graded.json`; `observation-theory-campaigns\experiments\SEALS.md:85` |
| chapter 13 section 13.3 | ZooKeeper hot 0.99 cold 0.01 witnessed 0.0, Postgres 0.50 to 0.06, MongoDB 0.47 to 0.03, production Postgres 0.47 to 0.02, real substrates, disjoint seeds | `observation-theory-campaigns\experiments\DATABASE-FRESHNESS-TRACK.md:1-45` |

## failures and corrections

none

## conditions

- A naive certificate clears every decision, so its coverage is one and its conditional and joint false-clear rates coincide.
- A witnessed certificate clears fewer decisions, and its false-clear rate is read beside its coverage, never alone.
- The word also names, in chapter 14, what a moderation instrument can read of the signal its inputs carry, which is a different quantity and is not this entry.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Certificate.lean`, theorems `falseClear_mul_coverage`, `coverage_empty`, `falseClear_mem_unit`, `minOverStrata_passes_iff`, `minOverStrata_le_weighted_mean`, at observation-data-mining 51c193c.

## used in

*Data Mining as Observation* chapters 0, 10, 12, 13, 14.

## related

false-clear-rate, certificate, witness

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f206f90, theory-radar 37c4e6c, observation-data-mining 51c193c, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
