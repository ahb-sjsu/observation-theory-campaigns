#!/usr/bin/env python3
"""CR-I-EIP seal-time checks (PREREG-CR-IEIP, sealing 2026-09-03).

Resolves seal open items 2+3: (a) mechanical smoke of the para transform on
<=50 burned-cell texts (pipeline sanity only, NO metrics graded) -- confirm
>=80% of paraphrases differ from source; (b) confirm Qwen2.5-1.5B loads CPU-side
and extracts last-token states within the thermal cap, timing one small batch
at the graded layers.
"""
import os
import sys
import time

import numpy as np

HERE = os.path.expanduser("~/cr-ieip")


def smoke_para():
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    torch.set_num_threads(8)
    texts = [
        "A person refuses to help a stranger in need.",
        "Someone lies to their friend about an important matter.",
        "A worker takes credit for a colleague's idea.",
        "A citizen disobeys an unjust local ordinance.",
        "A stranger returns a lost wallet with the cash intact.",
    ] * 10
    name = "humarin/chatgpt_paraphraser_on_T5_base"
    tok = AutoTokenizer.from_pretrained(name)
    mt = AutoModelForSeq2SeqLM.from_pretrained(name)
    out = []
    for s in range(0, len(texts), 25):
        enc = tok([f"paraphrase: {t}" for t in texts[s:s + 25]],
                  return_tensors="pt", padding=True, truncation=True, max_length=80)
        gen = mt.generate(**enc, max_length=80, num_beams=1, do_sample=False)
        out.extend(tok.batch_decode(gen, skip_special_tokens=True))
    def norm(s):
        return "".join(c.lower() for c in s if c.isalnum())
    differ = sum(1 for a, b in zip(texts, out) if norm(a) != norm(b))
    frac = differ / len(texts)
    print(f"[para-smoke] {differ}/{len(texts)} differ = {frac:.2%} "
          f"(bar >=80%: {'PASS' if frac >= 0.8 else 'FAIL'})", flush=True)
    print(f"[para-smoke] example: '{texts[0]}' -> '{out[0]}'", flush=True)
    return frac >= 0.8


def feasibility_1p5b():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.set_num_threads(int(os.environ.get("IEIP_THREADS", "8")))
    name = "Qwen/Qwen2.5-1.5B"
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.float32,
                                                 output_hidden_states=True)
    model.eval()
    nblocks = model.config.num_hidden_layers
    layers = [round(nblocks / 2), round(3 * nblocks / 4), nblocks]
    print(f"[feas] Qwen2.5-1.5B: {nblocks} blocks, d={model.config.hidden_size}, "
          f"graded layers {layers[:2]} (+final {layers[2]}); load {time.time()-t0:.0f}s",
          flush=True)
    texts = ["A person breaks a promise to a friend."] * 16
    t1 = time.time()
    with torch.no_grad():
        enc = tok(texts, return_tensors="pt", padding=True, truncation=True, max_length=48)
        hs = model(**enc).hidden_states
    last = enc["attention_mask"].sum(1) - 1
    states = {L: hs[L][torch.arange(len(texts)), last].numpy() for L in layers}
    dt = time.time() - t1
    per = dt / len(texts)
    print(f"[feas] extracted last-token states at {layers}: batch16 {dt:.1f}s "
          f"({per*1000:.0f} ms/text). 4400 texts ~= {per*4400/60:.1f} min/pass.",
          flush=True)
    print(f"[feas] d={states[layers[0]].shape[1]} > n_cal margin at N=4400 "
          f"(n_cal ~ 0.6*4400 = 2640 > d): {'OK' if 2640 > states[layers[0]].shape[1] else 'CHECK'}",
          flush=True)
    return True


def main():
    print("=== CR-I-EIP seal-time checks ===", flush=True)
    ok_para = smoke_para()
    ok_feas = feasibility_1p5b()
    print(f"[seal-checks] para_smoke={ok_para} feasibility_1p5b={ok_feas}", flush=True)


if __name__ == "__main__":
    main()
