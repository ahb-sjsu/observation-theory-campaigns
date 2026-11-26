# inverse flavor problem

**id.** inverse-flavor-problem
**kind.** instrument
**volume.** Geometric Gastronomy, Volume 12 of the Geometric Series

## definition

Given a target flavor $\mathbf{f}^\star$, a palette matrix $B$ and a positive-definite metric matrix $M$, choose nonnegative doses $\mathbf{x}$ to minimize $(B\mathbf{x} - \mathbf{f}^\star)^\top M (B\mathbf{x} - \mathbf{f}^\star)$ under a cost ceiling and admissibility constraints. It is a convex quadratic program. Zero distance is reachable exactly when the target lies in the admissible hull of the palette.

**Example.** With palette vectors (1, 0) and (0, 1), the identity as metric and no other constraint, the target (2, 3) is reached exactly by doses (2, 3). The target (2, -1) is outside the hull, the best doses are (2, 0), and the residual distance is 1. The numbers are illustrative.

**Known as, or related to prior art.** Nonnegative least squares and convex quadratic programming.

## equation

none

## conditions

- The program is a modeling axiom and the reachability statement is tagged a theorem. It is stated for the linear-mixing regime with a positive-definite metric and a convex admissible set, and the volume's proof is one sentence from strict convexity in the flavor point $B\mathbf{x}$. The minimum is attained at a unique flavor point, and the dose vector is unique only when the palette vectors are linearly independent.
- Convexity fails where mixing is nonlinear, in synergy and antagonism and in threshold and saturation effects at high dose. There the program is a local model, refined by panel-tested iterations.
- When the target lies outside the reachable polytope, the residual distance is what the volume calls the artificiality gap, and the active constraints say which limit blocks a closer match.
- Masking, mimicry, cost-limited formulation and personalization are presented as the same program under different targets, palettes, constraints and metrics.

Conditions are curated in `volumes/geometric-gastronomy.toml` rather than read from a record.

## ledger

none. *standing.* A theorem in the volume's tagging, with a one-sentence proof and no machine-checked proof. The metric matrix and palette vectors it needs are posited, and the volume conjectures that measuring the metric for a given eater is the binding constraint.

## first stated

Section 13.4, [`geometric-gastronomy/chapters/ch13_designing_flavors.md:68-76`](https://github.com/ahb-sjsu/geometric-gastronomy/blob/1b6657d/chapters/ch13_designing_flavors.md#L68-L76). Online, [Geometric Gastronomy](https://erisml.org/geometric-gastronomy/ch13_designing_flavors.html).

## measurements

none

## failures and corrections

none

## invariance envelope

none declared


## machine checked

none

## used in

*Geometric Gastronomy*, Volume 12 of the Geometric Series.

## related

flavor-riemannian-metric, mahalanobis-distance, positive-definite, quadratic-form, receptor-basis-rotation, substitution-distance

## see also

none

## status

Generated 2026-11-25 by `encyclopedia/generate.py`; book at observation-data-mining 736f790; the commit of every record is listed in the encyclopedia's provenance.
