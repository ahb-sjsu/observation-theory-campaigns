# Moral parallel transport

**id.** moral-parallel-transport
**kind.** concept
**volume.** Geometric Ethics, Volume 2 of the Geometric Series

## definition

An obligation vector O is parallel-transported along a curve in the moral manifold when its covariant derivative along the curve vanishes, $\nabla_{\dot\gamma} O = 0$. Given the obligation at the start, the equations fix a unique obligation at every point of the curve. The volume reads it as faithful maintenance of an obligation across changing circumstances.

**Example.** With all connection coefficients zero the transport equation reduces to dO/dt = 0, so an obligation with care component 0.5 arrives with care component 0.5. With nonzero coefficients the components change while the transported obligation is, geometrically, the same one.

**Known as, or related to prior art.** Parallel transport along a curve under an affine connection, from differential geometry.

## equation

none

## conditions

- It needs a moral connection, which is defined within each stratum only. Across a boundary the connection may be discontinuous and the junction conditions of Definition 13.6 apply.
- Satisfaction is constant along the curve only when the connection is the Levi-Civita connection of the moral metric and both the obligation and the interest are transported (Proposition 10.1).
- The mathematics is the standard definition. Which connection moral reasoning uses is not measured, and the volume states that curvature has not been directly measured.

Conditions are curated in `volumes/geometric-ethics.toml` rather than read from a record.

## ledger

none. *standing.* Appendix F lists Definition 10.2 as a Formal Definition (ledger GE-DEF-10-2, class definition). Proposition 10.1 is a Conditional Theorem whose ledger row GE-PROP-10-1 is exploratory.

## first stated

Definition 10.2, Section 10.4, [`geometric-ethics/chapter-10-moral-dynamics-parallel-transport-holonomy-and-th.html:235-251`](https://github.com/ahb-sjsu/geometric-ethics/blob/ca9f708/chapter-10-moral-dynamics-parallel-transport-holonomy-and-th.html#L235-L251), on the moral connection of Definition 10.1, [`geometric-ethics/chapter-10-moral-dynamics-parallel-transport-holonomy-and-th.html:131-144`](https://github.com/ahb-sjsu/geometric-ethics/blob/ca9f708/chapter-10-moral-dynamics-parallel-transport-holonomy-and-th.html#L131-L144). Online, [Geometric Ethics](https://erisml.org/book/chapter-10-moral-dynamics-parallel-transport-holonomy-and-th.html).

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

moral-holonomy, moral-manifold, moral-stratification, curvature, moral-noether-theorem

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
