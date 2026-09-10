# geometric decision cost

**id.** geometric-decision-cost
**kind.** concept

## definition

The cost of an alternative in a decision task is the Mahalanobis distance between the encoding of the alternative and the encoding of the task's reference point under the inverse covariance. It is the pullback distance of the observer whose consumer is the scenario encoding, whose output metric is the inverse covariance, and whose inactive dimensions are directions in the kernel of that metric. The read operator of the program, written for a displacement from a reference point instead of for a code's error.

**Example.** In the ultimatum encoding an offer of 48 percent has social, identity, and epistemic displacements 0.373, 0.278, and 0.003 from the reference, so its cost is the square root of 0.373 squared over 78.26 plus 0.278 squared over 32.28 plus 0.003 squared over 0.01262, about 0.071, and no offer on the integer grid costs less.

**Known as, or related to prior art.** Mahalanobis, 1936, for the distance. Luce, 1959, for the logit choice rule the lottery predictions use. Kahneman and Tversky, 1979, for the six lottery problems, and Fehr and Schmidt, 1999, for the inequality-aversion baseline. The specialization is Corollary 2 of the observer-representation draft, which identifies this cost with the pullback of Theorem 1(b) and identifies nothing about the map from cost gaps to lottery frequencies beyond the rule as written.

## equation

none

## conditions

- For a discrete menu no Jacobian is needed and the cost is the exact pullback of the quadratic form through the encoding. On a continuous scenario manifold the local metric is the encoding's Jacobian transposed, times the inverse covariance, times the Jacobian, which is the read operator of `read-operator` with the inverse covariance as output metric, `geometric-observation/paper/observer-representation.tex:303-330`.
- The consumer is the hand-coded encoding of each task as a reference point and a menu of alternatives in nine dimensions, `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:339-376`, and the three active dimensions are a sparsity pattern of the metric chosen by a search, not a demonstrated budget of the reader.
- The three active variances are 78.26, 32.28, and 0.01262 on social impact, virtue and identity, and epistemic status. They were fitted on nine game targets by a search over every active set of size at most five, with a 20-point log grid from 0.01 to 100 for one and two dimensions and 5,000 seeded log-uniform draws on the same range for three or more, `eris-econ/src/eris_econ/structural_fuzz.py:94-186`. Candidate active sets were then ranked on all sixteen targets, `eris-econ/src/eris_econ/structural_fuzz.py:693-740`, so no lottery target is out of sample and the lottery matches are parameter reuse within a jointly selected architecture.
- The reference implementation, eris-econ 0.1.0, reproduces every reported prediction, 16 of 16 targets within tolerance at an unweighted mean absolute error of 2.70 percentage points and 3.95 on the six Ruggeri lottery items, `eris-econ/src/eris_econ/targets.py:338-461` and `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:692-722`. The calibration objective is a weighted mean absolute error, with weights 1 on the ultimatum mean, the dictator mean, and the responder threshold and 0.5 on the other game targets.
- Game predictions are cost minima on an integer percentage grid and involve no temperature. Lottery predictions are a binary logit whose temperature is the larger of 0.5 and 0.24 times the cost gap to the power 2.13, `eris-econ/src/eris_econ/targets.py:40-42`. That rule is not monotone above a cost gap of 1.41, four of the six lottery targets lie above it with gaps 3.48, 2.21, 2.24, and 2.21, and the ordering of the Allais problem against the strong-certainty problem is carried by the temperature and not by the geometry, since the encoding gives the Allais problem the larger gap while the data give it the higher risky-choice rate and no constant temperature reproduces both, `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:234-266`. The two temperature constants were set from those two targets.
- An inactive dimension is a direction in the kernel of the output metric. With the monetary dimension inactive, multiplying every stake by a constant leaves every prediction unchanged, and conversely a model whose predictions are unchanged for two distinct multipliers has no monetary weight, `geometric-observation/paper/observer-representation.tex:333-345`. The reference implementation also normalizes the monetary coordinate to the stake, so the encoding is stake-blind for every metric and a rejection of invariance refutes encoding and metric together.
- On the high-stakes ultimatum data of Andersen, Ertac, Gneezy, Hoffman, and List, collected in eight villages of Meghalaya in northeast India with 458 responders and stakes from 20 to 20,000 rupees against an average yearly income of about 17,000, three pre-specified tests reject invariance, Kruskal-Wallis H 60.7 at p 4.17e-13, chi-squared 16.18 at p 0.0010, and a likelihood-ratio test of a logit with a log-stake term at p 8.77e-5 with AIC falling from 584.9 to 571.5, `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:1005-1019`. The calibrated model predicts invariance and that prediction fails. The result motivates and does not test a monetary coordinate in absolute or income units with finite sensitivity, and no stake at which invariance fails is located, `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:1031-1043`.
- The fitted model is not a strong-utility model, because the Allais problem has both a larger cost gap and a higher risky-choice rate than the strong-certainty problem. On binary menus it predicts nothing outside the random-utility class. The non-reducibility theorem of the observer-representation draft concerns the budgeted observer whose read subspace is selected from the menu, and not this model.
- The cumulative-prospect-theory baseline passes all six lottery problems at a mean absolute error of 5.7 percentage points with its canonical parameters, `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:1194-1221`, and the baseline used does not specify strategic behavior. The two models differ in flexibility and fitting protocol, so the difference in error is not a ranking of the theories.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

