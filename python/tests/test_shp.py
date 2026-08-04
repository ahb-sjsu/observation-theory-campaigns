import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from shp_land2016 import (  # noqa: E402
    coupling_ge,
    final_velocity,
    impulse_system,
    rutherford_cot_half_angle,
    tdot_final,
)


def test_shp_eq66_vs_eq67_transcription_guard():
    for v in (0.2, 0.5):
        tdot_in = 1.0 / math.sqrt(1.0 - v * v)
        for rhat in ((0.8, 0.6), (0.28, 0.96)):
            for ge in (0.3, 1.7, 3.5):
                a, rhs = impulse_system(tdot_in, v, rhat, ge)
                assert np.allclose(
                    np.linalg.solve(a, rhs),
                    final_velocity(tdot_in, v, rhat, ge),
                    atol=1e-12,
                )


def test_shp_eq76_is_time_component_of_eq67():
    tdot_in = 1.0 / math.sqrt(1.0 - 0.36)
    closed = final_velocity(tdot_in, 0.6, (0.6, 0.8), 1.4)
    assert abs(closed[0] - tdot_final(tdot_in, 0.6, 0.6, 1.4)) < 1e-14


def test_shp_positive_definite_numerator_eq78():
    for v in (0.1, 0.5, 0.9):
        tdot_in = 1.0 / math.sqrt(1.0 - v * v)
        for rx in (0.1, 0.6, 0.99):
            discriminant = (v * rx) ** 2 - (1.0 + 2.0 / tdot_in)
            assert discriminant < 0.0


def test_shp_annihilation_threshold_eqs79_80():
    tdot_in = 1.0 / math.sqrt(1.0 - 0.16)
    for ge in (0.5, 1.0, 1.99):
        assert tdot_final(tdot_in, 0.4, 0.8, ge) > 0.0
    for ge in (2.01, 3.0, 20.0):
        assert tdot_final(tdot_in, 0.4, 0.8, ge) < 0.0
    lam, mass, radius = 0.05, 1.0, 1.0
    strength_at_threshold = 2.0 * mass * radius**2 / lam
    ge = coupling_ge(lam, mass, strength_at_threshold, radius)
    assert abs(ge - 2.0) < 1e-14


def test_shp_asymptote_eq81():
    tdot_in = 1.0 / math.sqrt(1.0 - 0.16)
    limit = -(tdot_in + 2.0)
    values = [tdot_final(tdot_in, 0.4, 0.8, ge) for ge in (10.0, 100.0, 1e4)]
    gaps = [abs(value - limit) for value in values]
    assert gaps[0] > gaps[1] > gaps[2]
    assert gaps[2] < 1e-3


def test_shp_rutherford_limit_eq74():
    assert abs(rutherford_cot_half_angle((0.6, 0.8)) - 4.0 / 3.0) < 1e-14
