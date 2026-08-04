import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from projection_fold import (  # noqa: E402
    analytic_fold_branches,
    classify_scalar_critical_point,
    schwinger_optimum,
    signed_branch_count,
    simulate_toy_hamiltonian,
)


def test_creation_fold_branch_counts_and_orientation():
    assert analytic_fold_branches(-1.0) == []
    at_fold = analytic_fold_branches(0.0)
    assert len(at_fold) == 1
    assert at_fold[0].orientation == 0
    after = analytic_fold_branches(1.0, velocity=2.0)
    assert len(after) == 2
    assert sorted(branch.orientation for branch in after) == [-1, 1]
    assert signed_branch_count(after) == 0
    assert sorted(round(branch.x, 12) for branch in after) == [-2.0, 2.0]


def test_annihilation_fold():
    before = analytic_fold_branches(-1.0, a=-1.0)
    assert len(before) == 2
    assert signed_branch_count(before) == 0
    assert len(analytic_fold_branches(1.0, a=-1.0)) == 0


def test_critical_point_classifier():
    assert classify_scalar_critical_point(1.0, 2.0) == "regular"
    assert classify_scalar_critical_point(0.0, 0.0) == "degenerate"
    assert classify_scalar_critical_point(0.0, 2.0) == "creation-fold"
    assert classify_scalar_critical_point(0.0, -2.0) == "annihilation-fold"


def test_schwinger_circle_baseline():
    radius, action = schwinger_optimum(2.0, 0.5)
    assert radius == 4.0
    assert math.isclose(action, 8.0 * math.pi)


def test_toy_energy_is_well_controlled():
    params = {"omega_t": 1.0, "omega_u": 1.2, "lambda": 0.1, "g": 0.25, "field": 1.0}
    result = simulate_toy_hamiltonian(
        [0.0, 1.0, 0.0, 0.2, 0.1, 0.0], params, dt=5e-4, tau_max=5.0
    )
    assert np.isfinite(result.energy_final)
    assert result.max_relative_energy_drift < 1e-4
    assert result.n_steps == 10000
