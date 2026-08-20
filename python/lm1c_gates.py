"""LM1-002 gate evaluator: consumer-anchored gates. Local, numpy,
deterministic from the committed raw log.
Usage: python lm1b_gates.py <log.json> [--out <analysis.json>]

Anchor rule (the LM1-001 lesson): every gate references MEASURED
consumer behavior; the planted task oracles appear only in an ungated
diagnostics block.

  H1 held-out prediction  (v2 estimand, respecified after pilot 1)
                          Spearman rank correlation between u'P u and
                          the DIRECTION-MEAN realized squared
                          directional derivative — mean over K fresh
                          states per fresh direction u — which is the
                          operator's defining property E_x[(D_u L)^2].
                          Pilot 1's one-state-per-direction form was
                          swamped by state-position (cliff-distance)
                          noise and measured ~0; disclosed.
  H2 structure margin     H1's rho minus the same rho computed from
                          diag(P) only — off-diagonal structure must
                          not hurt (bar ~ >= -eps; pilot calibrates
                          whether it helps).
  H3 consumer-anchored flip   1 - matrix cosine between P_A and P_B
                          (normalized operators) — the two consumers'
                          measured geometries differ, no reference to
                          planted supports.
  H4 stability            split-half matrix cosine of the normalized
                          operator (as LM1-001, passed there).
  H5-H7 instrument        repeat |dloss| max; parse rate; failure rate.
"""
import json
import sys

import numpy as np

# LM1-003 gates: pooled H1 is the load-bearing quantity (the 088
# lesson); per-consumer floor is secondary. Bars are frozen ONLY from
# the ACROSS-DRAW calibration of the two independent powered pilot
# draws (pilotA/pilotB), below their minimum with margin — the
# LM1-002 lesson. H2 (full-vs-diag) remains an ungated diagnostic.
# None = unfrozen; governed refuses to grade.
# Frozen 2026-08-20 from the ACROSS-DRAW calibration of two
# independent powered pilot draws (pilotA seed 20261030, pilotB seed
# 20261101): pooled H1 0.644/0.658 (min 0.644); per-consumer min
# 0.569 (A, whose dominant-direction geometry is stabilized by the
# canonical axis block); flip 0.438/0.472; stability 0.815-0.868;
# repeat max 0.095/0.065. Bars below across-draw minimums with margin.
GATES = {
    "H1_pooled_spearman_min": 0.45,      # mean of per-consumer rho
    "H1b_per_consumer_floor": 0.30,      # secondary: no consumer unpredicted
    "H3_flip_operator_distance_min": 0.25,
    "H4_splithalf_norm_min_both": 0.70,
    "H5_repeat_dloss_max": 0.50,
    "H6_parse_rate_min": 0.98,
    "H7_fail_rate_max": 0.01,
}
NORM_FLOOR = 0.05

ORACLE_DIAG = {
    "A": np.array([2.0, -1.0, 0.0, -1.0, 0.0, 0.0]),
    "B": np.array([0.0, 0.0, 1.0, 0.0, 1.0, 0.0]),
}
for k in ORACLE_DIAG:
    ORACLE_DIAG[k] = ORACLE_DIAG[k] / np.linalg.norm(ORACLE_DIAG[k])


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    return float(ra @ rb / np.sqrt((ra @ ra) * (rb @ rb)))


