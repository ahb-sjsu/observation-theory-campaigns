# Quantum-Computing Track: consumer-relative device reliability certification

**Status:** re-homed 2026-08-24 from `network-governor`. Chip ⚛️ QC. Freshness
program ([FRESHNESS-PROGRAM.md](FRESHNESS-PROGRAM.md)). Cell **XPROTO-QUANTUM**
UNSEALED — sealed rung gated on real IBM hardware (SJSU outreach in flight); the
aer model rung is code/model validation, refused as a seal in the checker.

## Question

A quantum device's **aggregate** certificate — average gate fidelity, Quantum
Volume — is blind to the **circuit footprint** (which qubits/gates a circuit uses).
On a heterogeneous device (a drifted qubit among good ones), a circuit whose
footprint touches the bad qubit **fails despite the "certified" device** — a
false-clear. A **footprint-relative** certificate that reads the per-qubit
calibration holds. This is the QC form of the benchmark-vs-application gap
(the AICSI/portfolio result) and geo-fleet nearest-certified routing, applied to
backend/qubit selection.

## Why QC is a genuine instance (not analogy)

- decoherence time **T2** *is* the coherence time → the refresh floor (recalibrate
  faster than the calibration decorrelates);
- the read operator *is* a **POVM**, `tr(P_C·ρ)` the Born rule;
- the distinguishability geometry is the **quantum Fisher / Bures** metric, and
  **Petz's classification of CPTP-monotone metrics** = "all consumer-relative
  distinguishability geometries"; the witness monotonicity is the **quantum DPI**.

So a "quantum OT" already largely exists as quantum estimation theory + Petz +
quantum DPI; OT adds the **operational** certification/governance layer, not new
physics. QEC is the deployed witnessed-correction loop (OT adds vocabulary, not
technique). This track targets the NISQ placement/certification gap.

## Design (family F-QUANTUM; harness `analysis/quantum/fam_quantum.py`)

qiskit-aer heterogeneous depolarizing device (8 qubits, q3 bad: 1q rate 0.12 vs
0.001, ×8 two-qubit on bad-incident pairs). Witness = **mirror-circuit success**
(random layers + exact inverse → ideal `|0…0>`, `optimization_level=0` + a barrier
so the mirror is not folded away). Naive policy applies the aggregate device cert
per circuit (blind); consumer-aware reads per-qubit calibration for the footprint.

Bars (`quantum_check.py`): B1 min naive_fc ≥ 0.25; B2 max aware_fc ≤ 0.10; B3
dominance; MC1 device aggregate-certified; MC2 good-footprint success ≥ target;
MC3 non-degenerate. `--seal` REFUSES unless mode=="hardware".

## Result (model rung, shakedown)

Seeds {0,1,2}: device aggregate-certified (0.984 ≥ 0.95) yet **naive_fc
0.275–0.425** vs **aware_fc 0.0**, good-footprint success 1.0. All bars + MCs PASS.
The **governed qiskit backend** (`quantum_governor.py`, `test_quantum_governor.py`
3/3) routes each circuit to the best footprint and drives false-clears
**0.40 → 0.00** vs a calibration-blind placement — the finding enforced
operationally. Design + the quantum-OT grammar table: `analysis/quantum/DESIGN.md`.

## Seal path

Real IBM hardware: `Calibration.from_target(backend.target)` (already wired) +
footprint-mapped mirror-circuit runs; aggregate cert = the backend's published
QV/avg-fidelity. Collaboration: SJSU MSQT (Wong — noise modeling/hardware; Hurst —
measurement-theory framing + standards). Seal ≥ construct+1 day once on hardware.
