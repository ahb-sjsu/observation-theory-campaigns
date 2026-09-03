#!/usr/bin/env python3
"""OT-UMAP shakedown (UNSEALED, exploratory) -- is DR faithfulness observer-indexed?

The claim under construction: preserving consumer-induced neighborhoods gives an
embedding that is objectively worse under conventional geometric metrics and
better for what the downstream observer can distinguish -- and two misaligned
observers order the embeddings OPPOSITELY, so there is no observer-independent
answer to "is this dimensionality reduction faithful?".

Design note (stated before running): with a CONSTANT consumer operator,
d_P(x,y)^2 = (x-y)^T P (x-y) factorizes through P = L^T L, so OT-UMAP is
EXACTLY euclidean UMAP on the transformed data X L^T. This shakedown therefore
tests the dissociation/inversion with derived (not learned-for-DR) constant
operators, and says so plainly: as a transform it is Mahalanobis-adjacent; the
derived-not-learned P and the observer-indexed evaluation are the OT content.
The position-dependent P_C(x) = J(x)^T J(x) cell (genuinely local geometry, no
global factorization, needs PyNNDescent callable metrics) is the successor.

Substrate: 20NG train MiniLM embeddings (cached, order = fetch order), 6,000
seeded subsample embedded. Probes are fit on the TEST split only (disjoint from
every embedded point). Consumers:
  C1 topic   -- 20-class logistic; the ALIGNED consumer (matched null arm)
  C2 length  -- log1p(len) median-binarised; natural off-axis (misaligned)
  C3 pc200   -- sign(u.x - med), u = PCA direction 200 of the test split;
                controlled off-axis (misaligned)
Operators: P_i = W_i^T W_i / ||.||_2 + eps*I (eps 0.05). Controls: P = I
(must reproduce UMAP-L2 exactly at fixed seed), pure projection eps=0 and
logit-space UMAP for C2 (the degenerate "you embedded the logits" baseline,
reported as such).

Embeddings (UMAP 2-D, n_neighbors=15, min_dist=0.1, random_state=0):
  E_L2, E_iso(control), E_OT1(topic), E_OT2(length), E_OT3(pc200),
  E_proj2(eps=0), E_logit2.

Metrics per embedding:
  conventional: trustworthiness (input L2, k=15); 10-NN recall vs input L2;
                Shepard Spearman on 200k sampled pairs.
  observer:     10-NN label accuracy in the embedding (3000 ref / 3000 query,
                seeded) for EACH of the three consumer labels.

PRE-STATED PREDICTIONS (grade after the run, disclosed either way):
  P1 dissociation: E_OT2 beats E_L2 on the length column by >= +0.05 while
     losing on ALL THREE conventional metrics; same shape for E_OT3 on pc200.
  P2 inversion: E_OT2 and E_OT3 order the (length, pc200) observer columns
     OPPOSITELY -- each is the best embedding for its own consumer and worse
     than E_L2 for the other. No embedding is best for both.
  P3 matched null: E_OT1 ~ E_L2 on topic (alignment H(topic) ~ 0, the
     conditional law: no headroom, no gain).
  P4 controls: E_iso == E_L2 identically; E_proj2/E_logit2 near-perfect on
     length and near-chance on topic (trivial, disclosed).
Conditional-law bookkeeping: D (probe acc) and A (input-space 10-NN acc) per
consumer on the embedded set, so every gain sits next to its headroom.
"""

import json
import os

import numpy as np

HERE = os.path.expanduser("~/cr-umap")
CACHE = "/home/claude/cr-ann/newsgroups_minilm.npz"
SEED = 0
N_EMB = 6000
EPS = 0.05
KNN = 10


def texts():
    from sklearn.datasets import fetch_20newsgroups
    rm = ("headers", "footers", "quotes")
    tr = fetch_20newsgroups(subset="train", remove=rm)
    te = fetch_20newsgroups(subset="test", remove=rm)
    return tr.data, te.data


def whiten(X, W, eps):
    P = W.T @ W
    P = P / (np.linalg.norm(P, 2) + 1e-12) + eps * np.eye(X.shape[1])
    vals, vecs = np.linalg.eigh(P)
    L = (vecs * np.sqrt(np.clip(vals, 0, None))) @ vecs.T
    return X @ L.T


