# Geometric Evaluation Theory

**id.** geometric-evaluation-theory
**kind.** concept

## definition

An evaluator-relative theory of preference, value, and choice. An evaluation object is a six-tuple of states with a belief, actions, an evaluator mapping actions and states into a consequence space, a metric of evaluation with an ideal point, a resolution budget, and an admissible set. The distinctions the evaluator can make are derived from the object, and preference and choice are derived from the distinctions. The world supplies the states, the actions, and the map; the evaluator owns the metric, the ideal, the budget, and the admissible set. Written GET, always spelled out, and distinct from Geometric Decision Theory.

**Example.** Two actions with consequences (1, 0) and (0.9, 2), an ideal at the origin, and an evaluator that resolves only the first coordinate rank the second action first at distance 0.9 against 1, while resolving both coordinates ranks it last at distance 2.19, so one evaluator with one metric and one ideal reverses its preference when its budget changes.

**Known as, or related to prior art.** The ideal-point models of Coombs and of spatial voting theory (weighted distance from an ideal) are its unbudgeted single-evaluator case. Luce's semiorders supply the form of finite-resolution preference, with the threshold here fixed by the budget. Rational inattention and limited attention are the nearest theories with a budget, and theirs acts on information about states while this one acts on the resolution of consequences. Dawid and Lauritzen's decision geometry is the identity-evaluator, unbudgeted case. Sen's menu-dependence argument supplies the admissibility theorem. Observation Theory supplies the pullback, the regret, and the budget cliff, and an evaluator is an observer whose output is scored from an ideal point.

## equation

none

## conditions

