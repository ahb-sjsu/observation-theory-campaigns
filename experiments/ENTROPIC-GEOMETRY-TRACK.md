# EG Track: Entropic Geometry from Singular Projections

**Status:** design draft, unsealed, non-claim-bearing. No physics claims are
made anywhere in this document. Every quantitative statement below is either
a citation, a definition, or a target for a future sealed run.

## 1. Question

Can spacetime geometry be reconstructed as the information geometry of a
singular projection, with gravity arising from matter-induced changes in the
distinguishability of hidden states?

Concretely: if an observer sees X = pi(Z) for hidden state Z, the fibers
pi^{-1}(x) carry an entropy field. Matter, modeled as a local deformation of
the hidden dynamics or hidden-state density, deforms the fiber measure. The
question is whether the induced gradients of distinguishability can play the
role of a gravitational potential, with the Newtonian Poisson equation
nabla^2 Phi = 4 pi G rho as the pilot target, without inserting that
structure anywhere in the model.

The track separates three claims that must not be conflated:

1. **Instrument claim:** fiber entropy, conditional entropy, and relative
entropy of fiber measures can be measured correctly at finite resolution.
This extends the PE track and is testable now.
2. **Structural claim:** some declarable projection geometry yields area-law
state counting, inverse-square attraction, universal coupling, and
conservation identities, none of them inserted. This is the campaign.
3. **Physical claim:** real gravity is such a projection. Nothing in this
track can support this claim and no run will be labeled as doing so.

## 2. Context: the entropic-gravity lineage

All four works below are theoretical proposals or derivations. None is an
experimental result. Each derives gravitational field equations FROM assumed
thermodynamic or information-theoretic inputs; none derives those inputs from
an independently specified microscopic substrate, which is exactly the gap
this track's constructive route targets.

**T. Jacobson, "Thermodynamics of Spacetime: The Einstein Equation of
State", arXiv:gr-qc/9504004 (v2, June 1995), Phys. Rev. Lett. 75, 1260-1263
(1995).** The lineage root. Demands that the Clausius relation
delta Q = T delta S hold for all local Rindler causal horizons, with
delta Q the energy flux and T the Unruh temperature seen by an accelerated
observer, and derives the Einstein equation as an equation of state. What it
establishes: Einstein dynamics follows from entropy proportional to horizon
area plus the Clausius relation. What it does not establish: why entropy is
proportional to area, what the microscopic states are, or what physical
system the entropy is the entropy of. The proportionality S ~ A is an input.

**G. Bianconi, "Gravity from entropy", arXiv:2408.14391 (v1 26 Aug 2024
through v7 8 Feb 2025), Phys. Rev. D 111, 066001 (2025).** Postulates an
entropic action given by the quantum relative entropy between the spacetime
metric, treated as an operator playing the role of an effective density
matrix, and a metric induced by matter fields in a topological
(Dirac-Kahler) representation. The modified Einstein equations reduce to the
standard ones with zero cosmological constant at low coupling, and an
auxiliary G-field acting as Lagrange multipliers yields an emergent small
positive cosmological constant. What it establishes: a self-consistent
action of relative-entropy form whose weak-coupling limit is Einstein
gravity. What it does not establish: the action is postulated, not derived;
there is no microscopic ensemble whose coarse-graining produces the density
matrices; there is no falsifiable prediction tested against data in the
paper.

**P. Dorau and A. Much, "From Quantum Relative Entropy to the Semiclassical
Einstein Equations", arXiv:2510.24491 (v1 28 Oct 2025, v3 3 Mar 2026),
listed journal reference Phys. Rev. Lett. 136, 091602 (2026).** Uses
Tomita-Takesaki modular theory to show that the relative entropy between the
vacuum and coherent excitations of a scalar quantum field on a bifurcate
Killing horizon equals the energy flux across the horizon; combined with the
Bekenstein-Hawking entropy-area formula this yields the semiclassical
Einstein equations, refining Jacobson by replacing classical thermodynamic
entropy with quantum relative entropy for a specific state class. What it
establishes: the flux-entropy equality is a theorem of modular theory for
that state class and geometry. What it does not establish: the
Bekenstein-Hawking formula is still an input, the state class is special,
and a Killing horizon is assumed rather than emergent.

**A. Alonso-Serrano, L. J. Garay, M. Liska, C. Lopez Pineros, "Gravity from
equilibrium thermodynamics of stretched light cones", arXiv:2509.08566 (v1
10 Sep 2025, v4 24 Feb 2026), Phys. Rev. D 112, 124026 (2025), DOI
10.1103/y9rz-b88v.** Studies stretched light cones of uniformly accelerating
observers, computes their expansion, shear, and vorticity, and shows the
shear vanishes so the analysis can be carried out entirely in equilibrium
thermodynamics; energy balance plus the Clausius relation then encodes the
gravitational dynamics. What it establishes: the Jacobson-type argument can
be run on a different, shear-free local structure without non-equilibrium
entropy production terms. What it does not establish: same as Jacobson; the
entropy-area proportionality and the Unruh temperature are inputs.

Two standing caveats govern how this track reads the entire lineage:

**Entropy is a functional, not a substance.** Entropy is a property of a
state (or ensemble) together with a coarse-graining. "Gravity from entropy"
is meaningless until the state, the coarse-graining, and the observer are
specified. In this track all three are explicit: the hidden ensemble, the
projection pi with resolutions (delta, epsilon), and the declared fiber
measure.

