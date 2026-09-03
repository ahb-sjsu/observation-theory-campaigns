#!/usr/bin/env python3
"""CR-ANN prereg open item 2 — calibration-split D check for the three MSA-axis
distilled probes (privacy_protection, identity_attack, physical_harm).

Runs BEFORE the seal, touches the CALIBRATION split only (the grading split is
written to disk, hashed, and never opened here — MC2). For each axis:

  1. Materialize the axis corpus from the exact xbse sources (joint_builders
     loaders), dedupe, seeded shuffle (SPLIT_SEED), cap at CAP rows.
  2. Write calibration.jsonl (70%) and grading.jsonl (30%) + sha256 manifest.
  3. LaBSE-encode the calibration texts (the retrieval substrate).
  4. Load the axis's VALIDATED xbse encoder (~/xbse_ckpt/<axis>_joint.pt),
     fit the DimensionScorer axis on calibration pos/neg, score calibration.
  5. Distilled probe = logistic regression, LaBSE embedding -> 1[xbse score>0],
     trained on the first 80% of calibration; D = its accuracy against the TRUE
     axis labels on the remaining 20%.
  6. Also report the direct-label probe's D (reference) and raw L2-1NN alignment
     A on the same 80/20 split, so H = D - A is visible pre-seal.

Output: ~/cr-ann/prereg/calibration_d_result.json (+ per-axis jsonls, manifest).
"""

import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/claude/xbse/src")

HERE = os.path.expanduser("~/cr-ann/prereg")
CKPT = os.path.expanduser("~/xbse_ckpt")
SPLIT_SEED = 20260901  # pinned in PREREG-CR-ANN; disjoint from graded seeds and SEED=0
CAP = 6000
CAL_FRAC = 0.70
PROBE_TRAIN_FRAC = 0.80
THREADS = 16  # Atlas thermal cap (nothing else heavy running)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_axis_rows(axis):
    """(text, label) with label 1 = violated/attack/harm ('-'), 0 = respected ('+'),
    from the exact sources xbse's joint builders use."""
    from xbse.instances import joint_builders as jb

    if axis == "privacy_protection":
        from xbse.instances.privacybse import PrivacyBSEPairSource
        rows = [(t, 1 if s == "-" else 0)
                for _, t, s in PrivacyBSEPairSource()._rows() if s in "+-"]
    elif axis == "identity_attack":
        rows = [(t, 1 if s == "-" else 0)
                for t, s in jb._signed_jsonl_simple(jb.CC_IDENTITY)]
        rows += [(t, 1 if s == "-" else 0)
                 for t, s in jb._signed_jsonl_simple(jb.MHS_IDENTITY)]
    elif axis == "physical_harm":
        from xbse.instances.physharm import PhysHarmBSEPairSource
        rows = [(t, 1 if int(lab) == 1 else 0)
                for _, t, lab in PhysHarmBSEPairSource()._rows()]
        rows += [(t, 1 if s == "-" else 0) for t, s in jb._ethics_rows(jb.HARM_KW)]
    else:
        raise ValueError(axis)
    seen, uniq = set(), []
    for t, y in rows:
        if t not in seen:
            seen.add(t)
            uniq.append((t, int(y)))
    return uniq


def materialize(axis):
    rng = np.random.default_rng(SPLIT_SEED)
    rows = load_axis_rows(axis)
    order = rng.permutation(len(rows))
    rows = [rows[i] for i in order][:CAP]
    n_cal = int(CAL_FRAC * len(rows))
    paths = {}
    for name, part in (("calibration", rows[:n_cal]), ("grading", rows[n_cal:])):
        p = os.path.join(HERE, f"{axis}.{name}.jsonl")
        with open(p, "w", encoding="utf-8") as f:
            for t, y in part:
                f.write(json.dumps({"text": t, "label": y}) + "\n")
        paths[name] = {"path": p, "rows": len(part), "sha256": sha256(p)}
    return rows[:n_cal], paths


def labse_encode(texts, enc_cache={}):
    from sentence_transformers import SentenceTransformer
    if "m" not in enc_cache:
        enc_cache["m"] = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    return enc_cache["m"].encode(texts, batch_size=128, normalize_embeddings=True,
                                 show_progress_bar=False).astype(np.float32)


