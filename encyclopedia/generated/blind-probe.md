# blind probe

**id.** blind-probe
**kind.** instrument

## definition

An instrument that recovers a consumer's read operator from calls to the consumer alone, without access to its gradients or its code. Chapters 11 and 12.

## equation

Book equation 0.8.

    g_j\;\approx\;\frac{C(x+h\,e_j)-C(x-h\,e_j)}{2h},\qquad j=1,\dots,d.

Book equation 0.9.

    P_C=\mathbb E\!\left[g\,g^{\top}\right],\qquad g=\nabla C(x).

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## ledger

- OT-3. Under subspace-confined second-order transcripts, fewer than d directions cannot identify a hidden leading eigenspace (theorem, adaptive to d−2 / oblivious to d−1); a known k₀-dim exclusion moves the cliff to exactly d−k₀ and never softens it. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:31` at 01e53bc.
- OT-6. The laws transfer outside compression with zero modification: blind-recovered P_C of a ranking consumer over embeddings; equal-Euclidean-energy perturbations; the trace picks the ranking-destroyer. `[predicted]`. `geometric-observation/claims/LEDGER.md:35` at 01e53bc.
- NEG-12. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction. `[refuted]`. `geometric-observation/claims/LEDGER.md:105` at 01e53bc.
- GO-B-Llama. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — blind probe on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:115` at 01e53bc.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 01e53bc.
- GO-B-Llama-rematch. Trained frontier LLM (Llama-3.2-3B), softmax-attention consumer — recon-matched dissociation on real post-RoPE keys `[predicted]`. `geometric-observation/claims/LEDGER.md:118` at 01e53bc.
- GO-B-legal (035→036). Legal-citation retrieval (CourtListener), cosine-ranking consumer, LaBSE embeddings — real large corpus, non-physical consumer `[predicted]`. `geometric-observation/claims/LEDGER.md:119` at 01e53bc.
- GO-EC-3. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe cost charged — capturing 94.6% of the known analytic optimum's gain on the positive-control arm (gate ≥ 75%) and improving 16.3% over the best consumer-agnostic policy on non-analytic consumers (gate ≥ 8%), with trace-matched ordering carried by the composition at 86.9% over 61 pairs (gate ≥ 65%). `[predicted]`. `geometric-observation/claims/LEDGER.md:162` at 01e53bc.

## first stated

