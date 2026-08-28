# PREREG-XPROTO-QOT-CM — the optical flip pair re-matched in a true cost functional

**STATUS: DRAFT — FAMILY-CONSTRUCTED 2026-08-28, EARLIEST SEAL 2026-08-29** (cooling-off
rule: one full day between family construction and seal). Graded seeds {20260906,
20260907, 20260908}, disjoint from the shakedown's {0,1,2}. Substrate = fam_qot's
GNPy GN-model GSNR over CORONET-CONUS (mode "gnpy-coronet") through fam_qotflip's
footprint fleets. The cost-matching cell the formal core requires (Def. 1, Eq. 1:
resource equivalence must be stated in C, not in nominal units), for the SIGMETRICS
2027 policy-reversal paper.

Why the construction date moved: the original graded-seed registration
{20260828, 20260829, 20260830} collided with the graded seeds of the sealed
XPROTO-CSI-FLIP cell, whose outcome on two of them is already visible in
`XPROTO-CSI-FLIP-graded.json`, so the registration was replaced on 2026-08-28
before any seal and the cooling-off clock restarted from that date. The
calibration this cell shares with F-QOT-GRAD and the registered predictions are
unchanged and were never re-derived: they are fixed by calibration seeds
{990..997}, which the replacement did not touch.

## Why this cell

The sealed XPROTO-QOT-FLIP pair is matched on fleet-mean margin in dB — C linear in
m, the NOMINAL budget. Capacity is nonlinear in dB, so equal mean margin does not
mean equal capacity forgone, and a critic can attribute the reversal to a hidden
budget advantage. This cell re-matches the pair EXACTLY in a declared capacity cost
functional and re-runs the A/B evaluation. If the reversal dies under true-cost
matching, that is a kept negative and is reportable, not discardable.

## The claim

The reversal survives cost re-matching: with policy B rescaled so that
C(m^B_cm) = C(m^A) exactly in the declared capacity functional, the class deltas
keep their sealed signs on every graded seed and lambda* moves by less than the
declared tolerance from the nominal-matching value.

## Family F-QOT-CM (code constructed + shaken down 2026-08-27; re-registered 2026-08-28)

`fam_qotcm.py`. Fleet, policies, and evaluation as in F-QOT-FLIP (K = 120, R/P
footprint fleets, m^A reach-weighted, m^B centrality-weighted, 1.0 dB nominal
fleet-mean; this family's own monitoring-noise stream, offset 6000, one draw per
seed, shared by all three policy evaluations — paired).

Cost functional (declared): C(m) = Σ_i [log2(1 + γ_i) − log2(1 + γ_i·10^(−m_i/10))],
γ_i = 10^(prov_GSNR_i/10) — the Shannon capacity forgone by backing service i's
provisioned operating GSNR off by its margin, summed over the fleet (bit/symbol
units). One-sentence justification: the substrate exposes each service's
provisioned GSNR, and the capacity price of reserving m_i dB is exactly the Shannon
capacity delta at that operating point, which is nonlinear in dB and
service-dependent, so equal mean dB is only nominal equivalence.

Rebalancing (declared): policy B is rescaled by one scalar s (m^B_cm = s·m^B_nom)
so C(m^B_cm) = C(m^A) exactly; B rather than A so the reach-weighted policy stays
the fixed reference shared with F-QOT-FLIP and F-QOT-GRAD, and a single scalar is
the minimal change that restores C-equality while preserving B's shape. Solver:
bisection on s in [0.25, 4.0] (C strictly increasing in s), 200 iterations;
relative cost residual must be ≤ 1e-9 (MC3; achieved ~1e-16 in shakedown).

## Bars (bind at seal; graded on {20260906, 20260907, 20260908})

- **B1 — signs survive cost matching.** Per seed: ΔR_R^cm < 0 < ΔR_P^cm, with the
  same signs as the nominal pair in the same run.
- **B2 — lambda* stability.** Per seed: |lambda*_cm − lambda*_nom| ≤ 0.10
  (tolerance declared from the shakedown, where the shift was 0.0000 on all seeds;
  pilot, disclosed; 0.10 also matches the F-QOT-GRAD band construction floor scale).
  To be explicit about that last clause: 0.10 is twice the F-QOT-GRAD band
  half-width floor of 0.05. It is adopted for scale consistency across the two
  cells. It is not derived from the F-QOT-GRAD floor, and nothing in this cell's
  verdict depends on the relation.

**Manipulation checks (bars too):**
- **MC1 — sane evaluation.** Per seed: all cost-matched class false-clears strictly
  inside (0,1).
- **MC2 — the policies differ.** Per seed: RMS(m^A − m^B_cm) ≥ 0.1 dB.
- **MC3 — the match is exact.** Per seed: relative cost residual ≤ 1e-9.
- **MC4 — the nominal flip holds in the same run.** Per seed: the nominal pair
  flips (if the nominal reversal itself fails on a graded seed, the comparison is
  vacuous and the cell is VOID, not silently graded).
- **MC5 — the graded record carries exactly the registered seeds.** The graded
  record must contain the three registered seeds {20260906, 20260907, 20260908},
  no more and no fewer. Violation VOIDs the cell. Coded in `qotcm_check.py`
  line 184, which refuses to grade any record whose seed set differs from the
  registered set, so no verdict can be minted from a padded or truncated record.

**Verdict:** any MC fail → VOID; B1 + B2 every seed → PASS; else FAIL, kept.
**Kills:** a cost-matched sign flip on any graded seed (the reversal is a
nominal-budget artifact) or a lambda* shift above tolerance.

## Shakedown (2026-08-27, seeds {0,1,2} as graded stand-ins; NEVER quoted in papers)

`QOTCMREP-shakedown.json`: verdict PASS. Rebalancing size (the informative number):
s = 0.9837 / 0.9855 / 0.9829; nominal cost gap C(A) − C(B_nom) = −1.65% / −1.47% /
−1.73% of C(A) (B nominal is slightly the COSTLIER policy in capacity, so it is
scaled DOWN ~1.6%); mean margin of B_cm 0.984 / 0.985 / 0.983 dB against the 1.0 dB
nominal. The rebalancing is tiny in the shakedown: nominal dB matching came within
~1.7% of true capacity matching, and the ~1.6% margin rescaling moved no false-clear
at all (deltas and lambda* unchanged to 4 decimals, shift 0.0000). Both of those are
pilot numbers on stand-in seeds and neither is a claim about the substrate. The
graded record on {20260906, 20260907, 20260908} settles both: how close nominal dB
matching is to true capacity matching here, and whether the rescaling moves any
false-clear. The shakedown fixes only that the code runs. Runtime: ~1 s for the
three cells + ~1 s GNPy comb precompute.
Shakedown numbers stand in for nothing beyond code correctness.

## Seal procedure

On 2026-08-29+: reread this prereg, flip STATUS to SEALED, commit; run
`fam_qotcm.py --graded --seeds 20260906 20260907 20260908` in the qot venv; write
`qotcm_check.py` (coded cooling-off + substrate guard, house pattern) and commit
`XPROTO-QOT-CM-graded.json`.

## Scope

The claim is robustness of the sealed reversal to true-cost re-matching in the
declared functional, not optimality of the functional. A different declared C
(goodput-weighted, launch-power) is future work; Eq. 1 of the formal core is the
matching criterion for any of them. Provenance: formal-core.tex (Def. 1, Eq. 1),
XPROTO-QOT-FLIP (sealed pair), OUTLINE.md (cost-matching requirement),
`fam_qotcm.py`.
