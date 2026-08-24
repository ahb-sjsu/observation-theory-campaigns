"""freshread tests. Core-logic tests plus a substrate-agnostic reproduction of
the ZK-FIX cost curve (cost = lag CDF, false-clear = 0) that needs no live
cluster -- it exercises the same decision the ZK/PG/Mongo adapters make.

    python test_freshread.py      # standalone runner (also pytest-compatible)
"""
import random

from core import FreshRead


def _mock(applied, refresh_applied):
    return FreshRead(read=lambda p: ("v", applied),
                     refresh=lambda p, W: ("v", refresh_applied))


def test_local_when_fresh():
    r = _mock(100, 100).get("/x", W=50)
    assert r.mode == "LOCAL" and r.certified and r.applied == 100


def test_refresh_when_stale():
    r = _mock(40, 100).get("/x", W=50)
    assert r.mode == "REFRESHED" and r.applied == 100 and r.certified


def test_local_exactly_at_watermark():
    r = _mock(50, 999).get("/x", W=50)          # applied == W -> local, no refresh
    assert r.mode == "LOCAL"


def test_refresh_reaches_watermark():
    r = _mock(0, 60).get("/x", W=60)            # sound: after refresh applied >= W
    assert r.certified


def test_cost_curve_generic():
    """Substrate-agnostic: a replica lagging a leader by a jittered amount;
    the reader needs state as of now-tau (W = now-tau); refresh reaches `now`.
    Reproduces the ZK-FIX result: false-clear 0 everywhere; cost = P(lag > tau)."""
    rng = random.Random(0)
    N, lag_mean, lag_sd = 4000, 200.0, 60.0
    taus = [0, 50, 100, 150, 200, 250, 300, 400]
    cost, fc = {}, {}
    for tau in taus:
        s = f = 0
        for _ in range(N):
            now = rng.uniform(1e6, 2e6)
            lag = max(0.0, rng.gauss(lag_mean, lag_sd))
            fr = FreshRead(read=lambda p, a=now - lag: ("v", a),
                           refresh=lambda p, W, n=now: ("v", n))
            r = fr.get("/z", W=now - tau)
            if r.mode == "REFRESHED":
                s += 1
            if r.mode == "LOCAL":
                assert r.applied >= r.required   # sound witness: no false local clear
            if not r.certified:
                f += 1                            # must stay 0
        cost[tau], fc[tau] = s / N, f / N
    assert all(v == 0.0 for v in fc.values()), fc          # false-clear zero
    c = [cost[t] for t in taus]
    assert all(c[i] >= c[i + 1] - 1e-9 for i in range(len(c) - 1)), c   # monotone
    assert cost[0] > 0.95 and cost[400] < 0.05             # the two blind endpoints
    print("  cost curve (sync rate):",
          {t: round(cost[t], 3) for t in taus}, "| false-clear: 0 at every tau")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for t in tests:
        t(); print("PASS", t.__name__)
    print(f"\nAll {len(tests)} freshread tests passed.")
