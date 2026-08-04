#!/usr/bin/env python3
"""PE-2 reversible fold cycle pilot.

Part A. One toy-Hamiltonian trajectory observed through constant-time
levels: unsigned multiplicity is a staircase whose breakpoints are exactly
the fold values of t (steps of 2) and the two endpoint values (steps of 1),
while the signed crossing count obeys the path-degree rule at every level.
Branch entropy from coarea weights rises and falls with multiplicity.

Part B. A symplectic ensemble evolved forward and then exactly reversed:
the observed binned entropy H_eps(t) changes along the trajectory while the
hidden dynamics loses nothing (momentum-flip reversal recovers the initial
ensemble to roundoff, and the reversed entropy curve retraces the forward
one). Any observed-entropy change is therefore observational, not
thermodynamic production.

Exploratory label. No thermodynamic claim.
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

from projection_fold import (  # noqa: E402
    branch_entropy_bits,
    canonical_sha256,
    polyline_level_crossings,
)

PARAMS = {"omega_t": 1.0, "omega_u": 1.2, "lambda": 0.1, "g": 0.25, "field": 1.0}
DT = 1e-3
TAU_MAX = 40.0
N_STEPS = int(round(TAU_MAX / DT))
SEED = 20260804
N_ENSEMBLE = 10000
SNAPSHOT_EVERY = 40
BIN_EDGES = np.arange(-3.0, 3.0 + 0.05, 0.05)
FOLD_MARGIN = 5e-3


def forces(t, u):
    coupling = PARAMS["g"] * PARAMS["field"]
    ft = -(PARAMS["omega_t"] ** 2) * t - coupling * u
    fu = -(PARAMS["omega_u"] ** 2) * u - PARAMS["lambda"] * u**3 - coupling * t
    return ft, fu


def energy(t, pt, px, u, pu):
    coupling = PARAMS["g"] * PARAMS["field"]
    return (
        0.5 * (pt**2 + px**2 + pu**2)
        + 0.5 * PARAMS["omega_t"] ** 2 * t**2
        + 0.5 * PARAMS["omega_u"] ** 2 * u**2
        + 0.25 * PARAMS["lambda"] * u**4
        + coupling * t * u
    )


def verlet_step(state, h):
    t, pt, x, px, u, pu = state
    ft0, fu0 = forces(t, u)
    pt_half = pt + 0.5 * h * ft0
    pu_half = pu + 0.5 * h * fu0
    t = t + h * pt_half
    u = u + h * pu_half
    x = x + h * px
    ft1, fu1 = forces(t, u)
    return [t, pt_half + 0.5 * h * ft1, x, px, u, pu_half + 0.5 * h * fu1]


def binned_entropy_bits(values):
    counts, _ = np.histogram(values, bins=BIN_EDGES)
    inside = int(counts.sum())
    if inside != values.size:
        raise ValueError("samples escaped the declared bin range")
    masses = counts[counts > 0] / inside
    return float(-(masses * np.log2(masses)).sum())


def part_a_single_trajectory():
    state = [0.0, 1.0, 0.0, 0.2, 0.1, 0.0]
    tau = np.linspace(0.0, TAU_MAX, N_STEPS + 1)
    t_path = np.empty(N_STEPS + 1)
    pt_path = np.empty(N_STEPS + 1)
    t_path[0], pt_path[0] = state[0], state[1]
    for k in range(1, N_STEPS + 1):
        state = verlet_step(state, DT)
        t_path[k], pt_path[k] = state[0], state[1]

    sign_flips = np.nonzero(pt_path[:-1] * pt_path[1:] < 0.0)[0]
    alpha = pt_path[sign_flips] / (pt_path[sign_flips] - pt_path[sign_flips + 1])
    fold_tau = tau[sign_flips] + alpha * DT
    fold_t = t_path[sign_flips] + alpha * (t_path[sign_flips + 1] - t_path[sign_flips])

    breakpoints = np.sort(np.concatenate([fold_t, [t_path[0], t_path[-1]]]))
    lo, hi = t_path.min() + 0.02, t_path.max() - 0.02
    levels = np.linspace(lo, hi, 400)
    levels = levels[np.min(np.abs(levels[:, None] - breakpoints[None, :]), axis=1) > FOLD_MARGIN]

    multiplicity, signed, entropy = [], [], []
    for level in levels:
        crossings, weights = polyline_level_crossings(tau, t_path, pt_path, level)
        multiplicity.append(len(crossings))
        signed.append(int(sum(c["orientation"] for c in crossings)))
        entropy.append(branch_entropy_bits(weights))

    multiplicity = np.array(multiplicity)
    signed = np.array(signed)
    t0, tT = t_path[0], t_path[-1]
    expected_signed = np.where(
        (levels > min(t0, tT)) & (levels < max(t0, tT)), np.sign(tT - t0), 0
    ).astype(int)
    assert np.array_equal(signed, expected_signed), "path-degree rule violated"

    band_index = np.searchsorted(breakpoints, levels)
    band_multiplicity = {}
    for band, m in zip(band_index, multiplicity, strict=True):
        band_multiplicity.setdefault(int(band), set()).add(int(m))
    assert all(len(v) == 1 for v in band_multiplicity.values()), \
        "multiplicity not constant between breakpoints"
    profile = {band: v.pop() for band, v in sorted(band_multiplicity.items())}
    fold_values = set(np.round(fold_t, 12))
    steps = []
    bands = sorted(profile)
    for a, b in zip(bands[:-1], bands[1:], strict=False):
        if b != a + 1:
            continue
        crossed = breakpoints[a]
        step = abs(profile[b] - profile[a])
        expected = 2 if np.round(crossed, 12) in fold_values else 1
        steps.append((float(crossed), int(step), int(expected)))
        assert step == expected, f"wrong multiplicity step at breakpoint {crossed}"

    return {
        "fold_tau": fold_tau.tolist(),
        "fold_t": fold_t.tolist(),
        "levels": levels.tolist(),
        "multiplicity": multiplicity.tolist(),
        "signed_count": signed.tolist(),
        "branch_entropy_bits": entropy,
        "multiplicity_profile_by_band": {str(k): v for k, v in profile.items()},
        "breakpoint_steps_checked": len(steps),
        "signed_rule": "verified at every level",
    }


def part_b_reversible_ensemble():
    rng = np.random.RandomState(SEED)
    t = 0.01 * rng.standard_normal(N_ENSEMBLE)
    pt = 1.0 + 0.05 * rng.standard_normal(N_ENSEMBLE)
    x = np.zeros(N_ENSEMBLE)
    px = 0.2 + 0.01 * rng.standard_normal(N_ENSEMBLE)
    u = 0.1 + 0.05 * rng.standard_normal(N_ENSEMBLE)
    pu = 0.05 * rng.standard_normal(N_ENSEMBLE)
    initial = np.stack([t, pt, x, px, u, pu])
    e0 = energy(t, pt, px, u, pu)

    def run(state_vec, n_steps, record):
        t, pt, x, px, u, pu = [s.copy() for s in state_vec]
        curve = []
        if record:
            curve.append(binned_entropy_bits(t))
        for k in range(1, n_steps + 1):
            ft0, fu0 = forces(t, u)
            pt_half = pt + 0.5 * DT * ft0
            pu_half = pu + 0.5 * DT * fu0
            t = t + DT * pt_half
            u = u + DT * pu_half
            x = x + DT * px
            ft1, fu1 = forces(t, u)
            pt = pt_half + 0.5 * DT * ft1
            pu = pu_half + 0.5 * DT * fu1
            if record and k % SNAPSHOT_EVERY == 0:
                curve.append(binned_entropy_bits(t))
        return [t, pt, x, px, u, pu], curve

    final, forward_curve = run(list(initial), N_STEPS, record=True)
    e_final = energy(final[0], final[1], final[3], final[4], final[5])
    drift = np.max(np.abs(e_final - e0) / np.maximum(np.abs(e0), 1.0))

    reversed_start = [final[0], -final[1], final[2], -final[3], final[4], -final[5]]
    back, reverse_curve = run(reversed_start, N_STEPS, record=True)
    recovered = np.stack([back[0], -back[1], back[2], -back[3], back[4], -back[5]])
    recovery_residual = float(np.max(np.abs(recovered - initial)))

    forward = np.array(forward_curve)
    reverse = np.array(reverse_curve)
    retrace_defect = float(np.max(np.abs(reverse - forward[::-1])))

    assert recovery_residual < 1e-9, "hidden state not recovered: dynamics not reversible"
    assert float(drift) < 1e-6, "energy drift exceeds the sealed fixed-step bar"

    return {
        "n_ensemble": N_ENSEMBLE,
        "seed": SEED,
        "snapshot_tau": (np.arange(forward.size) * SNAPSHOT_EVERY * DT).tolist(),
        "forward_entropy_bits": forward.tolist(),
        "reverse_entropy_bits": reverse.tolist(),
        "entropy_min": float(forward.min()),
        "entropy_max": float(forward.max()),
        "entropy_range_bits": float(forward.max() - forward.min()),
        "recovery_residual": recovery_residual,
        "retrace_defect": retrace_defect,
        "max_relative_energy_drift": float(drift),
        "bin_width": 0.05,
        "bin_range": [-3.0, 3.0],
    }


def main() -> int:
    part_a = part_a_single_trajectory()
    part_b = part_b_reversible_ensemble()
    record = {
        "schema": "pe2-reversible-fold-cycle-v1",
        "label": "exploratory",
        "parameters": PARAMS,
        "dt": DT,
        "tau_max": TAU_MAX,
        "part_a_observation_axis": part_a,
        "part_b_reversible_ensemble": part_b,
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
    output = Path(__file__).resolve().parents[1] / "results" / "pe2-cycle.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    folds = part_a["fold_tau"]
    print(f"part A: {len(folds)} folds; multiplicity profile "
          f"{list(part_a['multiplicity_profile_by_band'].values())}; "
          f"{part_a['breakpoint_steps_checked']} breakpoint steps verified; "
          f"signed rule verified at every level")
    print(f"part B: entropy range {part_b['entropy_range_bits']:.4f} bits "
          f"(min {part_b['entropy_min']:.4f}, max {part_b['entropy_max']:.4f}); "
          f"recovery residual {part_b['recovery_residual']:.3e}; "
          f"retrace defect {part_b['retrace_defect']:.3e}; "
          f"drift {part_b['max_relative_energy_drift']:.3e}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
