# gradient reversal layer

**id.** gradient-reversal-layer
**kind.** instrument
**volume.** Geometric Methods, Volume 1 of the Geometric Series

## definition

A layer between an encoder and a domain head that passes its input unchanged on the forward pass and multiplies the gradient by minus lambda on the backward pass. The domain head learns to predict the nuisance variable while the encoder is trained to make that prediction harder.

**Example.** With lambda 0.5, a domain-loss gradient of (2, -1) arriving at the layer reaches the encoder as (-1, 0.5), and the forward output equals the input.

**Known as, or related to prior art.** The domain-adversarial neural network of Ganin et al. (2016).

## equation

none

## conditions

- A domain head at chance means the representation defeats that discriminator. It does not mean the representation holds no information about the nuisance.
- The method fails when the nuisance and task subspaces coincide, when the domain head is too weak to detect the nuisance, or when the minimax training does not converge.
- Invariance is measured by a probe fitted after training on held-out data and by accuracy on a test set where the shortcut is broken. In the recorded run of Section 14.9 the probe recovered the nuisance 99.9% of the time under full reversal.

Conditions are curated in `volumes/geometric-methods.toml` rather than read from a record.

## ledger

none. *standing.* The README's status note of 2026-07-14 calls this volume the series' metrology discipline, a method that is normative and not a finding. Its Section 21.8 (November 2026) classes each result as proved, posited, or measured on a recorded run, and the tables of Chapters 1, 8, 9, 11 and 12 are posited illustrations.

## first stated

Section 14.2.1, [`geometric-methods/chapters/chapter-14-gradient-reversal.md:75-80`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-14-gradient-reversal.md#L75-L80), with the limit of what an equilibrium shows at [`geometric-methods/chapters/chapter-14-gradient-reversal.md:97-103`](https://github.com/ahb-sjsu/geometric-methods/blob/65452de/chapters/chapter-14-gradient-reversal.md#L97-L103). Online, [Geometric Methods](https://erisml.org/geometric-methods/chapter-14-gradient-reversal.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Methods*, Volume 1 of the Geometric Series.

## related

reversal-shortcut-experiment, nuisance, encoder, leakage, residualization

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
