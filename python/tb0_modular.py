#!/usr/bin/env python3
"""TB-0 modular instrument (exploratory, TYPE-III-BRIDGE track).

Two routes to relative entropy that generalize to type III von Neumann
algebras, implemented on the campaign's finite models and cross-checked
against the sealed Umegaki instrument (PEQO-FREEZE-002, bar B5).

Route 1, the relative modular operator. In the standard (doubled) form,
Delta_{sigma|rho} acts as left multiplication by sigma and right
multiplication by rho^{-1}, the GNS vector of rho is vec(rho^{1/2}),
and the Araki formula

  S(rho || sigma) = -( Psi_rho, log Delta_{sigma|rho} Psi_rho )

must equal the spectral Umegaki value exactly in type I. The relative
modular operator is the object that survives the passage to type III;
density matrices are its type I shadow.

Route 2, states as expectation functionals on a subalgebra. The
consumer's reduced state is assembled purely from expectations of the
subalgebra's matrix units, phi(E_ij), with no partial-trace primitive
anywhere; the restricted relative entropy is then computed from the
assembled A-states by Route 1. This is the states-on-algebras reading
that survives verbatim in type III, demonstrated concretely.

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
    ising_hamiltonian_jh,
    local_rotation,
    partial_trace,
    relative_entropy,
    thermal_state,
)

AGREEMENT_BAR = 1e-10


def araki_relative_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Route 1: -(Psi_rho, log Delta_{sigma|rho} Psi_rho) via spectra.

    With eigendecompositions rho = U_r diag(r) U_r^dagger and
    sigma = U_s diag(s) U_s^dagger, and M = U_s^dagger rho^{1/2} U_r,
    the Araki value is sum_ij |M_ij|^2 (log r_j - log s_i), which is
    evaluated without forming any d^2 x d^2 operator. Infinite when rho
    has weight outside the support of sigma.
    """
    r_vals, r_vecs = np.linalg.eigh(rho)
    s_vals, s_vecs = np.linalg.eigh(sigma)
    r_vals = np.clip(r_vals.real, 0.0, None)
    s_vals = np.clip(s_vals.real, 0.0, None)
    sqrt_rho = (r_vecs * np.sqrt(r_vals)) @ r_vecs.conj().T
    m = s_vecs.conj().T @ sqrt_rho @ r_vecs
    weights = np.abs(m) ** 2

    live_r = r_vals > 1e-300
    kernel_s = s_vals <= 1e-12
    if float(weights[kernel_s][:, live_r].sum()) > 1e-10:
        return float("inf")

    log_r = np.where(live_r, np.log(np.where(live_r, r_vals, 1.0)), 0.0)
    log_s = np.where(~kernel_s, np.log(np.where(~kernel_s, s_vals, 1.0)), 0.0)
    total = 0.0
    for i in range(len(s_vals)):
        if kernel_s[i]:
            continue
        row = weights[i]
        total += float(np.sum(row * (log_r - log_s[i])))
    return total


def matrix_units(dim: int):
    for i in range(dim):
        for j in range(dim):
            e = np.zeros((dim, dim), dtype=complex)
            e[i, j] = 1.0
            yield i, j, e


def functional_state_on_subalgebra(
    rho: np.ndarray, keep: list[int], n_qubits: int
) -> np.ndarray:
    """Route 2: assemble the consumer state from expectations
    phi(E_ij tensor I) of the subalgebra's matrix units. No partial
    trace is invoked; the state exists because the functional does."""
    keep = sorted(keep)
    dim = 2 ** len(keep)
    rest = [q for q in range(n_qubits) if q not in keep]
    dim_rest = 2 ** len(rest)
    state = np.zeros((dim, dim), dtype=complex)
    for i, j, e in matrix_units(dim):
        big = np.kron(e, np.eye(dim_rest))
        big = _reorder(big, keep + rest, n_qubits)
        state[i, j] = np.trace(rho @ big)
    return state.conj()  # phi(E_ij) = rho_A[j, i]; conjugate transpose fix


