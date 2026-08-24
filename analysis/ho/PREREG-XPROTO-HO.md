# PREREG-XPROTO-HO — handover / mobility cell (the geo-fleet cellular twin)

**STATUS: SEALED 2026-08-23.** FAMILY-CONSTRUCTED: 2026-08-22. Earliest compliant
seal **2026-08-23** (`ho_check.py` enforces the cooling-off in code). The
**sealed graded run is on the real NR substrate** (mode="nrsionna_ho":
`fam_ho.py` on Atlas — a 2-cell mobility geometry, serving-link BLER from the
real Sionna 5G NR LDPC curves). Graded on seeds {20260823, 20260824,
20260825}, disjoint from the shakedown's {0,1,2}. No evidential weight until
sealed and run on the NR substrate.

**IP posture:** public methodology; the **RAN-mobility twin of the geo-fleet
cell** (which cell/replica to route to when the freshness certificate is
stale). Nothing gated.

## The claim

A UE's RSRP measurement report is a certificate: it tells the network "cell X
is best / adequate," and the network keeps serving on that basis. Under
**mobility**, the report ages: the UE crosses the cell edge but the stale
periodic report keeps it on the old serving cell, whose RSRP has dropped and
whose former neighbor now interferes — the serving SINR collapses and the
link fails (HARQ NACK / radio-link failure). Graded against the **post-decision
outcome** (HARQ on the serving cell — the independent witness of whether the
consumer decoded), a stale periodic report has a false-clear rate far above
target, while an **outcome-witnessed** policy (RLM: on K consecutive serving
NACKs, re-measure and re-select) holds. The false-clear rate is
**consumer-relative**: set by the UE's own velocity vs the report cadence.
This is the exact shape of the geo-fleet routing-under-staleness cell, at the
RAN mobility layer. **The witness is the served-link outcome**, as across the
cellular cells.

## Family F-HO (constructed + shaken down 2026-08-22)

Two cells 500 m apart; the UE oscillates deep-cell-0 ↔ deep-cell-1 (5
sweeps) at 30 m/s, crossing the interference-limited edge. Per cell, an
**L3-filtered RSRP** (pathloss PL0+35·log10 d + correlated log-normal
shadowing, σ 6 dB, 20 m decorrelation) drives handover decisions; a mild
per-slot fast-fade term (σ 3 dB, PHY only) perturbs the serving SINR. The
serving SINR is interference-limited (the other cell interferes); the block
decode uses the **real Sionna 5G NR LDPC BLER curves** at a fixed cell-edge
MCS. Three policies over the SAME trajectory: **naive** (hand over only on
the stale periodic RSRP report, period 300 slots), **rlm** (periodic +
re-measure & re-select on K=3 consecutive serving NACKs — the outcome-
witnessed correction), **fresh** (re-select the best cell every slot — the
no-aging control).

## Bars (bind at seal; checked against the family record first)

*Demonstrated on seeds {0,1,2}: naive ≈ 0.31–0.44, rlm ≈ 0.09–0.12,
fresh ≈ 0.08–0.10, ho_lag ≈ 0.29–0.44.*

- **B1 — RSRP-report vacuity under mobility.** Per seed: `naive_bler ≥ 0.25`
  (the stale report false-clears ≥ 2.5× the 0.10 target).
- **B2 — witness holds.** Per seed: `rlm_bler ≤ 0.15`.
- **B3 — dominance.** Per seed: `rlm_bler ≤ naive_bler / 2`.

**Manipulation checks (bars too):**
- **MC1 — mobility is real.** `ho_lag_frac ≥ 0.10` (the naive policy spends a
  real fraction of time on a cell that is not the instantaneous best — the
  aging; if the UE never crosses there is no story).
- **MC2 — best-cell serving is sane.** `fresh_bler ≤ 0.15` (failures are
  attributable to serving the wrong cell, not a broken link).
- **MC3 — non-degenerate.** `n_slot ≥ 5000`, `n_ho ≥ 1` (handovers happen).

**Verdict rule:** any MC failure → VOID; all MCs + B1–B3 pass on every graded
seed → PASS; otherwise FAIL, kept as executed.

**Kills.** `naive_bler < 0.15` — no mobility vacuity in this regime; or
`rlm_bler > 0.30` — the witnessed re-selection does not hold.

## Seal procedure

On 2026-08-23 or later: confirm `HOREP-family.json` (mode "nrsionna_ho")
PASSes `ho_check.py --check-family`, reread this prereg, flip STATUS to
`SEALED <date>`, commit. Then on Atlas run `fam_ho.py --seeds 20260823
20260824 20260825 --out HOREP-graded-raw.json`, pull it, `ho_check.py`
(seal-guarded) → commit `XPROTO-HO-graded.json` as executed.

## Scope

A **link-level 2-cell proxy** for the mobility-robustness problem: an
interference-limited serving SINR + real Sionna LDPC decode, with L3-filtered
RSRP for handover and a fast-fade PHY term. A **system-level** substrate
(ns-3 5G-LENA or similar — many cells, real TTT / A3 events, RLF timers,
ping-pong counters, X2/Xn handover signalling) is the external-validity
graduation, and the natural home for the ping-pong-vs-too-late trade-off in
full. RLM-triggered re-selection is credited prior art; OT's delta is the
*measured, consumer-relative, calibrated* false-clear rate of a stale
measurement report and the *witnessed* alternative — the RAN instance of the
same certificate/witness grammar as the geo-fleet DB cell.

## Provenance

- Exploration: the 5G/6G applicability discussion (HARQ / served-link outcome
  as witness across adaptation certificates; the geo-fleet ↔ handover parallel).
- Geometry + decode: `fam_ho.py` (2-cell mobility + real Sionna LDPC curves).
- Grading: `ho_check.py` (seal-guard + coded cooling-off + NR-only sealed
  grading + pre-seal record check).
