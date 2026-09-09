# read operator

**id.** read-operator
**kind.** concept

![The averaged outer product of the sensitivity with itself.](../figures/read-operator.svg)

## definition

The average outer product of a consumer's sensitivity over a dataset, an average of local linearizations whose kernel is the set of directions unread at almost every row of the workload. Its range is the read subspace and its kernel is the nuisance. Equations 0.9 and 0.11.

**Example.** The affine consumer 3x1 + 4x2 has read operator with rows (9, 12) and (12, 16) at every row.

**Known as, or related to prior art.** In the scalar Euclidean-output case the read operator is the active-subspace matrix of Constantine and Gleich, the covariance of the gradient. What the program adds is the pullback through the output metric, the observer triple, the budget, and the audit discipline.

## equation

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 0.11.

    P_C(x)=J(x)^{\top}G\big(C(x)\big)\,J(x),\qquad J(x)=\frac{\partial C}{\partial x}(x),\qquad \bar P_{C,\mu}=\mathbb E_{\mu}\!\left[P_C(x)\right].

Book equation 2.1.

    P_{C_2\circ C_1}(x)=J_1(x)^{\top}\,P_{C_2}\big(C_1(x)\big)\,J_1(x),\qquad \operatorname{rank}P_{C_2\circ C_1}(x)\le\operatorname{rank}P_{C_2}\big(C_1(x)\big)\quad\text{at each row } x.

