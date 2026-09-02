#!/usr/bin/env python3
"""Consumer-relative ANN — the MISALIGNED cell (UNSEALED, exploratory).

Tests the sharpened hypothesis from the matched-cell negative: the dissociation
(consumer up / embedding fidelity down at fixed k) appears iff the consumer reads
OFF-AXIS from what the embedding emphasises. Two real-embedding experiments:

(1) CONTROLLED DIRECTION SWEEP. On the real 20NG MiniLM embeddings, define a
    binary consumer label = sign(u.x - median) for a unit direction u taken at
    descending PCA ranks (high variance = aligned/emphasised ... low variance =
    off-axis). Consumer read operator P_C = u u^T (rank-1: the consumer reads only
    u). Dial u from aligned to off-axis and watch the dissociation appear. This
    isolates the alignment condition on real geometry (labels controlled, geometry
    real).

(2) NATURAL OFF-AXIS ATTRIBUTES. Real document attributes a semantic encoder
    under-weights (log length, uppercase ratio), binarised at the median, with a
    real linear consumer (LogisticRegression) -> P_C = W^T W. Fully natural.

For each consumer: FAISS L2 candidate gen (k=50) -> rerank {L2 | OT} -> predict
label from reranked top-1. Alignment is MEASURED as the L2-1NN label accuracy
(how well the raw embedding neighbourhood already predicts the label). Prediction:
low alignment -> large dissociation; high alignment -> none.
"""
import os
import numpy as np

HERE = os.path.expanduser("~/cr-ann")
EMB = os.path.join(HERE, "newsgroups_minilm.npz")
K = 50


def load():
    z = np.load(EMB)
    return z["Xtr"], z["Xte"]


def texts():
    from sklearn.datasets import fetch_20newsgroups
    rm = ("headers", "footers", "quotes")
    return (fetch_20newsgroups(subset="train", remove=rm).data,
            fetch_20newsgroups(subset="test", remove=rm).data)


def cand_faiss(Xtr, Xte, k):
    import faiss
    idx = faiss.IndexFlatL2(Xtr.shape[1])
    idx.add(Xtr)
    _, I = idx.search(Xte, k)
    return I


def eval_dir(Xtr, Xte, cand, ytr, yte, u):
    """rank-1 consumer P_C = u u^T. Returns (L2 acc, OT acc, OT recall@1)."""
    l2 = float((ytr[cand[:, 0]] == yte).mean())
    ptr, pq = Xtr @ u, Xte @ u                       # projections onto u
    pc = ptr[cand]                                   # (Nte, K)
    j = np.argmin((pq[:, None] - pc) ** 2, axis=1)
    chosen = cand[np.arange(len(cand)), j]
    ot = float((ytr[chosen] == yte).mean())
    rec1 = float((chosen == cand[:, 0]).mean())
    return l2, ot, rec1


def eval_W(Xtr, Xte, cand, ytr, yte, W):
    """full P_C = W^T W via the consumer output space W x."""
    l2 = float((ytr[cand[:, 0]] == yte).mean())
    Wtr, Wq = Xtr @ W.T, Xte @ W.T                   # (N, C)
    Wc = Wtr[cand]                                    # (Nte, K, C)
    d = Wq[:, None, :] - Wc
    j = np.argmin((d * d).sum(-1), axis=1)
    chosen = cand[np.arange(len(cand)), j]
    ot = float((ytr[chosen] == yte).mean())
    rec1 = float((chosen == cand[:, 0]).mean())
    return l2, ot, rec1


def main():
    from sklearn.linear_model import LogisticRegression
    Xtr, Xte = load()
    d = Xtr.shape[1]
    cand = cand_faiss(Xtr, Xte, K)
    print(f"[mis] embeddings {Xtr.shape}/{Xte.shape} d={d} k={K}\n")

    # ---- (1) controlled direction sweep ----
    Xc = Xtr - Xtr.mean(0)
    # PCA directions (right singular vectors) + their variances
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = (S ** 2) / len(Xc)
    ranks = [0, 2, 5, 20, 50, 100, 200, 350]
    ranks = [r for r in ranks if r < d]
    print("=== (1) CONTROLLED DIRECTION SWEEP (real embeddings, sign(u.x) label) ===")
    print(f"  {'PCrank':>6} {'var(u)':>9} {'L2acc':>7} {'OTacc':>7} {'d_acc':>7} "
          f"{'OTrec@1':>8}  dissociation")
    for r in ranks:
        u = Vt[r].astype(np.float32)
        thr = np.median(Xtr @ u)
        ytr = (Xtr @ u > thr).astype(np.int64)
        yte = (Xte @ u > thr).astype(np.int64)
        l2, ot, rec1 = eval_dir(Xtr, Xte, cand, ytr, yte, u)
        diss = (ot > l2 + 0.02) and (rec1 < 0.98)
        print(f"  {r:6d} {var[r]:9.4f} {l2:7.3f} {ot:7.3f} {ot-l2:+7.3f} "
              f"{rec1:8.3f}  {diss}")
    print("  (high-var u = aligned -> L2 already good, no gain; "
          "low-var u = off-axis -> OT >> L2)\n")

    # ---- (2) natural off-axis attributes ----
    tr_txt, te_txt = texts()

    def attr(txts, fn):
        return np.array([fn(t) for t in txts], dtype=np.float64)

    def caps_ratio(t):
        letters = [c for c in t if c.isalpha()]
        return (sum(c.isupper() for c in letters) / len(letters)) if letters else 0.0

    natural = {
        "log_length": (lambda t: np.log1p(len(t))),
        "caps_ratio": caps_ratio,
    }
    print("=== (2) NATURAL OFF-AXIS ATTRIBUTES (real linear consumer, P_C=W^T W) ===")
    print(f"  {'attribute':>12} {'clf_acc':>8} {'L2acc':>7} {'OTacc':>7} {'d_acc':>7} "
          f"{'OTrec@1':>8}  dissociation")
    for name, fn in natural.items():
        atr, ate = attr(tr_txt, fn), attr(te_txt, fn)
        thr = np.median(atr)
        ytr = (atr > thr).astype(np.int64)
        yte = (ate > thr).astype(np.int64)
        clf = LogisticRegression(max_iter=2000, C=10.0)
        clf.fit(Xtr, ytr)
        W = clf.coef_.astype(np.float32)             # (1, d)
        l2, ot, rec1 = eval_W(Xtr, Xte, cand, ytr, yte, W)
        diss = (ot > l2 + 0.02) and (rec1 < 0.98)
        print(f"  {name:>12} {clf.score(Xte, yte):8.3f} {l2:7.3f} {ot:7.3f} "
              f"{ot-l2:+7.3f} {rec1:8.3f}  {diss}")
    print("  (clf_acc = linearly decodable? ; L2acc = does raw L2 already cluster "
          "by it? ; gap = dissociation)")


if __name__ == "__main__":
    main()
