# Value boundary

**id.** value-boundary
**kind.** concept
**volume.** Geometric AI, Volume 11 of the Geometric Series

## definition

A codimension-1 submanifold of the value manifold that separates regions where different moral regimes apply. Crossing boundary k incurs a penalty beta_k. The sacred-value boundary has an infinite penalty, so no value on any other dimension can offset crossing it.

**Example.** With a minimum acceptable value of 0.6 and a penalty of 10, the constraint lets the trajectory fall to 0.6 less 1/10, which is 0.5. With an infinite penalty, as for a sacred value, the reciprocal is 0 and the floor is 0.6 exactly.

## equation

none

## conditions

- The volume names five boundaries for AI alignment. They are harm, deception, consent, privacy and sacred value.
- Only the sacred-value penalty is infinite. The harm penalty is high but finite, and the consent and privacy penalties vary with context.
- As a constraint on a trajectory, the attribute value on the dimension must stay at or above its minimum less the reciprocal of the penalty. No penalty value is measured in the volume, and the calibrated penalties of Chapter 14 belong to the ARIA-G narrative.

Conditions are curated in `volumes/geometric-ai.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status block of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, whose alignment thesis is theory at licensed strength and not validated measurement. It adds that no alignment instrument has been evaluated under the xbse admission filter, and the front matter says that ARIA, the system whose numbers fill the chapter tables, is fictional.

## first stated

Definition 4.2, Section 4.4.1, [`geometric-ai/manuscript/part_ii/ch04_value_manifold.md:164-178`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_ii/ch04_value_manifold.md#L164-L178). The constraint form is in Section 14.2.2, [`geometric-ai/manuscript/part_iv/ch14_constitutional_geometry.md:48-56`](https://github.com/ahb-sjsu/geometric-ai/blob/2cc8c63/manuscript/part_iv/ch14_constitutional_geometry.md#L48-L56). Online, [Geometric AI](https://erisml.org/geometric-ai/ch04_value_manifold.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric AI*, Volume 11 of the Geometric Series.

## related

value-manifold, absorbing-stratum, moral-stratification, constitutional-geometry

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
