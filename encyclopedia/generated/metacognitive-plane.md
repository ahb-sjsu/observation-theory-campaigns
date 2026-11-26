# Metacognitive plane

**id.** metacognitive-plane
**kind.** concept
**volume.** Geometric Reasoning, Volume 3 of the Geometric Series

## definition

The unit square of points $(M_3, M_4)$, where $M_3$ is the self-monitoring score and $M_4$ is the strategy-selection or effort-scaling score. Scores above 0.5 on both axes are Quadrant I, full control. High $M_3$ alone is Quadrant II, aware but passive. High $M_4$ alone is Quadrant IV, reactive but blind.

**Example.** The volume's scores place one model at (0.094, 0.723), in Quadrant IV with a control bound of 0.094, and another at (0.700, 0.350), in Quadrant II with a bound of 0.350.

## equation

none

## conditions

- The plane and its quadrants are tagged a modeling axiom. The scores placed in it are benchmark measurements on five models.
- The volume bounds effective control by the smaller of the two scores, treating self-monitoring as a sensor and strategy selection as an actuator.
- The volume states that the two scores are strongly anti-correlated in the tested models. The five pairs in its Table 7.2 give a correlation of about -0.98, so the axes are not independent in its data.
- Four of the five tested models lie in Quadrants II and IV. The fifth scores 0.450 and 0.488 and lies just inside Quadrant III under the 0.5 cut.

Conditions are curated in `volumes/geometric-reasoning.toml` rather than read from a record.

## ledger

none. *standing.* A posited two-axis diagnostic filled with measured scores. The claim that Quadrant I is empty agrees with the tabulated scores. Since the correction of 2026-11-26 the volume no longer calls the axes independent and places one model in Quadrant III.

## first stated

Definition 9.2, [`geometric-reasoning/chapters/ch09_metacognition_as_search_control.md:444-458`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch09_metacognition_as_search_control.md#L444-L458), introduced in Section 9.9, [`geometric-reasoning/chapters/ch09_metacognition_as_search_control.md:325-339`](https://github.com/ahb-sjsu/geometric-reasoning/blob/149995b/chapters/ch09_metacognition_as_search_control.md#L325-L339). Online, [Geometric Reasoning](https://erisml.org/geometric-reasoning/ch09_metacognition_as_search_control.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Reasoning*, Volume 3 of the Geometric Series.

## related

prompt-recovery-ceiling, benchmark-scalar-irrecoverability, correlation, expected-calibration-error, calibration

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
