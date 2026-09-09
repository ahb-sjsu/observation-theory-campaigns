# OD Track: Observational Discovery, from the read operator to laws that survive observers

**Status:** D0 done; D1 done, INDETERMINATE by its sealed grader (five of six well-crossed cells pass every bar, the sixth misses one ratio by 0.003; the single-direction theorem exact and the pencil confirmed); D3 sealed (blob cde83217d6901d92003d25192092eb61eebd6169) and running; D2, D4 to D7 design drafts, non-claim-bearing until run. Chip 🔭 OD. Opened 2026-09-09.

## 1. Question

Observation Theory supplies the observer O = (C, G, B) and the geometry it induces,
P_C = J_C^T G J_C. Geometric Evaluation Theory supplies the evaluator whose metric and budget
can be recovered from its choices. The discipline of this repository supplies sealed gates,
registries of admissible transformations, and envelopes. The track asks whether those three,
run as one loop, find laws about observation that survive every declared observer, and it
starts with the objects that are already theorems in the read operator's spectrum.

The order is deliberate. First the statements that are provable now (D0, D1, D3), then the
law the program has the data and the search machinery for (D2), then the loop turned on the
program's own search processes (D4), and only then a dynamical system with a known singular
answer (D5). Fluid regularity is not a gate of this track. If D5 finds a signature that survives
the separation of simulation resolution from observation budget, a later track can carry it to
Euler; the track does not carry it to Navier–Stokes, whose question is a theorem this loop
does not produce.

## 2. Anchors

The article `geometric-evaluation-theory/articles/2026-09-09-identifiability-at-a-budget.md`
(Theorem 1, the observability Gramian as the budget-zero read operator; Theorem 2, the three
kinds of direction and d_obs(B, rho); Proposition 1, the observational Lyapunov exponent);
GET Theorem 4 and its gate G5; the encyclopedia entries read operator, nuisance, read direction,
effective rank, budget cliff, hubness, anti-hub, Poisson ceiling; the hubness track's finding
that hubness is almost entirely a property of the queries and the reader; Kalman (1960) and
Hermann and Krener (1977) for observability, to be cited with verified records before any
seal; `standards/DPE-RECORDS.md` for the records every gate below produces.

## 3. Anti-circularity contract

Every gate declares its observers as a family in `claims/transformations/OD.toml` before its
seal, and a claim that holds for one observer and fails for another in the family fails.
Every classical control (Euclidean distance, energy, spectral distance, the classical
Lyapunov exponent, the classical Gramian) is computed beside the observational quantity, and
a result that the classical quantity reproduces is not an Observation Theory result. Every
law found by search is frozen on the world it was found on and tested on a world it never
saw, with the transfer recorded as a registry test.

## 4. Gates

### D0. The theorem, machine-checked

Deliverable. Lean files checking Theorem 1 (the window consumer's read operator is the
Gramian, observability iff positive definite, kernel is the unobservable subspace), Theorem
2 (identifiable at (B, rho) iff the quadratic form clears B^2 / rho^2; d_obs non-increasing in B;
rank at B = 0), and Proposition 1 for a bounded positive spectrum. Mathlib has the Gramian's
ingredients (matrix exponential, integrals of matrix functions may need to be taken as a
hypothesis, recorded as G1 recorded Ky Fan).
Bar. Zero `sorry`; standard axioms only; every hypothesis taken in place of a Mathlib gap
named.
What falsifies. A statement that cannot be closed as written; the article is corrected first.
Record, 2026-09-09. DONE. `geometric-evaluation-theory/lean/GET/Identifiability.lean` at commit
9604c44 checks eight statements against Mathlib v4.32.2: the read operator of a linear consumer is
positive semidefinite for a positive semidefinite output metric; a kernel perturbation is
distinguishable at no budget; for a positive definite output metric, distinguishability at budget
zero is injectivity of the consumer; the scaled-direction criterion v^T P v > B^2 / rho^2;
antitonicity in the budget; d_obs antitone in B, equal to the positive-eigenvalue count at B = 0,
and zero once every lambda_i rho^2 <= B^2. Full project build 8,664 jobs, zero warnings, no
`sorry`, every theorem on propext, Classical.choice and Quot.sound only. Not checked: the Gramian
integral itself, which enters as the consumer's matrix; Proposition 1 on the Lyapunov exponent,
which needs the flow and is left for D3's registration. Ledger row GET-16 in the GET repository.

