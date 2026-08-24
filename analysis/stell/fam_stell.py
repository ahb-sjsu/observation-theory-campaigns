"""XPROTO-STELL family (F-STELL) -- PROTOTYPE: consumer-relative vacuity of the
quasi-symmetry certificate in stellarator design, on the qsc near-axis substrate.

Stellarator optimization minimizes a quasi-symmetry (QS) residual -- an aggregate
field-shape proxy. But the CONSUMER is a buildable device that must confine a finite
volume: it reads the usable-surface radius and the coil-buildable elongation, which
QS optimization is blind to. A QS-certified configuration **false-clears** when its
QS residual is excellent but the consumer metrics fail -- the reconstruction-vs-
consumer dissociation (the book's VALUE thesis) in magnetic-confinement design.

  * consumer = a reactor: needs usable volume (r_singularity) + buildable coils
    (bounded elongation).
  * certificate = QS residual (B20_variation) below threshold -> "good stellarator".
  * witness = the geometry the consumer actually reads (r_singularity, elongation).
  * naive: certify on QS alone; aware: certify on the consumer footprint too.

Substrate: qsc (pyQSC, Landreman) near-axis QS construction -- real, standard, fast.
PROTOTYPE: demonstrates the effect; hardening to a sealed cell (prereg + checker)
follows if it holds. Emits STELLREP-family.json.
"""
from __future__ import annotations

import argparse
import json
import os
import warnings

import numpy as np

warnings.filterwarnings("ignore")
from qsc import Qsc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

BASES = ["precise QA", "precise QH"]
N_PER_BASE = 40
PERTURB = 0.06             # relative perturbation of near-axis params
TAU_QS = 0.06             # QS certificate threshold (B20_variation)
R_MIN = 0.33              # consumer: usable-surface radius floor
E_MAX = 6.0              # consumer: coil-buildable elongation ceiling


def _family(base_name, n, rng):
    base = Qsc.from_paper(base_name, order="r2")
    rows = []
    for _ in range(n):
        rc = base.rc * (1 + PERTURB * rng.standard_normal(len(base.rc)))
        zs = base.zs * (1 + PERTURB * rng.standard_normal(len(base.zs)))
        etabar = base.etabar * (1 + PERTURB * rng.standard_normal())
        B2c = base.B2c + PERTURB * abs(base.etabar) * rng.standard_normal()
        try:
            q = Qsc(rc=rc, zs=zs, nfp=base.nfp, etabar=etabar, B2c=B2c,
                    p2=base.p2, order="r2", nphi=base.nphi)
            qs = float(q.B20_variation); rs = float(q.r_singularity)
            el = float(q.max_elongation)
            if not (np.isfinite(qs) and np.isfinite(rs) and np.isfinite(el)):
                continue
            rows.append((qs, rs, el))
        except Exception:
            continue
    return rows


def run_cell(seed):
    rng = np.random.default_rng(seed)
    rows = []
    for b in BASES:
        rows += _family(b, N_PER_BASE, rng)
    rows = np.array(rows)                      # cols: B20_var, r_singularity, elongation
    qs, rs, el = rows[:, 0], rows[:, 1], rows[:, 2]
    qs_cert = qs < TAU_QS                       # naive: QS certificate clears
    consumer_ok = (rs >= R_MIN) & (el <= E_MAX)  # witness: consumer actually served
    naive_fc = float((qs_cert & ~consumer_ok).sum() / max(1, qs_cert.sum()))
    aware_fc = 0.0                              # aware reads the consumer footprint
    # rank dissociation: does QS ranking predict the consumer ranking?
    from numpy import argsort
    r_qs = argsort(argsort(qs)); r_cons = argsort(argsort(-(rs - el / 20)))  # consumer FoM
    spearman = float(np.corrcoef(r_qs, r_cons)[0, 1])
    return {
        "seed": int(seed), "mode": "qsc-nearaxis",
        "naive_fc": round(naive_fc, 4), "aware_fc": round(aware_fc, 4),
        "qs_certified_frac": round(float(qs_cert.mean()), 4),
        "consumer_ok_frac": round(float(consumer_ok.mean()), 4),
        "qs_vs_consumer_rank_corr": round(spearman, 4),   # ~0 => dissociation (the flip)
        "n_configs": int(len(rows)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "STELLREP-family.json"))
    args = ap.parse_args()
    print("building qsc near-axis families (real QS construction)...", flush=True)
    cells = [run_cell(s) for s in args.seeds]
    for c in cells:
        print(f"seed {c['seed']}: naive_fc={c['naive_fc']} | qs_cert={c['qs_certified_frac']} "
              f"consumer_ok={c['consumer_ok_frac']} rank_corr={c['qs_vs_consumer_rank_corr']} "
              f"n={c['n_configs']}", flush=True)
    rec = {"family": "F-STELL", "mode": "qsc-nearaxis", "prototype": True,
           "constants": {"bases": BASES, "n_per_base": N_PER_BASE, "perturb": PERTURB,
                         "tau_qs": TAU_QS, "r_min": R_MIN, "e_max": E_MAX,
                         "substrate": "qsc (pyQSC) near-axis QS stellarators; consumer = "
                                      "usable volume (r_singularity) + buildable elongation"},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
