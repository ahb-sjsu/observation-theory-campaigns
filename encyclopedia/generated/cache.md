# cache

**id.** cache
**kind.** concept

## definition

A store of recently used data kept so that it need not be fetched again. A cold measurement is taken before the cache holds anything useful, a warm one after. Chapter 13.

## equation

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

Book equation 0.26.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad \text{coverage}=\Pr\big[\mathcal C_t\ \text{clears}\big].

## ledger

- OT-11. Feedback-free staleness: streaming-retrieval damage tracks measured drift; derived-cadence re-allocation removes it. `[void]`. `geometric-observation/claims/LEDGER.md:48` at 01e53bc.
- GO-12. The dynamic region's opening control — staleness is access width, not delay: with full context-path access, pure-delay aging is information-free (the recoding identity $(Y,V,S^{(\Delta)})\overset d=(Y,V,P^\Delta S^{(0)})$ makes every $\sigma(S)$-measurable conditional functional exactly $\Delta$-invariant; circulant-exact, $O(1/n)$ edge leakage on finite windows); with time-local slice access the tax is GO-11's static quadratic with the substitution set by the \emph{encoder's} access — single-letter $(Y_t,V_t)$ records at $(\rho,\ s/a^{2\Delta})$, context-epoch-latent records at the strictly smaller $(\rho a^\Delta,\ \tau^2)$ (gap up to $0.053$ bits) — both strictly increasing in $\Delta$ with common limit $\tfrac12\log_2(1/D)$. GO-8's age-dependence is the slice regime's operational face. Theorem 1 (the conditional-variance reduction) settles the causal-prefix eraser in the single-record setting: every observation-subset $\sigma$-algebra enters through $q_{\mathcal G}=\mathrm{Var}(V_t\mid\mathcal G)$ alone; slice/prefix/path = single-sample/Kalman-fixed-lag/noncausal-Wiener variances; strict interpolation at every finite lag with exact gap $C^{2\Delta}(P_f-q_{\mathrm{path}})$; $W(\Delta)=kT\ln2\cdot L_{\mathrm{prefix}}$ is the dynamic conditional-Landauer curve. Theorem 2-spectral (070): the spectral conditional RDF — at the work endpoint, $L(D)$ is the equal-slope allocation of per-frequency static quadratics over the circulant spectrum, with classical reverse water-filling ($\tau^2\to\infty$) and the static theorem (flat spectrum) exact; per-mode convexity proven; the third promotion of the water level completed for the single-consumer face; Toeplitz transfer scoped imported-with-lemmas, $O(1/n)$ numerics. The weighted spectral theorem (071) closes Conjecture 1 at circulant scope: $J_w$ decomposes per-frequency at every $w$, each mode carrying Theorem 3's two-water-level system $(\gamma_0(\omega),\gamma_1(\omega))$ under ONE common distortion price (the conjectured ``pair of prices'' refuted-as-phrased, rescoped to $(w,\mu)$); convexity via the full-region moment argument + perturbation. The third promotion is complete on BOTH faces. `[predicted]`. `geometric-observation/claims/LEDGER.md:78` at 01e53bc.

## first stated

Chapter 13 section 13.5 of *Data Mining as Observation*, with the cache reader row of chapter 1's consumer table and the hot-and-cold substrate measurements of the freshness track.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 8 section 8.9 | 13.7 ROUGE-L, 0.25/4.19/9.60/13.7 at 64/128/256/512, re-validation negative 0.31 n=40, 26.64 under symmetric nf4, `_quant_nf4a_group` unchanged since `289bdfc` before `4f7baab` | `turboquant-pro\CLAIMS.md:63-81`; `turboquant-pro\benchmarks\kvquant_matrix\REVAL-2026-08-08.md` |

## failures and corrections

none

## conditions

- A store of recently used data kept so that it need not be fetched again. A cache reader reads the entries in its footprint and nothing else, so its hit rate over a stream of requests lies in the unit interval, is zero cold and one warm, never falls when the cache holds more, and is unchanged by entries outside the requests.
- A cold and a warm measurement of the same system are two observers of it. The ZooKeeper substrate's false-clear rate was 0.99 hot and 0.01 cold, which is the case that a cache's number is the requests' number.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Cache.lean`, theorems `hitRate_mem_unit`, `hitRate_cold`, `hitRate_warm`, `hitRate_mono`, `hitRate_footprint`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

kv-cache, eviction, freshness, replica, consumer

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
