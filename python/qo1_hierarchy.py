#!/usr/bin/env python3
"""QO-1 consumer hierarchy: nested observer algebras, lawful ordering, gaps.

The hierarchy is realized as a degradation chain of channels, so the
ordering D_{A_1} <= D_{A_2} <= D_{A_3} <= D_{A_4} is a theorem (each weaker
consumer is a channel applied to the stronger one's output) and any
measured inversion is an implementation bug:

  A_4 full state        identity
  A_3 full boundary     partial trace over the interior
  A_2 position + flux   Z-pinch on all outside sites except the excited
                        one, whose full single-site algebra is kept; the
                        declared flux stand-in is the transverse-field
                        energy density -h X on that site (QO open
                        question 8: declared, not derived)
  A_1 position only     Z-pinch on every outside site (classical joint
                        Z distribution)

Two excitation axes probe where the distinction lives:
  Z-rotation: commutes with every Z-string, so the position-only consumer
  sees exactly nothing (a commutation theorem, asserted); the distinction
  enters at the flux rung. A position certificate is vacuous for this
  excitation.
  X-rotation: invisible to the single site by the state's spin-flip
  symmetry, but visible in position correlations, so the position-only
  consumer already sees it. The largest gap moves with the sector.

Classical anchors (closed form, asserted):
  Sufficiency equality: for the M0 weights (1/4, 1/2, 1/4) against the
  uniform fiber, merging the orientation pair loses exactly nothing
  (conditional distributions inside the merged group match), so the DPI
  gap is exactly zero: an exact equality case, not just an inequality.
  Nonzero gap: against the asymmetric reference (1/2, 1/4, 1/4) the same
  merge loses exactly ln2/4 - ln(4/3)/2 nats.

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
from qo0_instrument import (  # noqa: E402
    dephase,
    ising_hamiltonian,
    local_rotation,
    merge_branches,
    partial_trace,
    relative_entropy,
    thermal_state,
)

LEVELS = ["position_only", "position_plus_flux", "full_boundary", "full_state"]


def pinch_qubits(rho: np.ndarray, qubits: list[int], n_qubits: int) -> np.ndarray:
    """Z-basis pinching of the listed qubits (full dephasing, s = 1/2)."""
    out = rho
    for q in qubits:
        out = dephase(out, q, n_qubits, 0.5)
    return out


def hierarchy_pairs(
    rho: np.ndarray,
    sigma: np.ndarray,
    outside: list[int],
    n_qubits: int,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """The four consumer-level state pairs, built once per excitation."""
    m = len(outside)
    rho_out = partial_trace(rho, outside, n_qubits)
    sigma_out = partial_trace(sigma, outside, n_qubits)
    rest = list(range(1, m))
    everything = list(range(m))
    return {
        "full_state": (rho, sigma),
        "full_boundary": (rho_out, sigma_out),
        "position_plus_flux": (
            pinch_qubits(rho_out, rest, m), pinch_qubits(sigma_out, rest, m)
        ),
        "position_only": (
            pinch_qubits(rho_out, everything, m),
            pinch_qubits(sigma_out, everything, m),
        ),
    }


def hierarchy_chain(
    rho: np.ndarray,
    sigma: np.ndarray,
    outside: list[int],
    n_qubits: int,
    *,
    support_floor: float = 1e-12,
) -> dict[str, float]:
    """The four-level divergence chain for one state pair."""
    pairs = hierarchy_pairs(rho, sigma, outside, n_qubits)
    return {
        level: relative_entropy(a, b, support_floor=support_floor)
        for level, (a, b) in pairs.items()
    }


def classical_anchors() -> dict:
    m0 = np.diag([0.25, 0.5, 0.25])
    uniform = np.eye(3) / 3.0
    groups = [[0, 2], [1]]
    d_full = relative_entropy(m0, uniform)
    d_merged = relative_entropy(
        merge_branches(m0, groups), merge_branches(uniform, groups)
    )
    sufficiency_gap = d_full - d_merged
    assert abs(d_full - (math.log(3.0) - 1.5 * math.log(2.0))) < 1e-12
    assert abs(sufficiency_gap) < 1e-12, "orientation merge should be sufficient"

    asymmetric = np.diag([0.5, 0.25, 0.25])
    d_full_2 = relative_entropy(m0, asymmetric)
    d_merged_2 = relative_entropy(
        merge_branches(m0, groups), merge_branches(asymmetric, groups)
    )
    gap_2 = d_full_2 - d_merged_2
    expected_full = 0.25 * math.log(2.0)
    expected_gap = 0.25 * math.log(2.0) - 0.5 * math.log(4.0 / 3.0)
    assert abs(d_full_2 - expected_full) < 1e-12
    assert abs(gap_2 - expected_gap) < 1e-12

    return {
        "sufficiency_equality": {
            "d_full": d_full,
            "d_merged": d_merged,
            "gap": sufficiency_gap,
            "statement": "orientation label carries zero distinguishing "
                         "information for the symmetric pair: exact DPI equality",
        },
        "nonzero_gap": {
            "d_full": d_full_2,
            "d_merged": d_merged_2,
            "gap": gap_2,
            "expected_gap": expected_gap,
        },
    }


def quantum_hierarchies() -> dict:
    n = 8
    outside = [4, 5, 6, 7]
    beta = 0.5
    field = 2.0
    sigma = thermal_state(ising_hamiltonian(n, field), beta)
    smallest_weight = float(np.linalg.eigvalsh(sigma).min())
    assert smallest_weight > 1e-9, \
        "thermal spectrum too close to the support floor"
    thetas = [0.4, 0.8, 1.2]

    results = {}
    for axis in ("z", "x"):
        per_theta = {}
        for theta in thetas:
            u = local_rotation(n, 4, theta, axis)
            rho = u @ sigma @ u.conj().T
            chain = hierarchy_chain(rho, sigma, outside, n)
            assert all(np.isfinite(v) for v in chain.values()), \
                f"infinite divergence in chain ({axis}, theta={theta})"
            for weaker, stronger in zip(LEVELS[:-1], LEVELS[1:], strict=False):
                assert chain[weaker] <= chain[stronger] + 1e-10, \
                    f"hierarchy inversion at {weaker} ({axis}, theta={theta})"
            gaps = {
                f"{stronger}-{weaker}": chain[stronger] - chain[weaker]
                for weaker, stronger in zip(LEVELS[:-1], LEVELS[1:], strict=False)
            }
            largest = max(gaps, key=gaps.get)
            per_theta[str(theta)] = {
                "chain": chain, "gaps": gaps, "largest_gap": largest,
            }
        results[axis] = per_theta

    reference = results["z"]["0.8"]["chain"]
    assert reference["position_only"] < 1e-10, \
        "Z excitation must be exactly invisible to the position-only consumer"
    assert reference["position_plus_flux"] > 1e-3, \
        "flux rung degenerate: excitation invisible where it must be visible"
    x_reference = results["x"]["0.8"]["chain"]
    assert x_reference["position_only"] > 1e-6, \
        "X excitation should reach the position-only consumer via correlations"

    floors = [1e-14, 1e-13, 1e-12, 1e-11, 1e-10]
    u = local_rotation(n, 4, 0.8, "z")
    rho = u @ sigma @ u.conj().T
    pairs = hierarchy_pairs(rho, sigma, outside, n)
    spreads = []
    for level in LEVELS:
        a, b = pairs[level]
        values = [relative_entropy(a, b, support_floor=f) for f in floors]
        spreads.append(max(values) - min(values))
    floor_spread = float(max(spreads))
    assert floor_spread < 1e-9

    return {
        "model": {
            "n_qubits": n, "field": field, "beta": beta, "outside": outside,
            "excited_site": 4, "thetas": thetas,
            "flux_standin": "transverse-field energy density -h X on site 4 "
                            "(declared, QO open question 8)",
        },
        "hierarchies": results,
        "spectral_floor_spread": floor_spread,
    }


def main() -> int:
    anchors = classical_anchors()
    quantum = quantum_hierarchies()

    record = {
        "schema": "qo1-hierarchy-v1",
        "label": "exploratory",
        "divergence": "umegaki-nats",
        "levels": LEVELS,
        "classical_anchors": anchors,
        "quantum": quantum,
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
    output = Path(__file__).resolve().parents[1] / "results" / "qo1-hierarchy.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    suff = anchors["sufficiency_equality"]
    print(f"classical anchors: sufficiency gap {suff['gap']:.3e} (exact equality); "
          f"nonzero gap {anchors['nonzero_gap']['gap']:.12f} "
          f"(expected {anchors['nonzero_gap']['expected_gap']:.12f})")
    for axis in ("z", "x"):
        entry = quantum["hierarchies"][axis]["0.8"]
        chain = entry["chain"]
        print(f"{axis}-excitation chain (nats): "
              f"pos {chain['position_only']:.6f} <= "
              f"pos+flux {chain['position_plus_flux']:.6f} <= "
              f"boundary {chain['full_boundary']:.6f} <= "
              f"full {chain['full_state']:.6f}; "
              f"largest gap: {entry['largest_gap']}")
    print(f"floor spread: {quantum['spectral_floor_spread']:.3e}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
