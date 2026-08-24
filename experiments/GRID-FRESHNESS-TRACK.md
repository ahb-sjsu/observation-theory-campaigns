# Grid-Freshness Track: state-estimation staleness in power systems

**Status:** constructed 2026-08-24. Chip 🕒⚡ GRID. Freshness program
([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). Substrate: **pandapower** AC power
flow. Cell **XPROTO-GRID** UNSEALED (shakedown PASS; seal ≥ 2026-08-25). One of
the "dark places" — the false-clear here is rare, catastrophic, and unmeasured.

## Question

A grid operator's state estimate yields a **security certificate** — "all line
loadings within limits." Refreshed every R steps, it **ages** as load drifts, and
**false-clears** when it reports safe while the true AC power flow has a line over
its limit: an **undetected overload**, the precursor to a cascade (a stale/alarmed
-out state estimator is implicated in the 2003 Northeast blackout). The false-clear
is **consumer-relative** — it concentrates on the few binding lines. Witness = the
true loading from an up-to-date power flow (SCADA/PMU).

## Cell

**XPROTO-GRID** (`analysis/grid`, pandapower, IEEE case14): a state estimate held
for R=60 steps false-clears an undetected overload **~1 step in 4** (missing > half
of the true overloads, which occur ~40% of the time under stressed load), while
re-estimating each step holds it at **~1%** — a ~20× dominance. False-clears
concentrate on the critical lines (fc_line_spread > 0), so no blanket security
margin serves every consumer. Bars B1 naive_fc≥0.20 / B2 witnessed_fc≤0.10 / B3
dominance + MC1 overloads-real / MC2 consumer-relative / MC3 non-degenerate.

## Why it's a dark place

The false-clear is rare and catastrophic, and no operator reports the *rate* at
which their security certificate is stale-wrong — it is invisible until a cascade.
Naming the false-clear rate, and deriving the refresh floor from load-change
coherence (OT-14), makes a silent failure measurable. External-validity rung: a
real WLS/AC state estimator with SCADA/PMU noise + bad-data detection on a load
trace; larger cases; N-1 contingency certificates.
