# hub

**id.** hub
**kind.** concept

## definition

A row retrieved as a nearest neighbour far more often than chance allows. The book shows hubness is almost entirely a property of the queries and the reader, not of the corpus. Chapters 3 and 10.

## equation

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

Book equation 0.17.

    \Pr[X\ge c]=1-\sum_{i<c}e^{-\mu}\frac{\mu^{i}}{i!},\qquad c^{\star}=\max\{c:\ n\Pr[X\ge c]\ge 1\},\qquad \mu=\frac{n_q\,k}{n}.

Book equation 10.5.

    \begin{gathered} \text{central}:\ \mathrm{pct}_{\mathrm{centrality}}\ge0.95; \\ \text{dense}:\ \neg\text{central}\ \wedge\ \mathrm{pct}_{\mathrm{density}}\ge0.85; \qquad \text{prescribe by }f_{\mathrm{central}},\ f_{\mathrm{dense}}\ \text{at}\ 0.75. \end{gathered}

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 01e53bc.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 01e53bc.

## first stated

Radovanović, Nanopoulos, and Ivanović, hubs in space, 2010, as chapter 3 section 3.5 of *Data Mining as Observation* reads it, with the program's finding in openvector-bench that hubness is a query property, `openvector-bench/results/QUERY_COUPLING_ARTIFACT.md:1-20`.

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
- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- A row retrieved as a nearest neighbour far more often than chance allows, a count above the Poisson ceiling. Since the counts sum to the slots handed out, the number of rows with count above a ceiling is at most the slots over the ceiling plus one, so hubs are few by arithmetic, and a higher ceiling names fewer of them.
- Whether a row is a hub depends on the queries and the retrieval rule alone, which is the sense in which hubness is a query property, and the program's first hub counts fell by a factor of several when query coupling was removed.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Hub.lean`, theorems `card_hubs_le`, `hubs_congr`, `hubs_anti`, `hubs_empty`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 5, 10, 11, 12, 13.

## related

hubness, poisson-ceiling, anti-hub, robin-hood-index, null-model

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
