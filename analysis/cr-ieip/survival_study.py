#!/usr/bin/env python3
"""POST-HOC (exploratory, NOT sealed) survival study for the CR-I-EIP arc.

Question: does a 'perturbation-survival' measure forecast the consumer-read
advantage Delta where transform locality Lambda failed (V3 Spearman -0.05)?

Candidate survivals, per graded (cell, layer) unit, from cached states only
(faithful to the sealed pipeline: rho = ridge_fit(hx[cal],hg[cal],1e-2*n_cal),
hg ~= hx@rho.T, e = hg - hx@rho.T, delta = hg - hx, split 0.6):

  S_dir_ev  = median cos(e, delta) over the eval split   (rho never saw eval)
  S_dir_cal = median cos(e, delta) over held-out cal slice [n_fit:n_cal]
              (deployable-gate analogue of Lambda; rho-leakage caveat noted)
  S_patch   = Pearson(c_L, KL) over eval, where c_L is the CACHED true
              patch-response (does patching e reproduce the true output change)

Lambda recomputed uniformly here (identity-map held-out R^2 on [n_fit:n_cal])
so all units use one source. Delta = fc_raw - fc_true from the committed result
JSONs. Reports Spearman(S, Delta) across all units for each candidate, vs
Lambda's, and a per-unit table. Writes survival_study.json. Run on Atlas:
  /home/claude/venvs/jed/bin/python survival_study.py
"""
import json, os
import numpy as np
from scipy.stats import spearmanr, pearsonr

HERE = "/home/claude/cr-ieip"
RIDGE = 1e-2

# cell -> (family, [graded layers]); C excluded (states cache was deleted)
UNITS = {
    "cellA": ("para(T5)",   [12, 18]),   # V1 0.5B
    "cellB": ("bt(es)",     [14, 21]),   # V1 1.5B
    "cellD": ("bt(de)",     [12, 18]),   # V2 0.5B
    "cellE": ("bt(fr)",     [14, 21]),   # V2 1.5B
    "cellF": ("para(peg)",  [12, 18]),   # V2 0.5B
    "cellG": ("bt(de)",     [14, 21]),   # V2 1.5B
    "cellH": ("synonym",    [12, 18]),   # V3 0.5B
    "cellI": ("shuffle",    [14, 21]),   # V3 1.5B
    "cellJ": ("truncate",   [12, 18]),   # V3 0.5B
    "cellK": ("synonym",    [14, 21]),   # V3 1.5B
    "cellL": ("shuffle",    [12, 18]),   # V3 0.5B
}


def ridge_fit(X, Y, lam):
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d, dtype=np.float64)
    return np.linalg.solve(A, X.T @ Y).T


def rowcos(A, B):
    num = (A * B).sum(1)
    den = np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1) + 1e-12
    return num / den


rows = []
for tag, (fam, layers) in UNITS.items():
    sp = os.path.join(HERE, f"ieip_{tag}_states.npz")
    rp = os.path.join(HERE, f"cr_ieip_{tag}_result.json")
    if not (os.path.exists(sp) and os.path.exists(rp)):
        print(f"skip {tag} (missing states or result)"); continue
    z = np.load(sp, allow_pickle=True)
    res = json.load(open(rp))
    KL = z["KL"].astype(np.float64)
    n = len(KL); n_cal = int(0.6 * n); n_fit = int(0.8 * n_cal)
    cal = slice(0, n_cal); ev = slice(n_cal, n); cs = slice(n_fit, n_cal)
    cc = os.path.join(HERE, f"ieip_{tag}_consumer.npz")
    zc = np.load(cc) if os.path.exists(cc) else None
    for L in layers:
        hx = z[f"hx{L}"].astype(np.float64); hg = z[f"hg{L}"].astype(np.float64)
        rho = ridge_fit(hx[cal], hg[cal], RIDGE * n_cal)
        e = hg - hx @ rho.T
        d = hg - hx
        lam = 1 - (np.sum((d[cs])**2) / np.sum((hg[cs] - hg[cs].mean(0))**2))
        S_dir_ev = float(np.median(rowcos(e[ev], d[ev])))
        S_dir_cal = float(np.median(rowcos(e[cs], d[cs])))
        fc = res[str(L)]["false_clear"]
        delta = fc["raw"] - fc["true"]
        S_patch = None
        if zc is not None and f"c{L}" in zc.files:
            c = zc[f"c{L}"].astype(np.float64)
            if len(c) == (n - n_cal):
                S_patch = float(pearsonr(c, KL[ev])[0])
        rows.append({"unit": f"{tag[-1]}-L{L}", "fam": fam,
                     "Lambda": round(float(lam), 4), "Delta": round(float(delta), 4),
                     "S_dir_ev": round(S_dir_ev, 4), "S_dir_cal": round(S_dir_cal, 4),
                     "S_patch": None if S_patch is None else round(S_patch, 4)})

D = np.array([r["Delta"] for r in rows])
def corr(key):
    x = np.array([r[key] for r in rows if r[key] is not None])
    y = np.array([r["Delta"] for r in rows if r[key] is not None])
    return spearmanr(x, y).statistic, pearsonr(x, y)[0], len(x)

print(f"\n{len(rows)} units\n")
print(f"{'unit':7} {'fam':10} {'Lambda':>8} {'Delta':>7} {'S_dir_ev':>9} {'S_dir_cal':>10} {'S_patch':>8}")
for r in rows:
    sp = "  n/a" if r["S_patch"] is None else f"{r['S_patch']:+.3f}"
    print(f"{r['unit']:7} {r['fam']:10} {r['Lambda']:+8.3f} {r['Delta']:+7.3f} "
          f"{r['S_dir_ev']:+9.3f} {r['S_dir_cal']:+10.3f} {sp:>8}")

print("\nSpearman / Pearson (predictor vs Delta), floor for a law = 0.70:")
for k in ["Lambda", "S_dir_ev", "S_dir_cal", "S_patch"]:
    s, p, nn = corr(k)
    print(f"  {k:10} Spearman {s:+.3f}  Pearson {p:+.3f}  (n={nn})")

# does sign of Delta separate? report each predictor's separation of Delta>0 vs <0
pos = [r for r in rows if r["Delta"] > 0.02]
neg = [r for r in rows if r["Delta"] < -0.02]
print(f"\nadvantage units (Delta>+0.02): {len(pos)}  inversion/none (Delta<-0.02): {len(neg)}")
for k in ["Lambda", "S_dir_ev", "S_dir_cal", "S_patch"]:
    pv = [r[k] for r in pos if r[k] is not None]
    nv = [r[k] for r in neg if r[k] is not None]
    if pv and nv:
        print(f"  {k:10} median(adv)={np.median(pv):+.3f}  median(inv)={np.median(nv):+.3f}  gap={np.median(pv)-np.median(nv):+.3f}")

json.dump({"units": rows,
           "corr": {k: {"spearman": corr(k)[0], "pearson": corr(k)[1], "n": corr(k)[2]}
                    for k in ["Lambda", "S_dir_ev", "S_dir_cal", "S_patch"]}},
          open(os.path.join(HERE, "survival_study.json"), "w"), indent=2, default=str)
print("\nWROTE survival_study.json")
