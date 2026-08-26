# EXPLORATION — the Flip in AI deployment gating (kept, NOT registered)

**Date: 2026-08-26. Status: flip absent; kept as executed; no prereg, no seal.**

We tried to transfer the two-consumer verdict inversion to the LLM deployment
cell. Fleets were the lexical-overlap and constituent HANS subcases, policies
were matched deployment-margin budgets on the two heuristic axes, and the gate
deployed a slice when a 50-example probe cleared the accuracy bar plus the
slice's margin.

The flip did not appear. Nearly every false-clear rate is zero on all seeds
(`LLMFLIPREP-family.json`). The reason is structural, not a bug. HANS subcase
accuracies are bimodal: entailment slices sit near 1.0 and non-entailment slices
near 0.0, which is exactly the 0.38 spread the sealed XPROTO-LLM cell measured.
A 50-example probe almost never misjudges an accuracy of 0.99 or 0.02 against a
0.80 bar, so the gate faces no decisions near the boundary and the margin
allocation has nothing to trade. The inversion needs two things at once,
misaligned read axes and consumers operating near their thresholds. This
substrate has the first and lacks the second.

We did not move the bar into the bimodal gap to manufacture a boundary regime.
That would be tuning the experiment until the effect appears.

**What would make this registrable.** A deployment substrate with graded slice
difficulty (accuracies spread across the bar rather than bimodal): counterfactual
or adversarial slices with intermediate accuracy, or a weaker model whose HANS
performance is not saturated per slice. Until then the honest statement is: in
this cell the certificate's failure mode is the aggregate-vs-slice gap (the
sealed result), not a policy inversion.

The one-time inference cache (`LLM-hans-correct.json`, per-example correctness
for all 30 subcases) is committed and makes any future variant instant.

Code: `fam_llmflip.py`. Record: `LLMFLIPREP-family.json` (seeds {0,1,2}).
