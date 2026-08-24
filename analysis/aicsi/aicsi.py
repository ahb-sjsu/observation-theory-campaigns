"""XPROTO-AICSI experiment: the neural-CSI / turboquant bridge.

Thesis (turboquant-pro, in cellular form): a learned CSI-feedback codec
trained to minimize RECONSTRUCTION error (NMSE) can win the metric it was
trained on yet FALSE-CLEAR at the consumer -- the gNB precoder derived from
the reconstructed CSI, witnessed by HARQ -- because the consumer reads the
channel through a low-dim projection (its dominant eigen-direction), not the
Frobenius norm. A consumer/witness-aware codec (trained on the achieved
beamforming gain) holds. "Compress by the metric the consumer reads, not
reconstruction" -- the compression-domain twin of the KV-keys finding.

Setup: MIMO channels H (Nr x Nt) with angular structure (a dominant
singular direction). Two autoencoders share the architecture + bottleneck
(the feedback-bit proxy):
  nmse  : loss = ||H - Hhat||_F^2 / ||H||_F^2         (reconstruction)
  aware : loss = 1 - ||H w(Hhat)||^2 / ||H w(H)||^2   (consumer gain)
w(.) = top right singular vector (power iteration) = the MRT precoder. The
consumer's achieved SINR = operating_SINR + 10log10(gain fraction); HARQ
ACK/NACK / BLER from the real Sionna 5G NR LDPC curves (imported).

Run on Atlas GPU 1 (venv). Prints the NMSE-vs-false-clear paradox.
"""
import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import argparse
import json
import sys

import numpy as np
import tensorflow as tf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "csi"))
import csi_sionna as cs   # noqa: E402  (real Sionna 5G NR LDPC BLER curves)

HERE = os.path.dirname(os.path.abspath(__file__))

NR, NT = 2, 16              # UE / gNB antennas
NPATH = 4                   # angular clusters (competing singular directions)
B_LATENT = 9                # bottleneck dims (feedback-bit proxy)
N_TRAIN, N_TEST = 12000, 4000
STEPS, BATCH, LR = 3000, 1024, 1e-3
OPERATING_SINR_DB = 14.0    # SINR under PERFECT CSI (gain fraction = 1)
MCS_MARGIN_DB = 2.0
TARGET_BLER = 0.10
PI_ITERS = 6                # power-iteration steps for the top singular vector


def _steer(N, s):           # ULA steering, s = sin(angle)
    return np.exp(1j * np.pi * np.arange(N) * s) / np.sqrt(N)


def gen_channels(n, rng):
    H = np.zeros((n, NR, NT), np.complex64)
    for l in range(NPATH):
        c = (0.7 ** l) * (rng.standard_normal((n, 1, 1)) +
                          1j * rng.standard_normal((n, 1, 1))) / np.sqrt(2)
        sr = rng.uniform(-0.9, 0.9, (n, 1))
        st = rng.uniform(-0.9, 0.9, (n, 1))
        ar = np.exp(1j * np.pi * np.arange(NR)[None] * sr)[:, :, None] / np.sqrt(NR)
        at = np.exp(1j * np.pi * np.arange(NT)[None] * st)[:, None, :] / np.sqrt(NT)
        H += (c * ar * np.conj(at)).astype(np.complex64)
    H += (0.05 * (rng.standard_normal((n, NR, NT)) +
                  1j * rng.standard_normal((n, NR, NT))) / np.sqrt(2)).astype(np.complex64)
    # normalize to unit average power per entry
    p = np.mean(np.abs(H) ** 2, axis=(1, 2), keepdims=True)
    return (H / np.sqrt(p)).astype(np.complex64)


def to_real(H):
    return tf.concat([tf.math.real(H), tf.math.imag(H)],
                     axis=-1).numpy().reshape(H.shape[0], -1)


def to_complex(x):
    x = tf.reshape(x, [-1, 2, NR, NT])
    return tf.complex(x[:, 0], x[:, 1])


def top_rsv(Hc):
    """Top right singular vector via power iteration (differentiable)."""
    b = tf.shape(Hc)[0]
    v = tf.ones([b, NT, 1], tf.complex64) / tf.cast(tf.sqrt(float(NT)), tf.complex64)
    for _ in range(PI_ITERS):
        u = tf.matmul(Hc, v)                       # (b,Nr,1)
        v = tf.matmul(Hc, u, adjoint_a=True)       # (b,Nt,1)
        v = v / tf.cast(tf.norm(v, axis=1, keepdims=True) + 1e-9, tf.complex64)
    return v


def gain(Hc, v):
    return tf.reduce_sum(tf.abs(tf.matmul(Hc, v)) ** 2, axis=[1, 2])


def build():
    enc = tf.keras.Sequential([
        tf.keras.layers.Dense(256, "relu"), tf.keras.layers.Dense(128, "relu"),
        tf.keras.layers.Dense(B_LATENT)])
    dec = tf.keras.Sequential([
        tf.keras.layers.Dense(128, "relu"), tf.keras.layers.Dense(256, "relu"),
        tf.keras.layers.Dense(2 * NR * NT)])
    return enc, dec


