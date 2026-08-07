#!/usr/bin/env python3
"""PF-8 decay gate, governed exploratory run.

CAMPAIGN.md section PF-8 asks whether folding can account for particle
decay, one particle becoming two. The protocol with every bar is
written into that section and committed before this file runs. Every
declared number below is cited there and comes from the committed
probe record results/pf8-blind-probe.json.

PF-8a, the parity audit and the blind-consumer loophole, on the four
PF6-002 probe-verified members with the frozen PF-6 integrator and the
frozen polyline crossing instrument, and on the four PF5-002 cells with
the frozen PF-5 census.

PF-8b, lifetime statistics, on the thermal arm, measurement only.

Exploratory label. Not a sealed registration.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pf4_pilot as pilot  # noqa: E402
from pf5_accounting import census_run, signed_count_rule  # noqa: E402
from pf6_covariance import fold_count, integrate  # noqa: E402
from projection_fold import (  # noqa: E402
    canonical_sha256,
    polyline_level_crossings,
)

# ---- arm A, deterministic members bound by PREREG-PF6-002 ----------
MEMBERS = [(0.60, 0.8957885742187499, 3.0),
           (0.70, 1.0448364257812501, 3.0),
           (0.80, 1.2020141601562502, 3.0),
           (0.90, 1.3605468750000003, 2.0)]
PROBE_FOLDS = [4, 2, 2, 2]
N_STEPS = 40_000
LEVEL_FRACTIONS = [k / 100.0 for k in range(1, 100)]
EXCURSION_FRACTIONS = [0.1 * k for k in range(1, 10)]

# ---- the declared blind consumer -----------------------------------
# Fixed from results/pf8-blind-probe.json, record sha 6dce4c52a31e...
U_BLIND_LO = -0.70
U_BLIND_HI = 0.70

# ---- arm B, thermal cells bound by PREREG-PF5-002 ------------------
CELLS = [(0.60, 0.8957885742187499),
         (0.70, 1.0448364257812501),
         (0.80, 1.2020141601562502),
         (0.90, 1.3605468750000003)]
N_CELL = 5_000
SEEDS = [8_800_000 + 1000 * i for i in range(4)]
K_POLY = 100
LEVEL_MULTS = [-0.61, -0.26, 0.14, 0.41, 0.69]

# ---- PF-8b survival ladder -----------------------------------------
F_LADDER = [round(0.900 + 0.025 * k, 4) for k in range(21)]

MIN_MULTIBRANCH_LEVELS = 1
MIN_HIDDEN_CROSSINGS = 1


def detector_crossings(ts, pts, us, level, dt):
    """The detector model. The crossing list is the frozen polyline
    instrument's, keyed on the evolution parameter it returns, and the
    transverse coordinate of each crossing is read off by linear
    interpolation at that parameter."""
    taus = np.arange(len(ts)) * dt
    crossings, _ = polyline_level_crossings(taus, ts, pts, float(level))
    out = []
    for c in crossings:
        idx = c["tau"] / dt
        k = int(math.floor(idx))
        k = max(0, min(k, len(us) - 2))
        frac = idx - k
        out.append({"orientation": float(c["orientation"]),
                    "u": float(us[k] + frac * (us[k + 1] - us[k]))})
    return out


def blind_observer_record(ts, pts, us, level, lo, hi):
    """The blind consumer's own record, built by an independent route.
    It scans its own samples for sign changes of the observed time
    against the level, interpolates the transverse coordinate there by
    index arithmetic rather than by the evolution parameter, and simply
    fails to record any branch whose transverse coordinate falls inside
    its blind window."""
    s = np.asarray(ts, dtype=float) - float(level)
    if np.any(s == 0.0):
        raise ValueError("non-generic level for the observer record")
    seen = 0
    for k in np.nonzero(s[:-1] * s[1:] < 0.0)[0]:
        a = s[k] / (s[k] - s[k + 1])
        uu = us[k] + a * (us[k + 1] - us[k])
        if not (lo <= uu <= hi):
            seen += 1
    return int(seen)


def member_levels(ts, pts):
    """The declared ladder. A uniform background across the observed
    span, merged with levels inside every fold excursion, because the
    probe measured excursions as narrow as 0.00025 against a background
    spacing near 0.2."""
    t0, t1 = float(ts[0]), float(ts[-1])
    fold_idx = np.nonzero(pts[:-1] * pts[1:] < 0.0)[0]
    fold_ts = [float(ts[k]) for k in fold_idx]
    levels = [t0 + f * (t1 - t0) for f in LEVEL_FRACTIONS]
    excursions = []
    for j in range(0, len(fold_ts) - 1, 2):
        lo, hi = sorted((fold_ts[j], fold_ts[j + 1]))
        excursions.append({"lo": lo, "hi": hi, "width": hi - lo})
        levels += [lo + f * (hi - lo) for f in EXCURSION_FRACTIONS]
    return sorted(levels), fold_ts, excursions


def arm_a(record):
    members = {}
    d1_odd_jumps = 0
    d1_parity_failures = 0
    d2_rule_failures = 0
    d2_signed_spread = 0
    d3_mismatches = 0
    d3_parity_flips = 0
    d3_observations = 0
    d3_apparent_decays = 0
    d4_members_without_folds = 0
    total_hidden = 0
    total_multibranch = 0
    members_audited = 0
    refused_total = 0
    for idx, (p, e, pu0) in enumerate(MEMBERS):
        ts, pts, us, pus = integrate(p, e, n_steps=N_STEPS, pu0=pu0)
        t0, t1 = float(ts[0]), float(ts[-1])
        nf = fold_count(pts)
        members_audited += 1
        if nf < 1:
            d4_members_without_folds += 1
        levels, fold_ts, excursions = member_levels(ts, pts)

        seq_complete = []
        seq_blind = []
        signed_seen = set()
        used_levels = []
        refused = 0
        hidden_here = 0
        multibranch_here = 0
        for lv in levels:
            try:
                cr = detector_crossings(ts, pts, us, lv, pilot.DT)
                blind_seen = blind_observer_record(
                    ts, pts, us, lv, U_BLIND_LO, U_BLIND_HI)
            except ValueError:
                refused += 1
                continue
            n_complete = len(cr)
            hidden = sum(1 for c in cr
                         if U_BLIND_LO <= c["u"] <= U_BLIND_HI)
            predicted = n_complete - hidden
            signed = int(sum(c["orientation"] for c in cr))
            expect = (1 if t1 > lv else 0) - (1 if t0 > lv else 0)
            if n_complete % 2 != abs(expect) % 2:
                d1_parity_failures += 1
            if blind_seen != predicted:
                d3_mismatches += 1
            if (n_complete - predicted) % 2 != 0:
                d3_parity_flips += 1
            d3_observations += 1
            hidden_here += hidden
            if n_complete > 1:
                multibranch_here += 1
            signed_seen.add(signed)
            seq_complete.append(n_complete)
            seq_blind.append(blind_seen)
            used_levels.append(lv)

        jumps = [b - a for a, b in zip(seq_complete[:-1],
                                       seq_complete[1:])]
        odd_jumps = sum(1 for j in jumps if j % 2 != 0)
        d1_odd_jumps += odd_jumps
        blind_jumps = [b - a for a, b in zip(seq_blind[:-1],
                                             seq_blind[1:])]
        apparent_decays = sum(1 for j in blind_jumps if j == 1)
        d3_apparent_decays += apparent_decays
        fails, skipped = signed_count_rule(ts, pts, used_levels,
                                           pilot.DT)
        d2_rule_failures += len(fails)
        refused_total += refused + skipped
        spread = (max(signed_seen) - min(signed_seen)
                  if signed_seen else 0)
        d2_signed_spread = max(d2_signed_spread, spread)
        total_hidden += hidden_here
        total_multibranch += multibranch_here

        row = {
            "fold_count": int(nf),
            "probe_folds": PROBE_FOLDS[idx],
            "fold_count_even": bool(nf % 2 == 0),
            "t_start": t0, "t_end": t1,
            "t_min": float(ts.min()), "t_max": float(ts.max()),
            "fold_times": fold_ts,
            "excursions": excursions,
            "levels_used": len(used_levels),
            "levels_refused": int(refused + skipped),
            "complete_counts": {str(v): seq_complete.count(v)
                                for v in sorted(set(seq_complete))},
            "complete_jumps": {str(v): jumps.count(v)
                               for v in sorted(set(jumps))},
            "odd_jumps": int(odd_jumps),
            "signed_counts_seen": sorted(signed_seen),
            "path_degree_failures": int(len(fails)),
            "blind_counts": {str(v): seq_blind.count(v)
                             for v in sorted(set(seq_blind))},
            "blind_jumps": {str(v): blind_jumps.count(v)
                            for v in sorted(set(blind_jumps))},
            "apparent_decay_events": int(apparent_decays),
            "hidden_crossings": int(hidden_here),
            "multibranch_levels": int(multibranch_here)}
        members[f"P{p}_E{e:.6f}_pu{pu0:g}"] = row
        print(f"A P={p} folds={nf} levels={len(used_levels)} "
              f"complete={row['complete_counts']} "
              f"blind={row['blind_counts']} "
              f"apparent_decays={apparent_decays} "
              f"odd_jumps={odd_jumps} hidden={hidden_here}",
              flush=True)
    record["arm_a_members"] = members
    return {
        "members_audited": members_audited,
        "d1_odd_jumps": d1_odd_jumps,
        "d1_parity_failures": d1_parity_failures,
        "d2_rule_failures": d2_rule_failures,
        "d2_signed_spread": d2_signed_spread,
        "d3_observations": d3_observations,
        "d3_mismatches": d3_mismatches,
        "d3_parity_flips": d3_parity_flips,
        "d3_apparent_decays": d3_apparent_decays,
        "d4_members_without_folds": d4_members_without_folds,
        "total_hidden_crossings": total_hidden,
        "total_multibranch_levels": total_multibranch,
        "levels_refused": refused_total}


def arm_b(record):
    t_exit = -pilot.T_START
    levels = [m * t_exit for m in LEVEL_MULTS]
    cells = {}
    parity_failures = 0
    rule_failures = 0
    refused = 0
    polylines_audited = 0
    exact_reversal_steps = []
    census_totals = {"nonfinite": 0, "reversing": 0,
                     "transmitted": 0, "capped": 0}
    worst_resid = 0.0
    missing_total = 0
    for i, (p, e) in enumerate(CELLS):
        res = census_run(p, e, N_CELL, SEEDS[i],
                         keep_polyline=tuple(range(K_POLY)))
        counts = res["counts"]
        for k in census_totals:
            census_totals[k] += counts[k]
        missing_total += res["missing"]
        worst_resid = max(worst_resid, res["max_energy_residual"])
        cell_rev_steps = []
        for k in range(K_POLY):
            pl = res["polylines"][str(k)]
            ts = np.asarray(pl["t"], dtype=float)
            pts = np.asarray(pl["pt"], dtype=float)
            polylines_audited += 1
            if len(ts) > 1 and np.isfinite(pts[-1]) and pts[-1] <= 0.0:
                cell_rev_steps.append(len(ts) - 1)
            t0, t1 = float(ts[0]), float(ts[-1])
            for lv in levels:
                try:
                    cr, _ = polyline_level_crossings(
                        np.arange(len(ts)) * pilot.DT, ts, pts,
                        float(lv))
                except ValueError:
                    refused += 1
                    continue
                expect = ((1 if t1 > lv else 0)
                          - (1 if t0 > lv else 0))
                if len(cr) % 2 != abs(expect) % 2:
                    parity_failures += 1
            f, sk = signed_count_rule(pl["t"], pl["pt"], levels,
                                      pilot.DT)
            rule_failures += len(f)
            refused += sk
        exact_reversal_steps.append(cell_rev_steps)
        cells[f"P{p}_E{e:.6f}"] = {
            "counts": counts,
            "missing": int(res["missing"]),
            "max_energy_residual": float(res["max_energy_residual"]),
            "kept_polylines": K_POLY,
            "kept_reversing": len(cell_rev_steps),
            "steps_run": int(res["steps_run"])}
        print(f"B P={p} {counts} resid="
              f"{res['max_energy_residual']:.2e} "
              f"kept_rev={len(cell_rev_steps)}", flush=True)
        del res
    record["arm_b_cells"] = cells
    return {
        "polylines_audited": polylines_audited,
        "parity_failures": parity_failures,
        "rule_failures": rule_failures,
        "levels_refused": refused,
        "census_totals": census_totals,
        "missing_trajectories": missing_total,
        "max_energy_residual": worst_resid,
        "exact_reversal_steps": exact_reversal_steps,
        "levels": levels}


def lifetimes(record, arm_b_summary):
    out = {}
    pooled_tau = []
    for i, (p, e) in enumerate(CELLS):
        nominal = abs(pilot.T_START) / (p * pilot.DT)
        caps = [int(round(f * nominal)) for f in F_LADDER]
        rows = []
        for cap in caps:
            res = census_run(p, e, N_CELL, SEEDS[i], max_steps=cap)
            rows.append({"max_steps": cap,
                         "reversed_by": int(res["counts"]["reversing"])})
            print(f"  ladder P={p} cap={cap} "
                  f"rev={res['counts']['reversing']}", flush=True)
        key = f"P{p}_E{e:.6f}"
        cell_total = record["arm_b_cells"][key]["counts"]["reversing"]
        taus = []
        prev_cap, prev_n = 0, 0
        for r in rows:
            k = r["reversed_by"] - prev_n
            mid = 0.5 * (prev_cap + r["max_steps"]) * pilot.DT
            taus += [mid] * k
            prev_cap, prev_n = r["max_steps"], r["reversed_by"]
        beyond = cell_total - prev_n
        arr = np.array(taus, dtype=float)
        pooled_tau += taus
        out[key] = {"nominal_arrival_steps": float(nominal),
                    "caps": caps,
                    "ladder": rows,
                    "cell_reversing_total": int(cell_total),
                    "captured_in_ladder": int(prev_n),
                    "beyond_ladder": int(beyond),
                    "bin_width_tau": float(
                        (caps[1] - caps[0]) * pilot.DT),
                    "stats": _lifetime_stats(arr)}
        print(f"  P={p} rev_total={cell_total} in_ladder={prev_n} "
              f"beyond={beyond} stats={out[key]['stats']}", flush=True)
    pooled = np.array(pooled_tau, dtype=float)
    exact = [s for cell in arm_b_summary["exact_reversal_steps"]
             for s in cell]
    exact_tau = np.array(exact, dtype=float) * pilot.DT
    record["pf8b_cells"] = out
    return {
        "pooled_n": int(pooled.size),
        "pooled_stats": _lifetime_stats(pooled),
        "exact_crosscheck_n": int(exact_tau.size),
        "exact_crosscheck_mean_tau": (float(exact_tau.mean())
                                      if exact_tau.size else None),
        "exact_crosscheck_sd_tau": (float(exact_tau.std(ddof=1))
                                    if exact_tau.size > 1 else None),
        "exact_crosscheck_cv": (
            float(exact_tau.std(ddof=1) / exact_tau.mean())
            if exact_tau.size > 1 and exact_tau.mean() > 0 else None)}


def _lifetime_stats(arr):
    if arr.size < 2:
        return {"n": int(arr.size)}
    mean = float(arr.mean())
    sd = float(arr.std(ddof=1))
    cv = sd / mean
    onset = float(arr.min())
    shifted = arr - onset
    mean_s = float(shifted.mean())
    cv_shifted = (float(shifted.std(ddof=1) / mean_s)
                  if mean_s > 0 else None)
    # exponential survival fits, MLE rate is the reciprocal mean
    sup_raw = _sup_dev(arr, 1.0 / mean, 0.0)
    sup_shift = (_sup_dev(arr, 1.0 / mean_s, onset)
                 if mean_s > 0 else None)
    return {"n": int(arr.size), "mean_tau": mean, "sd_tau": sd,
            "min_tau": onset, "max_tau": float(arr.max()),
            "coefficient_of_variation": cv,
            "cv_minus_one": cv - 1.0,
            "coefficient_of_variation_onset_shifted": cv_shifted,
            "exp_fit_sup_deviation": sup_raw,
            "exp_fit_sup_deviation_onset_shifted": sup_shift}


def _sup_dev(arr, rate, shift):
    """Sup deviation between the empirical survival curve of the
    sample and the exponential survival curve whose mean matches it."""
    xs = np.sort(arr)
    n = xs.size
    emp = 1.0 - np.arange(1, n + 1) / n
    fit = np.exp(-rate * (xs - shift))
    return float(np.max(np.abs(emp - fit)))


def main() -> int:
    record: dict = {"schema": "pf8-decay-gate-v1",
                    "label": "exploratory",
                    "gate": "PF-8"}
    a = arm_a(record)
    b = arm_b(record)
    lif = lifetimes(record, b)

    d1 = (a["d1_odd_jumps"] == 0 and a["d1_parity_failures"] == 0
          and b["parity_failures"] == 0
          and all(v["fold_count_even"]
                  for v in record["arm_a_members"].values()))
    d2 = (a["d2_rule_failures"] == 0 and b["rule_failures"] == 0
          and a["d2_signed_spread"] == 0)
    d3 = (a["d3_mismatches"] == 0 and a["d3_parity_flips"] > 0)
    d4 = (a["d4_members_without_folds"] == 0
          and a["total_hidden_crossings"] >= MIN_HIDDEN_CROSSINGS
          and a["total_multibranch_levels"] >= MIN_MULTIBRANCH_LEVELS
          and b["census_totals"]["reversing"] > 0)
    verdict = ("PASS" if (d1 and d2 and d3 and d4)
               else ("vacuous" if not d4 else "FAIL"))

    record["arm_a_summary"] = a
    record["arm_b_summary"] = {k: v for k, v in b.items()
                               if k != "exact_reversal_steps"}
    record["arm_b_summary"]["exact_reversal_steps_per_cell"] = [
        sorted(c) for c in b["exact_reversal_steps"]]
    record["pf8b_summary"] = lif
    record["bars"] = {
        "D1_complete_observer_parity": bool(d1),
        "D2_signed_count": bool(d2),
        "D3_blind_consumer": bool(d3),
        "D4_anti_vacuity": bool(d4)}
    record["measured"] = {
        "members_audited": a["members_audited"],
        "polylines_audited": b["polylines_audited"],
        "odd_events": a["d1_odd_jumps"],
        "parity_failures_deterministic": a["d1_parity_failures"],
        "parity_failures_thermal": b["parity_failures"],
        "signed_count_failures_deterministic": a["d2_rule_failures"],
        "signed_count_failures_thermal": b["rule_failures"],
        "signed_count_spread": a["d2_signed_spread"],
        "blind_observations": a["d3_observations"],
        "blind_detector_mismatches": a["d3_mismatches"],
        "blind_parity_flips": a["d3_parity_flips"],
        "blind_parity_flip_fraction": (
            a["d3_parity_flips"] / a["d3_observations"]
            if a["d3_observations"] else None),
        "apparent_decay_events": a["d3_apparent_decays"],
        "hidden_crossings": a["total_hidden_crossings"],
        "multibranch_levels": a["total_multibranch_levels"],
        "thermal_reversing_total": b["census_totals"]["reversing"],
        "thermal_missing_trajectories": b["missing_trajectories"],
        "thermal_max_energy_residual": b["max_energy_residual"]}
    record["verdict"] = {"value": verdict,
                         "computed_from": ["D1", "D2", "D3", "D4"],
                         "pf8b": "measurement, no bar"}
    record["declared"] = {
        "members": MEMBERS, "probe_folds": PROBE_FOLDS,
        "n_steps": N_STEPS,
        "level_fractions": LEVEL_FRACTIONS,
        "excursion_fractions": EXCURSION_FRACTIONS,
        "blind_window_u": [U_BLIND_LO, U_BLIND_HI],
        "blind_window_source": "results/pf8-blind-probe.json, record "
                               "sha 6dce4c52a31e43cb",
        "cells": CELLS, "n_cell": N_CELL, "seeds": SEEDS,
        "k_poly": K_POLY, "level_mults": LEVEL_MULTS,
        "f_ladder": F_LADDER,
        "min_hidden_crossings": MIN_HIDDEN_CROSSINGS,
        "min_multibranch_levels": MIN_MULTIBRANCH_LEVELS,
        "truncation_note": "the frozen census stops a member at its "
                           "first reversal, so a reversing member's "
                           "kept polyline is half a worldline and "
                           "carries the endpoint form of the parity "
                           "bar, not the even-fold-count form"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf8-decay-gate.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("bars", record["bars"])
    print("measured", record["measured"])
    print("pf8b", record["pf8b_summary"])
    print("VERDICT", verdict)
    print("record_sha256", record["record_sha256"])
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
