#!/usr/bin/env python3
"""Consumer-relative I-EIP — decisive cell v2 (UNSEALED, exploratory).

Fixes the three shakedown weaknesses:
  (1) n >> d: 2400 pairs, cal 1440 > d 896 -> rho well-determined; eval R^2 reported.
  (2) TRUE consumer metric, no linear proxy: inject the equivariance residual e at
      layer l (last-position activation patch) and measure the network's own output
      response KL(p(x) || p(x with e patched at l)) -- the consumer's actual read of
      the residual, per-input, nonlinear. Linear-proxy metric kept as a comparison arm.
  (3) identical backtranslations dropped before analysis.

Ground truth unchanged: the model's actual next-token KL between x and g.x.
Question: which monitor-computable metric best predicts real behavioral change --
raw ||e||_2 (I-EIP's), linear-proxy ||Le||, or the true consumer read c(e)?
Note: at the final layer c(e) is near-circular with the ground truth (patching
pre-head ~= recomputing the output); layers 6-18 are the informative ones.
"""
import csv
import json
import os
import numpy as np

HERE = os.path.expanduser("~/cr-ieip")
TSV = "/archive/ethics-corpora/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv"
CACHE = os.path.join(HERE, "ieip_v2_states.npz")
CONS_CACHE = os.path.join(HERE, "ieip_v2_consumer.npz")
N_TEXT = 2600            # before dedupe/identical filtering
LAYERS = [6, 12, 18, 24]
PROJ_D = 256
RIDGE = 1e-2
SEED = 0
MODEL = "Qwen/Qwen2.5-0.5B"
BATCH = 16
MAXLEN = 48


def load_texts(n):
    rng = np.random.default_rng(SEED)
    seen, out = set(), []
    with open(TSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            a = (r.get("action") or "").strip()
            if a and 20 <= len(a) <= 120 and a not in seen:
                seen.add(a)
                out.append(a)
    rng.shuffle(out)
    return out[:n]


def backtranslate(texts):
    import torch
    from transformers import MarianMTModel, MarianTokenizer
    torch.set_num_threads(16)

    def step(txts, name):
        tok = MarianTokenizer.from_pretrained(name)
        mt = MarianMTModel.from_pretrained(name)
        out = []
        for s in range(0, len(txts), 32):
            enc = tok(txts[s:s + 32], return_tensors="pt", padding=True,
                      truncation=True, max_length=64)
            gen = mt.generate(**enc, max_length=80, num_beams=1)
            out.extend(tok.batch_decode(gen, skip_special_tokens=True))
            if (s + 32) % 640 == 0:
                print(f"    bt {s+32}/{len(txts)} ({name.split('-')[-1]})", flush=True)
        return out

    es = step(texts, "Helsinki-NLP/opus-mt-en-es")
    return step(es, "Helsinki-NLP/opus-mt-es-en")


def get_model():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(16)
    tok = AutoTokenizer.from_pretrained(MODEL, padding_side="left")
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=None)
    model.eval()
    return tok, model


def base_forwards(tok, model, texts):
    """Batched (left-padded) forwards: last-position hidden states per layer + logits."""
    import torch
    H = {L: [] for L in LAYERS}
    LG = []
    with torch.no_grad():
        for s in range(0, len(texts), BATCH):
            enc = tok(texts[s:s + BATCH], return_tensors="pt", padding=True,
                      truncation=True, max_length=MAXLEN)
            o = model(**enc, output_hidden_states=True)
            for L in LAYERS:
                H[L].append(o.hidden_states[L][:, -1, :].float().numpy())
            LG.append(o.logits[:, -1, :].float().numpy())
            if (s + BATCH) % 320 == 0:
                print(f"    fwd {s+BATCH}/{len(texts)}", flush=True)
    return {L: np.concatenate(H[L]) for L in LAYERS}, np.concatenate(LG)


