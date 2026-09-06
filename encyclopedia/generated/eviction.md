# eviction

**id.** eviction
**kind.** concept

## definition

Choosing what to drop when a cache is full. Chapter 13.

## equation

Book equation 13.1.

    \mathrm{FC}=\Pr\big[W\ \text{refutes}\ \big|\ \mathcal C_t\ \text{clears}\big],\qquad d_O(\Delta)=\operatorname{tr}\big(P_C\,M_{\mathrm{drift}}(\Delta)\big),\qquad M_{\mathrm{drift}}(\Delta)=\mathbb E\big[\delta_\Delta\delta_\Delta^{\top}\big].

Book equation 0.23.

    \operatorname{softmax}(z)_i=\frac{e^{z_i}}{\sum_j e^{z_j}},\qquad \text{output}=\sum_i\operatorname{softmax}\!\Big(\frac{q\cdot k_i}{\sqrt{d}}\Big)_{\!i}\,v_i.

## ledger

- GO-12. The dynamic region's opening control — staleness is access width, not delay: with full context-path access, pure-delay aging is information-free (the recoding identity $(Y,V,S^{(\Delta)})\overset d=(Y,V,P^\Delta S^{(0)})$ makes every $\sigma(S)$-measurable conditional functional exactly $\Delta$-invariant; circulant-exact, $O(1/n)$ edge leakage on finite windows); with time-local slice access the tax is GO-11's static quadratic with the substitution set by the \emph{encoder's} access — single-letter $(Y_t,V_t)$ records at $(\rho,\ s/a^{2\Delta})$, context-epoch-latent records at the strictly smaller $(\rho a^\Delta,\ \tau^2)$ (gap up to $0.053$ bits) — both strictly increasing in $\Delta$ with common limit $\tfrac12\log_2(1/D)$. GO-8's age-dependence is the slice regime's operational face. Theorem 1 (the conditional-variance reduction) settles the causal-prefix eraser in the single-record setting: every observation-subset $\sigma$-algebra enters through $q_{\mathcal G}=\mathrm{Var}(V_t\mid\mathcal G)$ alone; slice/prefix/path = single-sample/Kalman-fixed-lag/noncausal-Wiener variances; strict interpolation at every finite lag with exact gap $C^{2\Delta}(P_f-q_{\mathrm{path}})$; $W(\Delta)=kT\ln2\cdot L_{\mathrm{prefix}}$ is the dynamic conditional-Landauer curve. Theorem 2-spectral (070): the spectral conditional RDF — at the work endpoint, $L(D)$ is the equal-slope allocation of per-frequency static quadratics over the circulant spectrum, with classical reverse water-filling ($\tau^2\to\infty$) and the static theorem (flat spectrum) exact; per-mode convexity proven; the third promotion of the water level completed for the single-consumer face; Toeplitz transfer scoped imported-with-lemmas, $O(1/n)$ numerics. The weighted spectral theorem (071) closes Conjecture 1 at circulant scope: $J_w$ decomposes per-frequency at every $w$, each mode carrying Theorem 3's two-water-level system $(\gamma_0(\omega),\gamma_1(\omega))$ under ONE common distortion price (the conjectured ``pair of prices'' refuted-as-phrased, rescoped to $(w,\mu)$); convexity via the full-region moment argument + perturbation. The third promotion is complete on BOTH faces. `[predicted]`. `geometric-observation/claims/LEDGER.md:78` at 01e53bc.
- GO-2/GO-12/GO-13 operational (KV serving, 077). Consumer-relative access width measured on a production serving stack (Qwen2.5-7B KV-cache eviction, matched budget): task quality tracks measured predictive uncertainty u about the consumer's future reads, not nominal scorer width — the 32-query snapshot beats the 1024-query scorer +0.4375±0.070 at 5% keep (bar 0.30) and survives 97% eviction with zero drop, while wide-window scoring is statistically indistinguishable from random eviction at extreme budgets; the recency-hoarding starvation signature replicated across three disjoint prompt sets (oracle-miss gap 0.370 vs bar 0.25). The novel equal-uncertainty analytic-equality control (degradation-titrated, constructible by design) REFUTED its own equality prediction on the pre-registered branch: with calibration health 4×–130× inside gates, equal scalar u did NOT give equal quality (V4 +0.078 vs 0.0625 tolerance; the pre-registered ρ=0.03 contrast firmed to +0.359±0.068, 5.3 SE) — equal scalar uncertainty is insufficient, error structure matters, consistent with GO-13 Theorem 1's own r≥2 scoping of equal-q universality (a scalar-context privilege). Successor arc: 056 honest miss → 075 ID burned on a disclosed design failure → 077 sealed and split-verdict. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:81` at 01e53bc.

## first stated

Chapter 13 section 13.6 of *Data Mining as Observation*, with the program's serving-stack case in `geometric-observation/prereg/GO-P-2026-077-kv-consumer-relative-eviction.md` and the ledger row that carries it.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 13 section 13.6 | attempt two, broken proxy, control did not exist, identifier burned, 16 prompts, 1360 s | `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md:1-15`; `geometric-observation\results\GO13-kvaw-pilot-disclosed.json` |
| chapter 13 section 13.6 | attempt three, windows 1024, 256, 32, uncertainty 0.982 to 0.892, 5 of 6, 0.4375 with SE 0.070 at 5 percent keep vs 0.30, 97 percent eviction, oracle-miss 0.370 vs 0.25, V4 0.078 vs 0.0625, contrast 0.359 with SE 0.068, n 64, seed 20260812, 89 duty cycles | `geometric-observation\claims\LEDGER.md` row GO-2/GO-12/GO-13 operational; `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md`; `geometric-observation\results\GO13-kvaw2-governed.json` |

## failures and corrections

none

## conditions

- Choosing what to drop when a cache is full. Evicting tokens replaces attention over all tokens with attention over the kept subset, so the output lies between the kept values, equals them when they agree, and the whole cache is the case of no eviction.
- Which tokens can go is consumer-relative, since a head reads a key only through its score, and the serving-stack measurement of ninety-seven percent eviction at a five percent keep against an oracle is the ledger's number, after one attempt whose control did not exist.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Eviction.lean`, theorems `kept_weights_sum`, `keptOutput_le_max`, `min_le_keptOutput`, `keptOutput_const`, `keptOutput_univ`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 0, 13.

## related

kv-cache, attention, coherence-time, budget

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
