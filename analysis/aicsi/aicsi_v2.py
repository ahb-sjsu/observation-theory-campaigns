"""XPROTO-AICSI-V2: the neural-CSI reconstruction-vs-consumer dissociation on the
COMMUNITY-STANDARD substrate -- a CsiNet-class CONVOLUTIONAL autoencoder over real
3GPP CDL channels (Sionna 1.2), replacing the v1 synthetic-ULA + MLP-AE.

Thesis (unchanged): a learned CSI-feedback codec trained on RECONSTRUCTION NMSE wins
the metric it optimizes yet FALSE-CLEARS at the consumer -- the per-subcarrier MRT
precoder, witnessed by the real Sionna 5G NR LDPC decoder -- because the consumer reads
the channel through its dominant eigen-direction, not the Frobenius norm. A
consumer-aware codec (trained on achieved beam gain) holds.

Substrate upgrades over v1 (the WCNC rigor rungs):
  * channels: real 3GPP CDL-C (Sionna tr38901), Nr=2 x Nt=16 dual-pol, 32 subcarriers
  * codec: convolutional CsiNet-class AE (conv encoder + dense bottleneck + conv
    decoder w/ residual refine) on the (Nt x Nsub x 2Nr) CSI image
  * witness: the SAME real Sionna 5G NR LDPC BLER curves as XPROTO-CSI (csi_sionna)

Run on Atlas GPU 1 (sionna-venv). Prints the NMSE-vs-false-clear dissociation.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import argparse
import json
import sys

import numpy as np
import tensorflow as tf

for _g in tf.config.list_physical_devices("GPU"):   # avoid cuDNN 'No algorithm worked' (5003)
    try:
        tf.config.experimental.set_memory_growth(_g, True)
    except Exception:
        pass
# Conv2D hits a cuDNN execution failure on this GV100/TF build; the model is tiny, so we
# run on CPU. Cap threads (Atlas thermal discipline: <=20) to keep the Xeons cool.
tf.config.threading.set_intra_op_parallelism_threads(int(os.environ.get("TF_INTRA", "16")))
tf.config.threading.set_inter_op_parallelism_threads(2)

from sionna.phy.channel.tr38901 import CDL, AntennaArray
from sionna.phy.channel import subcarrier_frequencies, cir_to_ofdm_channel

sys.path.insert(0, os.path.expanduser("~/csi"))
import csi_sionna as cs   # noqa: E402  (real Sionna 5G NR LDPC BLER curves)

HERE = os.path.dirname(os.path.abspath(__file__))
NR, NT, NSUB = 2, 16, 32
FC, SCS, DS = 3.5e9, 30e3, 100e-9
B_LATENT = 32               # bottleneck (feedback-bit proxy); CR = 32/2048
N_TRAIN, N_TEST = 4000, 1500
STEPS, BATCH, LR = 1800, 256, 1e-3
OPERATING_SINR_DB = 14.0
MCS_MARGIN_DB = 2.0
TARGET_BLER = 0.10
PI_ITERS = 6
CHUNK = 500


def make_cdl(speed=1.0):
    ut = AntennaArray(num_rows=1, num_cols=1, polarization="dual", polarization_type="VH",
                      antenna_pattern="omni", carrier_frequency=FC)
    bs = AntennaArray(num_rows=1, num_cols=NT // 2, polarization="dual", polarization_type="VH",
                      antenna_pattern="38.901", carrier_frequency=FC)
    return CDL(model="C", delay_spread=DS, carrier_frequency=FC, ut_array=ut, bs_array=bs,
               direction="downlink", min_speed=speed, max_speed=speed)


def gen_channels(n, cdl, freqs):
    out, got = [], 0
    while got < n:
        b = min(CHUNK, n - got)
        a, tau = cdl(batch_size=b, num_time_steps=1, sampling_frequency=SCS * NSUB)
        h = cir_to_ofdm_channel(freqs, a, tau, normalize=True)
        out.append(tf.squeeze(h, axis=[1, 3, 5]).numpy().astype(np.complex64))  # (b,NR,NT,NSUB)
        got += b
    H = np.concatenate(out, 0)[:n]
    p = np.mean(np.abs(H) ** 2, axis=(1, 2, 3), keepdims=True)
    return (H / np.sqrt(p)).astype(np.complex64)


def to_img(H):   # (n,NR,NT,NSUB) complex -> (n,NT,NSUB,2NR) real  [re(NR), im(NR)]
    Ht = np.transpose(H, (0, 2, 3, 1))                      # (n,NT,NSUB,NR)
    return np.concatenate([Ht.real, Ht.imag], axis=-1).astype(np.float32)


def from_img(x):  # (n,NT,NSUB,2NR) -> (n,NR,NT,NSUB) complex
    x = tf.reshape(x, [-1, NT, NSUB, 2, NR])
    Hc = tf.complex(x[:, :, :, 0, :], x[:, :, :, 1, :])    # (n,NT,NSUB,NR)
    return tf.transpose(Hc, [0, 3, 1, 2])                  # (n,NR,NT,NSUB)


def build():
    enc = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu"),
        tf.keras.layers.Conv2D(8, 3, padding="same", activation="relu"),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(B_LATENT)])
    dec = tf.keras.Sequential([
        tf.keras.layers.Dense(NT * NSUB * 2 * NR, activation="relu"),
        tf.keras.layers.Reshape((NT, NSUB, 2 * NR)),
        tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu"),
        tf.keras.layers.Conv2D(8, 3, padding="same", activation="relu"),
        tf.keras.layers.Conv2D(2 * NR, 3, padding="same")])
    return enc, dec


def top_rsv(Hc):  # (...,NR,NT) -> (...,NT,1) via power iteration
    ntd = Hc.shape[-1]
    lead = tf.shape(Hc)[:-2]
    v = tf.ones(tf.concat([lead, [ntd, 1]], 0), tf.complex64) / tf.cast(tf.sqrt(float(ntd)), tf.complex64)
    for _ in range(PI_ITERS):
        u = tf.matmul(Hc, v)
        v = tf.matmul(Hc, u, adjoint_a=True)
        v = v / tf.cast(tf.norm(v, axis=-2, keepdims=True) + 1e-9, tf.complex64)
    return v


def gain(Hc, v):
    return tf.reduce_sum(tf.abs(tf.matmul(Hc, v)) ** 2, axis=[-2, -1])


def _persub(H):   # (n,NR,NT,NSUB) -> (n,NSUB,NR,NT)
    return tf.transpose(H, [0, 3, 1, 2])


def opt_gain(H):  # optimal per-sample mean beam gain over subcarriers
    Hs = _persub(H)
    return tf.reduce_mean(gain(Hs, top_rsv(Hs)), axis=1)


def train(kind, Xtr, Htr, og_tr):
    enc, dec = build()
    opt = tf.keras.optimizers.Adam(LR)
    ntr = int(Xtr.shape[0])
    enc(Xtr[:1]); dec(enc(Xtr[:1]))
    variables = enc.trainable_variables + dec.trainable_variables

    @tf.function
    def step(idx):
        xb = tf.gather(Xtr, idx); Hb = tf.gather(Htr, idx); ob = tf.gather(og_tr, idx)
        with tf.GradientTape() as tape:
            h = enc(xb)
            z = h + tf.random.normal(tf.shape(h), stddev=0.05)   # rate proxy
            Hh = from_img(dec(z))
            if kind == "nmse":
                num = tf.reduce_sum(tf.abs(Hb - Hh) ** 2, [1, 2, 3])
                den = tf.reduce_sum(tf.abs(Hb) ** 2, [1, 2, 3]) + 1e-9
                loss = tf.reduce_mean(num / den)
            else:
                ach = tf.reduce_mean(gain(_persub(Hb), top_rsv(_persub(Hh))), axis=1)
                loss = tf.reduce_mean(-tf.math.log(ach / (ob + 1e-9) + 1e-6))
        g = tape.gradient(loss, variables)
        opt.apply_gradients(zip(g, variables))
        return loss

    for _ in range(STEPS):
        step(tf.random.uniform([BATCH], 0, ntr, dtype=tf.int32))
    return enc, dec


def evaluate(enc, dec, Xte, Hte, og_te, curves, mcs):
    Hh = from_img(dec(enc(tf.constant(Xte))))
    nmse = float(tf.reduce_mean(tf.reduce_sum(tf.abs(Hte - Hh) ** 2, [1, 2, 3]) /
                                (tf.reduce_sum(tf.abs(Hte) ** 2, [1, 2, 3]) + 1e-9)))
    ach = tf.reduce_mean(gain(_persub(Hte), top_rsv(_persub(Hh))), axis=1)
    frac = np.clip((ach / (og_te + 1e-9)).numpy(), 1e-3, 1.0)
    sinr = OPERATING_SINR_DB + 10 * np.log10(frac)
    bler = np.array([cs.bler_at(curves, mcs, s) for s in sinr])
    return {"nmse": round(nmse, 4), "gain_frac": round(float(frac.mean()), 4),
            "false_clear": round(float(bler.mean()), 4)}


def run_cell(seed, curves, mcs):
    tf.random.set_seed(seed)
    cdl = make_cdl()
    freqs = subcarrier_frequencies(NSUB, SCS)
    print(f"  seed {seed}: generating CDL channels...", flush=True)
    Htr = tf.constant(gen_channels(N_TRAIN, cdl, freqs))
    Hte = tf.constant(gen_channels(N_TEST, cdl, freqs))
    Xtr, Xte = to_img(Htr.numpy()), to_img(Hte.numpy())
    og_tr, og_te = opt_gain(Htr), opt_gain(Hte)
    print(f"  seed {seed}: training nmse codec...", flush=True)
    tf.random.set_seed(seed); enc_n, dec_n = train("nmse", Xtr, Htr, og_tr)
    print(f"  seed {seed}: training aware codec...", flush=True)
    tf.random.set_seed(seed + 100); enc_a, dec_a = train("aware", Xtr, Htr, og_tr)
    r_n = evaluate(enc_n, dec_n, Xte, Hte, og_te, curves, mcs)
    r_a = evaluate(enc_a, dec_a, Xte, Hte, og_te, curves, mcs)
    fc_perfect = round(float(cs.bler_at(curves, mcs, OPERATING_SINR_DB)), 4)
    return {"seed": int(seed), "mode": "nrsionna_cdl_csinet",
            "nmse_recon_nmse": r_n["nmse"], "nmse_recon_aware": r_a["nmse"],
            "nmse_false_clear": r_n["false_clear"], "aware_false_clear": r_a["false_clear"],
            "nmse_gain_frac": r_n["gain_frac"], "aware_gain_frac": r_a["gain_frac"],
            "perfect_false_clear": fc_perfect, "mcs": int(mcs), "target_bler": TARGET_BLER,
            "channel": "3GPP-CDL-C", "arch": "csinet-conv-ae"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "AICSIV2REP-family.json"))
    args = ap.parse_args()
    print("loading real 5G NR LDPC BLER curves (Sionna)...", flush=True)
    curves = cs.measure_bler_curves()
    req = cs.required_snr(curves)
    cand = np.where(req <= OPERATING_SINR_DB - MCS_MARGIN_DB)[0]
    mcs = int(cand[-1]) if cand.size else 0
    cells = []
    for seed in args.seeds:
        c = run_cell(seed, curves, mcs)
        cells.append(c)
        print(f"seed {seed}: recon nmse={c['nmse_recon_nmse']} aware={c['nmse_recon_aware']} "
              f"| FC nmse={c['nmse_false_clear']} aware={c['aware_false_clear']} "
              f"perfect={c['perfect_false_clear']} | gain nmse={c['nmse_gain_frac']} "
              f"aware={c['aware_gain_frac']}", flush=True)
    rec = {"family": "F-AICSI-V2", "mode": "nrsionna_cdl_csinet",
           "constants": {"nr": NR, "nt": NT, "nsub": NSUB, "b_latent": B_LATENT,
                         "channel": "3GPP-CDL-C", "arch": "csinet-conv-ae",
                         "operating_sinr_db": OPERATING_SINR_DB, "target_bler": TARGET_BLER},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
