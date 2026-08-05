#!/usr/bin/env python3
"""TB-3 theorem verification: the Pauli-rotation exactness law.

THEOREM (proved; proof in TYPE-III-BRIDGE.md, algebraic core
formalized in proofs/PauliRotation.lean). Let rho be a full-rank
density matrix, P a Hermitian involution (P^2 = I), and
U(theta) = exp(i theta P). Then for every theta

  S( U rho U^dagger || rho ) = sin^2(theta) * S( P rho P || rho ).

Proof, in three steps. First, since P^2 = I,
U = cos(theta) I + i sin(theta) P, so

  U rho U^dagger = cos^2 rho + sin^2 P rho P
                   + i sin cos (P rho - rho P).

Second, von Neumann entropy is unitarily invariant, so the relative
entropy reduces to S(theta) = tr[(rho - U rho U^dagger) log rho].
Third, the cross term vanishes identically because rho commutes with
its own logarithm, tr[(P rho - rho P) log rho] = tr[P (rho log rho
- log rho rho)] = 0 by cyclicity. What remains is
S(theta) = sin^2(theta) tr[(rho - P rho P) log rho], and the
coefficient is itself S(P rho P || rho) because P rho P is unitarily
related to rho. No symmetry of rho is used anywhere.

COROLLARIES. (a) For any window W containing the support of P, the
reduction commutes with U, so S_W(theta) = kappa_W sin^2(theta)
exactly with kappa_W = S(P rho_W P || rho_W). (b) The Kubo-Mori form
equals kappa_W, by matching Taylor coefficients at theta = 0. (c) The
lambda fitted in TB-3 is the pure kinematic constant
sum theta^2 sin^2 theta / sum theta^4 of the declared grid, which is
why it was measured constant to thirteen digits across all eighty
window-and-coupling combinations, and QO-3's theta^2-law residuals
were the universal sin^2-versus-theta^2 mismatch.

This runner is the verification instrument. Part one checks the
theorem on seeded random full-rank states and random involutions far
outside the Ising family, at large angles including pi/2. Part two
checks corollary (a) and (b) on the campaign's Ising window. Part
three checks corollary (c) against the committed TB-3 evidence
record, with no refit.

Label: proved (theorem), with this instrument as the numerical
witness and the Lean file as the machine-checked algebraic core.
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
    ising_hamiltonian_jh,
    partial_trace,
    relative_entropy,
    thermal_state,
)
from tb3_wedge import kubo_mori_form, pauli_site  # noqa: E402

SEED = 20260807
DIMS = [4, 6, 8, 16]
CASES_PER_DIM = 5
THETA_TEST = [0.3, 0.7, 1.0, math.pi / 2, 2.0, -0.4]
EXACTNESS_BAR = 1e-11
ISING = {"N": 8, "J": 1.0, "h": 2.0, "beta": 0.4,
         "window": [1, 2, 3, 4, 5], "site": 3}
QO3_THETAS = [0.05, 0.1, 0.15, 0.2]


def random_state(rng, dim: int) -> np.ndarray:
    g = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
    _, vecs = np.linalg.eigh(g + g.conj().T)
    p = rng.dirichlet(np.ones(dim) * 2.0)
    return (vecs * p) @ vecs.conj().T


def random_involution(rng, dim: int) -> np.ndarray:
    g = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
    _, vecs = np.linalg.eigh(g + g.conj().T)
    signs = rng.choice([-1.0, 1.0], size=dim)
    if np.all(signs == signs[0]):
        signs[0] = -signs[0]
    return (vecs * signs) @ vecs.conj().T


def rotate(rho: np.ndarray, p_op: np.ndarray, theta: float) -> np.ndarray:
    dim = rho.shape[0]
    u = math.cos(theta) * np.eye(dim) + 1j * math.sin(theta) * p_op
    return u @ rho @ u.conj().T


def main() -> int:
    rng = np.random.RandomState(SEED)

    # Part one: the theorem on random states and involutions.
    worst = 0.0
    n_checks = 0
    for dim in DIMS:
        for _ in range(CASES_PER_DIM):
            rho = random_state(rng, dim)
            p_op = random_involution(rng, dim)
            assert np.max(np.abs(p_op @ p_op - np.eye(dim))) < 1e-12
            kappa = relative_entropy(p_op @ rho @ p_op, rho)
            for theta in THETA_TEST:
                s = relative_entropy(rotate(rho, p_op, theta), rho)
                err = abs(s - math.sin(theta) ** 2 * kappa) / max(kappa, 1e-30)
                worst = max(worst, err)
                n_checks += 1
    assert worst < EXACTNESS_BAR, f"exactness violated: {worst}"

    # Part two: corollaries (a) and (b) on the campaign's Ising window.
    sigma = thermal_state(
        ising_hamiltonian_jh(ISING["N"], ISING["J"], ISING["h"]),
        ISING["beta"])
    sigma_w = partial_trace(sigma, ISING["window"], ISING["N"])
    p_full = pauli_site(ISING["N"], ISING["site"])
    idx = ISING["window"].index(ISING["site"])
    p_w = pauli_site(len(ISING["window"]), idx)
    kappa_w = relative_entropy(p_w @ sigma_w @ p_w, sigma_w)
    worst_model = 0.0
    for theta in THETA_TEST:
        rho_w = partial_trace(rotate(sigma, p_full, theta),
                              ISING["window"], ISING["N"])
        s = relative_entropy(rho_w, sigma_w)
        worst_model = max(worst_model,
                          abs(s - math.sin(theta) ** 2 * kappa_w) / kappa_w)
    assert worst_model < EXACTNESS_BAR, \
        f"model exactness violated: {worst_model}"
    drho_w = partial_trace(1j * (p_full @ sigma - sigma @ p_full),
                           ISING["window"], ISING["N"])
    q_w = kubo_mori_form(sigma_w, drho_w)
    kubo_defect = abs(q_w - kappa_w) / kappa_w
    assert kubo_defect < 1e-10, f"Kubo-Mori vs kappa: {kubo_defect}"

    # Part three: corollary (c) against the committed TB-3 record.
    lam_kinematic = (sum(t**2 * math.sin(t) ** 2 for t in QO3_THETAS)
                     / sum(t**4 for t in QO3_THETAS))
    tb3 = json.loads((Path(__file__).resolve().parents[1] / "results"
                      / "tb3-wedge.json").read_text())
    lams = [w["lambda_modular"] for p in tb3["coupling_points"]
            for w in p["windows"].values()]
    lam_dev = max(abs(v - lam_kinematic) for v in lams)
    assert lam_dev < 1e-10, f"kinematic lambda mismatch: {lam_dev}"
    probe_kinematic = math.sin(0.02) ** 2 / 0.02**2
    probes = [w["probe_ratio"] for p in tb3["coupling_points"]
              for w in p["windows"].values()]
    probe_dev = max(abs(v - probe_kinematic) for v in probes)
    assert probe_dev < 1e-9, f"kinematic probe mismatch: {probe_dev}"

    record = {
        "schema": "tb3-theorem-v1",
        "label": "proved",
        "theorem": "S(exp(i theta P) rho exp(-i theta P) || rho) = "
                   "sin^2(theta) S(P rho P || rho) for full-rank rho "
                   "and Hermitian involution P",
        "declared": {"seed": SEED, "dims": DIMS,
                     "cases_per_dim": CASES_PER_DIM,
                     "theta_test": THETA_TEST,
                     "exactness_bar": EXACTNESS_BAR,
                     "ising_instance": ISING,
                     "qo3_thetas": QO3_THETAS},
        "part1_random": {"checks": n_checks,
                         "worst_relative_error": worst},
        "part2_model": {"kappa_window": kappa_w,
                        "kubo_mori_Q": q_w,
                        "worst_relative_error": worst_model,
                        "kubo_vs_kappa_relative": kubo_defect},
        "part3_kinematics": {"lambda_kinematic": lam_kinematic,
                             "max_lambda_deviation": lam_dev,
                             "probe_kinematic": probe_kinematic,
                             "max_probe_deviation": probe_dev},
        "statement": "the thirteen-digit constancy of TB-3's lambda is "
            "a theorem, not a coincidence: relative entropy under a "
            "Hermitian-involution rotation is exactly sin^2(theta) "
            "times the involution defect S(P rho P || rho), the "
            "Kubo-Mori form equals that defect, and the fitted lambda "
            "is a pure kinematic constant of the declared grid",
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
    output = Path(__file__).resolve().parents[1] / "results" \
        / "tb3-theorem.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"part1: {n_checks} random checks, worst {worst:.3e}")
    print(f"part2: kappa {kappa_w:.12f}, Q {q_w:.12f}, "
          f"worst {worst_model:.3e}, kubo defect {kubo_defect:.3e}")
    print(f"part3: lambda* {lam_kinematic:.13f}, max dev {lam_dev:.3e}, "
          f"probe* {probe_kinematic:.10f}, max dev {probe_dev:.3e}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