### D1. Identifiability at a budget, finite-sample form

Prediction. Theorem 2 is a statement about one direction at a time; the gate measures its two
finite-sample consequences (article Corollaries 3 and 4). Single-parameter probes, one coordinate
of a basis that is not the eigenbasis perturbed at a time on a ladder of sizes, learn exactly
which coordinates are identifiable at (B, rho), a bracket on each diagonal entry, and nothing
off the diagonal. Mixed probes, random directions on the sphere of radius rho, learn the whole
operator, below-threshold eigenvalues included, up to the pencil s P + (1 - s)(B^2 / rho^2) I,
wherever the sphere crosses the ellipsoid delta^T P delta = B^2 substantially, and nothing where
it does not, because the oracle is then constant; the analytic centre returns the pencil's end,
P itself with a kernel and the member with smallest eigenvalue zero without one.
World. Read operators of declared spectrum in a random frame: n = 5 with a kernel, n = 8 with
two kernel directions, n = 8 positive definite; rho = 1; B on 0.25 to 2; 20 evaluators per cell;
the oracle answers whether delta^T P delta exceeds B^2 and nothing else; queries 60 to 960.
Estimator. World A none, verdicts and brackets read from the oracle. World B the analytic
centre of the positive semidefinite operators consistent with the answers under a declared cap.
Bars. A1 verdicts and brackets exact; B1 in well-crossed cells the medians of the Frobenius,
above-threshold and below-threshold errors at most 0.30 of chance; B2 no crossing, constant
oracle; B3 monotone in queries; B4 in the positive definite world the estimate nearer the
pencil's end than P.
What falsifies. A verdict that contradicts the inequality; an operator mixed probes cannot
recover up to the pencil under a substantial crossing; below-threshold eigenvalues left at
chance; a non-constant oracle where the crossing condition fails; an analytic centre nearer P
than the pencil's end.
Record. The first design read Theorem 2 as an operator statement and predicted that mixed
probes recover only the above-threshold directions; its pilot (`pilot_v1.json`) refuted that
before any seal, recovering the below-threshold eigenvalues to 3 to 10 percent of chance, and the
geometry explains it. The second pilot fixed REC = 0.30 with no exclusions and found the crossing
condition necessary and not sufficient for a non-constant oracle in finite samples. A pre-seal
probe (`pencil_probe.json`) found that answers at one radius identify P only up to a pencil and
that the analytic centre returns the pencil's end, which became Proposition 2 and Corollary 4 of
the article and bar B4. SEALED 2026-09-09 as `experiments/OD/D1/PREREG-D1.md`, blob 74c03eae77c20854f5bd4512d22187823b3d79b6.
Run, 2026-09-09 (Atlas, screen `od-d1`, 08:48 to 09:12 UTC, `run.log`, code at 3a57462, seed
20260914, fresh frames and queries, 90 cells). `results.json` and `grade.json` committed as
executed; `d1_grade.py results.json --rec 0.30` run by hand on Atlas. Verdict by the sealed
grader: INDETERMINATE. What held: A1, verdicts and brackets exact in every evaluator of all
fifteen World A cells; B2, the oracle constant in the one cell the theory says cannot cross
(n = 5, B = 2) and, as in the pilot, in the thin crossing at n = 8 positive definite, B = 0.25;
B3, the Frobenius median falling along the whole query ladder in all six well-crossed cells; B4,
the estimate nearer the pencil's end than the truth in 20 of 20 evaluators at both B = 1 and
B = 1.5 in the positive definite world (Frobenius 0.223 against P, 0.181 against P*; 0.117
against 0.102); B1 in five of the six well-crossed cells, Frobenius medians 0.045 to 0.111 of
chance, above-threshold medians 0.055 to 0.111 of chance, below-threshold medians 0.037 to
0.172 of chance. What missed: in the sixth cell, n = 8 positive definite at B = 1, the Frobenius
ratio 0.198 and the below-threshold ratio 0.068 held and the above-threshold ratio was 0.303
against REC = 0.30, the pilot having sat at 0.299 in that same cell and REC having been fixed as
the pilot's maximum rounded up to two decimals, a rule that carries no margin for a fresh seed.
The bar is not moved. What the gate establishes: Theorem 2 read along a coordinate is exact in
finite samples (300 evaluators, 0 mismatches); mixed probes at one radius recover the operator,
below-threshold eigenvalues included, to a tenth of chance in every kernel world and to a fifth
in the positive definite one, and they recover the pencil's end and not the truth there, as
Proposition 2 and Corollary 4 say; the crossing condition is necessary and not sufficient for a
non-constant oracle in finite samples. What it does not establish: the registered factor 0.30
for the above-threshold eigenvalues at 960 queries in the positive definite world, missed by
0.003 of a ratio. Registration lesson, for later gates of this track: a tolerance fixed at a
pilot's own maximum, rounded up, is a bar with no margin; fix it as a declared multiple of the
pilot's maximum instead. The second pilot's uncommitted duplicates (`pilot_v2.json`,
`pilot_v2.log`, named in the sealed text) were deleted from the Atlas clone by the sync script
that pulled the sealed commit; the committed third pilot reproduces every field of the second
exactly, as the sealed Section 7 records.

