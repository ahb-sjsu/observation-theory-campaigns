#!/usr/bin/env python3
"""Consumer-relative I-EIP — smallest cell (UNSEALED, exploratory).

The I-EIP Monitor (erisml-lib) grades internal equivariance h_l(g.x) ~ rho_l(g) h_l(x)
in the RAW L2 norm of the activation space. OT says layer l's activations have a
consumer -- the downstream network -- and the norm that matters is the consumer's read:
||e||_{P_C}, P_C = J^T J of the map from h_l to the model's output.

Claim under test: the consumer-weighted equivariance error predicts REAL behavioral
change (next-token KL between x and g.x) better than the raw L2 error, and at matched
flag rates the raw metric false-clears behavioral changes the consumer metric catches.

Substrate: Qwen2.5-0.5B (CPU), ~600 Social-Chem actions, g = backtranslation paraphrase
(MarianMT en->es->en). Probes: last-token hidden state at layers {6,12,18,24}.
rho_l: ridge Procrustes (the whitepaper's own estimator) on a calibration split.
Consumer map: ridge L: h_l -> R.logits (R = fixed JL projection of the vocab axis),
fit on calibration only; P_C = L^T L. Ground truth: KL(p_x || p_gx) at the last
position, full vocab. Eval on the held-out split. Isotropic control: P_C = I == raw.
"""
import csv
import json
import os
import numpy as np

HERE = os.path.expanduser("~/cr-ieip")
TSV = "/archive/ethics-corpora/social-chem-101/social-chem-101/social-chem-101.v1.0.tsv"
CACHE = os.path.join(HERE, "ieip_states.npz")
N_TEXT = 600
LAYERS = [6, 12, 18, 24]      # hidden_states index (24 = final for a 24-layer model)
PROJ_D = 256                  # JL projection of the vocab axis for the consumer map
RIDGE = 1e-2
SEED = 0
MODEL = "Qwen/Qwen2.5-0.5B"


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
            b = txts[s:s + 32]
            enc = tok(b, return_tensors="pt", padding=True, truncation=True, max_length=64)
            gen = mt.generate(**enc, max_length=80, num_beams=1)
            out.extend(tok.batch_decode(gen, skip_special_tokens=True))
        return out

    print("[ieip] backtranslating en->es...", flush=True)
    es = step(texts, "Helsinki-NLP/opus-mt-en-es")
    print("[ieip] backtranslating es->en...", flush=True)
    return step(es, "Helsinki-NLP/opus-mt-es-en")


def collect_states(texts, paras):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(16)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32)
    model.eval()

    H = {L: {"x": [], "g": []} for L in LAYERS}
    KL = []
    logits_x_all, logits_g_all = [], []
    rngR = np.random.default_rng(SEED)
    R = None

    with torch.no_grad():
        for i, (x, gx) in enumerate(zip(texts, paras)):
            outs = []
            for t in (x, gx):
                enc = tok(t, return_tensors="pt", truncation=True, max_length=48)
                o = model(**enc, output_hidden_states=True)
                hs = [o.hidden_states[L][0, -1, :].numpy().astype(np.float32)
                      for L in LAYERS]
                lg = o.logits[0, -1, :].numpy().astype(np.float64)
                outs.append((hs, lg))
            (hx, lx), (hg, lg) = outs
            for j, L in enumerate(LAYERS):
                H[L]["x"].append(hx[j])
                H[L]["g"].append(hg[j])
            # behavioral ground truth: KL(p_x || p_gx), full vocab, last position
            px = np.exp(lx - lx.max()); px /= px.sum()
            pg = np.exp(lg - lg.max()); pg /= pg.sum()
            KL.append(float(np.sum(px * (np.log(px + 1e-12) - np.log(pg + 1e-12)))))
            if R is None:
                R = rngR.standard_normal((PROJ_D, len(lx))).astype(np.float32) / np.sqrt(PROJ_D)
            logits_x_all.append(R @ lx.astype(np.float32))
            logits_g_all.append(R @ lg.astype(np.float32))
            if (i + 1) % 50 == 0:
                print(f"    forwards {i+1}/{len(texts)}", flush=True)

    data = {"KL": np.array(KL, dtype=np.float64),
            "Lx": np.stack(logits_x_all), "Lg": np.stack(logits_g_all)}
    for L in LAYERS:
        data[f"hx{L}"] = np.stack(H[L]["x"])
        data[f"hg{L}"] = np.stack(H[L]["g"])
    return data


def ridge_fit(X, Y, lam):
    """rows are samples: solve M (d_in->d_out): Y ~ X M^T."""
    d = X.shape[1]
    A = X.T @ X + lam * np.eye(d, dtype=np.float64)
    return np.linalg.solve(A, X.T @ Y).T          # (d_out, d_in)


def spearman(a, b):
    def rank(v):
        order = np.argsort(v)
        r = np.empty(len(v)); r[order] = np.arange(len(v))
        return r
    ra, rb = rank(np.asarray(a)), rank(np.asarray(b))
    ra -= ra.mean(); rb -= rb.mean()
    den = np.sqrt((ra**2).sum() * (rb**2).sum())
    return float((ra * rb).sum() / den) if den > 0 else float("nan")


