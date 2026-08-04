#!/usr/bin/env python3
"""TB-2 flip persistence (exploratory, TYPE-III-BRIDGE track).

Open question 4 decided (primary accounting): the budget is a FIXED
ABSOLUTE number of stored qubits k as N grows. Rationale recorded in
the track document: the task is local and its relevant halo converges
(TB-1), so scarcity relative to the task is N-independent, and a
fractional budget has no type III meaning because algebra dimension is
the quintessential type I artifact. The fractional accounting is
retained only as the secondary diagnostic expected to trivialize.

Protocol: the QO-2 flip on the kept half of chains N = 6, 8, 10, 12.
Kept region = sites N/2..N-1 (m = N/2 qubits), flux site = reduced
index 0 (the cut boundary), strong site = reduced index m//2. Scenario
grids are those of PREREG-QO2-001 (train and held disjoint). Encoder
family = keep k of the m qubits with vacuum-marginal decode, exhaustive
subset search, arms selected on training, verdicts on held-out, with
the anti-arm (flux qubit pinched) at every budget. Witnesses: per-N
flip indicator versus k, held-out task and infidelity gaps at fixed
k = 1 and k = 2 (the convergence question), the largest flipping k
(the collapse budget), and its fraction of m (expected to shrink).

Exploratory label. No physics claim.
"""
from __future__ import annotations

import itertools
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
from qo0_instrument import (  # noqa: E402
    dephase,
    ising_hamiltonian_jh,
    local_rotation,
    partial_trace,
    thermal_state,
)
from qo2_flip import reorder_qubits, uhlmann_fidelity  # noqa: E402

J_COUPLING = 1.0
H_FIELD = 2.0
BETA = 0.5
LADDER = [6, 8, 10, 12]
TRAIN_STRONG = [0.55, 0.85, 1.15]
TRAIN_WEAK = [0.12, 0.22, 0.32]
HELD_STRONG = [0.70, 1.00, 1.30]
HELD_WEAK = [0.08, 0.18, 0.28]
MARGIN = 0.01


def flux_op(m: int) -> np.ndarray:
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    op = np.array([[1.0]], dtype=complex)
    for j in range(m):
        op = np.kron(op, x if j == 0 else np.eye(2))
    return -H_FIELD * op


def scenarios(vacuum: np.ndarray, m: int, strong_q: int,
              strong_list, weak_list):
    states = []
    for ts, tw in itertools.product(strong_list, weak_list):
        u = (local_rotation(m, strong_q, ts, "z")
             @ local_rotation(m, 0, tw, "z"))
        states.append(u @ vacuum @ u.conj().T)
    return states


def encode_decode(rho, keep, vacuum, m, *, pinch_flux=False):
    keep = sorted(keep)
    discard = [q for q in range(m) if q not in keep]
    kept = partial_trace(rho, keep, m)
    if pinch_flux and 0 in keep:
        kept = dephase(kept, keep.index(0), len(keep), 0.5)
    if discard:
        prior = partial_trace(vacuum, discard, m)
        combined = np.kron(kept, prior)
    else:
        combined = kept
    return reorder_qubits(combined, keep + discard, m)


def arm_scores(states, keep, vacuum, m, task, *, pinch_flux=False):
    t_err, infid = [], []
    for rho in states:
        rec = encode_decode(rho, keep, vacuum, m, pinch_flux=pinch_flux)
        t_err.append(abs(float(np.real(np.trace(rho @ task)))
                         - float(np.real(np.trace(rec @ task)))))
        infid.append(1.0 - uhlmann_fidelity(rho, rec))
    return float(np.mean(t_err)), float(np.mean(infid))


