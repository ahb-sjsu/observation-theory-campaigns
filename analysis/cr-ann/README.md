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

## Real-data cell (2026-09-01, `cr_ann_realdata.py`): NEGATIVE — disclosed

20 Newsgroups (headers/footers/quotes stripped) → all-MiniLM-L6-v2 (384-d, L2-
normed) → linear consumer (logistic regression, test acc 0.661); P_C = WᵀW.
FAISS L2 candidate gen k=50 → rerank → 1-NN-via-retrieval.

| metric | L2 rerank | OT rerank |
|---|---|---|
| downstream accuracy | 0.656 | **0.637** (−0.019) |
| embedding recall@1 | 0.992 | 0.165 |
| mean L2 dist chosen | 0.901 | 1.001 |

**Dissociation FALSE.** OT reranking did **not** improve consumer performance; it
slightly hurt. Negative control (P_C = I): identical (0.656 = 0.656). The OT
prediction does **not** replicate here.

**Why (and why it sharpens, not refutes, the theory).** The L2 1-NN accuracy
(0.656) already ≈ the consumer classifier's own accuracy (0.661): a good general
encoder on a matched task produces an embedding space **already aligned** with the
consumer, so the L2-nearest neighbour is already class-consistent and there is
little misalignment to exploit. Consistent with the flip law — the dissociation
needs *misaligned* reads, which this matched encoder+task pair does not have. The
synthetic cell showed +0.42 precisely because it *forced* misalignment (label in
an L2-ignored subspace). Recorded as a boundary of the effect, not hidden.

**Consequence for the campaign.** The live hypothesis narrows: consumer-relative
reranking helps only under demonstrable embedding/consumer **misalignment**. The
next real-data cell must construct a genuinely misaligned case — a general
embedding + a consumer reading an **off-axis** attribute the embedding does not
emphasise (e.g. sentiment/formality/author when the embedding is topic-dominated;
a fine-grained attribute; or a task the encoder was not tuned for). The
prereg must therefore include a *measured* alignment condition, and test the
misaligned regime — a matched pair is predicted to show no effect.

## Status and next steps

Synthetic shakedown: dissociation confirmed (guaranteed-if-theory-holds; validates
pipeline + mechanism + control). Real-data matched cell: NEGATIVE (aligned →
no effect). The theory now predicts *when* the effect appears (misalignment) and
when it does not (alignment) — both arms tested.

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