### D2. Observer-relative hubness, the law

Prediction. There is a low-complexity relation H_k = F(d_eff(P_C), kappa(P_C), B, k / N, ...)
between a point's k-occurrence under an observer's distance and the observer's spectrum, and
it survives a change of observer within a declared family, a change of data from synthetic
to real embeddings, and a change of scale.
World. The trillion-vector machinery and the hubness track's corpora; observers as declared
read operators (isotropic, anisotropic with declared spectra, learned consumers' recovered
P_C); the null of the Poisson ceiling per observer.
Search. Theory-radar's symbolic search over expressions in the registry's variables, scored on
held-out accuracy, expression complexity, and invariance across the declared observer family
(the envelope), with the evaluator's own metric over those criteria recovered from the
program's past acceptances and rejections by the G5 estimator rather than asserted.
Discipline. Discover on synthetic Gaussian and anisotropic worlds; freeze; test on embeddings
and ANN corpora without retuning; the transfer is a registry test with outcome survived,
boundary, or failed.
Bars. Held-out accuracy above the null; the frozen law within a registered tolerance on the
unseen worlds; the law's envelope strictly containing that of the best classical
(observer-free) hubness predictor at comparable complexity.
What falsifies. A frozen law that fails on the unseen worlds, or a classical predictor with
the same envelope at no more complexity.
Paper. The draft *Hub Relativity: Observer-Dependent Geometry in High-Dimensional Spaces*
(Bond, 2026, unpublished) is this gate's paper. Its objects map onto the gate as follows: the
observer-relative k-occurrence H_k(x | O) and the polarity score with thresholds fixed before
validation are the measured quantities; the cross-observer hubness matrix H[i, j] over N points
and M observers, with its effective rank, is the gate's central new object and gets its own
registered bar (effective rank far below min(N, M) against a spectrum-matched random-observer
null); the observer-sensitivity R_H and the hubness distance between observers D_H define the
observer equivalence classes, which are the registry's families read back from the data; and
its Appendix A experiments are the gate's cells, A1 the dimensional baseline (calibration, no
claim), A2 the observer swap on fixed data (the polarity-reversal rate against the
random-orientation null), A3 the controlled spectrum sweep (polarity crossings located in the
spectral exponent), A4 the budget sweep (the critical resolution B_c), A5 the cross-observer
matrix, A6 the frozen law on unseen distributions, A7 the scale test. The paper's own
falsifiers, whitening removing the effect, nominal dimension predicting as well as effective
dimension, finite resolution adding nothing beyond dimensionality reduction, and laws that
fail beyond one family, are the gate's. Before any seal the paper must cite the hubness
literature it builds on (Radovanovic, Nanopoulos and Ivanovic 2010; hubness reduction by
local scaling and mutual proximity, Schnitzer et al. 2012; Feldbauer and Flexer 2019), since
"a change of representation changes hubness" is known there, and the gate's claim is the law
and the latent rank, not the reversal.

