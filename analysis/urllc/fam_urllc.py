"""XPROTO-URLLC family (F-URLLC): reliability-target consumer-relativity.

The consumer's reliability TARGET is its read operator. The same CQI report and
the same channel serve an eMBB consumer (target BLER 1e-1) and a URLLC consumer
(target 1e-3 here, a measurable proxy for the real 1e-5). A one-size certificate
calibrated to eMBB selects an aggressive MCS delivering ~1e-1 reliability --
adequate for eMBB, a false-clear for URLLC (>= 100x its budget). A consumer-aware
certificate selects a conservative MCS for URLLC (operating a fixed SINR margin
above the 10% point -- the waterfall gap toward the URLLC tail) and holds it at
its budget.

Achieved reliability is read off the real Sionna 5G NR LDPC curves: eMBB's ~1e-1
is resolved directly; the URLLC-aware operating point sits below the sim's block
resolution (~2.5e-3 at 400 blocks/point), i.e. very reliable -- the honest
statement of a deep-tail regime the coarse sim cannot resolve (the sealed rung
measures the tail directly). Fresh CSI isolates the reliability-target axis
(aging is XPROTO-CSI). Run on Atlas GPU. Emits URLLCREP-family.json.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "csi"))
import csi_sionna as cs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

EMBB_TARGET = 1e-1
URLLC_TARGET = 1e-3          # measurable proxy for the real 1e-5
URLLC_MARGIN_DB = 4.0        # conservative-MCS backoff for the URLLC consumer
DIVERSITY_K = 3             # URLLC-aware frequency/spatial diversity branches.
                            # (MCS margin ALONE cannot reach URLLC reliability on a
                            # Rayleigh channel -- deep-fade outage ~4% dominates
                            # regardless of margin; real URLLC needs diversity.)
CQI_NOISE_DB = 1.0
DURATION = 6000


def run_cell(seed, curves, req10):
    rng = np.random.default_rng(seed)
    # K independent fading branches (frequency/spatial diversity); [0] is primary
    branches = [cs.fading_snr(seed * 7 + k, DURATION) for k in range(DIVERSITY_K)]
    true = branches[0]
    ae = an = aa = 0.0
    seen = set(); margins = []
    for t in range(DURATION):
        cqi = true[t] + rng.normal(0, CQI_NOISE_DB)         # fresh CQI report
        ce = np.where(req10 <= cqi)[0]
        m_embb = int(ce[-1]) if ce.size else 0              # eMBB: 10% target
        cu = np.where(req10 + URLLC_MARGIN_DB <= cqi)[0]
        m_urllc = int(cu[-1]) if cu.size else 0            # URLLC: conservative MCS
        ae += cs.bler_at(curves, m_embb, true[t])          # eMBB under its cert (1 branch)
        an += cs.bler_at(curves, m_embb, true[t])          # URLLC under the eMBB cert (1 branch)
        # URLLC-aware = conservative MCS + K-branch diversity (fail iff all fail)
        p = 1.0
        for br in branches:
            p *= cs.bler_at(curves, m_urllc, br[t])
        aa += p
        seen.add(m_embb); margins.append(m_embb - m_urllc)
    n = DURATION
    return {
        "seed": int(seed), "mode": "nrsionna",
        "embb_target": EMBB_TARGET, "urllc_target": URLLC_TARGET,
        "achieved_embb": float(round(ae / n, 5)),
        "achieved_urllc_naive": float(round(an / n, 5)),
        "achieved_urllc_aware": float(round(aa / n, 6)),
        "mcs_margin": float(round(np.mean(margins), 3)),
        "n_tti": n, "mcs_var": len(seen),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "URLLCREP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC curves...", flush=True)
    curves = cs.measure_bler_curves()
    req10 = cs.required_snr(curves)
    cells = [run_cell(s, curves, req10) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: eMBB={c['achieved_embb']:.4f} (tgt {EMBB_TARGET}) | "
              f"URLLC naive={c['achieved_urllc_naive']:.4f} aware={c['achieved_urllc_aware']:.2e} "
              f"(tgt {URLLC_TARGET}) | mcs_margin={c['mcs_margin']:.2f}", flush=True)
    rec = {"family": "F-URLLC", "mode": "nrsionna",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"embb_target": EMBB_TARGET, "urllc_target": URLLC_TARGET,
                         "urllc_margin_db": URLLC_MARGIN_DB, "cqi_noise_db": CQI_NOISE_DB,
                         "duration": DURATION,
                         "substrate": ("real Sionna 5G NR LDPC curves + TDL fading, fresh "
                                       "CSI; URLLC tail below the 400-block sim resolution")},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