Book equation 6.1.

    s(x)=w\cdot x+b,\qquad P_C=\mathbb E\big[\sigma'(s)^{2}\big]\,w\,w^{\top},\qquad \operatorname{rank}P_C=1.

## conditions

- Each local operator is positive semidefinite, so the kernel of the workload average is the intersection of the local kernels up to sets of rows of measure zero, and an average-null direction is locally unread at almost every row of that workload.
- The average depends on the workload it was taken over and is written with that workload where the difference matters.
- Its off-diagonal entries are co-sensitivities, how two features' sensitivities vary together across rows, and not interactions, which are cross-partials and live in the Hessian.
- The metric in the vector-output form is the local geometry of the output metric where that metric has a local quadratic representation. A dataset-level loss has none, and the operator is then taken on the score with the identity geometry.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

- *measures.* GO-EC-3 `[predicted]`. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe … [`geometric-observation/claims/LEDGER.md:162`](https://github.com/ahb-sjsu/geometric-observation/blob/ab4a0db/claims/LEDGER.md#L162).

## first stated

Volume 14, chapters 4 and 5, `geometric-observation/chapters/ch04_the_observer_triple.md:9-60` and `geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:7-48`, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 1 section 1.2 | the observer triple, read subspace, nuisance, same read operator means same read geometry | [`geometric-observation/chapters/ch04_the_observer_triple.md:9-60`](https://github.com/ahb-sjsu/geometric-observation/blob/ab4a0db/chapters/ch04_the_observer_triple.md#L9-L60); [`geometric-observation/OBSERVATION.md:1-10`](https://github.com/ahb-sjsu/geometric-observation/blob/ab4a0db/OBSERVATION.md#L1-L10) |

## failures and corrections

- [`geometric-observation/chapters/ch05_the_read_metric_and_the_quotient.md:42-47`](https://github.com/ahb-sjsu/geometric-observation/blob/ab4a0db/chapters/ch05_the_read_metric_and_the_quotient.md#L42-L47) at ab4a0db. **Operating-point dependence.** $P_C$ is a *local* object — it depends on $x_0$ through $J$. For a linear consumer it is global; for a nonlinear one it varies over $X$, and the honest version of every result carries $P_C$ as a field, not a constant. The blind probe of Chapter 10 recovers $P_C$ *at* an operating point precisely because it is local; averaging it over a data distribution gives the $\bar P_C$ that enters the alignment law $\kappa$ (Chapter 12).

## invariance envelope

**Survived.**

- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: A single-direction probe along coordinate e_i at size rho is reported identifiable at budget B exactly when P_ii > B^2 / rho^2, and a ladder of sizes brackets P_ii between B^2 / r_hi^2 and B^2 / r_lo^2 (article Theorem 2(b), Corollary 3). `experiments/DISCOVERY-TRACK.md, D1 record; experiments/OD/D1/grade.json axis`. Witness: exact in every evaluator of all fifteen World A cells (three worlds, five budgets, 20 evaluators each) on the run seed, as in every pilot. Absorbed by: .
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: In a positive definite world the analytic centre returns the pencil's end P* = s* P + (1 - s*) c I, s* = c / (c - lambda_min), so the estimate is nearer P* than P (article Corollary 4). `experiments/OD/D1/grade.json, B4; experiments/OD/D1/pencil_probe.json`. Witness: nearer P* in 20 of 20 evaluators at B = 1 and at B = 1.5 on the run seed (Frobenius 0.223 against P, 0.181 against P*; 0.117 against 0.102), 20 of 20 in the third pilot, 6 of 6 cells in the pre-seal probe; in the kernel worlds the pencil's end is P itself and the two errors coincide. Absorbed by: .
- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: Where lambda_min rho^2 < B^2 < lambda_max rho^2 fails the oracle is constant in every direction; where it holds it need not be non-constant in finite samples. `experiments/OD/D1/grade.json, B2 entries`. Witness: constant in all 20 evaluators at n = 5, B = 2 (no crossing, B^2 = lambda_max rho^2) and at n = 8 positive definite, B = 0.25 (a crossing by theory so thin that 960 random directions in each of 20 evaluators all answered distinguishable). Absorbed by: .
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: For a positive definite read operator with spectrum in [a, b] the observational and classical window exponents differ by at most log(b / a) / (2 (T - t0)) (article Proposition 1, lean/GET/Horizon.lean). `experiments/DISCOVERY-TRACK.md, D3 record; experiments/OD/D3/grade.json exact E1`. Witness: 3,200 of 3,200 windows on Lorenz-63 and Lorenz-96 under an anisotropic observer with b / a = 16 and 4; the worst ratio to the bound 0.96 in the pilot, so the bound is nearly attained. Absorbed by: .
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: An observer with a kernel reads a smaller exponent than the classical one when an unread direction grows faster (World K, mu = 2), the same when it grows slower (mu = 1/2), and a kernel-started perturbation reads a transiently larger exponent that converges. `experiments/OD/D3/grade.json K1, K1c, K2, K3`. Witness: gap 0.82 to 1.25 in 64 of 64 starts at mu = 2 with the classical exponent at its predicted 1.965; control equal within 0.0072; kernel starts larger on the first window in 83 to 98 percent of starts with median excess +1.5 to +3.5 falling to 0.09 to 0.17 by T = 20; generic starts under every projection within 0.035 of the classical exponent at T = 20. Absorbed by: .
- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: The horizon T_O(B) is non-decreasing in B, lies between the Euclidean horizons at B / sqrt(b) and B / sqrt(a) for a positive definite observer, and is never earlier than the Euclidean horizon for a projection. `experiments/OD/D3/grade.json exact H1`. Witness: 8,960 of 8,960 checks. Absorbed by: .
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: An observer's horizon offset from the full reader at budget B equals the first-passage time Delta_O(B) = E_s[inf{t >= s : L(t) - L(s) + g_O(t) >= log B} - inf{t >= s : L(t) - L(s) >= log B}] of its read-fraction process along the leading Lyapunov direction, computed on an independent long trajectory (the horizon offset law). `experiments/DISCOVERY-TRACK.md, D3v2 record; experiments/OD/D3v2/grade.json`. Witness: all 22 cells (eleven observers of Lorenz-63 and Lorenz-96 at B = 1000 and 10000) within 0.259 time units, largest error 0.149; signs and the Lorenz-63 order exact; the symmetric site blocks of Lorenz-96 equal within 0.07; anisotropic offsets inside the D3 bracket; the constant-fraction approximation -E[log f_O] / lambda_1, refuted by the first probe, wrong by 0.09 to 1.0 on the same rows. Absorbed by: . Revision: the law replaced the constant-fraction statement before any pilot; recorded in the registration's Section 7.

**Boundary measured.**

- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: Mixed probes at one radius, where the sphere crosses the ellipsoid substantially, recover the read operator up to the pencil s P + (1 - s)(B^2 / rho^2) I, below-threshold eigenvalues included, with Frobenius, above-threshold and below-threshold medians at most 0.30 of chance at 960 queries. `experiments/DISCOVERY-TRACK.md, D1 record; experiments/OD/D1/grade.json mixed`. Boundary: held in five of six well-crossed cells (Frobenius 0.045 to 0.111 of chance, above 0.055 to 0.111, below 0.037 to 0.172); in the positive definite world at B = 1 the Frobenius ratio 0.198 and the below ratio 0.068 held and the above ratio was 0.303 against 0.30. Witness: the tolerance was fixed as the pilot's own maximum in that same cell (0.299) rounded up to two decimals, so it carried no margin for a fresh seed; the estimator, the crossing and the recovery are unchanged between pilot and run. Absorbed by: declaration. Revision: none for the claim; for later gates, fix a tolerance as a declared multiple of the pilot's maximum.
- OD:world-transfer, transfer of a law frozen on synthetic worlds to embedding corpora, ANN corpora, and dynamical state spaces without retuning. Claim: The hubness law frozen on seven synthetic families, log(1 + skew) = 2.811 + 0.0047 d_ent - 0.0928 / cv_d - 2.461 sqrt(top_share), predicts hubness on families it was not discovered on, on real embeddings and at larger N within declared multiples of its pilot error, and beats the nominal-dimension formula and the frozen D2 law. `experiments/DISCOVERY-TRACK.md, D2v2 record; experiments/OD/D2v2/grade.json`. Boundary: survives on all eight unseen synthetic families (0.37 to 1.41 against 1.84), on SIFT base and queries (1.27, 0.75) and within 3 REF on Wikipedia (2.54, 2.37 against 2.77); misses the heavy-tail and Wikipedia scale cells (2.26, 2.55 against 1.84) and loses to a constant in k and N on the Wikipedia slices (1.41, 1.29); beats the D2 law in 14 of 16 transfer worlds and both competitors pooled (1.45 against 2.20 and 2.85). Witness: Wikipedia embeddings have TwoNN intrinsic dimension 8 to 20 at entropy dimension up to 320 and skewness at most 1.5; the intrinsic dimension was in the declared pool and the search dropped it, since on full-dimensional discovery families it duplicates the spectral dimension. Absorbed by: declaration. Revision: D2v3 would put clouds on embedded manifolds into the discovery families so that the intrinsic dimension becomes informative; not registered here.
- OD:world-transfer, transfer of a law frozen on synthetic worlds to embedding corpora, ANN corpora, and dynamical state spaces without retuning. Claim: The hubness law frozen on eleven families including four manifold families, log(1 + skew) = -1.463 - 0.013 / cv_knn + 0.748 log(id_twonn) + 0.069 sqrt(d_eff), predicts hubness on unseen families and manifolds, on real embeddings and at larger N within declared multiples of its pilot error, and beats the nominal formula and the frozen D2 and D2v2 laws. `experiments/DISCOVERY-TRACK.md, D2v3 record; experiments/OD/D2v3/grade.json`. Boundary: real corpora within REF for the first time (Wikipedia 1.00 and 0.21, SIFT 0.44 and 0.37 against 2.24); eight of ten unseen worlds within 1.49 and the group pooled at 1.18 against 1.12; Laplace (1.93) and the 256-dimensional cube (2.69) outside; heavy tails at N = 16000 at 1.91 against 1.49; beats all three competitors pooled (1.05 against 3.58, 2.77, 1.69) and within every group. Witness: the intrinsic dimension became the law's main term once the discovery set held clouds whose intrinsic dimension sits below their spectral one; the misses are where TwoNN leaves its calibrated regime (125 on a 4,000-point cube in 256 dimensions) or where tails outrun every training family. Absorbed by: declaration. Revision: a D2v4 would bound the intrinsic-dimension term or add full-dimensional worlds at d = 256 and heavier tails to the discovery set; not registered here.

**Failed, with witness.**

- OD:world-transfer, transfer of a law frozen on synthetic worlds to embedding corpora, ANN corpora, and dynamical state spaces without retuning. Claim: The hubness law frozen on Gaussian clouds, skew = -0.026 + 0.421 / cv_d + 0.817 sqrt(d_eff) / k, predicts hubness on distributions it was not discovered on, on real embeddings and at larger N, within declared multiples of its pilot error. `experiments/DISCOVERY-TRACK.md, D2 record; experiments/OD/D2/grade.json`. Witness: fresh seeds of the discovery family replicate (0.93 against 1.19) but uniform balls (error up to 4.5, the law over-predicting by up to 2.8), Student t (under-predicting by up to 2.4) and Wikipedia embeddings (5.3, measured skewness at most 1.1 at effective dimension 156 where the law says 10) fail; the nominal-dimension competitor is worse pooled (14.8 against 2.9) and better on the unseen synthetic group alone (1.74 against 2.45). Absorbed by: none. Revision: not proposed here: a successor would need a shape variable that separates tails and roundness from the spectrum and a discovery set of more than one family.


## machine checked

[`lean/DataMiningAsObservation/ReadOperator.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/95af30c/lean/DataMiningAsObservation/ReadOperator.lean), theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining 95af30c; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/95af30c/chapters/machine_checked.md).

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 7, 8, 11, 12, 13, 14.

## related

read-distortion, quotient, identity-reader, blind-probe, flip

## see also

Ledger rows that cite the entry's records without naming it: OT-7, GO-1.

Sources-table rows that share a record with the entry without naming it: chapter 2 section 2.2, chapter 2 section 2.3, chapter 6 section 6.1, chapter 6 section 6.2, chapter 11 section 11.7.

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining 95af30c; the commit of every record is listed in the encyclopedia's provenance.
