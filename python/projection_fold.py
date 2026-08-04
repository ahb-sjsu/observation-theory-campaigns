"""Reference models and diagnostics for projection-fold experiments.

The module deliberately separates exact kinematics from candidate dynamics.
Nothing here is a model of quantum electrodynamics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Iterable
import json
import math

import numpy as np


@dataclass(frozen=True)
class Branch:
    tau: float
    t: float
    x: float
    orientation: int


@dataclass(frozen=True)
class FoldEvent:
    tau: float
    t: float
    x: float
    acceleration_t: float
    fold_type: str


@dataclass
class ToyResult:
    parameters: dict[str, float]
    initial_state: list[float]
    fold_events: list[dict[str, Any]]
    fold_count: int
    positive_orientation_segments: int
    negative_orientation_segments: int
    energy_initial: float
    energy_final: float
    max_relative_energy_drift: float
    final_state: list[float]
    n_steps: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(payload.encode("utf-8")).hexdigest()


def analytic_fold_branches(
    t_obs: float,
    *,
    t0: float = 0.0,
    tau0: float = 0.0,
    a: float = 1.0,
    x0: float = 0.0,
    velocity: float = 1.0,
    atol: float = 1e-12,
) -> list[Branch]:
    """Return all branches of t=t0+a(tau-tau0)^2 at an observation time."""
    if abs(a) <= atol:
        raise ValueError("a must be nonzero")
    ratio = (t_obs - t0) / a
    if ratio < -atol:
        return []
    if abs(ratio) <= atol:
        return [Branch(tau0, t0, x0, 0)]

    root = math.sqrt(ratio)
    branches: list[Branch] = []
    for sign in (-1.0, 1.0):
        tau = tau0 + sign * root
        dt_dtau = 2.0 * a * (tau - tau0)
        orientation = 1 if dt_dtau > 0 else -1
        x = x0 + velocity * (tau - tau0)
        branches.append(Branch(tau, t_obs, x, orientation))
    return branches


def signed_branch_count(branches: Iterable[Branch]) -> int:
    return int(sum(branch.orientation for branch in branches))


def classify_scalar_critical_point(
    first_derivative: float,
    second_derivative: float,
    *,
    first_tol: float = 1e-9,
    second_tol: float = 1e-8,
) -> str:
    if abs(first_derivative) > first_tol:
        return "regular"
    if abs(second_derivative) <= second_tol:
        return "degenerate"
    return "creation-fold" if second_derivative > 0 else "annihilation-fold"


def polynomial_time_branches(
    coefficients: Iterable[float],
    t_obs: float,
    *,
    x0: float = 0.0,
    velocity: float = 1.0,
    imag_tol: float = 1e-9,
    residual_tol: float = 1e-10,
    derivative_floor: float = 1e-9,
) -> list[Branch]:
    """Return all branches of a polynomial time map t(tau) at one observation time.

    Coefficients use the numpy convention, highest degree first. The worldline
    is x(tau) = x0 + velocity*tau. Generic slices only: an observation time
    whose preimage touches a critical point of the time map is refused with
    ValueError, because branch counting is ill-posed there; the critical point
    itself belongs to ``polynomial_critical_points`` and the classifier.
    """
    poly = np.asarray(list(coefficients), dtype=float)
    shifted = poly.copy()
    shifted[-1] -= t_obs
    candidates = np.roots(shifted) if len(shifted) > 1 else np.array([])
    taus = np.sort(candidates[np.abs(candidates.imag) <= imag_tol].real)
    derivative = np.polyder(poly)
    branches: list[Branch] = []
    for tau in taus:
        residual = abs(float(np.polyval(shifted, tau)))
        if residual > residual_tol:
            raise ValueError(f"root residual {residual:g} exceeds {residual_tol:g}")
        slope = float(np.polyval(derivative, tau))
        if abs(slope) <= derivative_floor:
            raise ValueError(
                "non-generic slice: a preimage lies on a critical point; "
                "use polynomial_critical_points for the fold itself"
            )
        orientation = 1 if slope > 0 else -1
        branches.append(
            Branch(float(tau), float(t_obs), x0 + velocity * float(tau), orientation)
        )
    return branches


def polynomial_critical_points(
    coefficients: Iterable[float],
    *,
    first_tol: float = 1e-9,
    second_tol: float = 1e-8,
    imag_tol: float = 1e-9,
) -> list[dict[str, Any]]:
    """Locate and classify all real critical points of a polynomial time map."""
    poly = np.asarray(list(coefficients), dtype=float)
    d1 = np.polyder(poly)
    d2 = np.polyder(d1)
    candidates = np.roots(d1) if len(d1) > 1 else np.array([])
    taus = np.sort(candidates[np.abs(candidates.imag) <= imag_tol].real)
    points: list[dict[str, Any]] = []
    for tau in taus:
        first = float(np.polyval(d1, tau))
        second = float(np.polyval(d2, tau))
        points.append(
            {
                "tau": float(tau),
                "t": float(np.polyval(poly, tau)),
                "first_derivative": first,
                "second_derivative": second,
                "classification": classify_scalar_critical_point(
                    first, second, first_tol=first_tol, second_tol=second_tol
                ),
            }
        )
    return points


def schwinger_circle_action(radius: float, mass: float, charge_field: float) -> float:
    """Semiclassical circular worldline action S=2*pi*m*R-pi*|qE|*R^2."""
    if radius < 0 or mass <= 0 or charge_field <= 0:
        raise ValueError("radius>=0, mass>0, and |qE|>0 are required")
    return 2.0 * math.pi * mass * radius - math.pi * charge_field * radius**2


def schwinger_optimum(mass: float, charge_field: float) -> tuple[float, float]:
    if mass <= 0 or charge_field <= 0:
        raise ValueError("mass>0 and |qE|>0 are required")
    radius = mass / charge_field
    action = math.pi * mass**2 / charge_field
    return radius, action


def toy_energy(state: np.ndarray, params: dict[str, float]) -> np.ndarray:
    """Hamiltonian energy for one state or a batch of states.

    State order is [t, p_t, x, p_x, u, p_u].
    """
    y = np.asarray(state, dtype=float)
    t, pt, _x, px, u, pu = np.moveaxis(y, -1, 0)
    wt = params["omega_t"]
    wu = params["omega_u"]
    lam = params["lambda"]
    coupling = params["g"] * params["field"]
    return (
        0.5 * (pt**2 + px**2 + pu**2)
        + 0.5 * wt**2 * t**2
        + 0.5 * wu**2 * u**2
        + 0.25 * lam * u**4
        + coupling * t * u
    )


def _toy_force(t: np.ndarray, u: np.ndarray, params: dict[str, float]) -> tuple[np.ndarray, np.ndarray]:
    wt = params["omega_t"]
    wu = params["omega_u"]
    lam = params["lambda"]
    coupling = params["g"] * params["field"]
    force_t = -(wt**2) * t - coupling * u
    force_u = -(wu**2) * u - lam * u**3 - coupling * t
    return force_t, force_u


def simulate_toy_hamiltonian(
    initial_state: Iterable[float],
    params: dict[str, float],
    *,
    dt: float,
    tau_max: float,
    fold_velocity_tol: float = 1e-10,
) -> ToyResult:
    """Integrate the toy Hamiltonian with velocity Verlet and locate p_t zero crossings."""
    if dt <= 0 or tau_max <= 0:
        raise ValueError("dt and tau_max must be positive")
    state = np.asarray(list(initial_state), dtype=float)
    if state.shape != (6,):
        raise ValueError("initial_state must contain [t,pt,x,px,u,pu]")

    required = {"omega_t", "omega_u", "lambda", "g", "field"}
    missing = required - params.keys()
    if missing:
        raise ValueError(f"missing parameters: {sorted(missing)}")

    n_steps = int(math.ceil(tau_max / dt))
    energy0 = float(toy_energy(state, params))
    scale = max(abs(energy0), 1.0)
    max_drift = 0.0
    folds: list[FoldEvent] = []

    t, pt, x, px, u, pu = state.tolist()
    previous_pt = pt
    previous_tau = 0.0
    previous_t = t
    previous_x = x

    positive_segments = int(pt > fold_velocity_tol)
    negative_segments = int(pt < -fold_velocity_tol)

    for step in range(1, n_steps + 1):
        tau = min(step * dt, tau_max)
        h = tau - previous_tau
        ft0, fu0 = _toy_force(np.array(t), np.array(u), params)
        pt_half = pt + 0.5 * h * float(ft0)
        pu_half = pu + 0.5 * h * float(fu0)

        t_new = t + h * pt_half
        u_new = u + h * pu_half
        x_new = x + h * px

        ft1, fu1 = _toy_force(np.array(t_new), np.array(u_new), params)
        pt_new = pt_half + 0.5 * h * float(ft1)
        pu_new = pu_half + 0.5 * h * float(fu1)

        crossed = (
            (previous_pt > fold_velocity_tol and pt_new < -fold_velocity_tol)
            or (previous_pt < -fold_velocity_tol and pt_new > fold_velocity_tol)
        )
        if crossed:
            alpha = abs(previous_pt) / (abs(previous_pt) + abs(pt_new))
            tau_fold = previous_tau + alpha * h
            t_fold = previous_t + alpha * (t_new - previous_t)
            x_fold = previous_x + alpha * (x_new - previous_x)
            acceleration_t = float(ft0 + alpha * (ft1 - ft0))
            fold_type = "creation-fold" if acceleration_t > 0 else "annihilation-fold"
            folds.append(FoldEvent(tau_fold, t_fold, x_fold, acceleration_t, fold_type))

        if pt_new > fold_velocity_tol and previous_pt <= fold_velocity_tol:
            positive_segments += 1
        if pt_new < -fold_velocity_tol and previous_pt >= -fold_velocity_tol:
            negative_segments += 1

        t, pt, x, px, u, pu = t_new, pt_new, x_new, px, u_new, pu_new
        state_now = np.array([t, pt, x, px, u, pu])
        energy_now = float(toy_energy(state_now, params))
        max_drift = max(max_drift, abs(energy_now - energy0) / scale)

        previous_pt = pt
        previous_tau = tau
        previous_t = t
        previous_x = x

    final_state = [float(v) for v in (t, pt, x, px, u, pu)]
    return ToyResult(
        parameters={key: float(params[key]) for key in sorted(required)},
        initial_state=[float(v) for v in initial_state],
        fold_events=[asdict(event) for event in folds],
        fold_count=len(folds),
        positive_orientation_segments=positive_segments,
        negative_orientation_segments=negative_segments,
        energy_initial=energy0,
        energy_final=float(toy_energy(np.asarray(final_state), params)),
        max_relative_energy_drift=max_drift,
        final_state=final_state,
        n_steps=n_steps,
    )
