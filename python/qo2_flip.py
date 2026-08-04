#!/usr/bin/env python3
"""QO-2 gravitational flip: task-optimized versus fidelity-optimized encoding.

Hypothesis under test (QO track section 3): at a fixed budget, an encoding
optimized to preserve the declared flux functional predicts it better than
a global-fidelity-optimized encoding at matched budget, while having lower
global state fidelity.

Declared design (Level 0, fixed before any sweep):

- Model: the QO-0/1 outside region (4 qubits, sites 4..7 of the 8-qubit
  gapped Ising chain at beta 0.5), vacuum sigma_out. Scenario states apply
  a STRONG Z rotation on the fidelity-dominant site (site 6, reduced index
  2) and a WEAK Z rotation on the flux site (site 4, reduced index 0), so
  the fidelity signal and the task signal live on different qubits; this
  is the quantum analogue of the classical flip's misalignment between the
  read metric and the source covariance.
- Task functional: the QO-1 flux stand-in, transverse-field energy density
  f(rho) = Tr(rho * (-h X)) on the flux site. The area-response variant is
  deferred until the QO open question 3 declaration discipline is settled;
  this run instantiates the flip for the energy-flux consumer only.
- Encoder family (discrete, exhaustively searched, identical for every
  arm): keep a subset S of the 4 qubits with |S| = budget k; encode is the
  partial trace onto S; decode reattaches the vacuum marginals on the
  discarded qubits. Budget counts stored qubit slots.
- Arms, selected on the training grid only: F-arm minimizes mean
  infidelity 1 - F(rho, decode(encode(rho))); T-arm minimizes mean flux
  distortion |f(rho) - f(decode(encode(rho)))|; the anti-arm is the
  T-arm's encoder with the flux qubit Z-pinched before storage, which
  destroys the flux observable at identical budget (QO open question 7).
- Train and held-out scenario grids are disjoint in both angles; the flip
  verdict is read on held-out states only.

Exploratory label. No physics claim.
"""
from __future__ import annotations

import itertools
import json
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
    ising_hamiltonian,
    local_rotation,
    partial_trace,
    thermal_state,
)

N_FULL = 8
OUTSIDE = [4, 5, 6, 7]
M = 4
FLUX_QUBIT = 0
STRONG_QUBIT = 2
FIELD = 2.0
BETA = 0.5

TRAIN_STRONG = [0.6, 0.9, 1.2]
TRAIN_WEAK = [0.1, 0.2, 0.3]
HELD_STRONG = [0.75, 1.05]
HELD_WEAK = [0.15, 0.25]

TASK_MARGIN = 0.01
FIDELITY_MARGIN = 0.01


