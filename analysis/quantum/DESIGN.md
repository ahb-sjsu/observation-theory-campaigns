# A consumer-relative reliability governor for quantum devices

**Draft design note, 2026-08-23.** Companion to the O-RAN freshness governor
(`analysis/ran/DESIGN.md`). Where the RAN governor certifies radio freshness, this
certifies **quantum-device reliability** — per circuit, witnessed, refreshed at
the drift floor. It is the operational layer of the quantum-OT sketch below.

---

## 1. The problem it addresses

Quantum devices publish **aggregate** certificates — average gate fidelity,
Quantum Volume, algorithmic-qubit counts, a "calibrated" timestamp. Three
failures recur, and they are the same three the cross-domain whitepaper names:

- **Consumer-blindness.** The aggregate is blind to the **circuit footprint**
  (which qubits/gates/connectivity the circuit uses). A device with excellent
  average fidelity but one drifted qubit is fine for one circuit and broken for
  another *at the same instant* — measured in `XPROTO-QUANTUM`: on a device
  certified at 0.984 aggregate fidelity, **27–42% of circuits false-clear**
  because their footprint touches the bad qubit, while a footprint-aware
  certificate mis-clears 0%.
- **No witness.** "Calibrated" is inferred from the last calibration run, not
  graded against the outcome. The witness is native and cheap: **mirror /
  randomized-benchmarking / cycle-benchmarking success**, or a syndrome record.
- **No refresh floor.** Recalibration cadence is set by convention (hourly,
  daily), not derived from the **drift coherence time** — so a calibration goes
  stale-on-use between runs.

The consequence is the QC form of the benchmark-vs-application gap (the
AICSI/portfolio result): the number that certifies the device does not predict
what a specific algorithm feels.

## 2. The quantum-OT grammar (why the mapping is exact, not analogy)

OT's classical grammar has a literal quantum reading — and its foundations are
already **quantum estimation theory / quantum information geometry**:

| OT (classical) | Quantum reading | Established as |
|---|---|---|
| read operator `P_C` | a **POVM** `{E_k}`; `tr(P_C·ρ)` is the Born rule | measurement theory |
| distinguishability geometry | **quantum Fisher / Bures metric** | Braunstein–Caves |
| "all consumer-relative geometries" | **Petz monotone metrics** (all CPTP-monotone metrics on states) | Petz classification |
| what the consumer can't read | **quantum Fisher − classical Fisher** of the chosen POVM | Helstrom / Holevo |
| witness monotonicity | **quantum data-processing inequality** (relative entropy ↓ under CPTP) | Uhlmann/Lindblad |
| refresh floor ∝ coherence time | **T2** (dephasing time) + no-cloning / collapse | decoherence theory |
| distortion `tr(P_C·Σ)` | error read through the measurement/footprint | — |

So **a "quantum Observation Theory" already largely exists** as the union of
quantum estimation theory, Petz monotone metrics, and the quantum DPI. OT's
genuine addition is *not* new foundations but the **operational layer**:
consumer-relative, witnessed, refresh-floored **certification and governance** of
real devices — plus the cross-domain unification. That operational layer is what
this governor is, and it is buildable and measurable today (unlike, say, the
Ricci-flow speculation, which is deductive and has no consumer to serve).

**Honest scope.** Quantum error correction is the deployed witnessed-correction
loop — syndrome measurement is the non-demolition witness, correction is applied,
and the code-distance-vs-cycle-time condition *is* a refresh floor. OT unifies the
vocabulary but adds **no technique** to QEC. This governor targets the NISQ /
early-fault-tolerant operational gap (calibration drift, footprint-blind
certification, backend selection), not code design or the threshold theorem.

## 3. Architecture (mirrors `governor.ran`)

`observe → measure → govern → certify`, per **(certificate, consumer-circuit-family)**:

