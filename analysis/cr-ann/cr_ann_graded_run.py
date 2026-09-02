#!/usr/bin/env python3
"""CR-ANN graded run — executes PREREG-CR-ANN v1.0 (SEALED 2026-09-02, d68b292)
exactly as written. Runs on Atlas.

Order of operations (MC2 by construction):
  1. Verify the sha256 manifests of the six sealed MSA split files.
  2. Materialize the four Social-Chem foundation splits with the sealed
     machinery (split seed 20260901, balanced <=3000+3000, 70/30), hash them.
  3. For every consumer: LaBSE-encode calibration; build the FROZEN probe
     (MSA axes: distill the xbse joint encoder's centroid-axis score, probe =
     logistic LaBSE->sign(score) on the first 80% of calibration; foundations:
     logistic LaBSE->label on the first 80%); measure D (vs true labels,
     last 20%) and A (L2-1NN, same internal split); assign the arm by the
     sealed rule (misaligned: D>=0.75 & H>=0.04; matched: H<0.02; else
     excluded). All of this touches CALIBRATION ONLY.
  4. Only then open the grading splits. Per graded seed {20260902, 20260903,
     20260904}: redraw floor(0.8*n_grading) queries without replacement
     (operationalization of "redraw the grading queries", recorded as
     executed); FAISS IndexFlatL2 k=50 over the FULL calibration database;
     score L2 top-1, OT rerank (P_C = W^T W), recall@1, isotropic control
     (MC1), oracle ceiling (S1).
  5. Grade B1/B2 (verdict), B3 (secondary), MC1-MC4; write
     ~/cr-ann/prereg/graded_result.json.

Every constant below is the sealed value; nothing is tuned here.
"""

import csv
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/claude/xbse/src")

HERE = os.path.expanduser("~/cr-ann/prereg")
CKPT = os.path.expanduser("~/xbse_ckpt")
TSV = "/archive/ethics-corpora/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv"

SPLIT_SEED = 20260901
GRADED_SEEDS = [20260902, 20260903, 20260904]
CAP = 6000
FOUNDATION_PER_CLASS = 3000
CAL_FRAC = 0.70
PROBE_TRAIN_FRAC = 0.80
QUERY_FRAC = 0.80          # per-seed redraw of the grading split (operationalization)
K = 50
D_FLOOR, H_MIS, H_MATCH = 0.75, 0.04, 0.02
B1_FRAC, B1_RECALL, B2_GAIN, B3_SPEARMAN = 0.3, 0.5, 0.01, 0.6
MC1_TOL = 0.005
THREADS = int(os.environ.get("CRANN_THREADS", "16"))  # Atlas cap: 20 total across jobs

FOUNDATIONS = ["fairness-cheating", "loyalty-betrayal",
               "authority-subversion", "sanctity-degradation"]
