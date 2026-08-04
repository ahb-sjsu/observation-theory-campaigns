#!/usr/bin/env python3
"""QO-0 finite-dimensional instrument for consumer-relative distinguishability.

Declared defaults (QO track open questions 4, 5, 10, resolved for this
instrument and recorded in the evidence):

- Divergence: Umegaki quantum relative entropy D(rho||sigma) =
  Tr rho (ln rho - ln sigma), in nats; bits are derived by /ln(2).
- The channel is the primitive object; algebra restriction enters only as
  the pinching channel (full computational-basis dephasing).
- Commuting embedding of the classical anchors: fiber branches ordered by
  increasing tau are the computational basis states, coarea weights are the
  eigenvalues of a diagonal density matrix, the uniform fiber I/d is the
  reference state, and the branch-label algebra is the diagonal algebra.
  Under this embedding S(rho) = log2(d) - D(rho || I/d)/ln 2 must reproduce
  the PE-0 branch entropies exactly (1 bit for P0, 1.5 bits for M0).

Model for the sweep: an 8-qubit transverse-field Ising chain in the gapped
paramagnetic phase, thermal reference state, matter as a local unitary
rotation. Consumer channels: partial trace over the inside region, local
dephasing on an outside qubit, pinching. Every DPI and composition margin
is a theorem; the instrument's job is to compute the objects the theorem
is about and expose implementation error.

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

LN2 = float(np.log(2.0))


# ---- instrument core -----------------------------------------------------

def relative_entropy(
    rho: np.ndarray,
    sigma: np.ndarray,
    *,
    support_floor: float = 1e-12,
    support_tol: float = 1e-10,
) -> float:
    """Umegaki relative entropy in nats; inf on support violation.

    Eigenvalues of sigma at or below support_floor are treated as outside
    its support; if rho puts more than support_tol mass there, the
    divergence is infinite by definition.
    """
    p, _ = np.linalg.eigh(rho)
    p = np.clip(p.real, 0.0, None)
    term1 = float(np.sum(p[p > 1e-300] * np.log(p[p > 1e-300])))

    s, v = np.linalg.eigh(sigma)
    s = np.clip(s.real, 0.0, None)
    weights = np.real(np.sum(v.conj() * (rho @ v), axis=0))
    kernel = s <= support_floor
    if float(weights[kernel].sum()) > support_tol:
        return float("inf")
    live = ~kernel
    term2 = float(np.sum(weights[live] * np.log(s[live])))
    return term1 - term2


def partial_trace(rho: np.ndarray, keep: list[int], n_qubits: int) -> np.ndarray:
    """Reduce an n-qubit density matrix to the sorted qubit subset kept."""
    keep = sorted(keep)
    rest = [i for i in range(n_qubits) if i not in keep]
    perm = keep + rest
    rho_t = rho.reshape([2] * (2 * n_qubits))
    rho_t = rho_t.transpose(perm + [i + n_qubits for i in perm])
    dk = 2 ** len(keep)
    dt = 2 ** len(rest)
    rho_t = rho_t.reshape(dk, dt, dk, dt)
    return np.einsum("aibi->ab", rho_t)


def dephase(rho: np.ndarray, qubit: int, n_qubits: int, strength: float) -> np.ndarray:
    """Local Z-dephasing channel (1-s) rho + s Z rho Z on one qubit."""
    z = np.array([[1.0, 0.0], [0.0, -1.0]])
    op = np.array([[1.0]])
    for k in range(n_qubits):
        op = np.kron(op, z if k == qubit else np.eye(2))
    return (1.0 - strength) * rho + strength * (op @ rho @ op)


def pinch(rho: np.ndarray) -> np.ndarray:
    """Full computational-basis pinching (the diagonal-algebra consumer)."""
    return np.diag(np.diag(rho))


def merge_branches(rho: np.ndarray, groups: list[list[int]]) -> np.ndarray:
    """Classical merging channel: Kraus |g><i| for each basis index i in
    group g. Collapses branch labels within each group; CPTP by
    construction when the groups partition the basis."""
    d_out = len(groups)
    out = np.zeros((d_out, d_out), dtype=complex)
    for g, members in enumerate(groups):
        for i in members:
            k = np.zeros((d_out, rho.shape[0]))
            k[g, i] = 1.0
            out += k @ rho @ k.T
    return out


# ---- model for the sweep -------------------------------------------------

def ising_hamiltonian_jh(n_qubits: int, coupling: float, field: float) -> np.ndarray:
    """Open-chain Ising H = -J sum ZZ - h sum X with both couplings free."""
    x = np.array([[0.0, 1.0], [1.0, 0.0]])
    z = np.array([[1.0, 0.0], [0.0, -1.0]])

    def site(op, k):
        full = np.array([[1.0]])
        for j in range(n_qubits):
            full = np.kron(full, op if j == k else np.eye(2))
        return full

    h = np.zeros((2**n_qubits, 2**n_qubits))
    for k in range(n_qubits - 1):
        h -= coupling * (site(z, k) @ site(z, k + 1))
    for k in range(n_qubits):
        h -= field * site(x, k)
    return h


def ising_hamiltonian(n_qubits: int, field: float) -> np.ndarray:
    return ising_hamiltonian_jh(n_qubits, 1.0, field)


def thermal_state(hamiltonian: np.ndarray, beta: float) -> np.ndarray:
    energies, vectors = np.linalg.eigh(hamiltonian)
    boltzmann = np.exp(-beta * (energies - energies.min()))
    boltzmann /= boltzmann.sum()
    return (vectors * boltzmann) @ vectors.conj().T


def local_rotation(n_qubits: int, qubit: int, theta: float, axis: str) -> np.ndarray:
    """exp(i theta P) for a single-site Pauli P on one qubit.

    Axis choice matters physically: the Ising thermal state's single-site
    reduced state is exactly (I + m X)/2 by the global spin-flip symmetry,
    so an X-axis rotation commutes with it and is invisible to a site-only
    consumer even though it acts on that consumer's own qubit. A Z-axis
    rotation is not absorbed. The sweep uses Z for the visible excitation
    and the invisibility of the X case is itself a symmetry null control.
    """
    pauli = {
        "x": np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex),
        "z": np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex),
    }[axis]
    full = np.array([[1.0]], dtype=complex)
    for j in range(n_qubits):
        full = np.kron(full, pauli if j == qubit else np.eye(2))
    dim = 2**n_qubits
    return np.cos(theta) * np.eye(dim) + 1j * np.sin(theta) * full


def local_x_rotation(n_qubits: int, qubit: int, theta: float) -> np.ndarray:
    return local_rotation(n_qubits, qubit, theta, "x")


def local_z_rotation(n_qubits: int, qubit: int, theta: float) -> np.ndarray:
    return local_rotation(n_qubits, qubit, theta, "z")


# ---- anchor and sweep runs -----------------------------------------------

def classical_anchors() -> dict:
    p0 = np.diag([0.5, 0.5])
    p0_bits = 1.0 - relative_entropy(p0, np.eye(2) / 2.0) / LN2
    assert abs(p0_bits - 1.0) < 1e-12
    assert np.allclose(pinch(p0), p0)

    m0 = np.diag([0.25, 0.5, 0.25])
    m0_bits = float(np.log2(3.0)) - relative_entropy(m0, np.eye(3) / 3.0) / LN2
    assert abs(m0_bits - 1.5) < 1e-12
    assert np.allclose(pinch(m0), m0)

    merged = merge_branches(m0, [[0, 2], [1]])
    merged_ref = merge_branches(np.eye(3) / 3.0, [[0, 2], [1]])
    d_full = relative_entropy(m0, np.eye(3) / 3.0)
    d_merged = relative_entropy(merged, merged_ref)
    assert d_merged <= d_full + 1e-12
    merged_bits = 1.0 - relative_entropy(merged, np.eye(2) / 2.0) / LN2
    assert abs(merged_bits - 1.0) < 1e-12

    return {
        "embedding": "branches by increasing tau as computational basis; "
                     "coarea weights as eigenvalues; uniform fiber as reference; "
                     "branch-label algebra as the diagonal algebra",
        "p0_bits": p0_bits,
        "m0_bits": m0_bits,
        "m0_merged_orientation_pair_bits": merged_bits,
        "dpi_margin_merge": d_full - d_merged,
    }


def closed_forms() -> dict:
    rng = np.random.RandomState(20260804)
    residuals = {}

    p = np.array([0.7, 0.2, 0.1])
    q = np.array([0.4, 0.4, 0.2])
    kl = float(np.sum(p * np.log(p / q)))
    residuals["commuting_kl"] = abs(relative_entropy(np.diag(p), np.diag(q)) - kl)

    plus = np.array([[0.5, 0.5], [0.5, 0.5]])
    residuals["pure_vs_maximally_mixed"] = abs(
        relative_entropy(plus, np.eye(2) / 2.0) - LN2
    )

    zero = np.diag([1.0, 0.0])
    one = np.diag([0.0, 1.0])
    residuals["support_violation_is_inf"] = (
        0.0 if relative_entropy(zero, one) == float("inf") else 1.0
    )

    a = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    rho = a @ a.conj().T
    rho /= np.trace(rho).real
    b = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    sigma = b @ b.conj().T
    sigma /= np.trace(sigma).real
    residuals["self_divergence"] = abs(relative_entropy(rho, rho))
    u, _ = np.linalg.qr(rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4)))
    residuals["unitary_invariance"] = abs(
        relative_entropy(u @ rho @ u.conj().T, u @ sigma @ u.conj().T)
        - relative_entropy(rho, sigma)
    )
    return residuals


def dpi_sweep() -> dict:
    """DPI, monotonicity, and floor-stability sweep on the Ising model.

    Design note (a real finding from the first version of this sweep): a
    unitary, or any CPTP map, acting only on the traced-out interior cannot
    change the exterior reduced state at all; that is the no-signalling
    theorem, and it made an interior-excitation sweep trivially degenerate
    (every consumer-side divergence exactly zero). The sweep therefore uses
    interior excitation as an exact NULL CONTROL, and generates nontrivial
    distinguishability by exciting a site the consumer can see, with the
    consumer hierarchy formed by shrinking the kept region toward that site.
    """
    n = 8
    outside = [4, 5, 6, 7]
    beta = 0.5
    field = 2.0
    hamiltonian = ising_hamiltonian(n, field)
    sigma = thermal_state(hamiltonian, beta)
    smallest_weight = float(np.linalg.eigvalsh(sigma).min())
    assert smallest_weight > 1e-9, \
        "thermal spectrum too close to the support floor: divergences " \
        "would go infinite for spectral, not physical, reasons"

    thetas = [0.1, 0.4, 0.8, 1.2]
    strengths = [0.1, 0.25, 0.5]
    margins = []
    monotone_defects = []
    composition_margins = []

    no_signalling = {}
    for site_label, site_index in (("deep_inside", 1), ("boundary_inside", 3)):
        u = local_x_rotation(n, site_index, 0.8)
        rho = u @ sigma @ u.conj().T
        d_out = relative_entropy(
            partial_trace(rho, outside, n), partial_trace(sigma, outside, n)
        )
        no_signalling[site_label] = d_out
        assert abs(d_out) < 1e-10, "no-signalling null control failed"

    symmetry_null = {}
    u = local_x_rotation(n, 4, 0.8)
    rho = u @ sigma @ u.conj().T
    symmetry_null["x_rotation_site_only"] = relative_entropy(
        partial_trace(rho, [4], n), partial_trace(sigma, [4], n)
    )
    assert abs(symmetry_null["x_rotation_site_only"]) < 1e-10, \
        "symmetry null control failed: X rotation should be invisible on-site"

    regions = [[4, 5, 6, 7], [4, 5, 6], [4, 5], [4]]
    region_divergences = {}
    for theta in thetas:
        u = local_z_rotation(n, 4, theta)
        rho = u @ sigma @ u.conj().T
        d_global = relative_entropy(rho, sigma)
        assert np.isfinite(d_global), \
            "global divergence infinite: support semantics misfired on a " \
            "full-rank pair"
        chain = [d_global]
        for keep in regions:
            chain.append(relative_entropy(
                partial_trace(rho, keep, n), partial_trace(sigma, keep, n)
            ))
        for larger, smaller in zip(chain[:-1], chain[1:], strict=False):
            margins.append(larger - smaller)
        region_divergences[str(theta)] = chain[1:]

        rho_pair = partial_trace(rho, [4, 5], n)
        sigma_pair = partial_trace(sigma, [4, 5], n)
        d_pair = relative_entropy(rho_pair, sigma_pair)
        previous = d_pair
        for s in strengths:
            d_s = relative_entropy(
                dephase(rho_pair, 0, 2, s), dephase(sigma_pair, 0, 2, s)
            )
            margins.append(d_pair - d_s)
            monotone_defects.append(d_s - previous)
            previous = d_s

        once = (dephase(rho_pair, 0, 2, 0.25), dephase(sigma_pair, 0, 2, 0.25))
        twice = (dephase(once[0], 0, 2, 0.25), dephase(once[1], 0, 2, 0.25))
        composition_margins.append(
            relative_entropy(*once) - relative_entropy(*twice)
        )
        margins.append(d_pair - relative_entropy(pinch(rho_pair), pinch(sigma_pair)))

    floor_values = [1e-14, 1e-13, 1e-12, 1e-11, 1e-10]
    u = local_z_rotation(n, 4, 0.8)
    rho = u @ sigma @ u.conj().T
    rho_out = partial_trace(rho, outside, n)
    sigma_out = partial_trace(sigma, outside, n)
    d_by_floor = [
        relative_entropy(rho_out, sigma_out, support_floor=f) for f in floor_values
    ]
    floor_spread = max(d_by_floor) - min(d_by_floor)

    reference_chain = region_divergences[str(0.8)]
    assert reference_chain[-1] > 1e-3, \
        "sweep degenerate: consumer sees nothing, model lacks structure"

    return {
        "model": {
            "n_qubits": n, "hamiltonian": "transverse-field Ising, open chain",
            "field": field, "beta": beta,
            "excitation": "exp(i theta Z) on qubit 4 (visible to the consumer)",
            "null_controls": "no-signalling: X rotation on interior qubits 1, 3; "
                             "symmetry: X rotation on qubit 4 invisible on-site",
            "consumer_regions": regions, "thetas": thetas,
            "dephasing_strengths": strengths,
        },
        "no_signalling_null_control": no_signalling,
        "symmetry_null_control": symmetry_null,
        "region_divergences_by_theta": region_divergences,
        "min_dpi_margin": float(min(margins)),
        "n_dpi_checks": len(margins),
        "max_dephasing_monotonicity_defect": float(max(monotone_defects)),
        "min_composition_margin": float(min(composition_margins)),
        "spectral_floor_values": floor_values,
        "spectral_floor_spread": float(floor_spread),
        "correlation_assistance_exploratory": {
            "d_keep_site_only": reference_chain[-1],
            "d_keep_full_outside": reference_chain[0],
            "assistance": reference_chain[0] - reference_chain[-1],
        },
    }


def main() -> int:
    anchors = classical_anchors()
    forms = closed_forms()
    sweep = dpi_sweep()

    assert max(forms.values()) < 1e-10, "closed-form residual too large"
    assert sweep["min_dpi_margin"] > -1e-10, "DPI violated beyond numerical floor"
    assert sweep["max_dephasing_monotonicity_defect"] < 1e-10
    assert sweep["min_composition_margin"] > -1e-10
    assert sweep["spectral_floor_spread"] < 1e-9

    record = {
        "schema": "qo0-instrument-v1",
        "label": "exploratory",
        "divergence": "umegaki-nats",
        "classical_anchors": anchors,
        "closed_form_residuals": forms,
        "dpi_sweep": sweep,
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
    output = Path(__file__).resolve().parents[1] / "results" / "qo0-instrument.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print(f"anchors: P0 {anchors['p0_bits']:.12f} bits, "
          f"M0 {anchors['m0_bits']:.12f} bits, "
          f"merged pair {anchors['m0_merged_orientation_pair_bits']:.12f} bits")
    print(f"closed forms: max residual {max(forms.values()):.3e}")
    print(f"DPI: min margin {sweep['min_dpi_margin']:.3e} over "
          f"{sweep['n_dpi_checks']} checks; "
          f"composition min {sweep['min_composition_margin']:.3e}; "
          f"floor spread {sweep['spectral_floor_spread']:.3e}")
    null = sweep["no_signalling_null_control"]
    print(f"no-signalling null control: deep {null['deep_inside']:.3e}, "
          f"boundary {null['boundary_inside']:.3e}")
    assist = sweep["correlation_assistance_exploratory"]
    print(f"correlation assistance (exploratory): site-only "
          f"D {assist['d_keep_site_only']:.6f} -> full-outside "
          f"D {assist['d_keep_full_outside']:.6f}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
