# defect campaign, the recorded run

**id.** defect-campaign-null-result
**kind.** correction
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

The recorded run of the defect-prediction campaign did not recover the generator's structure. The best configuration contains the OO group, which the generator makes pure noise, and won on one correct positive prediction. The robustness index was exactly zero because the evaluation function reads only whether each parameter is below 1000.

**Example.** A configuration that finds no defective module misses the precision, recall and F1 targets by 70, 65 and 67 points, so its mean absolute error over the five targets is at least (70 + 65 + 67)/5 = 40.4. The numbers are from the volume's recorded run.

## equation

none

## conditions

- An earlier version of the chapter printed typical output that no run had produced and reported that the analysis recovered the generator's structure. The recorded output differs from it in almost every respect.
- The targets cannot be met on these data. The generator's own formula, used as an oracle, reaches an AUC of 54.5% against a target of 80%, and the 31 configurations span 43% to 59%, within two standard errors of chance.
- Over 20 redraws of the same generator 15 different configurations win, so the choice of best configuration carries no information about the generator.
- The run is exploratory. No prediction was registered before it.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* Measured on one recorded run of 16 November 2026, with an oracle bound and a 20-seed redraw. Exploratory, since no prediction was registered before the run (Section 21.8).

## first stated

Sections 19.4 and 19.5, [`geometric-methods/chapters/chapter-19-case-study-defect-prediction.md:183-221`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-19-case-study-defect-prediction.md#L183-L221), and Section 19.7, [`geometric-methods/chapters/chapter-19-case-study-defect-prediction.md:237-241`](https://github.com/ahb-sjsu/geometric-methods/blob/371478c/chapters/chapter-19-case-study-defect-prediction.md#L237-L241). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-19-case-study-defect-prediction.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

model-robustness-index, subset-enumeration, admissibility-checks, split, auroc, posited-versus-measured

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
