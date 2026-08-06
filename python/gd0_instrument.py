#!/usr/bin/env python3
"""GD-0 decision-theoretic instrument layer (exploratory, GD track).

The new track's mandatory first experiment, per
GAMES-DECISIONS-TRACK.md. Two instruments, validated against exact
closed forms before any later GD experiment may run.

VALUE OF AN EXPERIMENT. For prior pi over states, utility u(a, s),
and experiment A with A[s, y] = P(signal y | state s), the value is
the expected posterior-optimal payoff, an exact finite sum.

BLACKWELL GARBLING CHECKER. A is Blackwell-above B iff B = A M for a
row-stochastic M, a linear feasibility problem solved exactly enough
by least squares on the simplex via projected iterations with an
exact residual certificate (no scipy dependency; the certificate is
the checked object, the solver is only a search).

Controls.
C1 closed forms, the uninformative experiment's value equals the
   no-information payoff and the perfect experiment's value equals
   the full-information payoff, exactly.
C2 monotonicity, garbling never raises the value for any task in a
   declared battery.
C3 detection, a declared garble is certified feasible, its reverse
   infeasible, and a signal permutation is certified both ways.
C4 the binary symmetric channel ordering, BSC(e1) above BSC(e2) iff
   e1 <= e2 <= 1/2, agreeing with the checker across a grid.
C5 an incomparable pair, infeasible both ways, whose declared task
   battery exhibits a preference reversal, one task strictly prefers
   each experiment. This seeds GD-1.

Exploratory label. No claim about human beings.
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

FEAS_TOL = 1e-7


def experiment_value(prior, utility, likelihood) -> float:
    """Exact expected posterior-optimal payoff."""
    prior = np.asarray(prior, dtype=float)
    utility = np.asarray(utility, dtype=float)  # (actions, states)
    lik = np.asarray(likelihood, dtype=float)   # (states, signals)
    joint = prior[:, None] * lik                # (states, signals)
    value = 0.0
    for y in range(lik.shape[1]):
        col = joint[:, y]
        p_y = col.sum()
        if p_y <= 0:
            continue
        value += np.max(utility @ col)
    return float(value)


def garbling_certificate(a, b, iters=20_000):
    """Search for row-stochastic M with A M = B; return (feasible,
    residual). The certificate is the residual of the best M found
    projected to the simplex rows, checked against FEAS_TOL; the
    solver is only a search, the residual is the checked object."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ya, yb = a.shape[1], b.shape[1]
    m = np.full((ya, yb), 1.0 / yb)
    lam = float(np.linalg.eigvalsh(a.T @ a).max())
    step = 0.9 / max(lam, 1e-12)
    for _ in range(iters):
        grad = a.T @ (a @ m - b)
        m = m - step * grad
        # project rows to the probability simplex
        for r in range(ya):
            v = np.sort(m[r])[::-1]
            css = np.cumsum(v) - 1.0
            rho = np.nonzero(v - css / (np.arange(ya * 0 + yb) + 1)
                             > 0)[0][-1]
            theta = css[rho] / (rho + 1.0)
            m[r] = np.maximum(m[r] - theta, 0.0)
    resid = float(np.max(np.abs(a @ m - b)))
    return resid < FEAS_TOL, resid


def bsc(eps: float) -> np.ndarray:
    return np.array([[1 - eps, eps], [eps, 1 - eps]])


