# educational gauge violation tensor

**id.** educational-gauge-violation-tensor
**kind.** instrument
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

A matrix $V_{ij}$ whose row i is one of the five changes of instrument and whose column j is a score dimension, with a single column for a scalar score. The entry is the expected change in score j when the instrument is changed, $V_{ij} = E[A_j(x, I_i') - A_j(x, I_i)]$. A gauge-invariant assessment has every entry zero.

**Example.** The volume's estimated ranges for the SAT are 50 to 150 points for format, 80 to 200 for language, 10 to 30 for time and 50 to 100 for context. The lower ends sum to 190 and the upper ends to 480, which the volume rounds to 200 to 500.

## equation

none

## conditions

- The entries are expectations over students, taken with the learner state held fixed while the instrument changes.
- The SAT table gives estimated ranges with no source and no study behind them. The examiner row is marked not applicable because the test is machine-scored.
- The total violation is defined as the sum of absolute values across the changes. The volume puts it on the order of 200 to 500 SAT points.
- The volume proposes the measurement and reports no measured tensor.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments. No education-domain instrument has been evaluated by the series' admission filter, and Chapter 18 states that the six predictions of Section 16.3 have not been tested and that no method for estimating the learner metric has been validated at scale.

## first stated

Definition 9.2, [`geometric-education/manuscript/part_iii/ch09_gauge_invariance.md:97-103`](https://github.com/ahb-sjsu/geometric-education/blob/085dda1/manuscript/part_iii/ch09_gauge_invariance.md#L97-L103), with the table for the SAT at [`geometric-education/manuscript/part_iii/ch09_gauge_invariance.md:105-115`](https://github.com/ahb-sjsu/geometric-education/blob/085dda1/manuscript/part_iii/ch09_gauge_invariance.md#L105-L115). Online, [Geometric Education](https://erisml.org/geometric-education/ch09_gauge_invariance.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Education*, Volume 9 of the Geometric Series.

## related

gauge-violation-tensor, assessment-gauge-invariance, gauge-invariance-test-battery, economic-gauge-violation-tensor, expectation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
