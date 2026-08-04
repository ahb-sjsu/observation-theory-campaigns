#!/usr/bin/env python3
"""TB-1 scaling ladder (exploratory, TYPE-III-BRIDGE track).

Chains of N = 4..12 sites, transverse-field Ising at (J, h) = (1, 2),
thermal reference at beta = 0.5, cut at half chain, excitation exp(i
theta Z) at the first kept site (the cut boundary), theta = 0.8. The
thesis under test: consumer-relative RELATIVE quantities converge as N
grows, while the absolute entropy of the kept half diverges (thermal
entropy is extensive), included deliberately as the diverging control.

Per rung: restricted relative entropy of excitation versus vacuum for
three consumers (the excited site, the boundary pair, the kept half),
the global relative entropy (N <= 10, where dense eigensolves stay
cheap), the von Neumann entropy of the kept half of the vacuum, and
the TB-0 route cross-checks (Araki-modular everywhere; the
states-as-functionals route at N <= 8 where matrix-unit assembly is
affordable). The Z excitation is diagonal, so it applies elementwise
and the ladder needs no dense 4096x4096 unitary conjugation.

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
    ising_hamiltonian_jh,
    partial_trace,
    relative_entropy,
    thermal_state,
)
from tb0_modular import (  # noqa: E402
    araki_relative_entropy,
    functional_state_on_subalgebra,
)

J_COUPLING = 1.0
H_FIELD = 2.0
BETA = 0.5
THETA = 0.8
LADDER = [4, 6, 8, 10, 12]
GLOBAL_D_MAX_N = 10
FUNCTIONAL_MAX_N = 8
ROUTE_BAR = 1e-10


def z_diagonal(n_qubits: int, qubit: int) -> np.ndarray:
    """Diagonal of the Pauli Z on one site, as a length-2^n vector."""
    pattern = np.array([1.0, -1.0])
    diag = np.array([1.0])
    for k in range(n_qubits):
        diag = np.kron(diag, pattern if k == qubit else np.ones(2))
    return diag


def excite(sigma: np.ndarray, n_qubits: int, qubit: int,
           theta: float) -> np.ndarray:
    """exp(i theta Z_qubit) sigma exp(-i theta Z_qubit), elementwise."""
    phase = np.exp(1j * theta * z_diagonal(n_qubits, qubit))
    return (phase[:, None] * sigma) * phase.conj()[None, :]


def von_neumann_entropy(rho: np.ndarray) -> float:
    vals = np.clip(np.linalg.eigvalsh(rho).real, 0.0, None)
    live = vals > 1e-300
    return float(-(vals[live] * np.log(vals[live])).sum())


def rung(n: int) -> dict:
    cut = n // 2
    kept = list(range(cut, n))
    site = cut
    sigma = thermal_state(ising_hamiltonian_jh(n, J_COUPLING, H_FIELD), BETA)
    rho = excite(sigma, n, site, THETA)

    consumers = {
        "site": [site],
        "pair": [site, site + 1] if site + 1 < n else [site],
        "half": kept,
    }
    out = {"N": n, "cut": cut, "excited_site": site}
    for label, keep in consumers.items():
        rho_c = partial_trace(rho, keep, n)
        sigma_c = partial_trace(sigma, keep, n)
        umegaki = relative_entropy(rho_c, sigma_c)
        araki = araki_relative_entropy(rho_c, sigma_c)
        assert abs(umegaki - araki) < ROUTE_BAR, \
            f"Araki route disagreement at N={n}, {label}"
        entry = {"D": umegaki, "araki_gap": abs(umegaki - araki)}
        if n <= FUNCTIONAL_MAX_N:
            rho_fn = functional_state_on_subalgebra(rho, keep, n)
            sigma_fn = functional_state_on_subalgebra(sigma, keep, n)
            d_fn = araki_relative_entropy(rho_fn, sigma_fn)
            assert abs(umegaki - d_fn) < ROUTE_BAR, \
                f"functional route disagreement at N={n}, {label}"
            entry["functional_gap"] = abs(umegaki - d_fn)
        out[label] = entry

    if n <= GLOBAL_D_MAX_N:
        out["global_D"] = relative_entropy(rho, sigma)

    out["half_entropy_vacuum"] = von_neumann_entropy(
        partial_trace(sigma, kept, n)
    )
    return out


def main() -> int:
    rungs = [rung(n) for n in LADDER]
    for r in rungs:
        print(f"N={r['N']}: D_site {r['site']['D']:.6f}, "
              f"D_pair {r['pair']['D']:.6f}, D_half {r['half']['D']:.6f}, "
              f"global {r.get('global_D', float('nan')):.6f}, "
              f"S_half {r['half_entropy_vacuum']:.4f}")

    def diffs(key_path):
        values = []
        for r in rungs:
            v = r
            for k in key_path:
                v = v[k] if not isinstance(k, str) or k in v else None
                if v is None:
                    break
            values.append(v)
        values = [v for v in values if v is not None]
        return values, [abs(b - a) for a, b in zip(values[:-1], values[1:],
                                                   strict=False)]

    analysis = {}
    for label in ("site", "pair", "half"):
        values, deltas = diffs([label, "D"])
        analysis[label] = {"values": values, "successive_diffs": deltas,
                           "converging": deltas[-1] < deltas[0]}
    s_values = [r["half_entropy_vacuum"] for r in rungs]
    s_deltas = [b - a for a, b in zip(s_values[:-1], s_values[1:],
                                      strict=False)]
    slope = float(np.polyfit(LADDER, s_values, 1)[0])
    analysis["half_entropy_control"] = {
        "values": s_values, "successive_increments": s_deltas,
        "linear_slope_per_site_pair": slope,
        "diverging": all(d > 0.1 for d in s_deltas),
    }

    assert analysis["site"]["converging"], "site-consumer D not converging"
    assert analysis["pair"]["converging"], "pair-consumer D not converging"
    assert analysis["half_entropy_control"]["diverging"], \
        "the diverging control failed to diverge"

    record = {
        "schema": "tb1-ladder-v1",
        "label": "exploratory",
        "declared": {"J": J_COUPLING, "h": H_FIELD, "beta": BETA,
                     "theta": THETA, "ladder": LADDER,
                     "global_D_max_N": GLOBAL_D_MAX_N,
                     "functional_max_N": FUNCTIONAL_MAX_N,
                     "route_bar": ROUTE_BAR},
        "rungs": rungs,
        "analysis": analysis,
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
    output = Path(__file__).resolve().parents[1] / "results" / "tb1-ladder.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    for label in ("site", "pair", "half"):
        a = analysis[label]
        print(f"{label}: values {[round(v, 6) for v in a['values']]}, "
              f"diffs {[f'{d:.2e}' for d in a['successive_diffs']]}, "
              f"converging {a['converging']}")
    c = analysis["half_entropy_control"]
    print(f"S_half control: {[round(v, 3) for v in c['values']]}, "
          f"slope {c['linear_slope_per_site_pair']:.4f}/site-pair, "
          f"diverging {c['diverging']}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
