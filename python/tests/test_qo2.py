import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from qo0_instrument import dephase, partial_trace  # noqa: E402
from qo2_flip import (  # noqa: E402
    encode_decode,
    reorder_qubits,
    uhlmann_fidelity,
)


def test_qo2_uhlmann_closed_forms():
    rng = np.random.RandomState(11)
    a = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    rho = a @ a.conj().T
    rho /= np.trace(rho).real
    assert abs(uhlmann_fidelity(rho, rho) - 1.0) < 1e-10

    psi = np.array([1.0, 0.0])
    phi = np.array([1.0, 1.0]) / math.sqrt(2.0)
    overlap = abs(np.vdot(psi, phi)) ** 2
    assert abs(
        uhlmann_fidelity(np.outer(psi, psi), np.outer(phi, phi)) - overlap
    ) < 1e-10

    p = np.array([0.7, 0.3])
    q = np.array([0.4, 0.6])
    classical = float(np.sqrt(p * q).sum() ** 2)
    assert abs(uhlmann_fidelity(np.diag(p), np.diag(q)) - classical) < 1e-10


def test_qo2_reorder_roundtrip():
    rng = np.random.RandomState(3)
    parts = []
    for _ in range(3):
        a = rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2))
        m = a @ a.conj().T
        parts.append(m / np.trace(m).real)
    a, b, c = parts
    scrambled = np.kron(b, np.kron(c, a))
    restored = reorder_qubits(scrambled, [1, 2, 0], 3)
    assert np.allclose(restored, np.kron(a, np.kron(b, c)), atol=1e-12)


def test_qo2_encode_decode_identity_at_full_budget():
    rng = np.random.RandomState(5)
    a = rng.standard_normal((16, 16)) + 1j * rng.standard_normal((16, 16))
    rho = a @ a.conj().T
    rho /= np.trace(rho).real
    vacuum = np.eye(16) / 16.0
    reconstructed = encode_decode(rho, [0, 1, 2, 3], vacuum)
    assert np.allclose(reconstructed, rho, atol=1e-12)


def test_qo2_two_qubit_analytic_flip_control():
    """A hand-sized flip no optimizer can fake: the fidelity signal and the
    task signal live on different qubits, and one stored qubit forces the
    choice between them."""
    single = (np.eye(2) + 0.9 * np.array([[0.0, 1.0], [1.0, 0.0]])) / 2.0
    vacuum = np.kron(single, single)

    def z_rot(theta):
        z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
        return np.cos(theta) * np.eye(2) + 1j * np.sin(theta) * z

    u = np.kron(z_rot(1.2), z_rot(0.25))
    rho = u @ vacuum @ u.conj().T

    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    task_op = np.kron(np.eye(2), x)

    def task(state):
        return float(np.real(np.trace(state @ task_op)))

    def reconstruct(keep, pinch_task=False):
        kept = partial_trace(rho, [keep], 2)
        if pinch_task and keep == 1:
            kept = dephase(kept, 0, 1, 0.5)
        prior = partial_trace(vacuum, [1 - keep], 2)
        combined = np.kron(kept, prior)
        return reorder_qubits(combined, [keep, 1 - keep], 2)

    arms = {}
    for keep in (0, 1):
        rec = reconstruct(keep)
        arms[keep] = (
            abs(task(rho) - task(rec)), 1.0 - uhlmann_fidelity(rho, rec)
        )
    f_arm = min(arms, key=lambda k: arms[k][1])
    t_arm = min(arms, key=lambda k: arms[k][0])
    assert f_arm == 0 and t_arm == 1

    anti = reconstruct(1, pinch_task=True)
    anti_task = abs(task(rho) - task(anti))
    assert anti_task > max(arms[0][0], arms[1][0])

    assert arms[t_arm][0] < arms[f_arm][0] - 0.01
    assert arms[t_arm][1] > arms[f_arm][1] + 0.01
