# Consumer-relative I-EIP — smallest cell (UNSEALED, exploratory)

OT applied to erisml-lib's **I-EIP Monitor** (Internal Epistemic Invariance:
`h_ℓ(g·x) ≈ ρ_ℓ(g)·h_ℓ(x)`, graded in raw L2, gating the forward pass). The OT
critique: layer ℓ's activations have a consumer — the downstream network — and
the norm that matters is the consumer's read, `‖e‖_{P_C}`. A raw-L2 gate can
false-alarm on dead subspaces and, worse, **false-clear** an error concentrated
where downstream reads (the spec-gaming case §1.2 of the whitepaper exists to
catch). Same dissociation as AICSI / KV-keys / CR-ANN, relocated to a safety
monitor.

## Cell (2026-09-01, `cr_ieip_cell.py`)

Qwen2.5-0.5B (CPU), 600 Social-Chem actions, g = backtranslation paraphrase
(MarianMT en→es→en; 73/600 returned identical). Probes at layers {6,12,18,24}
(last-token state). ρ̂ per layer = the whitepaper's own ridge Procrustes, fit on
a 360-pair calibration split. Consumer map = ridge `L: h_ℓ → JL-projected
logits` (calibration only); `P_C = LᵀL`. Ground truth = the model's actual
next-token KL between x and g·x. Eval on the held-out 240.

| layer | ρ̂ cal R² | Spearman raw | Spearman P_C | false-clear raw | false-clear P_C |
|---|---|---|---|---|---|
| 6 | 0.924 | 0.441 | 0.411 | 0.554 | **0.446** |
| 12 | 0.940 | 0.461 | 0.462 | 0.589 | **0.482** |
| 18 | 0.964 | 0.420 | 0.383 | 0.589 | 0.554 |
| 24 | 1.000 | 0.248 | 0.244 | 0.625 | 0.625 |

(false-clear = fraction of behavior-changed cases NOT flagged, flagging the top
25% by each metric; "changed" = KL above the calibration 75th percentile.)

## Honest read

- **Not supported:** the strong claim. Globally the consumer-weighted error does
  not rank-predict behavioral change better than raw L2 (0/4 layers).
- **Supported, in the gating tail:** at the matched flag rate a monitor actually
  operates at, the consumer metric false-clears fewer behavior-changing cases at
  3/4 layers (~11 pp at layers 6 and 12). Equal metrics globally; the consumer
  weighting catches more of the tail the gate exists to catch.
- **Caveats (real):** ρ̂ is underdetermined here (d = 896 > n_cal = 360; the
  whitepaper's own estimator near-interpolates, cal R² 0.92–1.0, so part of the
  residual is estimation artifact — a limitation the I-EIP calibration procedure
  itself inherits at small corpora); the consumer map is a linear JL-projected
  proxy for the true downstream Jacobian; single small model; 12% identical
  paraphrases dilute the KL spread.

**Verdict: suggestive-in-the-tail, not confirmed.** The right shakedown outcome
to have before proposing metric changes to the I-EIP sprint plan. A decisive
cell needs n ≫ d calibration, a per-input local Jacobian (or JVP-sampled P_C),
harder transforms, and a second model.

## Decisive cell v2 (2026-09-01, `cr_ieip_v2.py`): CONFIRMED at mid layers

Fixes the v1 weaknesses: 2,312 non-identical pairs (ρ̂ properly determined,
n_cal = 1,387 > d = 896, held-out R² reported) and a **true consumer read** — the
equivariance residual e is injected at layer ℓ (last-position activation patch)
and the network's own output response KL is the consumer metric. Linear proxy
kept as a comparison arm. 216/925 eval pairs are behavior-changed.

| layer | ρ̂ R² cal→eval | sp raw | sp proxy | sp **true** | fc raw | fc proxy | fc **true** |
|---|---|---|---|---|---|---|---|
| 6 | 0.815 → 0.473 | 0.473 | 0.473 | 0.373 | 0.593 | 0.491 | 0.542 |
| 12 | 0.809 → 0.500 | 0.519 | 0.538 | **0.648** | 0.574 | 0.449 | **0.384** |
| 18 | 0.835 → 0.422 | 0.532 | 0.465 | **0.678** | 0.556 | 0.523 | **0.347** |
| 24 | 0.883 → **−0.31** | 0.315 | 0.290 | 0.284 | 0.616 | 0.620 | 0.625 |

