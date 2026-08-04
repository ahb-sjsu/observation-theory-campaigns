#!/usr/bin/env python3
"""Governed run of PREREG-PF4-003: the frozen-measure pulse-train family.

The family. A thermal-free event (u at the shifted equilibrium, pu = 0,
no ensemble, no measure) crosses an alternating train of Sauter slabs,
tilt(t) = g E L sum_k (-1)^k tanh((t - kD)/L), whose force profile
retains the single slab's sech^2 analyticity. Each crossing deposits
the action-suppressed residual measured by hunt probe one; deposits
accumulate and the event reverses when the gap is spent. The
observable is N_rev(P), the slab count at reversal, and the sealed
claim is that log N_rev is organized by the action model a + b/P and
not by a power law, on held-out velocities.

The C5 plant (mandatory here). The square-wave variant replaces tanh
by sign, the sudden limit with no analyticity suppression, so its
transfer per slab is velocity-independent at leading order and its
N_rev must be organized by the power law. The pipeline must find the
plant power-law-organized and the two prescriptions in disagreement,
or the run is void.

Vectorized RK4 across the velocity grid, per-trajectory freezing on
reversal. Every constant is from the sealed document.
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
from pf4_pilot import G, LAM, OMEGA_U, shifted_equilibrium  # noqa: E402

E_FIELD = 0.6
L_SLAB = 3.0
D_SPACING = 18.0
DT = 2e-3
N_CAP = 4000
TRAIN_P = [1.2, 1.5, 1.8, 2.1]
HELD_P = [1.35, 1.65, 1.95]
RATIO_BAR = 4.0
PLANT_DISAGREE_BAR = 0.5
MIN_HELD_USABLE = 3


def tilt_and_force(t: np.ndarray, smooth: bool):
    """Alternating-slab tilt s(t) and force profile f(t) = s'(t)*L."""
    s = np.zeros_like(t)
    f = np.zeros_like(t)
    k0 = np.floor(t / D_SPACING).astype(int)
    for dk in range(-4, 5):
        k = k0 + dk
        sign = np.where(k % 2 == 0, 1.0, -1.0)
        valid = k >= 0
        arg = (t - k * D_SPACING) / L_SLAB
        if smooth:
            s += np.where(valid, sign * np.tanh(arg), 0.0)
            f += np.where(valid, sign / np.cosh(np.clip(arg, -30, 30))**2,
                          0.0)
        else:
            s += np.where(valid, sign * np.sign(arg), 0.0)
    lo = k0 - 5
    n_lo = np.maximum(lo + 1, 0)
    tail_lo = np.where(n_lo % 2 == 1, 1.0, 0.0)
    s += tail_lo
    return s, f


def run_family(p_values, smooth: bool):
    p = np.array(p_values, dtype=float)
    n = p.size
    u0 = shifted_equilibrium(E_FIELD, -4.0 * L_SLAB)
    t = np.full(n, -4.0 * L_SLAB)
    pt = p.copy()
    u = np.full(n, u0)
    pu = np.zeros(n)
    alive = np.ones(n, dtype=bool)
    n_rev = np.full(n, -1.0)

    def rhs(t, pt, u, pu):
        s, f = tilt_and_force(t, smooth)
        return (pt,
                -G * E_FIELD * u * f,
                pu,
                -OMEGA_U**2 * u - LAM * u**3 - G * E_FIELD * L_SLAB * s)

    tau_max = (N_CAP * D_SPACING) / max(min(p_values), 0.1)
    steps = int(round(tau_max / DT))
    for _ in range(steps):
        if not alive.any():
            break
        d1 = rhs(t, pt, u, pu)
        d2 = rhs(t + 0.5 * DT * d1[0], pt + 0.5 * DT * d1[1],
                 u + 0.5 * DT * d1[2], pu + 0.5 * DT * d1[3])
        d3 = rhs(t + 0.5 * DT * d2[0], pt + 0.5 * DT * d2[1],
                 u + 0.5 * DT * d2[2], pu + 0.5 * DT * d2[3])
        d4 = rhs(t + DT * d3[0], pt + DT * d3[1],
                 u + DT * d3[2], pu + DT * d3[3])
        m = alive
        t = np.where(m, t + DT / 6 * (d1[0] + 2 * d2[0] + 2 * d3[0]
                                      + d4[0]), t)
        pt_new = np.where(m, pt + DT / 6 * (d1[1] + 2 * d2[1] + 2 * d3[1]
                                            + d4[1]), pt)
        u = np.where(m, u + DT / 6 * (d1[2] + 2 * d2[2] + 2 * d3[2]
                                      + d4[2]), u)
        pu = np.where(m, pu + DT / 6 * (d1[3] + 2 * d2[3] + 2 * d3[3]
                                        + d4[3]), pu)
        reversed_now = m & (pt_new <= 0.0)
        if reversed_now.any():
            n_rev[reversed_now] = np.maximum(
                t[reversed_now] / D_SPACING, 0.5)
            alive &= ~reversed_now
        pt = pt_new
        if (t[alive] > N_CAP * D_SPACING).any():
            capped = alive & (t > N_CAP * D_SPACING)
            alive &= ~capped
    return [{"P": float(pv), "N_rev": float(nr),
             "reversed": bool(nr > 0)}
            for pv, nr in zip(p, n_rev, strict=True)]


