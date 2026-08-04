#!/usr/bin/env python3
"""QO-3 consumer-family consistency: is the Jacobson quantifier inert?

Model-internal only. The declared requirement, per coupling point (J, h) of
the Ising family H = -J sum ZZ - h sum X at beta = 0.4:

  for every consumer c in the declared family,
  D_c(theta) = lambda_c * theta^2 within relative residual epsilon,
  and lambda_c is universal across consumers within spread delta.

Declarations (Level 0, before the sweep; QO open question 3 discipline):

- Consumers: right-exterior wedges [c..7] of the open chain, cuts
  c = 1..6. Geometric, fixed by the model graph. In one dimension every
  cut has boundary size one, so this experiment tests the UNIVERSALITY
  content of the all-observers quantifier, not area scaling (that is
  EG-1's job and is not claimed here).
- Excitation family: Z rotation at the boundary site of each consumer's
  own wedge (each wedge probed through its own horizon), strengths
  theta in {0.05, 0.1, 0.15, 0.2}.
- Flux weight: w(theta) = theta^2, from the excitation parameter alone;
  no dynamical or informational quantity enters the declaration.
- Thresholds: epsilon = 0.05 (theta^2-law residual), delta = 0.05
  (universality spread); both also reported at 0.15.

Witnesses: per-consumer survival of the theta^2 law over the coupling
grid; joint survival for nested prefix subfamilies {1}, {1,2}, ..,
{1..6} and for the bulk subfamily {2..5}; the tightening curve versus
family size (QO open question 11: a curve, not a guess). Verdicts:
"quantifier active" if the joint constraint is strictly tighter than
every single-consumer constraint and tightens with family size;
"quantifier inert" if joint equals single; "declaration fails" if no
coupling point survives even loose thresholds. Every outcome is a
result.

Structural null (asserted): consumer c+1 is exactly blind to consumer
c's boundary excitation, by no-signalling.

Exploratory label. No physics claim.
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

N = 8
BETA = 0.4
CUTS = [1, 2, 3, 4, 5, 6]
THETAS = [0.05, 0.1, 0.15, 0.2]
J_GRID = [0.6, 0.8, 1.0, 1.2]
H_GRID = [1.6, 1.8, 2.0, 2.2]
EPSILON = 0.05
DELTA = 0.05
LOOSE = 0.15


def fit_quadratic_through_origin(thetas, values):
    t2 = np.asarray(thetas, dtype=float) ** 2
    v = np.asarray(values, dtype=float)
    lam = float((t2 @ v) / (t2 @ t2))
    scale = max(float(np.max(np.abs(v))), 1e-300)
    residual = float(np.max(np.abs(v - lam * t2)) / scale)
    return lam, residual


def consumer_divergences(sigma, cut):
    wedge = list(range(cut, N))
    sigma_w = partial_trace(sigma, wedge, N)
    values = []
    for theta in THETAS:
        u = local_rotation(N, cut, theta, "z")
        rho = u @ sigma @ u.conj().T
        d = relative_entropy(partial_trace(rho, wedge, N), sigma_w)
        assert np.isfinite(d) and d >= -1e-12
        values.append(float(d))
    assert all(b > a for a, b in zip(values[:-1], values[1:], strict=False)), \
        "divergence not increasing in excitation strength"
    return values


def coupling_point(j, h):
    sigma = thermal_state(ising_hamiltonian_jh(N, j, h), BETA)
    smallest = float(np.linalg.eigvalsh(sigma).min())
    assert smallest > 1e-9, \
        f"thermal spectrum too close to the support floor at J={j}, h={h}"

    blind_wedge = list(range(2, N))
    u = local_rotation(N, 1, 0.2, "z")
    rho = u @ sigma @ u.conj().T
    d_blind = relative_entropy(
        partial_trace(rho, blind_wedge, N), partial_trace(sigma, blind_wedge, N)
    )
    assert abs(d_blind) < 1e-10, "no-signalling wedge null failed"

    lambdas, residuals = {}, {}
    for cut in CUTS:
        lam, res = fit_quadratic_through_origin(
            THETAS, consumer_divergences(sigma, cut)
        )
        lambdas[cut] = lam
        residuals[cut] = res
    return lambdas, residuals


def spread(lambdas, cuts):
    values = np.array([lambdas[c] for c in cuts])
    return float((values.max() - values.min()) / max(values.mean(), 1e-300))


def main() -> int:
    points = []
    for j in J_GRID:
        for h in H_GRID:
            lambdas, residuals = coupling_point(j, h)
            points.append({
                "J": j, "h": h,
                "lambda_by_cut": {str(c): lambdas[c] for c in CUTS},
                "residual_by_cut": {str(c): residuals[c] for c in CUTS},
                "universality_spread_full": spread(lambdas, CUTS),
                "universality_spread_bulk": spread(lambdas, [2, 3, 4, 5]),
            })

    def survives_single(point, cut, eps):
        return point["residual_by_cut"][str(cut)] < eps

    def survives_joint(point, cuts, eps, delta):
        law = all(survives_single(point, c, eps) for c in cuts)
        lam = {c: point["lambda_by_cut"][str(c)] for c in cuts}
        return law and (len(cuts) < 2 or spread(lam, cuts) < delta)

    n_points = len(points)
    summary = {}
    for eps, delta, tag in ((EPSILON, DELTA, "strict"), (LOOSE, LOOSE, "loose")):
        single = {
            str(c): sum(survives_single(p, c, eps) for p in points) / n_points
            for c in CUTS
        }
        prefixes = [CUTS[: k + 1] for k in range(len(CUTS))]
        joint_curve = [
            sum(survives_joint(p, fam, eps, delta) for p in points) / n_points
            for fam in prefixes
        ]
        bulk = sum(
            survives_joint(p, [2, 3, 4, 5], eps, delta) for p in points
        ) / n_points
        summary[tag] = {
            "single_survival_by_cut": single,
            "joint_survival_by_prefix_size": joint_curve,
            "bulk_family_survival": bulk,
        }

    strict = summary["strict"]
    min_single = min(strict["single_survival_by_cut"].values())
    joint_full = strict["joint_survival_by_prefix_size"][-1]
    loose_full = summary["loose"]["joint_survival_by_prefix_size"][-1]
    if loose_full == 0.0:
        verdict = "declaration fails in this model class: no coupling point " \
                  "satisfies the family requirement even at loose thresholds"
    elif joint_full < min_single:
        verdict = "quantifier active: the family requirement is strictly " \
                  "tighter than every single-consumer requirement"
    else:
        verdict = "quantifier inert in this model class: the family adds " \
                  "nothing beyond the tightest single consumer"

    record = {
        "schema": "qo3-family-v1",
        "label": "exploratory",
        "declared": {
            "model_family": "open-chain Ising H = -J sum ZZ - h sum X",
            "beta": BETA, "J_grid": J_GRID, "h_grid": H_GRID,
            "consumers": "right-exterior wedges, cuts 1..6",
            "excitations": "Z rotation at each consumer's boundary site",
            "thetas": THETAS, "flux_weight": "theta^2 (parameter only)",
            "epsilon": EPSILON, "delta": DELTA, "loose": LOOSE,
            "scope_note": "1D cuts all have boundary size one; this tests "
                          "the universality content of the quantifier, not "
                          "area scaling",
        },
        "coupling_points": points,
        "summary": summary,
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
    output = Path(__file__).resolve().parents[1] / "results" / "qo3-family.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print("single survival (strict):", strict["single_survival_by_cut"])
    print("joint survival by family size (strict):",
          [round(v, 3) for v in strict["joint_survival_by_prefix_size"]])
    print("bulk family survival (strict):", strict["bulk_family_survival"])
    print("joint survival by family size (loose):",
          [round(v, 3) for v in summary["loose"]["joint_survival_by_prefix_size"]])
    sample = points[0]
    print("sample lambdas at J=%.1f h=%.1f:" % (sample["J"], sample["h"]),
          {c: round(v, 4) for c, v in sample["lambda_by_cut"].items()})
    print("verdict:", verdict)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
