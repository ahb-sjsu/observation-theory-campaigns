# RESULTS-CR-IEIP-V3 — the locality law, graded as executed

**Verdict: FAIL** (graded, not VOID). Graded 2026-09-17 03:40 UTC against
PREREG-CR-IEIP-V3 v1.0 (sealed 2026-09-05, commit a4f1ac1). MC-S passes (6 local
units, 2 non-local, 2 transition). P1 fails in both arms. P2 does not hold
(Spearman −0.05 against a bar of 0.7). Records: `v3_gate.json`,
`v3_graded.json`, `cr_ieip_cell{H,I,J,K,L}_result.json`, `logs/cell{H..L}.log`;
grader `grade_v3.py`.

## How this came to be graded eleven days late

The five cells ran on Atlas on 2026-09-05 and 2026-09-06 with the sealed
runner (`/home/claude/cr_ieip_v3.py`, sha256 `baff7375…`, identical to the
committed file), every one to exit status 0 (H 19 min, I 3 h 02, J 37 min,
K 1 h 32, L 36 min). The result JSONs and state caches were written to
`~/cr-ieip` and never pulled back or graded. A repo sweep on 2026-09-16 found
the sealed prereg with no results file, and the owner asked for the cell to be
run. It had run. This document is the grade.

Two bookkeeping defects found on the way, both fixed in this commit and
neither touching a bar. The prereg says Λ is computed by "the committed
`v2_gate.py` machinery" and cites `lambda_checksum.py`; neither file was in
git. Both lived only in `/home/claude` on Atlas. They are committed beside
this document, byte-for-byte as found. The grader `grade_v3.py` reproduces
`lambda_checksum.py`'s formula exactly (rows `n_fit:n_cal` of the calibration
split, `n_cal = int(0.6 n)`, `n_fit = int(0.8 n_cal)`) and `v2_gate.py`'s ridge
fit for the S1 secondary.

## The ten graded units

Layers {12, 18} on Qwen2.5-0.5B and {14, 21} on Qwen2.5-1.5B, the V2 unit
rule. Δ = fc_raw − fc_true at matched top-25 percent flag rates. Arms by
measured Λ (local ≥ +0.20, non-local ≤ −0.20).

| cell | model | transform | layer | Λ | ρ̂-gate R² (S1) | fc raw | fc true | Δ | arm | predicted | P1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H | 0.5B | synonym | 12 | +0.872 | +0.741 | 0.454 | 0.326 | **+0.128** | local | local | pass |
| H | 0.5B | synonym | 18 | +0.854 | +0.708 | 0.407 | 0.244 | **+0.163** | local | local | pass |
| I | 1.5B | shuffle | 14 | +0.144 | +0.170 | 0.287 | 0.471 | −0.184 | transition | local | no bar |
| I | 1.5B | shuffle | 21 | −0.006 | −0.097 | 0.281 | 0.365 | −0.084 | transition | local | no bar |
| J | 0.5B | truncate | 12 | −0.802 | −0.126 | 0.847 | 0.661 | **+0.185** | non-local | non-local | **FAIL** |
| J | 0.5B | truncate | 18 | −0.723 | −0.346 | 0.791 | 0.602 | **+0.189** | non-local | non-local | **FAIL** |
| K | 1.5B | synonym | 14 | +0.802 | +0.589 | 0.544 | 0.425 | **+0.119** | local | local | pass |
| K | 1.5B | synonym | 21 | +0.768 | +0.432 | 0.531 | 0.406 | **+0.125** | local | local | pass |
| L | 0.5B | shuffle | 12 | +0.385 | +0.525 | 0.335 | 0.425 | −0.090 | local | local | **FAIL** |
| L | 0.5B | shuffle | 18 | +0.297 | +0.376 | 0.326 | 0.344 | −0.019 | local | local | **FAIL** |

Arm-versus-prediction: 8 of 10 units landed in the predicted arm. The two
misses are the 1.5B shuffle units, which the design probe (0.5B only) had
placed local at Λ 0.45 / 0.36 and which measured 0.14 / −0.01 at 1.5B.

## What the record says

**The locality law is refuted in both directions.** The law predicted that
the consumer-metric advantage appears when the transform is local in
representation space and vanishes when it is not. The data say the advantage
is a property of the transform family, not of its locality.

- **Synonym substitution** (H, K, four units, Λ 0.77 to 0.87): the advantage is
  present and large, +0.12 to +0.16, at both scales. These are the four units
  that pass.
- **Interior word shuffle** (L, two units, Λ 0.30 to 0.39): local by the sealed
  bar, and the consumer metric is **worse** than raw, −0.09 and −0.02. This was
  the discriminator cell, designed to be textually dissimilar yet
  representation-local. It is local, and the advantage is absent. The 1.5B
  shuffle units (I) land in the transition band with the same sign, −0.18 and
  −0.08, and carry no bar.
- **Truncate-to-half** (J, two units, Λ −0.80 and −0.72): non-local by a wide
  margin, and the advantage is the **largest in the study**, +0.185 and +0.189.
  The non-local arm's bar (Δ ≤ +0.01) is missed by a factor of eighteen.

P2, the monotonicity claim, is at Spearman −0.05 over the ten units. There is
no monotone relation between Λ and Δ in this data. Nor does the ρ̂-gate (S1)
order it: J's ρ̂-gate is negative (−0.13, −0.35) beside the largest Δ, and L's
is positive (+0.53, +0.38) beside a negative Δ. The V2 diagnosis, that ρ̂-fit
was the wrong ordering variable, stands. The V3 hypothesis, that identity-map
locality is the right one, is now also refuted.

**What does order the ten units, descriptively and unregistered:** the raw
false-clear rate itself. The two cells where raw grading is already poor
(J at 0.79 to 0.85) show the largest advantage; the cells where raw grading is
already decent (I and L at 0.28 to 0.34) show none or a loss; synonym sits in
between on both. That is a ceiling-and-floor reading, not a law, and it is
recorded here so the next family, if there is one, starts from it rather than
rediscovers it.

## Secondaries

- **S2, final-layer collapse:** rho_R2_eval at the final layer is 0.56 (H),
  0.22 (I), −1.50 (J), 0.64 (K), −0.11 (L). The expected 8/8 collapse from
  V1/V2 does not hold uniformly here; two of five final layers keep a positive
  held-out R². Reported, no verdict weight.
- **S3, the Δ-versus-Λ scatter** is the table above; with Spearman −0.05 there is
  no figure worth drawing.

## Standing

V1 FAIL, V2 FAIL, V3 FAIL, all as sealed. Three families have now tested
three ordering variables for when consumer-metric gating beats raw grading of
an equivariance residual (the V1 design, the ρ̂-fit gate, and identity-map
locality), and none orders the outcome. The construction-stage phenomenon
(consumer-metric gating cutting false clears 15 to 21 points on back-
translation, PREREG-CR-IEIP §construction) remains a phenomenon on the
transforms where it was found. The short paper draft in `paper/` describes a
law this record refutes and must not be circulated as it stands.

Per the amendment discipline, a FAIL's post-mortem is a new family, not a
patch. No new family is registered by this document.
