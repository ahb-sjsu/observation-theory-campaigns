# geodesic distance

**id.** geodesic-distance
**kind.** concept

## definition

The length of the shortest path along edges between two nodes of a graph. Chapter 0 section 0.10.

## equation

Book equation 3.2.

    R(i,j)=\sum_{k\ge2}\frac1{\lambda_k}\left(\frac{u_k(i)}{\sqrt{d_i}}-\frac{u_k(j)}{\sqrt{d_j}}\right)^{2}\ \longrightarrow\ \frac1{d_i}+\frac1{d_j}\quad(n\to\infty,\ \dim\ge3).

Book equation 3.3.

    X_i=r_i\,\theta_i,\qquad r_i\ \to\ \frac1{\sqrt{d_i}},\qquad \theta_i=\frac{X_i}{\|X_i\|}\in S^{m-1}.

Book equation 0.20.

    \Psi_i=\left(\frac{u_k(i)}{\sqrt{\lambda_k\,d_i}}\right)_{k\ge2},\qquad \|\Psi_i-\Psi_j\|^{2}=R(i,j)=\frac{C(i,j)}{\operatorname{vol}(G)}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 7d91883.
- NEG-16 (KV serving, end-task). *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task. `[refuted]`. `geometric-observation/claims/LEDGER.md:92` at 7d91883.
- NEG-15 (Bell boundary). *Query-conditioned hubness supplies a mechanism for Bell-inequality violation without action at a distance.* Refuted as a mechanism; the settings-as-queries reframing survives only as vocabulary. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:93` at 7d91883.
- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 7d91883.
- NEG-10. (prospective) The consumer-driven reconstruction-blind flip appears on any independent representation, e.g. embedding retrieval. `[refuted]`. `geometric-observation/claims/LEDGER.md:103` at 7d91883.
- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 7d91883.
- NEG-12. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction. `[refuted]`. `geometric-observation/claims/LEDGER.md:105` at 7d91883.
- NEG-13 → resolved. (GO-P-2026-026, prospective, real LLM) Appendix-E's omission floor is a rate-irreducible downstream wall on trained Llama read operators. `[missed]`. `geometric-observation/claims/LEDGER.md:106` at 7d91883.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 7d91883.

## first stated

Chapter 0 section 0.10 and chapter 3 section 3.3 of *Data Mining as Observation*, with the geodesic-rank reader of Volume 14 chapter 9, `geometric-observation/chapters/ch09_legibility.md:10-41`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.2 | condition (A2), tangential displacement | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `geometric-observation\chapters\ch09_legibility.md:42-54` |
| chapter 3 section 3.3 | resistance converges to 1 over d_i plus 1 over d_j, simplex argument, radius converges to 1 over root d_i | `the-angular-observer\theorem.md:110-146` |
| chapter 3 section 3.3 | radius against degree correlation 0.92 to 0.99 | `the-angular-observer\README.md:135-139` |
| chapter 3 section 3.3 | angle 0.92 flat in m, magnitude 0.03, full 0.75 decaying | `wolfram-observer-bridge\theorem.md:1-20`; `the-angular-observer\theorem.md:187-224` |
| chapter 3 section 3.3 | substrate table | `the-angular-observer\README.md:99-109` |
| chapter 3 section 3.3 | row normalization is the projection onto the read subspace of the geodesic-rank consumer | `geometric-observation\chapters\ch09_legibility.md:31-41`; `geometric-observation\chapters\ch03_historical_precursors.md:98-110` |
| chapter 3 section 3.3 | proven versus conjectured ledger, d at least 3, d equals 2 borderline, fixed-m conditional theorem, heat filter uniform, commute metric form false, Green-kernel rank limit for d at most 3, obstruction at d equals 4 | `the-angular-observer\theorem.md:84-107,147-224`; `the-angular-observer\README.md:150-185` |
| chapter 3 section 3.3 | the self-refuted v0.8 claim, NEG-1 | `the-angular-observer\README.md:170-175`; `geometric-observation\chapters\ch16_honest_negatives.md` NEG-1 |
| chapter 3 section 3.3 | hyperbolic rejected, curvature negative 0.98 to negative 0.14, trend 1.09 minus 0.157 d across 20 manifolds and 5 families | `the-angular-observer\README.md:111-147,183-185` |
| chapter 9 section 9.1 | the geodesic-rank reader discards the radius, row normalization is the angular projection | `geometric-observation\chapters\ch09_legibility.md:10-41`; `the-angular-observer\theorem.md:110-146` |
| chapter 9 section 9.2 | the battery, three new templates, frozen ratios, code hash, bars at least 10 of 12 and the dimension ordering, eccentricity scope | `the-angular-observer\PREREG_RECOGNIZER_BATTERY.md:1-80` |
| chapter 9 section 9.2 | 12 of 12, dimensions 1.81, 2.80, 1.74, angular Spearman ranges, eccentricity spreads, verdict confirmed, GO-P-2026-041 | `the-angular-observer\experiments\manifold-recovery\battery_result.json` |
| chapter 9 section 9.2 | causal set 0.57 with dimension 2.9 to 10.7, small world 0.45, control 0.01, rung 4 decay 0.747 to 0.679 below 0.75 | `the-angular-observer\README.md:99-109`; `wolfram-observer-bridge\rung4_scaledm_result.json`; `wolfram-observer-bridge\review-2.txt` |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |

## failures and corrections

- NEG-16 (KV serving, end-task), `[refuted]`. *At matched bits and matched reconstruction error, steering KV quantization error into the attention read subspace degrades LongBench task score by the registered floors on a deployed-class model.* Refuted at its registered effect sizes on this model and task.
- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.
- NEG-10, `[refuted]`. (prospective) The consumer-driven reconstruction-blind flip appears on any independent representation, e.g. embedding retrieval.
- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.
- NEG-12, `[refuted]`. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction.
- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- The length of the shortest path along edges between two nodes. It is zero from a node to itself, symmetric, one between adjacent nodes, and on a connected graph obeys the triangle inequality.
- The geodesic-rank reader reads only the ordering of these distances, so a strictly increasing transform of them leaves its nearest neighbour unchanged. That the angle of the spectral embedding carries the ordering and the radius carries degree is the measured claim of chapter 3, with the refuted commute-filter row beside it.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/GeodesicDistance.lean`, theorems `dist_self`, `dist_comm`, `dist_triangle`, `dist_adj`, `geodesic_rank_invariant`, at observation-data-mining 1c6cd64.

## used in

*Data Mining as Observation* chapters 0, 3, 9, 10.

## related

rank-faithful, laplacian, recognizer, bi-lipschitz

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 7d91883, observation-theory-campaigns 09cc919, theory-radar 37c4e6c, observation-data-mining 1c6cd64, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
