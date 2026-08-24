"""XPROTO-BEAM family (F-BEAM): the mmWave beam-aging cell.

The FR2 twin of CSI aging. Certificate = the UE's reported best beam
(SSB/CSI-RS index). Consumer = the beamformed link. Under angular drift
(rotation / mobility), the reported beam ages: the true dominant direction
moves off the beam the gNB is still steering to, the beamforming gain
collapses (narrow beams), the transmission on the misaligned beam fails.
Witness = HARQ ACK/NACK. The deployed witnessed correction is Beam-Failure
Recovery (BFR): consecutive NACKs trigger a beam re-selection.

Three policies over the SAME angular track:
  naive : beam from the last periodic report, held (trust the certificate
          at its report cadence).
  bfr   : periodic report + re-select on beam failure (K consecutive NACKs)
          -- the deployed HARQ-witnessed correction (credited prior art).
  fresh : re-select every slot (no aging) -- the control (MC2).

Physics is real: a lambda/2 ULA array factor (exact) gives the beamforming
gain vs misalignment; the block decode uses the real Sionna 5G NR LDPC
BLER curves (imported from csi_sionna). Aging driver = angular velocity.

  mode "nrsionna_beam": real NR LDPC curves + exact ULA array factor.
Run on Atlas GPU 1 (venv). Emits BEAMREP-family.json.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import argparse
import json
import sys

import numpy as np

# reuse the real Sionna 5G LDPC BLER curves from the CSI cell
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "csi"))
import csi_sionna as cs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed cell constants (bars reference these; do not tune) -------
N_ANT = 16                  # ULA elements (narrow FR2 beams)
FOV_DEG = 60.0
N_BEAMS = 24                # beam codebook size
OMEGA_DPS = 300.0           # angular velocity (deg/s) -- the aging regime
REPORT_PERIOD = 20          # slots between beam reports
SLOT_S = 1e-3
DURATION_SLOT = 6000
ANG_NOISE_DEG = 1.0         # beam measurement (angle est.) noise
ANG_JITTER_DEG = 0.5        # small AR jitter on the true angle
BFR_NACK_THRESH = 2         # consecutive NACKs -> beam failure -> recover
BASE_SNR_DB = 0.0           # per-element; aligned SINR = 10log10(N_ANT)
MCS_MARGIN_DB = 2.0         # operate this far below the aligned SINR (so the
                            # fresh-beam control sits comfortably below target)
TARGET_BLER = 0.10

BEAM_ANGLES = np.linspace(-FOV_DEG, FOV_DEG, N_BEAMS)
ALIGNED_SINR = BASE_SNR_DB + 10 * np.log10(N_ANT)   # ~12 dB at N=16


def array_gain(theta_deg, beam_deg):
    """|AF|^2 of a lambda/2 ULA (unit weights) steered to beam_deg, at
    incidence theta_deg. Range 0..N_ANT^2 (N_ANT^2 at perfect alignment)."""
    n = np.arange(N_ANT)
    psi = np.pi * (np.sin(np.deg2rad(theta_deg)) - np.sin(np.deg2rad(beam_deg)))
    return float(np.abs(np.exp(1j * n * psi).sum()) ** 2)


def best_beam(theta_meas):
    return int(np.argmax([array_gain(theta_meas, b) for b in BEAM_ANGLES]))


def sinr_db(beam_idx, theta_true):
    g = array_gain(theta_true, BEAM_ANGLES[beam_idx])          # 0..N^2
    return BASE_SNR_DB + 10 * np.log10(max(g, 1e-9) / N_ANT)   # aligned -> 10log10(N)


def angle_track(rng, n):
    """Bounded angular drift (rotation) + AR jitter -- the aging process."""
    th = np.empty(n)
    a = rng.uniform(-30, 30)
    v = OMEGA_DPS * (1 if rng.random() < 0.5 else -1)
    x = 0.0
    for i in range(n):
        x = 0.9 * x + ANG_JITTER_DEG * rng.standard_normal()
        a += v * SLOT_S
        if a > 40:
            a, v = 40.0, -abs(v)
        if a < -40:
            a, v = -40.0, abs(v)
        th[i] = a + x
    return th


def run_policy(rng, theta, policy, curves, req, mcs):
    n = len(theta)
    beam = best_beam(theta[0] + rng.normal(0, ANG_NOISE_DEG))
    nack = 0
    seen = set()
    loss = 0.0
    consec = 0
    for i in range(n):
        report = (policy == "fresh" or i % REPORT_PERIOD == 0
                  or (policy == "bfr" and consec >= BFR_NACK_THRESH))
        if report:
            beam = best_beam(theta[i] + rng.normal(0, ANG_NOISE_DEG))
            consec = 0
        seen.add(beam)
        s = sinr_db(beam, theta[i])
        loss += ALIGNED_SINR - s                       # beamforming gain lost
        is_nack = rng.random() < cs.bler_at(curves, mcs, s)   # real LDPC BLER
        if is_nack:
            nack += 1
            consec += 1
        else:
            consec = 0
    return {"bler": nack / n, "beam_var": len(seen), "beam_loss_db": loss / n}


def run_cell(seed, curves, req):
    rng = np.random.default_rng(seed)
    theta = angle_track(rng, DURATION_SLOT)                    # one track shared
    # fixed MCS: most aggressive supportable at (aligned SINR - margin), to
    # isolate the BEAM certificate (MCS is not the variable under test) and
    # keep the fresh-beam control below target.
    cand = np.where(req <= ALIGNED_SINR - MCS_MARGIN_DB)[0]
    mcs = int(cand[-1]) if cand.size else 0
    naive = run_policy(np.random.default_rng(seed * 10 + 1), theta, "naive", curves, req, mcs)
    bfr = run_policy(np.random.default_rng(seed * 10 + 2), theta, "bfr", curves, req, mcs)
    fresh = run_policy(np.random.default_rng(seed * 10 + 3), theta, "fresh", curves, req, mcs)
    return {
        "seed": int(seed), "mode": "nrsionna_beam", "omega_dps": OMEGA_DPS,
        "report_period": REPORT_PERIOD, "n_ant": N_ANT, "mcs": mcs,
        "naive_bler": float(round(naive["bler"], 4)),
        "bfr_bler": float(round(bfr["bler"], 4)),
        "fresh_bler": float(round(fresh["bler"], 4)),
        "beam_loss_db": float(round(naive["beam_loss_db"], 3)),
        "n_slot": DURATION_SLOT, "beam_var": int(naive["beam_var"]),
        "target_bler": TARGET_BLER,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "BEAMREP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC BLER curves (Sionna)...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    cells = []
    for seed in args.seeds:
        c = run_cell(seed, curves, req)
        cells.append(c)
        print(f"seed {seed}: naive_bler={c['naive_bler']} bfr_bler={c['bfr_bler']} "
              f"fresh_bler={c['fresh_bler']} beam_loss={c['beam_loss_db']}dB "
              f"beam_var={c['beam_var']} mcs={c['mcs']}", flush=True)
    rec = {
        "family": "F-BEAM", "mode": "nrsionna_beam",
        "sim_is_code_validation_not_evidence": False,
        "constants": {
            "n_ant": N_ANT, "n_beams": N_BEAMS, "omega_dps": OMEGA_DPS,
            "report_period": REPORT_PERIOD, "duration_slot": DURATION_SLOT,
            "target_bler": TARGET_BLER, "bfr_nack_thresh": BFR_NACK_THRESH,
            "substrate": ("exact lambda/2 ULA array factor (beamforming gain vs "
                          "angular misalignment) + real 5G NR LDPC BLER curves "
                          "(Sionna, imported from csi_sionna); angular-drift aging"),
        },
        "cells": cells,
    }
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