def rung(n: int) -> dict:
    m = n // 2
    kept_sites = list(range(m, n))
    strong_q = m // 2
    sigma_full = thermal_state(
        ising_hamiltonian_jh(n, J_COUPLING, H_FIELD), BETA
    )
    vacuum = partial_trace(sigma_full, kept_sites, n)
    task = flux_op(m)
    train = scenarios(vacuum, m, strong_q, TRAIN_STRONG, TRAIN_WEAK)
    held = scenarios(vacuum, m, strong_q, HELD_STRONG, HELD_WEAK)

    budgets = {}
    for k in range(1, m):
        subsets = [list(s) for s in itertools.combinations(range(m), k)]
        train_scores = {
            tuple(s): arm_scores(train, s, vacuum, m, task) for s in subsets
        }
        f_arm = list(min(train_scores, key=lambda s: train_scores[s][1]))
        t_arm = list(min(train_scores, key=lambda s: train_scores[s][0]))
        f_held = arm_scores(held, f_arm, vacuum, m, task)
        t_held = arm_scores(held, t_arm, vacuum, m, task)
        anti = arm_scores(held, t_arm, vacuum, m, task, pinch_flux=True)
        interpretable = anti[0] > max(f_held[0], t_held[0])
        flip = (interpretable
                and t_held[0] < f_held[0] - MARGIN
                and t_held[1] > f_held[1] + MARGIN)
        budgets[k] = {
            "f_arm": f_arm, "t_arm": t_arm,
            "F_task": f_held[0], "F_infid": f_held[1],
            "T_task": t_held[0], "T_infid": t_held[1],
            "anti_task": anti[0],
            "interpretable": bool(interpretable), "flip": bool(flip),
        }

    flipping = [k for k, b in budgets.items() if b["flip"]]
    return {
        "N": n, "m": m, "strong_q": strong_q,
        "budgets": budgets,
        "flip_region": flipping,
        "k_collapse": max(flipping) if flipping else 0,
        "k_collapse_fraction": (max(flipping) / m) if flipping else 0.0,
    }


def main() -> int:
    rungs = [rung(n) for n in LADDER]
    for r in rungs:
        b1 = r["budgets"][1]
        print(f"N={r['N']} (m={r['m']}): flip region {r['flip_region']}, "
              f"k=1 gaps task {b1['F_task'] - b1['T_task']:.4f} / infid "
              f"{b1['T_infid'] - b1['F_infid']:.4f}, anti "
              f"{b1['anti_task']:.3f}")

    for r in rungs:
        for k, b in r["budgets"].items():
            assert b["interpretable"], \
                f"anti-arm not worst at N={r['N']}, k={k}"
        assert r["budgets"][1]["flip"], f"no flip at k=1 for N={r['N']}"
        assert abs(r["budgets"][1]["T_task"]) < 1e-12, \
            "T-arm should preserve the local functional exactly at k=1"

    task_gaps = [r["budgets"][1]["F_task"] - r["budgets"][1]["T_task"]
                 for r in rungs]
    infid_gaps = [r["budgets"][1]["T_infid"] - r["budgets"][1]["F_infid"]
                  for r in rungs]
    task_diffs = [abs(b - a) for a, b in zip(task_gaps[:-1], task_gaps[1:],
                                             strict=False)]
    infid_diffs = [abs(b - a) for a, b in
                   zip(infid_gaps[:-1], infid_gaps[1:], strict=False)]
    fractions = [r["k_collapse_fraction"] for r in rungs]

    analysis = {
        "k1_task_gap": {"values": task_gaps, "diffs": task_diffs,
                        "converging": task_diffs[-1] < task_diffs[0]},
        "k1_infid_gap": {"values": infid_gaps, "diffs": infid_diffs,
                         "converging": infid_diffs[-1] < infid_diffs[0]},
        "k_collapse": [r["k_collapse"] for r in rungs],
        "k_collapse_fraction": fractions,
        "fraction_shrinking": fractions[-1] <= fractions[0],
    }
    assert analysis["k1_task_gap"]["converging"], "task gap not converging"
    assert analysis["k1_infid_gap"]["converging"], "infid gap not converging"

    record = {
        "schema": "tb2-flip-ladder-v1",
        "label": "exploratory",
        "oq4_decision": "primary accounting is fixed absolute budget k; "
            "the task is local and its halo converges (TB-1), and "
            "fractional budgets have no type III meaning since algebra "
            "dimension is a type I artifact; the fraction is a secondary "
            "diagnostic expected to trivialize",
        "declared": {"J": J_COUPLING, "h": H_FIELD, "beta": BETA,
                     "ladder": LADDER, "margin": MARGIN,
                     "train": [TRAIN_STRONG, TRAIN_WEAK],
                     "held": [HELD_STRONG, HELD_WEAK]},
        "rungs": rungs,
        "analysis": analysis,
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
        / "tb2-flip-ladder.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True),
                      encoding="utf-8")

    print(f"k=1 task gaps {[round(v, 5) for v in task_gaps]} "
          f"(diffs {[f'{d:.1e}' for d in task_diffs]})")
    print(f"k=1 infid gaps {[round(v, 5) for v in infid_gaps]} "
          f"(diffs {[f'{d:.1e}' for d in infid_diffs]})")
    print(f"collapse k {analysis['k_collapse']}, fractions "
          f"{[round(f, 3) for f in fractions]}, shrinking "
          f"{analysis['fraction_shrinking']}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
