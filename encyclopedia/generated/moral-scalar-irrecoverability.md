# Scalar Irrecoverability Theorem

**id.** moral-scalar-irrecoverability
**kind.** result
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

Any continuous map Q from the nine-dimensional moral attribute vector to one scalar is not injective, has no function that recovers the vector from the scalar, and in general gives a scalar-optimal path that differs from the geodesic on the full manifold by an amount no function of Q alone bounds.

**Example.** Let Q be the sum of the nine coordinates. The states (1, 0, 0, 0, 0, 0, 0, 0, 0) and (0, 1, 0, 0, 0, 0, 0, 0, 0) both map to 1, so no function of the value 1 can return both. The directions Q cannot see number 9 - 1 = 8.

## equation

none

## conditions

- Q must be continuous, and continuously differentiable where the proof uses its differential (corrected in v1.25). At a regular point the kernel of the differential has dimension at least 8.
- Part (iii) is stated in general. It does not say that every scalar rule gives a worse path in every case.
- The theorem counts dimensions of the attribute space. Its moral reading assumes the nine coordinates carry independent morally relevant variation, which Section 5.3 qualifies (effective rank 5.19 of 8 on text).

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Tagged Theorem (conditional on Definition 5.2) in the text as of v1.29, where earlier versions tagged it Proved, and listed as a Conditional Theorem in Appendix F. The volume says the mathematical implication is sound for a continuous Q and that the ethical consequent depends on the nine-dimensional chart, a modeling axiom. The ledger row GE-THM-15-1 has class exploratory, so the text and the ledger now agree. The row's scope note still describes the earlier tag, and the v1.29 change notes say it should gain a history entry.

## first stated

Theorem 15.1, Section 15.6, [`geometric-ethics/chapter-15-from-tensor-to-decision-the-philosophy-of-moral-c.html:409-423`](https://github.com/ahb-sjsu/geometric-ethics/blob/ca9f708/chapter-15-from-tensor-to-decision-the-philosophy-of-moral-c.html#L409-L423), with the proof at [`geometric-ethics/chapter-15-from-tensor-to-decision-the-philosophy-of-moral-c.html:424-442`](https://github.com/ahb-sjsu/geometric-ethics/blob/ca9f708/chapter-15-from-tensor-to-decision-the-philosophy-of-moral-c.html#L424-L442). Online, [Geometric Ethics](https://erisml.org/book/chapter-15-from-tensor-to-decision-the-philosophy-of-moral-c.html).

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

nine-dimension-moral-chart, moral-decision-complex, scalar-irrecoverability, null-space, rank, projection

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
