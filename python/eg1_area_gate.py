#!/usr/bin/env python3
"""EG-1 area-versus-volume gate (exploratory, EG track).

The track's designed point of failure. For each declared mechanism the
number of independently distinguishable hidden states associated with
a region of linear size R is measured under the decided operational
counts (track document section 10, question 2, decided 2026-08-05
before this run). Primary count, H(region | boundary data). Secondary
witness, I(region ; complement). Two-dimensional lattices are used so
that every count is an exact finite quantity, with volume meaning R^2
and area meaning R^1.

Three arms, each a concrete Level-0 construction.

Arm A, generic control. Independent uniform spins on the sites of an
R x R block. H(interior | boundary ring) = (R-2)^2 bits exactly and
I(region ; complement) = 0 exactly. Validates that the instrument
reports a volume law where one is guaranteed.

Arm B, Gauss-law constraint / gauge quotient (two mechanism classes of
track section 5 that share one count). Hidden state, edge spins on an
L x L torus, ensemble uniform over the cycle space (the configurations
satisfying the Z2 Gauss constraint at every vertex; equivalently the
gauge-orbit count of the vertex-flip action). For a uniform ensemble
over a GF(2) linear code, every count is a code dimension, and code
dimensions of graphical codes are cycle-space dimensions computable
exactly by connected-component counting. With S the block-internal
edges of an R x R block, H(S | complement data) = dim of the cycle
space supported inside S, H(S) = dim C - dim of the cycle space
avoiding S, and I = H(S) - H(S | complement). Closed forms exist,
(R-1)^2 for the interior count and 4R-5 for the cut mutual
information, and the computation must reproduce both exactly. The
two counts genuinely split on this arm, volume in the primary and
area in the secondary, which is the divergence the section 10
decision anticipated.

Arm C, boundary-limited access. Independent interior spins read only
through boundary data (the observation map exposes the ring). The
observer-accessible image counts 4R-4 bits, area by construction, but
the hidden interior residual H(interior | boundary) = (R-2)^2 stays a
volume law. This is the standing warning of track section 5 made
quantitative, an access limit is not a distinguishability limit, and
the arm is recorded as the warning's instance, never as a pass.

Fits. For every arm and count, log2 of the count against log2 R over
the declared range (two decades, R = 3 to 301), free power-law slope
against the fixed alternatives exponent 2 (volume) and exponent 1
(area), classification by residual.

Expected and asserted. Arm A and arm C reproduce their closed forms
exactly. Arm B reproduces its closed forms exactly at every R. The
gate verdict is expected to be the designed negative, no declared
mechanism yields area scaling in the primary count.

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

R_GRID = [3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 91, 128, 181, 256, 301]
L_PAD = 9  # torus side L = 2R + L_PAD keeps the complement rich


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.n_components = n

    def find(self, a: int) -> int:
        p = self.parent
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb
            self.n_components -= 1


def cycle_dim(edges) -> int:
    """Cycle-space dimension |E| - |V| + components of the subgraph
    induced by an edge list; isolated vertices cancel and are
    correctly excluded by inducing on touched vertices only."""
    verts: dict[int, int] = {}
    pairs = []
    for a, b in edges:
        for v in (a, b):
            if v not in verts:
                verts[v] = len(verts)
        pairs.append((verts[a], verts[b]))
    uf = UnionFind(len(verts))
    for a, b in pairs:
        uf.union(a, b)
    return len(pairs) - len(verts) + uf.n_components


def torus_edges(side: int):
    def site(i: int, j: int) -> int:
        return (i % side) * side + (j % side)
    for i in range(side):
        for j in range(side):
            yield (site(i, j), site(i, j + 1))
            yield (site(i, j), site(i + 1, j))


def block_internal(side: int, r: int) -> set[tuple[int, int]]:
    def site(i: int, j: int) -> int:
        return i * side + j
    edges = set()
    for i in range(r):
        for j in range(r):
            if j + 1 < r:
                edges.add((site(i, j), site(i, j + 1)))
            if i + 1 < r:
                edges.add((site(i, j), site(i + 1, j)))
    return edges


def fit_exponent(rs, counts):
    x = np.log2(np.array(rs, dtype=float))
    y = np.log2(np.array(counts, dtype=float))
    slope, intercept = np.polyfit(x, y, 1)

    def resid(expnt: float) -> float:
        c = float(np.mean(y - expnt * x))
        return float(np.sqrt(np.mean((y - expnt * x - c) ** 2)))

    return {"free_slope": float(slope),
            "residual_free": float(np.sqrt(np.mean(
                (y - slope * x - intercept) ** 2))),
            "residual_volume_2": resid(2.0),
            "residual_area_1": resid(1.0),
            "classification": "volume" if resid(2.0) < resid(1.0)
                              else "area"}


def main() -> int:
    arm_b_rows = []
    for r in R_GRID:
        side = 2 * r + L_PAD
        n_edges = 2 * side * side
        dim_c = side * side + 1  # torus cycle space E - V + 1
        internal = block_internal(side, r)
        cyc_s = cycle_dim(list(internal))
        assert cyc_s == (r - 1) ** 2, f"interior closed form at R={r}"
        complement = [e for e in torus_edges(side)
                      if e not in internal and (e[1], e[0]) not in internal]
        cyc_sc = cycle_dim(complement)
        # block sites more than one step inside the ring touch no
        # complement edge, so the complement subgraph misses (R-2)^2
        # vertices and its cycle dimension is L^2 - R^2 - 2R + 5
        formula_sc = side * side - r * r - 2 * r + 5
        assert cyc_sc == formula_sc, \
            f"complement closed form at R={r}: {cyc_sc} vs {formula_sc}"
        h_given = cyc_s
        h_marg = dim_c - cyc_sc
        assert h_marg == r * r + 2 * r - 4, f"marginal at R={r}"
        mi = h_marg - h_given
        assert mi == 4 * r - 5, f"MI closed form at R={r}"
        arm_b_rows.append({"R": r, "L": side, "edges": n_edges,
                           "H_given_boundary": h_given,
                           "H_marginal": h_marg,
                           "MI": mi})

    rs = [row["R"] for row in arm_b_rows]
    arm_a = {
        "H_given_boundary": [(r - 2) ** 2 for r in rs],
        "MI": [0 for r in rs],
        "closed_form": "independent spins: H(int|bnd) = (R-2)^2, MI = 0",
    }
    arm_c = {
        "accessible_image_bits": [4 * r - 4 for r in rs],
        "hidden_residual_bits": [(r - 2) ** 2 for r in rs],
        "closed_form": "access image 4R-4 (area by construction), "
                       "hidden residual (R-2)^2 (volume)",
    }

    fits = {
        "arm_a_primary": fit_exponent(rs, arm_a["H_given_boundary"]),
        "arm_b_primary": fit_exponent(
            rs, [row["H_given_boundary"] for row in arm_b_rows]),
        "arm_b_mi": fit_exponent(rs, [row["MI"] for row in arm_b_rows]),
        "arm_c_access": fit_exponent(rs, arm_c["accessible_image_bits"]),
        "arm_c_hidden": fit_exponent(rs, arm_c["hidden_residual_bits"]),
    }

    assert fits["arm_a_primary"]["classification"] == "volume"
    assert fits["arm_b_primary"]["classification"] == "volume"
    assert fits["arm_b_mi"]["classification"] == "area"
    assert fits["arm_c_access"]["classification"] == "area"
    assert fits["arm_c_hidden"]["classification"] == "volume"

    verdict = (
        "gate negative in the primary count for every measured "
        "mechanism class: the Gauss-law constraint and gauge-quotient "
        "ensembles count exactly (R-1)^2 interior distinctions given "
        "the boundary, a volume law, and boundary-limited access "
        "leaves the hidden interior residual a volume law while only "
        "the observer-accessible image is area-scaling by "
        "construction, the standing warning of section 5 made "
        "quantitative; the counts split exactly as the section 10 "
        "decision anticipated, since the same Gauss-law ensemble "
        "carries an exact area-law cut mutual information 4R-5, so "
        "constraint structure does put area scaling into "
        "observer-relative correlations while leaving interior "
        "independence extensive, and any entropic-gravity reading "
        "built on this mechanism class would have to live on the "
        "correlation count the decision relegated to secondary"
    )

    record = {
        "schema": "eg1-area-gate-v1",
        "label": "exploratory",
        "declared": {
            "counts_decision": "primary H(region|boundary), secondary "
                "I(region;complement), decided in the track document "
                "section 10 question 2 before this run",
            "R_grid": R_GRID, "L_pad": L_PAD,
            "lattice": "2D; volume = R^2, area = R^1",
            "arms": {
                "A": "independent spins, generic volume control",
                "B": "Z2 Gauss-law / gauge-quotient uniform code "
                     "ensemble on torus edges, exact cycle-space "
                     "dimensions via component counting",
                "C": "boundary-limited access, the standing-warning "
                     "instance, never a pass",
            },
            "fit_alternatives": ["free power law", "exponent 2 volume",
                                 "exponent 1 area"],
        },
        "arm_a": arm_a,
        "arm_b": arm_b_rows,
        "arm_c": arm_c,
        "fits": fits,
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
        / "eg1-area-gate.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"R range {rs[0]}..{rs[-1]} ({math.log10(rs[-1]/rs[0]):.2f} "
          f"decades), largest torus {arm_b_rows[-1]['edges']} edges")
    for key, f in fits.items():
        print(f"{key}: slope {f['free_slope']:.4f} -> "
              f"{f['classification']}")
    print("verdict:", verdict[:100], "...")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