def hermitian_sqrt(rho: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(rho)
    values = np.clip(values.real, 0.0, None)
    return (vectors * np.sqrt(values)) @ vectors.conj().T


def uhlmann_fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    root = hermitian_sqrt(rho)
    inner = root @ sigma @ root
    values = np.clip(np.linalg.eigvalsh(inner).real, 0.0, None)
    return float(np.sqrt(values).sum() ** 2)


def reorder_qubits(rho: np.ndarray, order: list[int], n_qubits: int) -> np.ndarray:
    """Permute qubits so that current position i holds logical qubit order[i]."""
    inverse = [order.index(i) for i in range(n_qubits)]
    tensor = rho.reshape([2] * (2 * n_qubits))
    tensor = tensor.transpose(inverse + [i + n_qubits for i in inverse])
    dim = 2**n_qubits
    return tensor.reshape(dim, dim)


def encode_decode(
    rho: np.ndarray,
    keep: list[int],
    vacuum: np.ndarray,
    *,
    pinch_flux: bool = False,
) -> np.ndarray:
    """Keep the listed qubits, reattach vacuum marginals on the rest."""
    keep = sorted(keep)
    discard = [i for i in range(M) if i not in keep]
    kept = partial_trace(rho, keep, M)
    if pinch_flux and FLUX_QUBIT in keep:
        kept = dephase(kept, keep.index(FLUX_QUBIT), len(keep), 0.5)
    if discard:
        prior = partial_trace(vacuum, discard, M)
        combined = np.kron(kept, prior)
    else:
        combined = kept
    return reorder_qubits(combined, keep + discard, M)


def flux_value(rho: np.ndarray) -> float:
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    op = np.array([[1.0]], dtype=complex)
    for j in range(M):
        op = np.kron(op, x if j == FLUX_QUBIT else np.eye(2))
    return float(np.real(np.trace(rho @ (-FIELD * op))))


def scenario_states(vacuum: np.ndarray, strong: list[float], weak: list[float]):
    states = []
    for theta_strong, theta_weak in itertools.product(strong, weak):
        u = (
            local_rotation(M, STRONG_QUBIT, theta_strong, "z")
            @ local_rotation(M, FLUX_QUBIT, theta_weak, "z")
        )
        states.append(u @ vacuum @ u.conj().T)
    return states


def arm_distortions(states, keep, vacuum, *, pinch_flux=False):
    task, infidelity = [], []
    for rho in states:
        reconstructed = encode_decode(rho, keep, vacuum, pinch_flux=pinch_flux)
        task.append(abs(flux_value(rho) - flux_value(reconstructed)))
        infidelity.append(1.0 - uhlmann_fidelity(rho, reconstructed))
    return float(np.mean(task)), float(np.mean(infidelity))


def run_budget(k, train_states, held_states, vacuum) -> dict:
    subsets = [list(s) for s in itertools.combinations(range(M), k)]
    train = {
        tuple(s): arm_distortions(train_states, s, vacuum) for s in subsets
    }
    f_arm = list(min(train, key=lambda s: train[s][1]))
    t_arm = list(min(train, key=lambda s: train[s][0]))

    held = {
        "F": arm_distortions(held_states, f_arm, vacuum),
        "T": arm_distortions(held_states, t_arm, vacuum),
        "anti": arm_distortions(held_states, t_arm, vacuum, pinch_flux=True),
    }
    anti_train = arm_distortions(train_states, t_arm, vacuum, pinch_flux=True)
    interpretable = (
        anti_train[0] > max(train[tuple(f_arm)][0], train[tuple(t_arm)][0])
        and held["anti"][0] > max(held["F"][0], held["T"][0])
    )
    flip = (
        interpretable
        and held["T"][0] < held["F"][0] - TASK_MARGIN
        and held["T"][1] > held["F"][1] + FIDELITY_MARGIN
    )
    return {
        "budget_qubits": k,
        "f_arm_keeps": f_arm,
        "t_arm_keeps": t_arm,
        "arms_coincide": f_arm == t_arm,
        "training": {str(s): v for s, v in train.items()},
        "held_out": {
            arm: {"task_distortion": v[0], "infidelity": v[1]}
            for arm, v in held.items()
        },
        "anti_arm_interpretable": interpretable,
        "flip": flip,
    }


def main() -> int:
    sigma_full = thermal_state(ising_hamiltonian(N_FULL, FIELD), BETA)
    vacuum = partial_trace(sigma_full, OUTSIDE, N_FULL)
    train_states = scenario_states(vacuum, TRAIN_STRONG, TRAIN_WEAK)
    held_states = scenario_states(vacuum, HELD_STRONG, HELD_WEAK)

    budgets = [run_budget(k, train_states, held_states, vacuum) for k in (1, 2, 3)]
    assert all(b["anti_arm_interpretable"] for b in budgets), \
        "anti-arm not worst on task: declared functional does not govern " \
        "the task; run is uninterpretable"

    flip_region = [b["budget_qubits"] for b in budgets if b["flip"]]
    coincide_region = [b["budget_qubits"] for b in budgets if b["arms_coincide"]]

    record = {
        "schema": "qo2-flip-v1",
        "label": "exploratory",
        "declared": {
            "task": "transverse-field energy density -h X on the flux site; "
                    "area-response variant deferred pending open question 3",
            "budget": "stored qubit slots",
            "encoder_family": "keep-subset with vacuum-marginal decode; "
                              "exhaustive search, no optimizer",
            "anti_arm": "T-arm encoder with the flux qubit Z-pinched",
            "task_margin": TASK_MARGIN,
            "fidelity_margin": FIDELITY_MARGIN,
            "train_grid": [TRAIN_STRONG, TRAIN_WEAK],
            "held_grid": [HELD_STRONG, HELD_WEAK],
        },
        "budgets": budgets,
        "flip_region": flip_region,
        "arms_coincide_region": coincide_region,
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
    output = Path(__file__).resolve().parents[1] / "results" / "qo2-flip.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    for b in budgets:
        held = b["held_out"]
        print(f"k={b['budget_qubits']}: F keeps {b['f_arm_keeps']} "
              f"(task {held['F']['task_distortion']:.4f}, "
              f"infid {held['F']['infidelity']:.4f}); "
              f"T keeps {b['t_arm_keeps']} "
              f"(task {held['T']['task_distortion']:.4f}, "
              f"infid {held['T']['infidelity']:.4f}); "
              f"anti task {held['anti']['task_distortion']:.4f}; "
              f"flip={b['flip']} coincide={b['arms_coincide']}")
    print(f"flip region: {flip_region}; arms coincide: {coincide_region}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
