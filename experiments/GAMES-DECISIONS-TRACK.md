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

### GD-2: The budget flip in a game

A finite imperfect-information game where a player's information set
refinement is bought under a declared budget. Task-optimal versus
fidelity-optimal coarsenings, the QO-2 protocol transplanted.

### GD-3: Prospect signatures from budgeted consumers

A declared noisy budgeted estimator of gamble probabilities under a
declared prior. Measured question, does the optimal read exhibit
inverse-S weighting and asymmetric response to gains versus losses
WITHOUT any weighting or asymmetry inserted, per the efficient-coding
hypothesis, or does it fail to. Either outcome is a result. The
reverse-engineering audit of the EG track applies verbatim.

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
