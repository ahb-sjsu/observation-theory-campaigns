# hubness

**id.** hubness
**kind.** concept

## definition

The excess of a few rows in the nearest-neighbour lists of many queries over what the Poisson ceiling allows, measured by the busiest count and the Robin Hood index, a property of the queries. Chapter 3 section 3.5 and chapter 10.

## equation

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

Book equation 0.35.

    \mathrm{RH}=\sum_i\max\!\Big(0,\ \frac{N_i}{\sum_j N_j}-\frac1n\Big).

## ledger

- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 9f3829f.
- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 9f3829f.

## first stated

Radovanović, Nanopoulos, and Ivanović, hubs in space, 2010, as chapter 3 section 3.5 of *Data Mining as Observation* reads it, with the program's primer in `turboquant-pro/docs/HUBNESS_PRIMER.md:1-60`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:38-59,140-160` |
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |
| chapter 11 section 11.6 | count of ten, hubs and anti-hubs, max 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, abstain below 2.5k, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:1-60,60-170` |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- The excess of a few rows in the nearest-neighbour lists of many queries over what the Poisson ceiling allows, measured by the busiest count, the skew of the count distribution, and the Robin Hood index. The counts sum to the slots handed out, so the rows above any ceiling are few, and whether a row is a hub depends on the queries alone.
- Query coupling inflated the first hub counts by a factor of several, the density quotient that was to remove hubness was refuted four times, and the Bell-boundary audit found no mechanism in it, NEG-15.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Hubness.lean`, theorems `sum_count`, `sum_count_eq`, `count_congr`, `antiHub_iff`, at observation-data-mining 5bb2c0d.

`lean/DataMiningAsObservation/Hub.lean`, theorems `card_hubs_le`, `hubs_congr`, `hubs_anti`, `hubs_empty`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 1, 3, 10, 11.

## related

hub, anti-hub, poisson-ceiling, robin-hood-index, null-model

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
