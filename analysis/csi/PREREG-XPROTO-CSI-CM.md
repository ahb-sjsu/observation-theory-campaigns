# PREREG-XPROTO-CSI-CM — the radio flip pair re-matched in a true cost functional

**STATUS: DRAFT — FAMILY-CONSTRUCTED 2026-08-27, EARLIEST SEAL 2026-08-28** (cooling-off
rule: one full day between family construction and seal). Graded seeds {20260828,
20260829, 20260830}, disjoint from the shakedown's {0,1,2}. Substrate = real Sionna
5G NR LDPC BLER curves + TDL-A fading (`csi_sionna`, mode "nrsionna") through
fam_csiflip's fleets. The radio twin of XPROTO-QOT-CM: the cost-matching cell the
formal core requires (Def. 1, Eq. 1), for the SIGMETRICS 2027 policy-reversal paper.

## Why this cell

The sealed XPROTO-CSI-FLIP pair is matched on fleet-mean margin in dB, the NOMINAL
budget. Spectral efficiency is nonlinear in dB and SNR-dependent, and here the
nominal matching is genuinely loose: policy A spends its margin on 12 dB users where
a dB of backoff forgoes more MCS spectral efficiency than on policy B's 7 dB users,
so A is the costlier policy at equal mean dB. A critic can attribute the sealed
reversal to that hidden budget gap. This cell re-matches the pair EXACTLY in the
substrate's own MCS cost and re-runs the evaluation. If the reversal dies, that is a
kept negative and is reportable, not discardable.

## The claim

The reversal survives cost re-matching: with policy B rescaled so that
C(m^B_cm) = C(m^A) exactly in the declared spectral-efficiency functional, the fleet
deltas keep their sealed signs on every graded seed and lambda* moves by less than
the declared tolerance from the nominal-matching value.

## Family F-CSI-CM (constructed + shaken down 2026-08-27)

`fam_csicm.py`. Fleets, policies, and evaluation as in F-CSI-FLIP (12 users per
fleet, per-user TDL-A traces with the flip sub-seeds, 6000 TTI, 20-TTI reports,
m^A Doppler-weighted, m^B deficit-weighted, 1.5 dB nominal fleet mean; per-user
random streams seeded exactly as the sealed flip evaluation, shared by all three
policy evaluations — paired).

Cost functional (declared): C(m) = Σ_i [SE(snr_i) − SE(snr_i − m_i)], snr_i = the
user's mean SNR (12 dB fleet M, 7 dB fleet S), SE(x) = piecewise-linear
interpolation of the per-MCS spectral efficiency Qm·R over the required-SNR points
measured from the real Sionna LDPC curves at the 0.10 BLER target, clamped at the
table ends. One-sentence justification: a dB of selection backoff costs the link
exactly the MCS spectral efficiency it forgoes at the operating SNR, and that price
is nonlinear and SNR-dependent, so equal mean dB is only nominal equivalence.

Rebalancing (declared): policy B is rescaled by one scalar s (m^B_cm = s·m^B_nom)
so C(m^B_cm) = C(m^A) exactly; B rather than A so the Doppler-weighted policy stays
the fixed reference shared with F-CSI-FLIP and F-CSI-GRAD, and a single scalar is
the minimal change that restores C-equality while preserving B's deficit shape.
Solver: bisection on s in [0.25, 4.0] (C nondecreasing in s, continuous
piecewise-linear), 200 iterations; relative cost residual must be ≤ 1e-9 (MC3;
achieved 0.0 in shakedown). Because the fleet composition and both policy shapes
are seed-independent, s is one fleet constant: s = 1.24128 (pilot, disclosed;
deterministic given the cached curves).

## Bars (bind at seal; graded on {20260828, 20260829, 20260830})

- **B1 — signs survive cost matching.** Per seed: ΔR_M^cm < 0 < ΔR_S^cm, with the
  same signs as the nominal pair in the same run.
- **B2 — lambda* stability.** Per seed: |lambda*_cm − lambda*_nom| ≤ 0.10
  (tolerance declared from the shakedown, where the shift was 0.0224-0.0269;
  pilot, disclosed; 2 times the largest pilot shift rounded up to the 0.05-grid,
  matching the GRAD band floor scale).

**Manipulation checks (bars too):**
- **MC1 — sane evaluation.** Per seed: all cost-matched fleet NACK rates strictly
  inside (0,1).
- **MC2 — the policies differ.** Per seed: RMS(m^A − m^B_cm) ≥ 0.5 dB.
- **MC3 — the match is exact.** Per seed: relative cost residual ≤ 1e-9.
- **MC4 — the nominal flip holds in the same run.** Per seed: the nominal pair
  flips (otherwise the comparison is vacuous and the cell is VOID).

**Verdict:** any MC fail → VOID; B1 + B2 every seed → PASS; else FAIL, kept.
**Kills:** a cost-matched sign flip on any graded seed (the reversal is a
nominal-budget artifact) or a lambda* shift above tolerance.

## Shakedown (2026-08-27, seeds {0,1,2} as graded stand-ins; NEVER quoted in papers)

`CSICMREP-shakedown.json`: verdict PASS. Rebalancing size (the informative
numbers, and NOT tiny here, unlike the optical twin): nominal cost gap
C(A) − C(B_nom) = +16.29% of C(A) (8.2401 vs 6.8980 SE units); s = 1.24128, so
the cost-matched B carries a 1.862 dB fleet-mean margin against the 1.5 dB
nominal — a 24% level increase concentrated on the S fleet. The reversal
strengthens slightly rather than dying: ΔR_M essentially unchanged (−0.1356 →
−0.1352 on seed 0), ΔR_S up (+0.1035 → +0.1130), lambda* shifts +0.0224 /
+0.0269 / +0.0242. Runtime on Atlas CPU: 15.2 s for the three cells (~5.1 s per
seed), cached LDPC curves. Shakedown numbers stand in for nothing beyond code
correctness.

## Seal procedure

On 2026-08-28+: reread this prereg, flip STATUS to SEALED, commit; on Atlas run
`fam_csicm.py --graded --seeds 20260828 20260829 20260830` (sionna-venv, CPU),
pull; write `csicm_check.py` (coded cooling-off + substrate guard, house pattern)
and commit `XPROTO-CSI-CM-graded.json`.

## Scope

The claim is robustness of the sealed reversal to true-cost re-matching in the
declared functional, not optimality of the functional or of the allocators. The
16% nominal cost gap is itself a finding for the paper's cost-matching section:
equal mean dB was a genuinely loose budget on this substrate, and the reversal is
not an artifact of it. Provenance: formal-core.tex (Def. 1, Eq. 1),
XPROTO-CSI-FLIP (sealed pair), XPROTO-QOT-CM (optical twin), OUTLINE.md
(cost-matching requirement), `fam_csicm.py`.
