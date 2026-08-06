# GD Track: Games and Decisions Under Projection

**Status:** design draft, unsealed, non-claim-bearing. Chip ⬜ GD.
No claim anywhere in this track is a claim about human beings or
about empirical behavioral data. Everything is measured in declared
finite models.

## 1. Question

Observation Theory's consumer reads the world through a declared
channel, task, and budget. Imperfect-information decision theory has
lived with the same objects under other names for seventy years. An
information set is the fiber of a projection, many hidden histories
behind one observed set. Blackwell's informativeness ordering is the
decision-theoretic twin of the data-processing inequality. The
question of this track is whether the behavioral structures of
imperfect-information domains, the value of information, the
signature distortions of prospect theory, reference dependence, and
budget-limited equilibrium play, are consumer-relative phenomena,
derivable from declared channel, task, and budget structure with
nothing inserted, and which claimed anomalies are lawful
consumer-relative reads rather than departures from rationality.

Three claim types, never conflated. Instrument claims, that values
of experiments, garbling relations, and optimal budgeted reads can
be computed exactly in finite models. Structural claims, that
declared consumer structure produces the named behavioral signatures
without their being inserted, or measurably fails to. Behavioral
claims about actual humans, which nothing in this track can support
and no run will be labeled as supporting.

## 2. Anchors (verified citations to be completed before any seal)

Blackwell's theorem, garbling is equivalent to being worse for every
decision problem (Blackwell 1953). Cumulative prospect theory's
inverse-S weighting and loss aversion (Kahneman and Tversky 1979;
Tversky and Kahneman 1992). Rational inattention (Sims 2003) and the
derivation of logit choice from mutual-information costs (Matejka
and McKay 2015). Efficient-coding accounts of probability weighting
(to be surveyed and verified). Each anchor enters as a replication
target or a comparison, never as an inserted answer.

## 3. Anti-circularity contract

Forbidden inputs, mirroring CAMPAIGN.md section 3. No probability
weighting function anywhere in a model's declarations. No reference
point chosen after inspecting outcomes. No loss-aversion coefficient
as an input. No task battery selected after seeing which tasks favor
a wanted verdict. Budgets, channels, priors, and utilities are
declared before claim-bearing runs, and any behavioral signature
must appear in the measured optimal reads, or the claim fails.

## 4. Experiments

### GD-0: Decision-theoretic instrument layer

Exact value of an experiment for a declared prior, utility, and
likelihood system (posterior-optimal action per signal). An exact
Blackwell garbling checker (feasibility of a stochastic factorization
by linear programming). Controls with closed forms, the uninformative
and perfect experiments, value monotonicity under declared garbles
for a declared task battery, garbling detection with permutation
equivalence, the binary symmetric channel ordering, and a classic
incomparable pair whose task battery shows a preference reversal.
No later GD experiment runs until GD-0 passes.

### GD-1: The flip meets Blackwell

The campaign's flip found task-optimized encoders beating
fidelity-optimized ones at scarce budget. Blackwell's theorem says
garbling loses for EVERY task, while divergence orderings are
single-numbered. GD-1 constructs exact experiment pairs where every
declared f-divergence orders A above B while a declared task prefers
B, measuring the wedge between fidelity orderings and task orderings
that the flip exploited, now in decision form.

#### GD-1 protocol (declared 2026-08-05, before the run)

Setting. Binary state, uniform prior, experiments are 2 by k
row-stochastic likelihood matrices with strictly positive entries.
For a binary state every scalar fidelity ordering in the declared
battery is an f-divergence between the two conditional signal
distributions. Declared battery of seven, KL both directions, total
variation, squared Hellinger, chi-squared both directions, and
Jensen-Shannon. Values of experiments and garbling certificates come
from the GD-0 instrument layer unchanged, except that the certificate
search adds an early exit on residual convergence, the checked object
remains the residual against the same tolerance.