- **observe(cert, circuit_family, footprint, witness_ok, calib):** ingest per-qubit
  calibration (the device's published properties) and a benchmarking witness
  (mirror/RB success, or syndrome pass). `cert ∈ {gate_fidelity, readout,
  crosstalk, T2, layout}`.
- **FalseClearMeter:** rolling fraction of witnessed failures per
  (cert, circuit-family) — the first-class KPI, **per consumer**, not aggregate.
- **DriftFloorEstimator:** coherence time of the *calibration* value stream (the
  1/e autocorrelation crossing of the drift, reusing `RefreshFloorEstimator`), ×
  the measured floor slope → the **recalibration floor** (recalibrate faster than
  the calibration itself decorrelates — the OT-14 law, in the drift domain).
- **govern → GovernanceDecision** with the escalation ladder, quantum-specialized:
  1. **recalibrate_faster** — vacuous and the recal period exceeds the drift floor
     → shrink it (the direct OT-14 move).
  2. **re-layout / route_elsewhere** — already at the floor and still vacuous →
     the footprint hits a bad qubit/pair that recalibration won't fix → **map the
     circuit to a better footprint** (transpiler layout) or a better backend.
     This is **nearest-certified backend selection** (the geo-fleet cell) applied
     to QC: route by the footprint-witnessed certificate, not the aggregate QV.
  3. **add_mitigation** — no good footprint available → error mitigation
     (ZNE / measurement-error mitigation / dynamical decoupling) as the
     diversity analogue, at a stated cost.
- **certify:** emit a **footprint-relative** certificate (the consumer-aware cert
  of `XPROTO-QUANTUM`) that clears per circuit — the calibrated, witnessed object
  a scheduler can trust.

## 4. Integration surface

- **qiskit / IBM Quantum:** `backend.properties()` (per-qubit T1/T2, gate/readout
  error) is the calibration stream; the transpiler `layout`/`routing` stage is
  where **re-layout** actuates; mirror/RB circuits are the witness. Sealed rung of
  `XPROTO-QUANTUM` runs here on real hardware.
- **AWS Braket / IonQ / Quantinuum:** same grammar, architecture-specific floor —
  superconducting (T2 ~100 µs, fast drift, frequent recal), trapped-ion (T2 ~ s,
  slow drift, all-to-all), neutral-atom (reconfigurable layout). The governor is
  architecture-neutral; the floor and the actuation menu are the per-architecture
  profile — giving an **architecture-neutral, consumer-relative basis for
  comparing backends** (better than aggregate QV for "which backend for my
  circuit?").
- **Cloud schedulers:** the footprint-relative certificate is a routing input —
  send each circuit to the backend/footprint whose *witnessed* certificate clears
  it, not the one with the best headline number.

## 5. Where it fits (standards / community)

- A profile of the proposed IEEE-SA IC "Freshness and Reliability Certification"
  activity (the false-clear KPI + refresh floor, quantum profile).
- Aligns with device-benchmarking efforts (RB/XEB/mirror circuits, QED-C
  application-oriented benchmarks) by adding the **consumer-relative, witnessed,
  drift-floored certificate** as a first-class, reported object.
- Reference implementation path: a qiskit provider wrapper (a "governed backend")
  that layout-selects and certifies per circuit — the QC twin of the RAN rApp.

## 6. Status

- `XPROTO-QUANTUM` (model rung, qiskit-aer): shakedown **PASS**
  (naive_fc 0.28–0.43, aware_fc 0; agg-certified device). Sealed rung = real IBM
  hardware, seal ≥ 2026-08-24 (cooling-off).
- **`quantum_governor.py` BUILT** — the governed qiskit backend wrapper:
  `Calibration` (`from_target` for real hardware / `from_errors` for tests),
  `GovernedBackend.best_layout` (nearest-certified footprint, coupling-aware
  greedy), `.certify` (consumer-relative vs aggregate), `.run` (governs → certifies
  → runs on the base backend), escalation to `add_mitigation`. `test_quantum_
  governor.py` (3/3 PASS): best_layout avoids the bad qubit; the footprint cert
  clears a good layout (0.90) and flags a bad one (0.12) while the aggregate cert
  stays blind; and on a batch it drives false-clears **0.40 → 0.00** vs a
  calibration-blind placement — the cell's finding enforced operationally.
- Remaining: wire `Calibration.from_target` to a live IBM backend for the sealed
  rung; optional ZNE/DD in the `add_mitigation` branch.
