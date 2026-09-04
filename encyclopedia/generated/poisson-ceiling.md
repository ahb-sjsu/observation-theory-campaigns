# Poisson ceiling

**id.** poisson-ceiling
**kind.** instrument

## definition

The largest neighbour count that at least one point in a dataset would reach by chance under a Poisson null, above which a count is evidence of a hub. Equation 0.17.

## equation

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.

## first stated

openvector-bench, `openvector-bench/openvector_bench/hubness.py:41-100`, and chapter 0 section 0.8 and chapter 3 section 3.5 of *Data Mining as Observation*.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:38-59,140-160` |
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |
| chapter 8 section 8.1 | G1 339.9 vs 71.9 same corpus, real about 61, rounds 1 to 4 at 300 to 420, three families falsified | `openvector-bench\results\QUERY_COUPLING_ARTIFACT.md:1-20` |
| chapter 10 section 10.2 | anti-hubs as where compressed indexes fail first, aggregate recall barely moves | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 10 section 10.3 | abstain below 2.5 k | `turboquant-pro\docs\HUBNESS_PRIMER.md:140-160` |
| chapter 11 section 11.6 | count of ten, hubs and anti-hubs, max 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, abstain below 2.5k, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:1-60,60-170` |
| chapter 11 section 11.6 | anti-hub recall, p05, hub-rank correlation, hub-set overlap, the build gate | `turboquant-pro\docs\HUBNESS_PRIMER.md:86-131` |
| chapter 11 section 11.6 | the centroid-injection attack | `turboquant-pro\docs\HUBNESS_PRIMER.md:168-197`, citing arXiv 2604.05480 |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- Under the null that the slots are handed out at random, a row's count is Poisson with mean the slots per row, and the ceiling is the largest count at least one row would reach by chance. A count above it is evidence of a hub, and a count below it is not evidence of anything.
- The ceiling depends on the query set, through the mean and through the rows the queries reach, so it is recomputed when the queries change, and the program's first hubness numbers moved by a factor of several when query coupling was removed.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/PoissonCeiling.lean`, theorems `mass_nonneg`, `tail_antitone`, `tail_zero`, `tail_le_one`, `expectedAtLeast_antitone`, `example_mean`, at observation-data-mining a9fd869.

## used in

*Data Mining as Observation* chapters 0, 3.

## related

hubness, anti-hub, harness, min-over-strata

## status

Generated 2026-09-04 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns c5a03d7, theory-radar 37c4e6c, observation-data-mining a9fd869, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