Declared exhibit, the rare decisive signal. Experiment A has rows
(0.90, 0.05, 0.05) and (0.05, 0.05, 0.90). Experiment B has rows
(0.98, 0.019, 0.001) and (0.881, 0.02, 0.099). The exhibit task is a
screening decision with a safe action worth (0, 0) and a treat action
worth (-20, +1) across the two states. The design reasoning, declared
so the run can refute it, A's posteriors never clear the treat
threshold 20/21 so A is worthless for this task, while B is nearly
uninformative except for one rare signal whose posterior is 0.99,
and every divergence in the battery still orders A far above B.

Measured items and bars, fixed before the run.

G1 exhibit verification. All seven divergences order A above B each
with margin greater than 0.01, the exhibit task prefers B with margin
greater than 0.01, and the pair is certified Blackwell-incomparable
with both garbling residuals greater than 0.01. All three or G1 fails.

G2 data-processing control. For 500 declared garbled pairs (A random,
B equals A M with M random row-stochastic), every divergence orders A
at or above B within 1e-10 and no task in the declared battery of 205
(200 random utilities on three actions, seed-fixed, plus threshold
tasks at costs 2, 5, 10, 20, 50) prefers B by more than 1e-10. Zero
violations or G2 fails.

G3 localization. In a declared ensemble of 2000 random pairs (seed
20260807, Dirichlet rows, entries at least 0.005 by rejection), every
wedge instance, meaning all seven divergences strictly order one
experiment above the other while some battery task strictly prefers
the other by more than 1e-6, must be certified incomparable. Pairs are
classified comparable when either certificate residual is below the
GD-0 feasibility tolerance, incomparable when both exceed 1e-2, and
ambiguous otherwise, ambiguous pairs are counted and excluded. Zero
wedge instances among comparable pairs or G3 fails, this is
Blackwell's theorem plus the data-processing inequality, so a
violation indicts the instrument, not the theorem.

G4 prevalence, measurement with no bar. Among incomparable pairs in
the G3 ensemble, the fraction exhibiting unanimous divergence order,
the fraction of those with a task reversal in the battery, and the
distribution of maximum reversal margins.

Label. Exploratory, measured in model, unsealed. Substrate Python on
Atlas, results/gd1-flip-blackwell.json.

#### GD-1 results (run 2026-08-05, record sha 685153cd40af6819...)

Verdict FAIL, computed from the declared items. G2 passed exactly,
across 500 declared garbles no divergence rose (worst margin
1.8e-4 in the required direction, floor -1e-10 untouched) and no
task in the battery of 205 gained more than 3.3e-16. G3 passed,
2000 pairs classified 1044 comparable, 767 incomparable, 189
ambiguous, with zero wedge instances among comparable pairs. G4's
measurement is the substantive finding, among the 767 incomparable
pairs 281 showed unanimous divergence ordering and every one of the
281 carried a task reversal in the declared battery, maximum margin
0.0776, median 0.0214. Outside certified Blackwell comparability,
unanimous scalar-fidelity ordering guaranteed nothing about tasks in
a single instance of this ensemble.

G1 failed on one sub-item. The exhibit's seven divergence margins
(minimum 0.429) and task margin (0.0395 against values 0 and 0.0395)
passed, and the reverse residual 0.4198 passed, but the forward
residual measured 0.004486 against the declared bar 0.01. The bar
was set at a round number rather than a computed scale. The exhibit
is provably incomparable, a garbled experiment's joint columns are
conic combinations of the garbler's joint columns, which forces a
residual of at least (r t1 - t0)/(1 + r) with r the garbler's
minimum joint-column ratio, about 0.0021 for the declared exhibit,
so the search residual 0.0045 reflects genuine infeasibility four
orders above the feasibility tolerance. The declared bar failed the
exhibit anyway. The verdict stands as recorded, the design error was
thresholding a search residual instead of certifying infeasibility.

#### GD-1b protocol (declared 2026-08-05, before the run)

Same exhibit, same task, same divergence battery. The change is the
certificate. Incomparability is established by proof, not by a
residual threshold. Direction B-from-A, the exact conic lower bound
above, computed from the declared joint columns, must exceed 1e-3.
Direction A-from-B, total variation is an f-divergence, so a
garbling cannot raise it, and TV(A) minus TV(B) greater than 0.01
proves A is not a garbling of B. Consistency item, the GD-0 search
residual in the B-from-A direction must be at or above the analytic
lower bound. Bars, all seven divergence margins above 0.01, the task
margin above 0.01, the conic bound above 1e-3, the TV gap above
0.01, and the consistency item, all pass or GD-1b fails. G2, G3, G4
are not rerun, they stand as measured in GD-1. Exploratory label,
results/gd1b-exhibit-certificate.json.