**The reverse-engineering caveat.** For any potential V(x) one can define
S(x) = -V(x)/T and observe that F = -grad V = T grad S. This is a renaming,
not an explanation. Any "entropic force" account that selects its entropy
function to match a known potential has zero content. An entropic derivation
earns content only when the entropy is computed from an independently
specified state and coarse-graining, and the force law then follows without
having been inserted. The anti-circularity contract in section 4 is the
enforcement of this caveat, and EG-2 includes an explicit audit for
potential-equivalent inputs.

## 3. Projection-entropy objects

The objects are those of the PE track (ENTROPY-TRACK.md), extended by a
relative-entropy comparison between deformed and undeformed ensembles:

- hidden state Z in a smooth manifold M, with a declared reference ensemble
(the "vacuum" ensemble) and declared local dynamics;
- observation map pi: M -> observed space, X = pi(Z);
- the fiber pi^{-1}(x) of hidden states compatible with one observation;
- the fiber entropy S_pi(x) = k_B ln mu(pi^{-1}(x)) for a fiber measure mu
declared before any claim-bearing run;
- the conditional entropy H(Z_delta | X_epsilon) at finite hidden resolution
delta and finite observed resolution epsilon;
- the relative entropy D(mu_matter(x) || mu_vac(x)) between the
matter-deformed and vacuum fiber measures at each observed point.

The finite-resolution formulation is mandatory, not optional. Continuous
conditional entropy under a deterministic projection has coordinate
pathologies near singularities, and differential entropy is not
reparametrization invariant; a claimed entropy gradient that changes sign
under a hidden-coordinate change is an artifact, not a force. Every EG
witness is defined at stated (delta, epsilon) and must converge as both are
refined, exactly as the PE-1 convergence slice already demonstrates for the
fold caustic.

The candidate geometric object is an effective line element built from
distinguishability: the distance between nearby observed points x and x' is
measured by how distinguishable their fiber-conditional distributions are
(a Fisher-information or relative-entropy quadratic form on the family
mu(.|x)). Whether this object behaves like a metric at all, and whether
matter deformations curve it the right way, is what the campaign tests. It
is not assumed.

## 4. The decisive derivation chain and its anti-circularity contract

A claim-bearing EG result must traverse this chain in one direction only:

```text
Level 0: hidden manifold M, local dynamics, projection pi,
         fiber measure mu, vacuum ensemble
              |
Level 1: fiber entropy S_pi(x); relative entropy of
         matter-deformed versus vacuum fibers
              |
Level 2: effective metric from distinguishability;
         area law for boundary state counting
              |
Level 3: dynamics: Newtonian limit nabla^2 Phi = 4 pi G rho
         as pilot target; Einstein-like structure beyond
```

Everything at Level 0 is frozen before the claim-bearing sweep. Everything
at Levels 1-3 is measured, never adjusted. If the gravitational equation, or
any consequence of it, is used to select or tune the fiber measure, the run
is void. This is the EG analogue of the CAMPAIGN.md section 3 contract, and
the forbidden-input list mirrors it:

- a command or fitted term producing attraction, area scaling, or the
Poisson equation at the desired strength;
- any 1/r potential, 1/r^2 force, or their equivalents inserted into the
hidden dynamics, the projection, the fiber measure, or the source model;
- the Bekenstein-Hawking coefficient, or any entropy-area proportionality,
as an input rather than a measured output;
- an entropy function chosen after inspecting which choice reproduces a
target potential (the reverse-engineering caveat as a contract clause);
- a temperature defined from the first law it is later used to verify;
- postselection on regions, sources, or configurations that exhibit
attraction, area scaling, or the desired sign;
- coarse-graining or resolution choices made after examining their effect
on the witnesses;
- loss functions fitted to any target law on the parameter range used for
evaluation;
- observer-specific coordinate choices that are not transformed with the
observer.

The model may contain: local hidden fields and dynamics, a projection, a
declared fiber measure, a declared detector model for temperature, and a
source distribution, all fixed before the claim-bearing sweep.

## 5. The area-law gate

This is EG's first major gate and the expected point of failure.

Generic hidden multiplicity scales with volume. For a generic projection
and a generic ensemble, the number of independently distinguishable hidden
states associated with an observed region of linear size R scales as R^3
(in three observed dimensions), so S(R) ~ R^3. Every entropic account of
gravity in the lineage above requires boundary scaling, S(R) ~ R^2. The
framework becomes relevant to gravity only if some declarable projection
geometry makes the independently distinguishable states associated with a
region scale with its boundary area, and does so for a structural reason
that is itself not inserted.

Candidate mechanisms to be formalized and tested, each as a concrete
Level-0 construction:

- **Gauge redundancy.** Interior hidden states are identified under a
declared symmetry group; only the quotient is counted. Area scaling would
require the quotient's independent labels to live on the boundary.
- **Equivalence-related fibers.** Distinct fibers over interior points are
related by hidden-dynamics equivalences, so joint multiplicity is not the
product of fiber multiplicities.
- **Error-correcting encodings.** Interior information is redundantly
encoded across the region, so the number of independent logical states is
set by a boundary-sized code, not the physical volume.
- **Boundary-limited access.** The observation map reads the interior only
through boundary data. This must create a genuine distinguishability
limit in the declared ensemble, not merely an access inconvenience.
- **Projection rank constraints.** The rank of d(pi) restricted to the
region limits the number of independent observed directions.
- **Long-range correlation.** Interior states are correlated strongly
enough that joint entropy is subextensive.
- **Interior conservation links.** Constraints of Gauss-law type tie
interior configurations to boundary fluxes, removing interior
independence.

