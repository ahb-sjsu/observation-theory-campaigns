# projection

**id.** projection
**kind.** concept

## definition

The component of a vector along a unit direction. Equation 0.2.

## equation

Book equation 0.2.

    \operatorname{proj}_u(x)=(u\cdot x)\,u,\qquad \|u\|=1.

Book equation 0.12a.

    x\sim_C x'\quad\Longleftrightarrow\quad d_G\big(C(x),C(x')\big)=0.

Book equation 0.12b.

    x\sim_{\bar P_{C,\mu}} x'\quad\Longleftrightarrow\quad x-x'\in\ker\bar P_{C,\mu}.

## ledger

- GO-1. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. `[predicted]`. `geometric-observation/claims/LEDGER.md:62` at 01e53bc.
- GO-10. Serving two read operators from one description costs a complementarity tax, and erasure pays that tax only against what the reset context does not already know about the read plane: the rate floor $D_AD_B\ge\kappa\,2^{-2R}$, $\kappa=\det(B^{\mathsf T}\Sigma_xB)$, is exactly the joint rate–distortion function iff $\mathrm{diag}(D_A,D_B)\preceq B^{\mathsf T}\Sigma_xB$; the reset-work floor carries $\kappa_S=\det(B^{\mathsf T}\Sigma_{X\mid S}B)$; the two floors differ by exactly $I(u^{\mathsf T}X,v^{\mathsf T}X;S)$; and the measured rate-tax/work-tax gap on materialized codebook records is a substantial fraction of the family's floor ($\tfrac12\log_2(1/(s^2+(1-s^2)\hat d))$ Gaussian; $1-h_2(\hat d \ast q)$ binary), monotone in context quality, zero for a mismatched context. `[replicated]`. `geometric-observation/claims/LEDGER.md:75` at 01e53bc.
- GO-11. The exact conditional rate–work region behind the tax: the single-consumer CR function for a rank-one read with general jointly Gaussian side information is $\tfrac12\log_2 g^\star$, $g^\star$ the larger root of $Dsg^2-(D{+}s{-}\rho^2)g+(1{-}\rho^2)$ ($s=1{+}\tau^2$) — the first vector-Gaussian common-reconstruction-type function; the $m{=}1$ frontier is a two-water-level system with strict two-corner separation whenever the context is misaligned ($\rho^2\in(0,1)$ — Paper V's single-corner collapse is exactly the alignment degeneracy); the $m{=}2$ region is a nine-parameter matrix program from which the GO-10 tax-gap formula is \emph{derived}; and the work floor is attained iff the context is $X$-measurable-and-SDC or plane-blind (Thm 6, correcting Conjecture 3's $\Sigma_{Y\mid S}$ to the encoder-accessible $\Sigma_{Y\mid V}$). `[replicated]`. `geometric-observation/claims/LEDGER.md:77` at 01e53bc.
- GO-12. The dynamic region's opening control — staleness is access width, not delay: with full context-path access, pure-delay aging is information-free (the recoding identity $(Y,V,S^{(\Delta)})\overset d=(Y,V,P^\Delta S^{(0)})$ makes every $\sigma(S)$-measurable conditional functional exactly $\Delta$-invariant; circulant-exact, $O(1/n)$ edge leakage on finite windows); with time-local slice access the tax is GO-11's static quadratic with the substitution set by the \emph{encoder's} access — single-letter $(Y_t,V_t)$ records at $(\rho,\ s/a^{2\Delta})$, context-epoch-latent records at the strictly smaller $(\rho a^\Delta,\ \tau^2)$ (gap up to $0.053$ bits) — both strictly increasing in $\Delta$ with common limit $\tfrac12\log_2(1/D)$. GO-8's age-dependence is the slice regime's operational face. Theorem 1 (the conditional-variance reduction) settles the causal-prefix eraser in the single-record setting: every observation-subset $\sigma$-algebra enters through $q_{\mathcal G}=\mathrm{Var}(V_t\mid\mathcal G)$ alone; slice/prefix/path = single-sample/Kalman-fixed-lag/noncausal-Wiener variances; strict interpolation at every finite lag with exact gap $C^{2\Delta}(P_f-q_{\mathrm{path}})$; $W(\Delta)=kT\ln2\cdot L_{\mathrm{prefix}}$ is the dynamic conditional-Landauer curve. Theorem 2-spectral (070): the spectral conditional RDF — at the work endpoint, $L(D)$ is the equal-slope allocation of per-frequency static quadratics over the circulant spectrum, with classical reverse water-filling ($\tau^2\to\infty$) and the static theorem (flat spectrum) exact; per-mode convexity proven; the third promotion of the water level completed for the single-consumer face; Toeplitz transfer scoped imported-with-lemmas, $O(1/n)$ numerics. The weighted spectral theorem (071) closes Conjecture 1 at circulant scope: $J_w$ decomposes per-frequency at every $w$, each mode carrying Theorem 3's two-water-level system $(\gamma_0(\omega),\gamma_1(\omega))$ under ONE common distortion price (the conjectured ``pair of prices'' refuted-as-phrased, rescoped to $(w,\mu)$); convexity via the full-region moment argument + perturbation. The third promotion is complete on BOTH faces. `[predicted]`. `geometric-observation/claims/LEDGER.md:78` at 01e53bc.
- GO-13. The dynamic complementarity tax, opened with Theorem 1 settled: for $m=2$ single-letter records under the CI embedding, the eraser's access enters all coordinates only through $\Sigma_{T\mid\mathcal G}=\Sigma_T-(1-q_{\mathcal G})cc^{\mathsf T}$ (the matrix-$q$ reduction: Theorem 9's program at the conditional pair), so with scalar context every coordinate and both taxes are functions of $q_{\mathcal G}$ alone — equal-$q$ access classes give identical taxes — with coordinates nondecreasing in $q$ and $\mathrm{CT}_W\to\mathrm{CT}_R$ at $q\to1$. Theorem 2 (068): the tax-curve envelope sign law — staleness raises the tax iff the joint record's context coupling exceeds the binding consumer's, max-switch kink always downward, $w{=}1$ flat. Operational face (069): both theorems measured — the tax rises $+0.090$ under staleness at the regime map's rising instance ($+0.086$ predicted), equal-$q$ classes agree to $0.001$. Theorem 3 (072): the binary twin --- slice collapse exact at $q_{\mathrm{eff}}=q*\delta_\Delta$; the family survives every finite access class via the posterior reliability distribution; single-$q$ universality fails EXACTLY ($\sim9\times10^{-5}$, 50-digit-verified) though numerically near-universal --- universality is exactly a Gaussian privilege. Theorem 4 (073): the spectral m=2 theorem — per-frequency Theorem-9 matrix water levels under two common prices (static kernel: Xiao–Luo/Stylianou et al.). Theorem 5 (074): the m-record moment-convexity lemma PROVED — the weighted m=2 program is convex in moments; Theorem 9’s uniqueness resolved; the two-price rule globally optimal. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:79` at 01e53bc.
- GO-16. The adversarial observer — the revelation reduction and the partition/tie theorem, netted: leakage to a rank-$k$-budgeted reader depends on the record policy $(F,\Sigma_w)$ only through the revelation operator $K = F^\top N^{-1}F$; the minimal value cost of achieving $K$ is exactly $\mathrm{tr}(S(I-K)S^\top)$, attained by shrink-and-dither ($F = SK$, $\Sigma_w = SK(I-K)S^\top$); the game is a convex SDP whose bilinear saddle yields the four-way partition (conceded / blacked-out / contested / submerged) with contested directions priced to exact encoder indifference and the spectral tie $\lambda_k = \lambda_{k+1}$ forced by fractional attention; diagonal scope closes as the attention water level (contested $\rho_i = t^*/\mu_i$, reader mixing $\theta_i = s_i^2/(\lambda\mu_i)$, tie iff contested, fractional/integral two-regime alternative); noiseless records are idempotent revelators — deception requires dither. Discrete twin at governed grade: binary frontier = the symmetric channel exactly ($e(\rho) = (1-\sqrt\rho)/2$ — the LQG linear cost is a Gaussian privilege), the tie survives with generalized pricing $\theta_i = s_i^2/(4\lambda\sqrt{\mu_i t^*})$, a fifth class LQG forbids (interior-contested-above: partial balancing without indifference) at the pre-run hand prediction, mixing = the discrete carrier of dither. Corrections at equal prominence: v0.1 never-dither conjecture refuted; v0.2's jitter diagnosis of the v0.1 probe itself refuted by the R-IND-5 pass and replaced by the V10 measurement (near-projection optima at the v0.1 cells; the contested phase appears to concentrate on commuting-aligned $(\Sigma_S, M)$ pairs — open); no-commitment-gap scoped to the whitened-attention ($N$-conditioned) game, the fixed-instrument $\Theta$-mixture game open. Six lemmas Lean-checked (Atlas, zero `sorry`). Novelty posture per flank + quote-level sweep (13 verified / 2 corrected / 1 unverifiable-at-primary of 16): SDP machinery imported (Sayin–Akyol–Başar; Tamura), tie ancestor Overton–Womersley coalescence; headline = the partition / indifference-pricing / water-level / tie-iff theorem `[predicted]`. `geometric-observation/claims/LEDGER.md:84` at 01e53bc.

## first stated

Chapter 0 section 0.2 of *Data Mining as Observation*, with the program's angular projection in Volume 14 chapter 9, `geometric-observation/chapters/ch09_legibility.md:31-41`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 6 section 6.2 | planted probe, overlap 0.936 vs 0.059, twelve of twelve, reconstruction 0.40, five of five | `geometric-observation\claims\LEDGER.md` row GO-1 |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |

## failures and corrections

none

## conditions

- The component of a vector along a unit direction, the direction scaled by their dot product. Projecting twice is projecting once, the remainder is orthogonal to the direction, the projection is no longer than the vector, and adding anything orthogonal to the direction leaves it unchanged.
- The last is the quotient a one-direction reader takes. Row normalization is the projection onto the read subspace of the geodesic-rank consumer, and the invariant-nuisance split of the ledger is the same statement for a general consumer.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Projection.lean`, theorems `proj_proj`, `dot_sub_proj`, `proj_sq_le`, `proj_add_orth`, `proj_add`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 0, 1, 3, 4, 6, 7, 9, 11.

## related

dot-product, read-subspace, quotient, nuisance

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
