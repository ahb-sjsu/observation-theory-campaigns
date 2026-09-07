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
- For a fixed world, a preference is representable exactly when a semidefinite feasibility problem has a solution. Every representable preference obeys the hull law, that no action is strictly worse than every action whose consequences surround it, which holds for every convex metric of evaluation. Affinely independent consequences represent every order on at most m+1 actions, and consequences on a line represent exactly the single-peaked orders, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:269-291`. A closed-form combinatorial characterization is open.
- Uniqueness. From the order on an open connected set of consequences, the metric is identified up to a positive scale and the ideal up to the metric's null directions, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:292-336`. This is what the learned-geometry protocol can recover from choices and no more.
- Special cases with their conditions, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:337-374`. Expected utility, mean-variance evaluation, additive multi-attribute value and the ideal-point models, the geometric decision cost of the TCSS paper, satisficing, the Dawid-Lauritzen decision geometry, and Nash equilibrium through the behavioral game. Loss aversion and lexicographic priority as a metric are not in the theory as written.
- Four theorems a scalar utility on the action set does not provide. A change of rank budget reverses preference between two fixed actions with the evaluator unchanged, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:375-396`. Two evaluators share a standard of correctness exactly when their induced distances are ordinally equivalent, and agreement on every pair of one menu does not transfer to another, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:397-419`. A representation shared by several evaluators at rank k is optimal for all of them exactly when their geometries share a top-k eigenspace, and otherwise the least weighted regret is attained by the top-k eigenspace of the weighted sum and is strictly positive, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:420-447`. Admissibility that depends on the menu produces choice violating the weak axiom of revealed preference, so an obligation of that kind is not a preference at any strength, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:448-481`.
- Five predictions are stated in a form a measurement can fail, and none has been measured. The threshold tracks the budget, rank changes reverse preference, shared representations pay the regret bound, the hull law holds in a population with a known consequence map, and menu-dependent obligations produce the weak-axiom pattern, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:482-498`. The campaign that would grade them is `geometric-evaluation-theory/CAMPAIGN.md:1-40`, with gates G0 to G8, and only G0, the frozen foundations, is done.
- The three branches under the theory are descriptive choice, normative judgment, and multi-agent interaction, each with what is measured and what is posited stated, `geometric-evaluation-theory/paper/geometric-evaluation-theory.tex:499-522`. The correspondence of the ethics stack's deontic gate to the admissible set and of the invariance principle to factoring through the quotient is posited.

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
