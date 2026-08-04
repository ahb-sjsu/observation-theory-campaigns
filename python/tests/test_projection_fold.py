import math
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from projection_fold import (  # noqa: E402
    analytic_fold_branches,
    classify_scalar_critical_point,
    polynomial_critical_points,
    polynomial_time_branches,
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


def test_n0_monotone_null_single_branch_everywhere():
    for t_obs in (-2.0, 0.0, 1.5):
        branches = polynomial_time_branches([1.0, 0.0], t_obs)
        assert len(branches) == 1
        assert branches[0].orientation == 1
        assert math.isclose(branches[0].tau, t_obs, rel_tol=0.0, abs_tol=1e-12)
    assert polynomial_critical_points([1.0, 0.0]) == []


def test_p0_polynomial_instrument_matches_quadratic_reference():
    for t_obs in (0.25, 1.0, 4.0):
        general = polynomial_time_branches([1.0, 0.0, 0.0], t_obs)
        reference = sorted(analytic_fold_branches(t_obs), key=lambda b: b.tau)
        assert len(general) == len(reference) == 2
        assert signed_branch_count(general) == 0
        for got, want in zip(general, reference, strict=True):
            assert math.isclose(got.tau, want.tau, rel_tol=0.0, abs_tol=1e-12)
            assert got.orientation == want.orientation


def test_p1_annihilation_polynomial_instrument():
    before = polynomial_time_branches([-1.0, 0.0, 0.0], -1.0)
    assert len(before) == 2
    assert signed_branch_count(before) == 0
    assert polynomial_time_branches([-1.0, 0.0, 0.0], 1.0) == []


def test_d0_degenerate_cubic_not_classified_as_fold():
    points = polynomial_critical_points([1.0, 0.0, 0.0, 0.0])
    assert len(points) == 1
    assert points[0]["classification"] == "degenerate"


def test_m0_double_fold_band_structure_and_signed_invariant():
    coefficients = [1.0, 0.0, -1.0, 0.0]
    counts = []
    for t_obs in (-1.0, -0.2, 0.0, 0.2, 1.0):
        branches = polynomial_time_branches(coefficients, t_obs)
        counts.append(len(branches))
        assert signed_branch_count(branches) == 1
        for branch in branches:
            assert abs(branch.tau**3 - branch.tau - t_obs) < 1e-10
    assert counts == [1, 3, 3, 3, 1]


def test_m0_double_fold_critical_points_classified():
    fold_time = 2.0 / (3.0 * math.sqrt(3.0))
    low, high = polynomial_critical_points([1.0, 0.0, -1.0, 0.0])
    assert low["classification"] == "annihilation-fold"
    assert high["classification"] == "creation-fold"
    assert math.isclose(low["tau"], -1.0 / math.sqrt(3.0), rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(high["tau"], 1.0 / math.sqrt(3.0), rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(low["t"], fold_time, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(high["t"], -fold_time, rel_tol=0.0, abs_tol=1e-12)
    for point in (low, high):
        assert abs(point["first_derivative"]) < 1e-12
        assert abs(point["second_derivative"]) > 3.4


def test_non_generic_slice_is_refused():
    with pytest.raises(ValueError, match="non-generic"):
        polynomial_time_branches([1.0, 0.0, 0.0], 0.0)


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
