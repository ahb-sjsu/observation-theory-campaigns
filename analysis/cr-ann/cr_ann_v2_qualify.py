#!/usr/bin/env python3
"""CR-ANN-V2 seal-time qualification (PREREG-CR-ANN-V2, sealing 2026-09-03).

Resolves seal open items 1+2: pin single-domain unit corpora with sha256
manifests, and run 5-fold CROSS-FIT qualification (Change 1) touching the
CALIBRATION split only. Grading splits are written and hashed but NOT opened.

Units (axis, single source corpus) -- all fresh, never in V1 or construction.
legitimacy is EXCLUDED: it maps to authority-subversion, a V1-burned consumer.

Distillation (prereg rule): where a validated xbse joint checkpoint exists for
the axis, the probe target is the sign of its centroid-axis score; else direct
labels. Any checkpoint that fails to load falls back to direct labels with a
recorded note (the prereg's own fallback clause).
"""
import csv
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/claude/xbse/src")

HERE = os.path.expanduser("~/cr-ann/prereg_v2")
CKPT = os.path.expanduser("~/xbse_ckpt")
CORP = "/archive/ethics-corpora"
SPLIT_SEED = 20260911
CAP = 6000
CAL_FRAC = 0.70
NFOLD = 5
THREADS = int(os.environ.get("CRANN_THREADS", "8"))

# unit -> (axis, source path, loader kind, xbse checkpoint or None)
UNITS = {
    "privacy_aita":   ("privacy_protection", f"{CORP}/privacy/aita_privacy_labeled.jsonl", "signed_field:privacy", "privacy_joint.pt"),
    "fairness_mhs":   ("fairness_equity",     f"{CORP}/mhs/mhs_fairness.jsonl",            "signed_sign",          None),
    "autonomy_dark":  ("autonomy_respect",    f"{CORP}/darkpattern/dataset.tsv",           "darkpattern_tsv",      "autonomy_joint.pt"),
    "care_moralstories": ("virtue_care",      f"{CORP}/moral_stories/care_signed.jsonl",   "signed_sign",          "care_joint.pt"),
    "societal_env":   ("societal_environmental", f"{CORP}/environmental/env_labeled.jsonl", "signed_field:env",    None),
    "epistemic_sc":   ("epistemic_quality",   f"{CORP}/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv", "socialchem_kw", None),
}
EPI_KW = ("lie", "lying", "lied", "honest", "dishonest", "truth", "truthful",
          "deceive", "deceiv", "mislead")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load_unit(kind, path):
    """-> list[(text, label)], label 1 = violated/negative valence."""
    rows = []
    if kind.startswith("signed_field:"):
        field = kind.split(":")[1]
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                t = (d.get("text") or "").strip()
                v = d.get(field)
                if len(t) >= 20 and isinstance(v, (int, float)) and abs(v) > 0.05:
                    rows.append((t, 1 if v < 0 else 0))
    elif kind == "signed_sign":
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                t = (d.get("text") or "").strip()
                s = d.get("sign")
                if len(t) >= 12 and s in ("+", "-"):
                    rows.append((t, 1 if s == "-" else 0))
    elif kind == "darkpattern_tsv":
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                t = (r.get("text") or "").strip()
                lab = str(r.get("label", "")).strip()
                if len(t) >= 12 and lab in ("0", "1"):
                    rows.append((t, int(lab)))
    elif kind == "socialchem_kw":
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                a = (r.get("action") or "").strip()
                j = (r.get("action-moral-judgment") or "").strip()
                low = a.lower()
                if not a or not j or not any(k in low for k in EPI_KW):
                    continue
                try:
                    jv = float(j)
                except ValueError:
                    continue
                if jv != 0:
                    rows.append((a, 1 if jv < 0 else 0))
    # dedupe
    seen, uniq = set(), []
    for t, y in rows:
        if t not in seen:
            seen.add(t)
            uniq.append((t, int(y)))
    return uniq


_LABSE = {}


def labse(texts):
    from sentence_transformers import SentenceTransformer
    if "m" not in _LABSE:
        _LABSE["m"] = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    return _LABSE["m"].encode(texts, batch_size=128, normalize_embeddings=True,
                              show_progress_bar=False).astype(np.float32)