def knn_acc(E, y, rng):
    from sklearn.neighbors import KNeighborsClassifier
    idx = rng.permutation(len(E))
    ref, qry = idx[: len(E) // 2], idx[len(E) // 2:]
    clf = KNeighborsClassifier(n_neighbors=KNN)
    clf.fit(E[ref], y[ref])
    return float(clf.score(E[qry], y[qry]))


def conventional(X, E, rng):
    from scipy.stats import spearmanr
    from sklearn.manifold import trustworthiness
    from sklearn.neighbors import NearestNeighbors
    tw = float(trustworthiness(X, E, n_neighbors=15))
    nn_x = NearestNeighbors(n_neighbors=KNN + 1).fit(X)
    nn_e = NearestNeighbors(n_neighbors=KNN + 1).fit(E)
    ix = nn_x.kneighbors(return_distance=False)[:, 1:]
    ie = nn_e.kneighbors(return_distance=False)[:, 1:]
    rec = float(np.mean([len(set(a) & set(b)) / KNN for a, b in zip(ix, ie)]))
    i = rng.integers(0, len(X), 200000)
    j = rng.integers(0, len(X), 200000)
    m = i != j
    dx = np.linalg.norm(X[i[m]] - X[j[m]], axis=1)
    de = np.linalg.norm(E[i[m]] - E[j[m]], axis=1)
    shep = float(spearmanr(dx, de).statistic)
    return {"trustworthiness": tw, "knn10_recall": rec, "shepard_spearman": shep}


def main():
    os.makedirs(HERE, exist_ok=True)
    import umap
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier

    z = np.load(CACHE)
    Xtr, ytr, Xte, yte = z["Xtr"], z["ytr"], z["Xte"], z["yte"]
    ttr, tte = texts()
    assert len(ttr) == len(Xtr) and len(tte) == len(Xte)

    rng = np.random.default_rng(SEED)
    sub = rng.choice(len(Xtr), N_EMB, replace=False)
    X = Xtr[sub].astype(np.float64)

    # --- consumer labels on the embedded set; probes fit on the TEST split ---
    len_te = np.log1p([len(t) for t in tte])
    med_len = np.median(len_te)
    y_len_te = (len_te > med_len).astype(int)
    y_len = (np.log1p([len(ttr[i]) for i in sub]) > med_len).astype(int)

    pca = PCA(n_components=201, random_state=0).fit(Xte)
    u = pca.components_[200]
    med_u = np.median(Xte @ u)
    y_pc_te = (Xte @ u > med_u).astype(int)
    y_pc = (X @ u > med_u).astype(int)
    y_top = ytr[sub]

    c_top = LogisticRegression(max_iter=3000, C=10.0).fit(Xte, yte)
    c_len = LogisticRegression(max_iter=3000, C=10.0).fit(Xte, y_len_te)
    c_pc = LogisticRegression(max_iter=3000, C=10.0).fit(Xte, y_pc_te)

    labels = {"topic": y_top, "length": y_len, "pc200": y_pc}
    # conditional-law bookkeeping: D (probe acc on embedded set) and A
    # (input-space 10-NN acc, self-split) per consumer
    book = {}
    r0 = np.random.default_rng(SEED)
    for name, clf, y in (("topic", c_top, y_top), ("length", c_len, y_len),
                         ("pc200", c_pc, y_pc)):
        D = float(clf.score(X, y))
        A = knn_acc(X, y, np.random.default_rng(SEED))
        book[name] = {"D": D, "A_input_knn": A, "H": D - A}
        print(f"[book] {name}: D={D:.3f} A={A:.3f} H={D - A:+.3f}", flush=True)

    # --- the seven embeddings ---
    def emb(Xin, tag):
        print(f"[umap] {tag}...", flush=True)
        return umap.UMAP(n_neighbors=15, min_dist=0.1,
                         random_state=0).fit_transform(Xin)

    E = {}
    E["L2"] = emb(X, "L2")
    E["iso"] = emb(whiten(X, np.zeros((1, X.shape[1])), 1.0), "iso control")
    E["OT_topic"] = emb(whiten(X, c_top.coef_, EPS), "OT topic")
    E["OT_length"] = emb(whiten(X, c_len.coef_, EPS), "OT length")
    E["OT_pc200"] = emb(whiten(X, c_pc.coef_, EPS), "OT pc200")
    E["proj_length"] = emb(whiten(X, c_len.coef_, 0.0), "proj length (eps=0)")
    E["logit_length"] = emb((X @ c_len.coef_.T).reshape(-1, 1), "logit length")

    out = {"seed": SEED, "n": N_EMB, "eps": EPS, "bookkeeping": book,
           "embeddings": {}}
    for tag, e in E.items():
        conv = conventional(X, e, np.random.default_rng(SEED))
        obs = {n: knn_acc(e, y, np.random.default_rng(SEED))
               for n, y in labels.items()}
        out["embeddings"][tag] = {"conventional": conv, "observer": obs}
        print(f"[res] {tag:12s} tw={conv['trustworthiness']:.3f} "
              f"rec={conv['knn10_recall']:.3f} shep={conv['shepard_spearman']:.3f} | "
              f"topic={obs['topic']:.3f} length={obs['length']:.3f} "
              f"pc200={obs['pc200']:.3f}", flush=True)

    np.savez(os.path.join(HERE, "embeddings.npz"),
             **{k: v for k, v in E.items()}, X_idx=sub)
    with open(os.path.join(HERE, "cr_umap_shakedown_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {HERE}/cr_umap_shakedown_result.json", flush=True)


if __name__ == "__main__":
    main()
