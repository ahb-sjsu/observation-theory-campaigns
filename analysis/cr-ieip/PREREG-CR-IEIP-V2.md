# PREREG-CR-IEIP-V2 — the regime-gated conditional law

**Status: DRAFT v0.1. FAMILY-CONSTRUCTED 2026-09-04 (the V1 graded family —
cells A/B/C — and its RESULTS are this family's construction evidence).
Earliest seal 2026-09-05 (cooling-off). Not sealed. V1 graded FAIL and stays
FAIL; this family tests the sharper law V1's own record measured on both
arms.**

## Claim

Consumer-metric gating (activation-patch response) beats raw-L2 gating of an
equivariance monitor **iff the calibration map ρ̂ itself generalizes**, and
the regime is mechanically decidable BEFORE grading from calibration data
alone. Formally, per (model, transform) cell at each graded mid layer:

- **In-regime arm** (gate passes): fc_true ≤ fc_raw − 0.05 at matched
  top-25% flag rates.
- **Out-of-regime arm** (gate fails): fc_true ≥ fc_raw − 0.01 (no advantage;
  the sealed record predicts inversion, but the bar claims only the
  advantage's absence — the conservative arm).

**The gate (mechanical, calibration-only):** split the calibration pairs
80/20 internally; fit ρ̂ on the 80, measure held-out R² on the 20; the cell
is in-regime at a layer iff that R² ≥ **0.05**. Rationale from the committed
record: minimum in-regime value 0.074 (cell B, L21) vs maximum out-of-regime
−0.0003 (cell A, L12) — the constant sits in a wide measured gap and is
frozen at seal. The grading split is untouched by the gate.

## Construction (excluded from grading)

All seven prior (model, transform) runs: v2/fr/tl construction + graded
cells A/B/C (records in this directory) + the v1 shakedown. Every one is
burned; graded V2 cells must be fresh pairs.

## Graded cells (proposed; fresh pairs, both predicted arms)

| cell | model | transform | predicted arm | seed |
|---|---|---|---|---|
| D | Qwen2.5-0.5B | de backtranslation (opus-mt-en-de/de-en) | in-regime | 20260927 |
| E | Qwen2.5-1.5B | fr backtranslation | in-regime | 20260928 |
| F | Qwen2.5-0.5B | T5-para, second paraphraser (`Vamsi/T5_Paraphrase_Paws`) | out-of-regime | 20260929 |
| G | Qwen2.5-1.5B | de backtranslation | in-regime | 20261002 |

The ARM IS ASSIGNED BY THE GATE at run time, not by these predictions; the
predictions are recorded so a gate/prediction mismatch is itself reportable.
MC-S (sufficiency): ≥ 2 cells gate in-regime and ≥ 1 gates out, else VOID.
Seeds pending the standard collision re-scan at seal.

## Inherited machinery and checks

`cr_ieip_v3.py` as committed (1bd259f + env transports); layer rule
round(L/2)/round(3L/4); N pinned for n_cal > d (0.5B: 2600; 1.5B: 4400);
MC identifiability/power/para-sanity/matched-flag-rates/seed-discipline as
V1; **harvest rule added: results and MC counts are extracted and validated
BEFORE any job or log is deleted** (the cell-C capture gap may not recur).
Sizing from the measured footprint ledger only (RESULTS "Sizing record");
substrate free (Atlas or NRP) per the ledger.

## Secondaries (no verdict weight)

- S1: Spearman true-vs-raw per cell (the B2 pattern).
- S2: final-layer ρ̂ collapse (present in 6/6 runs to date; the cal-R²
  clause is dropped — the phenomenon is the eval collapse itself).
- S3: the gate margin (per-cell gate R² vs the 0.05 constant) — the
  quantity a future spec would monitor live.

## Verdict

**B1 = the in-regime arm bar AND the out-of-regime arm bar, every graded
cell, both graded layers.** One family, one conditional claim, both arms.

## Open items — resolved at seal (fresh day, ≥ 2026-09-05)

1. Seed collision re-scan (20260927/28/29, 20261002).
2. Commit the second-paraphraser transform option (env `IEIP_PARA_MODEL`
   already exists; smoke ≥ 80% differ on burned texts, mechanical only).
3. Freeze the gate constant 0.05 and both arm bars exactly as written, or
   amend with dated rationale BEFORE seal.
4. Confirm corpora/footprints per the ledger; nothing sized by guess.

## Amendment discipline

As V1: nothing changes after the seal line except by dated amendment;
verdicts committed as executed; a FAIL's post-mortem is a new family.
