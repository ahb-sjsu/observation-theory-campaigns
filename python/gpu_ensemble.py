#!/usr/bin/env python3
"""Vectorized fixed-step ensemble for NRP GPU or CPU execution.

This is an acceleration path for the toy negative control, not a QED simulator.
It uses CuPy when installed and otherwise falls back to NumPy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import cupy as xp  # type: ignore
    BACKEND = "cupy"
except ImportError:
    import numpy as xp  # type: ignore
    BACKEND = "numpy"


def scalar(value):
    if BACKEND == "cupy":
        return value.item()
    return value.item() if hasattr(value, "item") else value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=100000)
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--dt", type=float, default=0.001)
    parser.add_argument("--omega-t", type=float, default=1.0)
    parser.add_argument("--omega-u", type=float, default=1.2)
    parser.add_argument("--lambda", dest="lam", type=float, default=0.1)
    parser.add_argument("--g", type=float, default=0.25)
    parser.add_argument("--field", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=20260803)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rng = xp.random.RandomState(args.seed)
    n = args.n
    t = 0.01 * rng.standard_normal(n)
    pt = 1.0 + 0.05 * rng.standard_normal(n)
    x = xp.zeros(n)
    px = 0.2 + 0.01 * rng.standard_normal(n)
    u = 0.1 + 0.05 * rng.standard_normal(n)
    pu = 0.05 * rng.standard_normal(n)
    folds = xp.zeros(n, dtype=xp.int32)
    coupling = args.g * args.field

    def forces(tt, uu):
        ft = -(args.omega_t**2) * tt - coupling * uu
        fu = -(args.omega_u**2) * uu - args.lam * uu**3 - coupling * tt
        return ft, fu

    def energy(tt, ppt, ppx, uu, ppu):
        return (
            0.5 * (ppt**2 + ppx**2 + ppu**2)
            + 0.5 * args.omega_t**2 * tt**2
            + 0.5 * args.omega_u**2 * uu**2
            + 0.25 * args.lam * uu**4
            + coupling * tt * uu
        )

    e0 = energy(t, pt, px, u, pu)
    previous_sign = xp.sign(pt)
    for _ in range(args.steps):
        ft0, fu0 = forces(t, u)
        pt_half = pt + 0.5 * args.dt * ft0
        pu_half = pu + 0.5 * args.dt * fu0
        t = t + args.dt * pt_half
        u = u + args.dt * pu_half
        x = x + args.dt * px
        ft1, fu1 = forces(t, u)
        pt = pt_half + 0.5 * args.dt * ft1
        pu = pu_half + 0.5 * args.dt * fu1
        current_sign = xp.sign(pt)
        folds += ((current_sign * previous_sign) < 0).astype(xp.int32)
        previous_sign = current_sign

    ef = energy(t, pt, px, u, pu)
    scale = xp.maximum(xp.abs(e0), 1.0)
    drift = xp.abs(ef - e0) / scale
    histogram = xp.bincount(folds, minlength=int(scalar(xp.max(folds))) + 1)
    if BACKEND == "cupy":
        histogram = xp.asnumpy(histogram)
        sample_folds = xp.asnumpy(folds[: min(1024, n)])
    else:
        sample_folds = folds[: min(1024, n)]

    record = {
        "schema": "projection-fold-ensemble-v1",
        "backend": BACKEND,
        "backend_version": xp.__version__,
        "n": n,
        "steps": args.steps,
        "dt": args.dt,
        "parameters": {
            "omega_t": args.omega_t,
            "omega_u": args.omega_u,
            "lambda": args.lam,
            "g": args.g,
            "field": args.field,
            "seed": args.seed,
        },
        "total_folds": int(scalar(xp.sum(folds))),
        "mean_folds": float(scalar(xp.mean(folds))),
        "max_folds": int(scalar(xp.max(folds))),
        "fold_histogram": [int(v) for v in histogram.tolist()],
        "max_relative_energy_drift": float(scalar(xp.max(drift))),
        "mean_relative_energy_drift": float(scalar(xp.mean(drift))),
        "sample_fold_counts": [int(v) for v in sample_folds.tolist()],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
