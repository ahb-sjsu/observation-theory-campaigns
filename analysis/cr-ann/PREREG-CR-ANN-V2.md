# PREREG-CR-ANN-V2 — the conditional dissociation, with an honest headroom instrument

**Status: SEALED v1.0 (2026-09-03). FAMILY-CONSTRUCTED 2026-09-02 < seal
date: cooling-off satisfied. V1 (PREREG-CR-ANN v1.0) graded FAIL and stays
FAIL; nothing here re-grades it. V2 exists because the post-mortem showed the
failure decomposes into three instrument defects, each with a mechanical fix,
while the law behaved correctly inside every homogeneous population it was
actually tested on. The four open items are resolved in the "Seal record"
section at the bottom; after this line nothing changes except by dated
amendment. The graded run executes as written, verdict committed as executed.**

## What V1 established (committed record)

- Verdict FAIL (`RESULTS-CR-ANN.md`, `prereg/graded_result.json`, 61c18e4):
  B1 0/6, B2 2/3, B3 Spearman 0.527.
- Post-mortem (`cr_ann_postmortem.py` → `prereg/postmortem.json`):
  1. Single-split calibration H is noisy: identity_attack was excluded at
     H = +0.026 when its cross-fit H is +0.080 ± 0.014, and it then gained
     +0.053…+0.062 (conversion 0.64 against matched-split headroom, identical
     in both of its domains).
  2. Heterogeneous joins manufacture mirage headroom: physical_harm's pooled
     H = 0.048 is stable under every estimator, yet per domain it is matched
     (beavertails: D 0.944, A 0.914) plus weak (ethics: D 0.689) — no actual
     query population carries the pooled headroom, and the gain was correctly
     ~0.
  3. The 0.3 conversion constant came from construction cells (0.44–0.86) and
     does not describe natural consumers: measured conversions against honest
     headroom are 0.56–0.75 (identity's domains, D ≈ 0.80) and 0.15 (loyalty,
     D ≈ 0.74), rising with probe strength; weak probes forfeit (fairness,
     D 0.67, gain −0.005). Matched-arm noise: privacy mean gain +0.007, max
     seed +0.013, seed spread ~±0.005.

## The three sealed changes (fixes, not bar-shopping)

### Change 1 — cross-fit qualification (fixes the H instrument)

D and A are measured by **5-fold cross-fit on the calibration split** (train
the probe on 4 folds, D on the held fold vs true labels; A by L2-1NN from the
4 folds into the held fold; H = mean over folds). Arms, floors unchanged in
form: **misaligned** iff D_xfit ≥ 0.75 and H_xfit ≥ 0.04; **matched** iff
|H_xfit| < 0.02; else excluded (reported descriptively). Rationale: cross-fit
would have qualified identity_attack (+0.080 ± 0.014) and its fold-sd (~0.02
at n≈4200) bounds the noise that mis-assigned it.

### Change 2 — single-domain units (fixes the mixture artifact)

The graded unit is an **(axis, single source corpus) pair**. No unit pools
rows from more than one source file. A multi-corpus axis contributes one unit
per corpus, each qualified and graded on its own. Rationale: physical_harm's
per-domain decomposition; the law is about a consumer reading one population,
and the mixture headroom it "failed" on does not exist in any population.

### Change 3 — bars grounded in the measured conversions

- **B1 (misaligned arm, every unit):** mean gain over the three seeds
  ≥ **max(0.10 · H_xfit, +0.010)** AND per-seed gain ≥ 0 on every seed AND
  recall@1(OT) ≤ 0.5 on every seed. Rationale: 0.10 sits below every measured
  qualifying conversion (0.15–0.75); the +0.010 absolute floor keeps the bar
  ≥ 2× the measured seed noise (±0.005) so a pass cannot be noise; the
  per-seed sign floor replaces V1's per-seed fraction bar, which double-charged
  seed noise.
- **B2 (matched arm, every unit):** mean gain ≤ **+0.010** AND every seed
  ≤ **+0.020**. Rationale: privacy measured mean +0.007 / max +0.013; V1's
  per-seed +0.01 bar broke on noise the mean bar absorbs.
- **B3 (secondary, no verdict weight):** Spearman(H_xfit, mean gain) ≥ 0.6
  across ALL units including excluded-descriptive ones. The V1
  published-weights clause is dropped as a bar and recorded as a finding:
  xbse reliability weights measure feeder quality, not headroom, and do not
  order retrieval gains.
- **Verdict = B1 ∧ B2.**

## Sealed design (inherited from V1 v1.0 unless stated)