Standing warning: volume concentration near a boundary is NOT sufficient. A
measure concentrated in a shell near the boundary still counts
volume-independent distinctions unless the interior distinctions are
genuinely non-independent; a thin shell of thickness delta contributes
R^2 * delta / delta^3 states at resolution delta, which is still a
volume law in disguise as delta -> 0. The gate is about independence of
distinctions, not about where the measure sits.

A clean negative at this gate, a proof or measured demonstration that a
declared mechanism class cannot produce area scaling, is a publishable
result and the expected one.

## 6. Experiments

### EG-0: Projection entropy instrumentation — IMPLEMENTED, PASSING (exploratory)

**Question.** Do the finite-resolution entropy instruments measure
H(Z_delta | X_epsilon) and the relative entropy between matter-deformed and
vacuum fiber measures correctly?

**RESULTS (runner `python/eg0_instrument.py`, evidence
`results/eg0-instrument.json`).** All four parts pass on exact closed
forms. Part A reproduces the PE-0 values, the fold's branch bit to
1.4e-14, the double-fold symmetric slice at exactly 1.5 bits, the
degenerate cubic at exactly zero, and the caustic limit to 1.4e-3 at
epsilon 1e-5. Part B measures the conditional-entropy surface, the
aligned linear control equals log2(100) to 1e-12 with no error term,
and both resolution sweeps converge (successive-deviation ratios 6.2x
in delta, 1.4x in epsilon). Part C measures fiber relative entropy,
nested uniforms exact at 2 bits, the Gaussian control within 1.75e-10
of the closed-form KL with the floor identified as range truncation by
a widening control (drops below 1e-12 at 14 sigma), and the
piecewise-deformed fold's per-bin D equal to the binary divergence
closed form to 3.3e-16 across all 90 interior bins. Part D verifies
reparametrization invariance, exact under relabeling (8e-16) and at
the rounding floor under Jacobian-weighted re-gridding (8.2e-16,
shrinking to 4.4e-16 at quarter resolution).

**Sealing status.** Unsealed. The substrate clause requires MATLAB
replication before EG-0 seals; the Python layer is the reference
implementation. Open question 7 of section 10 is resolved, PE-2 and
the full PE track are measured, so the sequencing dependency is
satisfied rather than relaxed.

**Method.** Extend the PE-0 instrument (`pf.fiber_entropy` in MATLAB,
`fiber_branch_weights` / `branch_entropy_bits` in Python, exercised by
`run_pe0_entropy_controls.m` and pytest) with: (a) the full
H(Z_delta | X_epsilon) surface on the analytic control net; (b) relative
entropy D(mu_1 || mu_2) on control pairs with closed-form values (shifted
and scaled uniform fibers, Gaussian fibers with known KL divergence, the
exact fold with a declared deformation); (c) convergence sweeps in delta
and epsilon. Every EG-0 target must first reproduce the already-passing
PE-0 closed-form values (P0 one bit, M0 1.5 bits at the symmetric slice,
band-edge limit, N0/D0 zero) before any new target is evaluated.

**Primary witnesses.** Conditional-entropy error against closed form,
relative-entropy error against closed form, convergence order in delta and
epsilon, cross-language agreement, invariance of all witnesses under
declared hidden-coordinate reparametrization.

**Falsification bar.** Any disagreement with a closed-form value beyond
the sealed tolerance, any witness that fails to converge under resolution
refinement, or any witness that changes under hidden reparametrization
invalidates the instrument. No later EG experiment may run until EG-0 is
sealed and passing.

**Substrate.** MATLAB on Atlas with Python replication, exactly as PF-0.

---

### EG-1: Area-versus-volume scaling test — IMPLEMENTED, MEASURED (exploratory); GATE NEGATIVE IN THE PRIMARY COUNT

**Question.** For each candidate mechanism in section 5, does the measured
entropy of the independently distinguishable states associated with a
region of size R scale as R^3 or as R^2?

**RESULTS (runner `python/eg1_area_gate.py`, evidence
`results/eg1-area-gate.json`; two-dimensional lattices, so volume
means R^2 and area means R^1; R from 3 to 301, two full decades,
every count exact with closed forms reproduced at every R).**

Three arms under the section 10 counts decision. The generic
independent-spin control counts (R-2)^2 given the boundary with zero
cut mutual information, volume as guaranteed. The Gauss-law
constraint and gauge-quotient mechanisms, realized as the uniform
ensemble over the Z2 cycle space of torus edge configurations (both
mechanism classes share this count), give exactly (R-1)^2 interior
distinctions given the boundary, a volume law, so the two most
concrete constraint mechanisms FAIL the gate in the primary count.
Boundary-limited access leaves the hidden interior residual a volume
law (R-2)^2 while only the observer-accessible image is area-scaling
(4R-4) by construction, which is section 5's standing warning made
quantitative, an access limit is not a distinguishability limit.

The finding beyond the negative. The same Gauss-law ensemble carries
an exact area-law cut mutual information, I(region ; complement) =
4R-5, while its interior count stays extensive. The counts split
exactly as the section 10 decision anticipated, constraint structure
does put area scaling into observer-relative correlations while
leaving interior independence extensive. Any entropic-gravity reading
built on this mechanism class would have to live on the correlation
count, which the decision relegated to secondary, and would have to
justify that choice against the independence requirement the gate is
about.

Fitted free slopes over the full range: primary counts 2.13 to 2.33
(classified volume against the fixed alternatives), mutual
information and access image 1.09 and 1.07 (classified area).

