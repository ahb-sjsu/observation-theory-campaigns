#!/usr/bin/env python3
"""POST-HOC (exploratory, NOT sealed) TAIL probe for the CR-I-EIP arc.

The survival study tried CENTRAL scalars (median cos(e,delta), Pearson(c,KL))
and all failed to forecast Delta (Spearman well below the 0.70 law floor). But
Delta is itself a TAIL quantity: fc(m) is the miss-rate on the flagged tail
(changed = KL[ev] > quantile(KL[cal],0.75)), so a central statistic cannot see
it by construction. This probe asks the one untried question: does a statistic
of the FLAGGED TAIL forecast Delta?

Per graded (cell, layer) unit, from cached states only (identical loading to
survival_study.py: rho=ridge_fit(hx[cal],hg[cal],1e-2*n_cal), e=hg-hx@rho.T,
delta=hg-hx, split 0.6, changed as above):

  S_tail_cos  = median cos(e, delta) over the CHANGED (flagged) eval samples
  S_cos_q90   = 90th-percentile of |cos(e, delta)| over all eval (dist tail)
  S_rp_q90    = 90th-percentile of |e . dhat| over eval  (read-projected
                residual magnitude tail; dhat = delta/||delta||)
  S_tail_enorm= median ||e|| over changed / median ||e|| over eval
                (residual-energy concentration in the flagged tail)

Delta = fc_raw - fc_true from the committed result JSONs. Reports Spearman /
Pearson (predictor vs Delta) across units against the 0.70 law floor, plus the
advantage/inversion separation. Writes survival_tail.json. Exploratory; a hit
would be a NEW forecaster hypothesis to preregister, not a rescue of the sealed
FAIL. Run on Atlas: /home/claude/venvs/jed/bin/python survival_tail.py
"""
import json, os
import numpy as np
from scipy.stats import spearmanr, pearsonr

HERE = "/home/claude/cr-ieip"
RIDGE = 1e-2

UNITS = {
    "cellA": ("para(T5)",   [12, 18]),
    "cellB": ("bt(es)",     [14, 21]),
    "cellD": ("bt(de)",     [12, 18]),
    "cellE": ("bt(fr)",     [14, 21]),
    "cellF": ("para(peg)",  [12, 18]),
    "cellG": ("bt(de)",     [14, 21]),
    "cellH": ("synonym",    [12, 18]),
    "cellI": ("shuffle",    [14, 21]),
    "cellJ": ("truncate",   [12, 18]),
    "cellK": ("synonym",    [14, 21]),
    "cellL": ("shuffle",    [12, 18]),
}
KEYS = ["S_tail_cos", "S_cos_q90", "S_rp_q90", "S_tail_enorm"]


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
    n = len(KL); n_cal = int(0.6 * n)
    cal = slice(0, n_cal); ev = slice(n_cal, n)
    changed = KL[ev] > np.quantile(KL[cal], 0.75)   # the flagged tail (v3 line 522)
    for L in layers:
        hx = z[f"hx{L}"].astype(np.float64); hg = z[f"hg{L}"].astype(np.float64)
        rho = ridge_fit(hx[cal], hg[cal], RIDGE * n_cal)
        e = (hg - hx @ rho.T)[ev]
        d = (hg - hx)[ev]
        cos = rowcos(e, d)
        dhat = d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-12)
        rp_mag = np.abs((e * dhat).sum(1))
        enorm = np.linalg.norm(e, axis=1)
        nch = int(changed.sum())
        S_tail_cos = float(np.median(cos[changed])) if nch else float("nan")
        S_cos_q90 = float(np.quantile(np.abs(cos), 0.90))
        S_rp_q90 = float(np.quantile(rp_mag, 0.90))
        S_tail_enorm = float(np.median(enorm[changed]) / (np.median(enorm) + 1e-12)) if nch else float("nan")
        fc = res[str(L)]["false_clear"]
        delta = fc["raw"] - fc["true"]
        rows.append({"unit": f"{tag[-1]}-L{L}", "fam": fam, "n_changed": nch,
                     "Delta": round(float(delta), 4),
                     "S_tail_cos": round(S_tail_cos, 4), "S_cos_q90": round(S_cos_q90, 4),
                     "S_rp_q90": round(S_rp_q90, 4), "S_tail_enorm": round(S_tail_enorm, 4)})


def corr(key):
    xy = [(r[key], r["Delta"]) for r in rows if r[key] == r[key]]  # drop nan
    x = np.array([a for a, _ in xy]); y = np.array([b for _, b in xy])
    return spearmanr(x, y).statistic, pearsonr(x, y)[0], len(x)


print(f"\n{len(rows)} units\n")
hdr = f"{'unit':7} {'fam':10} {'nch':>4} {'Delta':>7} " + " ".join(f"{k:>11}" for k in KEYS)
print(hdr)
for r in rows:
    print(f"{r['unit']:7} {r['fam']:10} {r['n_changed']:>4} {r['Delta']:+7.3f} "
          + " ".join(f"{r[k]:>+11.3f}" for k in KEYS))

print("\nSpearman / Pearson (predictor vs Delta), law floor = 0.70:")
hit = []
for k in KEYS:
    s, p, nn = corr(k)
    flag = "  <-- clears 0.70" if abs(s) >= 0.70 else ""
    if abs(s) >= 0.70:
        hit.append(k)
    print(f"  {k:12} Spearman {s:+.3f}  Pearson {p:+.3f}  (n={nn}){flag}")

pos = [r for r in rows if r["Delta"] > 0.02]
neg = [r for r in rows if r["Delta"] < -0.02]
print(f"\nadvantage units (Delta>+0.02): {len(pos)}  inversion/none (Delta<-0.02): {len(neg)}")
for k in KEYS:
    pv = [r[k] for r in pos if r[k] == r[k]]
    nv = [r[k] for r in neg if r[k] == r[k]]
    if pv and nv:
        print(f"  {k:12} median(adv)={np.median(pv):+.3f}  median(inv)={np.median(nv):+.3f}  gap={np.median(pv)-np.median(nv):+.3f}")

print("\nVERDICT:", "TAIL FORECASTER FOUND (preregister): " + ", ".join(hit)
      if hit else "NO tail statistic clears the 0.70 floor -> three-strikes negative stands")

json.dump({"units": rows,
           "corr": {k: {"spearman": corr(k)[0], "pearson": corr(k)[1], "n": corr(k)[2]} for k in KEYS},
           "law_floor": 0.70, "hits": hit},
          open(os.path.join(HERE, "survival_tail.json"), "w"), indent=2, default=str)
print("WROTE survival_tail.json")
