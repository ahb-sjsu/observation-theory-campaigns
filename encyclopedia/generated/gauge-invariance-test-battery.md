# Assessment Gauge Invariance Test Battery (AGITB)

**id.** gauge-invariance-test-battery
**kind.** instrument
**volume.** Geometric Education, Volume 9 of the Geometric Series

## definition

Five parallel assessments of the same content, each varying one of examiner, format, language, time and context while holding the others fixed, each with a pass threshold. The composite score is GIS, equal to 1 minus the mean over the five tests of the smaller of 1 and the ratio of the absolute effect size to its threshold.

**Example.** If the five ratios of effect size to threshold are 0.5, 1.0, 0.2, 0.5 and 0.3, their mean is 2.5 divided by 5, which is 0.5, and GIS is 1 minus 0.5, which is 0.5. That is below 0.60, the band the appendix does not recommend for consequential decisions.

## equation

none

## conditions

- The thresholds are an effect size below 0.20 for format, language and context, below 0.15 for time, and a kappa of at least 0.80 or an intraclass correlation of at least 0.85 for examiners.
- The bands are GIS of 0.80 or more as adequate, 0.60 to 0.80 as moderate violation, and below 0.60 as not recommended for consequential decisions.
- The examiner test is scored by a reliability, where higher is better, and the other four by an effect size, where lower is better. The appendix does not say how the examiner test enters the composite formula.
- The appendix asks for at least 50 students per test and recommends ethics review. The battery is proposed, and the volume reports no administration of it.

Conditions are curated in `volumes/geometric-education.toml` rather than read from a record.

## ledger

none. *standing.* A proposed instrument. The README states that no education-domain instrument has been evaluated by the series' admission filter and that none currently passes its gate.

## first stated

Appendix C, Sections C.1 and C.2, [`geometric-education/manuscript/appendices/appendix_c_assessment.md:9-13`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/appendices/appendix_c_assessment.md#L9-L13), with the composite score in Section C.3, [`geometric-education/manuscript/appendices/appendix_c_assessment.md:65-75`](https://github.com/ahb-sjsu/geometric-education/blob/7bf76da/manuscript/appendices/appendix_c_assessment.md#L65-L75). Online, [Geometric Education](https://erisml.org/geometric-education/appendix_c_assessment.html).

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

assessment-gauge-invariance, educational-gauge-violation-tensor, threshold, gate, preregistration

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
