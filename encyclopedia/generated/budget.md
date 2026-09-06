# budget

**id.** budget
**kind.** concept

## definition

The third element of an observer. The bits, rows, calls, seconds, or dollars a consumer may spend. Chapter 1.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

Book equation 0.13.

    D(b)=\sum_i s_i v_i\,4^{-b_i},\qquad b_i=\max\!\Big(0,\ \tfrac12\log_2\frac{s_i v_i}{\theta}\Big),\qquad \sum_i b_i=B.

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## ledger

- OT-3. Under subspace-confined second-order transcripts, fewer than d directions cannot identify a hidden leading eigenspace (theorem, adaptive to d−2 / oblivious to d−1); a known k₀-dim exclusion moves the cliff to exactly d−k₀ and never softens it. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:31` at 7d91883.
- GO-4. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. `[replicated]`. `geometric-observation/claims/LEDGER.md:66` at 7d91883.
- GO-12. The dynamic region's opening control — staleness is access width, not delay: with full context-path access, pure-delay aging is information-free (the recoding identity $(Y,V,S^{(\Delta)})\overset d=(Y,V,P^\Delta S^{(0)})$ makes every $\sigma(S)$-measurable conditional functional exactly $\Delta$-invariant; circulant-exact, $O(1/n)$ edge leakage on finite windows); with time-local slice access the tax is GO-11's static quadratic with the substitution set by the \emph{encoder's} access — single-letter $(Y_t,V_t)$ records at $(\rho,\ s/a^{2\Delta})$, context-epoch-latent records at the strictly smaller $(\rho a^\Delta,\ \tau^2)$ (gap up to $0.053$ bits) — both strictly increasing in $\Delta$ with common limit $\tfrac12\log_2(1/D)$. GO-8's age-dependence is the slice regime's operational face. Theorem 1 (the conditional-variance reduction) settles the causal-prefix eraser in the single-record setting: every observation-subset $\sigma$-algebra enters through $q_{\mathcal G}=\mathrm{Var}(V_t\mid\mathcal G)$ alone; slice/prefix/path = single-sample/Kalman-fixed-lag/noncausal-Wiener variances; strict interpolation at every finite lag with exact gap $C^{2\Delta}(P_f-q_{\mathrm{path}})$; $W(\Delta)=kT\ln2\cdot L_{\mathrm{prefix}}$ is the dynamic conditional-Landauer curve. Theorem 2-spectral (070): the spectral conditional RDF — at the work endpoint, $L(D)$ is the equal-slope allocation of per-frequency static quadratics over the circulant spectrum, with classical reverse water-filling ($\tau^2\to\infty$) and the static theorem (flat spectrum) exact; per-mode convexity proven; the third promotion of the water level completed for the single-consumer face; Toeplitz transfer scoped imported-with-lemmas, $O(1/n)$ numerics. The weighted spectral theorem (071) closes Conjecture 1 at circulant scope: $J_w$ decomposes per-frequency at every $w$, each mode carrying Theorem 3's two-water-level system $(\gamma_0(\omega),\gamma_1(\omega))$ under ONE common distortion price (the conjectured ``pair of prices'' refuted-as-phrased, rescoped to $(w,\mu)$); convexity via the full-region moment argument + perturbation. The third promotion is complete on BOTH faces. `[predicted]`. `geometric-observation/claims/LEDGER.md:78` at 7d91883.

## first stated

Volume 14, chapter 4 for the triple and chapter 7 for cost, `geometric-observation/chapters/ch07_cost.md`, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.2 | GO-6, d 8 and r 4, output at or below surrogate at or below reconstruction at every rate, about 500 times, gap 0.41 to 0.005, isotropic control collapses | `geometric-observation\claims\LEDGER.md` row GO-6; `geometric-observation\chapters\ch07_cost.md` |
| chapter 4 section 4.2 | commission tax of order half r log M over m, omission floor, unbounded corrected to floor, naive projector 30 percent over, VI-6 | `geometric-observation\chapters\ch07_cost.md` section on mismatch; `geometric-observation\claims\LEDGER.md` VI-6 |
| chapter 4 section 4.2 | floor measured on 16 of 16 heads, naive assumption off 20 to 60 percent, about 100000 times, 0.10 nats against about 6e-7, first gate missed 0 of 16, NEG-13 | `geometric-observation\chapters\ch07_cost.md`; `geometric-observation\claims\LEDGER.md` GO-P-2026-027 and NEG-13 |
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | `geometric-observation\claims\LEDGER.md` row GO-4 |
| chapter 11 section 11.7 | confinement theorem, side information moves the cliff to d minus k0, noisy cliff proved then measured | `readscope\PRINCIPLES.md:112-142`; `geometric-observation\crucible\OT3-THEOREM.md`; `geometric-observation\crucible\OT3-NOISY-THEOREM.md` |
| chapter 13 section 13.6 | attempt three, windows 1024, 256, 32, uncertainty 0.982 to 0.892, 5 of 6, 0.4375 with SE 0.070 at 5 percent keep vs 0.30, 97 percent eviction, oracle-miss 0.370 vs 0.25, V4 0.078 vs 0.0625, contrast 0.359 with SE 0.068, n 64, seed 20260812, 89 duty cycles | `geometric-observation\claims\LEDGER.md` row GO-2/GO-12/GO-13 operational; `geometric-observation\prereg\GO-P-2026-077-kv-consumer-relative.md`; `geometric-observation\results\GO13-kvaw2-governed.json` |

## failures and corrections

none

## conditions

- The budget is the bits, rows, calls, seconds, or dollars a consumer may spend. It bounds what of the read operator can be measured and used, and changes the operator only when it changes the consumer.
- Comparisons are made at matched budget. A verdict at a fixed budget can invert under budget matching, and the ledger carries the case.
- For a probe the budget is consumer calls, and recovery of the read operator is a cliff at the full dimension of the space.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ProbeCliff.lean`, theorems `centralDiff_affine`, `centralDiff_basis`, `exists_blind_direction`, `indistinguishable`, `budget_cliff`, at observation-data-mining 7eba709.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.

## related

observer, water-filling, budget-cliff, coverage

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns f5585e7, theory-radar 37c4e6c, observation-data-mining 7eba709, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
