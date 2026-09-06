# inverted file

**id.** inverted-file
**kind.** instrument

## definition

An index that partitions vectors into cells by k-means and answers a query by searching only the cells nearest to it. The number of cells searched is the probe count. Chapter 11.

## equation

Book equation 11.3.

    \begin{gathered} \mathrm{recall}@k=\frac{\big|\text{returned top-}k\ \cap\ \text{true top-}k\big|}{k}, \\ \text{true top-}k\text{ computed from the uncompressed vectors}. \end{gathered}

Book equation 11.4.

    \text{directions resolved}(k)=\begin{cases}1\ \text{or}\ 2,& k<d\\[2pt] \operatorname{rank}P_C,& k\ge d\end{cases}\qquad \text{cost}=2d\ \text{consumer calls per operating point}.

## ledger

- GO-3. The certificate's vacuity threshold predicts where single-stage retrieval dies. `[demonstrated]`. `geometric-observation/claims/LEDGER.md:65` at 01e53bc.
- NEG-14. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe). `[refuted]`. `geometric-observation/claims/LEDGER.md:108` at 01e53bc.

## first stated

Sivic and Zisserman's video Google and the IVF index of Jégou, Douze, and Schmid, as chapter 11 section 11.3 of *Data Mining as Observation* presents them, with the program's probe sweeps in openvector-bench.

## measurements

| Where the book states it | Numbers, as the book's sources table records them | Source |
|---|---|---|
| chapter 11 section 11.2 | the calibration-time probe and the streaming monitor | `turboquant-pro\turboquant_pro\a2_probe.py:315-438`; `turboquant-pro\tests\test_a2_probe.py` |
| chapter 11 section 11.7 | GO-1 overlap 0.936 vs 0.059, flip 12 of 12, reconstruction 0.40 | `geometric-observation\claims\LEDGER.md` row GO-1; `geometric-observation\chapters\ch10_the_blind_probe.md:34-52` |
| chapter 12 section 12.3 | 035 miss 0.773 vs 0.757, identifiability diagnosis, 036 blind probe r 32, 0.779 vs 0.771, 200 of 200, recon 0.220 vs 0.584, 039 virgin split 0.796 vs 0.780, margin 0.008 to 0.016, edges baseline | `geometric-observation\chapters\ch10_the_blind_probe.md:53-90`; `geometric-observation\claims\LEDGER.md` rows GO-B-legal 035 and 036, GO-P-2026-039 |
| chapter 12 section 12.3 | 041 non-oracle, frozen LSA TF-IDF to SVD 100 train-only, AUROC 0.975 vs 0.910, flip tied, magnitude overshot, partial | `geometric-observation\chapters\ch10_the_blind_probe.md:100-118`; `geometric-observation\claims\LEDGER.md` row GO-B-blind 041 |
| chapter 14 section 14.8 | quantum falsified, 320 probes, contextuality zero, DOI 10.5281/zenodo.20660110 | `non-abelian-sqnd\README.md:5-22`; `sqnd-probe\README.md:12-20`; `sqnd-probe\CITATION.cff:16` |

## failures and corrections

- NEG-14, `[refuted]`. (GO-P-2026-037, prospective) `a2_probe.median_unit_displacement` is a single-statistic predictor of the flip regime (unit_disp ≷ 1.0 ⇒ generic-polar-flip vs needs-blind-probe).

## conditions

- An index that partitions vectors into cells by k-means and searches only the cells nearest the query. Probing more cells never loses a candidate, a neighbour is found exactly when its cell is probed, the scanned fraction is the probed cells' size over the corpus, and with equal cells it is the probe count over the cell count.
- The recall at one probe against eight in the chapter's table is a measurement, and the vacuity threshold of the certificate predicts where single-stage retrieval dies, which is the ledger's demonstrated row.

Conditions are curated in `entries.toml` rather than read from a record.

## machine checked

`lean/DataMiningAsObservation/InvertedFile.lean`, theorems `scanned_mono`, `found_iff`, `scannedFraction_mem_unit`, `equal_cells`, `scanned_univ`, at observation-data-mining 424e077.

## used in

*Data Mining as Observation* chapters 0, 11, 13, 14.

## related

recall-at-k, product-quantization, vacuity-threshold, anti-hub

## status

Generated 2026-09-05 by `encyclopedia/generate.py` from geometric-observation 01e53bc, observation-theory-campaigns 55ee1c6, theory-radar 37c4e6c, observation-data-mining 424e077, turboquant-pro 856c4cb, gtc-prototype 328741f, readscope c8d0289.
