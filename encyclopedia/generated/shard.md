# shard

**id.** shard
**kind.** instrument

## definition

One partition of an index that is searched separately, with the results merged. The global top k lies inside the union of the shards' top k. Chapter 13.

## equation

Book equation 11.3.

    \begin{gathered} \mathrm{recall}@k=\frac{\big|\text{returned top-}k\ \cap\ \text{true top-}k\big|}{k}, \\ \text{true top-}k\text{ computed from the uncompressed vectors}. \end{gathered}

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

Book equation 13.2.

    \begin{gathered} T_{\mathrm{coh}}=\frac{0.423}{f_D}, \\ \text{refuted fit:}\ \ \phi\approx0.177\,T_{\mathrm{coh}}\ (R^{2}=0.915), \qquad \text{sealed:}\ \ \phi\le 6\ \text{TTI at }10\ \text{Hz},\ \ 1\ \text{TTI at}\ \ge50\ \text{Hz}. \end{gathered}

## ledger

- GO-12. The dynamic region's opening control — staleness is access width, not delay: with full context-path access, pure-delay aging is information-free (the recoding identity $(Y,V,S^{(\Delta)})\overset d=(Y,V,P^\Delta S^{(0)})$ makes every $\sigma(S)$-measurable conditional functional exactly $\Delta$-invariant; circulant-exact, $O(1/n)$ edge leakage on finite windows); with time-local slice access the tax is GO-11's static quadratic with the substitution set by the \emph{encoder's} access — single-letter $(Y_t,V_t)$ records at $(\rho,\ s/a^{2\Delta})$, context-epoch-latent records at the strictly smaller $(\rho a^\Delta,\ \tau^2)$ (gap up to $0.053$ bits) — both strictly increasing in $\Delta$ with common limit $\tfrac12\log_2(1/D)$. GO-8's age-dependence is the slice regime's operational face. Theorem 1 (the conditional-variance reduction) settles the causal-prefix eraser in the single-record setting: every observation-subset $\sigma$-algebra enters through $q_{\mathcal G}=\mathrm{Var}(V_t\mid\mathcal G)$ alone; slice/prefix/path = single-sample/Kalman-fixed-lag/noncausal-Wiener variances; strict interpolation at every finite lag with exact gap $C^{2\Delta}(P_f-q_{\mathrm{path}})$; $W(\Delta)=kT\ln2\cdot L_{\mathrm{prefix}}$ is the dynamic conditional-Landauer curve. Theorem 2-spectral (070): the spectral conditional RDF — at the work endpoint, $L(D)$ is the equal-slope allocation of per-frequency static quadratics over the circulant spectrum, with classical reverse water-filling ($\tau^2\to\infty$) and the static theorem (flat spectrum) exact; per-mode convexity proven; the third promotion of the water level completed for the single-consumer face; Toeplitz transfer scoped imported-with-lemmas, $O(1/n)$ numerics. The weighted spectral theorem (071) closes Conjecture 1 at circulant scope: $J_w$ decomposes per-frequency at every $w$, each mode carrying Theorem 3's two-water-level system $(\gamma_0(\omega),\gamma_1(\omega))$ under ONE common distortion price (the conjectured ``pair of prices'' refuted-as-phrased, rescoped to $(w,\mu)$); convexity via the full-region moment argument + perturbation. The third promotion is complete on BOTH faces. `[predicted]`. `geometric-observation/claims/LEDGER.md:78` at 9f3829f.

## first stated

Chapter 13 section 13.1 of *Data Mining as Observation*, with the placement study in `turboquant-pro/docs/RESEARCH_ROADMAP.md:133-160` and the fleet run in `openvector-bench/README.md:250-263`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.4 | gate meta-rule, relative contrast discriminates nothing | `openvector-bench\openvector_bench\score_rc1.py:1-14`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 11 section 11.4 | R80 table, 25x probe depth, 92 percent own cell, one third cross-article, 0.53 matches same-article share, relative contrast discriminates nothing | `openvector-bench\results\R80_ANN.md:1-40`; `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 13 section 13.1 | 22.30 s cold vs 0.835 s warm at eight probes, every prior number warm, fragmentation 63.7 bracketing 42 to 47, 64 shards, routing sparsity computed and discarded | `turboquant-pro\docs\RESEARCH_ROADMAP.md:133-160` |
| chapter 13 section 13.1 | one hundred billion vectors on a preemptible fleet, systems result not a tier, corpus rejected by the admission battery | `openvector-bench\README.md:250-263` |

## failures and corrections

none

## conditions

- One partition of an index that is searched separately, with the results merged. If each shard returns its own top k and the global top k is strict, the global top k lies inside the union of the shards' answers, so the merge loses nothing and reads at most the number of shards times k candidates.
- A placement study over 64 shards reported search times taken with the file cache already holding the shards, and a speedup of 63.7 times was fragmentation, so a sharded number names whether it is warm and what the shards were.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Shard.lean`, theorems `global_in_local`, `global_in_union`, `merge_cost`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 11, 13.

## related

inverted-file, recall-at-k, cold-warm, cache, budget

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
