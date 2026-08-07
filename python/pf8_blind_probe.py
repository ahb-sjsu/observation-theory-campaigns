#!/usr/bin/env python3
"""PF-8 blind-window and lifetime-ladder probe (exploratory, unsealed).

The standing rule after PF5-001 and PF6-001 is that every registration
must cite a probe verifying event presence per bound cell and member,
and must fix its declared numbers from a committed probe record. PF-8
needs three numbers it cannot invent. The first is the level ladder on
which each bound deterministic member is observed, fine enough to
resolve the branch-count change across each fold. The second is the
distribution of the transverse coordinate u at the branch crossings,
from which the blind consumer's window is declared. The third is the
step range in which thermal members reverse, from which the PF-8b
survival ladder is declared.

This probe measures all three and records them. It declares nothing
and binds nothing.

A first pass of this probe, run at commit aff9b49, placed the levels
in the window where both worldline endpoints lie on the same side of
the level, which is the pair-creation configuration with even branch
count and zero signed count. It measured that window empty. Every one
of the four bound members ends at its own largest observed time,
t_end equal to t_max, and starts at its own smallest, so both
candidate windows have width exactly zero and all nineteen levels
were refused. The bound members are through-going, one branch in and
one branch out, which is the configuration a decay question wants
anyway. The level rule below is the corrected one, a uniform ladder
across the full observed span from t_start to t_end, and the parity
statement it supports is that the unsigned branch count changes by an
even amount across every fold, so a through-going worldline shows an
odd count at every level and can never read one becoming two.

Arm A. The four PF6-002 probe-verified members, integrated with the
frozen PF-6 instrument at the sealed step budget. Recorded per member,
the fold count, the worldline endpoints, the extreme observed times,
the fold times, the level ladder, and for every level the unsigned
crossing count, the signed count, and the sorted u coordinate of each
crossing. Pooled quantiles of every crossing u follow.

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
import time
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
LEVEL_FRACTIONS = [k / 100.0 for k in range(1, 100)]
EXCURSION_FRACTIONS = [0.1 * k for k in range(1, 10)]
COST_N = 5_000
COST_STEPS = 24_000

# arm B, one PF5-002 cell
LADDER_CELL = (0.60, 0.8957885742187499)
LADDER_N = 1_000
LADDER_SEED = 8_800_000
LADDER_CAPS = [16_000, 18_000, 20_000, 22_000, 24_000, 26_000,
               28_000, 32_000, 60_000]


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
    multi_u = []
    for p, e, pu0 in MEMBERS:
        ts, pts, us, pus = integrate(p, e, n_steps=N_STEPS, pu0=pu0)
        t0, t1 = float(ts[0]), float(ts[-1])
        lo, hi = min(t0, t1), max(t0, t1)
        t_min, t_max = float(ts.min()), float(ts.max())
        upper_width = t_max - hi
        lower_width = lo - t_min
        fold_idx = np.nonzero(pts[:-1] * pts[1:] < 0.0)[0]
        fold_ts = [float(ts[k]) for k in fold_idx]
        background = [t0 + f * (t1 - t0) for f in LEVEL_FRACTIONS]
        excursions = []
        exc_levels = []
        for j in range(0, len(fold_ts) - 1, 2):
            a, b = fold_ts[j], fold_ts[j + 1]
            elo, ehi = min(a, b), max(a, b)
            excursions.append({"fold_pair": [a, b],
                               "lo": elo, "hi": ehi,
                               "width": ehi - elo})
            exc_levels += [elo + f * (ehi - elo)
                           for f in EXCURSION_FRACTIONS]
        levels = sorted(background + exc_levels)
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
            if len(cr) > 1:
                multi_u.append({"P": p, "level": float(lv),
                                "count": len(cr), "u_sorted": uvals})
        counts_seq = [d.get("count") for d in per_level]
        jumps = [b - a for a, b in zip(counts_seq[:-1], counts_seq[1:])
                 if a is not None and b is not None]
        row = {"P": p, "E": e, "pu0": pu0,
               "fold_count": int(fold_count(pts)),
               "t_start": t0, "t_end": t1,
               "t_min": t_min, "t_max": t_max,
               "pair_window_upper_width": float(upper_width),
               "pair_window_lower_width": float(lower_width),
               "background_spacing": float(abs(t1 - t0)
                                          * (LEVEL_FRACTIONS[1]
                                             - LEVEL_FRACTIONS[0])),
               "fold_times": fold_ts,
               "excursions": excursions,
               "n_levels": len(levels),
               "refused_levels": refused,
               "count_sequence": counts_seq,
               "jumps": jumps,
               "odd_jumps": int(sum(1 for j in jumps if j % 2 != 0)),
               "levels": per_level}
        rows.append(row)
        print(f"P={p} folds={row['fold_count']} t0={t0:.4f} "
              f"t1={t1:.4f} nlev={len(levels)} "
              f"refused={refused} odd_jumps={row['odd_jumps']}",
              flush=True)
        print("   excursions", excursions, flush=True)
        print("   count histogram",
              {c: counts_seq.count(c) for c in set(counts_seq)},
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
    record["arm_a_multibranch_levels"] = multi_u
    print("pooled u quantiles", quant, flush=True)
    print("multibranch levels", len(multi_u), flush=True)
    for m in multi_u:
        print("   ", m, flush=True)

    t_cost = time.time()
    cost = census_run(*LADDER_CELL, COST_N, LADDER_SEED,
                      max_steps=COST_STEPS)
    t_cost = time.time() - t_cost
    record["arm_b_cost"] = {
        "n": COST_N, "max_steps": COST_STEPS,
        "wall_seconds": float(t_cost),
        "seconds_per_step": float(t_cost / cost["steps_run"]),
        "counts": cost["counts"]}
    print("cost", record["arm_b_cost"], flush=True)

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
        "excursion_fractions": EXCURSION_FRACTIONS,
        "window_rule": "the ladder is a uniform background at "
                       "t_start + f (t_end - t_start) for the declared "
                       "fractions f, merged with levels placed at the "
                       "declared excursion fractions inside each "
                       "interval spanned by a consecutive pair of "
                       "fold times, because the fold excursions are "
                       "far narrower than the background spacing",
        "first_pass_note": "the aff9b49 pass placed levels in the "
                           "pair-creation window and measured it "
                           "empty, t_end equals t_max and t_start "
                           "equals t_min on every bound member, so "
                           "both candidate windows had width zero",
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
