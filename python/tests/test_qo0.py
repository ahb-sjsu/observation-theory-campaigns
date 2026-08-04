import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from qo0_instrument import (  # noqa: E402
    classical_anchors,
    closed_forms,
    dephase,
    ising_hamiltonian,
    local_x_rotation,
    merge_branches,
    partial_trace,
    pinch,
    relative_entropy,
    thermal_state,
)

LN2 = math.log(2.0)


def test_qo0_classical_anchor_p0_is_one_bit_via_divergence():
    p0 = np.diag([0.5, 0.5])
    bits = 1.0 - relative_entropy(p0, np.eye(2) / 2.0) / LN2
    assert abs(bits - 1.0) < 1e-12
    assert np.allclose(pinch(p0), p0)


def test_qo0_classical_anchor_m0_is_three_halves_bits_via_divergence():
    m0 = np.diag([0.25, 0.5, 0.25])
    bits = math.log2(3.0) - relative_entropy(m0, np.eye(3) / 3.0) / LN2
    assert abs(bits - 1.5) < 1e-12


def test_qo0_merging_orientation_pair_returns_the_fold_bit():
    m0 = np.diag([0.25, 0.5, 0.25])
    merged = merge_branches(m0, [[0, 2], [1]])
    assert np.allclose(merged, np.diag([0.5, 0.5]))
    bits = 1.0 - relative_entropy(merged, np.eye(2) / 2.0) / LN2
    assert abs(bits - 1.0) < 1e-12
    d_full = relative_entropy(m0, np.eye(3) / 3.0)
    d_merged = relative_entropy(merged, merge_branches(np.eye(3) / 3.0, [[0, 2], [1]]))
    assert d_merged <= d_full + 1e-12


def test_qo0_anchor_runner_passes():
    anchors = classical_anchors()
    assert abs(anchors["p0_bits"] - 1.0) < 1e-12
    assert abs(anchors["m0_bits"] - 1.5) < 1e-12
    assert anchors["dpi_margin_merge"] >= -1e-12


def test_qo0_closed_forms_within_tolerance():
    residuals = closed_forms()
    assert max(residuals.values()) < 1e-10


def test_qo0_support_violation_is_infinite():
    zero = np.diag([1.0, 0.0])
    one = np.diag([0.0, 1.0])
    assert relative_entropy(zero, one) == float("inf")
    assert relative_entropy(one, zero) == float("inf")


def test_qo0_partial_trace_recovers_product_factors():
    a = np.diag([0.3, 0.7])
    plus = np.array([[0.5, 0.5], [0.5, 0.5]])
    c = np.diag([0.9, 0.1])
    rho = np.kron(a, np.kron(plus, c))
    assert np.allclose(partial_trace(rho, [0], 3), a, atol=1e-12)
    assert np.allclose(partial_trace(rho, [1, 2], 3), np.kron(plus, c), atol=1e-12)


def test_qo0_no_signalling_null_control():
    n = 4
    sigma = thermal_state(ising_hamiltonian(n, 2.0), 1.0)
    u = local_x_rotation(n, 1, 0.7)
    rho = u @ sigma @ u.conj().T
    d_out = relative_entropy(
        partial_trace(rho, [2, 3], n), partial_trace(sigma, [2, 3], n)
    )
    assert abs(d_out) < 1e-10
    assert relative_entropy(rho, sigma) > 1e-3


def test_qo0_dpi_on_small_model_with_visible_excitation():
    n = 4
    sigma = thermal_state(ising_hamiltonian(n, 2.0), 1.0)
    u = local_x_rotation(n, 2, 0.7)
    rho = u @ sigma @ u.conj().T
    d_global = relative_entropy(rho, sigma)
    rho_out = partial_trace(rho, [2, 3], n)
    sigma_out = partial_trace(sigma, [2, 3], n)
    d_traced = relative_entropy(rho_out, sigma_out)
    assert 1e-3 < d_traced <= d_global + 1e-10
    d_site = relative_entropy(
        partial_trace(rho, [2], n), partial_trace(sigma, [2], n)
    )
    assert d_site <= d_traced + 1e-10
    d_dephased = relative_entropy(
        dephase(rho_out, 0, 2, 0.3), dephase(sigma_out, 0, 2, 0.3)
    )
    assert d_dephased <= d_traced + 1e-10
    d_pinched = relative_entropy(pinch(rho_out), pinch(sigma_out))
    assert d_pinched <= d_traced + 1e-10
