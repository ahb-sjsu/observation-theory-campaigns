# hyperbolic attention bias

**id.** hyperbolic-attention-bias
**kind.** instrument
**volume.** Geometric Communication, Volume 7 of the Geometric Series

## definition

A term $B_{geo}(i, j) = -\alpha \, d_{\mathbb{B}}(e_i, e_j)$ added to a transformer's attention logits beside the position bias. Here $e_i$ and $e_j$ are Poincare ball embeddings of the tokens at positions i and j, $d_{\mathbb{B}}$ is the Poincare distance, and $\alpha$ is a learnable scalar. Tokens with nearby embeddings attend to each other more.

**Example.** At the initial scale of 0.1, token pairs at hyperbolic distances 2 and 5 receive biases of -0.2 and -0.5, so the nearer pair gets more attention. The module adds 384 times 32 plus 1 = 12,289 parameters, as the volume prints.

## equation

none

## conditions

- In the cuneiform model the embeddings are learnable, 32-dimensional, one for each of ByT5's 384 byte tokens, with the curvature parameter c fixed at 1.0 and the scale initialised to 0.1. The bias enters the first four encoder layers.
- The bias is monotonically decreasing in hyperbolic distance when the scale is positive (Proposition 5.5).
- The ablation is reported as qualitative trends. A footnote of Chapter 9 says final numbers are not reported because they depend on seed, hardware and session, and the validation split has about 156 examples.
- Chapter 9 lists what was not measured. Supplementary data and augmentation are confounded, the number of biased layers and the curvature were not varied, and the bias acts on bytes and not on signs.

Conditions are curated in `volumes/geometric-communication.toml` rather than read from a record.

## ledger

none. *standing.* A construction with an ablation that the volume reports only as relative trends. The volume's claim is a measurable improvement concentrated on rare and polysemous signs, with no score stated.

## first stated

Section 5.6.2, [`geometric-communication/manuscript/part_ii/ch05_hyperbolic_embeddings.md:254-262`](https://github.com/ahb-sjsu/geometric-communication/blob/22f0bb0/manuscript/part_ii/ch05_hyperbolic_embeddings.md#L254-L262), and Section 9.4.1, [`geometric-communication/manuscript/part_iv/ch09_cuneiform.md:116-122`](https://github.com/ahb-sjsu/geometric-communication/blob/22f0bb0/manuscript/part_iv/ch09_cuneiform.md#L116-L122). Online, [Geometric Communication](https://erisml.org/geometric-communication/ch05_hyperbolic_embeddings.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Communication*, Volume 7 of the Geometric Series.

## related

attention, hyperbolic-embedding-advantage-regime, translation-loop-residual, translation-error-decomposition, einstein-midpoint

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
