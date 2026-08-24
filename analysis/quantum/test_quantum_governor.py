"""Tests for governor.quantum: the governed backend reads calibration, routes each
circuit to the best footprint (avoiding the bad qubit), and certifies honestly --
so a calibration-blind placement that false-clears is replaced by one that holds.

    python test_quantum_governor.py
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from fam_quantum import (N_QUBITS, BAD_QUBITS, ERR2, DEPTH, device_noise_model,
                         err1, SINGLE_GATES)
from quantum_governor import Calibration, GovernedBackend, mirror_success

WIDTH = 3
TARGET = 0.70


def _calibration():
    single_q = {q: err1(q) for q in range(N_QUBITS)}
    two_q = {frozenset({a, b}): ERR2 * (8 if (a in BAD_QUBITS or b in BAD_QUBITS) else 1)
             for a in range(N_QUBITS) for b in range(a + 1, N_QUBITS)}
    return Calibration.from_errors(single_q, two_q, {}, N_QUBITS)


def _backend():
    return GovernedBackend(AerSimulator(noise_model=device_noise_model()),
                           _calibration(), target_success=TARGET)


def _mirror(width, rng):
    qc = QuantumCircuit(width, width)
    ops = []
    for _ in range(DEPTH):
        for q in range(width):
            g = rng.choice(SINGLE_GATES); getattr(qc, g)(q); ops.append((g, q))
        for k in range(0, width - 1, 2):
            qc.cx(k, k + 1); ops.append(("cx", k, k + 1))
    qc.barrier()
    for op in reversed(ops):
        if op[0] == "cx":
            qc.cx(op[1], op[2])
        elif op[0] == "s":
            qc.sdg(op[1])
        else:
            getattr(qc, op[0])(op[1])
    qc.measure(range(width), range(width))
    return qc


def test_best_layout_avoids_bad_qubit():
    g = _backend()
    layout = g.best_layout(WIDTH)
    assert not (set(layout) & BAD_QUBITS), layout          # never routes onto q3
    assert len(set(layout)) == WIDTH
    print(f"  best_layout({WIDTH}) = {layout} (bad qubits {sorted(BAD_QUBITS)} avoided)")


def test_certificate_is_consumer_relative():
    g = _backend()
    rng = np.random.default_rng(0)
    qc = _mirror(WIDTH, rng)
    good = g.certify(qc, [0, 1, 2], consumer_relative=True)
    bad = g.certify(qc, [3, 1, 2], consumer_relative=True)      # includes the bad qubit
    agg = g.certify(qc, [3, 1, 2], consumer_relative=False)     # naive aggregate cert
    assert good.cleared and not bad.cleared                      # footprint cert sees it
    assert agg.cleared                                           # aggregate cert is blind
    assert good.predicted_success > bad.predicted_success
    print(f"  footprint cert: good={good.predicted_success:.3f}(clear) "
          f"bad={bad.predicted_success:.3f}(vacuous) | aggregate blind={agg.cleared}")


def test_governed_beats_naive_placement():
    """Batch: naive calibration-blind (random) placement false-clears; the governed
    backend routes to the best footprint and holds -- same bars as XPROTO-QUANTUM."""
    g = _backend()
    rng = np.random.default_rng(7)
    naive_fc = gov_fc = 0
    K = 30
    for _ in range(K):
        qc = _mirror(WIDTH, rng)
        rand = sorted(rng.choice(N_QUBITS, WIDTH, replace=False).tolist())
        rn = g.run(qc, shots=2000, govern=False, layout=rand)    # blind placement
        rg = g.run(qc, shots=2000, govern=True)                  # governed
        naive_fail = mirror_success(rn.counts, WIDTH) < TARGET
        gov_fail = mirror_success(rg.counts, WIDTH) < TARGET
        naive_fc += rn.certificate.cleared and naive_fail        # cleared but failed
        gov_fc += rg.certificate.cleared and gov_fail
    naive_fc /= K; gov_fc /= K
    print(f"  naive_fc={naive_fc:.3f} (aggregate cert + blind layout) | "
          f"governed_fc={gov_fc:.3f} (footprint cert + best layout)")
    assert naive_fc >= 0.25, naive_fc
    assert gov_fc <= 0.10, gov_fc


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for t in tests:
        t(); print("PASS", t.__name__)
    print(f"\nAll {len(tests)} governor.quantum tests passed.")