**Standing per the falsification bar.** The measured mechanism
classes fail the gate; the negative classification stands for them.
The remaining section 5 candidates (error-correcting encodings with a
structural rather than inserted origin, subextensive long-range
correlation, projection rank constraints) are not yet constructed and
the gate stays open for them. The track continues only if some future
declared mechanism passes the primary count without insertion.

### EG-1b: Mechanism discovery — CAUSAL DETERMINISM PASSES (exploratory)

Runner `python/eg1b_mechanism.py`, evidence
`results/eg1b-mechanism.json`. The discovery effort was theory-first,
and both theory pieces were recorded before the run.

**Entropy-density lemma (proved).** For a translation-invariant
ensemble with entropy density h, the chain rule gives
H(interior | boundary) >= H(region) - H(boundary) >= h R^2 - c R.
An area-law primary count therefore forces h = 0. This makes the
EG-1 negatives structural rather than accidental, every mechanism
class with positive bulk entropy density fails before construction,
and it directs the search to zero-density ensembles with
boundary-sized residual freedom.

**Causal-cone bound (proved).** The natural non-inserted origin of
zero density is deterministic local dynamics with the region read as
a spacetime region, per the section 10 corollary decision. For any
deterministic radius-one rule, an R x R spacetime patch is a function
of its causal-cone data of 3R-2 cells, so H(patch) <= 3R-2, perimeter
scaling for ANY such rule and any initial ensemble, and the top row
and side columns determine the interior by induction, so
H(interior | boundary) is exactly zero.

**Measured.** Additive rules 90 and 150 with i.i.d. uniform initial
data, every entropy an exact GF(2) rank, R over two decades (3 to
301): H(patch) = 3R-2 EXACTLY at every R, the cone bound is
saturated, and H(interior | boundary) = 0 exactly at every R. The
nonlinear rule 110 by exact enumeration at R = 3, 4, 5 gives 5.04,
6.97, 8.85 bits, inside the bound, rule-independence witnessed. The
structural-origin audit, the same rule 90 construction with one
fresh noise bit per cell per step, gives H(patch) = R^2 exactly at
every measured R, free-fit slope 2.0000, a volume law. The area law
tracks determinism and nothing tuned. Insertion audit, the rules are
generic and untuned, the bound is causality itself, no area-sized
structure, potential, or code is declared anywhere.

**Reading.** Causal determinism is an area-law mechanism for
spacetime regions, and it is destroyed by any bulk entropy
production. Within this model class the gate's requirement selects
exactly the ensembles with zero entropy production, which is the
structural feature the thermodynamic gravity literature assumes when
it works on causal horizons. The reframing is declared honestly, the
passing region is a spacetime region, not a spatial one, and the
spatial-region negative of EG-1 stands unchanged.

**Gate standing after EG-1b.** EG-2 through EG-5 are conditionally
unblocked on the causal-determinism substrate, meaning designs may
now use deterministic local hidden dynamics with spacetime regions
and must carry the noise-audit control in every claim-bearing run.

### EG-2 RESULTS on the causal substrate — MEASURED (exploratory)