def train(kind, Xtr_t, Htr_t, og_tr_t):
    enc, dec = build()
    opt = tf.keras.optimizers.Adam(LR)
    ntr = int(Xtr_t.shape[0])
    variables = enc.trainable_variables + dec.trainable_variables
    if not variables:                       # build weights so the list is populated
        enc(Xtr_t[:1]); dec(enc(Xtr_t[:1])); variables = enc.trainable_variables + dec.trainable_variables

    @tf.function
    def step(idx):
        xb = tf.gather(Xtr_t, idx)
        Hb = tf.gather(Htr_t, idx)
        og = tf.gather(og_tr_t, idx)
        with tf.GradientTape() as tape:
            h = enc(xb)
            z = h + tf.random.normal(tf.shape(h), stddev=0.05)   # rate proxy
            Hh = to_complex(dec(z))
            if kind == "nmse":
                loss = tf.reduce_mean(tf.reduce_sum(tf.abs(Hb - Hh) ** 2, [1, 2]) /
                                      (tf.reduce_sum(tf.abs(Hb) ** 2, [1, 2]) + 1e-9))
            else:
                ach = gain(Hb, top_rsv(Hh))
                # mean SINR deficit (nats) -- penalizes the low-gain tail that
                # drives false-clear, aligning the objective with the consumer
                loss = tf.reduce_mean(-tf.math.log(ach / (og + 1e-9) + 1e-6))
        g = tape.gradient(loss, tape.watched_variables())
        opt.apply_gradients(zip(g, tape.watched_variables()))
        return loss

    for _ in range(STEPS):
        step(tf.random.uniform([BATCH], 0, ntr, dtype=tf.int32))
    return enc, dec


def evaluate(enc, dec, Xte, Hte, opt_gain_te, curves, mcs):
    z = enc(tf.constant(Xte))
    Hh = to_complex(dec(z))
    nmse = float(tf.reduce_mean(tf.reduce_sum(tf.abs(Hte - Hh) ** 2, [1, 2]) /
                                (tf.reduce_sum(tf.abs(Hte) ** 2, [1, 2]) + 1e-9)))
    frac = (gain(Hte, top_rsv(Hh)) / (opt_gain_te + 1e-9)).numpy()
    frac = np.clip(frac, 1e-3, 1.0)
    sinr = OPERATING_SINR_DB + 10 * np.log10(frac)          # consumer-relative
    bler = np.array([cs.bler_at(curves, mcs, s) for s in sinr])
    return {"nmse": round(nmse, 4), "gain_frac": round(float(frac.mean()), 4),
            "false_clear": round(float(bler.mean()), 4)}


def run_cell(seed, curves, mcs):
    rng = np.random.default_rng(seed)
    Htr = tf.constant(gen_channels(N_TRAIN, rng))
    Hte = tf.constant(gen_channels(N_TEST, rng))
    Xtr, Xte = to_real(Htr), to_real(Hte)
    og_tr = gain(Htr, top_rsv(Htr))
    og_te = gain(Hte, top_rsv(Hte))
    tf.random.set_seed(seed)
    enc_n, dec_n = train("nmse", Xtr, Htr, og_tr)
    tf.random.set_seed(seed + 100)
    enc_a, dec_a = train("aware", Xtr, Htr, og_tr)
    r_n = evaluate(enc_n, dec_n, Xte, Hte, og_te, curves, mcs)
    r_a = evaluate(enc_a, dec_a, Xte, Hte, og_te, curves, mcs)
    # perfect-CSI control (gain fraction = 1)
    fc_perfect = round(float(cs.bler_at(curves, mcs, OPERATING_SINR_DB)), 4)
    return {
        "seed": int(seed), "mode": "nrsionna_aicsi",
        "nmse_recon_nmse": r_n["nmse"], "nmse_recon_aware": r_a["nmse"],
        "nmse_false_clear": r_n["false_clear"], "aware_false_clear": r_a["false_clear"],
        "nmse_gain_frac": r_n["gain_frac"], "aware_gain_frac": r_a["gain_frac"],
        "perfect_false_clear": fc_perfect, "mcs": int(mcs), "target_bler": TARGET_BLER,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--out", default=os.path.join(HERE, "AICSIREP-family.json"))
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
        print(f"seed {seed}: NMSE recon nmse={c['nmse_recon_nmse']} aware="
              f"{c['nmse_recon_aware']} | false-clear nmse={c['nmse_false_clear']} "
              f"aware={c['aware_false_clear']} perfect={c['perfect_false_clear']} "
              f"| gain_frac nmse={c['nmse_gain_frac']} aware={c['aware_gain_frac']}",
              flush=True)
    rec = {"family": "F-AICSI", "mode": "nrsionna_aicsi",
           "sim_is_code_validation_not_evidence": False,
           "constants": {"nr": NR, "nt": NT, "b_latent": B_LATENT, "npath": NPATH,
                         "operating_sinr_db": OPERATING_SINR_DB, "target_bler": TARGET_BLER,
                         "substrate": ("learned CSI autoencoders (recon-NMSE vs "
                                       "consumer-gain loss) + real Sionna 5G NR LDPC "
                                       "BLER curves; MRT precoder = top singular vector")},
           "cells": cells}
    json.dump(rec, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
