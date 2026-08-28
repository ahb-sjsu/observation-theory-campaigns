# SJSU Quantum Technology program: outreach draft

**From:** Andrew H. Bond, Senior Member IEEE (SJSU, Computer/Software Engineering)
**Re:** a consumer-relative reliability certificate for quantum devices, checked
against an independent measurement. Looking for a collaborator and real-hardware
access for the one run that would count as evidence.
**Status:** DRAFT for the owner to send. Nothing sent. Private repo. The quantum
wing is low-IP, since it reframes existing quantum estimation theory (see the
honesty note). Two candidate contacts below, in the order I'd approach them.

---

Distributed and networked systems constantly issue certificates of reliability:
this replica is fresh, this rate is supportable, this device is calibrated.
Observation Theory (OT) is a small set of rules, used across domains, for stating
and measuring such claims. A certificate should be evaluated through what the
actual consumer reads rather than through an aggregate, checked against an
independent measurement of the true outcome, and refreshed often enough to stay
ahead of drift. The number I report is the false-clear rate: how often "safe"
is wrong. I have measured it in routing,
databases, coordination services, and real 5G NR. The newest case is quantum
devices, and that is where I would value your program's expertise and hardware.

The quantum case is already built and reproducible. A device's aggregate
certificate, average gate fidelity or Quantum Volume, is blind to the circuit
footprint, meaning which qubits and gates a circuit actually uses. On a
heterogeneous device, say one drifted qubit among good ones, a circuit whose
footprint touches the bad qubit fails even though the device is certified. That
is a false clear. A certificate that reads the per-qubit calibration for the
footprint in use holds up instead.

I measured this on a qiskit-aer noise model I hand-constructed, so it is model
validation, not evidence. On a device certified at 0.984 aggregate fidelity, 27
to 42 percent of circuits false-clear, while a footprint-aware certificate
mis-clears 0 percent. The independent check is mirror-circuit success. A qiskit
backend wrapper, `GovernedBackend`, reads the calibration, routes each circuit to
the best footprint, and certifies per circuit. In a runnable test that takes
false-clears from 0.40 to 0.00 against calibration-blind placement.
`Calibration.from_target(backend.target)` is already wired for a real backend.
The same pattern shows up outside quantum. A benchmark can look excellent in
aggregate, at 99 percent explained variance, or 0.995 cosine similarity, or a
high Quantum Volume, and still be badly wrong on the specific thing a consumer
reads.

The ask that needs you is real IBM hardware. The pre-registration fixes the pass
and fail thresholds before the run, and it calls for real published calibration
and real mirror-circuit runs on a genuinely heterogeneous device. I will not
count a simulator result as evidence, and that rule holds across the program. The
mirror circuits are small and the runtime is modest.

The first person I would approach is Prof. Hiu Yung Wong in Electrical
Engineering (hiuyung.wong@sjsu.edu). He holds the Silicon Valley AMDT Endowed
Chair, is founding faculty of the MSQT program, and wrote "Introduction to
Quantum Computing: From Algorithm to Hardware." His research is
quantum-computing noise modeling and he teaches with qiskit and the IBM Q
Experience, so he very likely has the hardware access this run needs. EE is also
my product's home discipline. Three asks. First, point
`Calibration.from_target` at an IBM backend his group can reach and co-run the
mirror-circuit benchmark. Second, sanity-check the realism of the noise model and
whether the footprint-blindness gap survives on a real device. I expect it does,
since real backends genuinely have good and bad qubits. Third, if it holds,
co-author the quantum case. A qiskit provider built around this wrapper is a
natural student project.

The second is Prof. Hilary Hurst in Physics and Astronomy, the MSQT program
director (hilary.hurst@sjsu.edu, quantum@sjsu.edu). She works on quantum
measurement and feedback control for open systems, was at NIST and JQI in the
Spielman group, and was OSTP National Quantum Coordination Office liaison from
2024 to 2025. Two reasons. The first is the foundations. My honest claim, below,
is that a quantum OT is essentially quantum estimation theory, meaning Fisher
information in the Braunstein and Caves sense and Petz's classification of
CPTP-monotone metrics, plus the quantum data-processing inequality, with OT
adding only the operational certification layer. Her expertise is the right lens
for telling me whether that idea is new or already standard. The second is
standards. I am drafting an IEEE-SA Industry Connections whitepaper proposing
this as a cross-domain measurement methodology with a quantum profile, and her
OSTP quantum-coordination background bears on it directly. It fits the program's
mission too. Three asks. First, 30 minutes to assess the framing: is
consumer-relative, independently checked device certification a real gap or a
re-description?
Second, a pointer to whoever in the program has the cleanest IBM hardware path,
which may be Prof. Wong. Third, whether the standards angle or a program tie-in
interests her.

I should say this to a domain expert rather than hide it. The quantum
foundations here largely already exist. Petz's monotone metrics are all the
consumer-relative distinguishability geometries. Quantum Fisher information is
the best any consumer can do. The quantum data-processing inequality gives the
monotonicity of the independent check. What OT genuinely contributes is the
operational layer, meaning consumer-relative certification and governance of real
devices, checked against an independent measurement and refreshed against drift,
plus the cross-domain unification. It is not new physics. Quantum error
correction is already the deployed check-and-correct loop, and there I add
vocabulary, not technique. This is a NISQ operations contribution, about
benchmarking versus application. If that operational framing is also already
published, the fastest and most valuable outcome is you telling me where. That is
why I want a domain expert in the loop early.

The code is shareable now, in `analysis/quantum/`:

1. `fam_quantum.py`, the experiment.
2. `quantum_check.py`, the pass and fail bars, including the refusal to accept a
   simulator run as evidence.
3. `quantum_governor.py` and `test_quantum_governor.py`, the backend wrapper,
   3/3 tests pass.
4. `DESIGN.md`, the wrapper design and a table mapping OT terms onto quantum ones.
5. `PREREG-XPROTO-QUANTUM.md`, the pre-registration, which requires real IBM
   hardware before the result counts.

It all runs on a laptop CPU under qiskit-aer. The real-hardware run is the ask.