def fit_models(rows_train, rows_held):
    def usable(rows):
        return [r for r in rows if r["reversed"]]
    tr, he = usable(rows_train), usable(rows_held)
    if len(he) < MIN_HELD_USABLE or len(tr) < 3:
        return None
    x_tr = np.array([1.0 / r["P"] for r in tr])
    lx_tr = np.array([math.log(r["P"]) for r in tr])
    y_tr = np.array([math.log(r["N_rev"]) for r in tr])
    x_he = np.array([1.0 / r["P"] for r in he])
    lx_he = np.array([math.log(r["P"]) for r in he])
    y_he = np.array([math.log(r["N_rev"]) for r in he])

    b_exp = np.polyfit(x_tr, y_tr, 1)
    b_pow = np.polyfit(lx_tr, y_tr, 1)
    mse_exp = float(np.mean((y_he - np.polyval(b_exp, x_he)) ** 2))
    mse_pow = float(np.mean((y_he - np.polyval(b_pow, lx_he)) ** 2))
    return {"action_slope_b": float(b_exp[0]),
            "power_exponent_c": float(b_pow[0]),
            "held_mse_action": mse_exp, "held_mse_power": mse_pow,
            "ratio_power_over_action": mse_pow / max(mse_exp, 1e-300),
            "n_train_usable": len(tr), "n_held_usable": len(he)}


def main() -> int:
    smooth_train = run_family(TRAIN_P, True)
    smooth_held = run_family(HELD_P, True)
    plant_train = run_family(TRAIN_P, False)
    plant_held = run_family(HELD_P, False)
    for tag, rows in (("smooth-train", smooth_train),
                      ("smooth-held", smooth_held),
                      ("plant-train", plant_train),
                      ("plant-held", plant_held)):
        print(tag, [(r["P"], round(r["N_rev"], 1)) for r in rows])

    fits_smooth = fit_models(smooth_train, smooth_held)
    fits_plant = fit_models(plant_train, plant_held)

    if fits_smooth is None:
        label, outcome = "unevaluable", \
            "manifest-design failure: insufficient usable cells (smooth)"
    else:
        plant_ok = False
        disagree = 0.0
        if fits_plant is not None:
            plant_ok = (fits_plant["ratio_power_over_action"] <= 1.0)
            pairs = [(s, q) for s, q in
                     zip(smooth_train + smooth_held,
                         plant_train + plant_held, strict=True)
                     if s["reversed"] and q["reversed"]]
            if pairs:
                disagree = max(abs(math.log(s["N_rev"])
                                   - math.log(q["N_rev"]))
                               for s, q in pairs)
        c5_pass = plant_ok and disagree > PLANT_DISAGREE_BAR
        if not c5_pass:
            label, outcome = "void", \
                "C5 plant not flagged: pipeline void, no claim readable"
        elif fits_smooth["ratio_power_over_action"] >= RATIO_BAR:
            label = "demonstrated-in-model"
            outcome = ("claim PASSES: the frozen-measure family's slab "
                       "count is organized by the action model and the "
                       "power law fails to compete")
        elif fits_smooth["ratio_power_over_action"] <= 1.0:
            label, outcome = "refuted", \
                "claim REFUTED: the power law fits held-out as well or "\
                "better on the smooth family"
        else:
            label, outcome = "neither-model", \
                "neither bar met: reported with both residual sets"

    record = {
        "schema": "prereg-pf4-003-run-v1",
        "registration_id": "PREREG-PF4-003",
        "label": label, "outcome": outcome,
        "declared": {"E": E_FIELD, "L": L_SLAB, "D": D_SPACING,
                     "dt": DT, "n_cap": N_CAP,
                     "train_P": TRAIN_P, "held_P": HELD_P,
                     "ratio_bar": RATIO_BAR,
                     "plant_disagree_bar": PLANT_DISAGREE_BAR,
                     "action_band_secondary": [
                         math.pi * OMEGA_U * L_SLAB / 2,
                         math.pi * OMEGA_U * L_SLAB]},
        "smooth": {"train": smooth_train, "held": smooth_held,
                   "fits": fits_smooth},
        "plant": {"train": plant_train, "held": plant_held,
                  "fits": fits_plant},
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
        / "prereg-pf4-003.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")
    if fits_smooth:
        print(f"smooth: b {fits_smooth['action_slope_b']:.2f} "
              f"(secondary band [{math.pi*OMEGA_U*L_SLAB/2:.2f}, "
              f"{math.pi*OMEGA_U*L_SLAB:.2f}]), power/action ratio "
              f"{fits_smooth['ratio_power_over_action']:.2f}")
    if fits_plant:
        print(f"plant: power/action ratio "
              f"{fits_plant['ratio_power_over_action']:.2f}")
    print(outcome)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
