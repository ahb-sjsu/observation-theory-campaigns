# Divergence of utilitarian and manifold-optimal triage

**id.** triage-divergence-theorem
**kind.** result
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

The allocation that maximizes total outcomes equals the allocation that minimizes total clinical friction when triage activates only the outcomes dimension and crosses no moral boundary. They differ when a boundary is crossed or another dimension is active, as in ventilator withdrawal, age-based deprioritization and the choice of a lottery between similar prognoses.

**Example.** One ventilator, a current patient and a new patient whose outcome gain from reallocation is worth 8. With an abandonment penalty of 15, the low end of the volume's typical range, and a trust penalty of 5, withdrawal costs 20 against a gain of 8, so the friction-minimizing allocation keeps the ventilator and the outcome-maximizing one moves it. The figures 8 and 5 are arithmetic from the statement.

## equation

none

## conditions

- Both allocations obey the same resource bound. The triage problem is a set of patients, one complex and one goal region per patient, and that bound.
- In the withdrawal case the allocations differ only when the abandonment and trust penalties exceed the outcome differential between the two patients.
- The proof is an argument from the form of the edge weight. The penalties it uses are not calibrated, and the trust and justice penalties are not among the five boundaries of Definition 4.3.
- The three predictions about clinician distress in Section 10.5 are described as consistent with the pandemic literature. No test of them is reported.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* A theorem with an argument given in Section 10.2. Its numerical content depends on boundary penalties that have not been estimated.

## first stated

Theorem 10.1, [`geometric-medicine/manuscript/part_iv/ch10_pandemic_triage.md:81-91`](https://github.com/ahb-sjsu/geometric-medicine/blob/6c8c4c4/manuscript/part_iv/ch10_pandemic_triage.md#L81-L91), on the triage problem of Definition 10.1, [`geometric-medicine/manuscript/part_iv/ch10_pandemic_triage.md:24-35`](https://github.com/ahb-sjsu/geometric-medicine/blob/6c8c4c4/manuscript/part_iv/ch10_pandemic_triage.md#L24-L35). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch10_pandemic_triage.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Medicine*, Volume 8 of the Geometric Series.

## related

forced-contraction, clinical-friction, clinical-moral-boundaries, qaly-adequacy-conditions, clinical-moral-injury, allocation

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
