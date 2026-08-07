#!/usr/bin/env python3
"""PF-8 blind-window and lifetime-ladder probe (exploratory, unsealed).

The standing rule after PF5-001 and PF6-001 is that every registration
must cite a probe verifying event presence per bound cell and member,
and must fix its declared numbers from a committed probe record. PF-8
needs three numbers it cannot invent. The first is the level window in
which each bound deterministic member is observed in the pair-creation
configuration, both worldline endpoints on the same side of the level,
so the complete observer's unsigned branch count is even and the signed
count is zero. The second is the distribution of the transverse
coordinate u at the branch crossings, from which the blind consumer's
window is declared. The third is the step range in which thermal
members reverse, from which the PF-8b survival ladder is declared.

This probe measures all three and records them. It declares nothing
and binds nothing.

Arm A. The four PF6-002 probe-verified members, integrated with the
frozen PF-6 instrument at the sealed step budget. Recorded per member,
the fold count, the worldline endpoints, the extreme observed times,
the candidate level windows and their widths, the declared level
ladder inside the chosen window, and for every level the unsigned
crossing count together with the sorted u coordinate of each crossing.
Pooled quantiles of every crossing u follow.

Arm B. One PF5-002 cell, coarse ladder in the step cap, giving the
cumulative count of thermal members that have reversed by each cap.
The reversal step range read off this ladder fixes the fine ladder of
the governed run.

Exploratory label. No claim.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pf4_pilot as pilot  # noqa: E402
from pf5_accounting import census_run  # noqa: E402
from pf6_covariance import fold_count, integrate  # noqa: E402
from projection_fold import (  # noqa: E402
    canonical_sha256,
    polyline_level_crossings,
)

# (gap, field, pu0) bound by PREREG-PF6-002 from the member probe
MEMBERS = [(0.60, 0.8957885742187499, 3.0),
           (0.70, 1.0448364257812501, 3.0),
           (0.80, 1.2020141601562502, 3.0),
           (0.90, 1.3605468750000003, 2.0)]
N_STEPS = 40_000
LEVEL_FRACTIONS = [0.05 * k for k in range(1, 20)]

# arm B, one PF5-002 cell
LADDER_CELL = (0.60, 0.8957885742187499)
LADDER_N = 1_000
LADDER_SEED = 8_800_000
LADDER_CAPS = [4_000, 8_000, 12_000, 16_000, 18_000, 20_000, 22_000,
               24_000, 28_000, 32_000, 36_000, 60_000]


def crossing_u(ts, pts, us, level, dt):
    """Crossings of one observed level, with the transverse coordinate
    of each crossing. The crossing list is the frozen instrument's.
    Only the u lookup is added here, by linear interpolation at the
    returned evolution parameter."""
    taus = np.arange(len(ts)) * dt
    crossings, _ = polyline_level_crossings(taus, ts, pts, float(level))
    out = []
    for c in crossings:
        idx = c["tau"] / dt
        k = int(np.floor(idx))
        k = max(0, min(k, len(us) - 2))
        frac = idx - k
        out.append({"tau": float(c["tau"]),
                    "orientation": float(c["orientation"]),
                    "u": float(us[k] + frac * (us[k + 1] - us[k]))})
    return out


def main() -> int:
    record: dict = {"schema": "pf8-blind-probe-v1",
                    "label": "exploratory"}
    rows = []
    pooled_u = []
    for p, e, pu0 in MEMBERS:
        ts, pts, us, pus = integrate(p, e, n_steps=N_STEPS, pu0=pu0)
        t0, t1 = float(ts[0]), float(ts[-1])
        lo, hi = min(t0, t1), max(t0, t1)
        t_min, t_max = float(ts.min()), float(ts.max())
        upper_width = t_max - hi
        lower_width = lo - t_min
        if upper_width >= lower_width:
            window = (hi, t_max)
            side = "upper"
            width = upper_width
        else:
            window = (t_min, lo)
            side = "lower"
            width = lower_width
        levels = [window[0] + f * (window[1] - window[0])
                  for f in LEVEL_FRACTIONS]
        fold_idx = np.nonzero(pts[:-1] * pts[1:] < 0.0)[0]
        per_level = []
        refused = 0
        for lv in levels:
            try:
                cr = crossing_u(ts, pts, us, lv, pilot.DT)
            except ValueError:
                refused += 1
                per_level.append({"level": float(lv),
                                  "refused": True})
                continue
            uvals = sorted(round(c["u"], 6) for c in cr)
            signed = int(sum(c["orientation"] for c in cr))
            pooled_u.extend(uvals)
            per_level.append({"level": float(lv),
                              "count": len(cr),
                              "signed": signed,
                              "u_sorted": uvals})
        row = {"P": p, "E": e, "pu0": pu0,
               "fold_count": int(fold_count(pts)),
               "t_start": t0, "t_end": t1,
               "t_min": t_min, "t_max": t_max,
               "upper_window_width": float(upper_width),
               "lower_window_width": float(lower_width),
               "window_side": side,
               "window": [float(window[0]), float(window[1])],
               "window_width": float(width),
               "fold_times": [float(ts[k]) for k in fold_idx],
               "refused_levels": refused,
               "levels": per_level}
        rows.append(row)
        print(f"P={p} folds={row['fold_count']} t0={t0:.4f} "
              f"t1={t1:.4f} tmax={t_max:.4f} side={side} "
              f"width={width:.4f} refused={refused}", flush=True)
        print("   counts", [d.get("count") for d in per_level],
              flush=True)

    arr = np.array(pooled_u, dtype=float) if pooled_u else np.array([0.0])
    quant = {f"q{int(100 * q):02d}": float(np.quantile(arr, q))
             for q in [0.0, 0.05, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6,
                       0.7, 0.75, 0.8, 0.9, 0.95, 1.0]}
    record["arm_a_members"] = rows
    record["arm_a_pooled_u"] = {
        "n_crossings": int(arr.size),
        "min": float(arr.min()), "max": float(arr.max()),
        "mean": float(arr.mean()), "quantiles": quant}
    print("pooled u quantiles", quant, flush=True)

    ladder = []
    p, e = LADDER_CELL
    for cap in LADDER_CAPS:
        res = census_run(p, e, LADDER_N, LADDER_SEED, max_steps=cap)
        ladder.append({"max_steps": cap,
                       "counts": res["counts"],
                       "steps_run": res["steps_run"]})
        print("ladder", cap, res["counts"], flush=True)
    record["arm_b_ladder"] = {
        "cell": [p, e], "n": LADDER_N, "seed": LADDER_SEED,
        "caps": LADDER_CAPS, "rows": ladder}

    record["declared"] = {
        "members": MEMBERS, "n_steps": N_STEPS,
        "level_fractions": LEVEL_FRACTIONS,
        "window_rule": "levels sit inside the wider of the two "
                       "windows in which both worldline endpoints lie "
                       "on the same side of the level, upper "
                       "(max(t_start,t_end), t_max) or lower "
                       "(t_min, min(t_start,t_end))",
        "purpose": "fix the PF-8 level ladder, the blind window, and "
                   "the PF-8b survival ladder from measured numbers "
                   "before the governed run"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf8-blind-probe.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
