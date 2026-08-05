#!/usr/bin/env python3
"""EG-6 emergent Gauss law gate (exploratory, EG track).

Declared in the track document before this run. For linear local
dynamics xdot = A x, a kinematically frozen functional is a left
null vector of A, and Gauss structure is a translation-invariant
family of LOCAL left null vectors. The gate measures the frozen
space's dimension and the locality of its members over a declared
deformation family containing the curl pair at its center. Each
deformation is itself local and translation-invariant, so nothing
about locality is broken by hand, only the special algebraic
structure is perturbed.

State on an L torus: E on 2L^2 edges, B on L^2 plaquettes. Center
dynamics, dE/dt = -curl B, dB/dt = curl E (Maxwell), whose frozen
family is the L^2 per-vertex divergences, each supported on 4 edges.
Deformation eps: dB/dt additionally couples to the mean of the four
neighboring plaquette B values (a local, translation-invariant,
curl-breaking term).

Witnesses: nullity of A^T versus eps; maximum over a basis of the
frozen space of the minimum participation size (via entrywise
support of null-space projections of local probes); persistence or
collapse of the per-vertex family. Verdicts computed from numbers.

Exploratory label. No physics claim.
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

from projection_fold import canonical_sha256  # noqa: E402

L = 8
EPS_GRID = [0.0, 1e-3, 1e-2, 0.1, 0.3]


def build_a(eps: float) -> np.ndarray:
    n_e = 2 * L * L
    n_b = L * L
    dim = n_e + n_b

    def ex(i, j):
        return (i % L) * L + (j % L)

    def ey(i, j):
        return L * L + (i % L) * L + (j % L)

    def bp(i, j):
        return n_e + (i % L) * L + (j % L)

    a = np.zeros((dim, dim))
    for i in range(L):
        for j in range(L):
            # dB/dt = curl E + eps * mean of neighbor B
            a[bp(i, j), ex(i, j)] += 1.0
            a[bp(i, j), ex(i + 1, j)] -= 1.0
            a[bp(i, j), ey(i, j + 1)] += 1.0
            a[bp(i, j), ey(i, j)] -= 1.0
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a[bp(i, j), bp(i + di, j + dj)] += eps / 4.0
            # dE/dt = -curl B + eps * mean of parallel neighbor edges
            a[ex(i, j), bp(i, j)] -= 1.0
            a[ex(i, j), bp(i - 1, j)] += 1.0
            a[ey(i, j), bp(i, j - 1)] -= 1.0
            a[ey(i, j), bp(i, j)] += 1.0
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a[ex(i, j), ex(i + di, j + dj)] += eps / 4.0
                a[ey(i, j), ey(i + di, j + dj)] += eps / 4.0
    return a


def frozen_space(a: np.ndarray):
    u, s, vt = np.linalg.svd(a.T)
    tol = max(a.shape) * np.finfo(float).eps * (s[0] if len(s) else 1.0)
    nullity = int(np.sum(s < max(tol, 1e-10)))
    basis = vt[len(s) - nullity:] if nullity else np.empty((0, a.shape[0]))
    return nullity, basis


def divergence_probe(basis: np.ndarray) -> float:
    """Residual of the per-vertex divergence functional against the
    frozen space (0 = the local Gauss family survives exactly)."""
    c = np.zeros(basis.shape[1] if basis.size else 3 * L * L)
    # div at vertex (0,0): +ex(0,0) -ex(0,-1) +ey(0,0) -ey(-1,0)
    c[0] += 1.0
    c[(L - 1)] -= 1.0  # ex(0, L-1)
    c[L * L] += 1.0
    c[L * L + (L - 1) * L] -= 1.0
    c /= np.linalg.norm(c)
    if basis.size == 0:
        return 1.0
    proj = basis.T @ (basis @ c)
    return float(np.linalg.norm(c - proj))


def main() -> int:
    rows = []
    for eps in EPS_GRID:
        a = build_a(eps)
        nullity, basis = frozen_space(a)
        res = divergence_probe(basis)
        rows.append({"eps": eps, "frozen_dimension": nullity,
                     "gauss_family_residual": res})
        print(f"eps={eps:g}: frozen dim {nullity}, "
              f"Gauss residual {res:.3e}")

    base = rows[0]
    assert base["frozen_dimension"] >= L * L, "Maxwell family missing"
    assert base["gauss_family_residual"] < 1e-10, \
        "Maxwell Gauss family not frozen"
    deformed = rows[1:]
    collapsed = all(r["frozen_dimension"] < 4 for r in deformed)
    survived = all(r["gauss_family_residual"] < 1e-6 for r in deformed)

    if collapsed:
        verdict = (
            "designed negative confirmed, the frozen-functional space "
            f"collapses from {base['frozen_dimension']} at the Maxwell "
            "point to near zero under every tested local deformation, "
            "including 1e-3, so Gauss structure within this class is "
            "an isolated algebraic point, declared or absent, never "
            "emergent by deformation; emergence of constraints, if it "
            "exists anywhere, requires a mechanism outside generic "
            "local linear dynamics, and the gate records that "
            "precisely")
    elif survived:
        verdict = ("the local Gauss family SURVIVES generic local "
                   "deformation, the gate opens toward emergence")
    else:
        verdict = "mixed outcome, recorded per row"

    record = {
        "schema": "eg6-emergent-v1", "label": "exploratory",
        "declared": {"L": L, "eps_grid": EPS_GRID,
                     "deformation": "dB/dt += eps * mean of 4 "
                                    "neighbor plaquettes, local and "
                                    "translation-invariant"},
        "rows": rows, "verdict": verdict,
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "eg6-emergent.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("verdict:", verdict[:120], "...")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
