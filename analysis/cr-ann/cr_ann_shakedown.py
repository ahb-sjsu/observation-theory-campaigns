#!/usr/bin/env python3
"""Consumer-relative ANN — smallest confirmatory shakedown (UNSEALED, exploratory).

OT prediction: at a fixed candidate budget k, reranking FAISS L2 candidates by the
consumer's read operator P_C improves downstream consumer performance DESPITE
worsening ordinary embedding-space fidelity. The dissociation is the claim.

Controlled substrate so the mechanism is testable and the code is validated:
- Embeddings in R^d. A small RELEVANT subspace A (m<<d) drives the downstream
  label; the IRRELEVANT dims carry LARGER variance, so L2 distance is
  distractor-dominated and the L2-nearest neighbour is a poor consumer match.
- Consumer readout y = A x (linear); its read operator is P_C = J^T J = A^T A
  (for a nonlinear consumer, P_C(x) = J(x)^T J(x) locally). Downstream TASK =
  classification: the label is the nearest of C fixed centroids in the relevant
  subspace, so the label depends ONLY on A x.

Pipeline: FAISS IndexFlatL2 candidate gen (top-k) -> rerank {L2 | OT d_C} ->
1-NN class prediction from the reranked top-1.

Reported: downstream accuracy (OT should be higher) and embedding-space fidelity
(recall@1 vs the true L2-nearest, and mean L2 distance of the chosen neighbour;
OT should be worse). Negative control: P_C = I -> OT == L2 (no dissociation).
Anisotropy sweep: dissociation should grow with the distractor/relevant variance
ratio (the misalignment dial), echoing the flip law.
"""
import numpy as np

try:
    import faiss
    HAVE_FAISS = True
except Exception:
    HAVE_FAISS = False

RNG = np.random.default_rng(0)
D = 32          # embedding dim
M = 4           # relevant-subspace dim (the consumer reads these)
N_DB = 20000
N_Q = 2000
K = 50          # candidate budget
N_CLASS = 8


def make_world(distractor_var):
    """Relevant dims variance 1; irrelevant dims variance `distractor_var`."""
    A = np.zeros((M, D), dtype=np.float32)
    A[np.arange(M), np.arange(M)] = 1.0            # relevant subspace = first M dims
    scale = np.ones(D, dtype=np.float32)
    scale[M:] = np.sqrt(distractor_var)            # inflate irrelevant dims
    centroids = RNG.standard_normal((N_CLASS, M)).astype(np.float32) * 1.5
    return A, scale, centroids


def label(xrel, centroids):
    d = ((xrel[:, None, :] - centroids[None, :, :]) ** 2).sum(-1)
    return d.argmin(1)


def gen(n, scale):
    return (RNG.standard_normal((n, D)).astype(np.float32) * scale)


def candidates_faiss(db, q, k):
    idx = faiss.IndexFlatL2(D)
    idx.add(db)
    _, I = idx.search(q, k)
    return I


def candidates_numpy(db, q, k):
    out = np.empty((len(q), k), dtype=np.int64)
    for s in range(0, len(q), 256):
        qq = q[s:s + 256]
        d2 = ((qq[:, None, :] - db[None, :, :]) ** 2).sum(-1)
        out[s:s + len(qq)] = np.argpartition(d2, k, axis=1)[:, :k]
    return out


def run(distractor_var, P_C_iso=False, seed_tag=""):
    A, scale, centroids = make_world(distractor_var)
    db = gen(N_DB, scale)
    q = gen(N_Q, scale)
    db_y = label(db @ A.T, centroids)
    q_y = label(q @ A.T, centroids)

    cand = (candidates_faiss if HAVE_FAISS else candidates_numpy)(db, q, K)

    # P_C: consumer read operator. OT case = A^T A; isotropic control = I.
    PC = np.eye(D, dtype=np.float32) if P_C_iso else (A.T @ A)

    acc = {}
    fidelity = {}
    meanL2 = {}
    for name in ("L2", "OT"):
        chosen = np.empty(N_Q, dtype=np.int64)
        for i in range(N_Q):
            cids = cand[i]
            diff = db[cids] - q[i]                       # (K, D)
            if name == "L2":
                score = (diff * diff).sum(1)
            else:
                score = np.einsum("kd,de,ke->k", diff, PC, diff)  # d_C^2
            chosen[i] = cids[score.argmin()]
        pred = db_y[chosen]
        acc[name] = float((pred == q_y).mean())
        # embedding fidelity: is the chosen neighbour the true L2-nearest? (cand[:,0])
        fidelity[name] = float((chosen == cand[:, 0]).mean())
        meanL2[name] = float(np.sqrt(((db[chosen] - q) ** 2).sum(1)).mean())
    return acc, fidelity, meanL2


def main():
    print(f"backend: {'FAISS IndexFlatL2' if HAVE_FAISS else 'numpy exact-L2 (faiss absent)'}"
          f"  D={D} M={M} N_db={N_DB} N_q={N_Q} k={K} classes={N_CLASS}\n")

    print("=== MAIN: anisotropic consumer (distractor_var=9) ===")
    acc, fid, l2 = run(9.0)
    print(f"  downstream accuracy : L2={acc['L2']:.3f}  OT={acc['OT']:.3f}   "
          f"(OT-L2 = {acc['OT']-acc['L2']:+.3f})")
    print(f"  embedding recall@1  : L2={fid['L2']:.3f}  OT={fid['OT']:.3f}   "
          f"(OT picks the true L2-nearest this often)")
    print(f"  mean L2 dist chosen : L2={l2['L2']:.3f}  OT={l2['OT']:.3f}   "
          f"(OT chooses L2-farther neighbours)")
    diss = (acc['OT'] > acc['L2'] + 0.02) and (fid['OT'] < fid['L2'] - 0.02)
    print(f"  --> DISSOCIATION (consumer up, embedding fidelity down): {diss}\n")

    print("=== NEGATIVE CONTROL: isotropic consumer P_C=I (same data) ===")
    acc0, fid0, l20 = run(9.0, P_C_iso=True)
    print(f"  downstream accuracy : L2={acc0['L2']:.3f}  OT={acc0['OT']:.3f}   "
          f"(should be ~equal)")
    print(f"  embedding recall@1  : L2={fid0['L2']:.3f}  OT={fid0['OT']:.3f}   "
          f"(should be ~equal)")
    print(f"  --> no dissociation expected: "
          f"{abs(acc0['OT']-acc0['L2'])<0.01 and abs(fid0['OT']-fid0['L2'])<0.01}\n")

    print("=== ANISOTROPY SWEEP (distractor/relevant variance ratio) ===")
    print(f"  {'var':>5}  {'acc_L2':>7} {'acc_OT':>7} {'d_acc':>7}  "
          f"{'fid_OT':>7}  dissociation")
    for v in (1.0, 2.0, 4.0, 9.0, 16.0):
        a, f, _ = run(v)
        d = (a['OT'] > a['L2'] + 0.02) and (f['OT'] < f['L2'] - 0.02)
        print(f"  {v:5.0f}  {a['L2']:7.3f} {a['OT']:7.3f} {a['OT']-a['L2']:+7.3f}  "
              f"{f['OT']:7.3f}  {d}")
    print("\n(v=1 isotropic-ish -> small effect; effect grows with misalignment.)")


if __name__ == "__main__":
    main()
