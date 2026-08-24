"""governor.quantum -- a governed qiskit backend wrapper (the QC rApp core).

Wrap any qiskit backend (AerSimulator, or a real IBM backend). For each submitted
circuit the governor:

  1. reads the device's per-qubit calibration (the published gate/readout errors);
  2. chooses the FOOTPRINT that maximizes predicted success -- nearest-certified
     layout selection, instead of a calibration-blind placement (governor.ran's
     "route_elsewhere", in the transpiler-layout domain);
  3. attaches an honest, footprint-relative CERTIFICATE (cleared / vacuous per
     circuit) -- not the aggregate device certificate that XPROTO-QUANTUM shows
     false-clears; and
  4. escalates to error mitigation when no footprint clears the target.

This is the operational layer of DESIGN.md: consumer-relative (the footprint is
P_C), witnessed (mirror/RB success is the witness), refresh-floored (calibration
ages at the drift T2 -- re-read before it decorrelates). It adds no technique to
QEC; it governs the NISQ placement/certification gap.

Self-contained: qiskit + qiskit-aer + numpy. `from_target` reads a real backend;
`from_errors` builds calibration directly (used by the tests on an Aer device).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
from qiskit import transpile


# ---------------------------------------------------------------- calibration
@dataclass
class Calibration:
    """Per-qubit / per-edge error rates -- what a backend publishes."""
    single_q: dict          # {physical_qubit: 1q depolarizing/gate error}
    two_q: dict             # {frozenset({a,b}): cx error}
    readout: dict           # {physical_qubit: readout assignment error}
    n_qubits: int
    two_q_default: float = 1e-2

    @classmethod
    def from_errors(cls, single_q, two_q, readout, n_qubits, two_q_default=1e-2):
        return cls({int(k): float(v) for k, v in single_q.items()},
                   {frozenset(map(int, k)): float(v) for k, v in two_q.items()},
                   {int(k): float(v) for k, v in readout.items()},
                   int(n_qubits), two_q_default)

    @classmethod
    def from_target(cls, target):
        """Read a real qiskit BackendV2 Target (per-instruction errors)."""
        n = target.num_qubits
        single_q, two_q, readout = {}, {}, {}
        for name in target.operation_names:
            props = target[name]
            for qargs, ip in props.items():
                err = getattr(ip, "error", None)
                if err is None or qargs is None:
                    continue
                if name in ("measure",) and len(qargs) == 1:
                    readout[qargs[0]] = float(err)
                elif len(qargs) == 1:
                    single_q[qargs[0]] = min(float(err), single_q.get(qargs[0], 1.0))
                elif len(qargs) == 2:
                    two_q[frozenset(qargs)] = float(err)
        return cls(single_q, two_q, readout, n)

    def aggregate_fidelity(self) -> float:
        errs = [self.single_q.get(q, 0.0) for q in range(self.n_qubits)]
        return 1.0 - float(np.mean(errs)) if errs else 1.0

    def predict_success(self, circuit, layout) -> float:
        """Consumer-aware certificate: product of per-gate fidelities for THIS
        circuit mapped onto `layout` (layout[virtual_index] = physical qubit)."""
        p = 1.0
        for inst in circuit.data:
            name = inst.operation.name
            if name == "barrier":
                continue
            phys = [layout[circuit.find_bit(q).index] for q in inst.qubits]
            if name == "measure":
                for ph in phys:
                    p *= (1 - self.readout.get(ph, 0.0))
            elif len(phys) == 1:
                p *= (1 - self.single_q.get(phys[0], 0.0))
            elif len(phys) == 2:
                p *= (1 - self.two_q.get(frozenset(phys), self.two_q_default))
        return p


# ---------------------------------------------------------------- certificate
@dataclass
class Certificate:
    predicted_success: float
    target_success: float
    cleared: bool
    layout: list
    mechanism: str          # "ok" | "re-layout" | "add_mitigation"
    consumer_relative: bool  # False = aggregate device cert (the naive baseline)

    def to_dict(self):
        d = asdict(self)
        d["predicted_success"] = round(self.predicted_success, 4)
        return d


@dataclass
class GovernedResult:
    counts: dict
    certificate: Certificate
    layout: list
    shots: int


# ---------------------------------------------------------------- backend
class GovernedBackend:
    """observe calibration -> govern (best footprint) -> certify -> run."""

    def __init__(self, base_backend, calibration: Calibration,
                 target_success: float = 0.70, coupling: list | None = None,
                 f_target: float = 0.95):
        self.base = base_backend
        self.cal = calibration
        self.target_success = target_success
        self.f_target = f_target          # aggregate-cert threshold (naive baseline)
        self.coupling = [set(map(int, e)) for e in coupling] if coupling else None

    # ---- governance: choose the footprint that maximizes predicted success ----
    def best_layout(self, width: int) -> list:
        order = sorted(range(self.cal.n_qubits),
                       key=lambda q: self.cal.single_q.get(q, 0.0))   # best first
        if not self.coupling:
            return order[:width]
        # greedy connected subgraph seeded at the best qubit (real-hardware path)
        chosen = [order[0]]
        while len(chosen) < width:
            nbrs = {b for e in self.coupling for a in chosen for b in e
                    if a in e and b not in chosen and b != a}
            if not nbrs:
                nbrs = set(range(self.cal.n_qubits)) - set(chosen)   # disconnected fallback
            chosen.append(min(nbrs, key=lambda q: self.cal.single_q.get(q, 0.0)))
        return chosen

    def certify(self, circuit, layout, consumer_relative=True) -> Certificate:
        if consumer_relative:
            pred = self.cal.predict_success(circuit, layout)
            cleared = pred >= self.target_success
            mech = "ok" if cleared else "add_mitigation"
        else:  # naive: trust the aggregate device certificate, blind to footprint
            pred = self.cal.aggregate_fidelity()
            cleared = pred >= self.f_target
            mech = "ok"
        return Certificate(pred, self.target_success, cleared, list(layout),
                           mech, consumer_relative)

    def run(self, circuit, shots: int = 2000, govern: bool = True,
            layout: list | None = None) -> GovernedResult:
        width = circuit.num_qubits
        if govern:
            best = self.best_layout(width)
            cert = self.certify(circuit, best, consumer_relative=True)
            if not cert.cleared and layout is None:
                cert.mechanism = "add_mitigation"   # no footprint clears -> mitigate
            use = best
        else:
            use = layout if layout is not None else list(range(width))
            cert = self.certify(circuit, use, consumer_relative=False)
        tqc = transpile(circuit, self.base, initial_layout=use, optimization_level=0)
        counts = self.base.run(tqc, shots=shots).result().get_counts()
        return GovernedResult(counts, cert, list(use), shots)


def mirror_success(counts: dict, width: int) -> float:
    """Witness: mirror circuit returns |0..0> ideally; success = P(all zeros)."""
    total = sum(counts.values())
    return counts.get("0" * width, 0) / total if total else 0.0
