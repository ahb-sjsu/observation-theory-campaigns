# query set

**id.** query-set
**kind.** concept

## definition

The rows a retrieval benchmark asks about. Hubness and the never-retrieved floor are properties of it. Chapter 3 section 3.5 and chapter 10 section 10.2.

## equation

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

Book equation 10.4.

    \text{never retrieved}\ \ge\ 1-\frac{|Q|\,k}{n}\qquad\text{whenever}\quad |Q|\,k<n.

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

## ledger

- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 9f3829f.
- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 9f3829f.

## first stated

Chapter 3 section 3.5 and chapter 10 section 10.2 of *Data Mining as Observation*, with the query-coupling artifact in `openvector-bench/results/QUERY_COUPLING_ARTIFACT.md:1-20`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |
| chapter 3 section 3.5 | query mass best single feature at every K for all four responses, seven features add at most 20 percent, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |
| chapter 10 section 10.2 | five kinds, balanced accuracy 0.611, 0.718, 0.684, the category table, per-category 0.57 to 0.82, the sweep, pigeonhole floor | `openvector-bench\results\R13_STAGE1_RESULT.md:40-75` |
| chapter 10 section 10.2 | half 2 failed, at most 1.28 times against 2, withdrawal and its scope | `openvector-bench\results\R13_STAGE1_RESULT.md:75-110` |
| chapter 11 section 11.6 | query mass best single feature at every K for all four responses, seven features add at most 20 percent at 12 leaves, threshold 1.25 on three of four, zero of four, 1000 real queries, 1024 dimensions | `openvector-bench\results\R13_STAGE0_RESULT.md:40-50`; `openvector-bench\results\R13_STAGE1_RESULT.md:1-40` |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- The rows a retrieval benchmark asks about. Two query sets that retrieve the same lists have the same hubs, no queries give no hubs, and the rows never retrieved number at least the row count less the queries times k, so hubness and the never-retrieved floor are properties of the query set.
- Queries drawn from the corpus inflated the first hub counts by a factor of several, and a generator matched on the query budget would be matched on an artifact.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Hub.lean`, theorems `card_hubs_le`, `hubs_congr`, `hubs_anti`, `hubs_empty`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Hubness.lean`, theorems `sum_count`, `sum_count_eq`, `count_congr`, `antiHub_iff`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 8, 10, 11, 12, 13.

## related

hub, hubness, poisson-ceiling, recall-at-k, harness

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
