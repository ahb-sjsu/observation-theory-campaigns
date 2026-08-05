#!/usr/bin/env python3
"""PE-4 noise and inaccessible hidden state (exploratory, PE track).

The PE-2 reversible cycle, now coupled to an environment. The toy
system (t, p_t, u, p_u) couples through u to a 32-mode thermal bath
with spread frequencies at strength kappa. The whole evolution stays
Hamiltonian and time-symmetric, so nothing is irreversible in the full
space at any kappa. The observer, however, can flip only the system
momenta, not the bath's. The protocol per kappa is one forward leg,
then two return legs from the same stored state, a system-only flip
(what the observer can do) and a full flip including the bath (the
control). Witnesses are the hidden-state recovery defect and the
observed-entropy retrace defect for each flip, the energy transferred
to the bath, and the plugin mutual information between the binned
observed coordinate and the binned bath energy.

Expected and asserted: at kappa 0 the system-only flip reproduces the
PE-2 result (recovery and retrace at machine precision, mutual
information at the estimator floor). As kappa grows the system-only
recovery defect rises monotonically and the entropy curve stops
retracing, while the full flip recovers exactly at EVERY kappa. The
irreversibility is therefore bookkeeping about which degrees of
freedom the observer can reach, not a property of the dynamics.
Entropy production appears exactly when projection ambiguity leaks
into an environment the consumer cannot flip. This is the only PE
experiment entitled to thermodynamic language, and the language it
earns is consumer-relative.

Exploratory label.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

OMEGA_T = 1.0
OMEGA_U = 1.2
LAM = 0.1
G_COUP = 0.25
E_FIELD = 1.0
T_BATH = 1.0
N_MODES = 32
W_LO, W_HI = 0.5, 2.5
DT = 1e-3
TAU_FWD = 20.0
N_ENS = 8_000
SEED = 20260806
EPS = 0.05
MI_BINS = 12
KAPPAS = (0.0, 0.05, 0.1, 0.2, 0.4)

W_MODES = np.linspace(W_LO, W_HI, N_MODES)


def entropy_bits(t: np.ndarray) -> float:
    # the half-bin offset keeps the degenerate initial ensemble
    # (t identically zero) off a bin edge, where round-trip 1e-16
    # noise would split one bin into two and fake a retrace defect
    centered = t - t.mean()
    counts = np.bincount(
        np.clip(((centered + 8.0 + EPS / 2) / EPS).astype(int), 0,
                int(16.0 / EPS)))
    p = counts[counts > 0] / len(t)
    return float(-(p * np.log2(p)).sum())


def forces(state, c):
    t, pt, u, pu, e, pe = state
    ft = -OMEGA_T**2 * t - G_COUP * E_FIELD * u
    fu = (-OMEGA_U**2 * u - LAM * u**3 - G_COUP * E_FIELD * t
          - e @ c)
    fe = -W_MODES**2 * e - c * u[:, None]
    return ft, fu, fe


def evolve(state, c, record=False):
    t, pt, u, pu, e, pe = (a.copy() for a in state)
    curve = []
    steps = int(round(TAU_FWD / DT))
    for k in range(steps):
        if record and k % 40 == 0:
            curve.append(entropy_bits(t))
        ft, fu, fe = forces((t, pt, u, pu, e, pe), c)
        pt = pt + 0.5 * DT * ft
        pu = pu + 0.5 * DT * fu
        pe = pe + 0.5 * DT * fe
        t = t + DT * pt
        u = u + DT * pu
        e = e + DT * pe
        ft, fu, fe = forces((t, pt, u, pu, e, pe), c)
        pt = pt + 0.5 * DT * ft
        pu = pu + 0.5 * DT * fu
        pe = pe + 0.5 * DT * fe
    if record:
        curve.append(entropy_bits(t))
    return (t, pt, u, pu, e, pe), curve


def bath_energy(state) -> np.ndarray:
    _, _, _, _, e, pe = state
    return 0.5 * (pe**2 + (W_MODES**2) * e**2).sum(axis=1)


def mutual_information_bits(x: np.ndarray, y: np.ndarray) -> float:
    def digitize(v):
        edges = np.linspace(v.min(), v.max() + 1e-12, MI_BINS + 1)
        return np.clip(np.digitize(v, edges) - 1, 0, MI_BINS - 1)
    joint = np.zeros((MI_BINS, MI_BINS))
    np.add.at(joint, (digitize(x), digitize(y)), 1.0)
    joint /= joint.sum()
    px = joint.sum(axis=1, keepdims=True)
    py = joint.sum(axis=0, keepdims=True)
    mask = joint > 0
    return float((joint[mask]
                  * np.log2(joint[mask] / (px @ py)[mask])).sum())


def recovery_defect(final, initial) -> float:
    # after the closing flip the round trip should reproduce the
    # initial system state exactly
    t, pt, u, pu, _, _ = final
    t0, pt0, u0, pu0, _, _ = initial
    return float(math.sqrt(np.mean(
        (t - t0)**2 + (pt - pt0)**2 + (u - u0)**2 + (pu - pu0)**2)))


def flip(state, include_bath: bool):
    t, pt, u, pu, e, pe = (a.copy() for a in state)
    pt, pu = -pt, -pu
    if include_bath:
        pe = -pe
    return t, pt, u, pu, e, pe


def main() -> int:
    rng = np.random.RandomState(SEED)
    t0 = np.zeros(N_ENS)
    pt0 = np.ones(N_ENS)
    u0 = rng.standard_normal(N_ENS) * math.sqrt(T_BATH) / OMEGA_U
    pu0 = rng.standard_normal(N_ENS) * math.sqrt(T_BATH)
    e0 = (rng.standard_normal((N_ENS, N_MODES))
          * math.sqrt(T_BATH) / W_MODES)
    pe0 = rng.standard_normal((N_ENS, N_MODES)) * math.sqrt(T_BATH)
    initial = (t0, pt0, u0, pu0, e0, pe0)
    e_bath0 = float(bath_energy(initial).mean())

    per_kappa = {}
    for kappa in KAPPAS:
        c = kappa / math.sqrt(N_MODES) * np.ones(N_MODES)
        turned, fwd_curve = evolve(initial, c, record=True)

        back_sys, ret_curve = evolve(flip(turned, False), c, record=True)
        closed_sys = flip(back_sys, False)
        back_full, _ = evolve(flip(turned, True), c)
        closed_full = flip(back_full, True)

        retrace = float(np.max(np.abs(
            np.array(fwd_curve) - np.array(ret_curve)[::-1])))
        mi = mutual_information_bits(turned[0], bath_energy(turned))
        entry = {
            "kappa": kappa,
            "recovery_defect_system_flip": recovery_defect(
                closed_sys, initial),
            "recovery_defect_full_flip": recovery_defect(
                closed_full, initial),
            "entropy_retrace_defect_bits": retrace,
            "bath_energy_gain": float(bath_energy(turned).mean())
                - e_bath0,
            "mutual_information_Z_Ebath_bits": mi,
            "forward_entropy_first_last_bits": [fwd_curve[0],
                                                fwd_curve[-1]],
        }
        per_kappa[f"{kappa:g}"] = entry
        print(f"kappa {kappa:g}: sys-flip defect "
              f"{entry['recovery_defect_system_flip']:.3e}, full-flip "
              f"{entry['recovery_defect_full_flip']:.3e}, retrace "
              f"{retrace:.3e} bits, dE_bath "
              f"{entry['bath_energy_gain']:.4f}, MI {mi:.4f} bits",
              flush=True)

    defects = [per_kappa[f"{k:g}"]["recovery_defect_system_flip"]
               for k in KAPPAS]
    base = per_kappa["0"]
    assert base["recovery_defect_system_flip"] < 1e-9, \
        "kappa 0 must reproduce PE-2 reversibility"
    assert base["entropy_retrace_defect_bits"] < 1e-9, \
        "kappa 0 entropy curve must retrace"
    assert base["mutual_information_Z_Ebath_bits"] < 0.05, \
        "kappa 0 mutual information should sit at the estimator floor"
    assert all(b > a for a, b in zip(defects, defects[1:])), \
        "system-flip recovery defect must rise monotonically with kappa"
    top = per_kappa[f"{KAPPAS[-1]:g}"]
    assert top["recovery_defect_system_flip"] > 0.01, \
        "strong coupling must produce a macroscopic recovery failure"
    assert top["entropy_retrace_defect_bits"] > 0.05, \
        "strong coupling must break the entropy retrace"
    assert top["mutual_information_Z_Ebath_bits"] > \
        base["mutual_information_Z_Ebath_bits"] + 0.1, \
        "leaked information must show up in I(Z; E_bath)"
    for k in KAPPAS:
        assert per_kappa[f"{k:g}"]["recovery_defect_full_flip"] < 1e-9, \
            f"full flip must recover exactly at kappa {k:g}"

    record = {
        "schema": "pe4-noise-v1",
        "label": "exploratory",
        "declared": {"omega_t": OMEGA_T, "omega_u": OMEGA_U, "lam": LAM,
                     "g": G_COUP, "E": E_FIELD, "T": T_BATH,
                     "n_modes": N_MODES, "mode_band": [W_LO, W_HI],
                     "dt": DT, "tau_forward": TAU_FWD, "n": N_ENS,
                     "seed": SEED, "eps": EPS, "mi_bins": MI_BINS,
                     "kappas": list(KAPPAS),
                     "coupling": "kappa/sqrt(n_modes) * u * e_j, "
                                 "no counter-term"},
        "per_kappa": per_kappa,
        "statement": "irreversibility here is bookkeeping about reach, "
            "not dynamics: the system-only flip fails monotonically in "
            "kappa while the full flip recovers exactly at every "
            "kappa, and the failure is witnessed by energy and mutual "
            "information deposited in the bath, so entropy production "
            "is projection ambiguity leaked into an environment the "
            "consumer cannot flip",
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
        },
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "pe4-noise.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
