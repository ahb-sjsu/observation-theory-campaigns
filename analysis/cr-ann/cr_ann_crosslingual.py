#!/usr/bin/env python3
"""Consumer-relative ANN — the CROSS-LINGUAL arm (UNSEALED, exploratory).

The most novel CR-ANN claim, and moral-spectrum-analyzer's "invariant under
translation" beat measured at the RETRIEVAL level: with LaBSE's 109-language
alignment, does the CONSUMER-RELATIVE neighborhood survive translation better
than the L2 neighborhood?

Setup: take Social-Chem actions with a moral-valence label (good/bad). Machine-
translate the DATABASE side to another language (es, fr) with MarianMT; keep the
labels identical (translation preserves valence). Embed queries (English) and the
translated database with LaBSE. Consumer P_C = W^T W is the English-trained valence
probe (the consumer does NOT change with the database language -- that is the point).

Cross-lingual retrieval: English query -> FAISS L2 candidates over the LANG database
-> rerank {L2 | OT} -> predict the query's valence from the reranked top-1
neighbour's label. Compared to the monolingual (en->en) baseline.

Predictions:
  (1) L2 cross-lingual valence-retrieval accuracy DROPS vs monolingual (translation
      shifts the geometry off the query).
  (2) OT rerank recovers more of the valence signal cross-lingually -- the gain
      (OT - L2) is >= the monolingual gain: the consumer-relative neighborhood is
      more translation-robust than the raw-L2 one.
  (3) Isotropic control P_C=I == L2 in every language.
"""
import csv
import os
import sys
import numpy as np

HERE = os.path.expanduser("~/cr-ann")
TSV = "/archive/ethics-corpora/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv"
CACHE = os.path.join(HERE, "crosslingual.npz")
N_PER_CLASS = 1500        # kept modest: MarianMT on CPU
K = 50
SEED = 0
LANGS = {"es": "Helsinki-NLP/opus-mt-en-es", "fr": "Helsinki-NLP/opus-mt-en-fr"}


