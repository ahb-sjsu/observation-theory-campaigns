# OD Track: Observational Discovery, from the read operator to laws that survive observers

**Status:** D0 done; D1 done, INDETERMINATE by its sealed grader (five of six well-crossed cells pass every bar, the sixth misses one ratio by 0.003; the single-direction theorem exact and the pencil confirmed); D3 done, INDETERMINATE by its sealed grader (every exact bar and every tolerance bar held except the horizon's observer dependence at the largest budget, real in direction and short of the registered level); D2 done, FAIL by its sealed grader (the Gaussian-world hubness law replicates on fresh seeds and does not transfer to other shapes or to Wikipedia embeddings; polarity and latent rank largely held); D3v2 done, PASS (the horizon offset law, a first passage of the read-fraction process, within tolerance in all 22 cells of two flows); D2v2 done, INDETERMINATE (the law transfers to every unseen synthetic family and to SIFT, misses two scale cells and loses to a constant on Wikipedia, whose intrinsic dimension is the variable the discovery set could not teach); D2v3 done, INDETERMINATE (the intrinsic-dimension law fits every real corpus within REF and beats all three competitors on every transfer group; misses the per-world limit on Laplace and a 256-dimensional cube and on heavy tails at N = 16000); D2v4 done, INDETERMINATE (extrapolates to d = 512 and to heavy tails at scale, fits real corpora within half the pilot error, beats every earlier law; misses heavier tails at higher dimension than it was shown); D2v5 sealed (blob 1b9592f8085e98ccac61bf4ef27d5065341bfea5) and running, the search having declined the tail variable; D4 to D7 design drafts, non-claim-bearing until run. Chip 🔭 OD. Opened 2026-09-09.

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

Prediction. Within a family of observers with declared spectra and random orientation, the
hubness of a point cloud under an observer (skewness of the k-occurrence counts) is a
low-complexity function of summaries of the observed geometry and not of the nominal dimension;
discovered on Gaussian clouds and frozen, it transfers without refitting to distributions it was
not discovered on, to real embeddings and to a larger N, and beats the best nominal-dimension
formula at the same complexity. The cross-observer hubness matrix has an effective rank far
below its shuffled null. A change of spectrum changes the hub sets more than a change of
orientation.
World. Observers C = diag(i^-alpha) R, G = I, alpha on 0 to 2 with four rotations; Gaussian
clouds with covariance eigenvalues i^-alpha_data (training), unseen spectra and shapes
(held-out), then, on the run only, uniform cube and ball, Student t, a Gaussian mixture, an
anisotropic cube, 4000 Cohere Wikipedia embeddings (1024-d), 4000 BigANN SIFT descriptors, and
scale cells at N = 16000 and 12000; k on 5, 10, 20; a budget sweep by quantization, exploratory.
Search. Enumeration of a declared 27-feature family in one- and two-term linear models, fitted
on training rows, ranked by held-out error, frozen at the pilot (theory-radar's engine is a
classifier search; this is its regression form; the G5 recovery of the evaluation metric is
deferred).
Bars. L1 fresh seeds within 1.5 REF; L2 unseen families within 2 REF each and 1.5 REF pooled;
L3 real corpora within 3 REF; L4 scale within 2 REF; L5 the law at most 0.8 of the competitor's
error on the transfer groups; X1 effective-rank ratio at most FRAC_X in every world; P1 hub-set
overlap across orientations above the overlap across spectra.
What falsifies. A frozen law that fails on unseen distributions, real embeddings or a larger
N; a nominal-dimension formula that predicts as well; a cross-observer matrix no lower in rank
than its null; spectra that change the hub sets no more than orientations.
Record. Registered 2026-09-09. The probe found direct polarity reversals too rare to grade
(one to three in ten thousand) and the polarity bar was restated on hub-set overlap; the pilot
froze the law skew = -0.026 + 0.421 / cv_d + 0.817 sqrt(d_eff) / k (held-out error 0.37,
pooled 0.80, REF) against a nominal-dimension competitor at 1.86, found effective-rank ratios
0.11 to 0.31 (FRAC_X = 0.48), hub-set overlap 0.29 to 0.41 across orientations against 0.12 to
0.23 across spectra, and, in the exploratory budget sweep, a resolution of a tenth of the
nearest-neighbour distance already changing the polarity of 12 percent of points. SEALED
2026-09-09 as `experiments/OD/D2/PREREG-D2.md`, blob 319f6c6e107757c96e0328dd0cb34b4f782e1c4e.
Run, 2026-09-09 (Atlas, screen `od-d2`, 15:42 to 15:45 UTC, `run.log`, code at bee2177, seed
20260920, 26 worlds, 1,656 law rows). `results.json` and `grade.json` committed as executed;
`d2_grade.py results.json --tols tolerances.json` run on Atlas and reproduced locally. Verdict
by the sealed grader: FAIL, by the Fail clause on the unseen group, where the frozen law's
pooled error 2.45 exceeds 3 REF = 2.39. What held: L1, the law replicates on fresh seeds of the
worlds it was discovered on (pooled error 0.93 against 1.19); P1, hub sets overlap more across
orientations than across spectra in every one of the 26 worlds, real corpora included (Jaccard
0.19 to 0.45 against 0.03 to 0.29); L5, the law beats the nominal-dimension competitor pooled
over the transfer groups (2.90 against 14.8), though only because the competitor extrapolates
wildly to 1024 dimensions (39.8 on Wikipedia) while on the unseen synthetic group alone the
competitor is better (1.74 against 2.45); the scale cell of the discovery family (N = 16000,
error 0.80). What failed: L2, the unseen families, error 1.08 to 4.52 per world against 1.59,
with the law over-predicting hubness on uniform cubes and balls (bias +0.8 to +2.8, the
128-dimensional ball measuring skewness at most 2.0 where the law says 10) and under-predicting
it on heavy tails (Student t, bias -1.5 to -2.4, skewness up to 7.3 at a coefficient of
variation the Gaussian family never reached); L3, the real corpora, Wikipedia embeddings at
error 5.27 (measured skewness 0.17 to 1.14 across the whole observer ladder at effective
dimension up to 156, where the law says up to 10) and SIFT at 1.66 (limit 2.39, so SIFT alone
would have passed); L4 for the Wikipedia scale cell (5.19); X1 in three of 26 worlds, the
64- and 128-dimensional balls (ratios 0.44, 0.59) and the Wikipedia scale cell (0.42) against
0.48, the other 23 between 0.10 and 0.30. What the gate establishes: on Gaussian clouds of any
declared covariance and any observer of the family, hubness is set by distance concentration
and the observed effective dimension per neighbour, and the law replicates; the hub sets of a
cloud are an orientation-stable, spectrum-sensitive object in every world tried; the
cross-observer matrix is low-rank against its null everywhere, at a ratio that rises for the
least concentrated clouds. What it refutes: that this law, or any law in the concentration and
effective-dimension variables of the Gaussian family, governs hubness across shapes; the
Wikipedia embeddings show almost no hubness at an effective dimension where Gaussians show a
great deal, and heavy tails show a great deal where the Gaussian variables say little. The
program's earlier finding that hubness belongs to the queries and the reader rather than the
corpus stands beside this one: a corpus-side law fitted on one shape does not carry. The
exploratory budget sweep found that a resolution of a quarter of the nearest-neighbour distance
changes the polarity of 79 percent of the Wikipedia points under the isotropic observer (12
percent at a tenth), against 7 percent under the anisotropic one, so the finite budget is
a first-order effect on real embeddings, not a refinement of dimensionality reduction. The
draft paper's hypothesis that observer-relative hubness is governed by general geometric laws
is, for laws of this form, refuted as registered; a successor gate would need a variable that
separates shape from spectrum (tail weight, or the concentration of the neighbour distances
themselves) and would have to be discovered on more than one family.

### D2v2. Observer-relative hubness, the law with a shape variable

Prediction. D2's repair: hubness under an observer is a low-complexity function of quantities
measured on the observed cloud alone, spectral summaries together with family-blind shape
summaries (centroid-distance spread and tails, coordinate kurtosis, TwoNN dimension, neighbour
distance concentration, relative contrast), discovered on seven families at once, frozen, and
transferring to families, corpora and sizes it was not discovered on, beating both the best
nominal-dimension formula and the frozen D2 law. Latent rank and polarity as in D2.
World. D2's observers; training on Gaussian (three covariance exponents), cube, ball, Student t
(5 degrees of freedom) and a four-centre mixture at d = 32, 64, 128; held-out on other shapes,
dimensions and observer spectra; on the run only, Laplace, log-normal, the sphere, a two-scale
mixture, Student t (2.5 degrees), the cube at d = 256, a steep Gaussian, two Wikipedia slices,
SIFT base and SIFT queries, and four scale cells.
Search. Enumeration of a declared 66-feature family in up to three terms under the identity and
the log(1 + skew) transforms, ranked on held-out error, frozen at the pilot.
Bars. As D2, with the frozen D2 law added to the competitor bar (L5).
Record. Registered 2026-09-09. The pilot froze log(1 + skew) = 2.811 + 0.0047 d_ent
- 0.0928 / cv_d - 2.461 sqrt(top_share): the search had the shape variables and chose none,
the log transform and the top eigenvalue's share doing the work on the balls (errors 0.44 to
0.95 where D2's law erred by up to 4.5); held-out error 0.45, pooled 0.92 = REF, against 2.04
for the nominal competitor and 2.13 for the D2 law. Effective-rank ratios 0.09 to 0.67 (the
ball at d = 96), so FRAC_X = 0.90 by the cap. SEALED 2026-09-09 as
`experiments/OD/D2v2/PREREG-D2V2.md`, blob 8608a57538edfeaa328b536e879a3200d07a6813.
Run, 2026-09-09 (Atlas, screen `od-d2v2`, 17:30 to 17:36 UTC, `run.log`, code at 269a512, seed
20260926, 44 worlds, 2,844 law rows). `results.json` and `grade.json` committed as executed;
`d2v2_grade.py results.json --tols tolerances.json` run on Atlas and reproduced locally to the
last digit of every bar. Verdict by the sealed grader: INDETERMINATE. What held: L1, fresh
seeds of the discovery families at 1.00 against 1.38; L2, every one of the eight unseen
families within 2 REF (Laplace 0.98 and 0.59, log-normal 0.50, the sphere 1.41, the two-scale
mixture 0.76, Student t with 2.5 degrees 1.39, the cube at 256 dimensions 1.35, the steep
Gaussian 0.37, against 1.84) and 1.00 pooled against 1.38, where D2's law had failed at 1.08 to
4.52; L3, the four real corpora within 3 REF (Wikipedia 2.54 and 2.37, SIFT base 1.27, SIFT
queries 0.75, against 2.77); X1, effective-rank ratios 0.09 to 0.69 in all 44 worlds against
0.90; P1, hub-set overlap across orientations above that across spectra in all 44 worlds. What
missed: L4, two of the four scale cells, Student t at N = 16000 (2.26, skewness up to 14.5,
the law under-predicting the heaviest tails by 1.6) and Wikipedia at N = 12000 (2.55) against
1.84, while the Gaussian and SIFT scale cells held (1.26, 1.15); and the per-group clause of
L5: pooled over the transfer groups the law beats both competitors (1.45 against 2.20 for the
nominal formula and 2.85 for the D2 law), and it beats both in the unseen and scale groups, but
in the real group the nominal competitor, which by the pilot's own ranking carries no dimension
term at all and predicts a constant 2.15 at k = 10, is better on the Wikipedia slices (1.41 and
1.29 against 2.54 and 2.37), because Wikipedia hubness is low and flat (skewness 0.2 to 1.5
across the whole observer ladder) and the law predicts up to 5.3 there. What the gate
establishes: a law in the entropy dimension, the pairwise-distance concentration and the top
eigenvalue's share, under a log transform, discovered on seven synthetic families, transfers
to eight further synthetic families and to SIFT descriptors, and beats the D2 law in every
transfer world but two; the hub sets are orientation-stable and spectrum-sensitive and the
cross-observer matrix low-rank in every one of 44 worlds. What it does not establish, and the
witness that says why: the Wikipedia embeddings have TwoNN intrinsic dimension 8 to 20 at
entropy dimension up to 320, the only worlds in the whole campaign whose intrinsic dimension
sits far below their spectral dimension, and their hubness is low; the search had the
intrinsic dimension among its variables and dropped it, because on the discovery families
(full-dimensional clouds) it carries the same information as the spectral dimension and the
held-out ranking could not tell them apart. The variable that separates real embeddings from
synthetic clouds was declared, measured, and uninformative on the discovery set. A D2v3 would
put low-intrinsic-dimension worlds (clouds on embedded manifolds) into the discovery families,
which is the only way the search can learn that the intrinsic dimension, not the spectral one,
sets the hubness. The exploratory budget sweep reproduced D2's finding on the fresh Wikipedia
slice: a resolution of a quarter of the neighbour distance changed the polarity of 55 percent
of points under the isotropic reader (6 percent at a tenth), 7 percent under the anisotropic
one.

### D2v3. Observer-relative hubness, the law with manifold worlds

Prediction. D2v2's repair: the discovery families gain clouds on embedded manifolds (a
Gaussian in a random subspace, a random Fourier embedding of a Gaussian, a product of circles
read through four harmonics, a swiss-roll sheet), so that the intrinsic dimension carries
information the spectral dimension does not; the law discovered on eleven families transfers
to unseen families, corpora and sizes and beats the nominal formula and the frozen D2 and D2v2
laws. Latent rank and polarity as before.
World. D2v2's observers and cells; 25 training and 8 held-out worlds; on the run only, the
D2v2 unseen families plus three unseen manifolds, four fresh real slices, and five scale cells.
Search. As D2v2. Bars. As D2v2, with the frozen D2v2 law added to L5 at 0.9.
Record. Registered 2026-09-09. The probe found the Fourier manifold reproducing the Wikipedia
signature (spectral dimension 54, intrinsic 12, skewness 0.24). The pilot froze
log(1 + skew) = -1.463 - 0.013 / cv_knn + 0.748 log(id_twonn) + 0.069 sqrt(d_eff): with
manifolds in the discovery set the search took the intrinsic dimension as its main term;
held-out error 0.48, pooled 0.75 = REF, against 1.40 for the D2v2 law, 2.26 for the D2 law and
2.19 for the nominal competitor. FRAC_X = 0.90 by the cap. SEALED 2026-09-09 as
`experiments/OD/D2v3/PREREG-D2V3.md`, blob 0073aea0857a3fa8b7d7c2e7989d8c7d4ea3da83.
Run, 2026-09-09 (Atlas, screen `od-d2v3`, 19:13 to 19:20 UTC, `run.log`, code at e79af28, seed
20260929, 51 worlds, 3,276 law rows). `results.json` and `grade.json` committed as executed;
`d2v3_grade.py results.json --tols tolerances.json` run on Atlas and reproduced locally.
Verdict by the sealed grader: INDETERMINATE. What held: L1, fresh seeds at 0.74 against 1.12;
L3, the four real corpora within 3 REF and, for the first time in the track, within REF itself
(Wikipedia 1.00 and 0.21, SIFT base 0.44, SIFT queries 0.37, against 2.24), the law fitting
the second Wikipedia slice with a bias of -0.12 where the D2v2 law had over-predicted by 1.7;
L5, the law beats all three competitors pooled over the transfer groups (1.05 against 3.58 for
the nominal formula, 2.77 for the D2 law and 1.69 for the D2v2 law) and within each group, the
real group at 0.59 against 2.00 for the D2v2 law; X1, effective-rank ratios 0.09 to 0.68 in all
51 worlds against 0.90; P1, hub-set overlap across orientations above that across spectra in all
51 worlds. What missed: L2, the unseen group pooled at 1.18 against 1.12, with eight of ten
unseen worlds inside the per-world limit (the three unseen manifolds at 0.12 to 0.37, the
log-normal, two-scale, sphere, heavy-tail and 24-dimensional Fourier worlds at 0.55 to 0.97)
and two outside it: Laplace at d = 64 (1.93, the law under-predicting skewness up to 8.8 by 1.3)
and the cube at d = 256 (2.69, over-predicting by 1.8, where the TwoNN estimate reaches 125 for
a full-dimensional cloud of 4,000 points and the intrinsic-dimension term extrapolates beyond
anything the discovery set contained); and L4, one of five scale cells, Student t at N = 16000
(1.91 against 1.49, under-predicting skewness up to 11.5), while the Gaussian, Fourier manifold,
Wikipedia and SIFT scale cells held (0.74, 0.42, 1.10, 0.46). What the gate establishes: with
manifold worlds in the discovery set the search takes the intrinsic dimension as the law's main
term, and the law then predicts hubness on real embeddings, Wikipedia included, as well as on the
synthetic families it was discovered on; across the three registrations the same declared
family and the same search produced a Gaussian law, a shape-blind law and an intrinsic-dimension
law, and only the discovery set changed, which is the track's thesis about discovery in one
line. What it does not establish: the transfer factor on the heaviest tails at large N and on
full-dimensional clouds far above the discovery set's dimensions, where the TwoNN estimator
itself leaves the regime it was calibrated in. The exploratory budget sweep reproduced the
finding of D2 and D2v2 on a third Wikipedia slice: a resolution of a quarter of the neighbour
distance changes the polarity of 75 percent of points under the isotropic reader, 6 percent
under the anisotropic one.

