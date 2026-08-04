# PE Track: Entropy Across Singular Projections

**Status:** design draft, unsealed. PE-0 and the PE-1 convergence slice are
implemented and passing; everything else is design. No thermodynamic claim is
made anywhere in this track.

## 1. Why an entropy track

The fold machinery is fundamentally about how a lower-dimensional observer
counts, distinguishes, and assigns probability to hidden states. Pair
creation is one striking interpretation of a fold; entropy, information loss,
coarse-graining, caustics, and observer-relative multiplicity may be the
deeper subject. The PF instrument net already validates the ingredients:
exact branch counts, orientation, signed-count conservation, and
fold-versus-degeneracy classification.

The clean objects, for hidden state Z in a manifold M observed through
X = pi(Z):

- the fiber pi^{-1}(x) of hidden states compatible with one observation;
- the fiber entropy S_fiber(x) = k_B ln Omega(x) when the hidden state is
  approximately uniform over the fiber;
- the conditional entropy H(Z | X), the uncertainty about the hidden state
  that remains after observing its projection;
- the finite-resolution version H(Z_delta | X_epsilon), which is the only
  version this track measures, because continuous conditional entropy under a
  deterministic projection has coordinate pathologies near singularities.

## 2. Three entropies that must not be conflated

1. **Hidden-state (conditional) entropy** H(Z | X): how much underlying
   information the observer lacks. Folds change the local number and
   weighting of compatible hidden states. This is the immediate connection.
2. **Coarse-grained dynamical entropy** H(X_epsilon): reversible hidden
   dynamics can keep fine-grained Gibbs entropy constant while the observed,
   binned distribution spreads and mixes. Information moves into hidden
   coordinates and correlations, exactly as in ordinary statistical
   mechanics.
3. **Thermodynamic entropy production**: requires a physical mechanism that
   makes lost distinctions inaccessible (dissipation, memory reset, a bath,
   uncontrolled degrees of freedom). A reversible trajectory through a fold
   can later unfold; nothing need have been erased.

The track's standing non-identity: projection ambiguity is not thermodynamic
entropy production unless a mechanism irreversibly discards the distinctions.

## 3. What a fold does to these objects

Near a generic fold the time map has normal form x - x0 = a (tau - tau0)^2.
Crossing the fold changes unsigned multiplicity 0 -> 2 while the signed count
is conserved; if the two branches are equally weighted the branch label
carries exactly one bit. The pushforward density follows the caustic law
p(x) ~ 1/sqrt(|x - x0|) on the two-branch side, by the coarea formula: the
projection compresses hidden volume where its Jacobian vanishes, so the
mechanism is hub-like at the observed level (a large hidden interval maps
into a small observed region).

General principle under test: projection can preserve a topological
invariant while increasing observational multiplicity. Apparent creation
events occur when the multiplicity of a coarse-grained description changes
under a singular projection; a particle pair is one observer-level
decomposition of the new branches.

## 4. Target classification (the paper-shaped result)

| Singularity | Multiplicity change | Signed degree | Local density law | Entropy signature |
|---|---|---|---|---|
| Regular projection | none | fixed | finite | smooth |
| Fold | +/-2 | fixed | inverse square root | one new binary branch distinction |
| Cusp | changes across fold boundaries | fixed globally | stronger structured caustic | correlated branch ambiguity |
| Higher catastrophe | larger structured changes | constrained | class-dependent | multiway ambiguity |

A finite-resolution theory connecting singularity class, oriented degree,
preimage multiplicity, consumer-relative conditional entropy, and reversible
versus irreversible entropy change. Working paper title: "Entropy Across
Singular Projections: Fiber Multiplicity, Caustics, and Observer-Relative
Information".

## 5. Experiments

### PE-0: Analytic entropy controls — IMPLEMENTED, PASSING

For the N0/P0/D0/M0 controls compute preimage multiplicity, signed degree,
coarea branch weights, and H(branch | X). Implemented as
`fiber_branch_weights` / `branch_entropy_bits` (Python) and
`pf.fiber_entropy` (MATLAB) on top of the sealed PF-0 polynomial instrument;
run via `run_pe0_entropy_controls.m` and pytest.

Closed-form targets, all verified in both languages:

- P0 fold: two branches, weights (1/2, 1/2) by symmetry, exactly 1 bit at
  every two-branch slice; 0 bits on the empty side; signed count 0.
- M0 at the symmetric slice t = 0: roots (-1, 0, 1), derivative magnitudes
  (2, 1, 2), weights (1/4, 1/2, 1/4), entropy exactly 1.5 bits; signed
  count +1.
