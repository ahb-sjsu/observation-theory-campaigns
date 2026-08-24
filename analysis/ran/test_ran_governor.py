"""Tests for governor.ran: the governor detects consumer-relative vacuity,
recommends refreshing to the coherence floor, and escalates to a mechanism
change when refreshing cannot close the loop.

    python test_ran_governor.py
"""
import numpy as np

from ran_governor import Consumer, RanGovernor, RefreshFloorEstimator


def _ar1(n, rho, seed):
    rng = np.random.default_rng(seed)
    x = np.zeros(n); e = np.sqrt(1 - rho * rho)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + e * rng.standard_normal()
    return x


def test_floor_tracks_coherence():
    est = RefreshFloorEstimator()
    for v in _ar1(512, 0.9, 0):
        est.observe(v)
    tc = est.coherence_slots()          # ~ -1/ln(0.9) ~ 9.5
    assert 6 <= tc <= 14, tc
    assert 0.5 <= est.floor_slots() <= 3.0


def test_consumer_relative_vacuity():
    """Same certificate stream, two consumers: vacuous for the strict one,
    certified for the lax one."""
    g = RanGovernor()
    g.register(Consumer("embb", 0.10))
    g.register(Consumer("urllc", 0.01))
    rng = np.random.default_rng(1)
    vals = _ar1(600, 0.9, 1)
    for t in range(600):
        ok = rng.random() > 0.05        # ~5% failure on the shared certificate
        g.observe("cqi", "embb", vals[t], ok)
        g.observe("cqi", "urllc", vals[t], ok)
    d_embb = g.govern("cqi", "embb", report_period_slots=20)
    d_urllc = g.govern("cqi", "urllc", report_period_slots=20)
    assert not d_embb.vacuous and d_embb.certified            # 0.05 <= 0.10
    assert d_urllc.vacuous and not d_urllc.certified          # 0.05 > 0.01
    print(f"  same cqi: eMBB fc={d_embb.false_clear} certified={d_embb.certified} | "
          f"URLLC fc={d_urllc.false_clear} vacuous={d_urllc.vacuous} -> {d_urllc.mechanism}")


def test_refresh_faster_then_mechanism():
    """A vacuous certificate reported above the floor -> refresh_faster; already
    at the floor and still vacuous -> a mechanism change."""
    g = RanGovernor()
    g.register(Consumer("embb", 0.10))
    rng = np.random.default_rng(2)
    vals = _ar1(600, 0.9, 2)
    for t in range(600):
        g.observe("cqi", "embb", vals[t], rng.random() > 0.30)   # 30% >> 0.10 -> vacuous
    floor = g.govern("cqi", "embb", 20).refresh_floor_slots
    far = g.govern("cqi", "embb", report_period_slots=20)        # 20 >> floor
    at = g.govern("cqi", "embb", report_period_slots=1)          # at the floor
    assert far.vacuous and far.mechanism == "refresh_faster"
    assert far.recommend_report_period <= far.report_period_slots
    assert at.vacuous and at.mechanism == "add_diversity"        # refreshing can't fix it
    print(f"  vacuous cqi (floor~{floor}): @P=20 -> {far.mechanism} "
          f"(rp {far.recommend_report_period}); @P=1 -> {at.mechanism}")


def test_serving_cert_routes_elsewhere():
    g = RanGovernor()
    g.register(Consumer("embb", 0.10))
    rng = np.random.default_rng(3)
    vals = _ar1(600, 0.8, 3)
    for t in range(600):
        g.observe("rsrp", "embb", vals[t], rng.random() > 0.30)
    at = g.govern("rsrp", "embb", report_period_slots=1)
    assert at.vacuous and at.mechanism == "route_elsewhere"      # serving cert -> re-route


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for t in tests:
        t(); print("PASS", t.__name__)
    print(f"\nAll {len(tests)} governor.ran tests passed.")
