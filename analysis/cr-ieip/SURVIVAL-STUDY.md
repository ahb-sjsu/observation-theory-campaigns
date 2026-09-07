# CR-I-EIP perturbation-survival study — POST-HOC, EXPLORATORY (not sealed)

**Date 2026-09-06. Verdict: NO SUCCESSOR PREDICTOR FOUND.** This tested the
successor hypothesis the V3 FAIL named (perturbation survival) as a forecaster of
the consumer-read advantage Δ, post-hoc on the 22 already-graded units
(V1 A/B + V2 D–G + V3 H–L; cell C excluded, its states cache was deleted). It is
a diagnostic, not a sealed family. Machinery: `survival_study.py`, records in
`survival_study.json` (canonical copy also at `/home/claude/cr-ieip/` on Atlas).

## What was tested

Faithful to the sealed pipeline: ρ̂ = ridge_fit(hx[cal], hg[cal], 1e-2·n_cal),
hg ≈ hx·ρ̂ᵀ, residual e = hg − hx·ρ̂ᵀ, true perturbation δ = hg − hx, split 0.6.
Three survival candidates, each a per-unit predictor of Δ = fc_raw − fc_true:

- **S_dir** = median cos(e, δ) — directional survival, "does the injected
  residual point along the true perturbation" (the paper's stated mechanism),
  computed on eval (no ρ̂ leakage) and on the held-out calibration slice
  (the deployable-gate analogue of Λ).
- **S_patch** = Pearson(c_L, KL) over eval, where c_L is the CACHED true
  patch-response — "does patching e reproduce the true output change."

Λ (identity-map held-out R²) recomputed uniformly for comparison.

## Result (Spearman with Δ, 22 units; a law needs ≥ 0.70)

| predictor | Spearman | Pearson | adv/inv median gap |
|---|---|---|---|
| Λ (locality) | +0.589 | +0.793 | +1.689 |
| S_dir (eval) | +0.269 | +0.129 | +0.049 |
| S_dir (cal slice) | +0.284 | +0.166 | +0.040 |
| S_patch | +0.590 | +0.733 | +0.377 |

- **Directional survival cos(e, δ) is dead.** Spearman 0.27, and it does not
  separate the advantage units from the inversion units at all (medians 0.61 vs
  0.56, gap 0.05). The residual points along δ about equally whether the consumer
  read helps or hurts. The paper's stated mechanism, as a scalar, does not
  forecast the sign.
- **Patch-response fidelity S_patch is no better than locality** (Spearman 0.59
  vs Λ's 0.59) and, critically, **fails on the same cells**. Its 0.59 comes from
  the easy backtranslation-vs-paraphrase split, not from the hard V3 cases.

## The truncate cell defeats every scalar (this is the point)

| cell | Λ | S_dir | S_patch | Δ (actual) |
|---|---|---|---|---|
| J truncate | −0.75 (predict no adv) | ~0.63 (mid) | 0.16–0.21 (predict no adv) | **+0.19 advantage** |
| L shuffle | +0.34 (predict adv) | ~0.55 (mid) | 0.60 (predict adv) | **−0.05 none** |

Truncation posts a large advantage while being non-local, mid-directional, AND
low patch-fidelity: no candidate explains it. Shuffling has the profile of an
advantage cell on Λ and S_patch and delivers none. Four scalars have now failed
to forecast the sign of the consumer-read advantage: nothing (V1), ρ̂ held-out
fit (V2), transform locality Λ (V3), and perturbation survival in two forms (this
study). The advantage is a tail phenomenon (false-clear at a matched top-quartile
flag rate) that no global statistic on the representation or on the patch, among
those tried, captures.

## Consequence

No V4 is warranted on these candidates. The sealed paper's conclusion is
reinforced, not overturned: the effect is real and replicated, and its sign is
not forecastable from the representation. The paper's successor paragraph is
updated to report this post-hoc test as executed. A forecaster, if one exists,
would have to be a tail statistic (of the flagging quantiles, not a global
correlation) and is genuine future work, not a queued family.

## Tail-statistic probe — the one candidate named above (2026-09-07)

`survival_tail.py` tests that tail idea directly: statistics of the FLAGGED tail
(`changed = KL[ev] > quantile(KL[cal], 0.75)`, the top-quartile flag set that
defines the false-clear), not global correlations, across the same 22 units.

| predictor | Spearman | Pearson | adv/inv gap |
|---|---|---|---|
| **S_tail_cos** = median cos(e, δ) over the flagged tail | **+0.683** | **+0.878** | +0.331 |
| S_cos_q90 = 90th-pct \|cos(e, δ)\| over eval | +0.196 | +0.252 | +0.067 |
| S_rp_q90 = 90th-pct \|e·δ̂\| over eval | +0.398 | +0.416 | +10.9 |
| S_tail_enorm = median ‖e‖(tail)/median ‖e‖(eval) | −0.534 | −0.253 | −0.392 |

**Near-miss, no rescue.** Restricting the read-alignment cos(e, δ) to the flagged
tail is by far the strongest forecaster the whole arc has produced — Spearman
0.683, Pearson 0.878, clean sign separation (advantage median 0.687 vs inversion
0.356). It confirms the signal lives exactly where the tail hypothesis predicted:
the advantage tracks read-alignment among the samples that actually get flagged,
which every central statistic averages away. But 0.683 is below the pre-stated
0.70 law floor, so by the committed rule there is **no successor and no rescue** —
the three-strikes negative stands. S_tail_cos is a lead for a future
preregistration (a directional read-alignment gate evaluated on the flag set),
not a forecaster this record can stand behind. Records: `survival_tail.py`,
`survival_tail.json`.
