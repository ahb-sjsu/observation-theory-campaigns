# PREREG-CR-ANN — consumer-relative ANN: the conditional dissociation, sealed

**Status: DRAFT v0.1. FAMILY-CONSTRUCTED 2026-09-01. Earliest seal 2026-09-02
(cooling-off; the checker enforces FAMILY-CONSTRUCTED < seal date). Not sealed.
The five construction cells (`README.md`) inform the bars and are EXCLUDED from
grading; every graded number comes from consumers, splits, and seeds named here
and not previously evaluated.**

## Claim family

FAISS-style ANN answers "what does *close* mean?" with the embedding metric (L2 /
inner product). Observation Theory answers "close to *whom*?": the downstream
consumer C reads the embedding through its own operator, and the consumer-relative
distance is

    d_C(x, x_j)^2 = (x − x_j)^T P_C(x) (x − x_j),    P_C = J_C^T J_C

(the Jacobian pullback of the consumer's output; = W^T W for a linear readout).
Two consumers of the same embedding database legitimately induce different
neighborhoods.

**The law under test (conditional, both arms):** at a fixed candidate budget k,
reranking L2 candidates by d_C improves the consumer's task **iff** the consumer
is (a) decodable from the embedding space and (b) misaligned with its raw
geometry — and the improvement comes *at the cost of* embedding-space fidelity.
Quantitatively, with

    decodability D = accuracy of the consumer's own probe on held-out data
    alignment    A = accuracy of raw L2 1-NN at the consumer's task
    headroom     H = D − A

the prediction is gain ≈ a substantial fraction of H when H is large and D is
strong, and no gain when H ≈ 0 (matched) or D is weak (noisy read). The
embedding-fidelity half (recall@1 against the true L2-nearest collapses under OT
reranking whenever P_C ≠ I) must hold wherever gain does.

## What is construction (excluded from grading)

Five cells, committed on this branch (3d2b1ad, e43f5c1, 0704f7e, 3e002f6):
synthetic forced-misalignment (+0.42); real matched topic (−0.02, the negative
that conditionalised the law); the controlled PCA-direction sweep (+0.08 → +0.41
monotone in misalignment); natural attributes (length +0.185, caps +0.019); and
LaBSE × {valence, care-harm} on Social-Chem (+0.027 / +0.003). These fixed the
design and the bars below. None of their consumers is graded.

## Sealed design

- **Encoder (fixed):** `sentence-transformers/LaBSE`, 768-d, L2-normalised
  (the substrate of the application stack: xbse → DEME → moral-spectrum-analyzer).
- **Corpus:** Social-Chemistry-101 actions + the xbse per-axis corpora needed for
  the confirmatory consumers (pinned exactly at seal, with SHA/manifest).
- **Candidate generation (fixed):** FAISS `IndexFlatL2`, budget **k = 50**.
- **Consumers (the graded units):** linear probes on the LaBSE space,
  `P_C = W^T W`, trained on the calibration split only. Where an xbse trained
  encoder exists for an axis, the probe is the **distillation** of its validated
  score onto the LaBSE space (regress/classify the xbse score); otherwise the
  probe is trained on the axis's labels directly. Derived from the consumer,
  never tuned on retrieval outcomes.
- **Task:** predict the query's axis label from the reranked top-1 neighbour's
  label. Metrics per consumer: gain = acc(OT) − acc(L2); recall@1 vs the true
  L2-nearest; D and A as defined above, both on the calibration split (grading
  split never touches probe training or the qualification decision).
- **Splits and seeds:** corpus split 70/30 calibration/grading by a seeded
  shuffle; three disjoint graded seeds {20260902, 20260903, 20260904} redraw the
  grading queries; the calibration split and probes are frozen before the first
  graded query is scored.

### Confirmatory consumers (pre-named; qualification is mechanical)

From the Social-Chem moral-foundations labels: `fairness-cheating`,
`loyalty-betrayal`, `authority-subversion`, `sanctity-degradation`.
From the xbse/MSA axes (distilled probes): `privacy_protection`,
`identity_attack`, `physical_harm`.

Each consumer is assigned an arm by measured calibration-split quantities, by
rule, before grading:

- **Misaligned arm** (the dissociation is predicted): D ≥ 0.75 and H ≥ 0.04.
- **Matched arm** (a null is predicted): H < 0.02 (any D).
- **Excluded** (no prediction, reported descriptively): everything else —
  in particular weak probes (D < 0.75), where the law predicts nothing.

## Bars (proposed, to seal)

- **B1 (conditional dissociation).** On EVERY misaligned-arm consumer, on every
  graded seed: gain ≥ **0.3·H** AND recall@1(OT) ≤ 0.5. *Rationale:* construction
  cells captured ~0.44–0.86 of headroom (valence 0.027/0.061, length
  0.185/0.215); 0.3 is conservative without being vacuous. The recall bar is the
  fidelity-down half; construction values were ~0.03–0.17 against ~0.99 for L2.
- **B2 (matched null).** On EVERY matched-arm consumer, on every graded seed:
  gain ≤ **+0.01** (one-sided — no benefit where the law predicts none).
  *Rationale:* the matched topic cell measured −0.019.
- **B3 (ordering, the cross-project prediction).** Across ALL qualifying
  consumers pooled over seeds, Spearman(H, gain) ≥ **0.6**; and, restricted to
  the three MSA axes, the gains order consistently with the *published* xbse/MSA
  reliability weights (privacy 0.71 and identity_attack 0.61 both ≥
  physical_harm 0.26's gain). *Rationale:* the ordering prediction comes from
  numbers published before this campaign existed — the cleanest kind of seal.
- **Verdict = B1 ∧ B2** (the two arms of the conditional law). B3 is a named
  secondary: reported PASS/FAIL, does not move the verdict.

## Manipulation checks (failure ⇒ VOID)

- **MC1 (control):** isotropic P_C = I reproduces L2 within |Δacc| < 0.005 on
  every consumer, every seed.
- **MC2 (no probe leakage):** probes and arm assignments are functions of the
  calibration split only; the grading split is opened after both are frozen
  (recorded by commit order, as the D8 discipline).
- **MC3 (sufficiency):** ≥ 2 consumers qualify for the misaligned arm and ≥ 1
  for the matched arm; otherwise VOID (the conditional law needs both arms).
- **MC4 (seed discipline):** graded seeds disjoint from every construction seed.

## Descriptive secondaries (no verdict weight)

- **S1 (candidate-generation ceiling):** for each misaligned-arm consumer, the
  oracle accuracy over the k=50 candidate set (best achievable by ANY rerank).
  The gap between OT and oracle bounds Phase 1; a binding ceiling is the
  registered motivation for Phase 2 (a consumer-relative index).
- **S2 (functional form):** fitted slope of gain vs H across all consumers.

## Prior-art delineation (checked before novelty claims)

Mahalanobis/learned metrics, local metric learning (query-dependent P), and
IR/RAG cross-encoder rerankers exist. This campaign claims neither a new metric
nor reranking. The registered contribution is (1) P_C **derived from the
consumer's own read operator** (Jacobian pullback), never learned against
retrieval outcomes; (2) the **conditional dissociation law** — consumer
performance up *while* embedding fidelity collapses, appearing iff D and H say
so — with both arms sealed; (3) the cross-project **ordering prediction** from
independently published reliability weights. A WebSearch pass for closer prior
art is a seal-time checklist item.

## Open items — resolved at seal

1. Pin the exact per-axis datasets/manifests for the seven confirmatory
   consumers (xbse instance sources + Social-Chem columns), with row counts.
2. Confirm the three MSA-axis distilled probes reach the D ≥ 0.75 floor on
   calibration data; any that do not are reported descriptively (the law is
   silent on weak probes), and MC3 governs sufficiency.
3. Prior-art WebSearch pass (delineation above).
4. Freeze bar constants (0.3·H, +0.01, 0.6, floors) exactly as written or amend
   with dated rationale BEFORE seal; nothing moves after.

## Amendment discipline

As the D8/XPROTO families: nothing changes after the seal line except by dated
amendment recorded here. Graded verdicts are committed as executed.