### D3. The observational predictability horizon

Prediction. Proposition 1 of the article, restated with this gate (draft 0.3, ledger GET-16r):
for a positive definite observer with spectrum in [a, b] the observational and the classical
window exponents differ by at most log(b / a) / (2 (T - t0)), machine-checked in
`geometric-evaluation-theory/lean/GET/Horizon.lean`; with a kernel the observational exponent
is smaller when the perturbation's Euclidean growth is carried by unread components growing
faster than the read ones, equal in the limit otherwise, transiently larger for a perturbation
started in a kernel the flow does not preserve, and undefined for one confined to an invariant
kernel. The horizon T_O(B) is non-decreasing in B, bracketed for a positive definite observer,
never earlier than the Euclidean horizon for a projection, and observer-dependent at fixed B
where no symmetry of the flow relates the observers, not where one does.
World. Tangent perturbations under the linearised flow of Lorenz-63 (observers full, an
anisotropic metric, x only, z only), of Lorenz-63 with a decoupled unread direction u' = mu u
at mu = 2 and the control mu = 1/2 (World K), and of Lorenz-96 at N = 40 (full, anisotropic,
one block of ten sites, the next block); 64 starts (32 for Lorenz-96) on the attractor; window
ladder 1 to 20; budget ladder 10 to 10000 for a unit perturbation.
Estimator. Window exponents and first-crossing horizons read off the recorded lengths; no
fitting.
Bars. Exact: E1 the window bound, KX the World K identity, H1 the horizon inclusions. With
tolerances fixed from the pilot as declared multiples: E2 convergence under the anisotropic
observers; K1 the smaller case at mu = 2 (gap at least 0.5, classical exponent near mu); K1c
the control; K2 kernel starts larger on the first window and converging; K3 generic starts
under projections converging; H2 horizons observer-dependent in Lorenz-63 by an exact paired
sign test and not across the Lorenz-96 shift symmetry.
What falsifies. A window exponent outside the bound; a kernel reader that sees the unread fast
direction; a kernel start whose read length does not outgrow its Euclidean length at first; a
horizon that decreases in B, leaves its bracket or precedes the Euclidean one; horizons
independent of the observer in Lorenz-63 or dependent across the Lorenz-96 symmetry.
Record. Registered 2026-09-09. The probe found the kernel-start transient already over by
t = 0.1 for half the x-reader starts, so the kernel window starts at 0.01, and found a
permutation test on medians underpowered where the paired sign test is not, so the horizon bar
uses the paired design. The article's Proposition 1 was corrected before the seal ("undefined"
for an invariant kernel, the smaller case with its condition, the window bound made explicit)
and its bound checked in Lean. SEALED 2026-09-09 as `experiments/OD/D3/PREREG-D3.md`, blob
cde83217d6901d92003d25192092eb61eebd6169. Run: pending.

### D4. The geometry of the program's own discovery

Prediction. Successful searches by the generator campaigns and theory-radar occupy a
different region of an observer-relative geometry than failed ones: effective dimension of
the candidate cloud falls before a hit, hubs form around productive candidates, and the
transition precedes the discovery; failed searches show none of it.
World. The logs of GENERATOR-G1, G2 and theory-radar runs already committed, and future runs
instrumented to record candidate trajectories; observers are declared embeddings of
candidates with recovered P_C.
Bars. A registered separation between successful and failed searches on a held-out set of
runs; the same separation under a second declared observer.
What falsifies. No separation, or a separation that one observer shows and another in the
family does not.

