# Collective geodesic

**id.** collective-geodesic
**kind.** concept
**volume.** Geometric Medicine, Volume 8 of the Geometric Series

## definition

For a population, the allocation of a resource such as vaccine doses that minimizes the sum of clinical friction over all its members. It differs from the Nash equilibrium of individual geodesics, in which each member minimizes their own friction without counting effects on others.

**Example.** A healthy young adult bears friction 1 from vaccination and friction 0 from refusing, and vaccination lowers the friction of contacts by 3 in total. Alone the adult refuses. Summed over the population vaccination changes total friction by 1 - 3 = -2, so the collective geodesic includes it. The numbers are arithmetic from the definition.

**Known as, or related to prior art.** The gap between a social optimum and a Nash equilibrium under externalities.

## equation

none

## conditions

- Theorem 11.1 says the two diverge whenever individual decisions create externalities on the social dimension, and that the divergence is proportional to the herd immunity contribution.
- The theorem is stated without a proof.
- Friction here inherits the unestimated covariance matrix and boundary penalties.

Conditions are curated in `volumes/geometric-medicine.toml` rather than read from a record.

## ledger

none. *standing.* The README's epistemic-status note of 2026-07-14 calls this volume a posited framework, speculative theory awaiting instruments, and says a clinical instrument is plausible but has not been built or gated. Its Section 18.8 says the covariance matrix has not been estimated and the clinical Bond Index has not been computed from clinical data, so every number in these entries is an illustration unless the entry says otherwise.

## first stated

Definition 11.1 and Theorem 11.1, [`geometric-medicine/manuscript/part_iv/ch11_allocation.md:23-37`](https://github.com/ahb-sjsu/geometric-medicine/blob/ecde39b/manuscript/part_iv/ch11_allocation.md#L23-L37). Online, [Geometric Medicine](https://erisml.org/geometric-medicine/ch11_allocation.html).

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

clinical-geodesic, clinical-friction, public-health-mandate-justification, bge-nash-relationship, bond-geodesic-equilibrium

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining bccca4f; the commit of every record is listed in the encyclopedia's provenance.