def load_actions():
    rng = np.random.default_rng(SEED)
    seen, good, bad = set(), [], []
    with open(TSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            a = (r.get("action") or "").strip()
            j = (r.get("action-moral-judgment") or "").strip()
            if not a or not j or a in seen:
                continue
            try:
                jv = float(j)
            except ValueError:
                continue
            if jv == 0:
                continue
            seen.add(a)
            (good if jv > 0 else bad).append(a)
    rng.shuffle(good); rng.shuffle(bad)
    acts = good[:N_PER_CLASS] + bad[:N_PER_CLASS]
    y = np.array([1] * min(N_PER_CLASS, len(good)) + [0] * min(N_PER_CLASS, len(bad)),
                 dtype=np.int64)
    idx = rng.permutation(len(acts))
    return [acts[i] for i in idx], y[idx]


def translate(texts, model_name):
    from transformers import MarianMTModel, MarianTokenizer
    tok = MarianTokenizer.from_pretrained(model_name)
    mt = MarianMTModel.from_pretrained(model_name)
    out = []
    B = 32
    for s in range(0, len(texts), B):
        batch = texts[s:s + B]
        enc = tok(batch, return_tensors="pt", padding=True, truncation=True, max_length=64)
        gen = mt.generate(**enc, max_length=80, num_beams=1)
        out.extend(tok.batch_decode(gen, skip_special_tokens=True))
        if (s + B) % 320 == 0:
            print(f"    translated {s+B}/{len(texts)}", flush=True)
    return out


def build():
    import torch
    torch.set_num_threads(16)
    acts, y = load_actions()
    print(f"[xling] {len(acts)} actions ({int(y.sum())} good / {int((y==0).sum())} bad)",
          flush=True)
    from sentence_transformers import SentenceTransformer
    enc = SentenceTransformer("sentence-transformers/LaBSE", device="cpu")
    data = {"y": y}
    print("[xling] embedding EN...", flush=True)
    data["en"] = enc.encode(acts, batch_size=128, normalize_embeddings=True,
                            show_progress_bar=False).astype(np.float32)
    for lg, mn in LANGS.items():
        print(f"[xling] translating -> {lg} ({mn})...", flush=True)
        tr = translate(acts, mn)
        print(f"[xling] embedding {lg}...", flush=True)
        data[lg] = enc.encode(tr, batch_size=128, normalize_embeddings=True,
                              show_progress_bar=False).astype(np.float32)
    np.savez(CACHE, **data)
    return data


def retrieve(Xdb, ydb, Xq, yq, cand, PC):
    if PC is None:
        chosen = cand[:, 0]
    else:
        chosen = np.empty(len(Xq), dtype=np.int64)
        for i in range(len(Xq)):
            diff = Xdb[cand[i]] - Xq[i]
            score = np.einsum("kd,de,ke->k", diff, PC, diff)
            chosen[i] = cand[i][score.argmin()]
    return float((ydb[chosen] == yq).mean())


def main():
    import faiss
    from sklearn.linear_model import LogisticRegression
    os.makedirs(HERE, exist_ok=True)
    if os.path.exists(CACHE):
        z = np.load(CACHE); data = {k: z[k] for k in z.files}
        print(f"[xling] cache hit {CACHE}", flush=True)
    else:
        data = build()
    y = data["y"]
    n = len(y); n_tr = int(0.7 * n)
    tr, te = slice(0, n_tr), slice(n_tr, n)
    d = data["en"].shape[1]

    # consumer: English-trained valence probe (fixed across DB languages)
    clf = LogisticRegression(max_iter=3000, C=10.0)
    clf.fit(data["en"][tr], y[tr])
    W = clf.coef_.astype(np.float32)
    PC = (W.T @ W).astype(np.float32)
    print(f"[xling] EN valence probe test acc = {clf.score(data['en'][te], y[te]):.3f}; "
          f"P_C = W^T W {W.shape}\n")

    Xq = data["en"][te]           # queries are always English
    yq = y[te]
    print(f"{'DB lang':>8} {'L2 acc':>7} {'OT acc':>7} {'gain':>7} {'iso':>7}  note")
    results = {}
    for lg in ["en", "es", "fr"]:
        Xdb, ydb = data[lg][tr], y[tr]
        idx = faiss.IndexFlatL2(d); idx.add(Xdb)
        _, cand = idx.search(Xq, K)
        l2 = retrieve(Xdb, ydb, Xq, yq, cand, None)
        ot = retrieve(Xdb, ydb, Xq, yq, cand, PC)
        iso = retrieve(Xdb, ydb, Xq, yq, cand, np.eye(d, dtype=np.float32))
        results[lg] = {"l2": l2, "ot": ot, "gain": ot - l2, "iso": iso}
        note = "monolingual baseline" if lg == "en" else "CROSS-LINGUAL"
        print(f"{lg:>8} {l2:7.3f} {ot:7.3f} {ot-l2:+7.3f} {iso:7.3f}  {note}")

    print("\n--- READ ---")
    base_gain = results["en"]["gain"]
    for lg in ["es", "fr"]:
        xg = results[lg]["gain"]
        l2drop = results["en"]["l2"] - results[lg]["l2"]
        robust = xg >= base_gain - 0.01
        print(f"  {lg}: L2 dropped {l2drop:+.3f} vs monolingual; OT gain {xg:+.3f} "
              f"(monolingual {base_gain:+.3f}) -> consumer-relative nbhd "
              f"{'survives translation' if robust else 'degrades'}")
    import json
    json.dump(results, open(os.path.join(HERE, "cr_ann_crosslingual_result.json"), "w"),
              indent=2)
    print(f"\nwrote {HERE}/cr_ann_crosslingual_result.json")


if __name__ == "__main__":
    main()