Runner `python/eg2_matter.py`, machinery `python/eg_ca_substrate.py`,
evidence `results/eg2-matter.json`. On the linear substrate every
window marginal is uniform on an image subspace, so the deformation
field is exact subspace arithmetic, classified equal, nested (finite
D in bits), or escaped (infinite D, support left the vacuum's).

Matter is a rule substitution, cells of a declared source use rule
150 in a rule 90 vacuum, sizes 1, 3, 5, 7 cells. The
reverse-engineering audit is structural, a positive reweighting
cannot move the support of a uniform-on-subspace measure while a
rule substitution does, so the source class is not
potential-equivalent by construction.

Findings, all exact. Causality null, every window outside the defect
cone carries the identical subspace, asserted. Local invisibility,
every single cell and every two-by-two patch inside the cone, and
every row segment up to length 64 at every position, is EXACTLY equal
to vacuum for every source, matter has no local field on this
substrate. Visibility onset, sources of width 1, 5, and 7 stay equal
at every proper segment up to length 256 and escape support only at
the closed ring (the defect frees the parity constraint rule 90
imposes, one global all-or-nothing bit). The width-3 source is the
exception, a rank-losing sink destroying exactly one bit per step
(global deficit 60 = T), which generates the only finite
distinguishability field, nested D values appearing from window
length 160, growing about half a bit per cell, and positioned in a
period-64 self-similar pattern (profile 3, 7, 11, 9, 5, 1 repeating)
set by the automaton's algebra, not by distance from the source.

### EG-3 RESULTS, the local first law — MEASURED, PASSING (exploratory)

Runner `python/eg3_first_law.py`, evidence
`results/eg3-first-law.json`. The three quantities are independent by
construction. delta Q counts declared noise injections inside the
spacetime patch, event bookkeeping with no entropy. T is the patch
response to one training injection, measured once, frozen at exactly
one bit per event. delta S is an exact rank difference.

A structural fact shapes the accounting and is itself a finding.
An injection BEFORE the patch's time span is absorbed exactly, the
uniform ensemble is already maximal on every reachable set, so
time-slice detectors are blind and only events inside the region
drive its entropy. Held-out, dilute, moderate, and stacked interior
patterns satisfy delta S = T delta Q EXACTLY (residual zero to
rounding), the all-past pattern gives delta S = 0 against a positive
naive flux, and the mixed pattern holds with inside-only accounting
while the all-events accounting overpredicts, asserted. The vacuum
patch entropy is 120 bits, exactly the perimeter form. On this
substrate the Clausius relation is an output once the flux is the one
crossing into the region, which is the ordering the thermodynamic
gravity literature assumes rather than derives.

### EG-4 RESULTS, the geometric equations — MEASURED, NEWTONIAN LIMIT REJECTED (exploratory)

Runner `python/eg4_geometry.py`, evidence
`results/eg4-geometry.json`. The candidate potential is the EG-2
field of the width-3 sink, the only field-bearing source class.

Item verdicts. Poisson FAILS, the field's discrete Laplacian is as
large far from the source as at it. Gauss FAILS, no monotone flank
exists to carry a flux reading. Superposition FAILS, and not by mere
nonlinearity, the deficits interfere destructively, two separated
width-3 sinks give a global deficit of ZERO at both tested
separations against the additive expectation of 120, and three sinks
give 1, so matter deficits compose by GF(2) algebra, not by
addition. Linearity FAILS with them. The interior item is
unevaluable, both between-source and far windows classify equal.

The sink law itself holds, each isolated sink loses exactly one bit
per step at either tested position.

### EG-4b DISCOVERY CAMPAIGN — declared before any run, 2026-08-05

Goal, get past the EG-4 bar without insertion. Diagnosis of the EG-4
failure, recorded first. The local invisibility of matter came from
the MAXIMAL vacuum ensemble, not from determinism, since an i.i.d.
uniform initial row makes every local marginal full-entropy and
leaves nothing local to distinguish, while the causal-cone bound and
the first law are ensemble-independent. The GF(2) composition of
deficits came from subspace dimension being the only measurable
quantity in the uniform case.

Declared direction. Keep the deterministic dynamics (preserving the
EG-1b area mechanism and the EG-3 first law), and give the vacuum a
structured initial ensemble, product Bernoulli with a declared bias.
Window distributions are then exactly computable by Walsh analysis,
each XOR combination of window functionals has expectation
(1-2p)^(support size), so every field value is an exact
Kullback-Leibler divergence, no sampling. The relative-entropy field
becomes real-valued and smooth in the perturbation, and
Kullback-Leibler additivity for weak independent perturbations is
exactly the weak-field regime the EG-4 superposition and linearity
items are stated in.

Declared probes and bars. Instrument control, the Walsh window
distribution must match brute-force enumeration on a small case to
1e-12 before any field is read. Causality null exact. Field
existence and gradedness, measured profile. Source-strength
linearity, deviation of the field from linearity in a declared
duration knob must shrink as the source weakens. Weak-field
superposition, the two-source field against the sum of single-source
fields, deviation must shrink as the sources weaken. Poisson and
Gauss forms evaluated on whatever profile is measured, with
data-driven verdicts written after measurement, never before. The
insertion audit is unchanged, sources are rule substitutions, no
potential or distance function anywhere, and the anti-circularity
contract applies.

**RESULTS after three rounds (runner `python/eg4b_discovery.py`,
evidence `results/eg4b-discovery.json`; instrument validated against
enumeration to 8.3e-17; causality null exact with the ring wrap
accounted for).**

Round one, the structured vacuum removes the invisibility
obstruction. With Bernoulli bias 0.2 initial data, a single
rule-substitution source produces a genuinely graded real-valued
field, a plateau of 0.812 bits inside the cone with smooth symmetric
monotone flanks rising over about eight cells, against exactly zero
everywhere on the maximal vacuum of EG-2. Two of the declared items
pass immediately, gradedness and monotone Gauss flanks. Two fail
informatively. The discrete Laplacian concentrates on the CAUSAL
FRONT, not at the source, and the superposition deviation (3.6 to
6.3 percent) does not shrink as the source weakens, because a rule
substitution is a quantized order-one perturbation, there is no
continuous weak-field knob in GF(2).

Round two, the ring has no static limit. With the source left on
until the front wraps and self-collides, the profile flattens to a
near-uniform 0.226 bits (spread 3.6 percent) and keeps drifting
between late times (23 percent), so the round-one gradient was
entirely front-borne.

Round three, escape to infinity yields exact statics, but flat. On a
lattice too large for any wrap, the near-source profile CONVERGES
EXACTLY under time doubling (relative changes 1.0e-3 then 0.0), a
true static limit reached by radiating the transient away, which is
how a reversible system relaxes without entropy production and
without harming the area law. The converged static field is flat,
0.812 bits at every scanned offset with a single point-like bump at
the source, spread 5.3 percent, no spatial gradient.

**Campaign verdict.** The EG-4 bar is not passed, and the obstruction
chain is now fully mapped. Local invisibility was an artifact of the
maximal vacuum and is removed by ensemble structure. The absence of a
static limit was an artifact of the closed ring and is removed by
escape to infinity. What remains is structural and twofold, the
static distinguishability field of this substrate class carries no
spatial gradient (all gradient is radiative, living on causal
fronts), and GF(2) dynamics admits no continuous weak-field
parameter. A substrate passing EG-4 would need a static response
with spatial structure, which points at higher dimension, richer
alphabets, or dynamics with a conserved charge coupling the vacuum
to the source at a distance, each of which leaves the
exact-instrument regime and would require sampling-based
preregistered runs. The campaign closes with two obstructions
removed, one precisely located, and the bar intact.

### EG-4c MINI-CAMPAIGN — declared before any run, 2026-08-05

Hypothesis, falsifiable and declared first. The flat statics of
EG-4b are a one-dimensional artifact. In one dimension radiation
does not dilute, flux conservation forces constant amplitude, so the
radiation passing any point looks the same at every distance and the
converged static field is flat. In two dimensions radiation dilutes
geometrically, so a distance-graded static response can arise from
geometry alone, and distance itself becomes a continuous weak-field
knob, attacking the GF(2) quantization obstruction as well. The
hypothesis fails if the two-dimensional static profile is again flat
or carries no monotone distance dependence.

Substrate, still exact. The two-dimensional XOR rule (each cell
becomes the XOR of its four von Neumann neighbors) is linear over
GF(2), the defect rule adds the cell's own value at declared source
sites, the initial ensemble is product Bernoulli with declared bias,
and every window distribution is exact Walsh analysis with
functionals computed by backward (adjoint) evolution, which for this
symmetric rule has the same form as the forward rule. No sampling
anywhere.

Declared probes. Instrument control against brute-force enumeration
on a small two-dimensional case. Causality null exact. Static
profile along an axis at two doubling times, with convergence and
gradedness both required for the hypothesis. Isotropy, the axis
profile against the diagonal profile at matched distances, since the
von Neumann neighborhood may imprint its anisotropy. Superposition
against source separation, with the deviation required to decay with
distance if dilution is the true weak-field knob. Two-dimensional
Poisson and Gauss forms on whatever profile is measured. All
verdicts computed from the numbers after measurement.

**ROUND 1 RESULT (runner `python/eg4c_mini.py`, evidence
`results/eg4c-mini.json`).** The dimensional-dilution hypothesis is
REFUTED. The two-dimensional axis profile is flat again (0.0611 bits
at every distance, spread 7e-6), the diagonal shows only parity
oscillation, and superposition deviations sit at one half of scale
at every separation. The refutation sharpens the obstruction, it is
not dimension but the finite field itself. Influence under GF(2)
linear rules is parity path-counting, zero or one and never small,
so no finite-field linear substrate can dilute with distance in any
dimension. Geometric dilution requires amplitudes that decay.

**ROUND 2 DECLARATION, before any run.** Real amplitudes with a
Gaussian vacuum, still exact. The substrate is the two-dimensional
discrete wave equation (leapfrog, reversible, deterministic, local,
linear over the reals, site stiffness kappa 0.2), the vacuum is
i.i.d. standard Gaussian initial data, and matter is an impedance
defect, a site whose stiffness is 0.4, a rule substitution with no
potential anywhere. Window marginals are exactly computable
Gaussians, functionals by adjoint evolution, covariances by dot
products, divergences by the closed Gaussian form. The physics
motivation is declared openly, the static limit of the wave equation
is the Poisson equation, so if the distinguishability field tracks
the static response this is the substrate where the Poisson item has
its best chance. Probes mirror round one, causality null exact
(unit wave speed), static profile at doubling times with escape to
infinity, gradedness and monotone decay, superposition against
separation, Poisson localization. Verdicts from the numbers.

### EG-5 GATE — MAY NOT RUN; the arc closes

The EG-5 design forbids the benchmark unless EG-1 through EG-4
passed. EG-4 rejects the Newtonian limit, so EG-5 does not run, and
running a black-hole analogy on top of a failed geometry is forbidden
by construction. The track's arc is complete and its shape is this.
The area gate is passable only by causal determinism (EG-1b). On
that substrate a genuine first law holds with independently defined
flux, temperature, and entropy (EG-3). But the same determinism that
buys the area law and the first law makes matter locally invisible
(EG-2) and gives the only surviving distinguishability field an
algebraic, non-additive, non-Poisson structure (EG-4). Within this
model class the two halves of the entropic-gravity program pull in
opposite directions, the counting half wants zero entropy production
and the geometry half wants a graded local field that zero entropy
production forbids. That tension, stated exactly and measured
exactly, is the campaign's result for this track. Nothing in it
bears on physical gravity.

**Method.** Implement each mechanism as a concrete Level-0 construction.
Measure S(R) at fixed (delta, epsilon) over at least two decades of R, then
repeat at refined resolutions to separate genuine scaling from resolution
artifacts. Fit the exponent against preregistered alternatives: exponent 3,
exponent 2, free power law, and a penalized spline.

**Primary witnesses.** Fitted scaling exponent with confidence interval,
residual structure, exponent stability under resolution refinement,
mechanism-by-mechanism classification.

**Falsification bar.** For any mechanism, a measured volume law where the
framework requires an area law fails that mechanism immediately; if all
declared mechanisms fail, the gravity relevance of the whole track fails at
this gate and the campaign result is the negative classification. An
apparent area law that drifts toward volume under resolution refinement is
classified as a resolution artifact, not a pass.

**Substrate.** MATLAB on Atlas for pilots and reduction; NRP CPU ensembles
for the scaling sweeps.

---

### EG-2: Matter deformation

**Question.** Does a local source, with NO inserted radial potential
anywhere in the model, deform the fiber measure so that the induced drift
on coarse variables has acceleration a(r) ~ -M/r^2?

**Method.** Declare a local source as a bounded modification of the hidden
dynamics or hidden-state density, verified by audit to contain no radial
potential or its equivalent. Compute the deformed fiber measure and the
relative-entropy field D(mu_matter(x) || mu_vac(x)). Derive the drift of
coarse observables from the coarse-grained hidden dynamics alone, with any
mobility or temperature factor declared at Level 0. Fit a(r) against r over
the accessible range, for several source strengths M.

**Reverse-engineering audit (mandatory).** Before the claim-bearing sweep,
run the declared source through an equivalence check: if the source's
effect on the fiber measure can be written as mu_matter = mu_vac *
exp(-V(x)/T) for some radial V equal to the target potential up to fit
tolerance, and V was expressible from the source parameters without
running the dynamics, the construction is potential-equivalent and the run
is void under section 4.

**Primary witnesses.** Log-log slope of |a| versus r (target -2), sign of
the drift (attraction), linearity in source strength, angular isotropy,
stability of all four under matched changes of coarse-graining, resolution,
and integrator.

**Falsification bar.** A slope excluding -2, repulsion, nonlinearity in M
in the weak-source regime, or a drift that appears or disappears under
matched resolution or coarse-graining changes rejects the mechanism. A
positive that fails the reverse-engineering audit is void, not positive.

**Substrate.** MATLAB on Atlas for exact small-N analytics; NRP for
ensemble estimation of the deformed measure.

---

### EG-3: Local first-law test

**Question.** Does delta Q = T delta S hold locally with flux, temperature,
and entropy each defined independently?

**Method.** Define delta Q from the conservation law of the hidden
dynamics (the same accounting discipline as PF-5). Define T from a declared
detector or fluctuation-response model that makes no reference to the first
law (the EG analogue of an Unruh-type response, fixed at Level 0). Define
delta S from the EG-0 instrument. Drive controlled quasi-static
deformations and compare the three independently measured quantities.

**Primary witnesses.** The residual delta Q - T delta S relative to each
term; an independence audit certifying that each of the three quantities
was computed without reference to the other two; residual behavior under
deformation-rate refinement (quasi-static limit).

**Falsification bar.** If the relation holds only when T is defined as
delta Q / delta S, the test is circular and void. A residual beyond the
sealed bar in the quasi-static limit rejects the thermodynamic reading of
the fiber entropy. This gate mirrors the role the Clausius relation plays
as an INPUT in Jacobson 1995 and arXiv:2509.08566; here it must be an
OUTPUT or the chain stops.

**Substrate.** MATLAB on Atlas.

---

### EG-4: Geometric equation test

**Question.** Does the induced potential satisfy the Poisson equation and
its structural consequences, none of which were inserted?

**Method.** Take the potential Phi measured in EG-2-class runs. Calibrate
the single constant G_eff once, on a training region only. Then test, on
held-out configurations:

1. Poisson: nabla^2 Phi = 4 pi G_eff rho pointwise within bars;
2. Gauss law: flux of the measured field through closed surfaces equals
4 pi G_eff times enclosed source, surface-shape independent;
3. shell theorem: a uniform shell produces null interior force and
exterior force equal to the point-source equivalent;
4. superposition: two weak sources produce the sum of their individual
fields within the weak-field bar;
5. equivalence principle: test states of different internal structure and
composition fall with the same acceleration;
6. conservation identities: source accounting and field-flux consistency
under time-dependent rearrangement of sources.

**Primary witnesses.** Poisson residual field, Gauss flux ratio across
surface shapes, interior shell residual, superposition defect, composition
dependence of test-state acceleration, conservation residuals.

**Falsification bar.** Failure of any single item beyond its sealed bar
rejects the Newtonian-limit claim. Items 3-5 are the discriminating ones: a
reverse-engineered entropy gradient can fake item 1 on the training region
but has no reason to pass shell, superposition, and universality on
held-out configurations simultaneously.

**Substrate.** NRP ensembles for field maps; MATLAB on Atlas for
independent reduction and the analytic shell/superposition references.

---

### EG-5: Black-hole benchmark

**Question.** At the compact-source limit, does the framework reproduce
horizon-like thermodynamics, and does the projection hide information
rather than delete it?

**Method.** Drive the declared source toward the compact limit permitted by
the model. Measure: (a) entropy of the enclosed region versus the area of
the enclosing surface; (b) the declared detector temperature versus the
surface-gravity analogue kappa (target relation T ~ kappa / 2 pi in the
model's units); (c) global recoverability: the full-resolution hidden
record must remain sufficient to reconstruct the initial hidden state
(volume preservation and invertibility audit), so that any apparent
information loss is attributable to the projection and resolution, never to
deletion; (d) the fine-grained conservation accounting of PF-5 throughout.

**Primary witnesses.** Stability of the entropy-area coefficient across
source strengths, slope of T versus kappa, hidden-state reconstruction
residual at full resolution, fine-grained volume-conservation residual.

**Falsification bar.** Entropy scaling with enclosed volume at the compact
limit, a temperature unrelated to kappa, or any apparent deletion of hidden
information traced to the model rather than to a declared resolution limit
rejects the benchmark. EG-5 may not run unless EG-1 through EG-4 have
passed; a black-hole analogy on top of a failed area gate is forbidden by
construction.

**Substrate.** NRP for the ensemble limit; MATLAB on Atlas for reduction.

## 7. Comparison: postulated entropic action versus constructive route

| Aspect | Bianconi, arXiv:2408.14391 | This track |
|---|---|---|
| Origin of entropy | Postulated action: quantum relative entropy between the metric, read as an effective density matrix, and a matter-induced metric | Derived: entropy of fibers of a concrete observation map with a fiber measure declared before runs |
| Status of the metric | Fundamental variable of the action | Candidate emergent object: distinguishability form on fiber-conditional distributions, tested rather than assumed |
| Matter coupling | Matter fields induce a second metric inside the postulated action | Matter is a declared local deformation of hidden dynamics; it deforms the fiber measure, and everything else must follow |
| Field equations | Variation of the postulated action; Einstein limit at low coupling | Must emerge from coarse-grained hidden dynamics and survive EG-4's held-out structural tests |
| Cosmological constant | Emergent, small, positive, from G-field multipliers | No statement; outside the pilot scope |
| Validation mode | Analytical self-consistency | Analytical work plus a sealed falsification campaign with preregistered bars |
| Designed failure point | None; the action is chosen to work | EG-1 area gate, where the generic expectation is failure |

The two routes are complementary, not competing: if the constructive route
ever produced an area law and a first law, comparing the resulting
effective action to Bianconi's postulated one would be a natural follow-up.
Nothing licenses that comparison today.

## 8. Position in the campaign

EG runs AFTER the PE entropy track validates its instruments. Concretely:
PE-0 is implemented and passing, but EG-0 additionally requires the full
H(Z_delta | X_epsilon) surface and the relative-entropy extension, and the
PE-2 reversible-cycle discipline is a prerequisite for reading any EG
entropy change correctly. No EG experiment is scheduled until the PE track
seals its instrument layer.

```text
PF-0 sealed instrument net (done)
      |
PE-0 / PE-1 entropy instruments (passing, unsealed)
      |
PE-2 reversibility discipline
      |
EG-0 projection entropy instrumentation
      |
EG-1 area-versus-volume gate   <- expected stopping point
      |
EG-2 matter deformation
      |
EG-3 local first law
      |
EG-4 geometric equations
      |
EG-5 black-hole benchmark
```

Substrates follow the campaign allocation: MATLAB on Atlas for analytic
controls, exact small-N work, and independent reduction; NRP for scaling
sweeps and ensembles, as finite Kubernetes Jobs under the standing cluster
policy.

The near-term deliverable is a theorem or a negative campaign establishing
which projection geometries CANNOT yield, simultaneously, area-law entropy,
inverse-square attraction, universal coupling, and Einstein-like
conservation. A positive model passing all four gates without inserting any
of them would matter; the negative classification is the expected outcome
and is publishable on its own under the campaign's evidence discipline. A
clean negative is a result.

## 9. Non-claims

Nothing in this track bears on physical gravity. No run in this track will
be labeled evidence that spacetime is a projection, that gravity is
entropic, or that the cited literature is confirmed or refuted. Evidence
labels follow CAMPAIGN.md section 9; everything in this document is
`[exploratory]` until a sealed preregistration exists, and the highest
label any EG result can earn is `[demonstrated-in-model]`.

## 10. Open design questions (must close before EG-0 seals)

Recorded at drafting time, 2026-08-04. Each needs a decision or a
PE-style closed-form control before the corresponding experiment can seal.

1. **Distinguishability metric underdefined.** Section 3 names a
Fisher/relative-entropy quadratic form on fiber-conditional distributions,
but at finite (delta, epsilon) several inequivalent discretizations exist,
and the Level-0 choice affects EG-4. Needs a closed-form control.
2. **"Independently distinguishable states associated with a region" has no
operational definition.** Mutual information with the complement,
conditional entropy given boundary data, and code-subspace dimension give
different counts; the EG-1 area-gate verdict could depend on the choice.
The single most important pre-seal decision.

   **DECIDED, 2026-08-05, before any EG-1 run.** The primary count is
   the conditional entropy of the region's hidden state at resolution
   delta given the boundary data, H(region | boundary), because it
   directly counts interior distinctions not fixed by the boundary,
   which is what the gate's independence requirement is about. The
   mutual information with the complement, I(region ; complement), is
   a mandatory secondary witness computed alongside it in every arm,
   because the two can diverge and the divergence is itself
   informative (the classical Gibbs mutual-information area law is a
   known confound the standing warning addresses). Any arm whose
   verdict differs between the two counts is reported under both,
   with the primary count deciding the gate.

   **COROLLARY DECISION for dynamical ensembles, 2026-08-05, before
   any EG-1b run.** The entropy-density lemma recorded under EG-1b
   forces any passing mechanism to have zero bulk entropy density, and
   the natural zero-density class is deterministic local dynamics with
   the region read as a spacetime region. For such ensembles the
   deterministic interior makes H(interior | boundary) exactly zero,
   which is degenerate rather than informative, so the operational
   count of states associated with a spacetime region is the marginal
   entropy H(region), compared against region volume R^(d+1) and
   region boundary R^d, with H(interior | boundary) still computed and
   reported. A pass additionally requires the structural-origin audit:
   the same construction with the structural feature removed (bulk
   noise added) must revert to a volume law, showing the scaling
   tracks the declared structure and nothing tuned.
3. **The EG-2 reverse-engineering audit is a criterion, not yet an
algorithm.** A formal test certifying that a source is not
potential-equivalent may be undecidable in general; a restricted declared
source class may be needed instead.
4. **No temperature definition exists yet for EG-3/EG-5.** Without an
Unruh-analogue response derived inside the model, EG-3 risks being
unrunnable rather than falsifiable.
5. **Can the fiber measure be canonical?** A measure induced by a hidden
symplectic/Liouville structure (as in the PF-2 toy) would strengthen any
positive and simplify the anti-circularity story versus an arbitrary
declaration.
6. **kappa in EG-5 is undefined until EG-4's metric exists.** The current
text assumes a surface-gravity analogue can be constructed.
7. **Sequencing tension.** This file requires PE-2 before EG-0, but PE-2 is
itself only designed. Starting EG-0 earlier is a conscious decision to
relax that dependency, not a silent violation.