### D5. Burgers shock formation as the first singular test

Prediction. Approaching a shock, the observer-induced geometry of perturbations shows a
transition (effective dimension, leading eigenvalue, shell thickness, hubness) that converges
as simulation resolution N grows and depends on the observation budget B through a scaling
collapse Phi(N, B, t) = N^beta F(B / B_c(t)); the classical diagnostics do not predict the
shock time earlier.
World. Inviscid and viscous Burgers, seeded initial conditions, a resolution ladder in N and
an independent ladder in B; the classical controls computed beside every observational
quantity; an adversarial search over initial conditions that maximizes the disagreement
between the observational and the classical diagnostics.
Bars. Convergence in N at fixed B; collapse across N; a registered lead over the classical
diagnostics on held-out trajectories; the 2-D Navier–Stokes negative control (regular flows)
not firing the signature above its registered false-positive rate.
What falsifies. A signature that disappears with N, that the classical diagnostics reproduce,
or that fires on regular 2-D flows.

### D6. Sensor placement as the choice of an observer under a budget

Prediction. For a linear system with candidate sensors, the observer C* that minimizes the
number of sensors subject to d_obs(B, rho) reaching a required count is found by a greedy
selection on the read operator's spectrum, and the observational predictability horizon
T_O(B) of the chosen observer exceeds that of an energy-based or random placement at the
same sensor count.
World. Linear and linearized systems of declared size (a diffusion chain, a linearized
Lorenz-96, a linearized shallow-water grid); candidate sensor sets; the window consumer of
Theorem 1 with the Gramian computed exactly; budgets on a ladder.
Bars. The selected placement's d_obs at least the required count in every declared world;
its horizon longer than the two baselines by a registered margin; the greedy choice within a
registered factor of exhaustive search where exhaustive search is feasible.
What falsifies. A baseline placement that matches d_obs and horizon at the same count, or a
greedy choice far from the exhaustive optimum.

### D7. The minimal observational geometry that closes a turbulent flow

Prediction. For a filtered flow (large-eddy filtering as the consumer C, filter scale as the
budget), the read operator of the resolved dynamics with respect to the unresolved state has a
spectrum whose leading part carries the information a closure needs, so that a closure built
on the leading eigen-directions predicts the resolved flow within a declared tolerance and a
closure built on the same number of energy-ranked directions does not.
World. Two-dimensional turbulence at declared resolutions with declared filters; the read
operator of the resolved tendency with respect to the subfilter state recovered by the blind
probe on the solver; classical controls, energy-ranked and random subspaces of the same
dimension.
Bars. Resolved-flow prediction error under the read-operator closure below the controls' by a
registered margin at matched dimension and matched budget, converging in resolution.
What falsifies. Energy-ranked directions closing as well, or a margin that vanishes with
resolution.

The thread that motivated this track also proposed phase transitions and critical phenomena,
quantum measurement, and computational complexity as observation problems; they are not gates
here, since none has an instrument the program owns.

## 5. Records

Each gate writes its registry families to `claims/transformations/OD.toml` before sealing,
its sealed registration under `experiments/OD/`, its verdict rows to the status ledger, its
witnesses as `[witness]` rows and its revisions as `[revised]` rows, and its transfer tests as
registry tests, so that the encyclopedia prints each entry's envelope.

## 6. Order and what stops the track

D0 and D1 first, together, since D1's estimator is G5's; D3 beside them, since it is a day of
compute. D2 needs the registry of observer families and the evaluator-metric recovery, which
D1 supplies. D4 needs only logs that exist. D6 follows D1 and D3 directly. D5 and D7 last,
with D7 after D5 since it needs the solver-side probe D5 builds. The track stops, with its record, if D1
recovers sub-budget directions (the budget theorem is wrong as stated) or if D2's frozen law
fails to transfer and no classical predictor is beaten (the observer-relative hubness idea
adds nothing to the classical one).