none

## first stated

The IEEE Transactions on Computational Social Systems paper, accepted 2026-09-06, `erisml-lib/docs/papers/foundations/submission/ieee-tcss/final_manuscript.tex:1-60`, and its reading as a pullback distance in `geometric-observation/paper/observer-representation.tex:303-330`.

## measurements

none

## failures and corrections

- [`erisml-lib/docs/papers/foundations/submission/ieee-tcss/FINAL-FILES-NOTES.md:60-71`](https://github.com/ahb-sjsu/erisml-lib/blob/7624301/docs/papers/foundations/submission/ieee-tcss/FINAL-FILES-NOTES.md#L60-L71) at 7624301. Round 2 (2026-09-07, after the owner's reviewer-style feedback on the final build) All three blockers and the temperature issue are addressed. Every number below was re-derived from eris-econ this session. 19. Holdout language removed everywhere. Because the reference implementation ranks candidate active sets on all sixteen targets, no lottery target is fully out of sample. The abstract, introduction, Section V.A, Section V.D (retitled "What Was Fitted or Selected on Which Targets"), Table VII (role column now "ranking only"), Section VI.F, the discussion, Limitation 5, and the conclusion now say: variances fitted on games, structure selected on the full benchmark, lottery results demonstrate cross-domain parameter reuse within a jointly selected architecture, not out-of-sample prediction. P11 is stated to test the reduction assumption rather than predict from distinct inputs. 20. CPT appendix corrected. The canonical absolute errors (4.7, 7.6, 5.3, 4.3, 3.4, 8.8 pp) are all within 10 pp, so canonical CPT passes 6/6 at MAE 5.7%, not 4/6. The accepted text's arithmetic was wrong. The "optimized" run (MAE 11.2%, claimed as the best MAE-minimizing solution while a 5.7% point was known) is withdrawn entirely, together with "pass-rate ceiling", "CPT does not exceed 4/6", and "both parameterizations fail P3 and P11". Table IX now reads CPT 6/6 at 5.7%, geometric 6/6 at 3.95% on the lottery subset, with a sentence that the two differ in flexibility and fitting protocol. "CPT cannot be applied to games" is now "the CPT baseline used here does not specify strategic behavior". The CPT fitting script was not found in any repo, so the canonical per-target numbers remain as reported in the accepted text and the pass count is corrected from those numbers. 21. Andersen interpretation made consistent with the stake-normalization caveat. Because the encoding normalizes money to the stake, no value of the monetary variance would predict a stake effect. The calibrated model predicts invariance and that prediction fails. Removed throughout: "as the model predicts", "becomes active at consequential stakes", "in the direction the theory anticipates", "locates the boundary". Abstract, introduction, contribution 4, Section VII.A (retitled "Money-Zero as a Falsifiable Prediction"), Fig. 5 caption ("prediction of the calibrated share-normalized model"), VII.B, VII.D, Limitation 8 ("Failure of invariance demonstrated, boundary not located"), and conclusion now say the result motivates but does not test an absolute- or income-scaled monetary coordinate with finite sensitivity. 22. Temperature nonmonotonicity reported. Turnover at cost gap 1.41. Cost gaps computed from eris-econ: P1 3.48, P3 2.21, P7 2.24, P11 2.21, P16 0.014, P17 0.013, so four of six targets sit on the nonmonotone branch. The encoding gives P1 a larger gap than P3 while the data show more risky choice on P1, and no constant temperature reproduces both (T = 0.5 gives P1 0.1%, T = 3.42 gives P3 34.4%). T

## invariance envelope

none declared


## machine checked

none

## used in

none

## related

geometric-evaluation-theory, mahalanobis-distance, read-operator, observer, consumer, output-metric, quotient, nuisance, whitening, softmax, read-direction

## see also

none

## status

Generated 2026-09-10 by `encyclopedia/generate.py`; book at observation-data-mining f3914f0; the commit of every record is listed in the encyclopedia's provenance.