#### GD-1b results (run 2026-08-05, record sha 61ef08e2665ab08a...)

Verdict PASS, all five items. Minimum divergence margin 0.429, task
margin 0.0395 (values 0 and 0.0395), conic lower bound 0.004263
against the 1e-3 bar, TV gap 0.751, and the GD-1 search residual
0.004486 sits above the analytic bound, which is nearly tight, the
search was measuring genuine infeasibility to within five percent.
The rare-decisive-signal exhibit therefore stands proved, every
declared f-divergence orders A above B by at least 0.429 while the
declared screening task strictly prefers B and the pair is
Blackwell-incomparable by proof in both directions. Together with
GD-1's ensemble measurement, 281 of 281 unanimous-divergence
incomparable pairs carrying a task reversal, the wedge the QO-2 flip
exploited is now exhibited exactly in decision form and localized to
exactly the region Blackwell's theorem leaves open.

### GD-2: The budget flip in a game

A finite imperfect-information game where a player's information set
refinement is bought under a declared budget. Task-optimal versus
fidelity-optimal coarsenings, the QO-2 protocol transplanted.

#### GD-2 protocol (declared 2026-08-05, before the run)

Setting. Six hidden states with a declared prior. Player one buys a
deterministic coarsening of the state, at most k cells for budget k,
the choice is public. Player two observes nothing. Both then move
simultaneously in a zero-sum game with state-dependent payoffs,
player one maximizing. With two actions for player two the value is
exact, the best response to a player-two mixture q is per-cell
greedy, so the game value is the minimum over q in [0, 1] of a
convex piecewise-linear function, minimized exactly by enumerating
the crossing points of the per-cell action lines. All 203 partitions
of six states are enumerated exhaustively. The fidelity-optimal read
at budget k maximizes mutual information, which for a deterministic
coarsening is the cell-mass entropy, ties collected within 1e-12 and
the flip always charged against the best-valued member of the tie
set. The task-optimal read maximizes game value.

Declared exhibit, the stake game. States are pairs (b, c) with b a
payoff-relevant bit of prior mass 0.8 and 0.2 and c a
payoff-irrelevant trit, uniform within b, so the six priors are 4/15
three times and 1/15 three times. Player one guesses b, payoff +1 on
a match and -2 on a miss, multiplied by a stake of 1 or 3 chosen by
player two. Closed forms, declared for the run to check. The
no-information value is 2/5. The task-optimal 2-cell read is the
b-split with value exactly 1, also the full-information value. The
fidelity-optimal 2-cell reads are the six mass-balancing partitions
splitting 8/15 against 7/15, every one mixing the bit in one cell,
each with value exactly 2/5. The fidelity-optimal spend of the
budget buys exactly nothing, and the flip is exactly 3/5.

Measured items and bars, fixed before the run. H1, the flip at
budget 2 is at least 0.5. H2, at budget 6 the fidelity-optimal and
task-optimal reads agree with the full-information value within
1e-10. C1, the task-optimal value ladder is nondecreasing in k
within 1e-10. C2, the fidelity-optimal entropy ladder is
nondecreasing within 1e-10. C3, no partition's value exceeds the
finest partition's value by more than 1e-10, in the exhibit and in
every ensemble game, this is the zero-sum
more-information-never-hurts theorem, a violation indicts the
instrument. C4, the measured exhibit numbers match the declared
closed forms within 1e-12, including the count of six tied
fidelity-optimal partitions. All six or GD-2 fails.

Ensemble measurement, no bar. 200 games, seed 20260808, prior
Dirichlet on six states, payoffs uniform on [-1, 1] with three
player-one actions and two player-two actions. At budgets 2 and 3,
the fraction of games where the task-optimal read strictly beats
every fidelity-optimal read by more than 1e-6, and the flip
magnitudes. Exploratory label,
results/gd2-budget-flip-game.json.