def patched_kl(tok, model, texts, layer, E):
    """For each text i, add E[i] to the LAST position's hidden state at `layer`
    (output of decoder block layer-1), rerun, return KL(p_base || p_patched).
    Left padding => last position is -1 for every row."""
    import torch
    block = model.model.layers[layer - 1]
    out_kl = np.empty(len(texts), dtype=np.float64)
    with torch.no_grad():
        for s in range(0, len(texts), BATCH):
            batch = texts[s:s + BATCH]
            enc = tok(batch, return_tensors="pt", padding=True,
                      truncation=True, max_length=MAXLEN)
            base = model(**enc).logits[:, -1, :].double()
            eb = torch.from_numpy(E[s:s + BATCH]).float()

            def hook(mod, inp, out):
                hs = out[0] if isinstance(out, tuple) else out
                hs = hs.clone()
                hs[:, -1, :] += eb
                return (hs,) + tuple(out[1:]) if isinstance(out, tuple) else hs

            h = block.register_forward_hook(hook)
            try:
                pat = model(**enc).logits[:, -1, :].double()
            finally:
                h.remove()
            pb = torch.softmax(base, dim=-1)
            lp = torch.log_softmax(pat, dim=-1)
            lb = torch.log_softmax(base, dim=-1)
            out_kl[s:s + BATCH] = (pb * (lb - lp)).sum(-1).numpy()
            if (s + BATCH) % 320 == 0:
                print(f"    patch L{layer} {s+BATCH}/{len(texts)}", flush=True)
    return out_kl


def ridge_fit(X, Y, lam):
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d, dtype=np.float64)
    return np.linalg.solve(A, X.T @ Y).T


def spearman(a, b):
    def rank(v):
        o = np.argsort(v)
        r = np.empty(len(v)); r[o] = np.arange(len(v))
        return r
    ra, rb = rank(np.asarray(a)), rank(np.asarray(b))
    ra -= ra.mean(); rb -= rb.mean()
    den = np.sqrt((ra**2).sum() * (rb**2).sum())
    return float((ra * rb).sum() / den) if den > 0 else float("nan")


