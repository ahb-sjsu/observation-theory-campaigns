#!/usr/bin/env python3
"""CR-ANN post-mortem — POST-HOC DIAGNOSTIC on the graded FAIL (2026-09-02).

Clearly labeled: this is exploratory forensics on the graded raw, exactly like
covering_route.py / mc2_retest.py after the D8-V1 VOID. The prereg and verdict
are untouched; nothing here re-grades anything.

Hypotheses:
  H1 (instrument): single-split calibration H mis-estimates grading headroom.
     The construction cells measured D, A, and gain on the SAME split; the
     sealed design took H from calibration and gain from grading. Test: for
     each consumer recompute D_g (FROZEN probe accuracy on the grading split)
     and A_g (L2-1NN, calibration DB -> all grading queries), H_g = D_g - A_g,
     and conversion_g = mean_gain / H_g. If conversion_g is law-like where
     conversion_cal was not, the law survives and the estimator failed.
  H2 (variance): cross-fit H on calibration (5-fold) to bound the noise of the
     single-split H that arm assignment used.
  H3 (heterogeneity): identity_attack (civil_comments + MHS) and physical_harm
     (BeaverTails + ETHICS) are two-domain joins; per-domain D/A/H/gain on the
     grading split to see whether the join hides opposite regimes.

Output: ~/cr-ann/prereg/postmortem.json + a printed table.
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/claude/xbse/src")

HERE = os.path.expanduser("~/cr-ann/prereg")
CKPT = os.path.expanduser("~/xbse_ckpt")
SPLIT_SEED = 20260901
GRADED_SEEDS = [20260902, 20260903, 20260904]
PROBE_TRAIN_FRAC = 0.80
K = 50
THREADS = int(os.environ.get("CRANN_THREADS", "16"))

FOUNDATIONS = ["fairness-cheating", "loyalty-betrayal",
               "authority-subversion", "sanctity-degradation"]
MSA_AXES = ["privacy_protection", "identity_attack", "physical_harm"]
MSA_CKPT = {"privacy_protection": "privacy_joint.pt",
            "identity_attack": "identity_attack_joint.pt",
            "physical_harm": "physharm_joint.pt"}


def read_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append((d["text"], int(d["label"])))
    return rows


def load_emb(tag):
    return np.load(os.path.join(HERE, f"emb_{tag}.npz"))["X"]


def xbse_scores(axis, texts, labels):
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
    pos, neg = Z[y == 0], Z[y == 1]
    ax = pos.mean(0) / (np.linalg.norm(pos.mean(0)) + 1e-9) \
        - neg.mean(0) / (np.linalg.norm(neg.mean(0)) + 1e-9)
    return Z @ (ax / (np.linalg.norm(ax) + 1e-9))


def domain_tags(name, texts):
    """Which source file each grading text came from (two-domain consumers)."""
    if name == "identity_attack":
        src = {"civil_comments":
               "/archive/ethics-corpora/identity_attack/civil_comments_identity.jsonl",
               "mhs": "/archive/ethics-corpora/identity_attack/mhs_identity.jsonl"}
        sets = {}
        for dom, p in src.items():
            with open(p, encoding="utf-8") as f:
                sets[dom] = {(json.loads(line).get("text") or "").strip()
                             for line in f}
        return [next((d for d, S in sets.items() if t in S), "unknown")
                for t in texts]
    if name == "physical_harm":
        from xbse.instances import joint_builders as jb
        eth = {t for t, _ in jb._ethics_rows(jb.HARM_KW)}
        return ["ethics" if t in eth else "beavertails" for t in texts]
    return None


def main():
    import torch
    torch.set_num_threads(THREADS)
    import faiss
    from sklearn.linear_model import LogisticRegression

    graded = json.load(open(os.path.join(HERE, "graded_result.json")))
    man = json.load(open(os.path.join(HERE, "calibration_d_result.json")))
    out = {}
    for name in FOUNDATIONS + MSA_AXES:
        cal_p = (man["axes"][name]["manifest"]["calibration"]["path"]
                 if name in MSA_AXES
                 else os.path.join(HERE, f"{name}.calibration.jsonl"))
        gr_p = cal_p.replace(".calibration.", ".grading.")
        cal, gr = read_jsonl(cal_p), read_jsonl(gr_p)
        y = np.array([lab for _, lab in cal], dtype=np.int64)
        gy = np.array([lab for _, lab in gr], dtype=np.int64)
        X, Xg = load_emb(f"{name}_cal"), load_emb(f"{name}_grade")
        n_tr = int(PROBE_TRAIN_FRAC * len(cal))
        if name in MSA_AXES:
            s = xbse_scores(name, [t for t, _ in cal], y)
            y_t = (s < 0).astype(np.int64)
        else:
            y_t = y
        probe = LogisticRegression(max_iter=3000, C=10.0)
        probe.fit(X[:n_tr], y_t[:n_tr])
        # grading-split quantities with the FROZEN probe
        D_g = float(probe.score(Xg, gy))
        idx = faiss.IndexFlatL2(X.shape[1])
        idx.add(X)
        _, nn1 = idx.search(Xg, 1)
        A_g = float((y[nn1[:, 0]] == gy).mean())
        H_g = D_g - A_g
        gains = [graded["results"][name][str(sd)]["gain"] for sd in GRADED_SEEDS]
        mg = float(np.mean(gains))
        # H2: cross-fit H on calibration (5-fold)
        rng = np.random.default_rng(SPLIT_SEED)
        order = rng.permutation(len(cal))
        folds = np.array_split(order, 5)
        Hs = []
        for i in range(5):
            te = folds[i]
            tr = np.concatenate([folds[j] for j in range(5) if j != i])
            pf = LogisticRegression(max_iter=3000, C=10.0)
            pf.fit(X[tr], y_t[tr])
            Df = float(pf.score(X[te], y[te]))
            ix = faiss.IndexFlatL2(X.shape[1])
            ix.add(X[tr])
            _, n1 = ix.search(X[te], 1)
            Af = float((y[tr][n1[:, 0]] == y[te]).mean())
            Hs.append(Df - Af)
        rec = {"cal": man["axes"][name] if name in MSA_AXES else None,
               "H_cal_run": graded["consumers"][name]["H"],
               "arm": graded["consumers"][name]["arm"],
               "D_grading": D_g, "A_grading": A_g, "H_grading": H_g,
               "mean_gain": mg,
               "conversion_cal": mg / graded["consumers"][name]["H"]
               if graded["consumers"][name]["H"] > 1e-9 else None,
               "conversion_grading": mg / H_g if abs(H_g) > 1e-9 else None,
               "H_crossfit_mean": float(np.mean(Hs)),
               "H_crossfit_sd": float(np.std(Hs)),
               "H_crossfit_folds": [round(h, 4) for h in Hs]}
        # H3: per-domain on the grading split
        tags = domain_tags(name, [t for t, _ in gr])
        if tags:
            per = {}
            Pg = Xg @ probe.coef_.astype(np.float32).T
            Pdb = X @ probe.coef_.astype(np.float32).T
            _, cand = idx.search(Xg, min(K, X.shape[0]))
            dproj = Pg[:, None, :] - Pdb[cand]
            j = np.argmin((dproj * dproj).sum(-1), axis=1)
            ot_lab = y[cand[np.arange(len(cand)), j]]
            l2_lab = y[cand[:, 0]]
            for dom in sorted(set(tags)):
                m = np.array([t == dom for t in tags])
                if m.sum() < 30:
                    continue
                per[dom] = {"n": int(m.sum()),
                            "D": float(probe.score(Xg[m], gy[m])),
                            "A": float((l2_lab[m] == gy[m]).mean()),
                            "l2_acc": float((l2_lab[m] == gy[m]).mean()),
                            "ot_acc": float((ot_lab[m] == gy[m]).mean()),
                            "gain": float((ot_lab[m] == gy[m]).mean()
                                          - (l2_lab[m] == gy[m]).mean())}
            rec["per_domain"] = per
        out[name] = rec
        print(f"[pm] {name}: arm={rec['arm']} H_cal={rec['H_cal_run']:+.3f} "
              f"H_grading={H_g:+.3f} (D_g={D_g:.3f} A_g={A_g:.3f}) "
              f"gain={mg:+.3f} conv_cal={rec['conversion_cal'] and round(rec['conversion_cal'],2)} "
              f"conv_g={rec['conversion_grading'] and round(rec['conversion_grading'],2)} "
              f"Hxfit={np.mean(Hs):+.3f}±{np.std(Hs):.3f}", flush=True)
        if tags:
            for dom, d in rec.get("per_domain", {}).items():
                print(f"      {dom}: n={d['n']} D={d['D']:.3f} A={d['A']:.3f} "
                      f"gain={d['gain']:+.3f}", flush=True)

    with open(os.path.join(HERE, "postmortem.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {HERE}/postmortem.json", flush=True)


if __name__ == "__main__":
    main()
