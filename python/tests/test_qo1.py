import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from qo0_instrument import (  # noqa: E402
    ising_hamiltonian,
    local_rotation,
    merge_branches,
    relative_entropy,
    thermal_state,
)
from qo1_hierarchy import (  # noqa: E402
    LEVELS,
    classical_anchors,
    hierarchy_chain,
    pinch_qubits,
)


def test_qo1_sufficiency_equality_anchor():
    m0 = np.diag([0.25, 0.5, 0.25])
    uniform = np.eye(3) / 3.0
    groups = [[0, 2], [1]]
    d_full = relative_entropy(m0, uniform)
    d_merged = relative_entropy(
        merge_branches(m0, groups), merge_branches(uniform, groups)
    )
    assert abs(d_full - d_merged) < 1e-12
    assert abs(d_full - (math.log(3.0) - 1.5 * math.log(2.0))) < 1e-12


def test_qo1_nonzero_gap_anchor():
    anchors = classical_anchors()
    expected = 0.25 * math.log(2.0) - 0.5 * math.log(4.0 / 3.0)
    assert abs(anchors["nonzero_gap"]["gap"] - expected) < 1e-12
    assert anchors["nonzero_gap"]["gap"] > 0.02


def test_qo1_pinch_qubits_is_idempotent_projection():
    rng = np.random.RandomState(7)
    a = rng.standard_normal((8, 8)) + 1j * rng.standard_normal((8, 8))
    rho = a @ a.conj().T
    rho /= np.trace(rho).real
    once = pinch_qubits(rho, [0, 1, 2], 3)
    twice = pinch_qubits(once, [0, 1, 2], 3)
    assert np.allclose(once, twice, atol=1e-14)
    assert np.allclose(once, np.diag(np.diag(once)), atol=1e-14)


def test_qo1_ordering_and_sector_dependence_small_model():
    n = 4
    outside = [2, 3]
    sigma = thermal_state(ising_hamiltonian(n, 2.0), 1.0)

    u = local_rotation(n, 2, 0.7, "z")
    chain_z = hierarchy_chain(u @ sigma @ u.conj().T, sigma, outside, n)
    for weaker, stronger in zip(LEVELS[:-1], LEVELS[1:], strict=False):
        assert chain_z[weaker] <= chain_z[stronger] + 1e-10
    assert abs(chain_z["position_only"]) < 1e-10
    assert chain_z["position_plus_flux"] > 1e-3

    u = local_rotation(n, 2, 0.7, "x")
    chain_x = hierarchy_chain(u @ sigma @ u.conj().T, sigma, outside, n)
    for weaker, stronger in zip(LEVELS[:-1], LEVELS[1:], strict=False):
        assert chain_x[weaker] <= chain_x[stronger] + 1e-10
    assert chain_x["position_only"] > 1e-6