- M0 at the band edge: the merging pair dominates the fiber measure and the
  entropy tends to 1 bit (measured deviation < 1e-3 at 1e-9 from the edge).
- N0 and D0: one branch everywhere, zero ambiguity. The degenerate critical
  point of t = tau^3 creates no branch entropy because the map stays
  monotone; multiplicity, not criticality, is what carries information.

**Falsification bar (instrument):** any disagreement with the closed-form
values above beyond stated numerical tolerance.

### PE-1: Resolution scaling — convergence slice IMPLEMENTED, PASSING

Sweep the observation-bin width epsilon. A claimed entropy increment must
converge as resolution improves; an increment that disappears or diverges is
a binning artifact. Implemented so far: the binned pushforward entropy of
the exact fold satisfies H(X_epsilon) + log2(epsilon) -> 1 - 1/ln(2) bits
(its differential entropy), monotonically in the tested range; the caustic
divergence is integrable and produces no pathology. Remaining: the
H(Z_delta | X_epsilon) surface in both resolutions, and the branch-entropy
plateau (1 bit away from the fold, resolution-limited within the unresolved
fold bin).

### PE-2: Reversible fold cycle — IMPLEMENTED, PASSING (exploratory)

Pilot `python/pe2_reversible_cycle.py`, evidence `results/pe2-cycle.json`,
instrument `polyline_level_crossings` (tested against the analytic fold,
refuses non-generic levels and exact sample hits).

Part A, one toy trajectory observed through constant-time levels: the
unsigned multiplicity is a staircase over the observation axis with band
profile 4-8-12-13-12-8-4, constant between breakpoints, and the signed
crossing count obeys the path-degree rule at every one of ~370 tested
levels. Branch entropy from coarea weights rises and falls with the
staircase. Caveat recorded honestly: the 12 fold values of t cluster near
the turning amplitudes, so only the 2 isolated breakpoints (the endpoint
values, steps of 1) admitted the per-breakpoint step check at this level
resolution; the clustered fold breakpoints were verified in aggregate
(steps of 4 across close pairs) plus band constancy. A finer level grid
around the clusters is the follow-up.

Part B, a 10000-member symplectic ensemble evolved forward and
momentum-flip reversed: observed binned entropy H_eps(t) spans a 2.07-bit
range (0.195 to 2.266 bits) along the trajectory, while the initial hidden
ensemble is recovered to 1.1e-14 and the reversed entropy curve retraces
the forward curve with defect 0.0 (bit-identical, as time-symmetric Verlet
guarantees); energy drift 6.1e-9, within the sealed T7 bar. The entropy
change is therefore entirely observational: more than two bits of observed
entropy appear and disappear with zero hidden information loss.

**Falsification bar (met):** signed-count violation at any level, failure
of band constancy, hidden-state recovery residual above 1e-9, or a
reversed entropy curve that does not retrace the forward one would have
invalidated the reading.

### PE-3: Mixing versus folding — DESIGNED

Matched systems: folds without chaotic mixing, mixing without projection
singularity, both, neither. Establishes whether observed entropy growth is
controlled by projection multiplicity, hidden mixing, finite resolution, or
their interaction.

### PE-4: Noise and inaccessible hidden state — DESIGNED

Controlled environmental coupling; measure I(Z; E) and compare with the
observer's lost information. Determines when recoverable projection
ambiguity becomes irreversible entropy production. This is the only PE
experiment that can legitimately produce thermodynamic language.

### PE-5: Observation-Theory consumer comparison — DESIGNED

Consumers reading position only; position and orientation; the branch label;
the full hidden state. Their conditional entropies must be ordered
H(Z|X_pos) >= H(Z|X_pos,orient) >= H(Z|X_branch) >= 0, with the gaps
measuring what each additional observable is worth. This turns
consumer-relative observation into a concrete singular-projection example.

## 6. Novelty discipline

Entropy as log multiplicity, coarse-graining, caustics, pushforward
divergence at folds, and constant fine-grained versus growing coarse-grained
entropy are all established. "Folds relate to entropy" is not a claim. The
candidate contribution is the synthesis: a finite-resolution theory relating
singularity class, oriented degree, multiplicity, consumer-relative
conditional entropy, and reversibility, validated by the same instrument
discipline as the PF track. The related but distinct entropic-gravity
question lives in its own track (ENTROPIC-GEOMETRY-TRACK.md) and starts only
after this track's instruments pass.
