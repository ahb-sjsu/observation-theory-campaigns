#!/usr/bin/env python3
"""Grade PREREG-CR-IEIP-V3 (sealed 2026-09-05) as executed. Runs on Atlas over
the five graded cells' state caches and result JSONs in ~/cr-ieip.

Per (cell, layer) unit, layers {12, 18} for Qwen2.5-0.5B and {14, 21} for
Qwen2.5-1.5B (the V2 unit rule, inherited):
  Lambda = identity-map held-out R^2 on the last 20% of the calibration split
           (n_cal = int(0.6 n), n_fit = int(0.8 n_cal); rows n_fit:n_cal), fit-free,
           exactly lambda_checksum.py's formula (the sealed gate, checksum-verified 2026-09-05)
  Delta  = fc_raw - fc_true from the runner's result JSON at that layer
Arms by measured Lambda: local if >= +0.20, non-local if <= -0.20, else transition band.
MC-S: >= 2 local units and >= 2 non-local units, else VOID.
P1 (verdict): every local unit Delta >= +0.05 and every non-local unit Delta <= +0.01.
P2 (secondary): Spearman(Lambda, Delta) over all graded units >= 0.7.
S1: rho-hat gate R^2 (v2_gate.py's ridge fit) beside Lambda. S2: final-layer rho_R2_eval.
Writes ~/cr-ieip/v3_gate.json and ~/cr-ieip/v3_graded.json (once; never overwrites).
"""
import json
import os
import sys

import numpy as np

HERE = os.path.expanduser("~/cr-ieip")
CELLS = {
    "cellH": {"model": "Qwen2.5-0.5B", "transform": "synonym", "seed": 20261006, "layers": [12, 18], "final": 24, "predicted": "local"},
    "cellI": {"model": "Qwen2.5-1.5B", "transform": "shuffle", "seed": 20261007, "layers": [14, 21], "final": 28, "predicted": "local"},
    "cellJ": {"model": "Qwen2.5-0.5B", "transform": "truncate", "seed": 20261008, "layers": [12, 18], "final": 24, "predicted": "non-local"},
    "cellK": {"model": "Qwen2.5-1.5B", "transform": "synonym", "seed": 20261009, "layers": [14, 21], "final": 28, "predicted": "local"},
    "cellL": {"model": "Qwen2.5-0.5B", "transform": "shuffle", "seed": 20261012, "layers": [12, 18], "final": 24, "predicted": "local"},
}
LAMBDA_LOCAL, LAMBDA_NONLOCAL = 0.20, -0.20
DELTA_LOCAL, DELTA_NONLOCAL = 0.05, 0.01
P2_BAR = 0.7
RIDGE = 1e-2


