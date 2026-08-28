# Same Budget, Opposite Rankings: Consumer-Conditional Policy Reversal in Optical and Radio Networks

**Status: OUTLINE v2 (2026-08-26, revised same day after external review of v1).**
The dedicated inversion paper. Evidence base: XPROTO-QOT-FLIP and XPROTO-CSI-FLIP
(sealing 2026-08-27, graded seeds 20260827-29) plus new phase-diagram and
cost-matched cells to be designed below. **Target: SIGMETRICS 2027, winter
deadline 2027-01-11** (fall 10-09 is feasible but there is no reason to rush;
build the theorem and the graded phase diagrams properly). Backup: ToN (journal
depth), HotNets next cycle (short thesis version).

## The claim (v2, per review)

Two resource-equivalent allocation policies can receive opposite
class-conditional rankings: class 1 is strictly safer under policy A, class 2
strictly safer under policy B. Consequently no scalar ranking that is
independent of the class mixture represents both consumers; any fleet aggregate
ranks the pair only by an implicit choice of class weights.

NOT the v1 claim "the fleet metric is non-ordering" (a scalar always orders;
the problem is that its order is mixture-dependent), and NOT "both
preconditions are necessary" (see Corrections below).

## The formal core (new, from review; verify and adopt)

Allocations m^A, m^B with d = m^A − m^B and q^T d = 0 for a real resource-cost
vector q. Class risk R_c(m); locally R_c(m^A) − R_c(m^B) ≈ ∇R_c(m̄)^T d.

- **Reversal condition:** (∇R_1^T d)(∇R_2^T d) < 0 — the classes have opposing
  sensitivities along a budget-neutral policy direction.
- **Mixture crossover:** for fleet weight λ, ΔR_λ = λΔR_1 + (1−λ)ΔR_2 changes
  sign at λ* = −ΔR_2 / (ΔR_1 − ΔR_2). Report λ* as a measured output in both
  substrates: the class mix at which the fleet verdict flips.
- **Cost matching:** equal mean dB margin is only a nominal budget. MCS/capacity
  are nonlinear in dB, so match q^T m (or matched lost capacity / goodput) and
  show the sealed cells' conclusions survive the re-matching. This needs a new
  cost-matched variant of both cells.

## Corrections to v1 the paper must respect

1. **Sufficiency, not necessity.** Read-operator misalignment + near-threshold
   operation is a *sufficient and empirically predictive mechanism* in the
   studied systems. Misalignment is NOT generally necessary (crossing outcome
   distributions along one scalar projection can invert consumers at different
   thresholds), and a threshold shift does NOT by itself guarantee dominance
   (dominance needs stochastic ordering or positively collinear sensitivities).
   Near-threshold operation is an exposure/detectability condition setting the
   magnitude of ∇R_c, not a universal necessity.
2. **Negatives are an appendix, not a section.** Grid/LLM/ZK go to the evidence
   ledger appendix as scope illustrations. Three absences do not prove
   necessity, and post-hoc mechanism stories for each absence would make the
   hypothesis look unfalsifiable.
3. **Construction threat is the main experimental risk**: policy A allocates by
   class-1's defining variable and B by class-2's, so opposite rankings can look
   built in. Anticipate it head-on (next section).

## Anti-construction evidence plan (the new experimental work)

- **Phase diagrams**: continuous maps over (reach × spectral position) and
  (Doppler × mean SNR) of the per-cell sign of ΔR = R(m^A) − R(m^B); the two
  classes are then just regions of a measured field, not constructed labels.
- **Predict before evaluate**: measure per-class sensitivity gradients ∇R_c
  under small margin perturbations first, register the predicted signs and λ*,
  then run A/B. The prereg discipline is exactly the right instrument here.
- **Baselines**: uniform margin and a robust (max-min) allocation alongside
  A/B; show both A and B are Pareto-nondominated (neither dominated on both
  classes) and that the reversal is not an artifact of strawman policies.
- **Goodput as primary evidence**: verdicts in delivered goodput/capacity, not
  only failure rate; failure-rate reversal that dies in goodput must be
  reported as such.
- **Cost matching** per the formal core.

## Relation to prior literature (must be explicit)