def main() -> int:
    record: dict = {"schema": "gd0-instrument-v1",
                    "label": "exploratory"}
    rng = np.random.RandomState(20260806)

    # C1: closed forms
    prior = np.array([0.3, 0.45, 0.25])
    utility = rng.uniform(0, 1, size=(4, 3))
    uninf = np.ones((3, 2)) / 2.0
    perfect = np.eye(3)
    v_no_info = float(np.max(utility @ prior))
    v_full = float(np.sum(prior * np.max(utility, axis=0)))
    v_uninf = experiment_value(prior, utility, uninf)
    v_perf = experiment_value(prior, utility, perfect)
    assert abs(v_uninf - v_no_info) < 1e-12, "C1 uninformative"
    assert abs(v_perf - v_full) < 1e-12, "C1 perfect"
    record["C1"] = {"no_info": v_no_info, "full_info": v_full}

    # C2: garbling never raises value, over a task battery
    battery = [rng.uniform(-1, 1, size=(3, 3)) for _ in range(20)]
    a_exp = rng.dirichlet(np.ones(4), size=3)
    worst_gain = -1.0
    for _ in range(10):
        m_g = rng.dirichlet(np.ones(3), size=4)
        b_exp = a_exp @ m_g
        for task in battery:
            gain = (experiment_value(prior, task, b_exp)
                    - experiment_value(prior, task, a_exp))
            worst_gain = max(worst_gain, gain)
    assert worst_gain < 1e-10, f"C2 garbling raised value: {worst_gain}"
    record["C2"] = {"max_value_gain_under_garbling": worst_gain}

    # C3: detection and permutation equivalence
    m_g = rng.dirichlet(np.ones(3), size=4)
    b_exp = a_exp @ m_g
    ok_fwd, r_fwd = garbling_certificate(a_exp, b_exp)
    ok_rev, r_rev = garbling_certificate(b_exp, a_exp)
    assert ok_fwd, f"C3 declared garble not certified: {r_fwd}"
    assert not ok_rev, f"C3 reverse wrongly certified: {r_rev}"
    perm = a_exp[:, [2, 0, 3, 1]]
    ok_p1, _ = garbling_certificate(a_exp, perm)
    ok_p2, _ = garbling_certificate(perm, a_exp)
    assert ok_p1 and ok_p2, "C3 permutation equivalence failed"
    record["C3"] = {"forward_residual": r_fwd,
                    "reverse_residual": r_rev}

    # C4: BSC ordering
    grid = [0.05, 0.15, 0.25, 0.35, 0.45]
    for e1, e2 in itertools.product(grid, grid):
        feas, _ = garbling_certificate(bsc(e1), bsc(e2))
        expected = e1 <= e2
        assert feas == expected, f"C4 failed at {e1},{e2}: {feas}"
    record["C4"] = {"grid": grid, "ordering": "e1<=e2 iff garblable"}

    # C5: incomparable pair with task reversal
    a5 = np.array([[0.9, 0.1], [0.5, 0.5], [0.1, 0.9]])
    b5 = np.array([[0.8, 0.2], [0.2, 0.8], [0.5, 0.5]])
    ok_ab, _ = garbling_certificate(a5, b5)
    ok_ba, _ = garbling_certificate(b5, a5)
    assert not ok_ab and not ok_ba, "C5 pair unexpectedly comparable"
    prior5 = np.array([1 / 3, 1 / 3, 1 / 3])
    task_a = np.array([[1.0, 0.0, 0.0], [0.0, 0.5, 0.5]])
    task_b = np.array([[0.0, 1.0, 0.0], [0.5, 0.0, 0.5]])
    d_a = (experiment_value(prior5, task_a, a5)
           - experiment_value(prior5, task_a, b5))
    d_b = (experiment_value(prior5, task_b, a5)
           - experiment_value(prior5, task_b, b5))
    assert d_a * d_b < 0, \
        f"C5 no task reversal: {d_a}, {d_b}"
    record["C5"] = {"task_a_prefers_A_by": float(d_a),
                    "task_b_prefers_A_by": float(d_b),
                    "reversal": True}

    record["statement"] = (
        "the decision-theoretic instrument layer is validated, exact "
        "experiment values on closed-form controls, garbling never "
        "raising any task value, certified detection with permutation "
        "equivalence, the binary-channel ordering reproduced across "
        "the grid, and an incomparable pair whose tasks reverse "
        "preference, the seed of GD-1; later GD experiments may now "
        "be designed against this layer")
    record["declared"] = {"feasibility_tol": FEAS_TOL,
                          "battery_size": 20, "bsc_grid": grid}
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "gd0-instrument.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("C1", record["C1"])
    print("C2 worst gain", worst_gain)
    print("C3 residuals", r_fwd, r_rev)
    print("C5 reversal", d_a, d_b)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