#### GD-2 results (run 2026-08-05, record sha 3b2d0d4e3ed1cc17...)

Verdict FAIL, computed from the declared items, and the failure is
the declaration's own bookkeeping. H1 passed, the flip is
0.6000000000000001 against the bar 0.5 and matches the declared
closed form exactly. H2, C1, C2, C3 all passed, and every declared
closed-form value matched within 1e-15, the task-optimal 2-cell
value 1, the fidelity-optimal 2-cell value 0.4 equal to the
no-information value, the finest value 1. C4 failed on one integer,
the declaration claimed six tied fidelity-optimal partitions and the
instrument counted three. The declaration double-counted, a two-cell
partition was tallied once from each of its cells, the mass-7/15
subsets are exactly the complements of the mass-8/15 subsets, three
partitions, not six. The ensemble measurement stands, at budget 2 a
strict flip appeared in 193 of 200 random games (fraction 0.965,
median magnitude 0.070, maximum 0.328), at budget 3 in 188 of 200.

#### GD-2b protocol (declared 2026-08-05, before the run)

Identical to GD-2 in every declared object, bar, seed, and ensemble,
with one correction. C4's declared count of tied fidelity-optimal
2-cell partitions is three, the double count above is the named
error. Exploratory label, results/gd2b-budget-flip-game.json.

#### GD-2b results (run 2026-08-05, record sha 2cc051297d42fdb9...)

Verdict PASS, all six items. The stake game stands with its rational
closed forms, task-optimal 2-cell value exactly 1, every
fidelity-optimal 2-cell read worth exactly 0.4, the no-information
value, so the mutual-information-optimal spend of the budget buys
exactly nothing and the flip is exactly 3/5. The three tied
fidelity-optimal partitions match the corrected count. The ladders
are monotone, no partition beats the finest, and at full budget the
two selection rules agree with the full-information value. The
ensemble confirms the flip is generic rather than constructed, at
budget 2 the task-optimal read strictly beat every
fidelity-optimal read in 193 of 200 random games, median flip 0.070,
maximum 0.328, and at budget 3 in 188 of 200. The QO-2 flip is now
measured in a game against an adversary, fidelity-optimal
information purchases are generically the wrong purchases at scarce
budget.

### GD-3: Prospect signatures from budgeted consumers

A declared noisy budgeted estimator of gamble probabilities under a
declared prior. Measured question, does the optimal read exhibit
inverse-S weighting and asymmetric response to gains versus losses
WITHOUT any weighting or asymmetry inserted, per the efficient-coding
hypothesis, or does it fail to. Either outcome is a result. The
reverse-engineering audit of the EG track applies verbatim.

#### GD-3 protocol (declared 2026-08-05, before the run)

Three declared consumers, all exact finite models, none containing a
weighting function, a reference point chosen after outcomes, or a
loss-aversion coefficient. The verdict is computed from the audits
alone. The findings each carry a declared directional bar and are
recorded pass or fail individually, either outcome is a result.

Consumer P1, the sample-budget reader. A gamble's win probability p
is read through n Bernoulli draws under a Beta(2, 2) environmental
prior, the read is the posterior mean, the budget is n over the
declared ladder 1, 2, 5, 10, 50, 200. The implied weight w(p) has
the closed form (2 + np)/(4 + n), checked on a declared grid.

Consumer P2, the log-odds reader. The state is log-odds l on a grid
from -6 to 6 in steps of 0.01, prior proportional to a Gaussian of
variance 1.5 on the grid, the channel adds discrete Gaussian noise
of standard deviation sigma on an m grid from -9 to 9 in the same
steps, the read is the exact posterior mean of p, and the implied
weight w(p) is the channel average of the read. Budget ladder sigma
1.0, 0.5, 0.25, and exactly 0 as the identity control. A shifted
environment with prior mean -1 is probed at sigma 1.0.