def main():
    os.makedirs(HERE, exist_ok=True)
    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=True)
        data = {k: z[k] for k in z.files}
        print(f"[v2] cache hit {CACHE}", flush=True)
    else:
        texts = load_texts(N_TEXT)
        paras = backtranslate(texts)
        keep = [i for i, (a, b) in enumerate(zip(texts, paras))
                if a.strip().lower() != b.strip().lower()]
        texts = [texts[i] for i in keep]
        paras = [paras[i] for i in keep]
        print(f"[v2] kept {len(texts)} non-identical pairs", flush=True)
        tok, model = get_model()
        print("[v2] base forwards (x)...", flush=True)
        Hx, Lx = base_forwards(tok, model, texts)
        print("[v2] base forwards (g.x)...", flush=True)
        Hg, Lg = base_forwards(tok, model, paras)
        px = np.exp(Lx - Lx.max(1, keepdims=True)); px /= px.sum(1, keepdims=True)
        pg = np.exp(Lg - Lg.max(1, keepdims=True)); pg /= pg.sum(1, keepdims=True)
        KL = (px * (np.log(px + 1e-12) - np.log(pg + 1e-12))).sum(1)
        rngR = np.random.default_rng(SEED)
        R = rngR.standard_normal((PROJ_D, Lx.shape[1])).astype(np.float32) / np.sqrt(PROJ_D)
        data = {"KL": KL, "PLx": Lx @ R.T, "PLg": Lg @ R.T,
                "texts": np.array(texts, dtype=object)}
        for L in LAYERS:
            data[f"hx{L}"] = Hx[L]
            data[f"hg{L}"] = Hg[L]
        np.savez(CACHE, **data)

    KL = data["KL"].astype(np.float64)
    texts = list(data["texts"])
    n = len(KL); n_cal = int(0.6 * n)
    cal, ev = slice(0, n_cal), slice(n_cal, n)
    print(f"[v2] n={n} cal={n_cal} eval={n-n_cal}; KL median={np.median(KL):.3f}",
          flush=True)

    # rho + residuals per layer (rho now well-determined: n_cal > d)
    E_ev, rho_stats, proxy = {}, {}, {}
    for L in LAYERS:
        hx = data[f"hx{L}"].astype(np.float64)
        hg = data[f"hg{L}"].astype(np.float64)
        rho = ridge_fit(hx[cal], hg[cal], RIDGE * n_cal)
        pred = hx @ rho.T
        e = hg - pred
        def r2(sl):
            return 1 - ((hg[sl] - pred[sl])**2).sum() / ((hg[sl] - hg[sl].mean(0))**2).sum()
        rho_stats[L] = (float(r2(cal)), float(r2(ev)))
        E_ev[L] = e[ev].astype(np.float32)
        Xc = np.vstack([hx[cal], hg[cal]])
        Yc = np.vstack([data["PLx"][cal], data["PLg"][cal]]).astype(np.float64)
        M = ridge_fit(Xc, Yc, RIDGE * len(Xc))
        proxy[L] = np.linalg.norm(e[ev] @ M.T, axis=1)

    # true consumer read: patch e into layer L at x, measure output KL
    if os.path.exists(CONS_CACHE):
        zc = np.load(CONS_CACHE)
        cons = {L: zc[f"c{L}"] for L in LAYERS}
        print(f"[v2] consumer cache hit", flush=True)
    else:
        tok, model = get_model()
        ev_texts = texts[n_cal:]
        cons = {}
        for L in LAYERS:
            print(f"[v2] patched forwards, layer {L}...", flush=True)
            cons[L] = patched_kl(tok, model, ev_texts, L, E_ev[L])
        np.savez(CONS_CACHE, **{f"c{L}": v for L, v in cons.items()})

    changed = KL[ev] > np.quantile(KL[cal], 0.75)
    print(f"\n[v2] behavior-changed cases in eval: {int(changed.sum())}/{len(KL[ev])}")
    print(f"\n{'layer':>5} {'rhoR2c':>7} {'rhoR2e':>7} | {'sp_raw':>7} {'sp_prox':>8} "
          f"{'sp_true':>8} | {'fcRaw':>6} {'fcProx':>7} {'fcTrue':>7}")
    results = {}
    for L in LAYERS:
        raw = np.linalg.norm(E_ev[L], axis=1)
        tr = cons[L]
        sp_r, sp_p, sp_t = spearman(raw, KL[ev]), spearman(proxy[L], KL[ev]), spearman(tr, KL[ev])
        def fc(m):
            t = np.quantile(m, 0.75)
            return float((changed & (m <= t)).sum() / max(changed.sum(), 1))
        fr, fp, ft = fc(raw), fc(proxy[L]), fc(tr)
        r2c, r2e = rho_stats[L]
        results[str(L)] = {"rho_R2_cal": round(r2c, 4), "rho_R2_eval": round(r2e, 4),
                           "spearman": {"raw": round(sp_r, 4), "proxy": round(sp_p, 4),
                                        "true": round(sp_t, 4)},
                           "false_clear": {"raw": round(fr, 4), "proxy": round(fp, 4),
                                           "true": round(ft, 4)}}
        print(f"{L:>5} {r2c:7.3f} {r2e:7.3f} | {sp_r:7.3f} {sp_p:8.3f} {sp_t:8.3f} | "
              f"{fr:6.3f} {fp:7.3f} {ft:7.3f}")

    print("\n--- READ (layers 6-18 informative; 24 near-circular anchor) ---")
    for L in [6, 12, 18]:
        r = results[str(L)]
        win_sp = r["spearman"]["true"] > r["spearman"]["raw"] + 0.03
        win_fc = r["false_clear"]["true"] < r["false_clear"]["raw"] - 0.02
        print(f"  L{L}: true-consumer beats raw -- Spearman: {win_sp}  false-clear: {win_fc}")
    json.dump(results, open(os.path.join(HERE, "cr_ieip_v2_result.json"), "w"), indent=2)
    print(f"wrote {HERE}/cr_ieip_v2_result.json")


if __name__ == "__main__":
    main()
