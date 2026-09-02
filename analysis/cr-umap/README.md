# OT-UMAP — consumer-indexed faithfulness (UNSEALED, exploratory)

Owner idea 2026-09-02: PyNNDescent builds k-NN graphs under arbitrary metrics,
and OT says the input-space metric should not be globally fixed at all — a
consumer-induced P_C(x) is locally induced geometry. The campaign question:
does preserving consumer-induced neighborhoods produce an embedding that is
objectively worse under conventional geometric metrics but better for what the
downstream observer can distinguish? The larger claim: there is no
observer-independent answer to whether a dimensionality reduction is faithful.

## Shakedown (2026-09-02, `cr_umap_shakedown.py`, predictions committed at 8640669 BEFORE the run)

Constant-P cell, factorized (euclidean UMAP on consumer-whitened data;
disclosed as Mahalanobis-adjacent — the position-dependent P_C(x) successor is
what needs callable metrics). 20NG MiniLM, 6,000 embedded points; probes fit
on the disjoint test split; P = WᵀW/‖·‖₂ + 0.05·I.

Consumer bookkeeping (conditional law): topic D 0.666 / A 0.684 / **H −0.019**
(aligned, the null arm); length D 0.885 / A 0.719 / **H +0.165**; pc200
D 0.960 / A 0.618 / **H +0.341**.

| embedding | trust | knn10-rec | Shepard | topic | length | pc200 |
|---|---|---|---|---|---|---|
| L2 | 0.923 | 0.192 | 0.336 | 0.630 | 0.604 | 0.573 |
| iso control | 0.923 | 0.192 | 0.336 | 0.630 | 0.604 | 0.573 |
| OT-topic | 0.907 | 0.140 | 0.342 | **0.637** | 0.613 | 0.539 |
| OT-length | 0.917 | 0.177 | 0.343 | 0.610 | **0.724** | 0.551 |
| OT-pc200 | 0.924 | 0.191 | 0.339 | 0.620 | 0.612 | **0.588** |
| proj-length (ε=0) | 0.553 | 0.007 | 0.040 | 0.065 | 0.878 | 0.528 |
| logit-length | 0.553 | 0.005 | 0.051 | 0.066 | 0.877 | 0.536 |

**Predictions graded (disclosed both ways):**

- **P1 dissociation — PARTIAL.** OT-length gains +0.120 on its consumer
  (≥ the +0.05 bar) and loses on trustworthiness and kNN-recall, but Shepard
  did NOT degrade (0.343 vs 0.336): at ε = 0.05 the geometric cost is a
  *neighborhood* cost, not a global-distance cost. The pre-stated "all three
  conventional metrics" clause fails on Shepard, marginally. OT-pc200 gains
  only +0.015 despite H = 0.341 — see the instrument finding below.
- **P2 inversion — the core HOLDS, one sub-clause marginal.** Diagonal
  dominance: every consumer's best non-degenerate embedding is its own OT
  embedding (topic → OT-topic 0.637; length → OT-length 0.724; pc200 →
  OT-pc200 0.588), the two misaligned observers order {OT-length, OT-pc200}
  oppositely, and no embedding tops two observer columns. "No
  observer-independent faithfulness" is instantiated, shakedown-grade. The
  sub-clause "each OT embedding is worse than L2 for the other consumer" held
  for OT-length (pc200 0.551 < 0.573) but not for OT-pc200 on length
  (0.612 vs 0.604, within noise).
- **P3 matched null — PASS.** OT-topic ≈ L2 on topic (+0.007), as the
  conditional law predicts at H ≈ 0. Note it still pays a small geometric cost
  (trust 0.907, recall 0.140) for nothing: whitening by an aligned consumer
  buys no headroom.
- **P4 controls — PASS.** iso ≡ L2 identically (pipeline exact). The
  projection/logit baselines are the disclosed degenerate case: length 0.878
  with everything else destroyed (topic 0.065, trust 0.553). The blended
  OT-length is NOT that: it reaches 0.724 on length while keeping topic at
  0.610 and trust at 0.917 — consumer structure gained without discarding the
  ambient manifold, which is the anti-triviality evidence.

**Instrument finding (for the successor and any prereg):** the ε-blend
under-weights low-raw-variance consumer directions. pc200's direction carries
tiny ambient variance, so at ε = 0.05 the whitened signal stays swamped by 383
ambient dimensions and only +0.015 of its H = 0.341 converts; length's
direction has natural variance and converts +0.120 of 0.165. The successor
pins ε per consumer by normalizing the consumer signal's whitened variance (or
sweeps ε as a registered covariate). Same lesson class as CR-ANN's headroom
instrument: measure the knob, don't guess it.

## Next cells

1. ε-normalized rerun (does pc200 convert once the blend is signal-scaled?).
2. **Position-dependent P_C(x)** = J(x)ᵀJ(x) from a nonlinear head — genuinely
   local geometry, no factorization, PyNNDescent callable metric with J(x)
   packed into the vectors; UMAP via `precomputed_knn`.
3. Consumer-relative intrinsic dimension / "no manifold under this read"
   (ties to the angular-observer program).
4. Prereg (V2-instrument inherited: cross-fit D/A/H, matched-null arm, honest
   conversion constants; prior-art pass: supervised/parametric UMAP, local
   metric learning, DR no-free-lunch, arXiv:2506.01599).
