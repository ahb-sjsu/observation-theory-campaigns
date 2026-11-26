# Evidence status of the moral metric

**id.** moral-metric-evidence-status
**kind.** result
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

The volume's statement, added in v1.28, that the moral metric is untested. No measurement it reports shows a metric, set by hand or learned from data, predicting moral judgements better than the boundary penalties alone. The one registered test of the question was void, so it neither supports nor refutes the metric.

**Example.** On 1,165 held-out posts no predictor beat the average verdict, so the registered comparison was not graded. The embeddings explain at most 4 percent of verdict variance where about 86 percent is not vote noise, so a missing metric effect could not be told from a present one.

## equation

none

## conditions

- The registered test (prereg-precedent-v1, run in November 2026) asked whether a metric learned on sentence embeddings improves prediction of community verdicts on 1,165 held-out forum posts, beyond two gates read from the text and the nearest earlier cases.
- No predictor in that run did better than the average verdict. The registration had fixed that outcome in advance as the sign of an instrument that reads no signal, so the run is void.
- A later check, not registered and made on the training posts, found that the embeddings explain between 2.5 and 4 percent of the variance of the verdicts while about 86 percent of that variance is not vote noise. The volume concludes the test could not have detected a metric effect of ordinary size.
- The statement covers the predictive value of the metric. It does not withdraw the boundaries, the gates or the proved results.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* A statement of absence of evidence, in the volume's words a model whose metric has not been tested. The void run is neither a pass nor a refutation, and the ledger has no row for the claim.

## first stated

Section 8.10a, paragraph headed Evidence status of the metric, [`geometric-ethics/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html:1305-1324`](https://github.com/ahb-sjsu/geometric-ethics/blob/401b9a5/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html#L1305-L1324), and limitation 8 of Section 17.7, [`geometric-ethics/chapter-17-empirical-evidence-for-geometric-ethics.html:973-978`](https://github.com/ahb-sjsu/geometric-ethics/blob/401b9a5/chapter-17-empirical-evidence-for-geometric-ethics.html#L973-L978). Online, [Geometric Ethics](https://erisml.org/book/chapter-8-stratification-boundaries-thresholds-and-phase-tra.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Ethics*, Volume 2 of the Geometric Series.

## related

moral-decision-edge-weight, moral-decision-complex, preregistration, posited-versus-measured, metric, null-model

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
