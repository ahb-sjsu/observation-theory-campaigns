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
from qo3_family import fit_quadratic_through_origin  # noqa: E402


def test_qo3_quadratic_fit_recovers_exact_law():
    thetas = [0.05, 0.1, 0.15, 0.2]
    values = [3.7 * t**2 for t in thetas]
    lam, residual = fit_quadratic_through_origin(thetas, values)
    assert abs(lam - 3.7) < 1e-12
    assert residual < 1e-12


def test_qo3_divergence_is_quadratic_at_small_theta():
    n = 4
    sigma = thermal_state(ising_hamiltonian_jh(n, 1.0, 2.0), 0.4)
    wedge = [1, 2, 3]
    sigma_w = partial_trace(sigma, wedge, n)

    def d(theta):
        u = local_rotation(n, 1, theta, "z")
        rho = u @ sigma @ u.conj().T
        return relative_entropy(partial_trace(rho, wedge, n), sigma_w)

    ratio = d(0.1) / d(0.05)
    assert abs(ratio - 4.0) < 0.1


def test_qo3_wedge_blindness_null():
    n = 4
    sigma = thermal_state(ising_hamiltonian_jh(n, 1.0, 2.0), 0.4)
    u = local_rotation(n, 0, 0.3, "z")
    rho = u @ sigma @ u.conj().T
    wedge = [1, 2, 3]
    d = relative_entropy(
        partial_trace(rho, wedge, n), partial_trace(sigma, wedge, n)
    )
    assert abs(d) < 1e-10


def test_qo3_lambda_depends_on_couplings():
    n = 4
    thetas = [0.05, 0.1, 0.15, 0.2]
    lambdas = []
    for j, h in ((0.6, 1.6), (1.2, 2.2)):
        sigma = thermal_state(ising_hamiltonian_jh(n, j, h), 0.4)
        wedge = [1, 2, 3]
        sigma_w = partial_trace(sigma, wedge, n)
        values = []
        for theta in thetas:
            u = local_rotation(n, 1, theta, "z")
            rho = u @ sigma @ u.conj().T
            values.append(
                relative_entropy(partial_trace(rho, wedge, n), sigma_w)
            )
        lam, residual = fit_quadratic_through_origin(thetas, values)
        assert residual < 0.1
        lambdas.append(lam)
    assert abs(lambdas[0] - lambdas[1]) > 1e-3
