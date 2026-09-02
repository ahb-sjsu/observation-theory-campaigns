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