def main():
    os.makedirs(HERE, exist_ok=True)
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        data = {k: z[k] for k in z.files}
        print(f"[ieip] cache hit {CACHE}", flush=True)
    else:
        texts = load_texts(N_TEXT)
        print(f"[ieip] {len(texts)} texts", flush=True)
        paras = backtranslate(texts)
        same = sum(1 for a, b in zip(texts, paras) if a.strip().lower() == b.strip().lower())
        print(f"[ieip] identical after backtranslation: {same}/{len(texts)}", flush=True)
        data = collect_states(texts, paras)
        np.savez(CACHE, **data)

    KL = data["KL"]
    n = len(KL)
    n_cal = int(0.6 * n)
    cal, ev = slice(0, n_cal), slice(n_cal, n)
    print(f"[ieip] n={n} (cal {n_cal} / eval {n - n_cal}); "
          f"KL median={np.median(KL):.3f} p90={np.quantile(KL, .9):.3f}", flush=True)

    changed = KL[ev] > np.quantile(KL[cal], 0.75)   # 'behavior changed' cut from cal
    results = {}
    print(f"\n{'layer':>5} {'rho_R2':>7} {'consR2':>7} | {'sp_raw':>7} {'sp_PC':>7} "
          f"{'sp_iso':>7} | {'fcRaw':>6} {'fcPC':>6}  (flag top-25%; fc = P(changed|not flagged... see note)")
    for L in LAYERS:
        hx, hg = data[f"hx{L}"].astype(np.float64), data[f"hg{L}"].astype(np.float64)
        # rho: whitepaper ridge Procrustes h_x -> h_gx, on calibration
        rho = ridge_fit(hx[cal], hg[cal], RIDGE * n_cal)
        pred = hx @ rho.T
        e = hg - pred                                   # equivariance residual
        ss_res = ((hg[cal] - pred[cal])**2).sum()
        ss_tot = ((hg[cal] - hg[cal].mean(0))**2).sum()
        rho_r2 = 1 - ss_res / ss_tot
        # consumer map: h_l -> projected logits, calibration only (both x and gx rows)
        Xc = np.vstack([hx[cal], hg[cal]])
        Yc = np.vstack([data["Lx"][cal], data["Lg"][cal]]).astype(np.float64)
        M = ridge_fit(Xc, Yc, RIDGE * len(Xc))          # (PROJ_D, d)
        ss_res = ((Yc - Xc @ M.T)**2).sum()
        ss_tot = ((Yc - Yc.mean(0))**2).sum()
        cons_r2 = 1 - ss_res / ss_tot
        # metrics on eval
        raw = np.linalg.norm(e[ev], axis=1)
        pc = np.linalg.norm(e[ev] @ M.T, axis=1)        # ||L e|| = ||e||_{P_C}
        sp_raw = spearman(raw, KL[ev])
        sp_pc = spearman(pc, KL[ev])
        sp_iso = spearman(raw, KL[ev])                  # P_C=I == raw by construction
        # matched flag rate: flag top 25% by each metric; false clear = behavior
        # changed but NOT flagged, as a fraction of changed cases
        thr_r = np.quantile(raw, 0.75); thr_p = np.quantile(pc, 0.75)
        fc_raw = float((changed & (raw <= thr_r)).sum() / max(changed.sum(), 1))
        fc_pc = float((changed & (pc <= thr_p)).sum() / max(changed.sum(), 1))
        results[str(L)] = {"rho_cal_R2": round(float(rho_r2), 4),
                           "consumer_cal_R2": round(float(cons_r2), 4),
                           "spearman_raw": round(sp_raw, 4),
                           "spearman_PC": round(sp_pc, 4),
                           "false_clear_raw": round(fc_raw, 4),
                           "false_clear_PC": round(fc_pc, 4)}
        print(f"{L:>5} {rho_r2:7.3f} {cons_r2:7.3f} | {sp_raw:7.3f} {sp_pc:7.3f} "
              f"{sp_iso:7.3f} | {fc_raw:6.3f} {fc_pc:6.3f}")

    print("\n--- READ ---")
    wins = sum(1 for L in LAYERS
               if results[str(L)]["spearman_PC"] > results[str(L)]["spearman_raw"] + 0.03)
    print(f"consumer metric beats raw (Spearman, margin .03) at {wins}/{len(LAYERS)} layers")
    fcw = sum(1 for L in LAYERS
              if results[str(L)]["false_clear_PC"] < results[str(L)]["false_clear_raw"] - 0.02)
    print(f"consumer metric false-clears less (margin .02) at {fcw}/{len(LAYERS)} layers")
    json.dump(results, open(os.path.join(HERE, "cr_ieip_result.json"), "w"), indent=2)
    print(f"wrote {HERE}/cr_ieip_result.json")


if __name__ == "__main__":
    main()
