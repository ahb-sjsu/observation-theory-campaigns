# SJSU Quantum Technology program — outreach draft

**From:** Andrew H. Bond, Senior Member IEEE (SJSU, Computer/Software Engineering)
**Re:** a consumer-relative, witnessed *reliability certificate* for quantum devices —
looking for a collaborator + real-hardware access to seal one measurement.
**Status:** DRAFT for the owner to send. Nothing sent. Private repo; the quantum
wing is low-IP (it reframes existing quantum estimation theory — see the honesty
note). Two candidate contacts below, in the order I'd approach them.

---

## The one-paragraph pitch

Distributed and networked systems constantly issue *certificates of reliability*
("this replica is fresh," "this rate is supportable," "this device is
calibrated"). Observation Theory (OT) is a small, cross-domain grammar for stating
and **measuring** such claims: a certificate should be (1) **consumer-relative** —
evaluated through the *read operator* of the actual consumer, not an aggregate;
(2) **witnessed** — graded against an independent measurement of the true outcome;
and (3) refreshed within its **coherence floor**. The reported metric is the
**false-clear rate**: how often "safe" is wrong. I've measured this across routing,
databases, coordination services, and real 5G NR. The newest instance is
**quantum devices** — and that's where I'd value your program's expertise and
hardware.

## The quantum instance, concretely (already built + reproducible)

A device's **aggregate** certificate — average gate fidelity, Quantum Volume — is
blind to the **circuit footprint** (which qubits/gates a circuit actually uses).
On a heterogeneous device (a drifted qubit among good ones), a circuit whose
footprint touches the bad qubit **fails despite the "certified" device** — a
false-clear. A footprint-relative certificate that reads the per-qubit calibration
holds.

- **Measured on a qiskit-aer noise model** (hand-constructed, so this is *model
  validation, not evidence*): on a device certified at 0.984 aggregate fidelity,
  **27–42% of circuits false-clear**; a footprint-aware certificate mis-clears 0%.
  Witness = mirror-circuit success.
- **A governed qiskit backend wrapper** (`GovernedBackend`) reads calibration,
  routes each circuit to the best footprint, and certifies per circuit — driving
  false-clears **0.40 → 0.00** vs a calibration-blind placement, in a runnable
  test. `Calibration.from_target(backend.target)` is already wired for a real
  backend.
- This is the QC form of a result I've measured elsewhere: a benchmark that looks
  great in aggregate (99% explained variance / 0.995 cosine / high QV) can be
  catastrophic on the specific thing a consumer reads.

**The ask that needs you:** the pre-registered *sealed* (evidence) rung requires
**real IBM hardware** — real published calibration + real mirror-circuit runs on a
genuinely heterogeneous device. I won't seal it on a simulator (a discipline I
hold across the program). Small mirror circuits; modest runtime.

## Contact 1 — Prof. Hiu Yung Wong (Electrical Engineering)

*hiuyung.wong@sjsu.edu · Silicon Valley AMDT Endowed Chair; MSQT founding faculty;
author, "Introduction to Quantum Computing: From Algorithm to Hardware."*

**Why him:** his research *is* quantum-computing **noise modeling**, and he teaches
with qiskit / IBM Q Experience — so the substrate is his home turf and he very
likely has the hardware access to seal the cell. EE is also my product's home
discipline.

**The concrete asks:** (a) point `Calibration.from_target` at an IBM backend his
group can reach and co-run the sealed mirror-circuit benchmark; (b) sanity-check
the noise-model realism and whether the footprint-blindness gap survives on a real
device (I expect it does — real backends genuinely have good and bad qubits); (c)
if it holds, co-author the quantum instance. A governed-backend qiskit provider is
a natural student project.

## Contact 2 — Prof. Hilary Hurst (Physics & Astronomy; MSQT Program Director)

*hilary.hurst@sjsu.edu · quantum@sjsu.edu · quantum measurement & feedback control
for open systems (ex-NIST/JQI, Spielman group); OSTP National Quantum Coordination
Office liaison, 2024–25.*

**Why her:** two reasons. First, the **foundations** — the honest claim below is
that a "quantum OT" is essentially quantum estimation theory (Braunstein–Caves
Fisher information, **Petz's classification of CPTP-monotone metrics**) plus the
quantum data-processing inequality, with OT adding only the *operational
certification* layer. Her measurement/feedback/open-systems expertise is exactly
the lens to tell me whether the "witnessed certificate" framing is new or already
standard — she is the ideal **witness** for the idea itself. Second, the
**standards** path: I'm drafting an IEEE-SA Industry Connections whitepaper
proposing this as a cross-domain measurement methodology, with a quantum profile;
her OSTP quantum-coordination background makes her an invaluable reader/ally, and
it dovetails with the program's mission.

**The concrete asks:** (a) 30 minutes to grade the framing — is consumer-relative,
witnessed device certification a real gap or a re-description? (b) a pointer to
whoever in the program has the cleanest IBM hardware path (may be Prof. Wong); (c)
interest in the standards angle / a program tie-in.

## Honesty note (say this to a domain expert, don't hide it)

To a measurement-theory or noise-modeling expert I must be upfront: the quantum
*foundations* here largely **already exist** (Petz monotone metrics = "all
consumer-relative distinguishability geometries"; quantum Fisher = the best any
consumer can do; quantum DPI = the witness monotonicity). OT's genuine
contribution is the **operational layer** — consumer-relative, witnessed,
drift-floored *certification and governance of real devices* — and the
cross-domain unification, **not** new physics. Quantum error correction is already
the deployed witnessed-correction loop; I add vocabulary, not technique, there.
This is a NISQ operations / benchmarking-vs-application contribution. If that
operational framing is also already published, the fastest, most valuable outcome
is you telling me where — that's why I want a domain expert in the loop early.

## Reproducibility hooks (shareable now)

`analysis/quantum/`: `fam_quantum.py` (the cell), `quantum_check.py` (sealed bars +
refuse-to-seal-on-sim), `quantum_governor.py` + `test_quantum_governor.py` (the
governed backend, 3/3 pass), `DESIGN.md` (the governor + the quantum-OT grammar
table), `PREREG-XPROTO-QUANTUM.md` (the pre-registration; sealed rung = real IBM
hardware). Runs on a laptop CPU (qiskit-aer); the real-hardware rung is the ask.