readscope, the blind probe as a specified instrument, PyPI `readscope`, `readscope/PRINCIPLES.md` and `readscope/SPEC.md`, and Volume 14 chapter 10.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | `readscope\readscope\regimes.py:1-60` |
| chapter 2 section 2.4 | C-7, sixteen points in 128 dimensions, rank fifteen, near ten to the eleventh nats, refuses when samples do not exceed dimension, warns below five per dimension, loading is a property of two distributions | `readscope\SPEC.md:653-680` |
| chapter 2 section 2.4 | C-7b, 92.1 percent, fit range 0.89 to 91.64, 15 percent inside, maximum 1.9e12, endpoint attenuation 0.437, 202 of 240 at 1.0, refuses to extrapolate, loading is a warning | `readscope\SPEC.md:680-720`; `readscope\readscope\loading.py:136-219` |
| chapter 2 section 2.6 | 0.647 published, 1.000 recovered, weighted vs unweighted median 0.796 range 0.678 to 0.985, probe 1.000 on every cell, 36 cells, one cell at 0.985 | `readscope\SPEC.md:410-450` |
| chapter 2 section 2.6 | C-10, 24 to 576 queries, reference rank 24 to 128, 0.821 to 0.703 vs 0.647, 68 percent of distance closed, 0.174 to 0.056, probe 1.000000 on 16 cells, residual uncontrolled | `readscope\SPEC.md:450-500` |
| chapter 3 section 3.4 | chance overlap rank over dim reported with every reading | `readscope\README.md:200-222`; `readscope\readscope\metrics.py:31-99` |
| chapter 4 section 4.2 | water-filling formula, directions below the water get no bits, the surrogate caveat | `readscope\readscope\allocate.py:1-100` |
| chapter 4 section 4.2 | effective rank as participation ratio, energy rank | `readscope\readscope\spectrum.py:35-70` |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | `readscope\readscope\regimes.py:1-60` |
| chapter 8 section 8.3 | C-8 D5 mean absolute error 0.0000, every reading 1.000, C-7b saturation, the F-21 rule | `readscope\CALIBRATION.md` F-21 (about line 519) |
| chapter 8 section 8.4 | C-11c paired null, rank 2 positional 0.385 vs null 0.572, 0.615 vs 0.224, 14 of 16 cells, scope 16 cells one 3B model 192 positions | `readscope\SPEC.md:806-857`; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.7 | k over d table 1, 2, 2, 16, 16, 16 | `readscope\README.md:118-141`; `readscope\SPEC.md:243-285`, record `readscope\calibration\records\c2e-budget-law.json` |
| chapter 11 section 11.7 | rank-independent, 0.646 vs 0.366 at half dimension, never 0.90 below k equals d | `readscope\CALIBRATION.md:419-434` F-15 |
| chapter 11 section 11.7 | C-15 equal budget, 3072 observations, medians 0.02, 0.11, 0.05, 0.04, 1.0, 1.0, margin 0.883 vs 0.3, 0.062 to 0.057 at 8x | `readscope\SPEC.md:285-323`, record `readscope\calibration\records\c15-budget-surface.json`, `readscope\calibration\DECLARATION-C15.md` |
| chapter 11 section 11.7 | confinement theorem, side information moves the cliff to d minus k0, noisy cliff proved then measured | `readscope\PRINCIPLES.md:112-142`; `geometric-observation\crucible\OT3-THEOREM.md`; `geometric-observation\crucible\OT3-NOISY-THEOREM.md` |
| chapter 11 section 11.7 | 124 cells at resolution 1.000 at k over d 1.25, five families, linearity partial | `readscope\README.md:200-222` |
| chapter 11 section 11.9 | drift at rank one 0.667 vs null 0.933, sixteen cells | `readscope\CALIBRATION.md:600-660` F-24; `readscope\calibration\records\c11c-operator-drift.json` |
| chapter 11 section 11.9 | C-12 four bars, 40 documents, 512 tokens, 13.4 point difference, teacher forcing removes it, negative 0.015 vs 0.005, Spearman negative 0.13 at p 0.45, sign test p 0.42, verdict FAIL, feedback compounding | `readscope\calibration\records\c12-longgen-drift-sym.json`; `readscope\calibration\DECLARATION-C12.md` at commit `90e2ce2`; `readscope\SPEC.md:806-825` |

## failures and corrections

- NEG-12, `[refuted]`. (Gate B, prospective, real LLM) On a trained frontier attention layer the blind probe recovers the read operator above the sealed bar *and* projection beats reconstruction.
- `readscope/README.md:102-116` at c8d0289. What none of this changes: **the budget law, in its proven scope.** The cliff at `k = d` is a property of consumer calls, not FLOPs — a faster backend buys speed, never admission. The theorem behind it ([PRINCIPLES.md](PRINCIPLES.md), P3; OT-3) covers **subspace-confined directional designs at an operating point**, which is what this probe's per-point estimators are; it does not cover every allocation of calls across many operating points, and the sketch expectation `(1+1/k)·S + tr(S)/k·I` shares `S`'s eigenspaces at every `k` — so whether many cheap points can average their way back to the population operator was a **sample-complexity question, not a proven impossibility** — and C-15 has now measured it: at equal total consumer calls, sub-dimensional budgets do not catch up, at any graded rank, within 8× the full-dimension spend (SPEC.md, C-15). The cliff is a property of total calls in the measured range; only the far asymptotic regime remains open.

## conditions

- The probe recovers the read operator at one operating point from calls to the consumer alone, two calls per input dimension for a central difference.
- Its budget law is a theorem for subspace-confined designs at an operating point, which is what its per-point estimators are, and does not cover allocations of calls across many operating points.
- The probe refuses when samples do not exceed the dimension and warns below a stated margin, since the identifiability miss of chapter 2 came from reading it past that point.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/ProbeCliff.lean`, theorems `centralDiff_affine`, `centralDiff_basis`, `exists_blind_direction`, `indistinguishable`, `budget_cliff`, at observation-data-mining 17f3e9f.

## used in

*Data Mining as Observation* chapters 0, 1, 2, 4, 6, 7, 11, 12, 14.

## related

read-operator, budget-cliff, read-distortion, flip

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 0c2e3f9, theory-radar 37c4e6c, observation-data-mining 17f3e9f, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
