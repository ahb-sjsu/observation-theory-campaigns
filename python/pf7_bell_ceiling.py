#!/usr/bin/env python3
"""PF-7a: the Bell ceiling. Bars declared in experiments/PF7-BELL-DECLARATION.md.

Question. PF-7 asks whether the model reproduces more than a classical
worldline picture. This run asks it against the one target with a theorem
behind it, entangled pair correlations.

Honest framing, recorded in the declaration and repeated here. The P0 null is
a THEOREM, not a discovery. With a setting independent source, strictly local
responses, and every emitted trial counted, the pointwise bound needs only
|A|,|B| <= 1, so S <= 2 for ANY source measure. The fold's particular hidden
measure therefore cannot change it. B1 is a code check. The bars that can fail
are B2 and B3, the SHAPE of the angular law, and B5, the blind consumer rate.

Arm semantics are taken unmodified from the audit harness
geometric-observation/experiments/bell_geometry_audit.py (GO-P-2026-057):
  P0 every premise intact, every trial counted, non detection an explicit 0
  P1 outcome accounting broken, post select on coincidence
  P2 measurement dependence, the source law depends on the settings
  P3 locality broken, Alice's response reads Bob's setting
Following that harness's documented wiring, P1's violation is read on the
POSTSELECTED score, because deleting non detections IS its premise break.

What is fold specific here, and not inherited from the audit:
  * signed count zero. PF-5's charge rule is charge = sign(dt/dtau), and a
    fold changes the unsigned branch count by exactly two and the signed count
    by exactly zero (Whitney genericity, PF-8). The pair's two branches are
    therefore exactly opposite in charge, which is what supplies B2.
  * per crossing transfer only, so events are independent, per PREREG-PF4-009.
  * the 1->3 zigzag. PF-8 records that a fold can make parent plus created
    pair, and that a consumer blind to one branch class reads such an event as
    a pair. That is the mechanism for B5, and it is the reason B5 is a fold
    result rather than a restatement of the detection loophole.

numpy only, CPU, deterministic.
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

# ---- declared constants, from PF7-BELL-DECLARATION.md ----------------------
SEED = 20260808
DIMS = (3, 8, 32, 128)
N_ORIENT = 60000
N_DRAW = 200000
N_ANG = 37
DETECTOR_SHARP = 3.0
ZIGZAG_FRACS = (0.0, 0.35)
B0_BAR = 2.0
B2_BAR = 0.99
B3_QUANTUM_BAR = 0.20
B3_SAWTOOTH_BAR = 0.05
B4_BAR = 0.01


# ---- fold source -----------------------------------------------------------
def fold_orientations(n, d, kappa, zipf_a, rng):
    """Worldline orientations at fold crossings, on S^(d-1).

    kappa concentrates the measure around a fold axis, which is what a field
    with a preferred direction produces. kappa = 0 is isotropic. The sweep over
    kappa exists to demonstrate that the P0 result does not depend on it, which
    is the theorem's content.
    """
    X = rng.standard_normal((n, d))
    if kappa > 0.0:
        axis = rng.standard_normal(d)
        axis /= np.linalg.norm(axis)
        X = X + kappa * axis[None, :]
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-12
    if zipf_a > 0:
        w = 1.0 / np.power(np.arange(1, n + 1), zipf_a)
        rng.shuffle(w)
        w /= w.sum()
    else:
        w = np.full(n, 1.0 / n)
    return X, w


def plane(d, rng):
    e1 = rng.standard_normal(d)
    e1 /= np.linalg.norm(e1)
    e2 = rng.standard_normal(d)
    e2 -= (e2 @ e1) * e1
    e2 /= np.linalg.norm(e2)
    return e1, e2


def dirn(e1, e2, t):
    return np.cos(t) * e1 + np.sin(t) * e2


def chsh(E):
    return abs(E[(0, 0)] + E[(0, 1)] + E[(1, 0)] - E[(1, 1)])


def eta_align(sharp):
    """Detection probability depends on lambda and the LOCAL setting only."""
    def f(L, q):
        return 1.0 / (1.0 + np.exp(-sharp * (L @ q)))
    return f


def outcomes(L, qa, qb, eta, rng, arm, qb_other=None, blind=None):
    """Local outcomes in {-1,0,+1}. 0 is explicit non detection, never deleted.

    Signed count zero gives B the opposite sign to A at matched settings, which
    is the fold's conservation signature and is inserted here and nowhere else.
    `blind` is a boolean mask of branches a declared blind consumer cannot see;
    it zeroes Bob's outcome for that class, which is the 1->3 zigzag loophole.
    """
    sa = L @ qa
    if arm == "P3" and qb_other is not None:
        sa = sa + 0.9 * (L @ qb_other)          # locality broken
    A = np.where(sa >= 0, 1.0, -1.0)
    B = np.where((L @ qb) >= 0, -1.0, 1.0)      # opposite charge
    if eta is not None:
        A = np.where(rng.random(len(L)) < eta(L, qa), A, 0.0)
        B = np.where(rng.random(len(L)) < eta(L, qb), B, 0.0)
    if blind is not None:
        B = np.where(blind, 0.0, B)
    return A, B


def run_arm(X, w, qA, qB, rng, n_draw, arm, sharp, zigzag=0.0):
    eta = None if sharp is None else eta_align(sharp)
    E_all, E_ps, marg, eff = {}, {}, {}, {}
    base = rng.choice(len(X), n_draw, p=w)
    # 1->3 zigzag: a declared fraction of events carry a third branch, and the
    # blind consumer cannot see it. Drawn once per trial, independent of the
    # settings, so it cannot itself break measurement independence.
    blind_base = rng.random(n_draw) < zigzag if zigzag > 0 else None
    for x in (0, 1):
        for y in (0, 1):
            if arm == "P2":
                tilt = w * np.exp(1.2 * (X @ qA[x]) * (X @ qB[y]))
                tilt /= tilt.sum()
                idx = rng.choice(len(X), n_draw, p=tilt)
            else:
                idx = base
            L = X[idx]
            A, B = outcomes(L, qA[x], qB[y], eta, rng, arm,
                            qb_other=qB[y] if arm == "P3" else None,
                            blind=blind_base)
            E_all[(x, y)] = float((A * B).mean())        # EVERY trial counted
            both = (A != 0) & (B != 0)
            eff[(x, y)] = float(both.mean())
            E_ps[(x, y)] = float((A[both] * B[both]).mean()) if both.sum() > 50 else 0.0
            marg[(x, y)] = (float(A.mean()), float(B.mean()))
    ns = max(max(abs(marg[(x, 0)][0] - marg[(x, 1)][0]) for x in (0, 1)),
             max(abs(marg[(0, y)][1] - marg[(1, y)][1]) for y in (0, 1)))
    return dict(arm=arm, S_all_counted=chsh(E_all), S_postselected=chsh(E_ps),
                no_signalling_residual=float(ns),
                eff_mean=float(np.mean(list(eff.values()))), zigzag=zigzag)


def angular_law(X, w, rng, d, n_draw, sharp):
    """E(theta) over ALL trials, against the local sawtooth and against -cos."""
    e1, e2 = plane(d, rng)
    eta = None if sharp is None else eta_align(sharp)
    L = X[rng.choice(len(X), n_draw, p=w)]
    qa = dirn(e1, e2, 0.0)
    ths = np.linspace(0.0, np.pi, N_ANG)
    E = np.array([float((lambda AB: (AB[0] * AB[1]).mean())(
        outcomes(L, qa, dirn(e1, e2, t), eta, rng, "P0"))) for t in ths])
    saw = -(1.0 - 2.0 * ths / np.pi)
    qm = -np.cos(ths)
    scale = float(np.dot(E, saw) / max(np.dot(saw, saw), 1e-12))
    return dict(
        thetas=ths.tolist(), E=E.tolist(),
        E_at_zero=float(E[0]),
        fitted_scale=scale,
        rms_vs_scaled_sawtooth=float(np.sqrt(np.mean((E - scale * saw) ** 2))),
        rms_vs_sawtooth=float(np.sqrt(np.mean((E - saw) ** 2))),
        mean_abs_vs_sawtooth=float(np.mean(np.abs(E - saw))),
        rms_vs_quantum=float(np.sqrt(np.mean((E - qm) ** 2))),
        max_gap_vs_quantum=float(np.abs(E - qm).max()),
        argmax_gap_theta=float(ths[int(np.abs(E - qm).argmax())]))


def main() -> int:
    rng = np.random.default_rng(SEED)
    tol = 4.0 / np.sqrt(N_DRAW)
    print(f"PF-7a Bell ceiling  seed={SEED} n_orient={N_ORIENT} n_draw={N_DRAW}")
    print("P0 null is a THEOREM here. B1 is a code check; B2/B3/B5 carry the run.\n",
          flush=True)

    grid = [dict(d=d, kappa=k, zipf_a=z)
            for d in DIMS for k in (0.0, 2.0) for z in (0.0, 1.5)]

    p0, ctrl, ang, blind = [], [], [], []
    for g in grid:
        X, w = fold_orientations(N_ORIENT, g["d"], g["kappa"], g["zipf_a"], rng)
        e1, e2 = plane(g["d"], rng)
        qA = {0: dirn(e1, e2, 0.0), 1: dirn(e1, e2, np.pi / 2)}
        qB = {0: dirn(e1, e2, np.pi / 4), 1: dirn(e1, e2, -np.pi / 4)}

        for sharp in (None, DETECTOR_SHARP):
            r = run_arm(X, w, qA, qB, rng, N_DRAW, "P0", sharp)
            r.update(g, sharp=(sharp or 0.0))
            p0.append(r)
        for arm in ("P1", "P2", "P3"):
            r = run_arm(X, w, qA, qB, rng, N_DRAW, arm,
                        DETECTOR_SHARP if arm == "P1" else None)
            r.update(g, sharp=DETECTOR_SHARP if arm == "P1" else 0.0)
            ctrl.append(r)
        for zz in ZIGZAG_FRACS:
            if zz == 0.0:
                continue
            r = run_arm(X, w, qA, qB, rng, N_DRAW, "P0", DETECTOR_SHARP, zigzag=zz)
            r.update(g, sharp=DETECTOR_SHARP)
            blind.append(r)
        ang.append(dict(**g, **angular_law(X, w, rng, g["d"], N_DRAW // 4, None)))
        print(f"  d={g['d']:3d} kappa={g['kappa']:.1f} zipf={g['zipf_a']:.1f} | "
              f"P0 S={[round(x['S_all_counted'], 4) for x in p0[-2:]]} | "
              f"P1ps={ctrl[-3]['S_postselected']:.3f} P2={ctrl[-2]['S_all_counted']:.3f} "
              f"P3={ctrl[-1]['S_all_counted']:.3f} | "
              f"E(0)={ang[-1]['E_at_zero']:+.4f} "
              f"maxgap_qm={ang[-1]['max_gap_vs_quantum']:.3f} "
              f"mad_saw={ang[-1]['mean_abs_vs_sawtooth']:.4f}", flush=True)

    s0 = np.array([r["S_all_counted"] for r in p0])
    ns0 = np.array([r["no_signalling_residual"] for r in p0])
    field = {"P1": "S_postselected", "P2": "S_all_counted", "P3": "S_all_counted"}
    byarm = {k: np.array([r[field[k]] for r in ctrl if r["arm"] == k])
             for k in ("P1", "P2", "P3")}
    e0 = np.array([a["E_at_zero"] for a in ang])
    gap_qm = np.array([a["max_gap_vs_quantum"] for a in ang])
    mad_saw = np.array([a["mean_abs_vs_sawtooth"] for a in ang])
    bs_all = np.array([r["S_all_counted"] for r in blind]) if blind else np.array([])
    bs_ps = np.array([r["S_postselected"] for r in blind]) if blind else np.array([])

    bars = {
        "B0_controls_fire": bool(all(byarm[k].min() > B0_BAR for k in ("P1", "P2", "P3"))),
        "B1_ceiling_code_check": bool(s0.max() <= 2.0 + 3.0 * tol),
        "B2_conservation_signature": bool(np.abs(e0).min() >= B2_BAR),
        "B3a_departs_from_quantum": bool(gap_qm.min() >= B3_QUANTUM_BAR),
        "B3b_follows_sawtooth": bool(mad_saw.max() <= B3_SAWTOOTH_BAR),
        "B4_no_signalling": bool(ns0.max() <= B4_BAR),
        "B5_blind_consumer_loophole": bool(
            bs_ps.size > 0 and bs_ps.max() > B0_BAR and bs_all.max() <= 2.0 + 3.0 * tol),
    }
    verdict = "PASS" if all(bars.values()) else "FAIL"
    if not bars["B0_controls_fire"]:
        verdict = "VOID_INSTRUMENT_NOT_LIVE"

    record = {
        "schema": "pf7a-bell-ceiling-v1",
        "declaration": "experiments/PF7-BELL-DECLARATION.md",
        "provenance": (
            "arm semantics vendored unmodified from geometric-observation/"
            "experiments/bell_geometry_audit.py (GO-P-2026-057); fold specific "
            "content is signed count zero, per crossing independence, and the "
            "PF-8 1->3 zigzag blind consumer"),
        "note_on_B1": (
            "the P0 null is a theorem for any source measure, so B1 is a code "
            "check and carries no evidence about folds; B2, B3 and B5 carry the run"),
        "p0": p0, "controls": ctrl, "blind_consumer": blind, "angular": ang,
        "summary": {
            "P0_S_max": float(s0.max()),
            "P0_no_signalling_max": float(ns0.max()),
            "control_S_min": {k: float(byarm[k].min()) for k in byarm},
            "E_at_zero_min_abs": float(np.abs(e0).min()),
            "max_gap_vs_quantum_min": float(gap_qm.min()),
            "mean_abs_vs_sawtooth_max": float(mad_saw.max()),
            "blind_S_all_counted_max": float(bs_all.max()) if bs_all.size else None,
            "blind_S_postselected_max": float(bs_ps.max()) if bs_ps.size else None,
            "finite_tolerance": float(tol),
        },
        "bars": bars,
        "verdict": {"value": verdict, "computed_from": sorted(bars)},
        "declared": {
            "seed": SEED, "dims": list(DIMS), "n_orient": N_ORIENT,
            "n_draw": N_DRAW, "n_ang": N_ANG, "detector_sharp": DETECTOR_SHARP,
            "zigzag_fracs": list(ZIGZAG_FRACS), "B0_bar": B0_BAR,
            "B2_bar": B2_BAR, "B3_quantum_bar": B3_QUANTUM_BAR,
            "B3_sawtooth_bar": B3_SAWTOOTH_BAR, "B4_bar": B4_BAR},
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "numpy": np.__version__,
            "platform": platform.platform(), "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" / "pf7a-bell-ceiling.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

    print("\n" + "=" * 68)
    for k, v in bars.items():
        print(f"  {k:34s} {'PASS' if v else 'FAIL'}")
    print("=" * 68)
    print("VERDICT", verdict)
    print(out)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
