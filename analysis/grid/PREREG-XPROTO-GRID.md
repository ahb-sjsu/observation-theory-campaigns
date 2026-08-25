# PREREG-XPROTO-GRID — consumer-relative staleness of the grid security certificate

**STATUS: SEALED 2026-08-25.** FAMILY-CONSTRUCTED: 2026-08-24. Earliest compliant seal
**2026-08-25** (`grid_check.py` codes the cooling-off). Graded seeds {20260825,
20260826, 20260827}, disjoint from the shakedown's {0,1,2}. Substrate =
**pandapower** AC power flow (the evidence rung).

**IP posture:** public methodology; the power-systems instance of the
witnessed-freshness-certificate grammar. Nothing gated.

## The claim

A grid operator's state estimate (SE) yields a **security certificate** — "all
line loadings within limits" — refreshed every R steps. Between refreshes the held
estimate ages as load/generation drift. The certificate **false-clears** when the
held estimate reports "all within limits" but the TRUE current AC power flow has a
line over its limit: an **undetected overload**, the precursor to a cascade (a
stale/alarm-suppressed state estimator is implicated in the 2003 Northeast
blackout). The false-clear is **consumer-relative**: it concentrates on the few
binding (critical) lines, so a consumer relying on a critical line is exposed while
a slack-line consumer is not — no single "the system is secure" assertion serves
both. Re-estimating each step (the witness) catches the overloads.

## Family F-GRID (constructed + shaken down 2026-08-24)

pandapower AC power flow on IEEE **case14**; each line rated to **60% loading at
base** (a declared modeling choice creating binding constraints). Load scaled by an
AR(1) walk (centre 1.29, ρ=0.75, σ=0.09, clipped [0.85,1.50]) — the system runs
stressed near its limits. True per-line loading precomputed over a load-scale grid
(real AC PF). SE estimates loading with 1.5% noise. **naive**: hold the SE for
R=60 steps; **witnessed**: re-estimate every step. A certificate clears when the
estimate shows all lines < 100%; it false-clears when it clears but the true state
has a line ≥ 100%.

## Bars (bind at seal; checked against the family record first)

*Demonstrated (seeds {0,1,2}): naive_fc ≈ 0.24–0.31, witnessed_fc ≈ 0.011–0.013,
true_overload ≈ 0.37–0.42, fc_line_spread ≈ 0.067–0.081. The bar sits where the
robust effect lives, not at a round number — the headline is the ~20× contrast.*

- **B1 — stale-certificate vacuity.** Per seed: `naive_fc ≥ 0.20` (the held SE
  false-clears an undetected overload ≥ 1 step in 5; it misses > half of all true
  overloads, which occur ~40% of the time).
- **B2 — witness holds.** Per seed: `witnessed_fc ≤ 0.10`.
- **B3 — dominance.** Per seed: `witnessed_fc ≤ naive_fc / 2`.

**Manipulation checks (bars too):**
- **MC1 — overloads are real.** `true_overload_rate ≥ 0.10` (the true state genuinely
  exceeds limits; if it never does there is no story).
- **MC2 — consumer-relativity.** `fc_line_spread ≥ 0.02` (per-line false-clears
  concentrate on the critical lines — a footprint property, not uniform; a blanket
  margin cannot be right for all consumers).
- **MC3 — non-degenerate.** `n_steps ≥ 1000` and `witnessed_fc < naive_fc`.

**Verdict:** any MC fail → VOID; all MCs + B1–B3 every seed → PASS; else FAIL,
kept. **Kills:** `naive_fc < 0.10` (no staleness vacuity) or `witnessed_fc > 0.20`
(re-estimation does not help).

## Seal procedure

On 2026-08-25+: confirm `GRIDREP-family.json` PASSes `--check-family`, reread, flip
STATUS to SEALED, commit; run `fam_grid.py --seeds 20260825 20260826 20260827 --out
GRIDREP-graded-raw.json`, `grid_check.py` → commit `XPROTO-GRID-graded.json`.

## Scope

pandapower AC power flow is the real physics; line ratings set to a base
utilisation is a declared choice to create binding constraints on a standard test
case. External-validity graduations (declared, not claimed): a real WLS/AC state
estimator with SCADA/PMU noise and bad-data detection; a real load trace; a larger
case (118/1354pegase); N-1 contingency certificates. Credited prior art: EMS state
estimation, real-time contingency analysis, PMU-based dynamic-state estimation;
OT's delta is the **measured, consumer-relative false-clear rate** of the security
certificate as a first-class number, and the refresh floor from load-change
coherence.

## Provenance

- Exploration: the "dark places" survey — grid state-estimation staleness as the
  rare-but-catastrophic freshness certificate (blackout precursor).
- Family + grading: `fam_grid.py` (pandapower) + `grid_check.py` (seal-guard +
  coded cooling-off + pandapower-only sealed grading + pre-seal record check).
