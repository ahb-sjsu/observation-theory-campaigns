# RESULTS — PREREG-CR-ANN v1.0 graded run

**Verdict: FAIL** (executed 2026-09-02, as sealed at d68b292; record
`prereg/graded_result.json`, runner `cr_ann_graded_run.py`). The run is valid:
MC1 (isotropic control) passed on every consumer and seed, MC3 passed
(2 misaligned + 1 matched), MC4 seeds disjoint, MC2 by commit order (seal
d68b292 precedes execution). The sealed quantitative law failed its bars.
Nothing here is a VOID; this is a negative, kept.

## Arm qualification (calibration only, mechanical)

| consumer | D | A | H | arm |
|---|---|---|---|---|
| fairness-cheating | 0.676 | 0.614 | +0.062 | excluded (D < 0.75) |
| loyalty-betrayal | 0.767 | 0.674 | +0.093 | **misaligned** |
| authority-subversion | 0.725 | 0.637 | +0.088 | excluded (D < 0.75) |
| sanctity-degradation | 0.727 | 0.640 | +0.087 | excluded (D < 0.75) |
| privacy_protection | 0.919 | 0.919 | +0.000 | **matched** |
| identity_attack | 0.777 | 0.751 | +0.026 | excluded (dead zone) |
| physical_harm | 0.775 | 0.727 | +0.048 | **misaligned** |

## Graded results (three seeds each)

| consumer (arm) | gains by seed | recall@1 (OT) | bar | result |
|---|---|---|---|---|
| loyalty-betrayal (mis, H .093) | +0.016 / +0.009 / +0.021 | 0.031–0.037 | ≥ 0.028 | **B1 fail 0/3** |
| physical_harm (mis, H .048) | +0.001 / −0.007 / +0.009 | 0.031–0.034 | ≥ 0.014 | **B1 fail 0/3** |
| privacy_protection (matched) | +0.007 / +0.000 / +0.013 | 0.051–0.054 | ≤ +0.01 | **B2 fail 2/3** (seed 20260904 over by 0.003) |
| identity_attack (excluded, descriptive) | +0.056 / +0.053 / +0.062 | 0.021–0.027 | — | largest gains in the run |
| sanctity-degradation (excluded, descriptive) | e.g. +0.017 (seed 04) | ~0.036 | — | — |

B3 secondary: Spearman(H, gain) = **0.527** (< 0.6, fail); the published-weights
clause passed (mean gains: identity 0.057 and privacy 0.007 both ≥ physical_harm
0.001) — the seal-time dated note predicted this clause would fail, and it
passed only because physical_harm gained nothing at all. S1: the oracle ceiling
is ≥ 0.997 everywhere — candidate generation never binds at k = 50; every miss
is the rerank metric's. S2: fitted slope of gain vs H = **0.089**.

## Honest read

The qualitative dissociation shows up almost everywhere: gains are positive in
11 of 12 anisotropic consumer-seed cells, and the fidelity-down half holds
universally (OT recall@1 0.02–0.05 against ~1.0 for L2). What failed is the
sealed conversion rate. The construction cells converted 44–86% of headroom;
the confirmatory consumers converted about 9% (S2). The bars were set from the
construction cells, and the confirmatory family did not honor them.

Two specific instrument findings, disclosed for any successor:

1. **Calibration H is a weak estimator of grading headroom.** physical_harm
   qualified misaligned at H = +0.048 and then gained ~0; identity_attack was
   excluded at H = +0.026 and gained +0.053 to +0.062 — more than its measured
   headroom. Its corpus is the two-domain join (civil_comments + MHS), where
   the internal 80/20 calibration estimate evidently does not transfer to the
   70/30 grading split. A successor should cross-fit H (repeated splits) and
   treat single-split H as noise-bounded.
2. **The matched null roughly held.** privacy at +0.007 / +0.000 / +0.013
   against a one-sided +0.01 bar is a near-pass; the arm logic (no headroom →
   no gain) behaved.

Per the amendment discipline the prereg is untouched and no bar moves
retroactively. Any V2 family (cross-fit H, homogeneous corpora, a conversion
constant justified by these numbers rather than the construction cells) is a
new prereg, owner's call.

## Post-mortem (post-hoc diagnostics, 2026-09-02)

`cr_ann_postmortem.py` → `prereg/postmortem.json`, run on the graded raw the
way covering_route/mc2_retest were run on D8-V1's. Three findings, each with a
mechanical fix:

1. **Single-split H is noisy (identity_attack's exclusion was an instrument
   error).** Cross-fit (5-fold) H for identity_attack is **+0.080 ± 0.014**;
   the single calibration split that excluded it drew +0.026. Against its
   matched-split grading headroom (+0.089) its gain converts at **0.64**. Both
   of its domains behave identically (civil_comments +0.047, MHS +0.054), so
   the gain is real and the arm assignment was wrong. Fix: qualify on
   cross-fit H.
2. **Heterogeneous joins manufacture mirage headroom (physical_harm).** Its H
   is stable under every estimator (0.048 cal, 0.049 grading, 0.048 ± 0.010
   cross-fit) and its gain is still ~0 — because per domain, beavertails is
   MATCHED (D 0.944, A 0.914) and ethics is a WEAK probe (D 0.689): the pooled
   headroom exists only in the mixture statistics, in no actual query
   population. The law behaved correctly in both domains; the unit of
   qualification was wrong. Fix: qualify and grade per single-domain unit.
3. **The 0.3 conversion constant was construction-inflated.** Honest
   conversions against cross-fit H for D ≥ 0.75 homogeneous units: identity
   domains 0.56–0.75, loyalty 0.15 (its D_g is borderline, 0.741); conversion
   rises with probe strength D, and weak probes forfeit entirely (fairness,
   D 0.67, gain −0.005). The matched arm behaved (privacy cross-fit H
   −0.009 ± 0.013, mean gain +0.007; the +0.01 B2 bar broke on ±0.005 seed
   noise, max seed +0.013).

Verdict unchanged: FAIL as graded. These diagnostics justify a V2 family
(PREREG-CR-ANN-V2) on fresh consumers with cross-fit qualification,
single-domain units, and bars grounded in these committed numbers.
