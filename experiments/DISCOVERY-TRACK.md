# OD Track: Observational Discovery, from the read operator to laws that survive observers

**Status:** design draft, unsealed, non-claim-bearing. Chip 🔭 OD. Opened 2026-09-09.

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

### D1. Identifiability at a budget, finite-sample form

Prediction. From outputs of a consumer at budget B, an estimator recovers the eigen-directions
of P_C above B^2 / rho^2 and not those below, and at B = 0 recovers the range and not the
kernel; recovery improves with the number of outputs and fails below a design bound.
World. Synthetic consumers first: linear consumers with declared G and known P_C of chosen
spectrum, including singular ones; then the window consumer of a linear system with a chosen
Gramian; then a nonlinear consumer whose local P_C is recovered by the blind probe. Outputs
observed at budget B as the indistinguishability oracle of Definition 1, that is, the
experimenter sees only whether two outputs are within B.
Estimator. The representation program of GET Theorem 3(a) run on the distinguishability
relation, as in G5, or a spectral estimator from pairs; declared before the seal.
Bars. On medians relative to chance as in G5: identified directions recovered, sub-budget
directions unrevealed, kernel unrevealed, monotone in the battery, cliff below the bound.
What falsifies. Recovery of a direction below the budget threshold, or failure above it at
the largest battery.

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

### D3. The observational predictability horizon

Prediction. Proposition 1: for a positive definite read operator along a trajectory the
observational Lyapunov exponent equals the classical one; with a kernel it can be smaller,
zero for kernel-confined perturbations, and transiently larger; the horizon T_O(B) is set by
the observer as much as by the flow.
World. Lorenz-63 and Lorenz-96 at declared sizes; observers as declared partial and coarse
read operators (subsets of coordinates, smoothed coordinates, a learned consumer's P_C);
perturbation ensembles by seed.
Bars. Equality of exponents within tolerance for positive definite observers; the kernel
cases as predicted; T_O(B) monotone in B and different across observers at fixed B by more
than the null.
What falsifies. An exponent that differs for a positive definite observer, or a horizon that
does not depend on the observer.

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

## 5. Records

Each gate writes its registry families to `claims/transformations/OD.toml` before sealing,
its sealed registration under `experiments/OD/`, its verdict rows to the status ledger, its
witnesses as `[witness]` rows and its revisions as `[revised]` rows, and its transfer tests as
registry tests, so that the encyclopedia prints each entry's envelope.

## 6. Order and what stops the track

D0 and D1 first, together, since D1's estimator is G5's; D3 beside them, since it is a day of
compute. D2 needs the registry of observer families and the evaluator-metric recovery, which
D1 supplies. D4 needs only logs that exist. D5 last. The track stops, with its record, if D1
recovers sub-budget directions (the budget theorem is wrong as stated) or if D2's frozen law
fails to transfer and no classical predictor is beaten (the observer-relative hubness idea
adds nothing to the classical one).
