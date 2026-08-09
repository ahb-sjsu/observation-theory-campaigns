#!/usr/bin/env python3
"""Involutivity gate. Bars in experiments/PF-INVOLUTIVITY-DECLARATION.md.

V0 validates the instrument on two exact constructions with known answers.
V1 then asks whether the real consumer's kernel varies at all over the space it
lives in, because a constant kernel is trivially involutive and makes the whole
question vacuous.

An analytic pre-check, done before this was written and recorded in the run
output, says V1 will fail for softmax attention. C-3b's exact ground truth is
dp_i/dk_s = p_i(delta_is - p_s) q_i / sqrt(d), so

    P_C(k_s) = sum_i c_i q_i q_i^T ,   c_i = [p_i(delta_is - p_s)]^2 / d

The coefficients depend on the key but the SPAN does not, because the queries do
not depend on the key being perturbed, and softmax weights are strictly positive
so every c_i > 0. Hence ker P_C = span{q_i}^perp is CONSTANT over key space.

That is a theorem, not an artifact, and the numeric part of this run exists to
confirm it rather than to discover it. The declaration's premise, that C-11c's
measured drift makes the kernel a varying distribution, conflated two things:
drift over DECODE POSITION indexes a family of consumers, it is not motion over
the manifold the kernel is a distribution on. This run records that correction.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

SEED = 20260808
EPS = 1e-3
N_PAIRS = 24
N_BASE = 32
N_RAND = 5
V0_INVOL_BAR = 0.05
V0_CONTACT_BAR = 0.50
V1_VARY_BAR = 0.02


def proj_from_basis(B):
    """Orthogonal projector onto the column span of B."""
    Q, _ = np.linalg.qr(B)
    return Q @ Q.T


def tau_at(pi_of, x, rng, eps=EPS, n_pairs=N_PAIRS):
    """Non-involutivity statistic at x for a projector field pi_of(x).

    T(a,b) = (I - Pi)[ (d_{Pi a} Pi) b - (d_{Pi b} Pi) a ], maximised over pairs.
    """
    P = pi_of(x)
    d = P.shape[0]
    I = np.eye(d)
    out = 0.0
    for _ in range(n_pairs):
        a = rng.standard_normal(d)
        b = rng.standard_normal(d)
        u, v = P @ a, P @ b
        nu, nv = np.linalg.norm(u), np.linalg.norm(v)
        if nu < 1e-12 or nv < 1e-12:
            continue
        du = (pi_of(x + eps * u) - pi_of(x - eps * u)) / (2 * eps)
        dv = (pi_of(x + eps * v) - pi_of(x - eps * v)) / (2 * eps)
        br = du @ b - dv @ a
        out = max(out, float(np.linalg.norm((I - P) @ br) / (nu * nv)))
    return out


# ---- V0 control 1: a fixed subspace, trivially involutive ------------------
def make_fixed_kernel(d, m, rng):
    B = rng.standard_normal((d, m))
    P = proj_from_basis(B)
    return lambda x: P


# ---- V0 control 2: the contact distribution, the textbook non-involutive ---
def contact_pi(x):
    """span{ d/dx , d/dy + x d/dz } on R^3. Bracket is d/dz, outside the span."""
    e1 = np.array([1.0, 0.0, 0.0])
    e2 = np.array([0.0, 1.0, x[0]])
    return proj_from_basis(np.stack([e1, e2], axis=1))


# ---- the real consumer: softmax attention read operator over KEY space -----
def attention_pi_factory(q_set, d_head, rank_cut=1e-3):
    """ker P_C for perturbing one key, with the head's queries fixed.

    P_C(k) = sum_i c_i q_i q_i^T with c_i set by the softmax weights at k.
    Returns the projector onto the numerical kernel.
    """
    def pi_of(k):
        logits = (q_set @ k) / np.sqrt(d_head)
        p = np.exp(logits - logits.max())
        p /= p.sum()
        # c_i for the self term s: p_i(delta_is - p_s); take s as the argmax key
        c = (p * (1.0 - p)) ** 2 / d_head
        M = (q_set * c[:, None]).T @ q_set
        w, V = np.linalg.eigh(M)
        keep = w > rank_cut * max(w.max(), 1e-30)
        K = V[:, ~keep]                      # kernel basis
        return K @ K.T if K.shape[1] else np.zeros((d_head, d_head))
    return pi_of


def variation(pi_of, xs, delta, rng):
    """How much does the projector move over the sampled base points?"""
    vals = []
    for x in xs:
        step = rng.standard_normal(len(x))
        step *= delta / np.linalg.norm(step)
        vals.append(float(np.linalg.norm(pi_of(x + step) - pi_of(x), "fro")))
    return vals


def main() -> int:
    rng = np.random.default_rng(SEED)
    print("Involutivity gate")
    print("analytic pre-check predicts V1 FAILS for softmax attention:")
    print("  ker P_C = span{queries}^perp, and the queries do not depend on the")
    print("  key being perturbed, so the kernel is CONSTANT over key space.\n",
          flush=True)

    rec = {}

    # ---- V0
    d = 6
    fixed = make_fixed_kernel(d, 3, rng)
    t_fixed = max(tau_at(fixed, rng.standard_normal(d), rng) for _ in range(8))
    t_contact = max(tau_at(contact_pi, rng.standard_normal(3), rng) for _ in range(8))
    print(f"V0 fixed-subspace kernel   tau = {t_fixed:.4f}   (bar <= {V0_INVOL_BAR})")
    print(f"V0 contact distribution    tau = {t_contact:.4f}   (bar >= {V0_CONTACT_BAR})")
    v0 = bool(t_fixed <= V0_INVOL_BAR and t_contact >= V0_CONTACT_BAR)
    rec["V0"] = {"fixed_tau": t_fixed, "contact_tau": t_contact, "pass": v0}

    # ---- V1 on the real consumer shape
    d_head, n_q = 128, 24
    cells = []
    for cell in range(12):
        q_set = rng.standard_normal((n_q, d_head))
        pi_of = attention_pi_factory(q_set, d_head)
        base = [rng.standard_normal(d_head) for _ in range(N_BASE)]
        var = variation(pi_of, base, delta=1.0, rng=rng)
        ker_dim = int(round(np.trace(pi_of(base[0]))))
        taus = [tau_at(pi_of, x, rng, n_pairs=6) for x in base[:6]]
        cells.append({"cell": cell, "kernel_dim": ker_dim,
                      "proj_variation_median": float(np.median(var)),
                      "proj_variation_max": float(np.max(var)),
                      "tau_median": float(np.median(taus))})
        print(f"  cell {cell:2d}  ker dim {ker_dim:3d}/{d_head}  "
              f"||dPi||_F median {np.median(var):.3e}  tau median {np.median(taus):.3e}",
              flush=True)

    var_med = float(np.median([c["proj_variation_median"] for c in cells]))
    v1 = bool(var_med >= V1_VARY_BAR)
    print(f"\nV1 kernel variation median {var_med:.3e}  (bar >= {V1_VARY_BAR})")
    rec["V1"] = {"variation_median": var_med, "pass": v1, "cells": cells}

    verdict = ("VOID_KERNEL_CONSTANT" if not v1 else
               "PASS_PROCEED" if v0 else "VOID_INSTRUMENT_NOT_LIVE")
    if not v0:
        verdict = "VOID_INSTRUMENT_NOT_LIVE"

    record = {
        "schema": "involutivity-gate-v1",
        "declaration": "experiments/PF-INVOLUTIVITY-DECLARATION.md",
        "analytic_precheck": (
            "ker P_C = span{q_i}^perp for softmax attention; the queries do not "
            "depend on the perturbed key and softmax weights are strictly "
            "positive, so every c_i > 0 and the span, hence the kernel, is "
            "constant over key space. V1 is predicted to fail."),
        "declaration_correction": (
            "the declaration's premise conflated two variations. C-11c's drift "
            "is over DECODE POSITION, which indexes a family of consumers; it is "
            "not motion over the manifold the kernel is a distribution on, so it "
            "does not make the kernel distribution non-involutive."),
        "bars": {"V0_instrument_live": v0, "V1_kernel_varies_GATE": v1},
        "verdict": {"value": verdict, "computed_from": ["V0_instrument_live",
                                                        "V1_kernel_varies_GATE"]},
        "results": rec,
        "declared": {"seed": SEED, "eps": EPS, "n_pairs": N_PAIRS,
                     "n_base": N_BASE, "d_head": d_head, "n_queries": n_q,
                     "V0_invol_bar": V0_INVOL_BAR,
                     "V0_contact_bar": V0_CONTACT_BAR,
                     "V1_vary_bar": V1_VARY_BAR},
        "runtime": {"generated_utc": datetime.now(timezone.utc).isoformat(),
                    "python": sys.version, "numpy": np.__version__,
                    "platform": platform.platform(), "hostname": platform.node(),
                    "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" / "involutivity-gate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print("\n" + "=" * 62)
    print(f"  V0_instrument_live        {'PASS' if v0 else 'FAIL'}")
    print(f"  V1_kernel_varies_GATE     {'PASS' if v1 else 'FAIL'}")
    print("=" * 62)
    print("VERDICT", verdict)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
