"""XPROTO-QUANTUM family (F-QUANTUM): consumer-relative reliability of a quantum
device certificate -- the QC twin of AICSI/portfolio (benchmark vs application)
and geo-fleet nearest-certified backend selection.

A device carries an AGGREGATE certificate (average gate fidelity / a quantum-
volume-style pass): "this backend is good." That certificate is blind to the
circuit FOOTPRINT. On a heterogeneous device (a drifted/bad qubit among good
ones), a circuit that touches the bad qubit fails despite the certified device --
a false-clear. A consumer-aware certificate reads the per-qubit calibration for
the footprint (P_C = the qubits/gates the circuit uses) and clears per circuit.

Witness = the actual mirror-circuit success under a real qiskit-aer noise model
(a mirror circuit returns |0...0> ideally; success = P(all zeros) under noise).
Consumer-aware prediction reads the same per-qubit calibration the device already
publishes -- footprint-relative, not aggregate.

  mode "aer": qiskit-aer noise model (this substrate). Sealed rung = real IBM
              hardware. Emits QUANTUMREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed device + cell constants ----------------------------------
N_QUBITS = 8
BAD_QUBITS = {3}
ERR1_GOOD = 1e-3            # good single-qubit depolarizing rate
ERR1_BAD = 1.2e-1          # a drifted/bad qubit
ERR2 = 6e-3               # two-qubit (cx) rate (good pairs)
FOOTPRINT_SIZE = 3
DEPTH = 6
K_FOOTPRINTS = 40          # circuits sampled per seed
SHOTS = 2000
TAU_SUCC = 0.70            # a circuit "succeeds" if mirror success >= this
F_TARGET = 0.95            # aggregate device certification threshold
SINGLE_GATES = ["h", "x", "y", "s"]


def err1(q):
    return ERR1_BAD if q in BAD_QUBITS else ERR1_GOOD


def device_noise_model():
    nm = NoiseModel()
    ones = ["h", "x", "y", "z", "s", "sdg", "rx", "ry", "rz", "u"]
    for q in range(N_QUBITS):
        nm.add_quantum_error(depolarizing_error(err1(q), 1), ones, [q])
    for a in range(N_QUBITS):
        for b in range(N_QUBITS):
            if a != b:
                e = ERR2 * (8 if (a in BAD_QUBITS or b in BAD_QUBITS) else 1)
                nm.add_quantum_error(depolarizing_error(min(e, 0.5), 2), ["cx"], [a, b])
    return nm


def aggregate_fidelity():
    return 1.0 - np.mean([err1(q) for q in range(N_QUBITS)])   # device-wide cert


def predicted_success(footprint):
    """Consumer-aware cert: read the per-qubit calibration for the footprint."""
    p = 1.0
    for q in footprint:
        p *= (1 - err1(q)) ** (2 * DEPTH)          # fwd + inverse single-q gates
    p *= (1 - ERR2) ** (2 * DEPTH)                  # a cx per layer, fwd+inverse
    return p


def mirror_circuit(footprint, rng):
    qc = QuantumCircuit(N_QUBITS, len(footprint))
    ops = []
    for _ in range(DEPTH):
        for q in footprint:
            g = rng.choice(SINGLE_GATES); getattr(qc, g)(q); ops.append((g, q))
        for k in range(0, len(footprint) - 1, 2):
            a, b = footprint[k], footprint[k + 1]; qc.cx(a, b); ops.append(("cx", a, b))
    qc.barrier(footprint)                            # stop the transpiler folding fwd*inv away
    for op in reversed(ops):                         # exact inverse -> ideal |0..0>
        if op[0] == "cx":
            qc.cx(op[1], op[2])
        elif op[0] == "s":
            qc.sdg(op[1])
        else:
            getattr(qc, op[0])(op[1])               # h,x,y self-inverse
    qc.measure(footprint, range(len(footprint)))
    return qc


def run_cell(seed):
    rng = np.random.default_rng(seed)
    sim = AerSimulator(noise_model=device_noise_model())
    device_cert = aggregate_fidelity() >= F_TARGET   # naive: device certified?
    naive_fc = aware_fc = 0
    good_ok = good_n = 0
    for _ in range(K_FOOTPRINTS):
        fp = sorted(rng.choice(N_QUBITS, FOOTPRINT_SIZE, replace=False).tolist())
        qc = mirror_circuit(fp, rng)
        counts = sim.run(transpile(qc, sim, optimization_level=0),
                         shots=SHOTS).result().get_counts()
        success = counts.get("0" * len(fp), 0) / SHOTS      # witness
        failed = success < TAU_SUCC
        aware_clear = predicted_success(fp) >= TAU_SUCC
        if device_cert and failed:
            naive_fc += 1                            # naive clears all -> false-clear
        if aware_clear and failed:
            aware_fc += 1                            # aware mis-clear
        if not (set(fp) & BAD_QUBITS):               # a good footprint
            good_n += 1; good_ok += (success >= TAU_SUCC)
    n = K_FOOTPRINTS
    return {
        "seed": int(seed), "mode": "aer",
        "device_certified": bool(device_cert),
        "aggregate_fidelity": round(float(aggregate_fidelity()), 5),
        "naive_fc": round(naive_fc / n, 4), "aware_fc": round(aware_fc / n, 4),
        "good_footprint_success_rate": round(good_ok / max(1, good_n), 4),
        "n_footprints": n, "target_success": TAU_SUCC,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "QUANTUMREP-family.json"))
    args = ap.parse_args()
    cells = [run_cell(s) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: device_cert={c['device_certified']} "
              f"(agg_fid={c['aggregate_fidelity']}) | naive_fc={c['naive_fc']} "
              f"aware_fc={c['aware_fc']} | good-fp success={c['good_footprint_success_rate']}",
              flush=True)
    rec = {"family": "F-QUANTUM", "mode": "aer",
           # aer with a hand-constructed heterogeneous device is MODEL validation,
           # not evidence. The sealed rung requires real IBM hardware (prereg).
           "sim_is_model_validation_not_evidence": True,
           "constants": {"n_qubits": N_QUBITS, "bad_qubits": sorted(BAD_QUBITS),
                         "err1_good": ERR1_GOOD, "err1_bad": ERR1_BAD, "err2": ERR2,
                         "footprint_size": FOOTPRINT_SIZE, "depth": DEPTH,
                         "target_success": TAU_SUCC, "f_target": F_TARGET,
                         "substrate": "qiskit-aer heterogeneous depolarizing noise model; "
                                      "mirror-circuit witness; sealed rung = real IBM hardware"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
