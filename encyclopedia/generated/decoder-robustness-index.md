# Decoder Robustness Index (DRI)

**id.** decoder-robustness-index
**kind.** instrument
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

Perturb each signal with nine acoustic transforms at eleven intensities, re-extract the inter-click intervals, decode, and score each outcome by a graded distance $\omega$ that is 0 for an unchanged label and between 0.5 and 1 for a flip. The index is 0.5 times the mean of $\omega$ plus 0.3 times its 75th percentile plus 0.2 times its 95th percentile.

**Example.** A flip that changes tempo only scores 0.5 + 0.5 times 0.7/2.3, about 0.65, since the four weights sum to 2.3. Scores with mean 0.2, 75th percentile 0.5 and 95th percentile 1.0 give an index of 0.10 + 0.15 + 0.20 = 0.45. These scores are chosen for the arithmetic.

## equation

none

## conditions

- For a flip, $\omega$ is 0.5 plus 0.5 times the weighted share of differing features, with weights 1.0 for rhythm, 0.7 for tempo, 0.4 for rubato and 0.2 for ornamentation.
- The signals are synthesised click trains. A footnote says the results describe robustness to perturbation of the synthesis model and not robustness under real ocean acoustics.
- The decoder is a single nearest-centroid classifier fed by a peak-detection click detector. The 40% of crossings under time shift is reported as a weakness of that detector.
- The chapter prints the formula and per-transform rates. It prints no overall value of the index in the text.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A defined index applied once, to synthesised signals and one decoder. The chapter states both limits.

## first stated

Section 7.4.2, [`geometric-communication/manuscript/part_iii/ch07_whale_communication.md:136-170`](https://github.com/ahb-sjsu/geometric-communication/blob/8184f3a/manuscript/part_iii/ch07_whale_communication.md#L136-L170). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch07_whale_communication.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

model-robustness-index, coda-boundary-asymmetry, bond-index, percentile, decision-boundary

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
