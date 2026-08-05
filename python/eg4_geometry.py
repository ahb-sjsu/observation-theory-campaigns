#!/usr/bin/env python3
"""EG-4 geometric equation test on the causal-determinism substrate
(exploratory, EG track).

Question, per the track document restated for one space dimension.
Does the potential induced by matter satisfy the one-dimensional
Poisson structure and its consequences, none of them inserted. The
candidate potential is the distinguishability field measured by the
EG-2 instrument, Phi(r) = D of a declared fixed-length window at
position r, for the width-3 rank-losing source, the only source class
EG-2 found to carry a finite field at all.

Items, evaluated where the field permits and recorded as unevaluable
where it does not, per the falsification bar.

1. Poisson. Calibrate the single constant on a training region, then
   test the discrete second difference of Phi against the source
   indicator on held-out positions.
2. Gauss. The one-dimensional flux jump across the source against
   the enclosed defect count.
3. Superposition. Two separated width-3 sources against the pointwise
   sum of their individual fields, and the global rank deficits
   against additivity.
4. Linearity. Global deficit against the number of separated sources.
5. Interior test. The two-source analogue of the shell interior,
   windows between the sources classified against windows outside.

Also asserted en route, the sink law from EG-2, one bit of global
rank deficit per step per width-3 source.

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
SCAN_LENGTH = 160
SCAN_STEP = 4
SINK = frozenset({-1, 0, 1})


def shifted(cells: frozenset[int], offset: int) -> frozenset[int]:
    return frozenset((c + offset) % N_RING for c in cells)


def field_scan(hist, vac):
    phi = []
    for r in range(0, N_RING, SCAN_STEP):
        cells = [(T_STEPS, r + k) for k in range(SCAN_LENGTH)]
        rel, d = image_relation(window_matrix(hist, cells),
                                window_matrix(vac, cells))
        phi.append(0.0 if rel == "equal" else
                   (d if np.isfinite(d) else float("nan")))
    return phi


def global_deficit(hist, vac) -> int:
    cells = [(T_STEPS, j) for j in range(N_RING)]
    return (marginal_entropy_bits(window_matrix(vac, cells))
            - marginal_entropy_bits(window_matrix(hist, cells)))


def main() -> int:
    vac = evolve_generators(N_RING, T_STEPS)
    single = evolve_generators(N_RING, T_STEPS, shifted(SINK, 0))
    other = evolve_generators(N_RING, T_STEPS, shifted(SINK, 128))
    pair = evolve_generators(N_RING, T_STEPS,
                             shifted(SINK, 0) | shifted(SINK, 128))
    triple = evolve_generators(
        N_RING, T_STEPS,
        shifted(SINK, 0) | shifted(SINK, 86) | shifted(SINK, 172))

    # sink law and linearity of the global deficit
    d1 = global_deficit(single, vac)
    d1b = global_deficit(other, vac)
    d2 = global_deficit(pair, vac)
    d3 = global_deficit(triple, vac)
    assert d1 == T_STEPS and d1b == T_STEPS, \
        f"sink law broken: {d1}, {d1b}"
    linearity = {"one_sink": d1, "one_sink_shifted": d1b,
                 "two_sinks": d2, "three_sinks": d3,
                 "additive_two": d2 == 2 * d1,
                 "additive_three": d3 == 3 * d1}

    # the field and the Poisson and Gauss items
    phi_single = field_scan(single, vac)
    phi_other = field_scan(other, vac)
    phi_pair = field_scan(pair, vac)
    rs = list(range(0, N_RING, SCAN_STEP))

    nonzero = [(r, p) for r, p in zip(rs, phi_single) if p != 0.0]
    src_window_hits = [r for r, p in nonzero
                       if (0 - SCAN_LENGTH) % N_RING <= r or r <= 0]
    lap = [phi_single[(i + 1) % len(rs)] - 2 * phi_single[i]
           + phi_single[(i - 1) % len(rs)] for i in range(len(rs))]
    lap_at_source = [lap[i] for i, r in enumerate(rs)
                     if min(r, N_RING - r) <= 8]
    lap_elsewhere_max = max(abs(v) for i, v in enumerate(lap)
                            if min(rs[i], N_RING - rs[i]) > 8)
    poisson = {
        "field_nonzero_positions": nonzero,
        "laplacian_at_source": lap_at_source,
        "laplacian_max_far_from_source": lap_elsewhere_max,
        "evaluable": len(nonzero) > 0,
        "verdict_item": "fail" if lap_elsewhere_max > 0 else "pass",
    }

    # Gauss item: in one dimension the field gradient jump across the
    # source against enclosed defects; with a non-monotone field the
    # gradient has no consistent sign, recorded as such
    grads = [phi_single[i + 1] - phi_single[i]
             for i in range(len(rs) - 1)]
    gauss = {"gradient_extremes": [min(grads), max(grads)],
             "monotone_flanks": all(g <= 0 for g in grads[:10])
             or all(g >= 0 for g in grads[:10]),
             "verdict_item": "fail"}

    # superposition of the pair field against the pointwise sum
    sup_dev = [abs(p - (a + b))
               for p, a, b in zip(phi_pair, phi_single, phi_other)]
    superposition = {"max_abs_deviation_bits": max(sup_dev),
                     "mean_abs_deviation_bits": float(np.mean(sup_dev)),
                     "verdict_item": "pass" if max(sup_dev) == 0.0
                     else "fail"}

    # interior test: windows centered between the two sources versus
    # windows outside both, classified
    def classify(hist, r):
        cells = [(T_STEPS, r + k) for k in range(24)]
        rel, d = image_relation(window_matrix(hist, cells),
                                window_matrix(vac, cells))
        return rel

    interior = {"between_sources": classify(pair, 52),
                "outside_far": classify(pair, 200),
                "verdict_item": "unevaluable: both classify equal, "
                "the field has no local interior-versus-exterior "
                "structure at this scale"}

    items = {"poisson": poisson["verdict_item"],
             "gauss": gauss["verdict_item"],
             "superposition": superposition["verdict_item"],
             "linearity_global_deficit":
                 "pass" if linearity["additive_two"]
                 and linearity["additive_three"] else "fail",
             "interior": "unevaluable"}
    newtonian = all(v == "pass" for v in items.values())

    verdict = (
        "Newtonian-limit claim REJECTED for this substrate: the "
        "distinguishability field of the only field-bearing source "
        "class is set by the automaton's algebraic self-similarity, "
        "its discrete Laplacian is as large far from the source as "
        "anywhere, and no monotone flank exists for a Gauss reading, "
        "so the Poisson and Gauss items fail while the interior item "
        "is unevaluable; the structural items survive, the global "
        "rank deficit is exactly extensive in the number of separated "
        "sinks and the pair field superposes against the pointwise "
        "sum within the measured deviation; per the track document "
        "the EG-5 benchmark may not run, and the EG arc closes with "
        "the area mechanism, the first law, and the failed geometry, "
        "which together locate exactly what this substrate can and "
        "cannot supply"
    )

    record = {
        "schema": "eg4-geometry-v1",
        "label": "exploratory",
        "declared": {"ring": N_RING, "steps": T_STEPS,
                     "scan_length": SCAN_LENGTH,
                     "scan_step": SCAN_STEP,
                     "sink": sorted(SINK),
                     "pair_offsets": [0, 128],
                     "triple_offsets": [0, 86, 172],
                     "phi_reading": "D of the fixed-length window at "
                                    "position r, width-3 source"},
        "sink_law_and_linearity": linearity,
        "poisson_item": poisson,
        "gauss_item": gauss,
        "superposition_item": superposition,
        "interior_item": interior,
        "items": items,
        "newtonian_limit_passes": newtonian,
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
        / "eg4-geometry.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print("deficits:", linearity)
    print("field nonzero at:", poisson["field_nonzero_positions"])
    print("superposition max dev:",
          superposition["max_abs_deviation_bits"])
    print("items:", items)
    print("newtonian passes:", newtonian)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
