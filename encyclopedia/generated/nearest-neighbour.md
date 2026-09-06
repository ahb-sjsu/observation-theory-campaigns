# nearest neighbour

**id.** nearest-neighbour
**kind.** concept

## definition

A row at minimal distance from a query. A strictly increasing transform of the distance names the same nearest neighbours, so the classifier reads the distance's order and nothing else. Chapter 6.

## equation

Book equation 3.1.

    \begin{gathered} d_O(u)=u^{\top}\Sigma\,u, \qquad u=(\cos15^\circ,\ \sin15^\circ), \\ \Sigma_1=\operatorname{diag}(0.3,1.7),\ \Sigma_2=\operatorname{diag}(1.7,0.3), \qquad d_O=0.394\ \text{vs}\ 1.606. \end{gathered}

Book equation 0.19.

    L=I-D^{-1/2}AD^{-1/2},\qquad D=\operatorname{diag}(d_1,\dots,d_n),\qquad L\,u_k=\lambda_k u_k,\ \ 0=\lambda_1\le\lambda_2\le\cdots.

Book equation 10.3.

    N_k(x\mid Q)=\big|\{q\in Q:\ x\in\operatorname{top}_k(q)\}\big|,\qquad \text{anti-hub}:\ N_k(x)=0.

## ledger

- NEG-11. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain. `[refuted]`. `geometric-observation/claims/LEDGER.md:104` at 9f3829f.

## first stated

Cover and Hart, nearest neighbor pattern classification, 1967, as chapter 6 section 6.1 of *Data Mining as Observation* reads it, with the neighbour lists of `openvector-bench/openvector_bench/hubness.py:41-100`.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 3 section 3.5 | 78 vs 369, density correlation about 0.67, 8 percent vs 34 percent, centering vs mutual-proximity rescaling | `turboquant-pro\docs\HUBNESS_PRIMER.md:38-59,140-160` |
| chapter 3 section 3.5 | Poisson null, hub excess, budget parameter | `openvector-bench\openvector_bench\hubness.py:41-100` |

## failures and corrections

- NEG-11, `[refuted]`. (GO-5, prospective ×4) The α=1 density/hubness quotient decisively and density-specifically restores invariant fidelity in a non-spectral domain.

## conditions

- A row at minimal distance from a query under a chosen distance. A strictly increasing transform of the distance names the same nearest neighbours, so a nearest-neighbour classifier reads the distance's order and nothing else, a row is its own nearest neighbour, and two nearest neighbours sit at the same distance.
- Under Euclidean distance the classifier reads every standardized coordinate equally and under cosine it reads the angle, so it inherits the distance's quotient, and the rows that appear in many neighbour lists are the hubs.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/NearestNeighbour.lean`, theorems `nearest_comp`, `nearest_smul`, `self_nearest`, `nearest_same_distance`, at observation-data-mining af776fd.

`lean/DataMiningAsObservation/Graph.lean`, theorems `outDegree`, `mutual_symm`, `mutual_sub`, `mutualNbrs_card_le`, `mem_mutualNbrs`, at observation-data-mining af776fd.

## used in

*Data Mining as Observation* chapters 0, 3, 6, 8, 10, 11, 12.

## related

neighbourhood-graph, hub, recall-at-k, euclidean-distance, cosine

## status

Generated 2026-09-06 by `encyclopedia/generate.py` from geometric-observation 9f3829f, observation-theory-campaigns 9d86211, theory-radar 37c4e6c, observation-data-mining af776fd, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
