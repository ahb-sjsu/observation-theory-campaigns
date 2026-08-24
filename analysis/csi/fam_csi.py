"""XPROTO-CSI family (F-CSI): the 5G/6G CSI-aging cell + a synthetic
fading simulator for validating the grading logic before the RFsim
substrate.

Certificate = the UE's CQI report, which drives the gNB's MCS choice
(target BLER 10%). Consumer = the UE's link. False-clear = a HARQ NACK:
the CQI-chosen MCS was implicitly certified "supportable," but the
transmission on the AGED channel failed. Witness = HARQ ACK/NACK, the
independent ground truth of whether the consumer decoded.

Two policies over the SAME channel realization:
  naive : MCS from the raw reported CQI (trust the certificate at its
          fixed report cadence)
  olla  : MCS from CQI + a HARQ-driven SINR offset (Outer-Loop Link
          Adaptation -- the deployed HARQ-WITNESSED correction; converges
          BLER to target). Credited prior art; OT's delta is calibrating
          the false-clear rate + the derivable refresh floor.
  fresh : a control -- CQI every TTI (no aging), to show the link
          adaptation is sane when CSI is fresh (MC2).

Claim: raw CQI is measurably vacuous under aging (BLER >> target) while
the witnessed policy holds BLER at target; and the aging is real
(consumer-relative, set by the UE's Doppler / coherence time).

  mode="sim"   : synthetic correlated-fading channel. Validates the CODE
                 and calibrates bars. NOT evidence about real 5G.
  mode="rfsim" : read per-transmission logs from srsRAN / OpenAirInterface
                 RFsim (see SUBSTRATE.md). The sealed measurement.

    python3 fam_csi.py --sim              # grading-logic validation
    python3 fam_csi.py --sim --seeds 7 8  # exploration
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- sealed cell constants (bars reference these; do not tune) -------
TTI_S = 0.001
MEAN_SINR_DB = 12.0
SIGMA_SINR_DB = 4.0
FD_HZ = 200.0            # Doppler (high mobility) -- the aging regime
REPORT_PERIOD = 20       # TTIs between CQI reports (aging bites at 200 Hz)
CQI_NOISE_DB = 1.0
TARGET_BLER = 0.10
DURATION_TTI = 6000
W_CURVE_DB = 1.0                          # BLER curve steepness
SINR50_DB = [-6 + 2 * i for i in range(15)]   # per-MCS SINR for 50% BLER
OLLA_UP_DB = 0.1                          # offset step per ACK
OLLA_DOWN_DB = OLLA_UP_DB * (1 - TARGET_BLER) / TARGET_BLER  # equilibrium=target


def bler(m: int, sinr_db: float) -> float:
    return 0.5 * math.erfc((sinr_db - SINR50_DB[m]) / (math.sqrt(2) * W_CURVE_DB))


def select_mcs(sinr_est_db: float) -> int:
    best = 0
    for m in range(len(SINR50_DB)):
        if bler(m, sinr_est_db) <= TARGET_BLER:
            best = m
    return best


def _channel(rng: random.Random, fd: float, n: int) -> list[float]:
    """AR(1) SINR trace with coherence time Tcoh = 0.423/fd (Clarke);
    correlation exp(-TTI/Tcoh) per step."""
    tcoh = 0.423 / fd
    rho = math.exp(-TTI_S / tcoh)
    a = math.sqrt(max(0.0, 1 - rho * rho))
    x = rng.gauss(0, 1)
    out = []
    for _ in range(n):
        x = rho * x + a * rng.gauss(0, 1)
        out.append(MEAN_SINR_DB + SIGMA_SINR_DB * x)
    return out


def _policy(rng: random.Random, sinr: list[float], policy: str,
            report_period: int) -> dict:
    est = sinr[0]
    offset = 0.0
    nacks = 0
    mcs_seen = set()
    errsum = 0.0
    for n, s in enumerate(sinr):
        if policy == "fresh" or n % report_period == 0:
            est = s + rng.gauss(0, CQI_NOISE_DB)
        eff = est + (offset if policy == "olla" else 0.0)
        m = select_mcs(eff)
        nack = rng.random() < bler(m, s)          # HARQ on the AGED channel
        mcs_seen.add(m)
        errsum += abs(s - est)
        if nack:
            nacks += 1
        if policy == "olla":
            offset += (-OLLA_DOWN_DB if nack else OLLA_UP_DB)
    n = len(sinr)
    return {"bler": nacks / n, "mcs_var": len(mcs_seen), "cqi_err_db": errsum / n}


def run_cell(seed: int, fd: float = FD_HZ, report_period: int = REPORT_PERIOD,
             duration: int = DURATION_TTI, mode: str = "sim") -> dict:
    if mode == "rfsim":
        return load_rfsim(seed)
    rng = random.Random(seed)
    sinr = _channel(rng, fd, duration)        # one channel; policies share it
    naive = _policy(rng, sinr, "naive", report_period)
    olla = _policy(rng, sinr, "olla", report_period)
    fresh = _policy(rng, sinr, "fresh", report_period)
    return {
        "seed": seed, "mode": mode, "fd_hz": fd, "report_period": report_period,
        "naive_bler": round(naive["bler"], 4),      # false-clear of raw CQI
        "olla_bler": round(olla["bler"], 4),        # HARQ-witnessed
        "fresh_bler": round(fresh["bler"], 4),      # MC2 control (fresh CSI)
        "cqi_err_db": round(naive["cqi_err_db"], 3),  # MC1 aging severity
        "n_tti": duration, "mcs_var": naive["mcs_var"],
        "target_bler": TARGET_BLER,
    }


def load_rfsim(seed: int):
    """Read per-transmission logs from an srsRAN/OAI RFsim run for a graded
    seed and reduce them to the same metrics. Schema (JSONL, SUBSTRATE.md):
      rfsim/seed_<seed>/<policy>/tx.jsonl  {"cqi","mcs","ack": true/false}
    for policy in {naive, olla, fresh}. BLER = NACK fraction; cqi_err from
    the reported-vs-realized SINR if logged. Raises if absent."""
    base = os.path.join(HERE, "rfsim", f"seed_{seed}")
    if not os.path.isdir(base):
        raise FileNotFoundError(
            f"RFsim logs missing: {base} — run srsRAN/OAI RFsim (SUBSTRATE.md)")
    def bler_of(policy):
        rows = [json.loads(l) for l in
                open(os.path.join(base, policy, "tx.jsonl")) if l.strip()]
        nack = sum(1 for r in rows if not r["ack"])
        return nack / max(1, len(rows)), len(rows)
    nb, n = bler_of("naive")
    ob, _ = bler_of("olla")
    fb, _ = bler_of("fresh")
    return {"seed": seed, "mode": "rfsim", "fd_hz": FD_HZ,
            "report_period": REPORT_PERIOD, "naive_bler": round(nb, 4),
            "olla_bler": round(ob, 4), "fresh_bler": round(fb, 4),
            "cqi_err_db": 99.0, "n_tti": n, "mcs_var": 2,
            "target_bler": TARGET_BLER}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", action="store_true",
                    help="synthetic fading validation (NOT evidence about real 5G)")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default="CSI-SIM-validation.json")
    args = ap.parse_args()
    mode = "sim" if args.sim else "rfsim"
    cells = []
    for seed in args.seeds:
        c = run_cell(seed, mode=mode)
        cells.append(c)
        print(f"seed {seed}: naive_bler={c['naive_bler']} olla_bler={c['olla_bler']} "
              f"fresh_bler={c['fresh_bler']} (target {c['target_bler']}) "
              f"cqi_err={c['cqi_err_db']}dB mcs_var={c['mcs_var']}", flush=True)
    rec = {"family": "F-CSI", "mode": mode,
           "sim_is_code_validation_not_evidence": (mode == "sim"),
           "constants": {"fd_hz": FD_HZ, "report_period": REPORT_PERIOD,
                         "target_bler": TARGET_BLER, "mean_sinr_db": MEAN_SINR_DB,
                         "duration_tti": DURATION_TTI},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
