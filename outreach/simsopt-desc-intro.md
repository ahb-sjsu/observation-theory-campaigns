# SIMSOPT / DESC outreach — collaborate on XPROTO-STELL

**From:** Andrew H. Bond, Senior Member IEEE (SJSU).
**Re:** a consumer-relative reading of the stellarator design objective — does
optimizing the aggregate quasi-symmetry residual *false-clear* a transport-grade
consumer along the optimization trajectory?
**Status:** DRAFT for the owner to send. Nothing sent. Public methodology; nothing
IP-gated. Two contacts below (use current published addresses / the repos' contact
routes — I have not hard-coded emails).

- **Contact 1 — Matt Landreman** (SIMSOPT lead + `pyQSC` author; U. Maryland /
  hiddenSymmetries). *The natural first contact — I used his `pyQSC` for the probe.*
- **Contact 2 — Egemen Kolemen & the DESC team** (Rory Conlin, Dario Panici, Daniel
  Dudt, Kaya Unalmis, Yigit Elmacioglu, …; Princeton Plasma Control Group /
  `PlasmaControl/DESC`).

---

## The one-paragraph pitch

Across networking, databases, wireless, optical, and power systems I've been
measuring a recurring failure: a system optimizes an **aggregate proxy** and
certifies success, while the **actual downstream consumer** — which reads only a
low-rank projection of the state — gets something much worse. The measured metric is
the *false-clear rate*: how often "certified good" is wrong for the consumer. The
stellarator design objective looks like a clean instance: quasi-symmetry residuals
are an aggregate field-shape proxy, while confinement (neoclassical + turbulent
transport, fast-ion loss) reads a specific projection — and the field already knows
these don't coincide (the "turbulence-optimized stellarator" thread exists for this
reason). I'd like to make that gap a *measured false-clear rate along an optimization
trajectory*, with you.

## Honest status (why I'm writing rather than publishing)

I ran a **substrate probe with `pyQSC`** — it works, and the tension is visible at
the base configs (`precise QA`: QS-excellent yet a magnetic hill). But my quick
**prototype was inconclusive**: random near-axis perturbation of QS-good bases only
produces QS↔consumer *co-variation* (rank-corr ~0.85), not the tradeoff — because
the tradeoff is a **directed** phenomenon that random sampling can't reach. The
honest experiment needs a **QS-optimization trajectory on SIMSOPT or DESC**, driving
the QS residual down while a **transport-grade consumer** (`ε_eff`, or a fast-ion
loss fraction, or a reduced turbulent-transport proxy) is tracked — exactly the
machinery you built. That is why this is a collaboration ask, not a paper I can write
alone: the faithful *witness* is your transport pipeline.

## The concrete study

Along a SIMSOPT/DESC QS-optimization run: (a) is there a regime where the QS
certificate clears (residual below a target) while the transport consumer is
already degrading — a measured false-clear rate? (b) does an **alignment scalar**
between the optimized-proxy direction and the transport-sensitive direction predict
*when* proxy-optimization tracks the consumer vs diverges (a "how-aligned-is-your-
metric" dial)? The deliverable is a reframing + that quantification — not new plasma
physics. If it's already folded into your objective design, the most valuable
outcome is you telling me where.

## What I bring / what I'd need
- **Bring:** the measurement discipline (sealed pre-registration, false-clear rate
  as a first-class KPI, the consumer-relative `tr(P_C·Σ)` framing) + a runnable
  `qsc` prototype and the cross-domain context.
- **Need:** guidance on the right transport consumer + a SIMSOPT/DESC optimization
  trajectory to instrument (a student project fits well).

## Reproducibility hooks (shareable now)
`observation-theory-campaigns/analysis/stell/` — `fam_stell.py` (the `qsc` probe) +
`EXPLORATION-STELL.md` (the honest inconclusive prototype + the directed design). The
broader freshness/consumer-relative program (routing, databases, 5G, optical, grid,
AI-eval) sits alongside as evidence the framing is not ad hoc.
