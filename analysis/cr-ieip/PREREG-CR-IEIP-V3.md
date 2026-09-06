# PREREG-CR-IEIP-V3 — the locality law

**Status: SEALED v1.0 (2026-09-05, UTC-verified). FAMILY-CONSTRUCTED
2026-09-04 < seal date: cooling-off satisfied. V1 and V2 graded FAIL and stay
FAIL. V3 tests the regime variable the V2 failures identified: consumer-metric
gating beats raw iff the transform is LOCAL in representation space, measured
by the identity-map held-out R² Λ — not by the equivariance map's fit. The
four open items are resolved in the "Seal record" below; after this line
nothing changes except by dated amendment. Verdicts commit as executed.**

## Claim

For an equivariance monitor, grading the residual in the consumer's read
(activation-patch response) beats grading it in raw L2 **as a monotone
function of transform locality**, where locality at layer ℓ is

    Λ_ℓ = identity-map held-out R²
        = 1 − Σ‖h_ℓ(g·x) − h_ℓ(x)‖² / Σ‖h_ℓ(g·x) − mean‖²

computed on a held-out slice of the CALIBRATION split (fit-free; no ρ̂). Two
predictions, both sealed:

- **P1 (threshold law, the verdict):** per (cell, layer) unit, the
  consumer-metric false-clear advantage `Δ = fc_raw − fc_true` satisfies
  **Δ ≥ +0.05 when Λ ≥ 0.20** (local arm) AND **Δ ≤ +0.01 when Λ ≤ −0.20**
  (non-local arm). Units with Λ in (−0.20, 0.20) are the transition band:
  no bar, reported descriptively.
- **P2 (monotonicity, secondary but pre-stated):** across ALL graded units
  pooled, **Spearman(Λ, Δ) ≥ 0.7**. This is the "law not threshold" claim.

Λ is measured BEFORE grading and assigns arms mechanically; the arm-vs-
prediction table is reported (a mismatch is itself a result, as in V2).

## Construction (excluded from grading)

All V1/V2 graded runs and construction runs (bt/fr/de/es transforms; two
paraphrasers; 0.5B/1.5B), and the locality design probe (synonym/shuffle/
trunc_half identity-R² on burned Social-Chem, states only). Every one burned.

## The locality ladder (fresh transforms, design-probe-measured on 0.5B)

| transform | text change | Λ (L12/L18, 0.5B) | predicted arm |
|---|---|---|---|
| synonym substitution | 39% | 0.921 / 0.907 | local |
| interior word shuffle | 86% | 0.446 / 0.360 | local (the discriminator: high text change, mid Λ) |
| truncate-to-half | 100% | −0.786 / −0.686 | non-local |

The shuffle unit is the cell that distinguishes this law from the ρ̂-fit law:
it is textually dissimilar yet representation-local, exactly the regime where
V2's deep-1.5B-bt units failed the ρ̂-gate while keeping the advantage.

## Graded cells (fresh (model, transform, seed); arms by measured Λ)

| cell | model | transform | seed | predicted |
|---|---|---|---|---|
| H | Qwen2.5-0.5B | synonym | 20261006 | local (both layers) |
| I | Qwen2.5-1.5B | shuffle | 20261007 | local (discriminator) |
| J | Qwen2.5-0.5B | truncate-half | 20261008 | non-local |
| K | Qwen2.5-1.5B | synonym | 20261009 | local |
| L | Qwen2.5-0.5B | shuffle | 20261012 | local |

Five cells span the ladder at both scales. MC-S (sufficiency): ≥ 2 units
land local (Λ ≥ 0.20) and ≥ 2 land non-local (Λ ≤ −0.20) after measurement,
else VOID (the law needs both arms populated). Seeds collision-scanned at
seal.

## Machinery (inherited)

`cr_ieip_v3.py` + three new deterministic transforms (synonym/shuffle/
truncate) committed with the seal, dispatched via `IEIP_TRANSFORM`;
transforms are pure string ops (no model, fully reproducible). Layer rule,
N (0.5B 2600 / 1.5B 4400 for n_cal > d), patch-response consumer read,
matched top-25% flag rates, MC identifiability/power/seed-discipline as V1/V2.
Λ is computed by the committed `v2_gate.py` machinery retargeted to the
identity map (no ρ̂). Sizing from the measured ledger; Atlas substrate; two
cells at a time. **Harvest: validate before delete.**

## Secondaries (no verdict weight)

- S1: the ρ̂-gate value alongside Λ per unit — to show on the record that Λ
  orders the outcomes where ρ̂-fit did not (the V2 diagnosis, now sealed).
- S2: final-layer collapse (expected 8/8 by now).
- S3: Δ vs Λ scatter (the law's picture; the paper figure).

## Verdict

**P1 both arms, every graded unit.** P2 monotonicity is a pre-stated
secondary that does not move the verdict but is the headline if it holds.

## Seal record — the four open items, resolved 2026-09-05

1. **Seed re-scan clean** (20261006/07/08/09/12 across the three repos).
2. **Three transforms committed** into `cr_ieip_v3.py` (`synonym_sub`,
   `word_shuffle` [deterministic on the graded seed], `truncate_half`),
   dispatched via `IEIP_TRANSFORM`; pure string ops, no model, fully
   reproducible. Design-probe smoke on burned Social-Chem (states only):
   synonym 39% changed / Λ 0.92, shuffle 86% / Λ 0.45, truncate 100% /
   Λ −0.79 — all as tabulated below.
3. **Constants frozen exactly as drafted:** Λ thresholds ±0.20; Δ bars 0.05
   (local arm) / 0.01 (non-local arm); P2 floor Spearman ≥ 0.7; transition
   band (−0.20, 0.20) descriptive.
4. **Λ-gate checksum PASSED** (`lambda_checksum.py`, 2026-09-05): the
   retargeted identity-map gate reproduces the V2 post-hoc numbers exactly —
   D +0.368/+0.381, E +0.453/+0.399, G +0.316/+0.284 (bt, all ≥ 0.28);
   F −1.796/−1.304 (para). The gate is the committed machinery, verified.

Operational note (dated): the date was verified against the Atlas UTC clock
(2026-09-05 18:58Z) before sealing, not the session banner; a full root
filesystem (an orphaned installer process holding 568 GB of deleted files)
was cleared first so writes and the checksum could run.

## Amendment discipline

As V1/V2: nothing changes after the seal line except by dated amendment;
verdicts committed as executed; a FAIL's post-mortem is a new family.