Consumer P3, the magnitude reader. Outcomes x from -100 to 100 in
steps of 0.5 are encoded as sign(x) ln(1 + |x|), the channel adds
discrete Gaussian noise of standard deviation sigma on a grid from
-6 to 6 in steps of 0.01, the read is the exact posterior mean of x,
v(x) is the channel average. Symmetric environment proportional to
exp(-|x|/25), asymmetric environment with loss scale 40 against gain
scale 20, declared here on the efficient-coding rationale that the
question is whether a budgeted read transmits environmental
asymmetry into valuation asymmetry. Budget ladder sigma 0.6, 0.3,
0.15, and exactly 0 as the identity control.

Audits, all must pass or GD-3 fails. A1, P1 measured against closed
form within 1e-10 at every n. A2, the zero-noise consumers read the
identity within 1e-12, the machinery inserts nothing. A3, symmetric
environments produce exactly symmetric reads, w(1-p) = 1 - w(p) and
v(-x) = -v(x) within 1e-9. A4, the maximum deviation from the
identity strictly decreases along every declared budget ladder, the
distortion is budget-borne.

Findings, each with its declared bar. F1, P1 is exactly linear
(second differences within 1e-10), regressive about the prior mean,
overweighting below and underweighting above, no inverse-S
curvature. F2, P2 at sigma 1.0 shows the inverse-S signature,
crossover in [0.4, 0.6], w - p above 0.01 on [0.02, 0.2], p - w
above 0.01 on [0.8, 0.98], endpoint secant slopes above 1.1 on
[0.001, 0.05] and [0.95, 0.999], middle secant below 0.9 on
[0.35, 0.65]. F3, the shifted environment moves the crossover below
0.35, the distortion tracks the environment, not the machinery. F4,
the asymmetric environment yields -v(-50)/v(50) at least 1.05, the
loss side is read less compressed. F5, diminishing sensitivity under
the symmetric environment, coarse second differences of v at lag 5
units on [5, 80] have maximum at most 0.01 and mean at most -0.01.
Exploratory label, results/gd3-prospect-signatures.json.

#### GD-3 results (run 2026-08-05, record sha 681bee9bedc132a5...)

Verdict PASS, all eight audits, and all five findings passed their
declared directional bars. P1 matches its closed form to 6.8e-14
with curvature 1.5e-14, the sample-budget reader's weighting is
exactly linear and regressive about the prior mean, prospect
theory's overweighting of small probabilities and underweighting of
large ones with no inverse-S curvature. P2 delivers the full
inverse-S from nothing but a log-odds code, a Gaussian budget, and
Bayes-optimal reading, crossover exactly 0.5 by symmetry, endpoint
secant slopes 3.00 against the bar 1.1, middle slope 0.51 against
the bar 0.9, overweight and underweight margins 0.099 where 0.01 was
required. The shifted environment moved the crossover to 0.338,
matching the prediction logistic(-1) to within grid resolution, the
distortion tracks the environment, not the machinery. P3's
symmetric-environment read is odd to 1.5e-13, the machinery inserts
no asymmetry, and the declared loss-heavy environment produced
-v(-50)/v(50) of 1.208, the loss side read less compressed with
nothing resembling a loss-aversion coefficient anywhere in the
model. Diminishing sensitivity is unambiguous, coarse second
differences all negative with maximum -0.092 and mean -0.402.
Every distortion shrinks monotonically along every declared budget
ladder and vanishes exactly at zero noise. The prospect-theoretic
signature set, regressive weighting, inverse-S, environment-borne
asymmetry, diminishing sensitivity, emerged in declared budgeted
consumers with no weighting function, no reference point, and no
loss-aversion coefficient among the inputs.

### GD-4: Reference dependence as observer functional choice

The PE-3 lesson transplanted, the same hidden gamble read through
declared reference functionals. Observer-dependent valuations are
retained only if the declared detector model predicts every
difference exactly, the PF-6 clause.

### GD-5: Equilibrium with budgeted consumers

Replication target, logit choice emerging from mutual-information
costs (Matejka-McKay), replicated exactly in a declared finite model,
then the campaign question, which equilibrium structures survive when
all players are budgeted consumers.

## 5. Evidence discipline and non-claims

Seals, labels, append-only records, and falsification bars as in
CAMPAIGN.md. Substrate, exact finite models in Python on Atlas.
Nothing in this track is evidence about human decision-making, about
the truth of prospect theory as psychology, or about rationality of
any person.
