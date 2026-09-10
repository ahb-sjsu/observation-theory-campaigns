"""Closing annotation for the D2 line (not a gate): does the frozen D2v7 law's miss on Laplace at
N = 12000 grow with N, or sit on the limit? Laplace at d = 64 and, as the control that held, Student t
with 3 degrees at d = 64, at N = 4000, 8000, 12000 and 16000, three seeds each, the D2v9 observers, k
ladder and scope (cv_knn >= 0.015). The frozen law is applied as it stands; the error is the RMS
log-ratio in hub excess on the in-scope rows, and it is compared with the D2v9 limit 2 REF = 0.638.

    python d2_close_sweep.py <out.json>
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D2v9")
from d2v9_hubness import apply_law, run_world  # noqa: E402

LAW = json.load(open("/archive/ahb-sjsu/observation-theory-campaigns/experiments/OD/D2v9/law.json"))["law"]
TAU = 0.015; LIMIT = 2 * 0.31917215230074464
CFG = {"k_ladder": [5, 10, 20], "k_law": 10, "observer_alphas": [0.0, 0.25, 0.5, 1.0, 1.5, 2.0], "rotations_per_alpha": 2, "budget_alphas": [], "budget_ladder": []}
SEEDS = [20261019, 20261020, 20261021]
FAMILIES = {"laplace": {"family": "laplace", "params": {}}, "student3": {"family": "student", "params": {"nu": 3.0}}}
NS = [4000, 8000, 12000, 16000]


def main():
    out = {"law": LAW, "tau": TAU, "limit": LIMIT, "cells": []}
    for fam, spec in FAMILIES.items():
        for N in NS:
            for si, seed in enumerate(SEEDS):
                w = {"name": f"{fam}_d64_N{N}_s{si}", "group": "sweep", "family": spec["family"], "d": 64, "N": N, "params": spec["params"], "seed_offset": 200 + si}
                t0 = time.time(); res = run_world(w, CFG, seed, log=lambda s: None)
                rs = [r for r in res["rows"] if "budget_rel" not in r]
                ins = [r for r in rs if r["variables"]["cv_knn"] >= TAU]
                y = np.array([r["targets"]["log_excess"] for r in ins]); p = apply_law(LAW, ins); e = p - y
                by_alpha = {}
                for a in CFG["observer_alphas"]:
                    sel = [i for i, r in enumerate(ins) if r["alpha"] == a]
                    by_alpha[str(a)] = {"n": len(sel), "rmse": float(np.sqrt(np.mean(e[sel] ** 2))), "median_residual": float(np.median(e[sel])), "excess_max": float(max(np.exp(y[sel])))}
                cell = {"family": fam, "N": N, "seed": seed, "n_in": len(ins), "n_out": len(rs) - len(ins), "rmse_in": float(np.sqrt(np.mean(e ** 2))), "median_residual": float(np.median(e)),
                        "excess_max": float(np.exp(y.max())), "by_alpha": by_alpha, "seconds": round(time.time() - t0, 1)}
                out["cells"].append(cell)
                print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in cell.items() if k != "by_alpha"}), flush=True)
                json.dump(out, open(sys.argv[1], "w"), indent=1)
    # summary: per family and N, mean and spread over seeds
    summ = {}
    for fam in FAMILIES:
        for N in NS:
            es = [c["rmse_in"] for c in out["cells"] if c["family"] == fam and c["N"] == N]
            summ[f"{fam}_N{N}"] = {"mean_rmse": float(np.mean(es)), "min": float(min(es)), "max": float(max(es)), "over_limit": int(sum(x > LIMIT for x in es)), "of": len(es)}
    out["summary"] = summ
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    print(json.dumps(summ, indent=1)); print("SWEEP_DONE")


if __name__ == "__main__":
    main()
