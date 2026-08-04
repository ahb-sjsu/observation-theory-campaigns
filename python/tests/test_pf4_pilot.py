import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from pf4_pilot import run_cell, static_family_reverses  # noqa: E402


def test_p1_static_reversal_is_deterministic_threshold():
    assert static_family_reverses(u_max=3.0, u_in=0.0, tdot_in=1.0, eps=0.5)
    assert not static_family_reverses(u_max=1.9, u_in=0.0, tdot_in=1.0,
                                      eps=0.5)
    assert not static_family_reverses(u_max=3.0, u_in=3.0, tdot_in=0.1,
                                      eps=10.0)


def test_p2_zero_field_null_and_energy_conservation():
    cell = run_cell(1.0, 0.0, n=2000)
    assert cell["count"] == 0
    assert cell["max_relative_energy_drift"] < 1e-6


def test_p2_reversal_fraction_decreases_with_gap():
    low = run_cell(1.0, 1.5, n=4000)
    high = run_cell(2.0, 1.5, n=4000)
    assert low["fraction"] > high["fraction"]
    assert low["max_relative_energy_drift"] < 1e-5
