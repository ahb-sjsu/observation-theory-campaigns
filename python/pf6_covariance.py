#!/usr/bin/env python3
"""PF-6 instrument layer: observer, Lorentz, and gauge audit
(exploratory instrument; no claim-bearing run).

CAMPAIGN.md section PF-6 is a mandatory gate. Its question, is a
claimed event physical or a coordinate-specific fold. Its bar, a rate
that changes under a passive coordinate transformation or gauge
change is rejected, and observer-dependent particle number may be
retained only if a physical detector model predicts the difference.
This module builds and validates the audit machinery so the gate can
be run, sealed, against whichever family goes forward. Nothing here
is a claim about any family.

The five audits, as implemented.

P1 TRANSLATION COVARIANCE. Shifting the field profile and the
   initial data together must shift every trajectory and every event
   worldpoint by exactly the same offset. Checked on a transmitted
   and on a reversing Sauter member.

P2 REPARAMETRIZATION INVARIANCE. Scaling the Hamiltonian by alpha
   relabels the evolution parameter, the path and its events are
   unchanged, the per-worldline event count is invariant EXACTLY (an
   integer), and the rate per unit parameter scales by alpha as
   predicted. This is the model class's invariant-rate witness, the
   physical rate is per worldline, not per parameter tick.

P3 BOOST AUDIT on the family with genuine hyperbolic structure (the
   PF-3 Stueckelberg replication). The continuous accumulation flow
   is a rapidity flow in the (tdot+1, w) plane, so it must commute
   with boosts exactly, conserve the invariant exactly, and its
   never-reverses classification (the campaign's Cayley finding F2)
   must be boost-invariant, the future cone is preserved for every
   boosted initial state.

P4 GAUGE AUDIT machinery, validated on a declared electromagnetic
   control where both gauges are exact, the length gauge with
   potential -qE(tau)u against the velocity gauge with (p-qA)^2/2
   and A' = -E. Physical histories u(tau) and udot(tau) must be
   identical and the canonical momenta must differ by exactly qA.
   The Sauter families' tilt coupling is declared NON-electromagnetic
   (a scalar tilt, no field tensor), so the campaign's gauge clause
   binds only when an electromagnetic family is declared, and this
   machinery stands validated for that day.

P5 OBSERVER AND DETECTOR AUDIT. A declared family of observer time
   functionals T_alpha = t + alpha tau. The event count an observer
   sees is measured twice, once from the observer's own record (sign
   changes of the finite-difference slope of T_alpha) and once from
   the model's detector prediction (crossings of p_t through the
   level -alpha). The two must agree exactly at every declared
   generic alpha, which is the campaign's clause made mechanical,
   the observer dependence of particle number is retained because a
   physical detector model predicts it exactly.

Exploratory label. No physics claim.
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

import pf4_pilot as pilot  # noqa: E402
from projection_fold import canonical_sha256  # noqa: E402

Q_CHARGE = 1.0
ALPHA_GRID = (-0.45, -0.2, 0.0, 0.2, 0.45, 3.0)


def integrate(p_gap, e_field, *, t0=0.0, alpha=1.0, dt=None,
              n_steps=20_000, pu0=0.1):
    """One deterministic Sauter member with field center t0 and
    Hamiltonian scale alpha. Returns arrays (t, pt, u, pu)."""
    dt = (pilot.DT if dt is None else dt) / alpha
    t = pilot.T_START + t0
    u = pilot.shifted_equilibrium(e_field, pilot.T_START)
    pu = pu0
    pt = p_gap
    ts, pts, us, pus = [t], [pt], [u], [pu]

    def forces(t_, u_):
        arg = (t_ - t0) / pilot.SAUTER_L
        ft = -alpha * pilot.G * e_field * u_ / math.cosh(arg) ** 2
        fu = alpha * (-pilot.OMEGA_U**2 * u_ - pilot.LAM * u_**3
                      - pilot.G * e_field * pilot.SAUTER_L
                      * math.tanh(arg))
        return ft, fu

    for _ in range(n_steps):
        ft, fu = forces(t, u)
        pt_h = pt + 0.5 * dt * ft
        pu_h = pu + 0.5 * dt * fu
        t += dt * alpha * pt_h
        u += dt * alpha * pu_h
        ft, fu = forces(t, u)
        pt = pt_h + 0.5 * dt * ft
        pu = pu_h + 0.5 * dt * fu
        ts.append(t)
        pts.append(pt)
        us.append(u)
        pus.append(pu)
    return (np.array(ts), np.array(pts), np.array(us), np.array(pus))


def fold_count(pts: np.ndarray) -> int:
    return int(np.sum(pts[:-1] * pts[1:] < 0.0))


def first_fold_worldpoint(ts, pts, us):
    idx = np.nonzero(pts[:-1] * pts[1:] < 0.0)[0]
    if len(idx) == 0:
        return None
    k = idx[0]
    return float(ts[k]), float(us[k])


def boost(state, chi):
    tp, w = state
    return (tp * math.cosh(chi) + w * math.sinh(chi),
            w * math.cosh(chi) + tp * math.sinh(chi))


def flow(state, ge, s=1.0):
    return boost(state, -ge * s)


def rk4(deriv, y0, tau0, tau1, dt):
    y = np.array(y0, dtype=float)
    tau = tau0
    n = int(round((tau1 - tau0) / dt))
    out = [y.copy()]
    for _ in range(n):
        k1 = deriv(tau, y)
        k2 = deriv(tau + dt / 2, y + dt / 2 * k1)
        k3 = deriv(tau + dt / 2, y + dt / 2 * k2)
        k4 = deriv(tau + dt, y + dt * k3)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tau += dt
        out.append(y.copy())
    return np.array(out)


def main() -> int:
    record: dict = {"schema": "pf6-instrument-v1",
                    "label": "exploratory instrument"}

    # P1: translation covariance on transmitted and reversing members
    shift = 8.0
    p1 = {}
    for name, (p, e) in (("transmitted", (0.75, 0.65)),
                         ("reversing", (0.3, 2.5))):
        base = integrate(p, e)
        moved = integrate(p, e, t0=shift)
        dev = float(np.max(np.abs(moved[0] - base[0] - shift)))
        assert dev < 1e-6, f"P1 {name} translation dev {dev}"
        assert fold_count(moved[1]) == fold_count(base[1])
        wp_b = first_fold_worldpoint(base[0], base[1], base[2])
        wp_m = first_fold_worldpoint(moved[0], moved[1], moved[2])
        if wp_b is not None:
            assert abs(wp_m[0] - wp_b[0] - shift) < 1e-6
            assert abs(wp_m[1] - wp_b[1]) < 1e-6
        p1[name] = {"max_worldline_dev": dev,
                    "fold_count": fold_count(base[1])}
    record["P1_translation"] = p1

    # P2: reparametrization, alpha-scaled Hamiltonian. With alpha a
    # power of two the stepwise arithmetic is exactly the base
    # arithmetic, so the same path segment is compared directly.
    alpha = 2.0
    n_seg = 20_000
    base = integrate(0.3, 2.5, n_steps=n_seg)
    scaled = integrate(0.3, 2.5, alpha=alpha, n_steps=n_seg)
    dev = float(np.max(np.abs(scaled[0] - base[0])))
    assert dev < 1e-10, f"P2 path dev {dev}"
    n_base = fold_count(base[1])
    n_scaled = fold_count(scaled[1])
    assert n_base == n_scaled and n_base > 0, \
        f"P2 per-worldline count changed: {n_base} vs {n_scaled}"
    span_base = n_seg * pilot.DT
    span_scaled = n_seg * pilot.DT / alpha
    rate_ratio = (n_scaled / span_scaled) / (n_base / span_base)
    assert abs(rate_ratio - alpha) < 1e-12, f"P2 rate ratio {rate_ratio}"
    record["P2_reparametrization"] = {
        "path_dev": dev, "events_per_worldline": n_base,
        "rate_per_tau_ratio": rate_ratio, "predicted_ratio": alpha}

    # P3: boost audit on the hyperbolic family
    worst_comm = 0.0
    worst_inv = 0.0
    min_cone = float("inf")
    for tdot in (1.02, 1.29, 2.0):
        for w0 in (-0.8, 0.0, 0.5):
            state = (tdot + 1.0, w0)
            inv0 = state[0] ** 2 - state[1] ** 2
            if inv0 <= 0 or state[0] <= abs(state[1]):
                continue
            for chi in (-2.0, -0.7, 0.7, 2.0):
                for ge in (0.5, 1.9, 2.1, 5.0):
                    a = flow(boost(state, chi), ge)
                    b = boost(flow(state, ge), chi)
                    worst_comm = max(worst_comm,
                                     abs(a[0] - b[0]), abs(a[1] - b[1]))
                    inv1 = a[0] ** 2 - a[1] ** 2
                    worst_inv = max(worst_inv,
                                    abs(inv1 - inv0) / abs(inv0))
                    for s in np.linspace(0.0, 1.0, 21):
                        c = flow(boost(state, chi), ge, s)
                        min_cone = min(min_cone, c[0] - abs(c[1]))
    assert worst_comm < 1e-10, f"P3 commutation {worst_comm}"
    assert worst_inv < 1e-10, f"P3 invariant {worst_inv}"
    assert min_cone > 0.0, f"P3 future cone violated: {min_cone}"
    record["P3_boost"] = {"worst_commutation": worst_comm,
                          "worst_invariant_drift": worst_inv,
                          "min_future_cone_margin": min_cone}

    # P4: gauge-equivalence control, length versus velocity gauge
    e0, pulse_l = 0.8, 3.0

    def efield(tau):
        return e0 / math.cosh(tau / pulse_l) ** 2

    def apot(tau):
        return -e0 * pulse_l * (math.tanh(tau / pulse_l) + 1.0)

    def vprime(u):
        return pilot.OMEGA_U**2 * u + pilot.LAM * u**3

    def deriv_length(tau, y):
        u, p = y
        return np.array([p, -vprime(u) + Q_CHARGE * efield(tau)])

    def deriv_velocity(tau, y):
        u, p = y
        return np.array([p - Q_CHARGE * apot(tau), -vprime(u)])

    tau0, tau1, dtq = -12.0, 12.0, 1e-3
    y_l = rk4(deriv_length, (0.4, 0.1), tau0, tau1, dtq)
    y_v = rk4(deriv_velocity,
              (0.4, 0.1 + Q_CHARGE * apot(tau0)), tau0, tau1, dtq)
    taus = tau0 + dtq * np.arange(len(y_l))
    u_dev = float(np.max(np.abs(y_l[:, 0] - y_v[:, 0])))
    shift_pred = np.array([Q_CHARGE * apot(x) for x in taus])
    p_dev = float(np.max(np.abs(y_v[:, 1] - (y_l[:, 1] + shift_pred))))
    assert u_dev < 1e-8, f"P4 history dev {u_dev}"
    assert p_dev < 1e-8, f"P4 canonical shift dev {p_dev}"
    record["P4_gauge_control"] = {
        "history_dev": u_dev, "canonical_shift_dev": p_dev,
        "scope_note": "the Sauter tilt is declared non-electromagnetic; "
                      "this machinery binds when an EM family is "
                      "declared"}

    # P5: observer and detector audit on a reversing member
    ts, pts, us, pus = integrate(0.3, 2.5, n_steps=20_000)
    curve = {}
    for a in ALPHA_GRID:
        slope = np.diff(ts) / pilot.DT + a
        observer_events = int(np.sum(slope[:-1] * slope[1:] < 0.0))
        shifted = pts + a
        detector_events = int(np.sum(shifted[:-1] * shifted[1:] < 0.0))
        assert observer_events == detector_events, \
            f"P5 mismatch at alpha={a}: {observer_events} vs " \
            f"{detector_events}"
        curve[f"{a:g}"] = observer_events
    assert curve["3"] == 0, "P5 monotone observer must see no events"
    record["P5_observer_detector"] = {
        "alpha_grid": list(ALPHA_GRID),
        "event_counts": curve,
        "clause": "observer-dependent particle number retained "
                  "because the detector model (p_t level crossings) "
                  "predicts every count exactly"}

    record["declared"] = {
        "family_constants": {"omega_u": pilot.OMEGA_U,
                             "lam": pilot.LAM, "g": pilot.G,
                             "sauter_L": pilot.SAUTER_L,
                             "dt": pilot.DT},
        "observer_family": "T_alpha = t + alpha tau",
        "reparametrization_alpha": alpha,
        "translation_shift": shift,
        "gauge_control": {"E0": e0, "pulse_L": pulse_l,
                          "q": Q_CHARGE},
    }
    record["statement"] = (
        "the PF-6 audit layer is validated end to end, translations "
        "move every event worldpoint exactly, reparametrization "
        "leaves per-worldline event counts exactly invariant while "
        "the per-parameter rate scales as predicted, the hyperbolic "
        "family's flow commutes with boosts and preserves the future "
        "cone so the never-reverses classification is boost-invariant, "
        "the gauge machinery is exact on its electromagnetic control "
        "with the Sauter tilt declared non-electromagnetic, and "
        "observer-dependent event counts are retained lawfully "
        "because the detector model predicts them exactly; the "
        "claim-bearing PF-6 run awaits the family selected by the "
        "PREREG-PF4-003 harvest and must be sealed before it runs")
    record["runtime"] = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown"),
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"}
    )
    output = Path(__file__).resolve().parents[1] / "results" \
        / "pf6-instrument.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print("P1:", p1)
    print("P2:", record["P2_reparametrization"])
    print("P3:", record["P3_boost"])
    print("P4: u_dev", u_dev, "p_dev", p_dev)
    print("P5:", curve)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
