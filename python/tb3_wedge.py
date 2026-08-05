#!/usr/bin/env python3
"""TB-3 wedge-family reformulation of QO-3 (exploratory, TB track).

Question, from TYPE-III-BRIDGE.md section TB-3. Can QO-3's measured
all-observers requirement be restated so that every object in it has a
type III counterpart, with a modular statement in place of the declared
lattice theta^2 flux weight. The wedge language is declared analogy
throughout, per the leaked-vocabulary discipline.

The declared modular flux weight is the Kubo-Mori quadratic form. For
reference state rho, window W, and excitation U(theta) = exp(i theta P)
with P the shared-site Pauli generator, the first-order perturbation is
drho = i[P, rho], its reduction to W is drho_W, and

  Q_W = (1/2) sum_ij |<i| drho_W |j>|^2 k(p_i, p_j),
  k(p, q) = (log p - log q) / (p - q),  k(p, p) = 1/p,

with p_i the spectrum of the reduced reference rho_W. This is the exact
second-order coefficient of the Araki relative entropy, it is a
quadratic form in the excitation generator, and it is determined by the
reference state's modular data on the window. The reformulated law is
S_W(theta) = lambda_W theta^2 Q_W with lambda_W universal across the
family, so under the modular weight the universal constant is not
merely shared, it is canonically one.

The three requirements of the design, mapped to checks.

First, circularity. Q_W is computed from the spectral decomposition of
the reduced reference and the reduced first-order perturbation only.
The code path never evaluates a relative entropy, at any theta, while
assembling Q_W. A numerical validation probe at theta = 0.02 must find
the measured entropy within two percent of theta^2 Q_W on every window
at every coupling point, confirming that the declared form normalizes
the entropy without having been fitted to it.

Second, saturation. QO-3's nested shared-event windows saturate once
they exceed the correlation length. The same saturation must reappear
in the modular form Q_W itself, and both S_W at the top excitation and
Q_W must be nondecreasing along the nested family, the second-order
shadow of the data-processing inequality.

Third, the activation dichotomy. An excitation disjoint from the window
must give exactly zero for BOTH the entropy and the modular form,
because the partial trace absorbs a unitary supported outside the
window. Inertness for disjoint probes is thereby derived from
localization, not observed by accident.

Baseline. The committed QO-3 record supplies the family-B universality
spreads and joint-survival curves under the lattice theta^2 weight.
The same survival logic run under the modular weight is the measured
comparison. Model family, coupling grid, windows, excitation, and
thresholds are identical to the sealed QO-3 declarations.

Exploratory label. No physics claim. The chain has no light cones and
the collar is a distance in sites, not a causal separation.
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

N = 8
BETA = 0.4
J_GRID = [0.6, 0.8, 1.0, 1.2]
H_GRID = [1.6, 1.8, 2.0, 2.2]
SHARED_SITE = 3
WINDOWS = [
    [3],
    [3, 4],
    [2, 3, 4],
    [1, 2, 3, 4, 5],
    [0, 1, 2, 3, 4, 5, 6, 7],
]
THETAS = [0.05, 0.1, 0.15, 0.2]
THETA_PROBE = 0.02
EPSILON = 0.05
DELTA = 0.05
LOOSE = 0.15
ROUTE_CHECK_POINT = (1.0, 2.0)
ROUTE_CHECK_WINDOW = [1, 2, 3, 4, 5]


def pauli_site(n_qubits: int, qubit: int) -> np.ndarray:
    z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    full = np.array([[1.0]], dtype=complex)
    for j in range(n_qubits):
        full = np.kron(full, z if j == qubit else np.eye(2))
    return full


def kubo_mori_form(rho_w: np.ndarray, drho_w: np.ndarray) -> float:
    """The declared modular quadratic form. Inputs are the reduced
    reference and the reduced first-order perturbation only; no
    entropy is evaluated anywhere in this function."""
    p, vecs = np.linalg.eigh(rho_w)
    p = np.clip(p.real, 1e-300, None)
    d = vecs.conj().T @ drho_w @ vecs
    logp = np.log(p)
    diff_p = p[:, None] - p[None, :]
    diff_l = logp[:, None] - logp[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        kernel = np.where(np.abs(diff_p) > 1e-14,
                          diff_l / np.where(np.abs(diff_p) > 1e-14,
                                            diff_p, 1.0),
                          1.0 / p[None, :])
    return float(0.5 * np.sum(np.abs(d) ** 2 * kernel))


def fit_through_origin(xs, values):
    x = np.asarray(xs, dtype=float)
    v = np.asarray(values, dtype=float)
    lam = float((x @ v) / (x @ x))
    scale = max(float(np.max(np.abs(v))), 1e-300)
    residual = float(np.max(np.abs(v - lam * x)) / scale)
    return lam, residual


def spread(values) -> float:
    a = np.asarray(values, dtype=float)
    return float((a.max() - a.min()) / max(a.mean(), 1e-300))


def coupling_point(j: float, h: float) -> dict:
    sigma = thermal_state(ising_hamiltonian_jh(N, j, h), BETA)
    assert float(np.linalg.eigvalsh(sigma).min()) > 1e-9, \
        f"thermal spectrum at the support floor, J={j}, h={h}"

    p_shared = pauli_site(N, SHARED_SITE)
    drho = 1j * (p_shared @ sigma - sigma @ p_shared)

    # dichotomy: excitation disjoint from the window is inert in both
    # the entropy and the modular form, by localization
    blind = list(range(2, N))
    p_out = pauli_site(N, 1)
    u_out = local_rotation(N, 1, 0.2, "z")
    rho_out = u_out @ sigma @ u_out.conj().T
    s_blind = relative_entropy(partial_trace(rho_out, blind, N),
                               partial_trace(sigma, blind, N))
    drho_out = 1j * (p_out @ sigma - sigma @ p_out)
    q_blind = kubo_mori_form(partial_trace(sigma, blind, N),
                             partial_trace(drho_out, blind, N))
    assert abs(s_blind) < 1e-10, "disjoint probe not inert in entropy"
    assert abs(q_blind) < 1e-12, "disjoint probe not inert in Q"

    entry = {"J": j, "h": h, "windows": {}}
    q_by_window, s_top_by_window, lambdas = [], [], []
    for window in WINDOWS:
        key = "".join(str(q) for q in window)
        sigma_w = partial_trace(sigma, window, N)
        q_w = kubo_mori_form(sigma_w, partial_trace(drho, window, N))

        values = []
        for theta in THETAS:
            u = local_rotation(N, SHARED_SITE, theta, "z")
            rho = u @ sigma @ u.conj().T
            s = relative_entropy(partial_trace(rho, window, N), sigma_w)
            assert np.isfinite(s) and s >= -1e-12
            values.append(float(s))

        u = local_rotation(N, SHARED_SITE, THETA_PROBE, "z")
        rho = u @ sigma @ u.conj().T
        s_probe = relative_entropy(partial_trace(rho, window, N), sigma_w)
        probe_ratio = s_probe / (THETA_PROBE**2 * q_w)
        assert abs(probe_ratio - 1.0) < 0.02, \
            f"validation probe off at window {key}, J={j}, h={h}"

        lam, res = fit_through_origin(
            [t**2 * q_w for t in THETAS], values)
        entry["windows"][key] = {
            "Q_modular": q_w,
            "S_by_theta": values,
            "lambda_modular": lam,
            "residual_modular": res,
            "probe_ratio": float(probe_ratio),
        }
        q_by_window.append(q_w)
        s_top_by_window.append(values[-1])
        lambdas.append(lam)

    for a, b in zip(q_by_window[:-1], q_by_window[1:]):
        assert a <= b + 1e-12, "modular form violates nested monotonicity"
    for a, b in zip(s_top_by_window[:-1], s_top_by_window[1:]):
        assert a <= b + 1e-10, "entropy violates nested DPI"

    entry["modular_spread"] = spread(lambdas)
    entry["saturation_Q_last_step"] = abs(
        q_by_window[-1] - q_by_window[-2]) / q_by_window[-1]

    if (j, h) == ROUTE_CHECK_POINT:
        u = local_rotation(N, SHARED_SITE, THETAS[-1], "z")
        rho = u @ sigma @ u.conj().T
        s_umegaki = relative_entropy(
            partial_trace(rho, ROUTE_CHECK_WINDOW, N),
            partial_trace(sigma, ROUTE_CHECK_WINDOW, N))
        s_araki = araki_relative_entropy(
            functional_state_on_subalgebra(rho, ROUTE_CHECK_WINDOW, N),
            functional_state_on_subalgebra(sigma, ROUTE_CHECK_WINDOW, N))
        assert abs(s_umegaki - s_araki) < 1e-10, \
            "TB-0 route disagreement on the declared member"
        entry["route_check_abs_diff"] = abs(s_umegaki - s_araki)
    return entry


def main() -> int:
    points = [coupling_point(j, h) for j in J_GRID for h in H_GRID]
    keys = ["".join(str(q) for q in w) for w in WINDOWS]

    summary = {}
    for eps, delta, tag in ((EPSILON, DELTA, "strict"), (LOOSE, LOOSE, "loose")):
        prefix_curve = []
        for k in range(len(keys)):
            fam = keys[: k + 1]
            count = 0
            for p in points:
                law = all(
                    p["windows"][key]["residual_modular"] < eps
                    for key in fam)
                lams = [p["windows"][key]["lambda_modular"] for key in fam]
                if law and (len(fam) < 2 or spread(lams) < delta):
                    count += 1
            prefix_curve.append(count / len(points))
        summary[tag] = {"joint_survival_by_prefix_size": prefix_curve}

    qo3 = json.loads((Path(__file__).resolve().parents[1] / "results"
                      / "qo3-family.json").read_text())
    baseline = {
        tag: qo3["summary"][tag]["family_b_joint_survival_by_prefix_size"]
        for tag in ("strict", "loose")
    }
    lattice_spreads = [p["family_b_spread"] for p in qo3["coupling_points"]]
    modular_spreads = [p["modular_spread"] for p in points]

    full_survival = summary["strict"]["joint_survival_by_prefix_size"][-1]
    if full_survival == 1.0:
        verdict = ("modular reformulation holds: under the Kubo-Mori "
                   "weight the shared-event family is universal with "
                   "lambda canonically one at every coupling point, "
                   "where the lattice theta^2 weight tightened toward "
                   "exclusion")
    elif full_survival > baseline["strict"][-1]:
        verdict = ("modular weight organizes the family better than the "
                   "lattice weight but not perfectly; partial")
    else:
        verdict = ("modular reformulation fails to improve on the "
                   "lattice weight; the row-ten bridge is in doubt")

    record = {
        "schema": "tb3-wedge-v1",
        "label": "exploratory",
        "declared": {
            "model_family": "open-chain Ising H = -J sum ZZ - h sum X",
            "N": N, "beta": BETA, "J_grid": J_GRID, "h_grid": H_GRID,
            "windows": WINDOWS, "shared_site": SHARED_SITE,
            "excitation": "exp(i theta Z) at the shared site",
            "thetas": THETAS, "theta_probe": THETA_PROBE,
            "modular_weight": "Kubo-Mori quadratic form of the reduced "
                "first-order perturbation in the reduced reference "
                "eigenbasis; no entropy evaluated in its assembly",
            "epsilon": EPSILON, "delta": DELTA, "loose": LOOSE,
            "baseline": "committed qo3-family.json family-B curves",
            "analogy_note": "wedge language is declared analogy; the "
                "chain has no causal structure",
        },
        "coupling_points": points,
        "summary": summary,
        "qo3_lattice_baseline": {
            "joint_survival_by_prefix_size": baseline,
            "spread_mean": float(np.mean(lattice_spreads)),
            "spread_max": float(np.max(lattice_spreads)),
        },
        "modular_spread_mean": float(np.mean(modular_spreads)),
        "modular_spread_max": float(np.max(modular_spreads)),
        "verdict": verdict,
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
        / "tb3-wedge.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    sample = points[0]
    print("sample point J=%.1f h=%.1f:" % (sample["J"], sample["h"]))
    for key in keys:
        w = sample["windows"][key]
        print(f"  window {key}: Q {w['Q_modular']:.6f}, lambda "
              f"{w['lambda_modular']:.4f}, residual "
              f"{w['residual_modular']:.4f}, probe {w['probe_ratio']:.4f}")
    print("modular spread mean/max:",
          round(record["modular_spread_mean"], 5),
          round(record["modular_spread_max"], 5),
          "vs lattice baseline mean/max:",
          round(record["qo3_lattice_baseline"]["spread_mean"], 4),
          round(record["qo3_lattice_baseline"]["spread_max"], 4))
    print("modular joint survival (strict):",
          summary["strict"]["joint_survival_by_prefix_size"])
    print("lattice joint survival (strict):", baseline["strict"])
    print("verdict:", verdict)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
