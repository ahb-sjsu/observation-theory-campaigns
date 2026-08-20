# LM track prior-art sweep — query-only read geometry for LLM consumers

Swept 2026-08-19 (fresh-context web agent, adversarial-concession
posture). Feeds the novelty section of any LM-track preregistration.
Quote-verification of individual entries is owed before any seal cites
one for a specific claim (the EC-5 discipline).

## Candidate claim swept

For a pipeline where an LLM consumes a serialized numeric/structured
STATE, a quadratic read geometry P_C = JᵀGJ of the LLM's task loss can
be recovered from the FROZEN BLACK-BOX model by query-only
finite-difference probing (logprob readout; no gradients, no attention
access), composed with an explicit uncertainty/quantization covariance
Σ as tr(P_C Σ), and used to PROSPECTIVELY allocate token/precision
budget across state components at matched total budgets, probe cost
charged, validated out of sample.

## Nearest neighbors by line (concessions first)

1. **Prompt/context compression.** LLMLingua (EMNLP 2023) /
   LongLLMLingua (ACL 2024): proxy-LM perplexity token pruning with
   budget control; LongLLMLingua is question-aware — the closest
   compression work to consumer-task-awareness, but white-box proxy
   signal, token-drop only. **CompactPrompt (ICAIF 2025 WS,
   arXiv:2510.18043): the nearest applied neighbor** — uniform
   quantization of numeric prompt fields under error bounds; uniform
   and sensitivity-blind, no probed metric, no Σ composition.
2. **KV-cache compression** (H2O NeurIPS'23, SnapKV NeurIPS'24,
   StreamingLLM ICLR'24, KIVI ICML'24): internal-attention importance
   or positional heuristics on the model's OWN cache; white-box,
   reactive, not consumer-task-derived, not over external state.
3. **Numeric serialization**: tokenization-scheme effects
   (arXiv:2402.14903), xVal continuous encodings (training-time),
   precision-limit measurements (arXiv:2510.08009, 2511.08022) —
   measurement, never allocation policy.
4. **RAG budgeting**: Know Before You Fetch (arXiv:2606.29959)
   prospective logprob-calibrated budget routing; budget-aware active
   RAG (arXiv:2607.24010) charges retrieval cost against gains. Scalar
   per-decision utilities; no per-component geometry, no Σ.
5. **White-box attribution counterpart**: IG (ICML 2017), attention
   rollout (ACL 2020) — need access the black-box setting lacks.
   **Concede LIME/KernelSHAP**: query-only sampled-perturbation
   surrogate attribution — but additive/linear, retrospective, no
   quadratic metric, no allocation. DBSA (AISTATS 2025) gradient-free
   token importance — distributional effect sizes, auditing use.
6. **Decision-focused learning**: **LODL (NeurIPS 2022) is the single
   nearest methodological neighbor** — sampled-perturbation local
   QUADRATIC surrogates of a black-box decision loss. Concede the
   estimator's mathematical heart. Not taken: LLM consumer, input-state
   target, budget allocation, Σ composition, probe-cost ledger. No DFL
   work found with an LLM as the downstream consumer.
7. **Perturbation sensitivity of LLMs**: DBPA (perturbation hypothesis
   testing), MeZO (NeurIPS 2023 — forward-only SPSA probing of LLMs is
   practical, over WEIGHTS). No quadratic input-state metric used for
   allocation found.
8. **Agent-memory staleness**: STALE benchmark, timestamp recipes,
   scalar VOI-flavored retrieval triggering — nothing direction- or
   geometry-aware (the DR-track opening transfers).
9. **Precision-allocation ancestor**: HAWQ-V2 (NeurIPS 2020) —
   Hessian-trace-weighted mixed-precision for WEIGHTS: tr(H·ΔW²) is
   the structural ancestor of tr(P_C Σ) over inputs.

## Novelty posture (sealed campaigns must quote this, not improve on it)

Every conjunct individually taken. Structural ancestors: LODL
(quadratic surrogate from samples) + HAWQ-V2 (trace-weighted precision
allocation). Nearest applied neighbor and REQUIRED BASELINE:
CompactPrompt-style uniform numeric quantization; LLMLingua-style
perplexity pruning is the second required comparator. The conjunction —
probed quadratic read metric of a frozen LLM over serialized state
components × quantization covariance × prospective matched-budget
per-component allocation × probe cost charged × out-of-sample — was
not found assembled anywhere. Claim the conjunction only.