### D2v4. Observer-relative hubness, the law with the discovery set widened to d = 256 and heavy tails

Prediction. D2v3's repair: full-dimensional clouds at d = 256 and heavy-tailed clouds join the
discovery families, so that the intrinsic-dimension estimator's behaviour beyond d = 128 and
on heavy tails is in the training rows; the law transfers to clouds at d = 512, heavy tails at
d = 256, fresh real slices and larger N, and beats the nominal formula and the frozen D2, D2v2
and D2v3 laws. Latent rank and polarity as before.
World. 31 training and 9 held-out worlds; on the run only, 12 unseen worlds, 4 real slices, 6
scale cells including Student t with 3 degrees at N = 16000.
Search. As before. Bars. As D2v3, with the frozen D2v3 law added to L5 at 0.95.
Record. Registered 2026-09-09. The pilot froze log(1 + skew) = -1.094 + 0.169 cv_r sqrt(d_eff)
- 0.032 log(d_nom) log(k) + 0.701 log(id_twonn): the intrinsic dimension keeps its coefficient,
the concentration term changes form, and a small nominal-dimension product enters for the
first time; pooled error 1.065 = REF against 1.13 for the D2v3 law, 1.43 for D2v2, 2.62 for
the nominal competitor; the cube and Gaussian at d = 256 now fit (0.98, 1.03 against 2.56, 2.72
for the D2v3 law) while Laplace at d = 64 fits no law of the family (3.86). SEALED 2026-09-09 as
`experiments/OD/D2v4/PREREG-D2V4.md`, blob 810a2b198d6efda21461632f79240a7774aa2f3c.
Run, 2026-09-09 (Atlas, screen `od-d2v4`, 19:50 to 19:58 UTC, `run.log`, code at 349776c, seed
20261003, 62 worlds, 3,924 law rows). `results.json` and `grade.json` committed as executed;
`d2v4_grade.py results.json --tols tolerances.json` run on Atlas and reproduced locally.
Verdict by the sealed grader: INDETERMINATE. What held: L1, fresh seeds at 1.25 against 1.60;
L3, the four fresh real slices at 0.16 to 0.64 against 3.20, the real group pooled at 0.43, the
best fit to real embeddings of any registration (D2v3's law 0.64 on the same slices); L5, the
law beats all four competitors pooled over the transfer groups (1.62 against 3.18 nominal, 3.47
D2, 2.38 D2v2, 1.77 D2v3) and within every group; X1 in all 62 worlds (ratios at most 0.68
against 0.90); P1 in all 62 worlds. What the widening bought: the clouds at d = 512, beyond the
new training worlds at 256, now fit (cube 1.30, Gaussian 1.79 against 2.13, where the D2v3 law
errs by 3.86 and 4.50), and Student t with 3 degrees at N = 16000, D2v3's scale miss, fits at
0.47. What missed: L2, the unseen group pooled at 1.95 against 1.60, with ten of twelve unseen
worlds inside the per-world limit and two outside, both heavier tails at higher dimension than
the training set holds, Student t with 4 degrees at d = 256 (3.52, skewness up to 20) and
Laplace at d = 192 (4.75, where every law of the family errs by 2.2 to 6.5); and L4, Student t
with 5 degrees at N = 16000 at 2.19 against 2.13. What the gate establishes: with full-dimensional
clouds at d = 256 in the discovery set the law extrapolates to d = 512; with Student t at 3
degrees in the set it holds at scale for that family; the real corpora fit within half the pilot
error. What it does not establish, twice over: a law of this feature family for heavy-tailed
clouds at dimensions and tail weights outside its training set. The feature family has no
tail-weight variable that survives the observer's rescaling except the coordinate kurtosis, which
the search never chose, and the registry records that as the next repair: a tail variable
measured on the neighbour distances rather than on the coordinates, or a discovery set with the
heavy tails placed at the dimensions the transfer asks about. The exploratory budget sweep
reproduced the polarity finding on a fourth Wikipedia slice: 65 percent of points change status
at a quarter of the neighbour distance under the isotropic reader, 7 percent under the
anisotropic one.

### D2v5. Observer-relative hubness, the law with a tail variable measured on the neighbour distances

Prediction. D2v4's repair: four scale-free tail variables measured on the neighbour distances
in the observed space (percentile ratios of the k-th and first neighbour distance, the excess
kurtosis of log r_k, the Hill log-excess of r_k) join the feature pool, and heavy tails are
placed at the transfer dimensions (Student t with 4 degrees at d = 192, Laplace at d = 128) in
the discovery set; the law transfers to heavier tails at d = 256 and 192, to Student t with 2.5
degrees at d = 128 and a log-normal at d = 192, to d = 512, to fresh real slices and to larger N,
and beats the nominal formula and the frozen D2, D2v2, D2v3 and D2v4 laws. Latent rank and
polarity as before.
World. 33 training and 9 held-out worlds; on the run only, 14 unseen worlds, 4 real slices, 7
scale cells including Laplace at N = 12000.
Search. As before, 79 features. Bars. As D2v4, with the frozen D2v4 law added to L5 at 0.95.
Record. Registered 2026-09-09. The pilot froze skew = -2.802 - 0.510 / cv_d + 1.190 log(id_twonn)
+ 1.067 sqrt(d_eff), and the search did not choose a tail variable: the best model containing
one has held-out error 0.752 against 0.709 and is worse on five of the eight heavy-tailed
pilot worlds (recorded before the run in `tail_check.json`). The frozen law is D2v3's form
refitted with heavy tails at the transfer dimensions in the training rows; pooled error 0.878
= REF against 0.932 for the D2v3 law, 1.214 for D2v4, 1.557 for D2v2, 2.674 for the nominal
competitor. SEALED 2026-09-09 as `experiments/OD/D2v5/PREREG-D2V5.md`, blob 1b9592f8085e98ccac61bf4ef27d5065341bfea5. Run:
pending.

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
cde83217d6901d92003d25192092eb61eebd6169.
Run, 2026-09-09 (Atlas, screen `od-d3`, 14:56 to 15:00 UTC, `run.log`, code at b48dc2c, seed
20260917, fresh starts, directions and frames, 384 rows). `results.json` and `grade.json`
committed as executed; `d3_grade.py results.json --tols tolerances.json` run on Atlas and
reproduced locally. Verdict by the sealed grader: INDETERMINATE. What held: the three exact bars
with zero violations, E1 over 3,200 window comparisons (the window bound, machine-checked),
KX, and H1 over 8,960 horizon checks; E2, the anisotropic observers converging to the classical
exponent (medians 0.0197 and 0.0050 at T = 20 against 0.024); K1, in World K at mu = 2 the
observational exponent below the classical in every start by 0.82 to 1.25 (medians 0.914 against
1.965, the classical at its predicted 2 + log(1/2) / 20); K1c, the mu = 1/2 control equal to
0.0072; K2, kernel starts larger on the first window in 83, 98 and 97 percent of starts with
median excesses of +1.53, +2.80 and +3.46 falling to 0.09, 0.14 and 0.17 by T = 20 against 0.231;
K3, generic starts under every projection converging (0.027 to 0.035 against 0.06); H2 in
Lorenz-96, the shift-symmetry control, p from 0.11 to 0.86. What missed: H2 in Lorenz-63 at the
largest budget, B = 10000, where the x reader reached the budget later than the z reader in 64
percent of pairs (median horizons 10.1 against 9.2) with sign-test p = 0.033 against the
registered 0.01, while at B = 10, 100 and 1000 it was later in 77, 78 and 70 percent of pairs
with p = 0.0000, 0.0000 and 0.0022; the pilot had 77 percent and p below 0.0001 at that budget.
The bar is not moved. What the gate establishes: Proposition 1 as restated, in every clause the
world can reach, exactly where it is a theorem and within the declared tolerances where it is a
limit; that the horizon is a property of the observer, later for the x reader than the z reader
of the same perturbation at every budget, with the paired effect weakening as the budget grows
and the perturbation aligns with the leading direction for longer; and that a symmetry of the
flow removes the dependence, as it must. What it does not establish: the registered level at the
largest budget, where the effect is real in direction and short of the level. Registration lesson,
alongside D1's: a per-budget bar at a fixed level over a ladder whose effect shrinks along it
should have declared the level per budget, or graded the ladder as a whole.

### D3v2. The horizon offset law

Prediction. Once a perturbation has aligned with the leading Lyapunov vector, an observer's
horizon differs from the full reader's by the time the growth needs to close the deficit of the
observer's read fraction at the crossing. Because the read fraction fluctuates on the fast
timescale of the flow, the mean log fraction is not the law (the probe refuted it by factors of
two to eight); the law is the first passage computed on one independent long trajectory
carrying the aligned vector, Delta_O(B) = E_s[inf{t >= s : L(t) - L(s) + g_O(t) >= log B} -
inf{t >= s : L(t) - L(s) >= log B}], with L the accumulated log growth and g_O the log read
fraction. It is zero for the full reader, equal across observers a symmetry relates, negative
for a metric exceeding the Euclidean one on the leading direction, and inside D3's bracket for a
positive definite observer.
World. D3's flows with the observer family widened: Lorenz-63 with the full reader, an
anisotropic metric, three coordinate readers, two rank-one readers along declared vectors and
the xy plane; Lorenz-96 with the full reader, an anisotropic metric, two blocks of sites and one
site; 128 and 64 random starts; budgets 10 to 10000; the long trajectory of 2000 (600) time
units integrated separately.
Estimator. First-crossing horizons and their paired mean differences; the prediction from the
long trajectory alone. No fitting.
Bars. Exact E1 and H1 inherited from D3; O1 the law within TOL_O1 at B = 1000 and 10000 for
every observer; O2 convergence between the two budgets; O3 sign and order (Spearman at least
0.9 over the Lorenz-63 observers); O4 the symmetric pair equal within TOL_O4; O5 the
anisotropic offset inside the bracket.
What falsifies. A measured offset off the first-passage prediction by more than the
tolerance, an offset that keeps moving with the budget, a sign or an order the law does not
give, unequal offsets across a symmetry, an anisotropic offset outside the bracket.
Record. Registered 2026-09-09 from D3's lesson. The first probe refuted the constant-fraction
law (Section 7 of the registration); the law was restated as the first passage before any
pilot; the second probe and the pilot then matched every one of the twelve observers within one
to two standard errors in both flows, with the order exact. Tolerances by the declared-multiple
rule: TOL_O1 = 0.259, TOL_O2 = 0.490, TOL_O4 = 0.137. SEALED 2026-09-09 as
`experiments/OD/D3v2/PREREG-D3V2.md`, blob 66397b664e64982759d34694f6f1445e50e438af.
Run, 2026-09-09 (Atlas, screen `od-d3v2`, 15:54 to 16:01 UTC, `run.log`, code at 58505fc, seed
20260923, fresh starts, perturbations and long trajectories, 192 rows). `results.json` and
`grade.json` committed as executed; `d3v2_grade.py results.json --tols tolerances.json` run on
Atlas and reproduced locally. Verdict by the sealed grader: PASS. Exact bars: no violation in
1,920 window comparisons and 10,176 horizon checks. O1: the first-passage prediction matched
the measured mean offset within the tolerance 0.259 in all 22 cells (eleven observers at two
budgets), the largest error 0.149 (`x_only` at B = 1000, predicted 0.97, measured 0.82 with
standard error 0.09); at B = 10000 Lorenz-63 gave `aniso` -0.56 against -0.50 (0.08), `x_only`
1.01 against 1.14 (0.12), `y_only` 0.23 against 0.29 (0.07), `z_only` 0.13 against 0.14 (0.04),
`u1` 0.29 against 0.38 (0.09), `u2` 0.85 against 0.98 (0.11), `xy_plane` 0.17 against 0.21
(0.06), and Lorenz-96 `aniso` -0.27 against -0.26 (0.03), `sub` 0.67 against 0.62 (0.07), `sub2`
0.67 against 0.70 (0.07), `site0` 1.44 against 1.57 (0.09). O2: offsets converged between the
two budgets within 0.32 of the tolerance 0.49. O3: every sign agreed and the Lorenz-63 order
was exact (Spearman 1.0). O4: the symmetric blocks of Lorenz-96 differed by 0.02 in prediction
and at most 0.07 in measurement. O5: the anisotropic offsets, predicted and measured, sat
inside the D3 bracket in both flows. Beside every prediction the constant-fraction value was
recorded and is wrong by 0.09 to 1.0 time units, up to eight times the measured offset. What
the gate establishes: an observer's predictability horizon on a chaotic flow is the full
reader's horizon plus a first-passage time of the observer's read-fraction process along the
leading Lyapunov direction, a quantity computable from one long trajectory without any horizon
experiment, in two flows, for metrics, coordinate readers, rank-one readers and site blocks,
with the symmetry and the bracket that the theory requires. Two exponents, 0.906 and 1.699,
and eleven observers: the law is observer-relative in the track's sense, a functional of the
read operator on the flow that survives the declared changes of observer and of dynamical
system.

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
