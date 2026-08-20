"""LM-1 gate evaluator (PREREG-LM1-001). Local, numpy; deterministic
from the committed raw log — the analysis half of the sealed harness
pair. Usage: python lm1_gates.py <log.json> [--out <analysis.json>]

P-hat per consumer = mean over states of g g^T from central differences
at the frozen width. Gates evaluated only when the log's mode is
"governed"; pilot logs get metrics without verdicts.
"""
import json
import sys

import numpy as np

# Frozen 2026-08-19 (PREREG-LM1-001) from pilots 1-2. Two estimators,
# each gating the claim it actually measures (pilot-2 respecification,
# disclosed): the MAGNITUDE-WEIGHTED operator P = mean(g g^T) is the
# belief-averaged object — it carries alignment and support
# concentration (cal A 0.942/0.965, B 0.986/0.797) but its half-sample
# variance is heavy-tailed (gradients spike at the cliff); the
# NORMALIZED operator P_n = mean(gg^T/|g|^2, |g| > 0.05) carries
# geometry STABILITY (cal splithalf matrix-cos A 0.903, B 0.886; the
# magnitude-weighted matrix-cos dips to 0.58 on B purely through
# half-sample magnitude variance while the geometry stands).
GATES = {
    "G1_align_min_both": 0.80,          # |cos|(top eig of P, oracle), A and B
    "G2_splithalf_norm_min_both": 0.75, # matrix-cos of half-sample P_n
    "G3_support_trace_min_both": 0.65,  # trace frac of P on oracle support axes
    "G4_flip_supports_disjoint": True,  # A top-3 vs B top-2 by diag of P
    "G5_repeat_dloss_max": 0.50,        # instrument: max |dloss|, repeat pairs
    "G6_parse_rate_min": 0.98,          # yes/no recoverable from top-5
    "G7_fail_rate_max": 0.01,           # transport failures
}
NORM_FLOOR = 0.05

ORACLE = {
    "A": {"dir": np.array([2.0, -1.0, 0.0, -1.0, 0.0, 0.0]), "support": {0, 1, 3}, "k": 3},
    "B": {"dir": np.array([0.0, 0.0, 1.0, 0.0, 1.0, 0.0]), "support": {2, 4}, "k": 2},
}
for v in ORACLE.values():
    v["dir"] = v["dir"] / np.linalg.norm(v["dir"])


def main():
    log_path = sys.argv[1]
    out_path = (sys.argv[sys.argv.index("--out") + 1]
                if "--out" in sys.argv else log_path.replace("_log", "_analysis"))
    d = json.load(open(log_path, encoding="utf-8"))
    D, NS, H = d["d"], d["n_states"], d["h"]

    tab = {}
    parse_ok = parse_all = 0
    for r in d["rows"]:
        tab[(r["consumer"], r["state"], r["kind"], r["comp"], r["sign"])] = r
        parse_all += 1
        if r["lp_yes"] is not None or r["lp_no"] is not None:
            parse_ok += 1

    metrics = {}
    diag_rank = {}
    for cid, oracle in ORACLE.items():
        grads = []
        for si in range(NS):
            g = np.zeros(D)
            ok = True
            for i in range(D):
                rp = tab.get((cid, si, "probe", i, 1))
                rm = tab.get((cid, si, "probe", i, -1))
                if rp is None or rm is None:
                    ok = False
                    break
                g[i] = (rp["loss"] - rm["loss"]) / (2 * H)
            if ok:
                grads.append(g)
        G = np.array(grads)
        # magnitude-weighted (belief-averaged) operator: alignment + support
        P = sum(np.outer(g, g) for g in G) / len(G)
        top = np.linalg.eigh(P)[1][:, -1]
        Pi = np.zeros((D, D))
        for i in oracle["support"]:
            Pi[i, i] = 1.0
        # normalized operator: geometry stability (matrix cosine between
        # half-sample estimates; insensitive to magnitude heavy-tails and
        # to eigenvector rotation in near-degenerate eigenspaces)
        sel = G[np.linalg.norm(G, axis=1) > NORM_FLOOR]
        N = np.array([g / np.linalg.norm(g) for g in sel])
        Na = sum(np.outer(g, g) for g in N[0::2]) / len(N[0::2])
        Nb = sum(np.outer(g, g) for g in N[1::2]) / len(N[1::2])
        splithalf_norm = float(np.sum(Na * Nb) /
                               (np.linalg.norm(Na) * np.linalg.norm(Nb)))
        diag = np.diag(P)
        diag_rank[cid] = set(np.argsort(diag)[-oracle["k"]:].tolist())
        metrics[cid] = {
            "n_states_used": len(G),
            "n_states_above_floor": int(len(N)),
            "align": float(abs(top @ oracle["dir"])),
            "splithalf_norm": splithalf_norm,
            "support_trace_frac": float(np.trace(Pi @ P @ Pi) / np.trace(P)),
            "topk_by_diag": sorted(int(i) + 1 for i in diag_rank[cid]),
            "diag": [round(float(x), 5) for x in diag],
            "top_eigvec": [round(float(x), 4) for x in top],
        }

    # instrument legs
    rep_pairs = []
    for r in d["rows"]:
        if r["kind"] == "repeat":
            base = tab.get((r["consumer"], r["state"], "base", -1, 0))
            if base is not None:
                rep_pairs.append(abs(r["loss"] - base["loss"]))
    ledger = d["ledger"]
    inst = {
        "repeat_pairs": len(rep_pairs),
        "repeat_dloss_max": (max(rep_pairs) if rep_pairs else None),
        "repeat_dloss_mean": (sum(rep_pairs) / len(rep_pairs) if rep_pairs else None),
        "parse_rate": parse_ok / parse_all,
        "fail_rate": ledger["fail"] / max(1, ledger["req"]),
    }

    verdicts = None
    if d["mode"] == "governed":
        if any(v is None for v in GATES.values()):
            raise SystemExit("GATES not frozen; refusing to grade a governed log.")
        verdicts = {
            "G1": all(metrics[c]["align"] >= GATES["G1_align_min_both"] for c in "AB"),
            "G2": all(metrics[c]["splithalf_norm"] >= GATES["G2_splithalf_norm_min_both"] for c in "AB"),
            "G3": all(metrics[c]["support_trace_frac"] >= GATES["G3_support_trace_min_both"] for c in "AB"),
            "G4": diag_rank["A"].isdisjoint(diag_rank["B"]) == GATES["G4_flip_supports_disjoint"],
            "G5": inst["repeat_dloss_max"] is not None and inst["repeat_dloss_max"] <= GATES["G5_repeat_dloss_max"],
            "G6": inst["parse_rate"] >= GATES["G6_parse_rate_min"],
            "G7": inst["fail_rate"] <= GATES["G7_fail_rate_max"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    out = {"campaign": d["campaign"], "mode": d["mode"], "seed": d["seed"],
           "gates": GATES if d["mode"] == "governed" else None,
           "verdicts": verdicts, "metrics": metrics, "instrument": inst,
           "ledger": ledger}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2)
    print(json.dumps(out, indent=2))
    print("written:", out_path)


if __name__ == "__main__":
    main()
