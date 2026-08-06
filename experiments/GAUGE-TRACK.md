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

#### GG-0 results (run 2026-08-05, record sha ab8594f96c60...)

Verdict PASS, all three items. Every sampled orbit has size exactly
256 with the action exactly constant on it. The single-plaquette
Wilson expectation agrees across the full enumeration, the
tree-gauge-fixed enumeration, and the exact torus closed form to
every printed digit, 0.38032051536830963 on all three routes. The
Elitzur control is exactly zero on every link in the full ensemble,
while the tree-gauge-fixed observer assigns non-tree links a
reading of 0.3803, which is no accident, in tree gauge a non-tree
link equals a Wilson loop through the tree, the observer's
bookkeeping is a gauge-invariant quantity wearing a gauge-variant
label. The instrument for the observer-family experiments is
validated.

### GG-1: Consumer-invariance across gauge-fixed observers

A declared family of gauge fixings (tree gauges on different trees,
maximal axial slices). Measured, which observables agree across the
whole family within machine precision and which depend on the
observer, with every dependence predicted by the declared fixing.

#### GG-1 protocol (declared 2026-08-05, before the run)

The GG-0 substrate unchanged, all 2^18 configurations at K = 0.4.
Three declared spanning-tree observers, each a maximal-tree gauge
slice on a different declared tree. Observables, the nine plaquette
Wilson expectations, a declared area-two loop, and all eighteen
link readings, computed in the full ensemble and on each observer's
slice.

Bars. G1, every gauge-invariant observable agrees between the full
ensemble and every observer's slice within 1e-12. G2, the detector
model is exact, every non-tree link reading of every observer
equals the full-ensemble expectation of the closed loop formed by
that link and its tree path, within 1e-12, and where the GF(2)
plaquette decomposition certifies the loop contractible with
enclosed area A the reading also equals the closed form (t^A +
t^(9-A))/(1 + t^9) within 1e-12, while loops the decomposition
certifies as winding read zero within 1e-13. G3, the observers
measurably disagree on link readings, maximum pairwise difference
at least 0.1, while the full-ensemble Elitzur zero stands. All
three or GG-1 fails. The reading, every observer's gauge-variant
bookkeeping is a relabeled gauge-invariant loop selected by its
declared tree, disagreement between observers is exactly the
difference in which loops their trees select, and nothing any
observer reads is outside the invariant algebra. Exploratory
label, results/gg1-observer-family.json.

### GG-2: The Gauss-law replay

EG-6's declared-or-absent gate in gauge language. Measured, whether
the lattice Gauss constraint structure is an isolated algebraic
point under declared deformations of the link ensemble. Either
outcome is a result.

#### GG-2 protocol (declared 2026-08-06, before the run)

The GG-0 substrate with the deformed weights exp(K sum of
plaquettes + epsilon sum of links), epsilon on the declared ladder
0, 1e-3, 1e-2, 1e-1, all 2^18 configurations enumerated at each
point, expectations by exact summation.

Bars. W1, at epsilon zero the GG-0 zeros replicate, every link
expectation within 1e-13 and the action exactly constant on
sampled orbits. W2, detectability at first order, at every
positive epsilon the maximum link expectation is at least 0.3
epsilon and the deformed action is strictly non-constant on every
sampled generic orbit, the broken constraint is visible at machine
precision immediately, not asymptotically. W3, sector split of the
response, the link expectation's log-log slope between epsilon
1e-3 and 1e-2 lies in [0.8, 1.2] while the plaquette expectation's
shift has log-log slope in [1.5, 2.5], the gauge-variant sector
responds at first order and the invariant sector only at second.
The reading, the EG-6 result in gauge language, constraint
structure is an isolated algebraic point, declared or absent, with
no approximately-gauge ensemble in between, and the observer that
watches invariants is second-order blind to the breaking that the
link sector shouts. Exploratory label,
results/gg2-gauss-replay.json.

#### GG-2 results (run 2026-08-06, record sha in the record)

Verdict FAIL on W3, and the failure is the declaration
underestimating the substrate's silence. W1 and W2 passed, the
zero point exact, every positive epsilon first-order loud in the
link sector with response slope 1.0000, every sampled orbit
strictly non-constant. The declared plaquette window [1.5, 2.5]
assumed a generic quadratic response, but the measured slope is
4.000003. The quadratic channel is closed exactly, at second order
the deformation enters through pairs of links, and no two links
form a closed loop with a plaquette on this graph, so the epsilon
squared coefficient vanishes identically and the first surviving
response is quartic, four deformation links closing a loop. The
invariant sector is not second-order blind, it is fourth-order
blind.

#### GG-2b protocol (declared 2026-08-06, before the run)

Identical to GG-2 except W3's plaquette window, now [3.5, 4.5],
with the loop-parity argument above as the declared prediction.
The named error, GG-2's window assumed a generic response the loop
structure forbids. Exploratory label,
results/gg2b-gauss-replay.json.

#### GG-2b results (run 2026-08-06, record sha d3f7b17776ac...)

Verdict PASS, all three items. The zero point exact, the link
sector first-order loud with response slope 1.0000, every sampled
orbit strictly non-constant at every positive epsilon, and the
plaquette response slope 4.000003 inside the corrected window with
the loop-parity prediction standing. The EG-6 result in gauge
language is measured, constraint structure is an isolated
algebraic point, declared or absent, with no approximately-gauge
ensemble in between, and the observer that watches only invariants
is fourth-order blind to a breaking the link sector announces at
first order.

### GG-3: Minimal-coupling audit

A declared matter field coupled to links. Measured, which coupled
observables survive the observer family, and whether charge
appears only as a property of the projection's fibers.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is a claim about continuum gauge field
theory.
