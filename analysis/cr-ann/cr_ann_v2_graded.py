#!/usr/bin/env python3
"""CR-ANN-V2 graded run -- executes PREREG-CR-ANN-V2 v1.0 (SEALED 2026-09-03,
16b2f4c) exactly as written. Runs on Atlas.

Order (MC2 by construction): verify the six units' sealed manifests
(calibration AND grading sha256) -> rebuild the FROZEN graded probes on the
first 80% of calibration (distilled target where the seal record says so) ->
only then open grading. Seeds {20260912, 20260913, 20260914}; per-seed query
redraw floor(0.8*n_grading) without replacement; FAISS IndexFlatL2 k=50 over
the full calibration DB; MC1 isotropic control; S1 oracle ceiling; S2 slope.

Bars (frozen): B1 misaligned units: mean gain >= max(0.10*H_xfit, 0.010) AND
every seed gain >= 0 AND recall@1 <= 0.5 every seed. B2 matched: mean <=
+0.010 AND every seed <= +0.020. Verdict = B1 AND B2. B3 secondary:
Spearman(H_xfit, mean gain) >= 0.6 over ALL ok units (excluded ones included
descriptively).
"""
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/claude/xbse/src")

HERE = os.path.expanduser("~/cr-ann/prereg_v2")
CKPT = os.path.expanduser("~/xbse_ckpt")
GRADED_SEEDS = [20260912, 20260913, 20260914]
PROBE_TRAIN_FRAC = 0.80
QUERY_FRAC = 0.80
K = 50
MC1_TOL = 0.005
THREADS = int(os.environ.get("CRANN_THREADS", "16"))
DISTILL_CKPT = {"privacy_aita": "privacy_joint.pt",
                "autonomy_dark": "autonomy_joint.pt",
                "care_moralstories": "care_joint.pt"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def read_jsonl(p):
    rows = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append((d["text"], int(d["label"])))
    return rows


_LABSE = {}


def labse_cached(tag, texts):
    p = os.path.join(HERE, f"emb_{tag}.npz")
    key = hashlib.sha256("\n".join(texts).encode()).hexdigest()[:16]
    if os.path.exists(p):
        z = np.load(p)
        if str(z["key"]) == key:
            return z["X"]
    from sentence_transformers import SentenceTransformer
    if "m" not in _LABSE:
        _LABSE["m"] = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    X = _LABSE["m"].encode(texts, batch_size=128, normalize_embeddings=True,
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


def main():
    import torch
    torch.set_num_threads(THREADS)
    import faiss
    from scipy.stats import spearmanr
    from sklearn.linear_model import LogisticRegression

    qual = json.load(open(os.path.join(HERE, "qualification_v2.json")))
    units = {u: r for u, r in qual["units"].items() if r.get("status") == "ok"}

    # 1. verify every sealed manifest before anything runs
    for u, r in units.items():
        for split, m in r["manifest"].items():
            assert sha256(m["path"]) == m["sha256"], f"MANIFEST MISMATCH {u}/{split}"
    print(f"[manifest] all {2*len(units)} sealed split files verified", flush=True)

    # 2. frozen probes (calibration only)
    frozen = {}
    for u, r in units.items():
        cal = read_jsonl(r["manifest"]["calibration"]["path"])
        texts = [t for t, _ in cal]
        y = np.array([lab for _, lab in cal], dtype=np.int64)
        X = labse_cached(f"{u}_cal", texts)
        n_tr = int(PROBE_TRAIN_FRAC * len(cal))
        if u in DISTILL_CKPT and r.get("distilled"):
            target = xbse_target(DISTILL_CKPT[u], texts, y)
        else:
            target = y
        probe = LogisticRegression(max_iter=3000, C=10.0)
        probe.fit(X[:n_tr], target[:n_tr])
        frozen[u] = {"W": probe.coef_.astype(np.float32), "X_db": X, "y_db": y}
        print(f"[freeze] {u}: probe trained (distill={bool(u in DISTILL_CKPT and r.get('distilled'))})",
              flush=True)

    # 3. grading (opened only now)
    results, mc1_ok = {}, True
    for u, r in units.items():
        gr = read_jsonl(r["manifest"]["grading"]["path"])
        gtexts = [t for t, _ in gr]
        gy = np.array([lab for _, lab in gr], dtype=np.int64)
        Xg = labse_cached(f"{u}_grade", gtexts)
        Xdb, ydb, W = frozen[u]["X_db"], frozen[u]["y_db"], frozen[u]["W"]
        idx = faiss.IndexFlatL2(Xdb.shape[1])
        idx.add(Xdb)
        per = {}
        for seed in GRADED_SEEDS:
            rng = np.random.default_rng(seed)
            nq = int(QUERY_FRAC * len(gr))
            qi = rng.choice(len(gr), size=nq, replace=False)
            Xq, yq = Xg[qi], gy[qi]
            _, cand = idx.search(Xq, min(K, Xdb.shape[0]))
            l2 = float((ydb[cand[:, 0]] == yq).mean())
            Pdb, Pq = Xdb @ W.T, Xq @ W.T
            dp = Pq[:, None, :] - Pdb[cand]
            j = np.argmin((dp * dp).sum(-1), axis=1)
            chosen = cand[np.arange(len(cand)), j]
            ot = float((ydb[chosen] == yq).mean())
            rec1 = float((chosen == cand[:, 0]).mean())
            df = Xq[:, None, :] - Xdb[cand]
            j0 = np.argmin((df * df).sum(-1), axis=1)
            iso = float((ydb[cand[np.arange(len(cand)), j0]] == yq).mean())
            ok = abs(iso - l2) < MC1_TOL
            mc1_ok &= ok
            oracle = float((ydb[cand] == yq[:, None]).any(1).mean())
            per[seed] = {"n_queries": nq, "l2_acc": l2, "ot_acc": ot,
                         "gain": ot - l2, "recall1": rec1, "iso_pass": bool(ok),
                         "oracle": oracle}
            print(f"[grade] {u} seed {seed}: L2={l2:.3f} OT={ot:.3f} "
                  f"gain={ot-l2:+.3f} rec1={rec1:.3f} iso={'ok' if ok else 'FAIL'} "
                  f"oracle={oracle:.3f}", flush=True)
        results[u] = per

    # 4. bars
    b1_items, b2_items = [], []
    for u, r in units.items():
        gains = [results[u][s]["gain"] for s in GRADED_SEEDS]
        mg = float(np.mean(gains))
        if r["arm"] == "misaligned":
            bar = max(0.10 * r["H_xfit"], 0.010)
            ok = (mg >= bar) and all(g >= 0 for g in gains) and \
                all(results[u][s]["recall1"] <= 0.5 for s in GRADED_SEEDS)
            b1_items.append((u, mg, bar, bool(ok)))
        elif r["arm"] == "matched":
            ok = (mg <= 0.010) and all(g <= 0.020 for g in gains)
            b2_items.append((u, mg, bool(ok)))
    B1 = len(b1_items) > 0 and all(x[3] for x in b1_items)
    B2 = len(b2_items) > 0 and all(x[2] for x in b2_items)
    hs = [r["H_xfit"] for r in units.values()]
    mgs = [float(np.mean([results[u][s]["gain"] for s in GRADED_SEEDS]))
           for u in units]
    sp = float(spearmanr(hs, mgs).statistic)
    B3 = sp >= 0.6
    slope = float(np.polyfit(hs, mgs, 1)[0])
    mc3 = qual["MC3"]["sufficient"]
    verdict = "VOID" if (not mc1_ok or not mc3) else ("PASS" if (B1 and B2) else "FAIL")

    out = {"prereg": "PREREG-CR-ANN-V2 v1.0 (sealed 2026-09-03, 16b2f4c)",
           "executed": "2026-09-03", "results": {u: {str(s): r for s, r in p.items()}
                                                 for u, p in results.items()},
           "bars": {"B1": B1, "B1_items": b1_items, "B2": B2, "B2_items": b2_items,
                    "B3": B3, "B3_spearman": sp},
           "secondaries": {"S2_slope": slope},
           "MCs": {"MC1": bool(mc1_ok), "MC2": "commit order", "MC3": bool(mc3),
                   "MC4": "seeds disjoint (sealed scan)"},
           "VERDICT": verdict}
    with open(os.path.join(HERE, "graded_v2.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"[VERDICT] {verdict}  B1={B1} {b1_items}  B2={B2} {b2_items}  "
          f"B3={B3} (sp={sp:.3f}, slope={slope:.3f})  MC1={mc1_ok}", flush=True)
    print(f"wrote {HERE}/graded_v2.json", flush=True)


if __name__ == "__main__":
    main()