MSA_AXES = ["privacy_protection", "identity_attack", "physical_harm"]
MSA_CKPT = {"privacy_protection": "privacy_joint.pt",
            "identity_attack": "identity_attack_joint.pt",
            "physical_harm": "physharm_joint.pt"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append((d["text"], int(d["label"])))
    return rows


# ---------------------------------------------------------------- step 1+2
def verify_msa_manifests():
    man = json.load(open(os.path.join(HERE, "calibration_d_result.json")))
    for axis in MSA_AXES:
        for split, m in man["axes"][axis]["manifest"].items():
            actual = sha256(m["path"])
            assert actual == m["sha256"], f"MANIFEST MISMATCH {axis}/{split}"
    print("[manifest] all six sealed MSA split files verified", flush=True)
    return man


def materialize_foundations():
    rng_master = np.random.default_rng(SPLIT_SEED)
    rows = []
    with open(TSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            a = (r.get("action") or "").strip()
            if not a:
                continue
            mf = r.get("rot-moral-foundations") or ""
            rows.append((a, mf))
    seen, uniq = set(), []
    for a, mf in rows:
        if a not in seen:
            seen.add(a)
            uniq.append((a, mf))
    print(f"[foundations] unique actions: {len(uniq)}", flush=True)
    out = {}
    for fnd in FOUNDATIONS:
        rng = np.random.default_rng(SPLIT_SEED)  # same machinery per consumer
        pos = [(a, 1) for a, mf in uniq if fnd in mf]
        neg = [(a, 0) for a, mf in uniq if fnd not in mf]
        rng.shuffle(pos)
        rng.shuffle(neg)
        n = min(FOUNDATION_PER_CLASS, len(pos), len(neg))
        sel = pos[:n] + neg[:n]
        rng.shuffle(sel)
        sel = sel[:CAP]
        n_cal = int(CAL_FRAC * len(sel))
        man = {}
        for name, part in (("calibration", sel[:n_cal]), ("grading", sel[n_cal:])):
            p = os.path.join(HERE, f"{fnd}.{name}.jsonl")
            with open(p, "w", encoding="utf-8") as f:
                for t, y in part:
                    f.write(json.dumps({"text": t, "label": y}) + "\n")
            man[name] = {"path": p, "rows": len(part), "sha256": sha256(p)}
        out[fnd] = man
        print(f"[foundations] {fnd}: pos={len(pos)} -> {n}+{n}, "
              f"cal={man['calibration']['rows']} grade={man['grading']['rows']}",
              flush=True)
    return out


# ---------------------------------------------------------------- encoders
_LABSE = {}


def labse(texts):
    from sentence_transformers import SentenceTransformer
    if "m" not in _LABSE:
        _LABSE["m"] = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    return _LABSE["m"].encode(texts, batch_size=128, normalize_embeddings=True,
                              show_progress_bar=False).astype(np.float32)


def labse_cached(tag, texts):
    p = os.path.join(HERE, f"emb_{tag}.npz")
    key = hashlib.sha256("\n".join(texts).encode()).hexdigest()[:16]
    if os.path.exists(p):
        z = np.load(p, allow_pickle=False)
        if str(z["key"]) == key:
            return z["X"]
    X = labse(texts)
    np.savez(p, X=X, key=np.str_(key))
    return X


def xbse_scores(axis, texts, labels):
    """Identical to the seal-time distillation (cr_ann_calibration_d.py)."""
    import torch
    from xbse.encoder import BSEEncoder
    sd = torch.load(os.path.join(CKPT, MSA_CKPT[axis]), map_location="cpu",
                    weights_only=True)
    hid = sd["backbone.embeddings.word_embeddings.weight"].shape[1]
    base = {1024: "BAAI/bge-m3", 768: "sentence-transformers/LaBSE"}[hid]
    enc = BSEEncoder(base_model=base, max_len=192, device="cpu")
    enc.load_state_dict(sd, strict=True)
    Z = enc.encode(texts, batch_size=32).cpu().numpy()
    del enc
    y = np.array(labels)
    pos = Z[y == 0]
    neg = Z[y == 1]
    ax = pos.mean(0) / (np.linalg.norm(pos.mean(0)) + 1e-9) \
        - neg.mean(0) / (np.linalg.norm(neg.mean(0)) + 1e-9)
    ax = ax / (np.linalg.norm(ax) + 1e-9)
    return Z @ ax


# ---------------------------------------------------------------- main
def main():
    import torch
    torch.set_num_threads(THREADS)
    import faiss
    from scipy.stats import spearmanr
    from sklearn.linear_model import LogisticRegression

    os.makedirs(HERE, exist_ok=True)
    man_msa = verify_msa_manifests()
    man_fnd = materialize_foundations()

    consumers = {}
    # ---- calibration phase: probes, D/A/H, arms (calibration split ONLY) ----
    for name in FOUNDATIONS + MSA_AXES:
        man = man_msa["axes"][name]["manifest"] if name in MSA_AXES else man_fnd[name]
        cal = read_jsonl(man["calibration"]["path"])
        texts = [t for t, _ in cal]
        y = np.array([lab for _, lab in cal], dtype=np.int64)
        X = labse_cached(f"{name}_cal", texts)
        n_tr = int(PROBE_TRAIN_FRAC * len(cal))
        if name in MSA_AXES:
            s = xbse_scores(name, texts, y)
            y_target = (s < 0).astype(np.int64)  # sign of the validated score
        else:
            y_target = y
        probe = LogisticRegression(max_iter=3000, C=10.0)
        probe.fit(X[:n_tr], y_target[:n_tr])
        D = float(probe.score(X[n_tr:], y[n_tr:]))       # vs TRUE labels
        idx = faiss.IndexFlatL2(X.shape[1])
        idx.add(X[:n_tr])
        _, nn1 = idx.search(X[n_tr:], 1)
        A = float((y[:n_tr][nn1[:, 0]] == y[n_tr:]).mean())
        H = D - A
        if D >= D_FLOOR and H >= H_MIS:
            arm = "misaligned"
        elif H < H_MATCH:
            arm = "matched"
        else:
            arm = "excluded"
        consumers[name] = {"D": D, "A": A, "H": H, "arm": arm,
                           "n_calibration": len(cal),
                           "W": probe.coef_.astype(np.float32),
                           "X_db": X, "y_db": y,
                           "grading_path": man["grading"]["path"]}
        print(f"[qualify] {name}: D={D:.3f} A={A:.3f} H={H:+.3f} -> {arm}",
              flush=True)

    arms = {n: c["arm"] for n, c in consumers.items()}
    n_mis = sum(1 for a in arms.values() if a == "misaligned")
    n_mat = sum(1 for a in arms.values() if a == "matched")
    mc3 = (n_mis >= 2) and (n_mat >= 1)
    print(f"[MC3] misaligned={n_mis} matched={n_mat} -> "
          f"{'ok' if mc3 else 'VOID'}", flush=True)

    # ---- grading phase (grading splits opened here, after the freeze) ----
    results, mc1_ok = {}, True
    for name, c in consumers.items():
        grade = read_jsonl(c["grading_path"])
        gtexts = [t for t, _ in grade]
        gy = np.array([lab for _, lab in grade], dtype=np.int64)
        Xg_all = labse_cached(f"{name}_grade", gtexts)
        Xdb, ydb, W = c["X_db"], c["y_db"], c["W"]
        idx = faiss.IndexFlatL2(Xdb.shape[1])
        idx.add(Xdb)
        per_seed = {}
        for seed in GRADED_SEEDS:
            rng = np.random.default_rng(seed)
            nq = int(QUERY_FRAC * len(grade))
            qi = rng.choice(len(grade), size=nq, replace=False)
            Xq, yq = Xg_all[qi], gy[qi]
            _, cand = idx.search(Xq, min(K, Xdb.shape[0]))
            l2_acc = float((ydb[cand[:, 0]] == yq).mean())
            # OT rerank in the probe's read space
            Pdb, Pq = Xdb @ W.T, Xq @ W.T
            dproj = Pq[:, None, :] - Pdb[cand]
            j = np.argmin((dproj * dproj).sum(-1), axis=1)
            chosen = cand[np.arange(len(cand)), j]
            ot_acc = float((ydb[chosen] == yq).mean())
            rec1 = float((chosen == cand[:, 0]).mean())
            # MC1: isotropic P_C = I over the same candidates
            dfull = Xq[:, None, :] - Xdb[cand]
            j0 = np.argmin((dfull * dfull).sum(-1), axis=1)
            iso_acc = float((ydb[cand[np.arange(len(cand)), j0]] == yq).mean())
            iso_pass = abs(iso_acc - l2_acc) < MC1_TOL
            mc1_ok &= iso_pass
            # S1: oracle ceiling over the candidate set
            oracle = float((ydb[cand] == yq[:, None]).any(1).mean())
            per_seed[seed] = {"n_queries": nq, "l2_acc": l2_acc, "ot_acc": ot_acc,
                              "gain": ot_acc - l2_acc, "recall1": rec1,
                              "iso_acc": iso_acc, "iso_pass": bool(iso_pass),
                              "oracle_ceiling": oracle}
            print(f"[grade] {name} seed {seed}: L2={l2_acc:.3f} OT={ot_acc:.3f} "
                  f"gain={ot_acc - l2_acc:+.3f} rec1={rec1:.3f} "
                  f"iso={'ok' if iso_pass else 'FAIL'} oracle={oracle:.3f}",
                  flush=True)
        results[name] = per_seed

    # ---- bars ----
    b1_items, b2_items = [], []
    for name, c in consumers.items():
        for seed in GRADED_SEEDS:
            r = results[name][seed]
            if c["arm"] == "misaligned":
                ok = (r["gain"] >= B1_FRAC * c["H"]) and (r["recall1"] <= B1_RECALL)
                b1_items.append((name, seed, ok))
            elif c["arm"] == "matched":
                ok = r["gain"] <= B2_GAIN
                b2_items.append((name, seed, ok))
    B1 = all(ok for _, _, ok in b1_items) and len(b1_items) > 0
    B2 = all(ok for _, _, ok in b2_items) and len(b2_items) > 0
    # B3 primary: Spearman(H, gain) pooled over QUALIFYING consumers x seeds
    hs, gs = [], []
    for name, c in consumers.items():
        if c["arm"] in ("misaligned", "matched"):
            for seed in GRADED_SEEDS:
                hs.append(c["H"])
                gs.append(results[name][seed]["gain"])
    sp = float(spearmanr(hs, gs).statistic) if len(set(hs)) > 1 else float("nan")
    # B3 weights clause (descriptive over the three MSA axes' mean gains)
    mg = {a: float(np.mean([results[a][s]["gain"] for s in GRADED_SEEDS]))
          for a in MSA_AXES}
    weights_clause = (mg["privacy_protection"] >= mg["physical_harm"]) and \
                     (mg["identity_attack"] >= mg["physical_harm"])
    B3 = (sp >= B3_SPEARMAN) and weights_clause
    # S2: slope of gain vs H
    slope = float(np.polyfit(hs, gs, 1)[0]) if len(set(hs)) > 1 else float("nan")

    void = (not mc1_ok) or (not mc3)
    verdict = "VOID" if void else ("PASS" if (B1 and B2) else "FAIL")

    out = {"prereg": "PREREG-CR-ANN v1.0 (sealed 2026-09-02, d68b292)",
           "executed": "2026-09-02",
           "operationalization": {
               "query_redraw": f"per seed, floor({QUERY_FRAC}*n_grading) queries "
                               "without replacement from the grading split",
               "probe": "frozen at calibration (first 80% of calibration split), "
                        "identical to the seal-time D measurement"},
           "foundation_manifests": man_fnd,
           "consumers": {n: {k: (float(v) if isinstance(v, (int, float, np.floating))
                                 else v)
                             for k, v in c.items()
                             if k in ("D", "A", "H", "arm", "n_calibration")}
                         for n, c in consumers.items()},
           "results": {n: {str(s): r for s, r in rs.items()}
                       for n, rs in results.items()},
           "bars": {"B1": B1, "B1_items": [(n, s, bool(o)) for n, s, o in b1_items],
                    "B2": B2, "B2_items": [(n, s, bool(o)) for n, s, o in b2_items],
                    "B3": B3, "B3_spearman": sp,
                    "B3_weights_clause": bool(weights_clause),
                    "msa_mean_gains": mg},
           "manipulation_checks": {"MC1_iso": bool(mc1_ok), "MC2": "by commit order",
                                   "MC3_sufficiency": bool(mc3),
                                   "MC4_seeds": "disjoint from construction SEED=0"},
           "secondaries": {"S2_slope_gain_vs_H": slope},
           "VERDICT": verdict}
    with open(os.path.join(HERE, "graded_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[VERDICT] {verdict}   B1={B1} B2={B2} B3={B3} "
          f"(spearman={sp:.3f}, weights_clause={weights_clause}) "
          f"MC1={mc1_ok} MC3={mc3}", flush=True)
    print(f"wrote {HERE}/graded_result.json", flush=True)


if __name__ == "__main__":
    main()