**Confirmed (layers 12, 18):** the consumer read of the residual predicts real
behavioral change far better than raw L2 (Spearman +0.13/+0.15) and cuts monitor
false-clears by **19–21 pp** at matched flag rates. v1's Spearman null is
explained by its weak linear proxy (the proxy-vs-true gap is visible in the
table). L6 mixed (early residuals read noisily through the remaining depth).

**Independent finding for the I-EIP calibration procedure:** the final-layer ρ̂
FAILS to generalize (eval R² = −0.31 despite cal 0.88) — final representations
are the most content-specific and hardest to Procrustes-map across paraphrases.
A monitor calibrated at the final layer grades against a broken ρ̂; and the
cal→eval R² gap (0.81→0.47 even mid-stack) says the whitepaper should require
held-out ρ̂ validation, not just fit.

Remaining limits: one model (Qwen2.5-0.5B), one transform family
(backtranslation), consumer read measured in x's context only.

## Replication on a second model (2026-09-02, `cr_ieip_v3.py`, TinyLlama-1.1B): CONFIRMED

Same v2 design (IEIP_TAG=tl, IEIP_MODEL=TinyLlama/TinyLlama-1.1B-Chat-v1.0,
es backtranslation, IEIP_N=4400 so n_cal > d=2048), layers 5/11/16/22 of 22.
Record: `cr_ieip_tl_result.json`.

| layer | ρ̂ R² cal→eval | sp raw | sp proxy | sp **true** | fc raw | fc proxy | fc **true** |
|---|---|---|---|---|---|---|---|
| 5 | 0.414 → 0.334 | 0.383 | 0.270 | 0.377 | 0.562 | 0.542 | 0.511 |
| 11 | 0.605 → 0.427 | 0.598 | 0.599 | **0.654** | 0.479 | 0.393 | **0.322** |
| 16 | 0.708 → 0.460 | 0.686 | 0.659 | **0.778** | 0.390 | 0.388 | **0.239** |
| 22 | 0.920 → **0.200** | 0.498 | 0.472 | 0.494 | 0.489 | 0.496 | 0.476 |

Both v2 findings replicate on a second model family: at mid layers the true
consumer read beats raw L2 on both metrics (Spearman +0.06/+0.09; false-clear
−16/−15 pp at layers 11/16), and the final-layer ρ̂ collapses held-out
(R² 0.92 cal → 0.20 eval), so the mid-layer calibration caveat stands.

## Replication on a second transform family (2026-09-02, fr backtranslation): CONFIRMED

Same v2 design on Qwen2.5-0.5B with en→fr→en (opus-mt-en-fr / fr-en) replacing
the es pair (the first launch died silently at bt 640/2600; relaunched clean).
Record: `cr_ieip_fr_result.json`.

| layer | ρ̂ R² cal→eval | sp raw | sp **true** | fc raw | fc **true** |
|---|---|---|---|---|---|
| 6 | 0.811 → 0.476 | 0.374 | 0.222 | 0.675 | 0.667 |
| 12 | 0.796 → 0.489 | 0.432 | **0.525** | 0.633 | **0.485** |
| 18 | 0.822 → 0.410 | 0.458 | **0.579** | 0.603 | **0.435** |
| 24 | 0.865 → **−0.285** | 0.203 | 0.174 | 0.679 | 0.684 |

**The v2 result is now replicated 2/2** (second model, second transform): at mid
layers the consumer read beats raw L2 on both metrics (here Spearman +0.09/+0.12,
false-clear −15/−17 pp at layers 12/18), L6 is mixed as in v2, and the
final-layer ρ̂ held-out collapse appears in all three runs. Remaining limits:
both transforms are backtranslation-style paraphrases, and the consumer read is
measured in x's context only. Next step per the publishability ranking: a
sealed CR-I-EIP prereg + short paper (interpretability/safety venue).

## The upgrade path for I-EIP (now evidence-backed at shakedown level)

1. Per-layer, per-EM `P_C`-weighted equivariance error (each EM evaluator
   supplies its read operator) — consistent with the whitepaper's own
   Reward-Irrecoverability refusal to collapse to a scalar.
2. A measured **false-clear rate for the monitor** (nominal = gate cleared;
   consumer_ok = behavior/EM verdict actually invariant) as a shipped,
   re-verifiable number.
3. ρ̂ freshness: the OT-14 refresh-floor law applied to calibration age
   (fine-tunes/LoRAs stale the Procrustes maps; the attestation should carry
   calibration age + estimation error — validity, not just provenance, per the
   POSO paper's distinction).
