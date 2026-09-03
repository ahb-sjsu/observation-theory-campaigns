# OT-UMAP prior-art sweep — 2026-09-02

Instruments: DBLP API + JMLR direct + arXiv API (arXiv began refusing near the
end; residual gaps listed). This sweep pays off the debt flagged in the
2026-09-02 map addendum: OT-UMAP built before it swept. Verdict up front:
**the metric construction is prior art, twice over; the campaign's novelty
must rest entirely on the inversion, the conditional-law instrument, and the
observer-indexed evaluation — never on the metric.**

## The thick flank — the Helsinki school owns the construction AND the ruler

1. **Kaski's learning-metrics program (2001–2004)** built position-dependent
   Riemannian metrics from the Fisher information of p(class|x) and used them
   for SOM/exploratory dimensionality reduction: "Bankruptcy analysis with
   self-organizing maps in learning metrics" (IEEE TNN 2001), "Principle of
   Learning Metrics for Exploratory Data Analysis" (J. VLSI Signal Process.
   2004), "Improved learning of Riemannian metrics for exploratory analysis"
   (Neural Networks 2004). This is the position-dependent consumer-metric
   move, twenty years early. The planned P_C(x) = J(x)ᵀJ(x) successor cell is
   **learning-metrics-adjacent and must say so** — for a label-trained probe,
   the probe-Jacobian metric and the Fisher learning metric nearly coincide.
2. **NeRV** (Venna, Peltonen, Nybo, Aidos, Kaski, *JMLR* 11(13):451–490,
   2010, verified against the JMLR page): dimensionality reduction as an
   information-retrieval task whose quality depends on the USER's relative
   cost of misses vs false neighbors. This is the philosophical ancestor of
   "faithfulness is not absolute" and gets cited prominently. The supervised
   variant folds class information into the similarities.
3. The same school authored **trustworthiness/continuity** — the conventional
   ruler our dissociation table uses. (A fact to feature, not hide: the
   trade-off is graded on the ancestor's own instrument.)
4. Supervised UMAP (label-blended graph via `target_metric`), parametric
   UMAP, and arXiv:2506.01599 (cross-model pullback alignment) stand as
   flagged.

## What survives (the narrowed kernel)

1. **The inversion is structurally beyond NeRV.** NeRV's relativity is a
   scalar preference (one retrieval task, a precision/recall dial λ). The OT
   claim is multiple AUTONOMOUS consumers with derived read operators
   ordering embeddings OPPOSITELY — diagonal dominance, measured (each
   consumer's best embedding is its own OT embedding; no embedding tops two
   columns). That is an impossibility statement about shared optima, not a
   preference dial, and no swept work states or measures it.
2. **Derived-for-deployed-readers provenance, honestly bounded.** Kaski
   metrics require labels at embed time; P_C is read off any DEPLOYED
   consumer — including consumers with no labels anywhere (a length reader, a
   head inside an LLM, a regression Jacobian). Where the consumer IS a label
   probe, the constructions nearly coincide and the prereg must say so
   plainly; the operational difference (no embed-time supervision needed,
   any reader, uniform across consumers) is real but modest.
3. **The measured dissociation with the conditional-law instrument**: the
   task-up/geometry-down table with matched-null arms (aligned consumer),
   D/A/H bookkeeping, the degenerate logit-space control, and pre-stated
   bars. The Helsinki line optimizes and philosophizes; it does not run this
   falsification battery.
4. **The scRNA-seq application** into the live faithfulness controversy
   (Chari & Pachter, "The specious art of single-cell genomics" — exact
   citation to verify at draft time; arXiv refused tonight) — the inversion
   says both camps are right, for different consumers.

## Residual gaps (close before any cr-umap prereg)

- Modern task-aware-DR sweep (post-2015): the query 503'd; rerun when arXiv
  cools.
- Chari–Pachter exact citation; supervised-UMAP mechanics quoted from the
  docs/paper rather than memory.
- Semantic Scholar pass for the learning-metrics line's later descendants
  (rate-limited all evening).

## Consequences applied

- The cr-umap README's framing stands (the constant-P cell already discloses
  Mahalanobis-adjacency); the successor P_C(x) cell must carry the
  learning-metrics citation from its first line.
- Any paper leads with NeRV + learning metrics in Related Work and claims
  ONLY: the multi-consumer inversion, the conditional-law falsification
  battery, and the consumer-indexed evaluation framework.