def ridge_fit(X, Y, lam):
    d = X.shape[1]
    return np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ Y).T


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    for f in ("v3_gate.json", "v3_graded.json"):
        if os.path.exists(os.path.join(HERE, f)):
            sys.exit(f"REFUSING: {f} exists; as-executed records are written once")
    gate, units = {}, []
    for tag, c in CELLS.items():
        z = np.load(os.path.join(HERE, f"ieip_{tag}_states.npz"), allow_pickle=True)
        res = json.load(open(os.path.join(HERE, f"cr_ieip_{tag}_result.json")))
        n = len(z["KL"]); n_cal = int(0.6 * n); n_fit = int(0.8 * n_cal)
        gate[tag] = {"n": n, "n_cal": n_cal, "n_fit": n_fit}
        for L in c["layers"]:
            hx = z[f"hx{L}"].astype(np.float64); hg = z[f"hg{L}"].astype(np.float64)
            ho_x, ho_g = hx[n_fit:n_cal], hg[n_fit:n_cal]
            lam = 1 - np.sum((ho_g - ho_x) ** 2) / np.sum((ho_g - ho_g.mean(0)) ** 2)
            rho = ridge_fit(hx[:n_fit], hg[:n_fit], RIDGE * n_fit)
            pred = ho_x @ rho.T
            rho_r2 = 1 - np.sum((ho_g - pred) ** 2) / np.sum((ho_g - ho_g.mean(0)) ** 2)
            fc = res[str(L)]["false_clear"]
            delta = fc["raw"] - fc["true"]
            arm = "local" if lam >= LAMBDA_LOCAL else ("non-local" if lam <= LAMBDA_NONLOCAL else "transition")
            if arm == "local":
                p1 = delta >= DELTA_LOCAL
            elif arm == "non-local":
                p1 = delta <= DELTA_NONLOCAL
            else:
                p1 = None
            u = {"cell": tag, "model": c["model"], "transform": c["transform"], "seed": c["seed"], "layer": L,
                 "lambda": round(float(lam), 4), "rho_gate_R2": round(float(rho_r2), 4),
                 "fc_raw": fc["raw"], "fc_true": fc["true"], "delta": round(float(delta), 4),
                 "arm": arm, "predicted_arm": c["predicted"], "P1": p1}
            gate[tag][str(L)] = {"lambda": u["lambda"], "rho_gate_R2": u["rho_gate_R2"], "arm": arm}
            units.append(u)
            print(f"{tag} L{L:<2} {c['model']:<13} {c['transform']:<8} Lambda {lam:+.4f} rho-gate {rho_r2:+.4f} "
                  f"fc raw {fc['raw']:.4f} true {fc['true']:.4f} Delta {delta:+.4f}  arm {arm:<10} "
                  f"(predicted {c['predicted']:<9}) P1 {p1}")
        fl = c["final"]
        gate[tag]["final_layer"] = {"layer": fl, "rho_R2_eval": res[str(fl)]["rho_R2_eval"],
                                   "delta": round(res[str(fl)]["false_clear"]["raw"] - res[str(fl)]["false_clear"]["true"], 4)}
    local = [u for u in units if u["arm"] == "local"]
    nonlocal_ = [u for u in units if u["arm"] == "non-local"]
    trans = [u for u in units if u["arm"] == "transition"]
    mcs = len(local) >= 2 and len(nonlocal_) >= 2
    p1_all = all(u["P1"] for u in local + nonlocal_) if mcs else None
    lam_all = np.array([u["lambda"] for u in units]); dl_all = np.array([u["delta"] for u in units])
    p2_rho = spearman(lam_all, dl_all)
    p2 = p2_rho >= P2_BAR
    verdict = "VOID" if not mcs else ("PASS" if p1_all else "FAIL")
    arm_match = sum(1 for u in units if u["arm"] == u["predicted_arm"])
    print(f"\nMC-S: {len(local)} local, {len(nonlocal_)} non-local, {len(trans)} transition -> {'ok' if mcs else 'VOID'}")
    print(f"P1 every graded unit in both arms: {p1_all}")
    print(f"P2 Spearman(Lambda, Delta) over {len(units)} units = {p2_rho:+.4f} (bar {P2_BAR}) -> {'holds' if p2 else 'does not hold'}")
    print(f"arm-vs-prediction: {arm_match}/{len(units)} units landed in the predicted arm")
    print(f"S2 final-layer rho_R2_eval: " + ", ".join(f"{t} L{gate[t]['final_layer']['layer']} {gate[t]['final_layer']['rho_R2_eval']}" for t in CELLS))
    print(f"\nPREREG-CR-IEIP-V3: {verdict}")
    graded = {"prereg": "PREREG-CR-IEIP-V3 v1.0 (sealed 2026-09-05)", "graded_utc": __import__("datetime").datetime.utcnow().isoformat() + "Z",
              "constants": {"lambda_local": LAMBDA_LOCAL, "lambda_nonlocal": LAMBDA_NONLOCAL, "delta_local": DELTA_LOCAL,
                            "delta_nonlocal": DELTA_NONLOCAL, "p2_bar": P2_BAR, "ridge": RIDGE},
              "units": units, "MC_S": {"local": len(local), "non_local": len(nonlocal_), "transition": len(trans), "ok": mcs},
              "P1": p1_all, "P2": {"spearman": round(p2_rho, 4), "holds": bool(p2)}, "arm_matches_prediction": arm_match,
              "verdict": verdict}
    json.dump(gate, open(os.path.join(HERE, "v3_gate.json"), "w"), indent=2)
    json.dump(graded, open(os.path.join(HERE, "v3_graded.json"), "w"), indent=2)
    print("wrote v3_gate.json, v3_graded.json")


if __name__ == "__main__":
    main()
