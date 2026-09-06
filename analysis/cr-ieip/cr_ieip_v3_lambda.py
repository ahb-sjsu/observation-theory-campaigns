#!/usr/bin/env python3
"""V3 Lambda gate for the graded cells H-L: identity-map held-out R^2 on the
held-out slice [n_fit:n_cal] of the calibration split (n_cal=0.6n,
n_fit=0.8*n_cal), fit-free (no rho-hat), the exact machinery of
lambda_checksum.py. Writes v3_lambda.json. Arms: Lambda>=0.20 local,
Lambda<=-0.20 non-local, else transition band (descriptive, no bar).

Run on Atlas: /home/claude/venvs/jed/bin/python cr_ieip_v3_lambda.py
(state caches at /home/claude/cr-ieip/ieip_cell{H..L}_states.npz)."""
import numpy as np, json, os

HERE = "/home/claude/cr-ieip"
CELLS = {"cellH": [6, 12, 18, 24], "cellI": [7, 14, 21, 28], "cellJ": [6, 12, 18, 24],
         "cellK": [7, 14, 21, 28], "cellL": [6, 12, 18, 24]}
GRADED = {"cellH": [12, 18], "cellI": [14, 21], "cellJ": [12, 18], "cellK": [14, 21], "cellL": [12, 18]}
out = {}
for tag, layers in CELLS.items():
    z = np.load(os.path.join(HERE, f"ieip_{tag}_states.npz"), allow_pickle=True)
    n = len(z["KL"]); n_cal = int(0.6 * n); n_fit = int(0.8 * n_cal)
    out[tag] = {"n": n, "n_cal": n_cal, "n_fit": n_fit, "held_slice": [n_fit, n_cal], "lambda": {}}
    for L in layers:
        hx = z[f"hx{L}"][n_fit:n_cal].astype(np.float64)
        hg = z[f"hg{L}"][n_fit:n_cal].astype(np.float64)
        r2 = 1 - np.sum((hg - hx) ** 2) / np.sum((hg - hg.mean(0)) ** 2)
        out[tag]["lambda"][L] = round(float(r2), 4)
    print(tag, "n=%d held=[%d:%d]" % (n, n_fit, n_cal), "graded", GRADED[tag],
          {L: out[tag]["lambda"][L] for L in layers})
json.dump(out, open(os.path.join(HERE, "v3_lambda.json"), "w"), indent=2)
print("WROTE v3_lambda.json")
