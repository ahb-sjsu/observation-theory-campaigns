# GG Track: Gauge Redundancy as Consumer Bookkeeping

**Status:** design draft, unsealed, non-claim-bearing. Chip 🟤 GG.
Everything is measured in declared exact finite models.

## 1. Question

A gauge orbit is the fiber of a projection, many link
configurations behind one physical state. The EG track found that
constraints source geometry and do not emerge. The inverse question
is whether gauge symmetry is anything but the fiber structure of
the observer's projection. Which quantities are consumer-invariant
across the family of gauge-fixed observers, which gauge-variant
readings are pure consumer bookkeeping, and does the Gauss-law
structure replay in gauge language the way EG-6 measured it.

## 2. Anchors (verified citations to be completed before any seal)

Wegner's Z2 lattice gauge theory, Elitzur's theorem on the
vanishing of gauge-variant expectations, and the exact solvability
of two-dimensional Z2 gauge theory. Each enters as a replication
target or a comparison, never as an inserted answer.

## 3. Anti-circularity contract

No gauge fixing is privileged. Observers (gauge-fixing rules) enter
as a declared family, and any claimed invariance must hold across
the whole family or the claim fails.

## 4. Experiments

### GG-0: Exact gauge-orbit instrument layer

Z2 gauge theory on a 3 by 3 periodic lattice, 18 links, all 2^18
configurations enumerated exactly, plaquette action with K = 0.4.
Protocol declared 2026-08-05, before the run.

C1 orbit structure, for 200 declared seeded configurations, the
action is exactly constant over the full 512-element gauge orbit,
and every orbit size is a power of two dividing 512, sizes
recorded. C2 route agreement and closed form, the single-plaquette
Wilson expectation from full enumeration equals the tree-gauge-fixed
enumeration within 1e-12, and both equal the exact torus closed
form (t + t^8)/(1 + t^9) with t = tanh K within 1e-12. C3
Elitzur control, every single-link expectation vanishes within
1e-13 in the full ensemble, while the declared tree-gauge-fixed
observer assigns some links a nonzero reading, recorded, the
gauge-variant reading is the observer's bookkeeping, not the
substrate's. All three or GG-0 fails. Exploratory label,
results/gg0-instrument.json.

### GG-1: Consumer-invariance across gauge-fixed observers

A declared family of gauge fixings (tree gauges on different trees,
maximal axial slices). Measured, which observables agree across the
whole family within machine precision and which depend on the
observer, with every dependence predicted by the declared fixing.

### GG-2: The Gauss-law replay

EG-6's declared-or-absent gate in gauge language. Measured, whether
the lattice Gauss constraint structure is an isolated algebraic
point under declared deformations of the link ensemble. Either
outcome is a result.

### GG-3: Minimal-coupling audit

A declared matter field coupled to links. Measured, which coupled
observables survive the observer family, and whether charge
appears only as a property of the projection's fibers.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about continuum gauge field
theory.
