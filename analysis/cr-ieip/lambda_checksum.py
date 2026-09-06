#!/usr/bin/env python3
"""V3 seal checksum: the retargeted Lambda gate (identity-map held-out R^2)
must reproduce the V2 post-hoc identity numbers exactly (they were computed
by v2_grade_pm.py). bt units +0.28..+0.45, para units -1.3/-1.8."""
import numpy as np

CELLS = {"cellD": [12, 18], "cellE": [14, 21], "cellF": [12, 18], "cellG": [14, 21]}
for tag, layers in CELLS.items():
    z = np.load(f"/home/claude/cr-ieip/ieip_{tag}_states.npz", allow_pickle=True)
    n = len(z["KL"]); n_cal = int(0.6 * n); n_fit = int(0.8 * n_cal)
    for L in layers:
        hx = z[f"hx{L}"][n_fit:n_cal].astype(np.float64)
        hg = z[f"hg{L}"][n_fit:n_cal].astype(np.float64)
        r2 = 1 - np.sum((hg - hx) ** 2) / np.sum((hg - hg.mean(0)) ** 2)
        print(f"{tag} L{L}: Lambda = {r2:+.4f}")
