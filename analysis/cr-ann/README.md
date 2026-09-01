# Consumer-relative ANN — shakedown (UNSEALED, exploratory)

New OT campaign (owner idea 2026-09-01). FAISS answers "what does *close* mean?"
with L2 / inner product; OT says the question is **close to whom?** — the
downstream consumer C. Rank candidates by the consumer's read operator:

    d_C(x, x_j)^2 = (x - x_j)^T P_C(x) (x - x_j),   P_C(x) = J(x)^T J(x)

(the Jacobian pullback of the consumer's output; = A^T A for a linear readout A).
This is turboquant-pro's P_C / `consumer_distortion` thesis on the *retrieval*
surface: two consumers of the same embedding DB legitimately get different
neighborhoods.

## Prediction under test (preregisterable)

At fixed candidate budget k, reranking FAISS L2 candidates by d_C improves
downstream consumer performance **despite worsening** ordinary embedding-space
fidelity. The dissociation is the claim (same shape as KV-keys: 0.995 cosine /
~1e4 perplexity, and the AICSI cell: reconstruction wins / consumer false-clears).

## Design (no FAISS modification)

FAISS `IndexFlatL2` candidate gen (top-k) -> rerank {L2 | OT d_C} -> 1-NN class
prediction from the reranked top-1. Controlled substrate: embeddings in R^32, a
4-dim relevant subspace A drives an 8-class label; irrelevant dims carry larger
variance so L2 is distractor-dominated. `cr_ann_shakedown.py`.

## Shakedown result (2026-09-01, `cr_ann_shakedown.py`, seed 0)

Backend: FAISS IndexFlatL2. D=32, M=4, N_db=20000, N_q=2000, k=50, 8 classes.

| metric | L2 rerank | OT rerank (P_C = A^T A) |
|---|---|---|
| downstream accuracy | 0.261 | **0.676** (+0.415) |
| embedding recall@1 (chose true L2-nearest) | 1.000 | **0.027** |
| mean L2 distance of chosen neighbour | 12.70 | 14.75 (farther) |

**Dissociation confirmed:** consumer performance up, embedding fidelity down, at
fixed k.

**Negative control (isotropic P_C = I):** accuracy 0.239 = 0.239, recall@1
1.000 = 1.000 — identical, zero dissociation. The effect requires genuine
consumer/embedding misalignment (the flip law), not a code artifact.

**Anisotropy sweep:** the accuracy gain holds +0.28 → +0.43 across
distractor/relevant variance ratios 1 → 16; robust and structural (label lives
in 4 of 32 dims).

## Status and next steps

Shakedown only — the synthetic substrate makes the dissociation *guaranteed if
the theory holds*; it validates the pipeline, the mechanism, and the negative
control, not real-world magnitude (like the other cells' sim modes).

1. **Real-data cell:** real embeddings (e.g. sentence embeddings) + a real
   downstream consumer whose P_C(x) = J(x)^T J(x) is computed from the actual
   model (linear probe / classifier head). The real test: does the dissociation
   appear on real embeddings, and how large.
2. **Prereg** (now de-risked): P_C = J^T J definition; the isotropic negative
   control; the dissociation bars; and the candidate-generation **recall
   ceiling** measurement (rerank can only reorder what L2 retrieved — if the
   consumer-relevant neighbours are outside the budget-k L2 set, Phase 1 rerank
   cannot recover them; if the ceiling bites, Phase 2 = a consumer-relative
   *index*).
3. **Prior-art honesty:** learned/Mahalanobis metrics, local metric learning,
   and IR/RAG cross-encoder rerankers all exist. The contribution is the OT
   framing (P_C = the consumer's own read operator, derived not learned) + the
   measured dissociation, NOT "a new metric" or "reranking." WebSearch before
   claiming novelty.

Natural productization home: turboquant-pro (ships read operators,
`consumer_distortion`, `TurboQuantFAISS`, the readscope bridge).
