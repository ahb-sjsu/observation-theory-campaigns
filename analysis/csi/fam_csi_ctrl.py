"""XPROTO-CSI-CTRL family (F-CSI-CTRL): a coherence-floor-driven adaptive CSI-reporting
CONTROLLER, evaluated on the reliability x feedback-overhead Pareto against fixed
periodicity (current practice, TR 38.214).

SUPERSEDED PREMISE (annotated 2026-08-27). The graded verdict for this cell is VOID
(SEALS.md, 2026-08-26), so no result from it stands. Separately, its premise is now
refuted: kappa = 0.177 came from csi_sweep.py, an exploration that was never sealed and
that measured its floors at a relaxed 0.15 BLER threshold while reporting against a 0.10
target. The sealed recompute XPROTO-CSI-SWEEP2 (2026-08-27) finds no proportional law at
the true budget. The sealed prereg and the graded records are immutable and are left as
executed. Do not build a new cell on kappa without redesigning against SWEEP2.

The technique operationalizes a coherence-proportional refresh floor: set the CSI report
period from the estimated coherence time, P*(f_D) = clamp(round(kappa * T_coh / TTI)),
kappa = 0.177 (see the note above; this is the superseded slope, retained so the family
reproduces as executed). This is mobility-adaptive rather than a fixed cadence. We compare
it against fixed periods on a Doppler sweep: the adaptive controller should meet the BLER
target at every mobility (like the safest fixed period P=1) while spending far less
feedback at low mobility, and unlike a low-overhead fixed period it never false-clears at
high mobility.

Real Sionna 5G NR LDPC curves + TDL-A fading (via csi_sionna); empirical HARQ NACK rate.
Run on Atlas. Emits CTRLREP-family.json.
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import csi_sionna as cs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TTI_MS = 1.0
TARGET = 0.10
KAPPA = 0.177               # superseded slope, kept for reproduction; see docstring
PMAX = 80
CQI_NOISE_DB = 1.0
DURATION = 6000
FDS = [5, 10, 25, 50, 100, 200, 400]   # Doppler (Hz), low -> high mobility
FIXED = [1, 10, 40, 80]                # fixed-period baselines (TTI)


THETA_DB = 2.0             # send-on-delta threshold (the consumer knob; a bias voltage)


def adaptive_period(fd):
    tcoh_ms = 0.423 / fd * 1000.0
    return int(min(PMAX, max(1, round(KAPPA * tcoh_ms / TTI_MS))))


def bler_of(snr, curves, req, period, seed):
    """Empirical HARQ NACK rate of a held-CSI naive certificate at fixed report `period`."""
    rng = np.random.default_rng(seed)
    est = snr[0]
    nack = 0
    for n, s in enumerate(snr):
        if n % period == 0:
            est = s + rng.normal(0, CQI_NOISE_DB)
        cand = np.where(req <= est)[0]
        m = int(cand[-1]) if len(cand) else 0
        if rng.random() < cs.bler_at(curves, m, s):
            nack += 1
    return nack / len(snr)


def bler_sod(snr, curves, req, theta, seed):
    """Send-on-delta (event-triggered) reporting: report only when the live channel has
    drifted from the last reported value by > theta dB (a S/H + comparator in analog).
    Returns (BLER, overhead, effective period P_eff = T / reports)."""
    rng = np.random.default_rng(seed)
    est = snr[0]
    last = snr[0]
    nack = 0
    reports = 1
    for s in snr:
        if abs(s - last) > theta:              # level crossing -> fire a report
            est = s + rng.normal(0, CQI_NOISE_DB)
            last = s
            reports += 1
        cand = np.where(req <= est)[0]
        m = int(cand[-1]) if len(cand) else 0
        if rng.random() < cs.bler_at(curves, m, s):
            nack += 1
    n = len(snr)
    return nack / n, reports / n, n / reports


def run_cell(seed, curves, req):
    out = {}
    for fd in FDS:
        cs.FD_HZ = fd                          # csi_sionna.fading_snr reads FD_HZ
        snr = cs.fading_snr(seed, DURATION)
        tcoh_ms = 0.423 / fd * 1000.0
        pa = adaptive_period(fd)
        sb, so, peff = bler_sod(snr, curves, req, THETA_DB, seed)
        rec = {"tcoh_ms": round(tcoh_ms, 2),
               "adaptive": {"P": pa, "bler": round(bler_of(snr, curves, req, pa, seed), 4),
                            "overhead": round(1.0 / pa, 4)},
               "sod": {"theta_db": THETA_DB, "bler": round(sb, 4),
                       "overhead": round(so, 4), "p_eff": round(peff, 2)}}
        for p in FIXED:
            rec[f"fixed{p}"] = {"P": p, "bler": round(bler_of(snr, curves, req, p, seed), 4),
                                "overhead": round(1.0 / p, 4)}
        out[str(fd)] = rec
    return {"seed": int(seed), "mode": "nrsionna", "fds": FDS, "target": TARGET,
            "kappa": KAPPA, "theta_db": THETA_DB, "sweep": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "CTRLREP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    cells = [run_cell(s, curves, req) for s in args.seeds]
    for c in cells:
        row = " ".join(f"{fd}:P{c['sweep'][str(fd)]['adaptive']['P']}"
                       f"/a{c['sweep'][str(fd)]['adaptive']['bler']:.3f}"
                       f"/f40_{c['sweep'][str(fd)]['fixed40']['bler']:.3f}" for fd in FDS)
        print(f"seed {c['seed']} (fd:Padapt/bler_a/bler_fixed40): {row}", flush=True)
    rec = {"family": "F-CSI-CTRL", "mode": "nrsionna",
           "constants": {"fds": FDS, "fixed": FIXED, "kappa": KAPPA, "target": TARGET,
                         "duration": DURATION, "pmax": PMAX,
                         "substrate": "real Sionna 5G NR LDPC curves + TDL-A fading"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
