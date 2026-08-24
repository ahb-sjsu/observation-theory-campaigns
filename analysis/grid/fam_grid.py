"""XPROTO-GRID family (F-GRID): consumer-relative staleness of the power-grid
security certificate, on the pandapower AC power flow.

A grid operator's state estimate (SE) yields a security certificate -- "all line
loadings within limits" -- refreshed every R steps. Between refreshes the held
estimate ages as load/generation drift. The certificate **false-clears** when the
held estimate says "all within limits" but the TRUE current power flow has a line
over its limit -- an undetected overload, the precursor to a cascade (a stale
state estimator sat behind the 2003 Northeast blackout). The false-clear is
**consumer-relative**: it concentrates on the few binding (critical) lines, so a
consumer protecting a critical line is exposed while a slack-line consumer is not.

  * consumer = a line's loading (the constraint an operator relies on).
  * certificate = "all within limits" from the last SE -> dispatch/no-shed.
  * witness = the TRUE line loading from an up-to-date AC power flow (SCADA/PMU).
  * naive: hold the SE for R steps; witnessed: re-estimate every step.

Substrate: pandapower AC power flow on IEEE case14; lines rated to a declared base
utilisation so load variation creates binding constraints. Emits GRIDREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandapower as pp
import pandapower.networks as nw

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed line-system + cell constants -----------------------------
TARGET_UTIL = 0.60         # rate each line to 60% loading at base (scale 1.0)
MEAN_SCALE = 1.29          # load walk centre (system stressed near its limits)
RHO = 0.75                 # AR(1) load-scale persistence
SIGMA = 0.09               # AR(1) load-scale innovation
SCALE_LO, SCALE_HI = 0.85, 1.50
R_REPORT = 60              # SE refresh period (steps)
SE_NOISE_PCT = 1.5         # state-estimation noise on loading% (1 sigma)
DURATION = 2000
LIMIT = 100.0              # loading% limit


def _build_lut():
    """Precompute per-line true loading% over a load-scale grid (real AC PF)."""
    net = nw.case14(); pp.runpp(net)
    net.line["max_i_ka"] = net.res_line.i_ka.values / TARGET_UTIL
    p0 = net.load.p_mw.values.copy(); q0 = net.load.q_mvar.values.copy()
    grid = np.round(np.arange(SCALE_LO, SCALE_HI + 1e-9, 0.005), 3)
    lut = {}
    for sc in grid:
        net.load["p_mw"] = p0 * sc; net.load["q_mvar"] = q0 * sc
        try:
            pp.runpp(net)
            lut[sc] = net.res_line.loading_percent.values.copy()
        except Exception:
            lut[sc] = np.full(len(net.line), 150.0)   # divergence => severe overload
    return grid, lut, len(net.line)


def _scale_walk(rng, n):
    s = np.empty(n); s[0] = MEAN_SCALE
    for t in range(1, n):
        s[t] = np.clip(MEAN_SCALE + RHO * (s[t - 1] - MEAN_SCALE) + rng.normal(0, SIGMA),
                       SCALE_LO, SCALE_HI)
    return s


def run_cell(seed, grid, lut, n_lines):
    rng = np.random.default_rng(seed)
    scales = _scale_walk(rng, DURATION)
    true = np.stack([lut[grid[np.abs(grid - s).argmin()]] for s in scales])  # T x lines
    held = true[0] + rng.normal(0, SE_NOISE_PCT, n_lines)      # last SE estimate (naive)
    naive_fc = wit_fc = true_over = 0
    per_line_fc = np.zeros(n_lines)
    for t in range(DURATION):
        if t % R_REPORT == 0:
            held = true[t] + rng.normal(0, SE_NOISE_PCT, n_lines)   # refresh SE
        fresh = true[t] + rng.normal(0, SE_NOISE_PCT, n_lines)      # witnessed: re-estimate now
        true_over_lines = true[t] >= LIMIT
        true_over += bool(true_over_lines.any())
        # naive certificate clears "all safe" from the HELD estimate
        if (held < LIMIT).all() and true_over_lines.any():
            naive_fc += 1
        if (fresh < LIMIT).all() and true_over_lines.any():
            wit_fc += 1
        # per-line false-clear (consumer = that line): held says safe, line truly over
        per_line_fc += (held < LIMIT) & true_over_lines
    n = DURATION
    per_line_fc /= n
    return {
        "seed": int(seed), "mode": "pandapower",
        "naive_fc": round(naive_fc / n, 4), "witnessed_fc": round(wit_fc / n, 4),
        "true_overload_rate": round(true_over / n, 4),
        "fc_line_spread": round(float(per_line_fc.std()), 4),   # >0 => consumer-relative
        "n_steps": n, "n_lines": int(n_lines), "r_report": R_REPORT,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "GRIDREP-family.json"))
    args = ap.parse_args()
    print("precomputing AC power-flow LUT (pandapower case14)...", flush=True)
    grid, lut, n_lines = _build_lut()
    cells = [run_cell(s, grid, lut, n_lines) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: naive_fc={c['naive_fc']} witnessed_fc={c['witnessed_fc']} "
              f"| true_overload={c['true_overload_rate']} fc_line_spread={c['fc_line_spread']}",
              flush=True)
    rec = {"family": "F-GRID", "mode": "pandapower",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"target_util": TARGET_UTIL, "mean_scale": MEAN_SCALE, "rho": RHO,
                         "sigma": SIGMA, "r_report": R_REPORT, "se_noise_pct": SE_NOISE_PCT,
                         "duration": DURATION, "limit": LIMIT,
                         "substrate": "pandapower AC power flow, IEEE case14, lines rated to "
                                      "60% base utilisation; witness = true AC PF loading"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