def xbse_scores(axis, texts, labels):
    """Load the validated joint encoder, fit the centroid valence axis on the
    calibration pos/neg, return signed scores for all calibration texts."""
    import torch
    from xbse.encoder import BSEEncoder

    ckpt = {"privacy_protection": "privacy_joint.pt",
            "identity_attack": "identity_attack_joint.pt",
            "physical_harm": "physharm_joint.pt"}[axis]
    sd = torch.load(os.path.join(CKPT, ckpt), map_location="cpu", weights_only=True)
    # infer base from the checkpoint's embedding table shape
    hid = sd["backbone.embeddings.word_embeddings.weight"].shape[1]
    base = {1024: "BAAI/bge-m3", 768: "sentence-transformers/LaBSE"}[hid]
    enc = BSEEncoder(base_model=base, max_len=192, device="cpu")
    enc.load_state_dict(sd, strict=True)
    print(f"  [{axis}] xbse encoder loaded ({ckpt}, base={base})", flush=True)
    Z = enc.encode(texts, batch_size=32).cpu().numpy()
    pos = Z[np.array(labels) == 0]  # '+' respected
    neg = Z[np.array(labels) == 1]  # '-' violated
    axis_v = pos.mean(0) / (np.linalg.norm(pos.mean(0)) + 1e-9) \
        - neg.mean(0) / (np.linalg.norm(neg.mean(0)) + 1e-9)
    axis_v = axis_v / (np.linalg.norm(axis_v) + 1e-9)
    return Z @ axis_v  # signed: >0 leans respected(+)


def main():
    import torch
    torch.set_num_threads(THREADS)
    os.makedirs(HERE, exist_ok=True)
    from sklearn.linear_model import LogisticRegression

    out = {"split_seed": SPLIT_SEED, "cap": CAP, "cal_frac": CAL_FRAC,
           "probe_train_frac": PROBE_TRAIN_FRAC, "axes": {}}
    for axis in ("privacy_protection", "identity_attack", "physical_harm"):
        print(f"=== {axis} ===", flush=True)
        cal, manifest = materialize(axis)
        texts = [t for t, _ in cal]
        y = np.array([lab for _, lab in cal], dtype=np.int64)
        print(f"  calibration rows: {len(cal)} (violated {int(y.sum())})", flush=True)
        X = labse_encode(texts)
        s = xbse_scores(axis, texts, y)
        y_distill = (s < 0).astype(np.int64)  # score<0 leans violated -> label 1
        agree = float((y_distill == y).mean())
        n_tr = int(PROBE_TRAIN_FRAC * len(cal))
        # distilled probe: LaBSE -> sign of the xbse score
        probe = LogisticRegression(max_iter=3000, C=10.0)
        probe.fit(X[:n_tr], y_distill[:n_tr])
        D_distill = float(probe.score(X[n_tr:], y[n_tr:]))  # vs TRUE labels
        # reference: direct-label probe
        ref = LogisticRegression(max_iter=3000, C=10.0)
        ref.fit(X[:n_tr], y[:n_tr])
        D_direct = float(ref.score(X[n_tr:], y[n_tr:]))
        # alignment A: raw L2 1-NN label accuracy on the same 80/20 split
        import faiss
        idx = faiss.IndexFlatL2(X.shape[1])
        idx.add(X[:n_tr])
        _, nn1 = idx.search(X[n_tr:], 1)
        A = float((y[:n_tr][nn1[:, 0]] == y[n_tr:]).mean())
        rec = {"manifest": manifest, "n_calibration": len(cal),
               "violated_frac": float(y.mean()),
               "xbse_score_label_agreement": agree,
               "D_distilled": D_distill, "D_direct_label": D_direct,
               "A_l2_1nn": A, "H_distilled": D_distill - A,
               "passes_floor": bool(D_distill >= 0.75)}
        out["axes"][axis] = rec
        print(f"  agree(xbse sign, label)={agree:.3f}  D_distilled={D_distill:.3f}  "
              f"D_direct={D_direct:.3f}  A={A:.3f}  H={D_distill - A:+.3f}  "
              f"floor(0.75): {'PASS' if rec['passes_floor'] else 'FAIL'}", flush=True)

    with open(os.path.join(HERE, "calibration_d_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {HERE}/calibration_d_result.json", flush=True)


if __name__ == "__main__":
    main()
