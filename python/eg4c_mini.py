#!/usr/bin/env python3
"""EG-4c mini-campaign: the dimensional-dilution hypothesis
(exploratory, EG track).

Declared in the track document before this run. Hypothesis, the flat
statics of EG-4b are a one-dimensional artifact, since radiation does
not dilute in one dimension, and two-dimensional geometric dilution
restores a distance-graded static response with distance as the
continuous weak-field knob. Fails if the two-dimensional static
profile is flat or carries no monotone distance dependence.

Substrate. The two-dimensional XOR rule, each cell becomes the XOR
of its four von Neumann neighbors, defect sites additionally XOR
their own value (the 150-analogue). Product Bernoulli(p) initial
ensemble. Every window functional is computed by backward adjoint
evolution, which for this symmetric rule takes the same form as the
forward rule, and every window distribution is exact Walsh analysis.

Probes. P0 instrument control against brute-force enumeration. P1
causality null exact. P2 static axis profile at two doubling times,
convergence and gradedness. P3 isotropy, axis against diagonal. P4
superposition against source separation. P5 two-dimensional Poisson
and Gauss forms on the measured profile. Verdicts computed from the
numbers after measurement.

Exploratory label. No physics claim.
"""
from __future__ import annotations

import itertools
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

P_BIAS = 0.2
T_TIMES = (32, 64)
WINDOW_SHAPE = (2, 3)  # 6 cells, 64 Walsh combinations
AXIS_RS = list(range(2, 31, 2))
PAIR_SEPS = (8, 16, 32)


def backward_functional(side: int, steps: int, cell: tuple[int, int],
                        defects: frozenset[tuple[int, int]]) -> np.ndarray:
    """Support of the GF(2) functional of a final-time cell over the
    initial lattice, by adjoint evolution."""
    f = np.zeros((side, side), dtype=bool)
    f[cell[0] % side, cell[1] % side] = True
    if defects:
        dmask = np.zeros((side, side), dtype=bool)
        for a, b in defects:
            dmask[a % side, b % side] = True
    for _ in range(steps):
        nxt = (np.roll(f, 1, axis=0) ^ np.roll(f, -1, axis=0)
               ^ np.roll(f, 1, axis=1) ^ np.roll(f, -1, axis=1))
        if defects:
            nxt[dmask] ^= f[dmask]
        f = nxt
    return f


def window_supports(side, steps, origin, defects):
    cells = [(origin[0] + di, origin[1] + dj)
             for di in range(WINDOW_SHAPE[0])
             for dj in range(WINDOW_SHAPE[1])]
    return [backward_functional(side, steps, c, defects) for c in cells]


def distribution_from_supports(supports, p: float) -> np.ndarray:
    m = len(supports)
    size = 1 << m
    bias = 1.0 - 2.0 * p
    coef = np.empty(size)
    coef[0] = 1.0
    cur = np.zeros_like(supports[0])
    prev_gray = 0
    for s in range(1, size):
        gray = s ^ (s >> 1)
        changed = gray ^ prev_gray
        cur = cur ^ supports[changed.bit_length() - 1]
        prev_gray = gray
        coef[gray] = bias ** int(cur.sum())
    vec = coef.copy()
    h = 1
    while h < size:
        for i in range(0, size, h * 2):
            a = vec[i:i + h].copy()
            b = vec[i + h:i + 2 * h].copy()
            vec[i:i + h] = a + b
            vec[i + h:i + 2 * h] = a - b
        h *= 2
    probs = vec / size
    assert probs.min() > -1e-12, f"negative probability {probs.min()}"
    probs = np.clip(probs, 0.0, None)
    return probs / probs.sum()


def kl_bits(p_mat: np.ndarray, q_vac: np.ndarray) -> float:
    mask = p_mat > 0
    if np.any(q_vac[mask] <= 0):
        return float("inf")
    return float((p_mat[mask]
                  * np.log2(p_mat[mask] / q_vac[mask])).sum())


def field_at(side, steps, origin, defects) -> float:
    mat = distribution_from_supports(
        window_supports(side, steps, origin, defects), P_BIAS)
    vac = distribution_from_supports(
        window_supports(side, steps, origin, frozenset()), P_BIAS)
    return kl_bits(mat, vac)


