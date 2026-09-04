# RESULTS — PREREG-CR-IEIP v1.0 graded family

**Verdict: FAIL** (as executed; sealed 2026-09-03 at 16b2f4c, graded
2026-09-04). B1 quantifies over every cell and cell A fails it; committed
exactly as the frozen rules grade it. The family nonetheless measured BOTH
arms of a sharper law, recorded below for the V2 successor.

## Graded cells (records committed beside this file)

| cell | model x transform | ρ̂ eval R² (graded layers) | fc raw → true | B1 (≥5pp both) |
|---|---|---|---|---|
| A (s20260918) | 0.5B x T5-para | −0.000 / −0.003 | 0.246→**0.750**, 0.218→**0.601** | **FAIL (inverted)** |
| B (s20260919) | 1.5B x es-bt | 0.280 / 0.074 | 0.598→**0.456**, 0.605→**0.451** | **PASS (−14.2, −15.4pp)** |
| C (s20260923) | 1.5B x T5-para | −0.213 / −0.404 | 0.111→**0.676**, 0.134→**0.481** | **FAIL (inverted)** |

Family verdict = B1 over every cell = **FAIL**.

Secondaries as sealed: B2 (Spearman true > raw both mid layers) passes only
in cell B (A and C invert there too). B3 as written (final-layer eval R² <
0.3 AND cal > 0.8) passes only in B — in A and C the final-layer collapse is
present and deeper (eval −0.80 / −0.31) but the cal > 0.8 clause, calibrated
on 0.5B-bt behavior, fails at 0.766/0.727; reported as written.

Manipulation checks: MC1 identifiability holds in all cells (A: 2589 pairs,
n_cal > d=896; B/C: 3882 > d=1536). MC2 power verified for A (248/1036
changed) and B (428/1553); **cell C's count was not captured** — the NRP job
log was deleted before the count was extracted (the same harvest error
disclosed in C's commit; the metric outputs themselves were recovered
verbatim). MC3 para sanity: 50/50 smoke at seal; per-run survivor counts
consistent. MC4 seeds as sealed. Verdict unaffected: B1's failure is cell
A's, fully verified.

## The finding the FAIL delivers (both arms, measured under one seal)

The consumer-metric advantage is **conditional on the calibration map
holding out of sample**:

- Where ρ̂ generalizes (backtranslation: eval R² 0.07–0.28 here, 0.41–0.49
  in the three construction runs), the consumer read wins at matched flag
  rates: −14.2/−15.4pp under seal (cell B), −15 to −21pp in construction —
  now at two model scales.
- Where ρ̂ fails held-out (paraphrase: eval R² ≤ 0.00 at BOTH scales), the
  advantage does not merely vanish — it **inverts** (+35 to +57pp worse than
  raw): patching a map-error-dominated residual measures sensitivity to a
  direction that is not the perturbation, while raw ‖e‖ degrades gracefully.
- The regime separation is wide and clean in the committed record: minimum
  in-regime eval R² 0.074 vs maximum out-of-regime −0.0003.

Spec consequence for erisml-lib (sharpened from the note's requirement):
a monitor MUST NOT deploy patch-response gating when ρ̂ fails held-out
validation — below that floor it is worse than the raw metric it replaces.
Fall back to raw or abstain. Cells A and C are the measured demonstration.

## Sizing record (for the footprint ledger)

Measured peaks (`/usr/bin/time -v`): cell A 14.4 GiB (0.5B+para, N=2600),
cell B 22.7 GiB (1.5B+bt, N=4400 — above every NRP request tried; Atlas was
the right substrate), probeB 6.2 GiB (N=600). Cell C ran clean on NRP at
26 GiB requested. The para pipeline is ~6–8 GiB heavier than bt at matched
scale, and footprint grows super-linearly with N beyond the states arrays —
size from measurement, never from model weights.