**Relation to the program's own Paper IV (cite first, before external
delineations).** Paper IV ("The Consumer-Relative Flip Across Domains",
`geometric-observation/paper/paper-IV-tmlr.tex`; public embodiment
turboquant-pro, MIT/DOI) is the COMPRESSION flip: one consumer versus the
reconstruction corner P_C = I, a claim about codes, where a fixed bit budget
should be spent. THIS paper is the POLICY reversal: two consumer classes
versus each other over a resource-equivalent allocation-policy pair, no
compression in the claim. Paper IV's dissociation exists with a single
consumer; the reversal requires two, and yields what Paper IV cannot:
opposite class-conditional signs, hence no mixture-free scalar ranking. One
sentence in related work; do not reuse "the flip" unqualified — in program
vocabulary "compression flip" = Paper IV, "policy reversal" = this paper.
(The 2026-08-15 flip_paper_revtex.tex draft is an Alberti-coauthored
networking spin-off of Paper IV's thesis, not prior art for this claim; its
disposition is an owner+collaborator decision, out of scope here.)

**Relation to budget-constrained perception (one paragraph in Discussion,
citations verified 2026-08-27).** The single-observer version of this
paper's setting is an established literature, not ours: rational
inattention (Sims) poses max E[U] subject to I(S;S-hat) <= C; efficient
coding derives probability weighting, diminishing sensitivity, and
reference dependence from capacity-limited encoders and predicts they
shrink as noise vanishes (Woodford, Ann. Rev. Econ. 2020; Frydman and Jin,
QJE 137(1):161-213, 2022); the thermodynamic wrapper is Ortega and Braun
(Proc. R. Soc. A 469:20120683, 2013). What that literature does not have
is the TWO-observer statement: those theories rank encoders by a single
representative consumer's utility. Proposition 3's corollary supplies the
missing case: two budget-constrained observers with different read
operators can rank the same encoder pair oppositely, so "the adaptive
encoding" is mixture-dependent, with a measurable crossover lambda*. One
paragraph, framed as the perceptual reading of the networking result, no
in-vivo claims.

**Future-work note (one sentence, scoped):** the in-vivo instantiation
(metabolic budget as C, two task-consumers of one percept, predicted
ranking flip) is a designable cell in the house discipline; it is future
work and is NOT claimed as a law. The 'Law of Budget-Constrained
Observation' framing (law.txt, 2026-08-27) is retired as a naming: its
single-observer axioms are prior art (above), its fidelity-failure axiom
is Paper IV, and its defensible kernel IS this paper's two-observer
corollary.

Distinguish from: Simpson's aggregation paradox (formal reversal conditions
exist, e.g. Front. Appl. Math. Stat. 9:1169164, doi:10.3389/fams.2023.1169164);
Pareto incomparability; subgroup fairness / heterogeneous treatment effects;
rank reversal in multi-criteria decision making. The defensible novelty is the
preregistered, cross-domain, networking-substrate evidence with a predictive
diagnostic (measured gradients → registered predictions → graded outcomes), not
the discovery that aggregation can reverse rankings.

## Structure (per review)

1. Definition: consumer-conditional policy reversal.
2. Sensitivity condition and mixture crossover λ*.
3. Registered protocol: cost matching, prediction-first, grading.
4. Optical inversion + phase diagram.
5. Radio inversion + phase diagram.
6. Controls: aligned-sensitivity (threshold-pair) and far-from-threshold cells.
7. Goodput, policy selection, operational implications.
8. Limitations; aggregation/fairness literature.
Appendix: evidence ledger incl. grid/LLM/ZK negatives and pilot trails.

## Venue mechanics

- SIGMETRICS is double-anonymous: anonymize cell names and the repository
  citation (anonymous artifact link), and disclose the WCNC/OFC submissions
  through the venue's related-work process.
- POMACS format; artifact evaluation is a strength given the sealed records.

## Rules

- No numbers until the 2026-08-27 seals land; graded numbers only.
- The λ*, gradient, cost-matched, and phase-diagram cells are NEW sealed work:
  family → shakedown → prereg → cooled seal → graded, per house discipline.
- Conference papers keep only their pointer sentences.
- House prose style per the academic-paper skill.