def main() -> int:
    # P0: instrument control on a small 2D case by enumeration
    s_small, t_small = 4, 2
    sup = window_supports(s_small, t_small, (0, 0),
                          frozenset({(1, 1)}))[:4]
    walsh = distribution_from_supports(sup, P_BIAS)
    brute = np.zeros(16)
    flat_sup = [x.reshape(-1) for x in sup]
    for config in itertools.product((0, 1), repeat=s_small * s_small):
        cfg = np.array(config, dtype=bool)
        weight = float(np.prod(np.where(cfg, P_BIAS, 1 - P_BIAS)))
        idx = 0
        for k, row in enumerate(flat_sup):
            idx |= (int(np.logical_and(row, cfg).sum()) & 1) << k
        brute[idx] += weight
    ctl_dev = float(np.max(np.abs(walsh - brute)))
    assert ctl_dev < 1e-12, f"instrument control failed: {ctl_dev}"

    results: dict = {"instrument_control_dev": ctl_dev}

    profiles = {}
    for t_steps in T_TIMES:
        side = 2 * t_steps + 48
        c = side // 2
        src = frozenset({(c, c)})

        # P1: causality null outside the diamond cone
        far = (c + t_steps + 10, c)
        d_far = field_at(side, t_steps, far, src)
        assert d_far == 0.0, f"causality violated at T={t_steps}"

        # P2: axis profile
        axis = [{"r": r,
                 "phi_bits": field_at(side, t_steps, (c, c + r), src)}
                for r in AXIS_RS]
        # P3: diagonal profile (Chebyshev-matched distances)
        diag = [{"r": r,
                 "phi_bits": field_at(side, t_steps,
                                      (c + r // 2, c + r // 2), src)}
                for r in AXIS_RS]
        profiles[str(t_steps)] = {"axis": axis, "diagonal": diag}

    a32 = np.array([row["phi_bits"]
                    for row in profiles["32"]["axis"]])
    a64 = np.array([row["phi_bits"]
                    for row in profiles["64"]["axis"]])
    scale = float(max(a64.max(), 1e-300))
    conv = float(np.max(np.abs(a64 - a32))) / scale
    spread = float((a64.max() - a64.min()) / scale) \
        if a64.max() > 0 else 0.0
    grads = np.diff(a64)
    monotone_decay = bool(np.all(grads <= 1e-12)) \
        or bool(np.all(grads >= -1e-12) and a64[0] < a64[-1])
    d64 = np.array([row["phi_bits"]
                    for row in profiles["64"]["diagonal"]])
    iso_dev = float(np.max(np.abs(a64 - d64))) / scale \
        if scale > 0 else 0.0

    # P4: superposition against separation at T = 64
    t_steps = 64
    side = 2 * t_steps + 48
    c = side // 2
    superposition = []
    for sep in PAIR_SEPS:
        s1 = frozenset({(c, c - sep // 2)})
        s2 = frozenset({(c, c + sep // 2)})
        s12 = s1 | s2
        devs, s_scale = [], 0.0
        for r in range(-sep, sep + 1, max(2, sep // 4)):
            origin = (c + 8, c + r)
            f1 = field_at(side, t_steps, origin, s1)
            f2 = field_at(side, t_steps, origin, s2)
            f12 = field_at(side, t_steps, origin, s12)
            devs.append(abs(f12 - (f1 + f2)))
            s_scale = max(s_scale, f1 + f2)
        superposition.append({"separation": sep,
                              "max_abs_deviation": max(devs),
                              "scale": s_scale,
                              "relative_deviation":
                                  max(devs) / max(s_scale, 1e-300)})

    # P5: Poisson and Gauss on the T = 64 axis profile
    lap = [a64[i + 1] - 2 * a64[i] + a64[i - 1]
           for i in range(1, len(a64) - 1)]
    lap_near = max(abs(v) for i, v in enumerate(lap)
                   if AXIS_RS[i + 1] <= 8)
    lap_mid = max((abs(v) for i, v in enumerate(lap)
                   if 10 <= AXIS_RS[i + 1] <= 24), default=0.0)
    poisson_localized = lap_near > 5.0 * lap_mid if lap_mid > 0 \
        else lap_near > 0

    sup_rel = [s["relative_deviation"] for s in superposition]
    items = {
        "causality_null": True,
        "static_converged": conv < 0.05,
        "static_graded": spread > 0.1,
        "monotone_decay": monotone_decay,
        "isotropy_within_2x_spread": iso_dev < 2.0 * max(spread, 1e-12),
        "superposition_decays_with_separation":
            sup_rel[-1] < sup_rel[0] and sup_rel[-1] < 0.05,
        "poisson_source_localized": bool(poisson_localized),
    }

    pieces = []
    pieces.append(
        f"axis profile at T=64 spans {a64.max():.4g} to "
        f"{a64.min():.4g} bits with spread {spread:.3g} and "
        f"doubling-time convergence {conv:.3g}.")
    pieces.append(
        "the dimensional-dilution hypothesis is "
        + ("SUPPORTED, the two-dimensional statics are graded"
           if items["static_graded"] and items["static_converged"]
           else "NOT supported at these times, "
           + ("the profile has not converged"
              if not items["static_converged"] else
              "the converged profile is flat again")) + ".")
    pieces.append(
        f"isotropy deviation {iso_dev:.3g} against spread "
        f"{spread:.3g}; superposition relative deviations "
        f"{[round(v, 4) for v in sup_rel]} across separations "
        f"{list(PAIR_SEPS)}.")
    passed = sum(1 for v in items.values() if v)
    pieces.append(f"{passed} of {len(items)} items pass; the EG-4 bar "
                  + ("is passed on this substrate."
                     if passed == len(items) else "remains intact."))
    verdict = " ".join(pieces)

    record = {
        "schema": "eg4c-mini-v1",
        "label": "exploratory",
        "declared": {"rule": "2D von Neumann XOR, defect adds center",
                     "bias_p": P_BIAS, "times": list(T_TIMES),
                     "window_shape": list(WINDOW_SHAPE),
                     "axis_rs": AXIS_RS,
                     "pair_separations": list(PAIR_SEPS),
                     "hypothesis": "flat statics are a 1D artifact; "
                                   "2D dilution restores gradedness"},
        "profiles": profiles,
        "static_convergence_relative": conv,
        "static_spread": spread,
        "isotropy_deviation": iso_dev,
        "superposition": superposition,
        "laplacian_near": lap_near,
        "laplacian_mid": lap_mid,
        "items": items,
        "verdict": verdict,
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
        / "eg4c-mini.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"control dev {ctl_dev:.2e}")
    print("axis T=64:", [(row["r"], round(row["phi_bits"], 4))
                         for row in profiles["64"]["axis"]])
    print("diag T=64:", [(row["r"], round(row["phi_bits"], 4))
                         for row in profiles["64"]["diagonal"]])
    print(f"conv {conv:.4g}, spread {spread:.4g}, iso {iso_dev:.4g}")
    print("superposition:", [(s["separation"],
                              round(s["relative_deviation"], 4))
                             for s in superposition])
    print("items:", items)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
