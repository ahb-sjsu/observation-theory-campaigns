# Laplacian

**id.** laplacian
**kind.** concept

## definition

A matrix built from a graph's edges whose eigenvectors, from the smallest eigenvalue up, are the smoothest functions on the graph. Equation 0.19.

## equation

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 0.20.

    \Psi_i=\left(\frac{u_k(i)}{\sqrt{\lambda_k\,d_i}}\right)_{k\ge2},\qquad \|\Psi_i-\Psi_j\|^{2}=R(i,j)=\frac{C(i,j)}{\operatorname{vol}(G)}.

Book equation 9.2.

    N(\lambda)=\#\{k:\lambda_k\le\lambda\}\ \sim\ C_d\,\lambda^{d/2}\qquad\Rightarrow\qquad d=2\,\frac{d\log N}{d\log\lambda}.

## ledger

- NEG-1. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter. `[refuted]`. `geometric-observation/claims/LEDGER.md:94` at 9f3829f.

## first stated

Chapter 0 section 0.10 of *Data Mining as Observation*, with the program's spectral work in Volume 14 chapter 9 and the-angular-observer.

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
| chapter 9 section 9.4 | explained ratios, effective rank 5.19 of 8, convergence with a second method, property of the representation not the space | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:10-18` |
| chapter 11 section 11.1 | condition (A2), cosine satisfies it, post-rotary keys do not, the cone below cell size | `turboquant-pro\docs\KV_KEYS_FINDING.md:61-86`; `the-angular-observer\README.md:26-31` |
| chapter 14 section 14.3 | floor 0.08 to 0.12, balanced resample 3001 items, identity attack 0.237 with interval 0.20 to 0.28 on 289, sexual 0.204, threat 0.093 retracted, first pass 18 positives, 87.7 and 1.4 percent | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:20-64` |
| chapter 14 section 14.3 | contraction 0.779 to 0.863, 77 of 1600, 4.8 percent, 0.872 to 0.863, weight 2.69 | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:66-99` |
| chapter 14 section 14.5 | the contraction formula fairness minus the general component | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:90-99` |
| chapter 14 section 14.7 | 51 percent moderated at 80 and 95 percent precision on the balanced set | `gtc-prototype\docs\SPECTRUM_FINDINGS.md:84-88` |

## failures and corrections

- NEG-1, `[refuted]`. Fixed-scale, uniform-in-m bi-Lipschitz for the commute filter.

## conditions

- A matrix built from a graph's edges whose quadratic form is half the weighted sum of squared differences across edges, so it is nonnegative, zero on every constant, and positive on any function that differs across an edge of positive weight. The eigenvectors from the smallest eigenvalue up are therefore the smoothest functions on the graph.
- The file states the unnormalized form, and equation 0.19's normalized form is the same quadratic form in rescaled coordinates. The commute-time scaling of the embedding and the uniform bi-Lipschitz claim for the commute filter are in the ledger, the second refuted.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/Laplacian.lean`, theorems `quad_eq`, `quad_nonneg`, `quad_const`, `quad_pos_of_edge`, at observation-data-mining 5bb2c0d.

## used in

*Data Mining as Observation* chapters 0, 3, 4, 9, 11.

## related

intrinsic-dimension, recognizer, rank-faithful, bi-lipschitz

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 859676b, theory-radar 37c4e6c, observation-data-mining 5bb2c0d, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
