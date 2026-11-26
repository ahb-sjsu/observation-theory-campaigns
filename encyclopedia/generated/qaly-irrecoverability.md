# QALY Irrecoverability Theorem

**id.** qaly-irrecoverability
**kind.** result
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

Any continuous function that maps the nine-component clinical-moral attribute vector to one scalar value is not injective, has no left inverse, and yields a value-maximizing path that can differ from the clinical geodesic by more than any amount fixed in advance. For the standard QALY, which depends on the outcomes score alone, all variation on the other eight dimensions is lost.

**Example.** The standard QALY reads the outcomes score only. Two patients with outcomes 0.5, one with trust 0.2 and one with trust 0.9, get the same value, and no function of that value can tell them apart. The kernel has dimension 9 - 1 = 8, which is the volume's count.

**Known as, or related to prior art.** The rank-nullity theorem applied to a map from nine dimensions to one. The volume gives it as the clinical form of the Scalar Irrecoverability Theorem of Geometric Reasoning.

## equation

none

## conditions

- The proof of non-injectivity uses rank and nullity where the function is differentiable and a dimension count where it is continuous.
- The unbounded divergence is shown by a constructed three-vertex complex in which the path the scalar prefers crosses a boundary whose penalty can be made as large as wished.
- Proposition 5.1 gives the case where the scalar is adequate. It needs a decision that activates mainly outcomes, a population homogeneous on the other eight dimensions, and no boundary crossed.
- The result is about loss of information under the map. That the nine dimensions are the right description of a clinical state is the volume's posited model.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* A theorem the volume proves in Section 5.2. Section 18.9 lists it as proved mathematically and consistent with the QALY critique literature.

## first stated

Theorem 5.1, [`geometric-medicine/manuscript/part_ii/ch05_qaly_irrecoverability.md:34-40`](https://github.com/ahb-sjsu/geometric-medicine/blob/6c8c4c4/manuscript/part_ii/ch05_qaly_irrecoverability.md#L34-L40), with the kernel of the standard QALY in Corollary 5.1, [`geometric-medicine/manuscript/part_ii/ch05_qaly_irrecoverability.md:70-74`](https://github.com/ahb-sjsu/geometric-medicine/blob/6c8c4c4/manuscript/part_ii/ch05_qaly_irrecoverability.md#L70-L74). Previewed as Theorem 1.1. Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch05_qaly_irrecoverability.html).

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

scalar-irrecoverability, moral-scalar-irrecoverability, null-space, qaly-adequacy-conditions, clinical-geodesic, economic-scalar-irrecoverability

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
