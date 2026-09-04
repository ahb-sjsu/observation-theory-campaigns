#!/usr/bin/env python3
"""CR-ANN conversion-determinant study -- POST-HOC EXPLORATORY (2026-09-03,
owner-directed 'investigate the conversion determinant before any new seal').

Question: what determines per-unit conversion (measured 190%/101%/74%/9%/~0
in V2 alone)? Hypothesis from the graded record: H = D - A is the wrong
potential because it uses the probe's CLASSIFICATION accuracy; the effect is
RETRIEVAL. Candidate potential, calibration-only (sealable by a V3 without
opening grading):

    R_C  = 1-NN label accuracy under the probe metric d_C (80/20 within cal)
    A    = 1-NN label accuracy under L2 (same split)
    predicted_gain = R_C - A

Test: Spearman(predicted_gain, measured graded mean gain) across ALL units of
both sealed families (V2 six + V1 seven), plus the V1 post-mortem's H variants
for comparison. Nothing here re-grades anything; both verdicts stand.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/claude/xbse/src")

V1DIR = os.path.expanduser("~/cr-ann/prereg")
V2DIR = os.path.expanduser("~/cr-ann/prereg_v2")
CKPT = os.path.expanduser("~/xbse_ckpt")
PROBE_TRAIN_FRAC = 0.80
THREADS = int(os.environ.get("CRANN_THREADS", "8"))

V2_DISTILL = {"privacy_aita": "privacy_joint.pt",
              "autonomy_dark": "autonomy_joint.pt",
              "care_moralstories": "care_joint.pt"}
V1_DISTILL = {"privacy_protection": "privacy_joint.pt",
              "identity_attack": "identity_attack_joint.pt",
              "physical_harm": "physharm_joint.pt"}


def read_jsonl(p):
    rows = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append((d["text"], int(d["label"])))
    return rows


_L = {}


def labse_cached(dirp, tag, texts):
    import hashlib
    p = os.path.join(dirp, f"emb_{tag}.npz")
    key = hashlib.sha256("\n".join(texts).encode()).hexdigest()[:16]
    if os.path.exists(p):
        z = np.load(p)
        if str(z["key"]) == key:
            return z["X"]
    from sentence_transformers import SentenceTransformer
    if "m" not in _L:
        _L["m"] = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    X = _L["m"].encode(texts, batch_size=128, normalize_embeddings=True,
                       show_progress_bar=False).astype(np.float32)
    np.savez(p, X=X, key=np.str_(key))
    return X


def xbse_target(ckpt, texts, labels):
    import torch
    from xbse.encoder import BSEEncoder
    sd = torch.load(os.path.join(CKPT, ckpt), map_location="cpu", weights_only=True)
    hid = sd["backbone.embeddings.word_embeddings.weight"].shape[1]
    base = {1024: "BAAI/bge-m3", 768: "sentence-transformers/LaBSE"}[hid]
    enc = BSEEncoder(base_model=base, max_len=192, device="cpu")
    enc.load_state_dict(sd, strict=True)
    Z = enc.encode(texts, batch_size=32).cpu().numpy()
    del enc
    y = np.array(labels)
    pos, neg = Z[y == 0], Z[y == 1]
    ax = pos.mean(0) / (np.linalg.norm(pos.mean(0)) + 1e-9) \
        - neg.mean(0) / (np.linalg.norm(neg.mean(0)) + 1e-9)
    ax /= (np.linalg.norm(ax) + 1e-9)
    return ((Z @ ax) < 0).astype(np.int64)


def unit_stats(cal_path, distill_ckpt, dirp, tag):
    import faiss
    from sklearn.linear_model import LogisticRegression  # noqa: F811
    cal = read_jsonl(cal_path)
    texts = [t for t, _ in cal]
    y = np.array([lab for _, lab in cal], dtype=np.int64)
    X = labse_cached(dirp, tag, texts)
    n_tr = int(PROBE_TRAIN_FRAC * len(cal))
    target = xbse_target(distill_ckpt, texts, y) if distill_ckpt else y
    probe = LogisticRegression(max_iter=3000, C=10.0)
    probe.fit(X[:n_tr], target[:n_tr])
    W = probe.coef_.astype(np.float32)
    D = float(probe.score(X[n_tr:], y[n_tr:]))
    # A: L2 1-NN on the 80/20 internal split
    idx = faiss.IndexFlatL2(X.shape[1])
    idx.add(X[:n_tr])
    _, nn = idx.search(X[n_tr:], 1)
    A = float((y[:n_tr][nn[:, 0]] == y[n_tr:]).mean())
    # R_C: 1-NN in the probe-projected space
    P_tr, P_te = X[:n_tr] @ W.T, X[n_tr:] @ W.T
    idc = faiss.IndexFlatL2(P_tr.shape[1])
    idc.add(np.ascontiguousarray(P_tr))
    _, nnc = idc.search(np.ascontiguousarray(P_te), 1)
    R_C = float((y[:n_tr][nnc[:, 0]] == y[n_tr:]).mean())
    # 5-fold cross-fit R_C - A: refit the probe per fold, retrieve in its
    # metric within the fold split; averages out single-split noise.
    rngf = np.random.default_rng(20260911)
    folds = np.array_split(rngf.permutation(len(cal)), 5)
    rcs, as_ = [], []
    for i in range(5):
        te = folds[i]
        tr = np.concatenate([folds[j] for j in range(5) if j != i])
        pf = LogisticRegression(max_iter=3000, C=10.0)
        pf.fit(X[tr], target[tr])
        Wf = pf.coef_.astype(np.float32)
        Ptr, Pte = X[tr] @ Wf.T, X[te] @ Wf.T
        ic = faiss.IndexFlatL2(Ptr.shape[1])
        ic.add(np.ascontiguousarray(Ptr))
        _, nc = ic.search(np.ascontiguousarray(Pte), 1)
        rcs.append(float((y[tr][nc[:, 0]] == y[te]).mean()))
        il = faiss.IndexFlatL2(X.shape[1])
        il.add(X[tr])
        _, nl = il.search(X[te], 1)
        as_.append(float((y[tr][nl[:, 0]] == y[te]).mean()))
    RC_x, A_x = float(np.mean(rcs)), float(np.mean(as_))
    return {"D": D, "A": A, "R_C": R_C, "pred_gain_RC_A": R_C - A,
            "RC_xfit": RC_x, "A_xfit5": A_x,
            "pred_xfit": RC_x - A_x,
            "pred_xfit_sd": float(np.std(np.array(rcs) - np.array(as_))),
            "H_classic": D - A, "n_cal": len(cal)}


def main():
    import torch
    torch.set_num_threads(THREADS)
    from scipy.stats import spearmanr

    out = {"study": "conversion determinant (post-hoc exploratory)",
           "date": "2026-09-03", "units": {}}

    # V2 units: measured mean gains from graded_v2.json
    g2 = json.load(open(os.path.join(V2DIR, "graded_v2.json")))
    q2 = json.load(open(os.path.join(V2DIR, "qualification_v2.json")))
    for u, r in q2["units"].items():
        if r.get("status") != "ok":
            continue
        st = unit_stats(r["manifest"]["calibration"]["path"],
                        V2_DISTILL.get(u) if r.get("distilled") else None,
                        V2DIR, f"{u}_cal")
        st["measured_gain"] = float(np.mean(
            [g2["results"][u][s]["gain"] for s in g2["results"][u]]))
        st["family"] = "V2"
        st["arm"] = r["arm"]
        out["units"][u] = st
        print(f"[pm] V2 {u}: R_C={st['R_C']:.3f} A={st['A']:.3f} "
              f"pred={st['pred_gain_RC_A']:+.3f} measured={st['measured_gain']:+.3f} "
              f"(H_classic={st['H_classic']:+.3f})", flush=True)

    # V1 units: calibration files + graded_result.json
    g1 = json.load(open(os.path.join(V1DIR, "graded_result.json")))
    for u in g1["results"]:
        cal_p = os.path.join(V1DIR, f"{u}.calibration.jsonl")
        if not os.path.exists(cal_p):
            print(f"[pm] V1 {u}: calibration file missing, skip", flush=True)
            continue
        st = unit_stats(cal_p, V1_DISTILL.get(u), V1DIR, f"{u}_cal")
        st["measured_gain"] = float(np.mean(
            [g1["results"][u][s]["gain"] for s in g1["results"][u]]))
        st["family"] = "V1"
        st["arm"] = g1["consumers"][u]["arm"]
        out["units"][u] = st
        print(f"[pm] V1 {u}: R_C={st['R_C']:.3f} A={st['A']:.3f} "
              f"pred={st['pred_gain_RC_A']:+.3f} measured={st['measured_gain']:+.3f} "
              f"(H_classic={st['H_classic']:+.3f})", flush=True)

    us = list(out["units"].values())
    pred = [u["pred_gain_RC_A"] for u in us]
    predx = [u["pred_xfit"] for u in us]
    meas = [u["measured_gain"] for u in us]
    hcl = [u["H_classic"] for u in us]
    sp_new = float(spearmanr(pred, meas).statistic)
    sp_x = float(spearmanr(predx, meas).statistic)
    sp_old = float(spearmanr(hcl, meas).statistic)
    r_new = float(np.corrcoef(pred, meas)[0, 1])
    r_x = float(np.corrcoef(predx, meas)[0, 1])
    slope = float(np.polyfit(pred, meas, 1)[0]) if len(us) > 2 else None
    slope_x = float(np.polyfit(predx, meas, 1)[0]) if len(us) > 2 else None
    out["summary"] = {"n_units": len(us),
                      "spearman_RCA_vs_gain": sp_new,
                      "pearson_RCA_vs_gain": r_new,
                      "slope_gain_vs_RCA": slope,
                      "spearman_xfit_vs_gain": sp_x,
                      "pearson_xfit_vs_gain": r_x,
                      "slope_gain_vs_xfit": slope_x,
                      "spearman_Hclassic_vs_gain": sp_old}
    print(f"[summary] n={len(us)}  single-split R_C−A: sp={sp_new:.3f} "
          f"r={r_new:.3f} slope={slope:.2f}  |  XFIT R_C−A: sp={sp_x:.3f} "
          f"r={r_x:.3f} slope={slope_x:.2f}  |  H_classic sp={sp_old:.3f}",
          flush=True)
    with open(os.path.join(V2DIR, "conversion_pm.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {V2DIR}/conversion_pm.json", flush=True)


if __name__ == "__main__":
    main()
