#!/usr/bin/env python3
"""EG-2 matter deformation on the causal-determinism substrate
(exploratory, EG track).

Question, per the track document with the substrate fixed by EG-1b.
Does a local source, with no inserted radial potential anywhere,
deform the fiber measure so that a distinguishability field with
gravitational structure appears? The pilot targets are restated for
the substrate's dimensionality (one space dimension), where the
Newtonian structure to test in EG-4 is the one-dimensional Poisson
and Gauss form, not an inverse-square law.

Level-0 declarations. Vacuum, rule 90 on a ring of 257 cells with an
i.i.d. uniform initial row, evolved 60 steps. Matter, a declared set
of defect cells centered at site zero that use rule 150 instead, with
source sizes 1, 3, and 7 cells. The source is a rule substitution.
It contains no function of distance, no potential, and no coupling
chosen after inspection.

Reverse-engineering audit (structural). A potential-equivalent source
would reweight the vacuum measure by a positive density. The vacuum
measure here is uniform on a linear subspace, and a positive
reweighting cannot move its support, while a rule substitution moves
the support to a different subspace of equal dimension. The declared
source class is therefore not potential-equivalent by construction,
and the audit reduces to verifying that supports actually move, which
the witnesses below record.

Witnesses, all exact subspace arithmetic.

1. Causality null. Every window disjoint from the defect light cone
   carries the identical marginal, subspace equality, not merely
   equal entropy. Asserted exact.
2. Cone-edge sharpness. Single-cell windows scanned across the cone
   boundary at the final time classify equal outside and must show
   any deviation only inside.
3. Local visibility. Single cells and two-by-two patches inside the
   cone, classified equal, nested, or escaped. For a deterministic
   linear substrate single cells are expected to be exactly blind to
   the source, since a nonzero linear functional is uniform either
   way.
4. Extended windows. Row segments of lengths 16, 32, 64 at the final
   time, scanned in position, classified, with finite relative
   entropies recorded where they exist. This is the candidate
   deformation field for EG-4.
5. Source-size dependence of every finite value.

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

from eg_ca_substrate import (  # noqa: E402
    evolve_generators,
    image_relation,
    marginal_entropy_bits,
    window_matrix,
)
from projection_fold import canonical_sha256  # noqa: E402

N_RING = 257
T_STEPS = 60
SOURCES = {1: frozenset({0}),
           3: frozenset({-1, 0, 1}),
           7: frozenset({-3, -2, -1, 0, 1, 2, 3})}
SEG_LENGTHS = [16, 32, 64]


def main() -> int:
    vac = evolve_generators(N_RING, T_STEPS)
    histories = {m: evolve_generators(N_RING, T_STEPS, cells)
                 for m, cells in SOURCES.items()}

    record: dict = {"schema": "eg2-matter-v1", "label": "exploratory"}
    per_source = {}
    for m, hist in histories.items():
        half = max(abs(c) for c in SOURCES[m])
        cone = half + T_STEPS
        entry: dict = {"defect_cells": sorted(SOURCES[m]),
                       "cone_half_width_final": cone}

        # 1. causality null, far window on the opposite side
        far = [(t, j) for t in (T_STEPS - 1, T_STEPS)
               for j in (127, 128, 129)]
        rel, d = image_relation(window_matrix(hist, far),
                                window_matrix(vac, far))
        assert rel == "equal", f"causality null failed for M={m}"
        entry["causality_null"] = rel

        # 2. cone-edge scan, single cells at the final time
        edge = {}
        for r in range(cone - 3, cone + 4):
            rel, d = image_relation(
                window_matrix(hist, [(T_STEPS, r)]),
                window_matrix(vac, [(T_STEPS, r)]))
            edge[r] = rel
            if r > cone:
                assert rel == "equal", \
                    f"deformation outside the cone at M={m}, r={r}"
        entry["cone_edge_single_cells"] = edge

        # 3. local visibility inside the cone
        singles = {}
        patches = {}
        for r in range(0, 61, 6):
            rel_s, _ = image_relation(
                window_matrix(hist, [(T_STEPS, r)]),
                window_matrix(vac, [(T_STEPS, r)]))
            singles[r] = rel_s
            cells = [(t, j) for t in (T_STEPS - 1, T_STEPS)
                     for j in (r, r + 1)]
            rel_p, d_p = image_relation(window_matrix(hist, cells),
                                        window_matrix(vac, cells))
            patches[r] = (rel_p, d_p if np.isfinite(d_p) else "inf")
        entry["single_cells_inside"] = singles
        entry["two_by_two_inside"] = patches

        # 4. extended row segments, the candidate field
        segments = {}
        for length in SEG_LENGTHS:
            row = []
            for r in range(-96, 97, 8):
                cells = [(T_STEPS, r + k) for k in range(length)]
                m_mat = window_matrix(hist, cells)
                m_vac = window_matrix(vac, cells)
                rel, d = image_relation(m_mat, m_vac)
                row.append({"r": r, "relation": rel,
                            "D_bits": d if np.isfinite(d) else "inf",
                            "H_vac": marginal_entropy_bits(m_vac),
                            "H_mat": marginal_entropy_bits(m_mat)})
            segments[str(length)] = row
        entry["row_segments"] = segments
        per_source[str(m)] = entry

    record["per_source"] = per_source

    # summary counts per relation type across the field windows
    summary = {}
    for m, entry in per_source.items():
        counts = {"equal": 0, "nested": 0, "escaped": 0}
        finite_d = []
        for rows in entry["row_segments"].values():
            for row in rows:
                counts[row["relation"]] += 1
                if row["relation"] == "nested":
                    finite_d.append(row["D_bits"])
        summary[m] = {"relation_counts": counts,
                      "finite_D_values": finite_d}
    record["field_summary"] = summary

    record["declared"] = {"ring": N_RING, "steps": T_STEPS,
                          "vacuum_rule": 90, "defect_rule": 150,
                          "sources": {str(k): sorted(v)
                                      for k, v in SOURCES.items()},
                          "segment_lengths": SEG_LENGTHS}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "eg2-matter.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    for m, s in summary.items():
        print(f"M={m}: relations {s['relation_counts']}, finite D "
              f"{s['finite_D_values'][:8]}")
    e1 = per_source["1"]
    print("cone edge (M=1):", e1["cone_edge_single_cells"])
    print("singles inside (M=1):",
          set(e1["single_cells_inside"].values()))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
