# budget

**id.** budget
**kind.** concept

![The third element of the observer, what the consumer can spend.](../figures/budget.svg)

## definition

The third element of an observer. The bits, rows, calls, seconds, or dollars a consumer may spend. Chapter 1.

**Example.** A probe with 2d calls at d equal to 16 spends 32 evaluations for one operating point.

## equation

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## conditions

- The budget is the bits, rows, calls, seconds, or dollars a consumer may spend. It bounds what of the read operator can be measured and used, and changes the operator only when it changes the consumer.
- Comparisons are made at matched budget. A verdict at a fixed budget can invert under budget matching, and the ledger carries the case.
- For a probe the budget is consumer calls, and recovery of the read operator is a cliff at the full dimension of the space.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

- *measures.* GO-4 `[replicated]`. Fixed-budget verdicts invert under budget-matched observation, per the wavelength mechanism. [`geometric-observation/claims/LEDGER.md:66`](https://github.com/ahb-sjsu/geometric-observation/blob/fc6b378/claims/LEDGER.md#L66).

## first stated

Volume 14, chapter 4 for the triple and chapter 7 for cost, `geometric-observation/chapters/ch07_cost.md`, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 4 section 4.4 | GO-4 budget inversion, fixed m 10 rises, matched m 121, 126, 159 collapses, 3 seeds | [`geometric-observation/claims/LEDGER.md`](https://github.com/ahb-sjsu/geometric-observation/blob/fc6b378/claims/LEDGER.md) row GO-4 |

## failures and corrections

none

## invariance envelope

**Survived.**

- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: A single-direction probe along coordinate e_i at size rho is reported identifiable at budget B exactly when P_ii > B^2 / rho^2, and a ladder of sizes brackets P_ii between B^2 / r_hi^2 and B^2 / r_lo^2 (article Theorem 2(b), Corollary 3). `experiments/DISCOVERY-TRACK.md, D1 record; experiments/OD/D1/grade.json axis`. Witness: exact in every evaluator of all fifteen World A cells (three worlds, five budgets, 20 evaluators each) on the run seed, as in every pilot. Absorbed by: .
- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: Where lambda_min rho^2 < B^2 < lambda_max rho^2 fails the oracle is constant in every direction; where it holds it need not be non-constant in finite samples. `experiments/OD/D1/grade.json, B2 entries`. Witness: constant in all 20 evaluators at n = 5, B = 2 (no crossing, B^2 = lambda_max rho^2) and at n = 8 positive definite, B = 0.25 (a crossing by theory so thin that 960 random directions in each of 20 evaluators all answered distinguishable). Absorbed by: .
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: For a positive definite read operator with spectrum in [a, b] the observational and classical window exponents differ by at most log(b / a) / (2 (T - t0)) (article Proposition 1, lean/GET/Horizon.lean). `experiments/DISCOVERY-TRACK.md, D3 record; experiments/OD/D3/grade.json exact E1`. Witness: 3,200 of 3,200 windows on Lorenz-63 and Lorenz-96 under an anisotropic observer with b / a = 16 and 4; the worst ratio to the bound 0.96 in the pilot, so the bound is nearly attained. Absorbed by: .
- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: The horizon T_O(B) is non-decreasing in B, lies between the Euclidean horizons at B / sqrt(b) and B / sqrt(a) for a positive definite observer, and is never earlier than the Euclidean horizon for a projection. `experiments/OD/D3/grade.json exact H1`. Witness: 8,960 of 8,960 checks. Absorbed by: .
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: An observer's horizon offset from the full reader at budget B equals the first-passage time Delta_O(B) = E_s[inf{t >= s : L(t) - L(s) + g_O(t) >= log B} - inf{t >= s : L(t) - L(s) >= log B}] of its read-fraction process along the leading Lyapunov direction, computed on an independent long trajectory (the horizon offset law). `experiments/DISCOVERY-TRACK.md, D3v2 record; experiments/OD/D3v2/grade.json`. Witness: all 22 cells (eleven observers of Lorenz-63 and Lorenz-96 at B = 1000 and 10000) within 0.259 time units, largest error 0.149; signs and the Lorenz-63 order exact; the symmetric site blocks of Lorenz-96 equal within 0.07; anisotropic offsets inside the D3 bracket; the constant-fraction approximation -E[log f_O] / lambda_1, refuted by the first probe, wrong by 0.09 to 1.0 on the same rows. Absorbed by: . Revision: the law replaced the constant-fraction statement before any pilot; recorded in the registration's Section 7.
- OD:simulation-resolution, change of the simulation resolution N at fixed observation budget B, for dynamical systems. Claim: The horizon offset law holds across a change of dynamical system, from Lorenz-63 (exponent 0.906) to Lorenz-96 at N = 40 (exponent 1.699). `experiments/OD/D3v2/grade.json O1 by world`. Witness: Lorenz-96 errors 0.001 to 0.138 over four observers and two budgets, Lorenz-63 0.014 to 0.149 over seven. Absorbed by: .

**Boundary measured.**

- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: Mixed probes at one radius, where the sphere crosses the ellipsoid substantially, recover the read operator up to the pencil s P + (1 - s)(B^2 / rho^2) I, below-threshold eigenvalues included, with Frobenius, above-threshold and below-threshold medians at most 0.30 of chance at 960 queries. `experiments/DISCOVERY-TRACK.md, D1 record; experiments/OD/D1/grade.json mixed`. Boundary: held in five of six well-crossed cells (Frobenius 0.045 to 0.111 of chance, above 0.055 to 0.111, below 0.037 to 0.172); in the positive definite world at B = 1 the Frobenius ratio 0.198 and the below ratio 0.068 held and the above ratio was 0.303 against 0.30. Witness: the tolerance was fixed as the pilot's own maximum in that same cell (0.299) rounded up to two decimals, so it carried no margin for a fresh seed; the estimator, the crossing and the recovery are unchanged between pilot and run. Absorbed by: declaration. Revision: none for the claim; for later gates, fix a tolerance as a declared multiple of the pilot's maximum.
- OD:observer-family, change of observer within a declared family: read operators of declared spectrum, coordinate subsets, coarsenings, and learned consumers' recovered read operators. Claim: At fixed budget the horizon depends on the observer where no symmetry of the flow relates the observers (Lorenz-63, x against z) and not where one does (Lorenz-96, one block of ten sites against the next). `experiments/DISCOVERY-TRACK.md, D3 record; experiments/OD/D3/grade.json H2`. Boundary: x later than z for the same perturbation in 77, 78, 70 and 64 percent of pairs at B = 10, 100, 1000, 10000 with sign-test p 0.0000, 0.0000, 0.0022 and 0.033 against the registered 0.01 at every budget; the Lorenz-96 control at p 0.11 to 0.86. Witness: the paired effect weakens as the budget grows and the perturbation aligns with the leading direction for longer, so a fixed per-budget level over the ladder was the wrong registration, not the wrong claim; the pilot at the same budget had 77 percent and p below 0.0001. Absorbed by: declaration. Revision: none for the claim; for later gates, declare the level per budget or grade the ladder as a whole.
- OD:budget, change of the observation budget B at fixed consumer and output metric. Claim: Coarsening the observer's resolution changes hub polarity monotonically in the resolution, and a resolution of a tenth of the nearest-neighbour distance changes little (exploratory, reported). `experiments/OD/D2/grade.json B1`. Boundary: monotone in all four sweeps; at a tenth of the neighbour distance 12 percent of Gaussian points and 6 percent of Wikipedia points change polarity under the isotropic observer, at a quarter 24 and 79 percent, against 4 to 7 percent under the anisotropic observer. Witness: the finite budget is a first-order effect on real embeddings under an isotropic reader; not graded, as declared. Absorbed by: declaration.


## machine checked

[`lean/DataMiningAsObservation/ProbeCliff.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/c149a10/lean/DataMiningAsObservation/ProbeCliff.lean), theorems `centralDiff_affine`, `centralDiff_basis`, `exists_blind_direction`, `indistinguishable`, `budget_cliff`, at observation-data-mining c149a10; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/c149a10/chapters/machine_checked.md).

## used in

*Data Mining as Observation* chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.

## related

observer, water-filling, budget-cliff, coverage

## see also

Book equations stated beside the entry's terms, not defining it: 1.1, 0.13.

Ledger rows that cite the entry's records without naming it: OT-3, GO-12.

Sources-table rows that share a record with the entry without naming it: chapter 4 section 4.2, chapter 11 section 11.7, chapter 13 section 13.6.

## status

Generated 2026-09-09 by `encyclopedia/generate.py`; book at observation-data-mining c149a10; the commit of every record is listed in the encyclopedia's provenance.