def main():
    log_path = sys.argv[1]
    out_path = (sys.argv[sys.argv.index("--out") + 1]
                if "--out" in sys.argv else log_path.replace("_log", "_analysis"))
    d = json.load(open(log_path, encoding="utf-8"))
    D, NS, H = d["d"], d["n_states"], d["h"]
    MDIR, KST = d["m_dir"], d["k_states"]

    tab = {}
    parse_ok = parse_all = 0
    for r in d["rows"]:
        tab[(r["consumer"], r["idx"], r["kind"], r["comp"], r["sign"])] = r
        parse_all += 1
        if r["lp_yes"] is not None or r["lp_no"] is not None:
            parse_ok += 1

    metrics, diags = {}, {}
    P_norm_store = {}
    for cid in ("A", "B"):
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
        P = sum(np.outer(g, g) for g in G) / len(G)

        sel = G[np.linalg.norm(G, axis=1) > NORM_FLOOR]
        N = np.array([g / np.linalg.norm(g) for g in sel])
        Pn = sum(np.outer(g, g) for g in N) / len(N)
        P_norm_store[cid] = Pn
        Na = sum(np.outer(g, g) for g in N[0::2]) / len(N[0::2])
        Nb = sum(np.outer(g, g) for g in N[1::2]) / len(N[1::2])
        splithalf = float(np.sum(Na * Nb) / (np.linalg.norm(Na) * np.linalg.norm(Nb)))

        # held-out leg v2: per DIRECTION, mean realized (D_u L)^2 over its
        # K fresh states — the estimand is E_x[(D_u L)^2] = u'Pu
        dirs = [np.array(u) for u in d["heldout"][cid]["dirs"]]
        cells = d["heldout"][cid]["cells"]
        acc = {di: [] for di in range(MDIR)}
        for ci, cell in enumerate(cells):
            rp = tab.get((cid, ci, "heldout", cell["dir"], 1))
            rm = tab.get((cid, ci, "heldout", cell["dir"], -1))
            if rp is None or rm is None:
                continue
            du = (rp["loss"] - rm["loss"]) / (2 * H)
            acc[cell["dir"]].append(du * du)
        pred_full, pred_diag, realized = [], [], []
        for di, u in enumerate(dirs):
            if not acc[di]:
                continue
            realized.append(float(np.mean(acc[di])))
            pred_full.append(float(u @ P @ u))
            pred_diag.append(float(u @ np.diag(np.diag(P)) @ u))
        rho_full = spearman(np.array(pred_full), np.array(realized))
        rho_diag = spearman(np.array(pred_diag), np.array(realized))

        top = np.linalg.eigh(P)[1][:, -1]
        metrics[cid] = {
            "n_probe_states": len(G),
            "n_heldout_directions": len(realized),
            "H1_heldout_spearman": round(rho_full, 4),
            "H2_structure_margin": round(rho_full - rho_diag, 4),
            "rho_diag_only": round(rho_diag, 4),
            "H4_splithalf_norm": round(splithalf, 4),
        }
        diags[cid] = {
            "oracle_align_DIAGNOSTIC": round(float(abs(top @ ORACLE_DIAG[cid])), 4),
            "diag_P": [round(float(x), 5) for x in np.diag(P)],
            "top_eigvec": [round(float(x), 4) for x in top],
        }

    mcos = float(np.sum(P_norm_store["A"] * P_norm_store["B"]) /
                 (np.linalg.norm(P_norm_store["A"]) * np.linalg.norm(P_norm_store["B"])))
    flip_distance = 1.0 - mcos

    rep_pairs = []
    for r in d["rows"]:
        if r["kind"] == "repeat":
            base = tab.get((r["consumer"], r["idx"], "base", -1, 0))
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
        pooled_rho = 0.5 * (metrics["A"]["H1_heldout_spearman"] +
                            metrics["B"]["H1_heldout_spearman"])
        verdicts = {
            "H1": pooled_rho >= GATES["H1_pooled_spearman_min"],
            "H1b": all(metrics[c]["H1_heldout_spearman"] >= GATES["H1b_per_consumer_floor"] for c in "AB"),
            "H3": flip_distance >= GATES["H3_flip_operator_distance_min"],
            "H4": all(metrics[c]["H4_splithalf_norm"] >= GATES["H4_splithalf_norm_min_both"] for c in "AB"),
            "H5": inst["repeat_dloss_max"] is not None and inst["repeat_dloss_max"] <= GATES["H5_repeat_dloss_max"],
            "H6": inst["parse_rate"] >= GATES["H6_parse_rate_min"],
            "H7": inst["fail_rate"] <= GATES["H7_fail_rate_max"],
        }
        verdicts["ALL"] = bool(all(verdicts.values()))

    pooled = 0.5 * (metrics["A"]["H1_heldout_spearman"] +
                    metrics["B"]["H1_heldout_spearman"])
    out = {"campaign": d["campaign"], "mode": d["mode"], "seed": d["seed"],
           "gates": GATES if d["mode"] == "governed" else None,
           "verdicts": verdicts, "metrics": metrics,
           "H1_pooled_spearman": round(pooled, 4),
           "H3_flip_operator_distance": round(flip_distance, 4),
           "diagnostics_ungated": diags, "instrument": inst, "ledger": ledger}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2)
    print(json.dumps(out, indent=2))
    print("written:", out_path)


if __name__ == "__main__":
    main()
