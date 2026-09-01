#!/usr/bin/env python3
"""Consumer-relative ANN — real-data shakedown (UNSEALED, exploratory).

Real embeddings + a real consumer whose read operator P_C = J^T J is computed from
the actual model. Tests whether the dissociation (consumer performance up, embedding
fidelity down, at fixed candidate budget k) appears on real data, and how large.

- Embedding DB: 20 Newsgroups (sklearn built-in, headers/footers/quotes stripped)
  encoded by a frozen general sentence encoder (all-MiniLM-L6-v2, 384-d, L2-normed
  so FAISS L2 candidate gen == cosine, the standard use).
- Consumer: a linear classifier (logistic regression) trained on the TRAIN
  embeddings for the 20-class task. Its read operator is P_C = W^T W (W = coef_),
  the exact Jacobian of the logits w.r.t. the embedding: d_C(x,x_j)^2 =
  ||W(x - x_j)||^2 = squared distance in the consumer's LOGIT space.
- Task (consumer-relevant retrieval): FAISS L2 candidate gen (top-k) -> rerank
  {L2 | OT d_C} -> predict the query's class from the reranked top-1 train
  neighbour's label (1-NN via retrieval). Downstream metric = accuracy.
- Embedding fidelity: recall@1 vs the true L2-nearest; mean L2 distance of the
  chosen neighbour. OT should be worse on both.
- Negative control: P_C = I -> OT == L2.

Prior-art honesty: supervised/logit-space metrics improving k-NN is KNOWN (LMNN,
NCA). The OT contribution is the DISSOCIATION framing (embedding fidelity down while
consumer up) and P_C DERIVED from the consumer's Jacobian, not learned for k-NN.
"""
import os
import numpy as np

HERE = os.path.expanduser("~/cr-ann")
os.makedirs(HERE, exist_ok=True)
EMB_CACHE = os.path.join(HERE, "newsgroups_minilm.npz")
K = 50


def embeddings():
    if os.path.exists(EMB_CACHE):
        z = np.load(EMB_CACHE)
        print(f"[cr-ann] using cache {EMB_CACHE}", flush=True)
        return z["Xtr"], z["ytr"], z["Xte"], z["yte"]
    import torch
    torch.set_num_threads(16)   # Atlas thermal cap (<=20 threads)
    from sklearn.datasets import fetch_20newsgroups
    from sentence_transformers import SentenceTransformer
    rm = ("headers", "footers", "quotes")
    tr = fetch_20newsgroups(subset="train", remove=rm)
    te = fetch_20newsgroups(subset="test", remove=rm)
    print(f"[cr-ann] train={len(tr.data)} test={len(te.data)} classes={len(tr.target_names)}",
          flush=True)
    # CPU: Atlas driver (12080) is older than torch 2.11+cu130 wants for GPU.
    enc = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    Xtr = enc.encode(tr.data, batch_size=256, normalize_embeddings=True,
                     show_progress_bar=False).astype(np.float32)
    Xte = enc.encode(te.data, batch_size=256, normalize_embeddings=True,
                     show_progress_bar=False).astype(np.float32)
    ytr, yte = tr.target.astype(np.int64), te.target.astype(np.int64)
    np.savez(EMB_CACHE, Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte)
    return Xtr, ytr, Xte, yte


def rerank_eval(Xtr, ytr, Xte, yte, cand, PC, name):
    """For each test query, choose top-1 among its candidates by score, predict its
    label; also report embedding fidelity of the choice."""
    chosen = np.empty(len(Xte), dtype=np.int64)
    for i in range(len(Xte)):
        cids = cand[i]
        diff = Xtr[cids] - Xte[i]
        if PC is None:
            score = (diff * diff).sum(1)
        else:
            score = np.einsum("kd,de,ke->k", diff, PC, diff)
        chosen[i] = cids[score.argmin()]
    acc = float((ytr[chosen] == yte).mean())
    recall1 = float((chosen == cand[:, 0]).mean())
    meanl2 = float(np.sqrt(((Xtr[chosen] - Xte) ** 2).sum(1)).mean())
    return acc, recall1, meanl2


def main():
    import faiss
    from sklearn.linear_model import LogisticRegression

    Xtr, ytr, Xte, yte = embeddings()
    d = Xtr.shape[1]
    print(f"[cr-ann] embeddings {Xtr.shape} / {Xte.shape}, dim={d}", flush=True)

    clf = LogisticRegression(max_iter=2000, C=10.0, n_jobs=-1)
    clf.fit(Xtr, ytr)
    W = clf.coef_.astype(np.float32)                 # (20, 384) = Jacobian of logits
    PC = (W.T @ W).astype(np.float32)                # consumer read operator
    print(f"[cr-ann] consumer linear classifier test acc = {clf.score(Xte, yte):.3f} "
          f"(context); P_C = W^T W, W {W.shape}", flush=True)

    idx = faiss.IndexFlatL2(d)
    idx.add(Xtr)
    _, cand = idx.search(Xte, K)

    print(f"\n=== fixed candidate budget k={K}, 1-NN-via-retrieval ===")
    aL2, rL2, lL2 = rerank_eval(Xtr, ytr, Xte, yte, cand, None, "L2")
    aOT, rOT, lOT = rerank_eval(Xtr, ytr, Xte, yte, cand, PC, "OT")
    print(f"  downstream accuracy : L2={aL2:.3f}  OT={aOT:.3f}   (OT-L2 = {aOT-aL2:+.3f})")
    print(f"  embedding recall@1  : L2={rL2:.3f}  OT={rOT:.3f}")
    print(f"  mean L2 dist chosen : L2={lL2:.3f}  OT={lOT:.3f}")
    diss = (aOT > aL2 + 0.005) and (rOT < rL2 - 0.02)
    print(f"  --> DISSOCIATION (consumer up, embedding fidelity down): {diss}")

    print(f"\n=== NEGATIVE CONTROL: P_C = I ===")
    a0, r0, _ = rerank_eval(Xtr, ytr, Xte, yte, cand, np.eye(d, dtype=np.float32), "iso")
    print(f"  downstream accuracy : L2={aL2:.3f}  OT_iso={a0:.3f}   (should be ~equal)")
    print(f"  embedding recall@1  : L2={rL2:.3f}  OT_iso={r0:.3f}   (should be ~equal)")
    print(f"  --> no dissociation: {abs(a0-aL2)<0.005 and abs(r0-rL2)<0.01}")

    import json
    json.dump({"k": K, "consumer_clf_acc": float(clf.score(Xte, yte)),
               "L2": {"acc": aL2, "recall1": rL2, "meanl2": lL2},
               "OT": {"acc": aOT, "recall1": rOT, "meanl2": lOT},
               "iso_control": {"acc": a0, "recall1": r0},
               "dissociation": bool(diss)},
              open(os.path.join(HERE, "cr_ann_realdata_result.json"), "w"), indent=2)
    print(f"\nwrote {HERE}/cr_ann_realdata_result.json")


if __name__ == "__main__":
    main()
