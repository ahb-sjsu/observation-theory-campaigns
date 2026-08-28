# SIMSOPT / DESC outreach: collaborate on XPROTO-STELL

**From:** Andrew H. Bond, Senior Member IEEE (SJSU).
**Re:** a consumer-relative reading of the stellarator design objective. Along the
optimization trajectory, does the aggregate quasi-symmetry residual certify
success while a transport-grade consumer is already degrading?
**Status:** DRAFT for the owner to send. Nothing sent. Public methodology; nothing
IP-gated. Two contacts below (use current published addresses or the repos' contact
routes; I have not hard-coded emails).

1. Matt Landreman (SIMSOPT lead and `pyQSC` author; U. Maryland /
   hiddenSymmetries). The natural first contact, since I used his `pyQSC` for the
   probe.
2. Egemen Kolemen and the DESC team (Rory Conlin, Dario Panici, Daniel Dudt, Kaya
   Unalmis, Yigit Elmacioglu, and others; Princeton Plasma Control Group /
   `PlasmaControl/DESC`).

---

Across networking, databases, wireless, optical, and power systems I have been
measuring a recurring failure. A system optimizes an aggregate proxy and
certifies success, while the actual downstream consumer, which reads only a
low-rank projection of the state, gets something much worse. The number I report
is the false-clear rate: how often "certified good" is wrong for that consumer.
The stellarator design objective looks like a clean instance. Quasi-symmetry
residuals are an aggregate field-shape proxy, while confinement (neoclassical and
turbulent transport, fast-ion loss) reads a specific projection. The field
already knows these do not coincide, which is why the turbulence-optimized
stellarator thread exists. I would like to make that gap a measured false-clear
rate along an optimization trajectory, with you.

I am writing rather than publishing because my own attempt was inconclusive. I
ran a substrate probe with `pyQSC`. It works, and the tension is visible at the
base configurations: `precise QA` is excellent on quasi-symmetry yet has a
magnetic hill. But the quick prototype settled nothing. Random near-axis
perturbation of quasi-symmetry-good bases only makes the residual and the
consumer move together, at a rank correlation of about 0.85. It does not produce
the tradeoff, because the tradeoff is a directed phenomenon that random sampling
cannot reach. The honest experiment needs a quasi-symmetry optimization
trajectory on SIMSOPT or DESC, driving the residual down while tracking a
transport-grade consumer such as `ε_eff`, a fast-ion loss fraction, or a reduced
turbulent-transport proxy. That is exactly the machinery you built, which is why
this is a collaboration ask and not a paper I can write alone. The faithful
independent check is your transport pipeline.

The study asks two things along a SIMSOPT or DESC quasi-symmetry optimization
run. First, is there a regime where the quasi-symmetry certificate clears, with
the residual below a target, while the transport consumer is already degrading?
That would be a measured false-clear rate. Second, does an alignment scalar
between the optimized-proxy direction and the transport-sensitive direction
predict when proxy optimization tracks the consumer and when it diverges? That
would give a dial for how aligned the metric is. The deliverable is a reframing
plus that quantification, not new plasma physics. If
it is already folded into your objective design, the most valuable outcome is you
telling me where.

What I bring is the measurement discipline: a pre-registration that fixes the
pass and fail bars before the run, the false-clear rate as the reported metric,
and the consumer-relative `tr(P_C·Σ)` reading. I also bring a runnable `qsc`
prototype and the cross-domain context. What I need from you is guidance on the
right transport consumer and a SIMSOPT or DESC optimization trajectory to
instrument. A student project fits well.

The code is shareable now. `observation-theory-campaigns/analysis/stell/` holds
`fam_stell.py`, the `qsc` probe, and `EXPLORATION-STELL.md`, which records the
inconclusive prototype and the directed design. The broader freshness and
consumer-relative work (routing, databases, 5G, optical, grid, AI evaluation)
sits alongside it as evidence the approach is not ad hoc.
