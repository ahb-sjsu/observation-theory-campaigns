#!/usr/bin/env python3
"""Sealed V2 gate, computed exactly as written: within the CALIBRATION half
(first 60% of pairs, the runner's convention), fit rho on the first 80% and
measure held-out R^2 on the last 20%. Same ridge (RIDGE=1e-2 * n_fit), same
estimator as the runner. Grading data untouched. In-regime iff R^2 >= 0.05."""
import json

import numpy as np

RIDGE = 1e-2
CELLS = {"cellD": [12, 18], "cellE": [14, 21], "cellF": [12, 18], "cellG": [14, 21]}


def ridge_fit(X, Y, lam):
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d, dtype=np.float64)
    return np.linalg.solve(A, X.T @ Y).T


out = {}
for tag, layers in CELLS.items():
    z = np.load(f"/home/claude/cr-ieip/ieip_{tag}_states.npz", allow_pickle=True)
    n = len(z["KL"])
    n_cal = int(0.6 * n)
    n_fit = int(0.8 * n_cal)
    out[tag] = {}
    for L in layers:
        hx = z[f"hx{L}"].astype(np.float64)
        hg = z[f"hg{L}"].astype(np.float64)
        rho = ridge_fit(hx[:n_fit], hg[:n_fit], RIDGE * n_fit)
        ho_x, ho_g = hx[n_fit:n_cal], hg[n_fit:n_cal]
        pred = ho_x @ rho.T
        ss_res = np.sum((ho_g - pred) ** 2)
        ss_tot = np.sum((ho_g - ho_g.mean(0)) ** 2)
        r2 = 1 - ss_res / ss_tot
        out[tag][L] = {"gate_R2": round(float(r2), 4),
                       "in_regime": bool(r2 >= 0.05)}
        print(f"{tag} L{L}: gate R2 = {r2:.4f} -> "
              f"{'IN' if r2 >= 0.05 else 'OUT'}-regime", flush=True)

json.dump(out, open("/home/claude/cr-ieip/v2_gate.json", "w"), indent=2)
print("wrote /home/claude/cr-ieip/v2_gate.json")
