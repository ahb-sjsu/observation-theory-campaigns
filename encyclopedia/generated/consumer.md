# consumer

**id.** consumer
**kind.** concept

![The computation that reads the vector, the first element of the observer.](../figures/consumer.svg)

## definition

The function that acts on a vector, the first element of an observer. A softmax, a classifier, an index, a person reading a report. Chapter 1.

**Example.** A logistic classifier reading a 30-column table is a consumer; so is a cosine ranker, and so is a person reading a summary.

## equation

Book equation 1.1.

    O=(C,\ G,\ B).

## conditions

- A consumer is any computation that takes a vector in and gives an output out, a softmax, a classifier, an index, a person reading a report. The book's quantities are functions of the consumer, and two consumers with the same read operator are not thereby the same consumer.
- A selection consumer, a tree or a threshold, has zero sensitivity almost everywhere and is read by counting where it selects rather than by finite differences.

Conditions are curated in `entries.toml` rather than read from a record.

## ledger

- *measures.* GO-1 `[predicted]`. The consumer's invariant/nuisance split is identifiable ex ante from the consumer functional. [`geometric-observation/claims/LEDGER.md:62`](https://github.com/ahb-sjsu/geometric-observation/blob/e15d65f/claims/LEDGER.md#L62).
- *measures.* GO-EC-3 `[predicted]`. A read operator recovered from a black-box consumer by query-only finite-difference probing, composed with the Kalman covariance as tr(P̂_C Σ), prospectively selects sensors that improve the held-out consumer at matched budgets with probe … [`geometric-observation/claims/LEDGER.md:201`](https://github.com/ahb-sjsu/geometric-observation/blob/e15d65f/claims/LEDGER.md#L201).

## first stated

Volume 14, chapter 4, `geometric-observation/chapters/ch04_the_observer_triple.md:9-64` and its consumer table at lines 60-135, DOI 10.5281/zenodo.21776291.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 2 section 2.3 | refusal regimes, selection consumers read order, recurrences compound | [`readscope/readscope/regimes.py:1-60`](https://github.com/ahb-sjsu/readscope/blob/856e678/readscope/regimes.py#L1-L60) |
| chapter 6 section 6.1 | the classifier row of the consumer table, the output metric makes a different observer | [`geometric-observation/chapters/ch04_the_observer_triple.md:60-135`](https://github.com/ahb-sjsu/geometric-observation/blob/e15d65f/chapters/ch04_the_observer_triple.md#L60-L135) |
| chapter 6 section 6.1 | selection consumers have zero sensitivity almost everywhere | [`readscope/readscope/regimes.py:1-60`](https://github.com/ahb-sjsu/readscope/blob/856e678/readscope/regimes.py#L1-L60) |

## failures and corrections

none

## invariance envelope

**Failed, with witness.**

- OP:koopman-dictionary, choice of the pool pairs on which a consumer's Koopman dictionary is built, the top r pairs of a ranking for each r on a ladder, judged by the EDMD forecast error of the consumer's coordinates. Claim: Ranking the further pool pairs by READ gives a lower EDMD forecast error of the consumer's coordinates than the better of ENERGY and BALL, pooled by at least 0.01, in each graded lift (RFF and TEND), converging in resolution. `experiments/OPEN-PROBLEMS-TRACK.md, OP1 run record; experiments/OP/OP1/run_grade.json`. Witness: READ's pooled advantage -0.0046 with 34 of 60 cells behind (worst -0.077 at r_nu030_n192, cutoff 3, RFF, r = 2), RFF -0.020 and TEND +0.011; READ, ENERGY and BALL pool within 0.003 of each other (0.428, 0.429, 0.426), so the choice among the three moves the error less than the margin; E1 and N1 hold; on the three run worlds that returned (r_nu020_n192 lost to node failures at both attempts, reported and not graded). Absorbed by: declaration.
- OP:koopman-read-ke, the one secondary selector that reached OP1's seal, an ordering of the pool pairs scored by OP:koopman-dictionary's forecast error: READ with the consumer's response measured in the kinetic-energy norm. Claim: READ-KE's forecast error is below the better of ENERGY and BALL in more cells than the one-sided binomial at alpha 0.05 allows by chance. `experiments/OPEN-PROBLEMS-TRACK.md, OP1 run record; experiments/OP/OP1/run_grade.json`. Witness: ahead in 29 of 59 untied cells with 37 needed (one-sided p 0.60), pooled -0.0025; against READ 21 ahead, 17 behind, 22 tied; on the three run worlds that returned (r_nu020_n192 lost to node failures at both attempts, reported and not graded). Absorbed by: declaration.
- OP:mz-explicit-modes, choice of which pool pairs a Mori-Zwanzig reduced model of the consumer carries explicitly, the top r pairs of one of OP1's rankings for each r on a ladder, judged by the memory left in the consumer block. Claim: The modes READ makes explicit leave a smaller Mori-Zwanzig memory share than the better of ENERGY's and BALL's, pooled by at least 0.01, at each cutoff, converging in resolution. `experiments/OPEN-PROBLEMS-TRACK.md, OP2 run record; experiments/OP/OP2/run_grade.json`. Witness: pooled advantage -0.026 with 17 of 30 cells behind (worst -0.613 at r_nu020_n128, cutoff 3, r = 8), cutoff 3 -0.037 and cutoff 5 -0.015; at nu 0.03 alone READ is ahead (+0.013 at n = 128, +0.007 at n = 192) and BALL's pooled share is below READ's (0.529 against 0.537); E1, L1E and N1 hold; on the three run worlds that returned (r_nu020_n192 lost to node failures at both attempts, reported and not graded). Absorbed by: declaration.
- OP:mz-read-ke, the one secondary selector that reached OP2's seal, OP:koopman-read-ke's ordering, scored by OP:mz-explicit-modes's memory share. Claim: The modes READ-KE makes explicit leave a smaller memory share than the better of ENERGY's and BALL's in more cells than the one-sided binomial at alpha 0.05 allows by chance. `experiments/OPEN-PROBLEMS-TRACK.md, OP2 run record; experiments/OP/OP2/run_grade.json`. Witness: below the control in 12 of 30 cells with 20 needed (one-sided p 0.90), pooled -0.023; against READ 12 below, 10 above, 8 tied; on the three run worlds that returned (r_nu020_n192 lost to node failures at both attempts, reported and not graded). Absorbed by: declaration.


## machine checked

[`lean/DataMiningAsObservation/ReadOperator.lean`](https://github.com/ahb-sjsu/observation-data-mining/blob/736f790/lean/DataMiningAsObservation/ReadOperator.lean), theorems `rank_one_reads_one_direction`, `readOp_mulVec`, `quad_readOp`, `quad_readOp_nonneg`, `readOp_mulVec_eq_zero_iff`, `readOp_diag`, `readOp_offdiag`, `readOp_symm`, `readOp_neg`, `affine_const_along_nuisance`, `readOp_affine`, `readOp_sqLength_basis`, at observation-data-mining 736f790; what the check covers is stated in the book's [appendix C](https://github.com/ahb-sjsu/observation-data-mining/blob/736f790/chapters/machine_checked.md).

## used in

*Data Mining as Observation* primer L, chapters 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

## related

observer, read-operator, sensitivity, budget

## see also

Book equations stated beside the entry's terms, not defining it: 0.8.

Sources-table rows that share a record with the entry without naming it: chapter 1 section 1.2, chapter 6 section 6.2, chapter 11 section 11.7.

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
