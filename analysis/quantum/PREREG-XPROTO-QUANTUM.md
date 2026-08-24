# PREREG-XPROTO-QUANTUM — consumer-relative reliability of a quantum device certificate

**Family:** F-QUANTUM
**Constructed:** 2026-08-23
**Earliest seal:** 2026-08-24 (construct + 1 day cooling-off, enforced; no override)
**Graded seeds (disjoint from shakedown {0,1,2}):** {20260824, 20260825, 20260826}
**Status:** shakedown PASS; UNSEALED.

## Claim
A quantum device's **aggregate** certificate — average gate fidelity, or a
quantum-volume-style pass ("this backend is good") — is **blind to the circuit
footprint**. On a heterogeneous device (a drifted/bad qubit among good ones), a
circuit whose footprint touches the bad qubit **fails despite the certified
device** (a false-clear). A **consumer-relative** certificate that reads the
per-qubit calibration for the footprint (`P_C` = the qubits/gates the circuit
uses) clears per circuit and holds. This is the QC twin of the AICSI/portfolio
benchmark-vs-application result and the geo-fleet nearest-certified routing.

## Substrate
- **Model rung (this run):** qiskit-aer heterogeneous depolarizing noise model,
  8 qubits, one bad qubit (single-qubit rate 0.12 vs 0.001 good; ×8 two-qubit rate
  on bad-incident pairs). Witness = **mirror-circuit success** (random layers +
  exact inverse → ideal `|0…0>`; success = P(all zeros), transpiled at
  `optimization_level=0` so the mirror is not folded away).
- **Sealed rung (evidence):** the identical family on **real IBM Quantum
  hardware** via a footprint-mapped mirror-circuit benchmark; the aggregate cert
  = the backend's published average fidelity / QV; the witness = measured success.

## Consumers (read operators)
Circuits are sampled footprints (`FOOTPRINT_SIZE=3` qubits, `DEPTH=6`). The
**naive** policy applies the aggregate device certificate to every circuit
(blind). The **consumer-aware** policy reads the per-qubit calibration restricted
to the footprint (`predicted_success` over the footprint's gates) — the same
calibration data the device already publishes, read footprint-relative.

## Bars (committed before the graded run)
- **B1** `min naive_fc ≥ 0.25` — the aggregate cert false-clears per circuit.
- **B2** `max aware_fc ≤ 0.10` — the footprint-aware cert holds.
- **B3** `aware_fc ≤ naive_fc / 2` per seed (dominance).

## Manipulation checks (any fail ⇒ VOID)
- **MC1** `device_certified` True — the device genuinely passes its aggregate
  benchmark (the naive cert is not wrong *about the device*; it is wrong to apply
  it per-circuit). Guards against a trivially-broken device.
- **MC2** `good_footprint_success_rate ≥ target_success` — good-footprint circuits
  succeed, so the device works and the aware cert is not merely rejecting
  everything. Guards against a degenerate "reject-all" pass.
- **MC3** non-degenerate — `n_footprints ≥ 30` and `naive_fc < 1` (a real mix of
  good and bad footprints, not all-fail).

## Shakedown (seeds {0,1,2}, model rung) — recorded
naive_fc = 0.35 / 0.425 / 0.275; aware_fc = 0 / 0 / 0; agg_fid = 0.984 (certified);
good-fp success = 1.0. VERDICT PASS. The graded run reseals on disjoint seeds
≥2026-08-24; the real-hardware rung is the sealed evidence.

## What would falsify
A homogeneous device (no bad qubit) collapses naive_fc → aware_fc (nothing to be
consumer-relative about). If IBM's published backend fidelity already reflected
per-circuit footprint (it does not — it is aggregate), the gap would vanish.
