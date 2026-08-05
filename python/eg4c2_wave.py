#!/usr/bin/env python3
"""EG-4c round two: real amplitudes restore dilution
(exploratory, EG track).

Declared in the track document before this run. Round one refuted
the dimensional-dilution hypothesis and located the obstruction in
the finite field, parity path-counting cannot decay. This round
replaces the field, not the discipline. The substrate is the
two-dimensional discrete wave equation, leapfrog with site stiffness
kappa, reversible, deterministic, local, and linear over the reals.
The vacuum is i.i.d. standard Gaussian initial data (positions and
previous positions). Matter is an impedance defect, one site whose
stiffness differs, a rule substitution containing no potential and
no function of distance.

Exact instrument. Every final-time cell value is a real linear
functional of the initial data, computed by the adjoint recursion
a' = 2a + b + L(kappa a), b' = -a, which handles site-dependent
stiffness exactly. A window's marginal is the zero-mean Gaussian
with covariance given by dot products of functional pairs, and
D(mat || vac) is the closed Gaussian form, no sampling and no
truncation beyond float arithmetic.

Probes. P0 control, the covariance of a small window against
direct dense evolution of the full covariance on a tiny lattice.
P1 causality null exact, unit wave speed. P2 static axis profile at
two doubling times on lattices too large for any wrap, convergence,
gradedness, monotone decay. P3 isotropy, axis against diagonal. P4
superposition against source separation. P5 Poisson localization of
the profile's discrete Laplacian. Verdicts computed from the
numbers after measurement.

Exploratory label. No physics claim.
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

KAPPA = 0.2
KAPPA_DEFECT = 0.4
T_TIMES = (32, 64)
WINDOW = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
AXIS_RS = list(range(2, 31, 2))
PAIR_SEPS = (8, 16, 32)


def laplacian(f: np.ndarray) -> np.ndarray:
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0)
            + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4.0 * f)


def adjoint_functional(side: int, steps: int, cell, kappa_map):
    """Functional pair (a, b) with value = sum a*phi_0 + b*phi_{-1}
    for the final-time position at `cell`, by adjoint recursion."""
    a = np.zeros((side, side))
    b = np.zeros((side, side))
    a[cell[0] % side, cell[1] % side] = 1.0
    for _ in range(steps):
        a_new = 2.0 * a + b + laplacian(kappa_map * a)
        b = -a
        a = a_new
    return a, b


def window_cov(side, steps, origin, kappa_map) -> np.ndarray:
    funcs = [adjoint_functional(side, steps,
                                (origin[0] + di, origin[1] + dj),
                                kappa_map)
             for di, dj in WINDOW]
    k = len(funcs)
    cov = np.empty((k, k))
    for i in range(k):
        for j in range(i, k):
            v = float((funcs[i][0] * funcs[j][0]).sum()
                      + (funcs[i][1] * funcs[j][1]).sum())
            cov[i, j] = cov[j, i] = v
    return cov


def gauss_kl_bits(cov_mat: np.ndarray, cov_vac: np.ndarray) -> float:
    k = cov_mat.shape[0]
    sign_v, logdet_v = np.linalg.slogdet(cov_vac)
    sign_m, logdet_m = np.linalg.slogdet(cov_mat)
    assert sign_v > 0 and sign_m > 0, "window covariance not PD"
    tr = float(np.trace(np.linalg.solve(cov_vac, cov_mat)))
    return float(0.5 * (tr - k + logdet_v - logdet_m) / math.log(2.0))


def kappa_field(side: int, defects) -> np.ndarray:
    kmap = np.full((side, side), KAPPA)
    for a, b in defects:
        kmap[a % side, b % side] = KAPPA_DEFECT
    return kmap


def field_at(side, steps, origin, defects) -> float:
    return gauss_kl_bits(
        window_cov(side, steps, origin, kappa_field(side, defects)),
        window_cov(side, steps, origin, kappa_field(side, ())))


def main() -> int:
    # P0: control against dense full-covariance evolution, tiny case
    s_small, t_small = 6, 4
    kmap = kappa_field(s_small, ((2, 2),))
    n = s_small * s_small
    big = np.zeros((2 * n, 2 * n))
    big[:n, :n] = np.eye(n)
    big[n:, n:] = np.eye(n)

    def step_dense(sigma):
        upd = np.zeros((2 * n, 2 * n))
        for idx in range(n):
            i, j = divmod(idx, s_small)
            e = np.zeros((s_small, s_small))
            e[i, j] = 1.0
            row = (2.0 * e + kmap[i, j] * laplacian(e))
            upd[idx, :n] = row.reshape(-1)
            upd[idx, n + idx] = -1.0
            upd[n + idx, idx] = 1.0
        return upd @ sigma @ upd.T

    sigma = big
    for _ in range(t_small):
        sigma = step_dense(sigma)
    cells = [(0, 0), (0, 1), (1, 0)]
    idxs = [i * s_small + j for i, j in cells]
    dense_cov = sigma[np.ix_(idxs, idxs)]
    funcs = [adjoint_functional(s_small, t_small, c, kmap)
             for c in cells]
    adj_cov = np.empty((3, 3))
    for i in range(3):
        for j in range(3):
            adj_cov[i, j] = float(
                (funcs[i][0] * funcs[j][0]).sum()
                + (funcs[i][1] * funcs[j][1]).sum())
    ctl_dev = float(np.max(np.abs(dense_cov - adj_cov)))
    assert ctl_dev < 1e-9, f"instrument control failed: {ctl_dev}"

    profiles = {}
    for t_steps in T_TIMES:
        side = 2 * t_steps + 48
        c = side // 2
        src = ((c, c),)

        d_far = field_at(side, t_steps, (c + t_steps + 10, c), src)
        assert d_far == 0.0, f"causality violated at T={t_steps}"

        axis = [{"r": r,
                 "phi_bits": field_at(side, t_steps, (c, c + r), src)}
                for r in AXIS_RS]
        diag = [{"r": r,
                 "phi_bits": field_at(side, t_steps,
                                      (c + r // 2, c + r // 2), src)}
                for r in AXIS_RS]
        profiles[str(t_steps)] = {"axis": axis, "diagonal": diag}

    a32 = np.array([row["phi_bits"] for row in profiles["32"]["axis"]])
    a64 = np.array([row["phi_bits"] for row in profiles["64"]["axis"]])
    scale = float(max(a64.max(), 1e-300))
    conv = float(np.max(np.abs(a64 - a32))) / scale
    spread = float((a64.max() - a64.min()) / scale) \
        if a64.max() > 0 else 0.0
    grads = np.diff(a64)
    monotone_decay = bool(np.all(grads <= 1e-12))
    d64 = np.array([row["phi_bits"]
                    for row in profiles["64"]["diagonal"]])
    iso_dev = float(np.max(np.abs(a64 - d64))) / scale

    t_steps = 64
    side = 2 * t_steps + 48
    c = side // 2
    superposition = []
    for sep in PAIR_SEPS:
        s1 = ((c, c - sep // 2),)
        s2 = ((c, c + sep // 2),)
        s12 = s1 + s2
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
            bool(sup_rel[-1] < sup_rel[0] and sup_rel[-1] < 0.05),
        "poisson_source_localized": bool(poisson_localized),
    }
    items = {k: bool(v) for k, v in items.items()}

    pieces = []
    pieces.append(
        f"wave-substrate axis profile at T=64 runs from "
        f"{a64[0]:.4g} bits at r=2 to {a64[-1]:.4g} at r=30, spread "
        f"{spread:.3g}, doubling-time convergence {conv:.3g}, "
        f"monotone decay {monotone_decay}.")
    pieces.append(
        "real amplitudes "
        + ("RESTORE dilution, the static field is graded"
           if items["static_graded"] else
           "do not restore dilution at these times") + ".")
    pieces.append(
        f"isotropy deviation {iso_dev:.3g}; superposition relative "
        f"deviations {[round(v, 4) for v in sup_rel]} across "
        f"separations {list(PAIR_SEPS)}; laplacian near/mid "
        f"{lap_near:.3g}/{lap_mid:.3g}.")
    passed = sum(1 for v in items.values() if v)
    pieces.append(f"{passed} of {len(items)} items pass; the EG-4 bar "
                  + ("is passed on this substrate."
                     if passed == len(items) else "remains intact."))
    verdict = " ".join(pieces)

    record = {
        "schema": "eg4c2-wave-v1",
        "label": "exploratory",
        "declared": {"substrate": "2D discrete wave equation, "
                                  "leapfrog, kappa 0.2",
                     "defect": "impedance site, kappa 0.4",
                     "vacuum": "iid standard Gaussian initial data",
                     "times": list(T_TIMES),
                     "window": WINDOW, "axis_rs": AXIS_RS,
                     "pair_separations": list(PAIR_SEPS)},
        "instrument_control_dev": ctl_dev,
        "profiles": profiles,
        "static_convergence_relative": conv,
        "static_spread": spread,
        "isotropy_deviation": iso_dev,
        "superposition": superposition,
        "laplacian_near": float(lap_near),
        "laplacian_mid": float(lap_mid),
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
        / "eg4c2-wave.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"control dev {ctl_dev:.2e}")
    print("axis T=64:", [(row["r"], round(row["phi_bits"], 5))
                         for row in profiles["64"]["axis"]])
    print(f"conv {conv:.4g}, spread {spread:.4g}, iso {iso_dev:.4g}")
    print("superposition:", [(s["separation"],
                              round(s["relative_deviation"], 4))
                             for s in superposition])
    print("items:", items)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
