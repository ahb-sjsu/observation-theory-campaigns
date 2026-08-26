"""XPROTO-GRID-FLIP family (F-GRID-FLIP): the two-consumer verdict inversion (the
Flip) in the grid security certificate, with its taxonomy-predicted null.

The sealed XPROTO-GRID cell drives every load with ONE global scale, so every
line reads the same one-dimensional projection of the state. That is the coupling
null and it cannot invert. The flip needs two independent axes, so this cell
splits the case14 loads into two ZONES with independent AR(1) walks. Lines sort
into fleets by which zone dominates their loading sensitivity (real AC power
flow): the Z1-fleet reads zone 1, the Z2-fleet reads zone 2.

Policies: a fixed fleet-mean certification margin (5 percentage points of
loading) allocated two ways. Policy A gives each line margin in proportion to its
zone-1 sensitivity. Policy B gives the same total in proportion to its zone-2
sensitivity. A line is certified safe when the held estimate sits below
LIMIT minus its margin; it false-clears when certified safe and truly over.
Claim: the Z1-fleet does better under A, the Z2-fleet under B, and the fleet
aggregate cannot order the pair.

Registered null: the sealed cell's single global walk, with the same two margin
policies. One driver means one read axis, so no inversion is expected.

Substrate: pandapower AC power flow on IEEE case14 (2-D load-scale LUT of real
power flows). Run in the grid venv (numpy<2). Emits GRIDFLIPREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pandapower as pp
import pandapower.networks as nw

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET_UTIL = 0.60
MEAN_SCALE = 1.29
RHO = 0.75
SIGMA = 0.09
SCALE_LO, SCALE_HI = 0.85, 1.50
R_REPORT = 60
SE_NOISE_PCT = 1.5
DURATION = 2000
LIMIT = 100.0
MARGIN_MEAN = 5.0            # fleet-mean certification margin (loading %)
STEP = 0.05                  # 2-D LUT grid step
DOM_RATIO = 1.3              # zone-dominance ratio for fleet membership


def _build():
    """2-D LUT of true per-line loading% over (zone1 scale, zone2 scale)."""
    net = nw.case14(); pp.runpp(net)
    net.line["max_i_ka"] = net.res_line.i_ka.values / TARGET_UTIL
    p0 = net.load.p_mw.values.copy(); q0 = net.load.q_mvar.values.copy()
    z1 = np.arange(len(net.load)) % 2 == 0            # interleaved zone split
    grid = np.round(np.arange(SCALE_LO, SCALE_HI + 1e-9, STEP), 3)
    lut = {}
    for s1 in grid:
        for s2 in grid:
            sc = np.where(z1, s1, s2)
            net.load["p_mw"] = p0 * sc; net.load["q_mvar"] = q0 * sc
            try:
                pp.runpp(net)
                lut[(s1, s2)] = net.res_line.loading_percent.values.copy()
            except Exception:
                lut[(s1, s2)] = np.full(len(net.line), 150.0)
    # zone sensitivities at the walk centre (real AC PF differences)
    c = grid[np.abs(grid - MEAN_SCALE).argmin()]
    hi = grid[min(len(grid) - 1, np.abs(grid - MEAN_SCALE).argmin() + 2)]
    sens1 = np.abs(lut[(hi, c)] - lut[(c, c)])
    sens2 = np.abs(lut[(c, hi)] - lut[(c, c)])
    return grid, lut, len(net.line), sens1, sens2


def _walk(rng, n):
    s = np.empty(n); s[0] = MEAN_SCALE
    for t in range(1, n):
        s[t] = np.clip(MEAN_SCALE + RHO * (s[t - 1] - MEAN_SCALE) + rng.normal(0, SIGMA),
                       SCALE_LO, SCALE_HI)
    return s


def _snap(grid, s):
    return grid[np.abs(grid - s).argmin()]


def _fc_per_line(true_series, margins, rng, n_lines):
    """Per-line false-clear rate: held SE certifies safe (held < LIMIT - margin)
    while the line is truly over. Held estimate refreshed every R_REPORT steps."""
    held = true_series[0] + rng.normal(0, SE_NOISE_PCT, n_lines)
    fc = np.zeros(n_lines)
    for t in range(len(true_series)):
        if t % R_REPORT == 0:
            held = true_series[t] + rng.normal(0, SE_NOISE_PCT, n_lines)
        fc += (held < LIMIT - margins) & (true_series[t] >= LIMIT)
    return fc / len(true_series)


def run_cell(seed, grid, lut, n_lines, sens1, sens2):
    rng = np.random.default_rng(seed)
    # fleets: lines whose loading is dominated by one zone's sensitivity
    f1 = sens1 > DOM_RATIO * sens2
    f2 = sens2 > DOM_RATIO * sens1
    m_a = sens1 / sens1.mean() * MARGIN_MEAN            # protect zone-1 readers
    m_b = sens2 / sens2.mean() * MARGIN_MEAN            # protect zone-2 readers
    # flip construction: independent zone walks
    s1 = _walk(rng, DURATION); s2 = _walk(rng, DURATION)
    true2 = np.stack([lut[(_snap(grid, a), _snap(grid, b))] for a, b in zip(s1, s2)])
    out = {"seed": int(seed), "mode": "pandapower", "n_lines": int(n_lines),
           "n_z1": int(f1.sum()), "n_z2": int(f2.sum()),
           "mean_margin_A": round(float(m_a.mean()), 4),
           "mean_margin_B": round(float(m_b.mean()), 4)}
    for m, tag in ((m_a, "A"), (m_b, "B")):
        fc = _fc_per_line(true2, m, np.random.default_rng(seed + 50), n_lines)
        out[f"fc_Z1_{tag}"] = round(float(fc[f1].mean()), 4)
        out[f"fc_Z2_{tag}"] = round(float(fc[f2].mean()), 4)
        out[f"fc_fleet_{tag}"] = round(0.5 * (out[f"fc_Z1_{tag}"] + out[f"fc_Z2_{tag}"]), 4)
    out["flip"] = bool(out["fc_Z1_A"] < out["fc_Z1_B"] and out["fc_Z2_B"] < out["fc_Z2_A"])
    # null construction: ONE global walk (both zones share it), same two policies
    sg = _walk(np.random.default_rng(seed + 200), DURATION)
    true1 = np.stack([lut[(_snap(grid, a), _snap(grid, a))] for a in sg])
    for m, tag in ((m_a, "A"), (m_b, "B")):
        fc = _fc_per_line(true1, m, np.random.default_rng(seed + 90), n_lines)
        out[f"null_fc_Z1_{tag}"] = round(float(fc[f1].mean()), 4)
        out[f"null_fc_Z2_{tag}"] = round(float(fc[f2].mean()), 4)
    out["null_flip"] = bool(out["null_fc_Z1_A"] < out["null_fc_Z1_B"]
                            and out["null_fc_Z2_B"] < out["null_fc_Z2_A"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "GRIDFLIPREP-family.json"))
    args = ap.parse_args()
    print("precomputing 2-D AC power-flow LUT (pandapower case14)...", flush=True)
    grid, lut, n_lines, sens1, sens2 = _build()
    cells = [run_cell(s, grid, lut, n_lines, sens1, sens2) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: Z1 A={c['fc_Z1_A']} B={c['fc_Z1_B']} | "
              f"Z2 A={c['fc_Z2_A']} B={c['fc_Z2_B']} | fleets n={c['n_z1']}/{c['n_z2']} | "
              f"FLIP={c['flip']} null_flip={c['null_flip']}", flush=True)
    rec = {"family": "F-GRID-FLIP", "mode": "pandapower",
           "constants": {"target_util": TARGET_UTIL, "mean_scale": MEAN_SCALE,
                         "margin_mean": MARGIN_MEAN, "r_report": R_REPORT,
                         "dom_ratio": DOM_RATIO, "duration": DURATION, "step": STEP,
                         "substrate": "pandapower AC PF, case14, two-zone loads"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
