#!/usr/bin/env python3
"""PF-5 instrument layer: conservation and complete accounting
(exploratory instrument; no claim-bearing run).

CAMPAIGN.md section PF-5 is a mandatory gate. Its question, is an
apparent pair event compatible with conservation rather than a
branch-counting illusion. This module builds and validates the
instrument layer so the gate can be run, sealed, against whichever
family goes forward after the PREREG-PF4-003 harvest. Nothing here
is a claim about any family.

The four requirements, as implemented.

1. COMPLETE CENSUS. Every trajectory ends in exactly one declared
   class, reversing (first p_t zero crossing), transmitted (exits
   the slab forward), capped (still in flight at the step cap), or
   nonfinite (numerical failure). Classification priority is
   declared, nonfinite first, then reversing, then transmitted,
   then capped. The census must sum exactly to the ensemble size,
   so the missing-trajectory count is identically zero, and no
   downstream statistic may silently drop a class. The instrument
   returns fractions only against explicitly declared denominators
   and always reports the census-complete value alongside.

2. CONTINUOUS CONSERVATION. The Stueckelberg Hamiltonian has no
   explicit evolution-parameter dependence, so H is conserved along
   every trajectory. The instrument tracks the maximum relative
   energy residual continuously (every audit stride) for every
   member, including the failed ones up to their failure step.

3. DECLARED CHARGE ASSIGNMENT. The orientation charge of a branch
   is the sign of dt/dtau, assigned before any run. The lawful
   statement is the path-degree rule, the signed crossing count of
   any generic observed level equals the endpoint bookkeeping
   [t_end > level] - [t_start > level], which is exactly the
   statement that folds create charge in cancelling pairs. The
   instrument checks the rule per member per level, exactly, using
   the sealed polyline instrument.

4. FIELD-ENERGY MATCHING is declared out of scope for external-field
   families, where the tilt is a fixed background. The campaign
   clause applies to dynamical-field models only, and the record
   says so rather than silently skipping it.

Validation controls, all exact, run before any application.

C1 harmonic conservation control, drift bar measured and frozen.
C2 census controls, a field-free cell must classify one hundred
   percent transmitted, and a deterministically reversing cell one
   hundred percent reversing.
C3 failure control, an absurd step size must produce nonfinite or
   capped members that are counted, with the census still summing
   exactly, proving failures are counted rather than dropped.
C4 charge control, the analytic double fold checked against the
   sealed polyline instrument, signed count equal to the endpoint
   rule at every generic level.
C5 deletion trap, a statistic computed with and without a deleted
   class must be flagged as discrepant by the instrument whenever
   the deleted class is populated.

The module then runs a smoke application on one Sauter cell of the
PF-4 family (constants imported from the committed pilot) to
demonstrate the full witness record end to end, at exploratory
label, with no claim attached.
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
from projection_fold import (  # noqa: E402
    canonical_sha256,
    polyline_level_crossings,
)

AUDIT_STRIDE = 25
MAX_STEPS = 60_000
CLASSES = ("nonfinite", "reversing", "transmitted", "capped")


def hamiltonian(t, pt, u, pu, e_field):
    return (0.5 * pt**2 + 0.5 * pu**2
            + 0.5 * pilot.OMEGA_U**2 * u**2 + 0.25 * pilot.LAM * u**4
            + pilot.G * e_field * pilot.SAUTER_L
            * np.tanh(t / pilot.SAUTER_L) * u)


def census_run(p_gap, e_field, n, seed, *, dt=None, max_steps=MAX_STEPS,
               keep_polyline=()):
    """Integrate an ensemble across the Sauter slab with complete
    accounting. Returns the census, the continuous energy residuals,
    and optional full polylines for declared members."""
    dt = pilot.DT if dt is None else dt
    rng = np.random.RandomState(seed)
    t = np.full(n, pilot.T_START)
    u_star = pilot.shifted_equilibrium(e_field, pilot.T_START)
    u = u_star + rng.standard_normal(n) * math.sqrt(pilot.T_BATH) \
        / pilot.OMEGA_U
    pu = rng.standard_normal(n) * math.sqrt(pilot.T_BATH)
    pt = np.full(n, p_gap)

    h0 = hamiltonian(t, pt, u, pu, e_field)
    scale = np.maximum(np.abs(h0), 1.0)
    max_resid = np.zeros(n)
    cls = np.full(n, -1, dtype=np.int64)  # index into CLASSES
    alive = np.ones(n, dtype=bool)
    t_exit = -pilot.T_START
    polylines = {k: {"t": [float(t[k])], "pt": [float(pt[k])]}
                 for k in keep_polyline}

    def force_t(t_, u_):
        sech2 = 1.0 / np.cosh(t_ / pilot.SAUTER_L) ** 2
        return -pilot.G * e_field * sech2 * u_

    def force_u(t_, u_):
        return (-pilot.OMEGA_U**2 * u_ - pilot.LAM * u_**3
                - pilot.G * e_field * pilot.SAUTER_L
                * np.tanh(t_ / pilot.SAUTER_L))

    step = 0
    err = np.errstate(all="ignore")
    err.__enter__()
    while np.any(alive) and step < max_steps:
        ft = force_t(t, u)
        fu = force_u(t, u)
        pt_h = np.where(alive, pt + 0.5 * dt * ft, pt)
        pu_h = np.where(alive, pu + 0.5 * dt * fu, pu)
        t = np.where(alive, t + dt * pt_h, t)
        u = np.where(alive, u + dt * pu_h, u)
        ft = force_t(t, u)
        fu = force_u(t, u)
        pt = np.where(alive, pt_h + 0.5 * dt * ft, pt)
        pu = np.where(alive, pu_h + 0.5 * dt * fu, pu)
        step += 1

        for k in keep_polyline:
            if alive[k]:
                polylines[k]["t"].append(float(t[k]))
                polylines[k]["pt"].append(float(pt[k]))

        bad = alive & ~(np.isfinite(t) & np.isfinite(pt)
                        & np.isfinite(u) & np.isfinite(pu))
        cls[bad] = CLASSES.index("nonfinite")
        alive &= ~bad
        rev = alive & (pt <= 0.0)
        cls[rev] = CLASSES.index("reversing")
        alive &= ~rev
        out = alive & (t >= t_exit)
        cls[out] = CLASSES.index("transmitted")
        alive &= ~out

        if step % AUDIT_STRIDE == 0 and np.any(alive):
            h = hamiltonian(t, pt, u, pu, e_field)
            resid = np.abs(h - h0) / scale
            finite = np.isfinite(resid)
            max_resid = np.where(alive & finite,
                                 np.maximum(max_resid, resid), max_resid)

    err.__exit__(None, None, None)
    cls[alive] = CLASSES.index("capped")
    counts = {name: int((cls == i).sum())
              for i, name in enumerate(CLASSES)}
    assert sum(counts.values()) == n, "census does not sum to N"
    return {
        "counts": counts,
        "missing": n - sum(counts.values()),
        "max_energy_residual": float(max_resid.max()),
        "polylines": {str(k): v for k, v in polylines.items()},
        "steps_run": step,
    }


def census_fraction(census, numerator: str, denominator_classes):
    """A fraction with an EXPLICIT denominator declaration. Returns
    the requested value together with the census-complete value and
    a discrepancy flag, so a deletion can never pass silently."""
    counts = census["counts"]
    total = sum(counts.values())
    denom = sum(counts[c] for c in denominator_classes)
    requested = counts[numerator] / denom if denom else float("nan")
    complete = counts[numerator] / total
    return {"requested": requested,
            "census_complete": complete,
            "denominator_classes": sorted(denominator_classes),
            "deleted_count": total - denom,
            "discrepant": bool(abs(requested - complete) > 1e-12
                               and total != denom)}


def signed_count_rule(ts, pts, levels, dt):
    """Check the path-degree rule at every generic level, exactly.
    The signed crossing count of a level must equal the endpoint
    bookkeeping, which is the statement that folds create orientation
    charge only in cancelling pairs. Non-generic levels, refused by
    the sealed instrument, are skipped and counted."""
    taus = np.arange(len(ts)) * dt
    ts = np.asarray(ts, dtype=float)
    pts = np.asarray(pts, dtype=float)
    t0, t1 = float(ts[0]), float(ts[-1])
    failures = []
    skipped = 0
    for level in levels:
        try:
            crossings, _ = polyline_level_crossings(taus, ts, pts,
                                                    float(level))
        except ValueError:
            skipped += 1
            continue
        signed = sum(int(c["orientation"]) for c in crossings)
        expect = (1 if t1 > level else 0) - (1 if t0 > level else 0)
        if signed != expect:
            failures.append((float(level), signed, expect))
    return failures, skipped


def main() -> int:
    record: dict = {"schema": "pf5-instrument-v1",
                    "label": "exploratory instrument"}

    # C1: harmonic conservation control (field-free, no quartic push
    # beyond the well, long integration)
    c1 = census_run(1.0, 0.0, 500, 1, max_steps=40_000)
    assert c1["max_energy_residual"] < 1e-6, \
        f"C1 drift {c1['max_energy_residual']}"

    # C2a: field-free cell, all members must transmit
    c2a = census_run(1.0, 0.0, 2_000, 2)
    assert c2a["counts"]["transmitted"] == 2_000, f"C2a {c2a['counts']}"

    # C2b: deterministically reversing cell, all members must reverse
    # (strong field far above the critical manifold at small gap)
    c2b = census_run(0.3, 2.5, 2_000, 3)
    assert c2b["counts"]["reversing"] == 2_000, f"C2b {c2b['counts']}"

    # C3: failure control, absurd step size, failures counted
    c3 = census_run(0.5, 0.8, 200, 4, dt=10.0, max_steps=2_000)
    assert c3["counts"]["nonfinite"] + c3["counts"]["capped"] > 0, \
        "C3 produced no failures to count"
    assert sum(c3["counts"].values()) == 200
    assert c3["missing"] == 0

    # C4: charge control on the analytic double fold
    taus = np.linspace(-1.5, 1.5, 4001)
    ts_fold = taus**3 - taus
    pts_fold = 3.0 * taus**2 - 1.0
    lvl = list(np.linspace(-1.37, 1.37, 41))
    c4_failures, c4_skipped = signed_count_rule(
        ts_fold, pts_fold, lvl, float(taus[1] - taus[0]))
    assert not c4_failures, f"C4 path-degree failures: {c4_failures}"
    assert c4_skipped < len(lvl) // 2, f"C4 too many refusals"

    # C5: deletion trap, the instrument must flag a dropped class
    frac_honest = census_fraction(c3, "reversing", CLASSES)
    frac_deleting = census_fraction(
        c3, "reversing", ("reversing", "transmitted"))
    assert not frac_honest["discrepant"]
    assert frac_deleting["discrepant"], \
        "C5: deleting failures was not flagged"

    record["controls"] = {
        "C1_harmonic_drift": c1["max_energy_residual"],
        "C2a_field_free_census": c2a["counts"],
        "C2b_deterministic_census": c2b["counts"],
        "C3_failure_census": c3["counts"],
        "C4_levels_checked": len(lvl),
        "C5_deletion_flagged": frac_deleting["discrepant"],
    }

    # Smoke application: one Sauter cell of the PF-4 family, full
    # witness record, no claim.
    smoke = census_run(0.75, 0.65, 5_000, 5, keep_polyline=(0, 1, 2))
    charge_failures = []
    for key, poly in smoke["polylines"].items():
        ts_m = poly["t"]
        span = (min(ts_m), max(ts_m))
        if span[1] - span[0] < 0.5:
            continue
        levels = list(np.linspace(span[0] + 0.05 * (span[1] - span[0]),
                                  span[1] - 0.05 * (span[1] - span[0]),
                                  37))
        fails, _ = signed_count_rule(ts_m, poly["pt"], levels, pilot.DT)
        charge_failures += fails
    assert not charge_failures, \
        f"smoke charge-balance failures: {charge_failures}"
    smoke_frac = census_fraction(smoke, "reversing", CLASSES)
    record["smoke_cell"] = {
        "P": 0.75, "E": 0.65, "n": 5_000,
        "census": smoke["counts"],
        "missing_trajectories": smoke["missing"],
        "max_energy_residual": smoke["max_energy_residual"],
        "reversal_fraction_census_complete":
            smoke_frac["census_complete"],
        "charge_rule_failures": 0,
    }
    assert smoke["max_energy_residual"] < 1e-5, \
        f"smoke drift {smoke['max_energy_residual']}"

    record["declared"] = {
        "family_constants": {"omega_u": pilot.OMEGA_U,
                             "lam": pilot.LAM, "g": pilot.G,
                             "sauter_L": pilot.SAUTER_L,
                             "t_start": pilot.T_START,
                             "dt": pilot.DT},
        "classes": list(CLASSES),
        "class_priority": "nonfinite, then reversing at first p_t "
                          "zero crossing, then transmitted at t >= "
                          "-T_START, then capped",
        "charge_assignment": "orientation charge = sign(dt/dtau), "
                             "declared here before any claim run",
        "audit_stride_steps": AUDIT_STRIDE,
        "energy_bar": 1e-5,
        "field_energy_clause": "out of scope for external-field "
            "families; applies when a dynamical field model is "
            "declared, and must be implemented before any such run",
    }
    record["statement"] = (
        "the PF-5 accounting layer is validated on exact controls, "
        "census always sums to the ensemble with zero missing "
        "trajectories, failures are counted rather than dropped and "
        "deletions are mechanically flagged, energy is tracked "
        "continuously for every member against a frozen bar, and the "
        "declared orientation charge obeys the path-degree rule "
        "exactly at every checked level; the claim-bearing PF-5 run "
        "awaits the family selected by the PREREG-PF4-003 harvest "
        "and must be sealed before it runs")
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
        / "pf5-instrument.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print("controls:", record["controls"])
    print("smoke census:", smoke["counts"], "drift",
          f"{smoke['max_energy_residual']:.2e}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