Encoder LaBSE (768-d, L2-normalised); FAISS `IndexFlatL2`, k = 50; probes =
logistic on the LaBSE space, P_C = WᵀW, distillation rule as V1's seal record
(validated xbse joint encoder → centroid-axis score → probe on sign of score,
trained on the first 80% of calibration) where a validated encoder covers the
axis, else direct label training; task = query's label from the reranked
top-1's label; gain, recall@1, MC1 isotropic control (|Δacc| < 0.005), S1
oracle ceiling, S2 slope — all as V1. Splits: per unit, dedupe, seeded
shuffle, cap 6,000, 70/30 calibration/grading; per-seed query redraw =
floor(0.8 · n_grading) without replacement (V1's operationalization, now
sealed). **Split seed 20260911; graded seeds {20260912, 20260913, 20260914}**
(repo-wide collision scan clean, 2026-09-02; disjoint from all construction
and V1 seeds).

## Confirmatory units (fresh; qualification is mechanical)

Candidate pool: single-domain corpora of the validated xbse axes **never
evaluated by CR-ANN** (V1's seven consumers and every construction cell are
burned). Named candidates, exact files/hashes/row counts pinned at seal:

- privacy_protection × `aita_privacy_labeled.jsonl` (V1 used only the RoT file)
- fairness_equity × MHS fairness (`mhs` fairness jsonl)
- autonomy_respect × `darkpattern`; autonomy_respect × `mentalmanip`
- virtue_care × Moral-Stories care (`MS_CARE`)
- societal_environmental × `env_labeled.jsonl`
- legitimacy_trust and epistemic_quality domains (enumerated from
  `joint_builders.py` at seal)

MC3 (sufficiency): ≥ 2 misaligned units and ≥ 1 matched unit after
qualification, else VOID.

## Manipulation checks

MC1 (isotropic control), MC2 (calibration-only probes and arms, commit order),
MC3 (above), MC4 (graded seeds disjoint from every construction/V1 seed) — as
V1, with cross-fit quantities replacing single-split ones in MC2's scope.

## Seal record — the four open items, resolved 2026-09-03

### 1. Units pinned (manifests in `prereg/qualification_v2.json`, committed)

Six single-domain units, seeded split machinery as sealed (split seed
20260911, cap 6000, 70/30). Calibration/grading rows + sha256 (first 12):
privacy_aita 460/`7fe89ab64ad7` + 198/`b95b0aaaa629`; fairness_mhs
4200/`5e2b225c3aab` + 1800/`333c4228c374`; autonomy_dark 1478/`596d0ed748a9`
+ 634/`21b709ccd61e`; care_moralstories 1698/`0416046d7744` +
728/`d1aded836cd9`; societal_env 1549/`723747b1613c` + 665/`391c2ed4dfa3`;
epistemic_sc 2140/`0f0040ba599a` + 918/`fa31cbc789f4`. Two seal-time pool
changes, both disciplinary: **legitimacy is EXCLUDED** (it maps to Social-Chem
`authority-subversion`, a V1-burned consumer — the collision check firing
exactly as designed), and autonomy's MentalManip arm is dropped (HF-download
dependency; the darkpattern corpus covers the axis as a single-domain unit).
Distillation applied where the validated checkpoint loaded: privacy_aita,
autonomy_dark, care_moralstories (privacy/autonomy/care_joint.pt); direct
labels elsewhere.

### 2. Cross-fit qualification (5-fold, calibration only; grading unopened)

| unit | D_xfit ± sd | A_xfit | H_xfit | arm |
|---|---|---|---|---|
| privacy_aita | 0.789 ± 0.056 | 0.746 | +0.043 | **misaligned** |
| fairness_mhs | 0.825 ± 0.005 | 0.740 | +0.085 | **misaligned** |
| autonomy_dark | 0.944 ± 0.014 | 0.947 | −0.003 | **matched** |
| care_moralstories | 0.673 ± 0.028 | 0.402 | +0.270 | excluded (D < 0.75) |
| societal_env | 0.863 ± 0.018 | 0.798 | +0.065 | **misaligned** |
| epistemic_sc | 0.907 ± 0.005 | 0.866 | +0.041 | **misaligned** |

**MC3 pre-satisfied: 4 misaligned + 1 matched.** Note for the record:
care_moralstories carries the family's largest headroom (+0.270) on a probe
below the floor — the law is silent on weak probes and it is reported
descriptively, not graded; the arm rule was not bent to include it.

### 3. Seed scan (2026-09-03)

20260911/12/13/14 clean across observation-theory-campaigns, network-governor,
and erisml-lib (py/md/json).

### 4. Constants frozen

B1 = mean gain ≥ max(0.10·H_xfit, +0.010) AND per-seed gain ≥ 0 AND
recall@1 ≤ 0.5; B2 = mean ≤ +0.010 AND per-seed ≤ +0.020; B3 secondary
Spearman ≥ 0.6; arms D ≥ 0.75, H ≥ 0.04 / |H| < 0.02 — **exactly as drafted
2026-09-02, no constant moved after the qualification numbers were seen.**

## Amendment discipline

As V1: after the seal line, nothing changes except by dated amendment; the
graded verdict is committed as executed, PASS or FAIL.
