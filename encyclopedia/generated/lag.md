# lag

**id.** lag
**kind.** concept

## definition

How far a replica trails the primary. The same lag gives two readers two staleness rates. Chapter 0 section 0.13 and chapter 13.

## equation

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

Book equation 0.25.

    T_{\mathrm{coh}}=\frac{0.423}{f_D}.

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 9f3829f.

## first stated

Chapter 0 section 0.13 of *Data Mining as Observation*, with the replica measurements in `observation-theory-campaigns/experiments/DATABASE-FRESHNESS-TRACK.md`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.2 | the grammar, certificate, witness, refresh floor, false-clear rate, vacuity, the witness table | `geometric-observation\chapters\ch19_the_certificate_that_ages.md:1-95`; `observation-theory-campaigns\experiments\FRESHNESS-PROGRAM.md:1-40` |
| chapter 13 section 13.3 | ZooKeeper hot 0.99 cold 0.01 witnessed 0.0, Postgres 0.50 to 0.06, MongoDB 0.47 to 0.03, production Postgres 0.47 to 0.02, real substrates, disjoint seeds | `observation-theory-campaigns\experiments\DATABASE-FRESHNESS-TRACK.md:1-45` |

## failures and corrections

none

## conditions

- How far a replica trails the primary, in writes or in time. A read of the replica is stale for a consumer whose footprint the lag has touched and fresh for one it has not, so the same lag gives two readers two staleness rates, and a mixed workload's rate lies between them.
- Postgres read 0.50 to 0.06, MongoDB 0.47 to 0.03, and production Postgres 0.47 to 0.02 across readers on the same lag, with disjoint seeds.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Replica.lean`, theorems `stale_mono`, `stale_zero`, `naive_certificate`, `witnessed_certificate`, `witnessed_coverage`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Freshness.lean`, theorems `disagree`, `mixedRate_between`, `mixedRate_eq_left_iff`, `stale_for_all`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 13.

## related

replica, freshness, coherence-time, false-clear-rate, footprint

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