- The evaluation object is E = (X, A, C, G, B, K), `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:108-130`. The world supplies (X, A, C) and the evaluator supplies (G, B, K), `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:131-140`. Without that split every weak order on a finite set is trivially an evaluation object, so the split is where the theory's content lives.
- Unbudgeted distinctions are an equivalence relation whose local tangents are the kernel of the evaluator's Jacobian. A rank budget coarsens it into a coarser equivalence. A length budget gives a tolerance, reflexive and symmetric, that is transitive only when no three distances form a chain of steps within the budget whose ends lie outside it, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:174-208`.
- Preference is derived, not assumed. At zero threshold it is a weak order represented by minus the distance to the ideal. At a positive threshold it is a Luce semiorder whose threshold is the budget itself, so intransitive indifference is the signature of finite resolution and its size is a property of the evaluation object, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:209-241`. Choice on a finite admissible menu is nonempty, and satisficing is the length budget with the aspiration as ideal, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:242-268`.
- For a fixed world, a preference is representable exactly when a semidefinite feasibility problem has a solution. Every representable preference obeys the hull law, that no action is strictly worse than every action whose consequences surround it, which holds for every convex metric of evaluation. Affinely independent consequences represent every order on at most m+1 actions, and consequences on a line represent exactly the single-peaked orders, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:269-291`. The hull law is machine checked as `hull_law` in `geometric-evaluation-theory/lean/GET/HullLaw.lean:1-43` against Mathlib, with the semidefinite characterization and the line case not checked. A closed-form combinatorial characterization is open.
- Uniqueness. From the order on an open connected set of consequences, the metric is identified up to a positive scale and the ideal up to the metric's null directions, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:292-336`. This is what the learned-geometry protocol can recover from choices and no more.
- Special cases with their conditions, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:337-374`. Expected utility, mean-variance evaluation, additive multi-attribute value and the ideal-point models, the geometric decision cost of the TCSS paper, satisficing, the Dawid-Lauritzen decision geometry, and Nash equilibrium through the behavioral game. Loss aversion and lexicographic priority as a metric are not in the theory as written.
- Four theorems a scalar utility on the action set does not provide. A change of rank budget reverses preference between two fixed actions with the evaluator unchanged, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:375-396`. Two evaluators share a standard of correctness exactly when their induced distances are ordinally equivalent, and agreement on every pair of one menu does not transfer to another, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:397-419`. A representation shared by several evaluators at rank k is optimal for all of them exactly when their geometries share a top-k eigenspace, and otherwise the least weighted regret is attained by the top-k eigenspace of the weighted sum and is strictly positive, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:420-447`. Admissibility that depends on the menu produces choice violating the weak axiom of revealed preference, so an obligation of that kind is not a preference at any strength, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:448-481`.
- Five predictions are stated in a form a measurement can fail. The threshold tracks the budget, rank changes reverse preference, shared representations pay the regret bound, the hull law holds in a population with a known consequence map, and menu-dependent obligations produce the weak-axiom pattern, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:482-502`. The campaign that grades them is `geometric-evaluation-theory/CAMPAIGN.md:1-40`, gates G0 to G8. Done at commit 8eda439: G0, the frozen foundations; G1, the Lean core; G2, the hull law, which passed; and G4 with its follow-up G4b, the shared-code regret, both indeterminate, together establishing what the prediction can and cannot test.
- The hull law has been measured once, under a registration sealed before any rating was read, on the 1972 American National Election Study, where respondents placed Nixon, McGovern, Wallace, and the two parties on seven-point issue scales and rated them on feeling thermometers, `geometric-evaluation-theory/CAMPAIGN.md:42-53` at dc14015. On the registered pair of scales, liberal-conservative and guaranteed jobs, 489 respondents had a menu in which the law could bind, 246 of them, 50.3 percent, violated it at least once, against 66.4 percent with a standard deviation of 1.6 when each respondent's ratings are shuffled among that respondent's own objects, and no shuffle in 200 reached the observed rate, `geometric-evaluation-theory/experiments/G2/results.json:1-87`. Five other pairs of the four scales gave the same ordering, observed rates of 54 to 63 percent against shuffled rates of 67 to 74 percent, the two tax-rate pairs at margins of 0.108 and 0.109 against the sealed bar of 0.10. The verdict is a pass by the sealed bars, and the number that matters more than the verdict is that half of the testable respondents violate the law at least once, so on this world the hull law holds as a population tendency, 10 to 16 points below the geometric base rate of violation, and fails as the deterministic statement of the representation theorem for about half the respondents. Placements are integers on seven-point scales, ratings are integers on a thermometer capped at 97, ties are counted as not strictly better, and no error model was registered, so no part of the half is attributed to rounding.
- The shared-representation regret prediction was measured once, under a registration sealed after one recorded revision and before any loss under any code was read, on Llama-3.2-3B, with the three query heads of each grouped-query group as the evaluators of one key cache and shared codes of rank 2, 4 and 8 in 128 dimensions, `geometric-evaluation-theory/CAMPAIGN.md:73-81` at 8eda439. The verdict by the sealed rule is indeterminate at every rank, `geometric-evaluation-theory/experiments/G4/grade.json:1-239`: at those ranks the measured attention loss is 20 to 330 times the second-order prediction, median 75, with a mean KL divergence of about 4 nats per query, so the regret formula and the deficiency bound were not tested. The registration's second-order bar was also defective as written, comparing the probe's one-key prediction to an all-keys measurement, and that is recorded as a registration defect. The ordering claim, measured on the actual losses, held in 32 of 32 non-vacuous cell-ranks: the leading eigenspace of the summed read operators beat all 32 random codes and the key-covariance code for the group's total loss. The own-code claim failed: a head's own leading eigenspace was the best code for that head in 1, 3 and 6 of 16 cells at ranks 2, 4 and 8, and the compromise was often better for a head than the head's own code. Outside the quadratic regime the theorem orders the shared codes and does not identify the private optimum. The probe that preceded the run, at the drafted ladder 8 to 64, had found the operators of effective rank 2.6 to 8.3 and the three heads largely coincident, `geometric-evaluation-theory/CAMPAIGN.md:71-71` at 8eda439.
- A second sealed run, G4b, measured the object the formula predicts: one key at each probed operating point perturbed by a small isotropic error in the discarded subspace, with an antithetic pair and common random numbers, on the same operators, `geometric-evaluation-theory/CAMPAIGN.md:89-98` at 8eda439. The second-order regime is reached, the ratio of measured to predicted loss is flat in the perturbation size up to a tenth of a whitened unit and its median over cells is 1.02 to 1.05, so the recovered operators predict the loss without bias; but 64 draws per cell leave each cell's ratio offset by a factor with standard deviation 0.16 to 0.24, the registered per-triple bar of 80 percent within 25 percent is missed at 64 to 70 percent, and the sealed verdict is indeterminate, `geometric-evaluation-theory/experiments/G4b/grade.json:1-814`. An exploratory seed check with fresh draws re-centered the five most extreme cells on one, so the offsets are draw noise. The registration's Monte Carlo error estimate and its diagnosis rule were both wrong and are recorded as registration errors. What the two gates establish together: inside the quadratic regime the regret formula, the bound and the compromise's optimality follow from the recovered operators by the theorem, so the prediction's only empirical content there is whether the loss is quadratic with the recovered operator, which holds at the median; outside it, the ordering claim survives and the own-code claim does not.
- The three branches under the theory are descriptive choice, normative judgment, and multi-agent interaction, each with what is measured and what is posited stated, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:503-526`. The correspondence of the ethics stack's deontic gate to the admissible set and of the invariance principle to factoring through the quotient is posited.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

none

## first stated

The foundational paper, draft 0.2, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:1-100`, in the repository ahb-sjsu/geometric-evaluation-theory, with the campaign, prior-art record, and claim ledger beside it.

## measurements

none

## failures and corrections

none

## machine checked

none

## used in

none

## related

geometric-decision-cost, observer, consumer, output-metric, budget, read-operator, quotient, nuisance, budget-cliff, mahalanobis-distance

## see also

none

## status

Generated 2026-09-07 by `encyclopedia/generate.py`; book at observation-data-mining 95af30c; the commit of every record is listed in the encyclopedia's provenance.
