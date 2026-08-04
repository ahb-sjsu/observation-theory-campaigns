#!/usr/bin/env python3
"""Non-measure-tail hunt, probe zero (exploratory, PF track).

The Schwinger exponent is an action, not an initial-measure tail. The
classical carrier of action-type exponentials is adiabatic-invariant
violation, where the energy transferred to an oscillator by a slow
smooth passage is exponentially small in the ratio of the passage's
analyticity width to the crossing speed. The Sauter slab already has
the required structure, since sech^2(t/L) has Fourier tails falling
like exp(-pi omega L / (2 v)) at oscillator frequency omega and
crossing speed v.

This probe measures the thermal-free deterministic kick to p_t across
the slab as a function of the incoming velocity P at fixed large L, in
the adiabatic corner where the crossing is slow against the oscillator
period. If log |kick| is linear in 1/P with a slope near
-pi omega_u L / 2, the family possesses a dynamics-set exponential
whose argument carries ONE power of the velocity scale, structurally
distinct from the measure tail (d/E)^2 the sealed runs established
for the anti-adiabatic corner, and the hunt has its candidate
mechanism. The fit window and the comparison slope are reported, not
sealed; this is a probe, and a preregistered family would come later.

Exploratory label.
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

from projection_fold import canonical_sha256  # noqa: E402
import pf4_pilot as fam  # noqa: e402

L_ADIABATIC = 6.0
E_FIELD = 0.4
P_GRID = [0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0]
DT = 5e-4


def probe_kick(p_gap: float) -> float:
    """Deterministic net kick |p_t(final) - P| across the slab."""
    fam.SAUTER_L = L_ADIABATIC
    fam.T_START = -4.0 * L_ADIABATIC
    out = fam.deterministic_probe(p_gap, E_FIELD, dt=DT)
    return out


def main() -> int:
    original_l, original_t = fam.SAUTER_L, fam.T_START
    fam.SAUTER_L = L_ADIABATIC
    fam.T_START = -4.0 * L_ADIABATIC
    old_tau = fam.TAU_MAX

    rows = []
    for p_gap in P_GRID:
        fam.TAU_MAX = (8.0 * L_ADIABATIC) / p_gap + 10.0
        out = fam.deterministic_probe(p_gap, E_FIELD, dt=DT)
        kick = p_gap - out["pt_min"]
        rows.append({"P": p_gap, "pt_min": out["pt_min"],
                     "kick": kick, "log_kick": math.log(max(kick, 1e-300))})
        print(f"P={p_gap}: pt_min {out['pt_min']:.6f}, kick {kick:.3e}")
    fam.SAUTER_L, fam.T_START, fam.TAU_MAX = original_l, original_t, old_tau

    inv_p = np.array([1.0 / r["P"] for r in rows])
    log_k = np.array([r["log_kick"] for r in rows])
    slope, intercept = np.polyfit(inv_p, log_k, 1)
    predicted_slope = -math.pi * fam.OMEGA_U * L_ADIABATIC / 2.0
    residuals = log_k - (slope * inv_p + intercept)
    r2 = 1.0 - float(np.sum(residuals**2)) \
        / max(float(np.sum((log_k - log_k.mean())**2)), 1e-300)

    record = {
        "schema": "pf4-hunt-probe-v1",
        "label": "exploratory",
        "declared": {"L": L_ADIABATIC, "E": E_FIELD, "P_grid": P_GRID,
                     "dt": DT, "omega_u": fam.OMEGA_U},
        "rows": rows,
        "fit": {"slope_vs_invP": float(slope),
                "intercept": float(intercept),
                "r_squared": r2,
                "analyticity_prediction": predicted_slope,
                "slope_ratio_measured_over_predicted":
                    float(slope / predicted_slope)},
        "statement": "if the deterministic kick is exponential in 1/P "
            "with the analyticity slope, the family has a dynamics-set "
            "action-type exponential in the adiabatic corner, the hunt's "
            "candidate mechanism for a non-measure-tail exponent",
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "pf4-hunt-probe.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"log|kick| vs 1/P: slope {slope:.3f} (analyticity prediction "
          f"{predicted_slope:.3f}, ratio {slope / predicted_slope:.3f}), "
          f"R^2 {r2:.4f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
