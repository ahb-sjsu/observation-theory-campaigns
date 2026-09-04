# RESULTS — PREREG-CR-IEIP-V2 graded family

**Verdict: FAIL** (as executed; sealed 2026-09-05 at 5e0bf26, graded same
day). Six of eight (cell, layer) units pass their arm bars; two fail, both
the same way, and the failure identifies the true regime variable the sealed
gate missed. Records: `cr_ieip_cell{D,E,F,G}_result.json`, `v2_gate.json`
(the sealed calibration-internal gate, computed exactly as written),
`v2_graded.json`. Runner sha `de572963…` (the sealed machinery + the
pre-seal `IEIP_PARA_BEAMS` knob).

## Graded table (gate applied blind; arm by gate, not by prediction)

| cell (model x transform) | layer | gate R² | arm (predicted) | fc raw → true | bar | result |
|---|---|---|---|---|---|---|
| D (0.5B x de-bt) | 12 | +0.419 | IN (in) | 0.621→0.566 (−5.5pp) | ≥5pp | PASS |
| D | 18 | +0.303 | IN (in) | 0.594→0.488 (−10.6pp) | ≥5pp | PASS |
| E (1.5B x fr-bt) | 14 | +0.174 | IN (in) | 0.660→0.461 (−20.0pp) | ≥5pp | PASS |
| E | 21 | **−0.100** | **OUT (in)** | 0.651→0.482 (−16.9pp) | no advantage | **FAIL** |
| F (0.5B x pegasus) | 12 | +0.029 | OUT (out) | 0.264→0.805 (inverted) | no advantage | PASS |
| F | 18 | −0.040 | OUT (out) | 0.289→0.671 (inverted) | no advantage | PASS |
| G (1.5B x de-bt) | 14 | +0.148 | IN (in) | 0.604→0.505 (−10.0pp) | ≥5pp | PASS |
| G | 21 | **−0.123** | **OUT (in)** | 0.595→0.502 (−9.2pp) | no advantage | **FAIL** |

Verdict = every cell, both layers ⇒ **FAIL** (E-L21, G-L21).
Gate-vs-prediction mismatches (reportable per the seal): E-L21 and G-L21
were predicted in-regime and gated OUT; the deep layer of both 1.5B
backtranslation cells fails ρ̂ held-out even inside calibration.

## What the two failures say (and the post-hoc diagnostic that nails it)

Both failures are the SAME event: at the deep layer of a 1.5B model under
backtranslation, ρ̂ fails held-out (gate R² ≈ −0.1) yet the consumer
advantage PERSISTS (−16.9pp, −9.2pp). Meanwhile both paraphrase units gate
OUT and duly invert. So ρ̂'s fit quality is NOT the regime variable: the
advantage never needed a good ρ̂ — it needs the patched residual to point
roughly along the true perturbation.

**Post-hoc diagnostic (labeled as such; verdict untouched): the identity-map
held-out R² — does h(g·x) ≈ h(x) at all — separates the outcomes
PERFECTLY on the same calibration-internal split:**

| unit class | identity R² | observed behavior |
|---|---|---|
| all backtranslation units (D, E, G — including both FAILED layers) | **+0.28 to +0.45** | advantage present |
| both paraphrase units (F) | **−1.80, −1.30** | inversion |

The gap is enormous (min +0.284 vs max −1.304). Interpretation: when the
transform is LOCAL in representation space (identity R² > 0), h(g·x) ≈ h(x)
+ δ, so even a noisy ρ̂ leaves e ≈ δ up to noise — the patch probes roughly
the right direction and the consumer read stays informative. When the
transform moves the representation wholesale (identity R² < 0, paraphrase),
e is dominated by map error and patching it is anti-informative. The regime
variable is TRANSFORM LOCALITY, not map fit. It is also cheaper: no ρ̂ fit
is needed to compute it.

## Standing of the arc after three sealed families

- The mid-layer consumer-read advantage under backtranslation is now
  **sealed-confirmed in five graded units across two families** (B; D both
  layers; E-L14; G-L14) plus three construction runs — reductions 5.5–20pp.
- The paraphrase inversion is sealed-confirmed at both model scales twice
  over (A, C, F).
- The final-layer ρ̂ collapse: present in 7 of 8 runs measured.
- What has failed three times is the GATING VARIABLE: none (V1), ρ̂ fit
  (V2). The identity-locality diagnostic is the natural V3 gate, with a
  measured 1.5+ separation gap to freeze a constant inside — recorded here
  for the owner; **no V3 is drafted by this document.**

## Sizing ledger additions (time -v peaks)

D 14.1 GiB (0.5B de-bt), E 23.8 GiB (1.5B fr-bt), F 13.3 GiB (0.5B
pegasus), G 24.1 GiB (1.5B de-bt).