def _reorder(op: np.ndarray, order: list[int], n_qubits: int) -> np.ndarray:
    inverse = [order.index(q) for q in range(n_qubits)]
    tensor = op.reshape([2] * (2 * n_qubits))
    tensor = tensor.transpose(inverse + [q + n_qubits for q in inverse])
    dim = 2**n_qubits
    return tensor.reshape(dim, dim)


def main() -> int:
    checks = {}

    p = np.diag([0.7, 0.2, 0.1])
    q = np.diag([0.4, 0.4, 0.2])
    kl = float(np.sum(np.diag(p) * np.log(np.diag(p) / np.diag(q))))
    checks["commuting_kl_vs_araki"] = abs(araki_relative_entropy(p, q) - kl)

    plus = np.array([[0.5, 0.5], [0.5, 0.5]])
    checks["pure_vs_mixed_vs_araki"] = abs(
        araki_relative_entropy(plus, np.eye(2) / 2) - math.log(2.0)
    )

    n = 8
    outside = [4, 5, 6, 7]
    sigma_full = thermal_state(ising_hamiltonian_jh(n, 1.0, 2.0), 0.5)
    u = local_rotation(n, 4, 0.8, "z")
    rho_full = u @ sigma_full @ u.conj().T

    umegaki_global = relative_entropy(rho_full, sigma_full)
    araki_global = araki_relative_entropy(rho_full, sigma_full)
    checks["global_umegaki_vs_araki"] = abs(umegaki_global - araki_global)

    sweep = {}
    for label, keep in (("outside4", outside), ("pair", [4, 5]),
                        ("site", [4])):
        rho_pt = partial_trace(rho_full, keep, n)
        sigma_pt = partial_trace(sigma_full, keep, n)
        umegaki = relative_entropy(rho_pt, sigma_pt)

        rho_fn = functional_state_on_subalgebra(rho_full, keep, n)
        sigma_fn = functional_state_on_subalgebra(sigma_full, keep, n)
        state_gap = float(np.max(np.abs(rho_fn - rho_pt)))
        araki_fn = araki_relative_entropy(rho_fn, sigma_fn)

        sweep[label] = {
            "umegaki_via_partial_trace": umegaki,
            "araki_via_functionals": araki_fn,
            "route_disagreement": abs(umegaki - araki_fn),
            "functional_vs_trace_state_gap": state_gap,
        }

    rho_deph = dephase(partial_trace(rho_full, [4, 5], n), 0, 2, 0.25)
    sigma_deph = dephase(partial_trace(sigma_full, [4, 5], n), 0, 2, 0.25)
    checks["dephased_umegaki_vs_araki"] = abs(
        relative_entropy(rho_deph, sigma_deph)
        - araki_relative_entropy(rho_deph, sigma_deph)
    )

    near = np.diag([0.5 + 5e-13, 0.5 - 5e-13])
    ref = np.eye(2) / 2
    checks["near_degenerate_stability"] = abs(
        araki_relative_entropy(near, ref) - relative_entropy(near, ref)
    )

    worst = max(
        [v for v in checks.values()]
        + [entry["route_disagreement"] for entry in sweep.values()]
        + [entry["functional_vs_trace_state_gap"] for entry in sweep.values()]
    )
    assert worst < AGREEMENT_BAR, f"TB-0 agreement bar failed: {worst:.3e}"

    record = {
        "schema": "tb0-modular-v1",
        "label": "exploratory",
        "agreement_bar": AGREEMENT_BAR,
        "closed_form_checks": checks,
        "consumer_sweep": sweep,
        "worst_disagreement": worst,
        "statement": "the relative modular route and the "
            "states-as-functionals route reproduce the sealed Umegaki "
            "instrument on the campaign models; the objects that survive "
            "the passage to type III agree with their type I shadows at "
            "machine precision",
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
    output = Path(__file__).resolve().parents[1] / "results" / "tb0-modular.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"closed forms: {', '.join(f'{k} {v:.2e}' for k, v in checks.items())}")
    for label, entry in sweep.items():
        print(f"{label}: routes agree to "
              f"{entry['route_disagreement']:.2e}, state gap "
              f"{entry['functional_vs_trace_state_gap']:.2e}")
    print(f"worst disagreement {worst:.3e} (bar {AGREEMENT_BAR})")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