def xbse_target(ckpt, texts, labels):
    import torch
    from xbse.encoder import BSEEncoder
    p = os.path.join(CKPT, ckpt)
    if not os.path.exists(p):
        return None
    try:
        sd = torch.load(p, map_location="cpu", weights_only=True)
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
        s = Z @ ax
        return (s < 0).astype(np.int64)
    except Exception as e:                                     # noqa: BLE001
        print(f"    xbse distill failed ({e}); direct labels", flush=True)
        return None


def main():
    import torch
    torch.set_num_threads(THREADS)
    os.makedirs(HERE, exist_ok=True)
    import faiss
    from sklearn.linear_model import LogisticRegression

    rng_seed = SPLIT_SEED
    out = {"prereg": "PREREG-CR-ANN-V2", "split_seed": SPLIT_SEED, "cap": CAP,
           "nfold": NFOLD, "units": {}}
    for uname, (axis, path, kind, ckpt) in UNITS.items():
        if not os.path.exists(path):
            print(f"[skip] {uname}: source missing {path}", flush=True)
            out["units"][uname] = {"status": "source_missing", "path": path}
            continue
        rows = load_unit(kind, path)
        if len(rows) < 400:
            print(f"[skip] {uname}: only {len(rows)} rows", flush=True)
            out["units"][uname] = {"status": "too_few", "n": len(rows)}
            continue
        rng = np.random.default_rng(rng_seed)
        order = rng.permutation(len(rows))
        rows = [rows[i] for i in order][:CAP]
        n_cal = int(CAL_FRAC * len(rows))
        cal, grade = rows[:n_cal], rows[n_cal:]
        man = {}
        for nm, part in (("calibration", cal), ("grading", grade)):
            fp = os.path.join(HERE, f"{uname}.{nm}.jsonl")
            with open(fp, "w", encoding="utf-8") as f:
                for t, y in part:
                    f.write(json.dumps({"text": t, "label": y}) + "\n")
            man[nm] = {"path": fp, "rows": len(part), "sha256": sha256(fp)}
        texts = [t for t, _ in cal]
        y = np.array([lab for _, lab in cal], dtype=np.int64)
        X = labse(texts)
        target = xbse_target(ckpt, texts, y) if ckpt else None
        distilled = target is not None
        if target is None:
            target = y
        # 5-fold cross-fit D (vs true labels) and A (L2-1NN)
        rngf = np.random.default_rng(SPLIT_SEED)
        folds = np.array_split(rngf.permutation(len(cal)), NFOLD)
        Ds, As = [], []
        for i in range(NFOLD):
            te = folds[i]
            tr = np.concatenate([folds[j] for j in range(NFOLD) if j != i])
            clf = LogisticRegression(max_iter=3000, C=10.0)
            clf.fit(X[tr], target[tr])
            Ds.append(float(clf.score(X[te], y[te])))
            idx = faiss.IndexFlatL2(X.shape[1])
            idx.add(X[tr])
            _, nn = idx.search(X[te], 1)
            As.append(float((y[tr][nn[:, 0]] == y[te]).mean()))
        D, A = float(np.mean(Ds)), float(np.mean(As))
        H = D - A
        arm = "misaligned" if (D >= 0.75 and H >= 0.04) else \
              ("matched" if abs(H) < 0.02 else "excluded")
        out["units"][uname] = {
            "status": "ok", "axis": axis, "distilled": distilled,
            "manifest": man, "n_calibration": len(cal),
            "violated_frac": float(y.mean()),
            "D_xfit": D, "D_xfit_sd": float(np.std(Ds)),
            "A_xfit": A, "H_xfit": H, "H_xfit_sd": float(np.std(np.array(Ds) - np.array(As))),
            "arm": arm}
        print(f"[qual] {uname} ({axis}): D={D:.3f}+-{np.std(Ds):.3f} A={A:.3f} "
              f"H={H:+.3f} distill={distilled} -> {arm}", flush=True)

    arms = [u["arm"] for u in out["units"].values() if u.get("status") == "ok"]
    out["MC3"] = {"misaligned": arms.count("misaligned"),
                  "matched": arms.count("matched"),
                  "sufficient": arms.count("misaligned") >= 2 and arms.count("matched") >= 1}
    with open(os.path.join(HERE, "qualification_v2.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"[MC3] {out['MC3']}", flush=True)
    print(f"wrote {HERE}/qualification_v2.json", flush=True)


if __name__ == "__main__":
    main()
