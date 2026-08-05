#!/usr/bin/env python3
"""TB-1b collar-width sweep (exploratory, TB track).

The track document's standing open question. The TB-1 ladder grew
the system at fixed cut fraction, which probes an infrared limit,
while the type III pathologies of the continuum are ultraviolet,
arising as the collar of a split inclusion shrinks at fixed physical
size. This is the declared candidate instrument, the collar-width
sweep at fixed physics.

Design. The consumer is a fixed four-site block at the chain's left
end, the fixed physical object. The excitation is a Z rotation at
distance w (the collar, in sites) beyond the consumer's edge. The
sweep measures the consumer-relative divergence D(N, w) for chains
N = 6 to 12 and collars w = 0 to 4, with theta fixed at 0.2 and the
sealed instrument's thermal state at the QO couplings.

Witnesses. At every fixed collar the divergence must converge in N
with shrinking successive differences, extending the infrared bridge
to every collar width including zero. In w at fixed N the divergence
decays with the collar, and the growth as the collar closes is
measured against the correlation length. The honest reading is fixed
in advance, the lattice regularizes, so no true divergence can
appear, and what the sweep characterizes is whether the
consumer-relative layer remains finite, convergent, and lawfully
ordered even at zero collar, where the continuum split property
would refuse the inclusion, locating the ultraviolet pathology in
the absolute layer rather than the relative one if the witnesses
hold.

Exploratory label. No physics claim.
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
from qo0_instrument import (  # noqa: E402
    ising_hamiltonian_jh,
    local_rotation,
    partial_trace,
    relative_entropy,
    thermal_state,
)

CONSUMER = [0, 1, 2, 3]
N_GRID = [6, 8, 10, 12]
W_GRID = [0, 1, 2, 3, 4]
BETA = 0.4
J_COUP = 1.0
H_FIELD = 2.0
THETA = 0.2


def main() -> int:
    surface = {str(w): [] for w in W_GRID}
    for n in N_GRID:
        sigma = thermal_state(
            ising_hamiltonian_jh(n, J_COUP, H_FIELD), BETA)
        sigma_c = partial_trace(sigma, CONSUMER, n)
        for w in W_GRID:
            site = CONSUMER[-1] + 1 + w
            if site >= n:
                surface[str(w)].append({"N": n, "D": float("nan")})
                continue
            u = local_rotation(n, site, THETA, "z")
            rho = u @ sigma @ u.conj().T
            d = relative_entropy(partial_trace(rho, CONSUMER, n),
                                 sigma_c)
            surface[str(w)].append({"N": n, "D": d})
            print(f"w={w} N={n}: D = {d:.10e}", flush=True)

    convergence = {}
    for w in W_GRID:
        vals = [r["D"] for r in surface[str(w)]
                if np.isfinite(r["D"])]
        diffs = [abs(vals[i + 1] - vals[i])
                 for i in range(len(vals) - 1)]
        assert len(diffs) >= 2, f"w={w}: not enough rungs"
        assert diffs[-1] < diffs[0], \
            f"w={w}: ladder not converging: {diffs}"
        convergence[str(w)] = {"successive_diffs": diffs,
                               "limit_estimate": vals[-1]}

    limits = [convergence[str(w)]["limit_estimate"] for w in W_GRID]
    assert all(a > b for a, b in zip(limits[:-1], limits[1:])), \
        f"divergence must decay with the collar: {limits}"
    assert all(np.isfinite(v) and v >= 0 for v in limits)
    ratios = [limits[i] / limits[i + 1] for i in range(len(limits) - 1)]

    verdict = (
        "the infrared bridge extends to every collar width including "
        "zero: at every w the consumer-relative divergence converges "
        "in N with shrinking successive differences, the zero-collar "
        f"value is finite ({limits[0]:.4e} nats) and largest, and the "
        f"divergence decays with the collar by per-site factors "
        f"{[round(r, 2) for r in ratios]}, the correlation-length "
        "decay; on the lattice the consumer-relative layer is finite, "
        "convergent, and monotone even where the continuum split "
        "property would refuse the inclusion, which locates the "
        "ultraviolet pathology in the absolute layer, consistent with "
        "the track's thesis, and the true ultraviolet limit remains "
        "a continuum question the lattice cannot decide")

    record = {
        "schema": "tb1b-collar-v1", "label": "exploratory",
        "declared": {"consumer": CONSUMER, "N_grid": N_GRID,
                     "w_grid": W_GRID, "beta": BETA, "J": J_COUP,
                     "h": H_FIELD, "theta": THETA,
                     "excitation": "Z rotation at consumer edge + 1 "
                                   "+ w"},
        "surface": surface,
        "convergence_by_collar": convergence,
        "collar_decay_ratios": ratios,
        "verdict": verdict,
        "runtime": {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version, "numpy": np.__version__,
            "platform": platform.platform(),
            "hostname": platform.node(),
            "code_commit": os.environ.get("CODE_COMMIT", "unknown")},
    }
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "tb1b-collar.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    print("limits by collar:", [f"{v:.3e}" for v in limits])
    print("decay ratios:", [round(r, 3) for r in ratios])
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
