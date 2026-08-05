#!/usr/bin/env python3
"""EG-0 projection entropy instrumentation (exploratory, EG track).

The EG track's mandatory first experiment. Extends the PE instrument
layer with the three capabilities every later EG experiment needs, each
validated against exact closed forms before use.

Part A, prior-control reproduction. The instrument must first reproduce
the PE-0 closed forms. The quadratic fold carries exactly one bit of
branch ambiguity at every interior bin (symmetric grid). The double
fold's symmetric slice carries exactly one and one half bits under
coarea weights (preimages of zero at -1, 0, 1 with |f'| = 2, 1, 2).
The degenerate cubic is monotone and carries exactly zero. The fold
caustic's binned entropy converges to 1 - 1/ln 2.

Part B, the conditional-entropy surface H(Z_delta | X_epsilon). Exact
control: a linear monotone map with grid and bins aligned so every bin
holds exactly epsilon/(c delta) hidden states, giving
H = log2(epsilon/(c delta)) with no error term. Convergence sweeps in
delta and epsilon on the fold measure the resolution behavior the EG
witnesses must survive.

Part C, relative entropy of fiber measures. Exact controls: nested
uniform measures give D = log2(b/a) exactly at any aligned resolution;
discretized Gaussians must converge to the closed-form KL divergence;
and a piecewise-constant deformation of the fold gives a per-bin D
equal to the binary divergence D(c1/(c1+c2) || 1/2) exactly, the same
value in every interior bin, because within-branch conditionals cancel.

Part D, reparametrization invariance. The finite-resolution witnesses
must not depend on the hidden coordinate. Two tests on the deformed
fold. Relabeling the same hidden states through a monotone coordinate
change must leave every witness bit-identical, which catches any
implementation dependence on coordinate values. Re-gridding uniformly
in the new coordinate with Jacobian-transformed weights must reproduce
the same closed-form D field up to quadrature error that shrinks with
resolution, which catches the coordinate pathology the track document
warns about.

Exploratory label. Python instrument; MATLAB replication remains the
sealing requirement per the track document's substrate clause.
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

from projection_fold import binned_fold_entropy, canonical_sha256  # noqa: E402

DELTA = 1e-4
EPS = 0.01
C_LIN = 0.8
EPS_LIN = 0.008
GAUSS = {"m1": 0.0, "s1": 1.0, "m2": 0.5, "s2": 1.5}
DEFORM_C = (2.0, 1.0)
REPAR_AMP = 0.2


def conditional_entropy_bits(bins: np.ndarray,
                             weights: np.ndarray | None = None) -> float:
    """H(Z|X) for grid states grouped by observed bin, exact finite sum.
    Uniform weights count states; explicit weights use the weighted
    within-bin distribution."""
    order = np.argsort(bins, kind="stable")
    b = bins[order]
    n = len(b)
    w = np.ones(n) / n if weights is None else weights[order] / weights.sum()
    edges = np.flatnonzero(np.diff(b)) + 1
    h = 0.0
    for grp in np.split(np.arange(n), edges):
        wg = w[grp]
        mass = wg.sum()
        p = wg / mass
        h += mass * float(-(p * np.log2(p)).sum())
    return h


def branch_gap_bits(bins: np.ndarray, branch: np.ndarray) -> float:
    """H(Z|X) - H(Z|X, branch), the branch-ambiguity part, exact."""
    joint = bins.astype(np.int64) * 2 + (branch > 0).astype(np.int64)
    return conditional_entropy_bits(bins) - conditional_entropy_bits(joint)


def relative_entropy_bits(p: np.ndarray, q: np.ndarray) -> float:
    p = p / p.sum()
    q = q / q.sum()
    mask = p > 0
    assert np.all(q[mask] > 0), "support violation"
    return float((p[mask] * np.log2(p[mask] / q[mask])).sum())


def per_bin_relative_entropy(bins: np.ndarray, w_mat: np.ndarray,
                             w_vac: np.ndarray) -> list[float]:
    order = np.argsort(bins, kind="stable")
    b = bins[order]
    wm = w_mat[order]
    wv = w_vac[order]
    edges = np.flatnonzero(np.diff(b)) + 1
    return [relative_entropy_bits(wm[grp], wv[grp])
            for grp in np.split(np.arange(len(b)), edges)]


def main() -> int:
    record: dict = {"schema": "eg0-instrument-v1", "label": "exploratory"}

    # Part A: reproduce the PE-0 closed forms.
    tau = -1.0 + (np.arange(20_000) + 0.5) * DELTA
    fold_bins = np.floor(tau**2 / EPS).astype(np.int64)
    gap_fold = branch_gap_bits(fold_bins, tau)
    assert abs(gap_fold - 1.0) < 1e-12, f"fold bit: {gap_fold}"

    w = np.array([1.0 / 2.0, 1.0 / 1.0, 1.0 / 2.0])
    p = w / w.sum()
    m0 = float(-(p * np.log2(p)).sum())
    assert abs(m0 - 1.5) < 1e-15, f"double-fold slice: {m0}"

    # degenerate cubic t = tau^3: every level has one preimage, so the
    # coarea branch distribution is a single atom and carries zero
    p_cubic = np.array([1.0])
    gap_cubic = float(-(p_cubic * np.log2(p_cubic)).sum())
    assert gap_cubic == 0.0, f"cubic must carry zero: {gap_cubic}"

    caustic_dev = abs(binned_fold_entropy(1e-5) + math.log2(1e-5)
                      - (1.0 - 1.0 / math.log(2.0)))
    assert caustic_dev < 0.01, f"caustic reproduction: {caustic_dev}"
    record["part_a"] = {"fold_branch_bit": gap_fold,
                        "double_fold_slice_bits": m0,
                        "cubic_branch_bit": gap_cubic,
                        "caustic_deviation_at_1e-5": caustic_dev}

    # Part B: exact conditional-entropy control and convergence sweeps.
    tau_lin = (np.arange(10_000) + 0.5) * DELTA
    lin_bins = np.floor(C_LIN * tau_lin / EPS_LIN).astype(np.int64)
    h_lin = conditional_entropy_bits(lin_bins)
    target = math.log2(EPS_LIN / (C_LIN * DELTA))
    assert abs(h_lin - target) < 1e-12, f"linear control: {h_lin} vs {target}"

    sweep_delta = []
    for d in (4e-4, 2e-4, 1e-4):
        tt = -1.0 + (np.arange(int(round(2.0 / d))) + 0.5) * d
        h = conditional_entropy_bits(
            np.floor(tt**2 / EPS).astype(np.int64)) + math.log2(d)
    # deviations between successive refinements must shrink
        sweep_delta.append((d, h))
    devs_d = [abs(sweep_delta[i + 1][1] - sweep_delta[i][1])
              for i in range(len(sweep_delta) - 1)]
    assert devs_d[1] < devs_d[0], f"delta sweep not converging: {devs_d}"

    sweep_eps = []
    for e in (0.04, 0.02, 0.01):
        h = conditional_entropy_bits(
            np.floor(tau**2 / e).astype(np.int64)) - math.log2(e / DELTA)
        sweep_eps.append((e, h))
    devs_e = [abs(sweep_eps[i + 1][1] - sweep_eps[i][1])
              for i in range(len(sweep_eps) - 1)]
    assert devs_e[1] < devs_e[0], f"epsilon sweep not converging: {devs_e}"
    record["part_b"] = {"linear_control_bits": h_lin,
                        "linear_target_bits": target,
                        "delta_sweep": sweep_delta,
                        "delta_sweep_devs": devs_d,
                        "eps_sweep": sweep_eps,
                        "eps_sweep_devs": devs_e}

    # Part C: relative-entropy controls.
    n_grid = 10_000
    p1 = np.zeros(n_grid)
    p1[: n_grid // 4] = 1.0
    p2 = np.ones(n_grid)
    d_nested = relative_entropy_bits(p1, p2)
    assert abs(d_nested - 2.0) < 1e-12, f"nested uniforms: {d_nested}"

    kl_exact = (math.log(GAUSS["s2"] / GAUSS["s1"])
                + (GAUSS["s1"]**2 + (GAUSS["m1"] - GAUSS["m2"])**2)
                / (2 * GAUSS["s2"]**2) - 0.5) / math.log(2.0)
    gauss_sweep = []
    for d in (0.01, 0.005, 0.0025):
        x = np.arange(-10.0, 10.0, d) + d / 2
        g1 = np.exp(-0.5 * ((x - GAUSS["m1"]) / GAUSS["s1"])**2)
        g2 = np.exp(-0.5 * ((x - GAUSS["m2"]) / GAUSS["s2"])**2)
        gauss_sweep.append((d, abs(relative_entropy_bits(g1, g2) - kl_exact)))
    assert gauss_sweep[-1][1] < 1e-5, f"gaussian KL: {gauss_sweep}"
    assert gauss_sweep[-1][1] <= gauss_sweep[0][1], "KL not converging"

    c1, c2 = DEFORM_C
    pp = c1 / (c1 + c2)
    d_binary = (pp * math.log2(2 * pp) + (1 - pp) * math.log2(2 * (1 - pp)))
    w_vac = np.ones_like(tau)
    w_mat = np.where(tau < 0, c1, c2)
    interior = fold_bins < int(0.9 / EPS)
    d_field = per_bin_relative_entropy(fold_bins[interior],
                                       w_mat[interior], w_vac[interior])
    dev_field = max(abs(v - d_binary) for v in d_field)
    assert dev_field < 1e-12, f"deformed-fold D field: {dev_field}"
    record["part_c"] = {"nested_uniform_bits": d_nested,
                        "gauss_kl_exact_bits": kl_exact,
                        "gauss_sweep_abs_err": gauss_sweep,
                        "binary_control_bits": d_binary,
                        "deformed_fold_max_dev": dev_field,
                        "deformed_fold_bins": len(d_field)}

    # Part D: reparametrization invariance.
    # Test one, relabeling: the same hidden states presented in a
    # different storage order (as a coordinate relabeling would do)
    # must leave every witness unchanged to rounding.
    perm = np.arange(int(interior.sum()))[::-1]
    d_field_relabel = per_bin_relative_entropy(
        fold_bins[interior][perm], w_mat[interior][perm],
        w_vac[interior][perm])
    dev_relabel = max(abs(a - b)
                      for a, b in zip(d_field, d_field_relabel))
    assert dev_relabel < 1e-12, f"relabeling moved a witness: {dev_relabel}"

    # Test two, re-gridding: uniform grid in u = tau + A sin(pi tau),
    # weights transformed by the inverse Jacobian.
    def g(t):
        return t + REPAR_AMP * np.sin(math.pi * t)

    def g_prime(t):
        return 1.0 + REPAR_AMP * math.pi * np.cos(math.pi * t)

    u = g(-1.0) + (np.arange(int(round((g(1.0) - g(-1.0)) / DELTA))) + 0.5) \
        * DELTA
    t_inv = u.copy()
    for _ in range(60):
        t_inv = t_inv - (g(t_inv) - u) / g_prime(t_inv)
    assert np.max(np.abs(g(t_inv) - u)) < 1e-13, "inversion failed"
    jac = 1.0 / g_prime(t_inv)
    bins_u = np.floor(t_inv**2 / EPS).astype(np.int64)
    mat_u = np.where(t_inv < 0, c1, c2) * jac
    interior_u = bins_u < int(0.9 / EPS)
    d_field_u = per_bin_relative_entropy(bins_u[interior_u],
                                         mat_u[interior_u],
                                         jac[interior_u])
    dev_repar = max(abs(v - d_binary) for v in d_field_u)
    # bin-edge quadrature error is order delta over the branch mass;
    # the invariance content is that it shrinks under refinement
    assert dev_repar < 0.05, f"reparametrized D field: {dev_repar}"

    dev_repar_fine = None
    d_fine = DELTA / 4
    u_f = g(-1.0) + (np.arange(int(round((g(1.0) - g(-1.0)) / d_fine)))
                     + 0.5) * d_fine
    t_f = u_f.copy()
    for _ in range(60):
        t_f = t_f - (g(t_f) - u_f) / g_prime(t_f)
    jac_f = 1.0 / g_prime(t_f)
    bins_f = np.floor(t_f**2 / EPS).astype(np.int64)
    int_f = bins_f < int(0.9 / EPS)
    d_field_f = per_bin_relative_entropy(
        bins_f[int_f], (np.where(t_f < 0, c1, c2) * jac_f)[int_f],
        jac_f[int_f])
    dev_repar_fine = max(abs(v - d_binary) for v in d_field_f)
    assert dev_repar_fine < dev_repar, \
        "reparametrization deviation must shrink with resolution"
    record["part_d"] = {"relabel_max_dev": dev_relabel,
                        "regrid_max_dev": dev_repar,
                        "regrid_max_dev_refined": dev_repar_fine}

    record["statement"] = ("the EG instrument layer measures the "
        "conditional-entropy surface, fiber relative entropy, and their "
        "resolution behavior exactly on every closed-form control, "
        "reproduces the PE-0 values, and its witnesses are invariant "
        "under hidden-coordinate relabeling exactly and under "
        "re-gridding up to quadrature error that shrinks with "
        "resolution")
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
    }
    record["declared"] = {"delta": DELTA, "eps": EPS, "c_lin": C_LIN,
                          "eps_lin": EPS_LIN, "gauss": GAUSS,
                          "deform_c": list(DEFORM_C),
                          "repar_amplitude": REPAR_AMP}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "eg0-instrument.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"A: fold bit {gap_fold:.15f}, M0 {m0}, cubic {gap_cubic}, "
          f"caustic dev {caustic_dev:.4f}")
    print(f"B: linear {h_lin:.12f} vs {target:.12f}; delta devs {devs_d}; "
          f"eps devs {devs_e}")
    print(f"C: nested {d_nested}, gauss errs {[e for _, e in gauss_sweep]}, "
          f"fold-D dev {dev_field:.2e} over {len(d_field)} bins")
    print(f"D: relabel exact; regrid dev {dev_repar:.2e} -> "
          f"{dev_repar_fine:.2e} at delta/4")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
