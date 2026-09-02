#!/usr/bin/env python3
"""Consumer-relative ANN — LaBSE x moral-dimension consumers (UNSEALED, exploratory).

The natural-consumer, cross-project cell: LaBSE (the xbse/LeBSE base family) embeds
real moral text (Social-Chemistry-101, the xbse corpus already on this host); the
consumers are xbse-style moral readers, as linear probes ON THE LaBSE SPACE
(P_C = W^T W, the consumer's exact Jacobian in the retrieval space, derived not
learned-for-kNN).

Consumers:
  valence   -- action-moral-judgment binarised (bad<0 vs good>0): "is this action
               morally good or bad?" (the core DEME/xbse read)
  care_harm -- rot-moral-foundations contains care-harm vs not (a dimension read)

Prediction (the conditional law, third domain): LaBSE neighborhoods are
topic/situation-dominated, so a moral consumer is OFF-AXIS -> measured alignment
(L2-1NN label acc) is modest, and OT reranking at fixed k improves the consumer
task while collapsing embedding recall@1. Isotropic control: P_C=I == L2.

Pipeline: FAISS IndexFlatL2 (k=50) -> rerank {L2 | OT} -> predict query label from
reranked top-1 train neighbour.
"""
import csv
import os
import sys
import numpy as np

HERE = os.path.expanduser("~/cr-ann")
TSV = "/archive/ethics-corpora/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv"
CACHE = os.path.join(HERE, "labse_socialchem.npz")
N_PER_CLASS = 8000        # per valence class, before split
K = 50
SEED = 0


def load_rows():
    """action text + valence label + care-harm flag (from the row's rot foundations)."""
    rows = []
    with open(TSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            a = (r.get("action") or "").strip()
            j = (r.get("action-moral-judgment") or "").strip()
            if not a or not j:
                continue
            try:
                jv = float(j)
            except ValueError:
                continue
            if jv == 0:
                continue
            mf = r.get("rot-moral-foundations") or ""
            rows.append((a, 1 if jv > 0 else 0, 1 if "care-harm" in mf else 0))
    return rows


def build():
    rng = np.random.default_rng(SEED)
    rows = load_rows()
    print(f"[labse-moral] usable rows: {len(rows)}", flush=True)
    # dedupe actions (same action appears many times), keep first label
    seen, uniq = set(), []
    for a, v, c in rows:
        if a not in seen:
            seen.add(a)
            uniq.append((a, v, c))
    print(f"[labse-moral] unique actions: {len(uniq)}", flush=True)
    good = [u for u in uniq if u[1] == 1]
    bad = [u for u in uniq if u[1] == 0]
    rng.shuffle(good)
    rng.shuffle(bad)
    sel = good[:N_PER_CLASS] + bad[:N_PER_CLASS]
    rng.shuffle(sel)
    texts = [s[0] for s in sel]
    y_val = np.array([s[1] for s in sel], dtype=np.int64)
    y_ch = np.array([s[2] for s in sel], dtype=np.int64)

    import torch
    torch.set_num_threads(16)     # Atlas thermal cap
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    print(f"[labse-moral] encoding {len(texts)} texts with LaBSE (CPU)...", flush=True)
    X = enc.encode(texts, batch_size=128, normalize_embeddings=True,
                   show_progress_bar=False).astype(np.float32)
    np.savez(CACHE, X=X, y_val=y_val, y_ch=y_ch)
    return X, y_val, y_ch


def main():
    os.makedirs(HERE, exist_ok=True)
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        X, y_val, y_ch = z["X"], z["y_val"], z["y_ch"]
        print(f"[labse-moral] cache hit {CACHE}", flush=True)
    else:
        X, y_val, y_ch = build()
    n = len(X)
    n_tr = int(0.7 * n)
    Xtr, Xte = X[:n_tr], X[n_tr:]
    print(f"[labse-moral] {Xtr.shape} train / {Xte.shape} test, dim={X.shape[1]}", flush=True)

    import faiss
    from sklearn.linear_model import LogisticRegression
    idx = faiss.IndexFlatL2(X.shape[1])
    idx.add(Xtr)
    _, cand = idx.search(Xte, K)

    def cell(name, ytr, yte):
        clf = LogisticRegression(max_iter=3000, C=10.0)
        clf.fit(Xtr, ytr)
        W = clf.coef_.astype(np.float32)
        clf_acc = clf.score(Xte, yte)
        # L2 (top-1 candidate), OT (rerank in consumer output space), iso control
        l2_acc = float((ytr[cand[:, 0]] == yte).mean())
        Wtr, Wq = Xtr @ W.T, Xte @ W.T
        dproj = Wq[:, None, :] - Wtr[cand]
        j = np.argmin((dproj * dproj).sum(-1), axis=1)
        chosen = cand[np.arange(len(cand)), j]
        ot_acc = float((ytr[chosen] == yte).mean())
        rec1 = float((chosen == cand[:, 0]).mean())
        diss = (ot_acc > l2_acc + 0.02) and (rec1 < 0.98)
        print(f"\n=== consumer: {name} ===")
        print(f"  linear decodability (clf acc)  : {clf_acc:.3f}")
        print(f"  MEASURED ALIGNMENT (L2-1NN acc): {l2_acc:.3f}")
        print(f"  OT rerank acc                  : {ot_acc:.3f}   "
              f"(gain {ot_acc - l2_acc:+.3f})")
        print(f"  OT embedding recall@1          : {rec1:.3f}")
        print(f"  --> DISSOCIATION: {diss}")
        return {"clf_acc": float(clf_acc), "l2_acc": l2_acc, "ot_acc": ot_acc,
                "gain": ot_acc - l2_acc, "ot_recall1": rec1, "dissociation": bool(diss)}

    out = {"n": int(n), "k": K, "encoder": "LaBSE",
           "corpus": "social-chem-101 actions"}
    out["valence"] = cell("moral valence (good vs bad action)",
                          y_val[:n_tr], y_val[n_tr:])
    out["care_harm"] = cell("care-harm foundation (vs other)",
                            y_ch[:n_tr], y_ch[n_tr:])

    # isotropic control on the valence consumer
    d = X.shape[1]
    dfull = Xte[:, None, :] - Xtr[cand]
    j0 = np.argmin((dfull * dfull).sum(-1), axis=1)
    chosen0 = cand[np.arange(len(cand)), j0]
    iso_acc = float((y_val[:n_tr][chosen0] == y_val[n_tr:]).mean())
    l2a = out["valence"]["l2_acc"]
    print(f"\n=== NEGATIVE CONTROL (P_C = I, valence) ===")
    print(f"  L2={l2a:.3f}  OT_iso={iso_acc:.3f}  -> equal: {abs(iso_acc - l2a) < 0.005}")
    out["iso_control_valence"] = {"acc": iso_acc, "equals_l2": bool(abs(iso_acc - l2a) < 0.005)}

    import json
    json.dump(out, open(os.path.join(HERE, "cr_ann_labse_moral_result.json"), "w"),
              indent=2)
    print(f"\nwrote {HERE}/cr_ann_labse_moral_result.json")


if __name__ == "__main__":
    main()
