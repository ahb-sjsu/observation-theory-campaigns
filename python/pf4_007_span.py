#!/usr/bin/env python3
"""PF4-007 span convergence of the transfer (exploratory).

Protocol declared in CAMPAIGN.md before this run. The PF4-006 gate
failed its entry-point clause. Moving the entry from twenty widths
to thirty changed the transfer by 1.289, 1.295, and 1.291 percent
at the three widths, a change that is large against the declared
bar and almost identical across widths. The timestep clause missed
its bar too, by 3e-7 against 1e-8, which is a bar set tighter than
the declared timestep can deliver rather than a defect.

The diagnosis to test. The arctangent tilt approaches its
asymptote algebraically rather than exponentially, so its field
never fully turns off and the transfer measured from a finite entry
point carries a tail contribution. If that is right, the
contribution falls as a power of the span, the sech-squared profile
whose tilt approaches exponentially does not show it, and because
the contribution is nearly common across widths it should move the
fitted intercept far more than the fitted exponent.

That last point is what the seal turns on. A claim about an
exponent survives a common multiplicative offset. A claim about the
transfer itself does not.

Exploratory label. Not claim-bearing.
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
from pf4_005_analyticity import (  # noqa: E402
    POLE_DISTANCE, run_cell)
from projection_fold import canonical_sha256  # noqa: E402

SPAN_LADDER = [20.0, 30.0, 45.0, 65.0, 90.0]
L_PROBE = 3.0
KAPPA_PROBE = 1.5
KAPPA_GRID = [0.9, 1.2, 1.5, 2.0, 2.5, 3.0]
L_GRID = [2.0, 3.0, 4.0]
DT = 2e-4
EXPONENT_SPANS = [20.0, 90.0]


def fit_slope(kappa_values, e_res):
    """Fit the log transfer against the adiabaticity itself. The
    first execution of this runner imported a helper that fits
    against the reciprocal, which is the named error that
    invalidated its exponent items."""
    x = np.array(kappa_values, dtype=float)
    y = np.log(np.asarray(e_res, dtype=float))
    a = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(a, y, rcond=None)
    pred = a @ coef
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(coef[0]), float(coef[1]), r2


def transfer(profile, l_s, kappa, span, dt=DT):
    import pf4_005_analyticity as mod
    saved = mod.SPAN
    mod.SPAN = span
    try:
        a = POLE_DISTANCE[profile] * l_s
        p_value = pilot.OMEGA_U * a / kappa
        e_res, _ = run_cell(profile, l_s, [p_value], dt)
        return float(e_res[0])
    finally:
        mod.SPAN = saved


def exponent_at_span(profile, l_s, span):
    import pf4_005_analyticity as mod
    saved = mod.SPAN
    mod.SPAN = span
    try:
        a = POLE_DISTANCE[profile] * l_s
        p_values = [pilot.OMEGA_U * a / k for k in KAPPA_GRID]
        e_res, _ = run_cell(profile, l_s, p_values, DT)
        slope, icept, r2 = fit_slope(KAPPA_GRID, e_res)
        return slope, icept, r2
    finally:
        mod.SPAN = saved


def main() -> int:
    record: dict = {"schema": "pf4-007-span-v1",
                    "label": "exploratory"}
    items = {}

    # S1 the convergence ladder, both profiles
    ladders = {}
    for profile in ("lorentz", "sech2"):
        vals = []
        for span in SPAN_LADDER:
            v = transfer(profile, L_PROBE, KAPPA_PROBE, span)
            vals.append(v)
            print(f"  {profile} span={span} E_res={v:.12e}",
                  flush=True)
        rel = [abs(vals[i + 1] - vals[i]) / abs(vals[i + 1])
               for i in range(len(vals) - 1)]
        ladders[profile] = {"values": vals,
                            "successive_relative_change": rel}
    lor_rel = ladders["lorentz"]["successive_relative_change"]
    sec_rel = ladders["sech2"]["successive_relative_change"]
    items["S1_lorentz_converges"] = all(
        lor_rel[i + 1] < lor_rel[i] for i in range(len(lor_rel) - 1))
    items["S2_sech2_already_converged"] = max(sec_rel) <= 1e-9

    # S3 the exponent's robustness, which is what a seal needs
    exponents = {}
    worst_exp_change = 0.0
    for profile in ("lorentz", "sech2"):
        for l_s in L_GRID:
            row = {}
            for span in EXPONENT_SPANS:
                slope, icept, r2 = exponent_at_span(profile, l_s,
                                                    span)
                row[str(span)] = {"slope": slope,
                                  "intercept": icept,
                                  "r_squared": r2}
            a1 = row[str(EXPONENT_SPANS[0])]["slope"]
            a2 = row[str(EXPONENT_SPANS[-1])]["slope"]
            change = abs(a2 - a1) / abs(a1)
            row["relative_slope_change"] = float(change)
            i1 = row[str(EXPONENT_SPANS[0])]["intercept"]
            i2 = row[str(EXPONENT_SPANS[-1])]["intercept"]
            row["intercept_change"] = float(abs(i2 - i1))
            exponents[f"{profile}_L{l_s}"] = row
            worst_exp_change = max(worst_exp_change, change)
            print(f"  {profile} L={l_s} slope {a1:.6f} -> "
                  f"{a2:.6f}  rel {change:.3e}", flush=True)
    items["S3_exponent_robust_to_span"] = worst_exp_change <= 0.01

    lor_far = [exponents[f"lorentz_L{l}"][str(EXPONENT_SPANS[-1])]
               ["slope"] for l in L_GRID]
    lor_spread = float((max(lor_far) - min(lor_far))
                       / abs(np.mean(lor_far)))
    items["S4_universality_survives"] = lor_spread <= 0.02

    record["measured"] = {
        "span_ladder": SPAN_LADDER,
        "probe_cell": {"L": L_PROBE, "kappa": KAPPA_PROBE},
        "ladders": ladders,
        "exponents_by_span": exponents,
        "worst_relative_exponent_change": float(worst_exp_change),
        "lorentz_slopes_at_far_span": lor_far,
        "lorentz_spread_at_far_span": lor_spread,
        "reading": "the transfer of a profile with algebraic tails "
                   "carries a tail contribution from any finite "
                   "entry point, and the question a seal turns on "
                   "is whether that contribution is common enough "
                   "across the grid to leave the exponent alone"}
    record["items"] = {k: bool(v) for k, v in items.items()}
    verdict = "PASS" if all(items.values()) else "FAIL"
    record["verdict"] = {"value": verdict,
                         "computed_from": sorted(items)}
    record["declared"] = {
        "span_ladder": SPAN_LADDER, "kappa_grid": KAPPA_GRID,
        "L_grid": L_GRID, "dt": DT,
        "exponent_spans": EXPONENT_SPANS,
        "bars": {"S3_exponent_change": 0.01,
                 "S4_universality_spread": 0.02,
                 "S2_sech2_convergence": 1e-9},
        "purpose": "decide the span and the bars a preregistration "
                   "on this profile must declare"}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "pf4-007-span.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("lorentz successive changes", lor_rel)
    print("sech2 successive changes", sec_rel)
    print("worst exponent change", worst_exp_change,
          "lorentz spread at far span", lor_spread)
    print("items", items)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
