"""LM-1 pilot 1 analysis: recover P-hat from the raw probe log, score vs oracles.

Runs locally (numpy). Input: lm1-probe-log.json fetched from Atlas.
P-hat(consumer, h) = mean over states of g g^T, where g_i is the central
difference [L(x + h e_i) - L(x - h e_i)] / (2h) of the fixed-truth loss.
Scores:
  R1 alignment      |cos| between top eigenvector of P-hat and the oracle
                    direction (A: (2,-1,0,-1,0,0)/norm; B: (0,0,1,0,1,0)/norm)
  R2 subspace       trace fraction of P-hat inside the oracle support
  R3 top-k          precision@k of diag(P-hat) ranking vs oracle support
  R4 stability      split-half (even/odd states): |cos| between the two
                    halves' top eigenvectors
  R5 flip precursor per-component diag rankings differ across consumers
"""
import json
import sys

import numpy as np

LOG = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\abptl\AppData\Local\Temp\claude\C--source-erisml-lib\924fee53-4f3c-448c-a4ac-59dee021c170\scratchpad\lm1-probe-log.json"
d = json.load(open(LOG, encoding="utf-8"))
D = d["d"]
NS = d["n_states"]

ORACLE = {
    "A": {"dir": np.array([2.0, -1.0, 0.0, -1.0, 0.0, 0.0]), "support": {0, 1, 3}},
    "B": {"dir": np.array([0.0, 0.0, 1.0, 0.0, 1.0, 0.0]), "support": {2, 4}},
}
for v in ORACLE.values():
    v["dir"] = v["dir"] / np.linalg.norm(v["dir"])

# index rows
tab = {}
for r in d["rows"]:
    tab[(r["consumer"], r["state"], r["h"], r["comp"], r["sign"])] = r["loss"]

report = {}
for cid, spec in d["consumers"].items():
    for h in spec["widths"]:
        grads = []
        for si in range(NS):
            g = np.zeros(D)
            ok = True
            for i in range(D):
                lp = tab.get((cid, si, h, i, 1))
                lm = tab.get((cid, si, h, i, -1))
                if lp is None or lm is None:
                    ok = False
                    break
                g[i] = (lp - lm) / (2 * h)
            if ok:
                grads.append(g)
        G = np.array(grads)
        P = sum(np.outer(g, g) for g in G) / len(G)
        w, V = np.linalg.eigh(P)
        top = V[:, -1]
        oracle = ORACLE[cid]
        r1 = float(abs(top @ oracle["dir"]))
        # R2: trace fraction inside oracle support (projector onto support axes
        # is loose for A whose direction mixes axes; also give directional frac)
        Pi = np.zeros((D, D))
        for i in oracle["support"]:
            Pi[i, i] = 1.0
        r2_support = float(np.trace(Pi @ P @ Pi) / np.trace(P))
        r2_dir = float(oracle["dir"] @ P @ oracle["dir"] / np.trace(P))
        k = len(oracle["support"])
        topk = set(np.argsort(np.diag(P))[-k:])
        r3 = len(topk & oracle["support"]) / k
        Pa = sum(np.outer(g, g) for g in G[0::2]) / len(G[0::2])
        Pb = sum(np.outer(g, g) for g in G[1::2]) / len(G[1::2])
        ta = np.linalg.eigh(Pa)[1][:, -1]
        tb = np.linalg.eigh(Pb)[1][:, -1]
        r4 = float(abs(ta @ tb))
        report[f"{cid}@h={h}"] = {
            "n_states_used": len(G),
            "R1_align_top_eig_vs_oracle": round(r1, 4),
            "R2_trace_frac_support_axes": round(r2_support, 4),
            "R2_trace_frac_oracle_dir": round(r2_dir, 4),
            "R3_topk_precision": r3,
            "R4_splithalf_align": round(r4, 4),
            "diag_Phat": [round(float(x), 5) for x in np.diag(P)],
            "top_eigvec": [round(float(x), 4) for x in top],
            "eig_spectrum": [round(float(x), 5) for x in w[::-1]],
        }

# R5 flip precursor: rankings differ across consumers (use A@0.10 vs B@0.15)
ra = np.argsort(report["A@h=0.1"]["diag_Phat"])[::-1][:3]
rb = np.argsort(report["B@h=0.15"]["diag_Phat"])[::-1][:2]
report["R5_flip_precursor"] = {
    "A_top3_components": [int(i) + 1 for i in ra],
    "B_top2_components": [int(i) + 1 for i in rb],
    "disjoint": bool(set(ra.tolist()).isdisjoint(set(rb.tolist()))),
}
report["ledger"] = d["ledger"]
print(json.dumps(report, indent=2))
out = LOG.replace("probe-log", "analysis")
json.dump(report, open(out, "w", encoding="utf-8"), indent=2)
print("written:", out)
