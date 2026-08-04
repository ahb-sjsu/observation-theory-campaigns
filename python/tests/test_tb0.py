import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from qo0_instrument import (  # noqa: E402
    ising_hamiltonian_jh,
    local_rotation,
    partial_trace,
    relative_entropy,
    thermal_state,
)
from tb0_modular import (  # noqa: E402
    araki_relative_entropy,
    functional_state_on_subalgebra,
)


def test_tb0_araki_equals_umegaki_closed_forms():
    p = np.diag([0.7, 0.2, 0.1])
    q = np.diag([0.4, 0.4, 0.2])
    kl = float(np.sum(np.diag(p) * np.log(np.diag(p) / np.diag(q))))
    assert abs(araki_relative_entropy(p, q) - kl) < 1e-12
    plus = np.array([[0.5, 0.5], [0.5, 0.5]])
    assert abs(
        araki_relative_entropy(plus, np.eye(2) / 2) - math.log(2.0)
    ) < 1e-12
    assert araki_relative_entropy(np.diag([1.0, 0.0]),
                                  np.diag([0.0, 1.0])) == float("inf")


def test_tb0_araki_equals_umegaki_on_random_pair():
    rng = np.random.RandomState(17)
    a = rng.standard_normal((6, 6)) + 1j * rng.standard_normal((6, 6))
    rho = a @ a.conj().T
    rho /= np.trace(rho).real
    b = rng.standard_normal((6, 6)) + 1j * rng.standard_normal((6, 6))
    sigma = b @ b.conj().T
    sigma /= np.trace(sigma).real
    assert abs(
        araki_relative_entropy(rho, sigma) - relative_entropy(rho, sigma)
    ) < 1e-10


def test_tb0_functional_route_matches_partial_trace():
    n = 4
    sigma = thermal_state(ising_hamiltonian_jh(n, 1.0, 2.0), 0.5)
    u = local_rotation(n, 2, 0.7, "z")
    rho = u @ sigma @ u.conj().T
    for keep in ([2, 3], [2]):
        via_fn = functional_state_on_subalgebra(rho, keep, n)
        via_pt = partial_trace(rho, keep, n)
        assert np.max(np.abs(via_fn - via_pt)) < 1e-12
