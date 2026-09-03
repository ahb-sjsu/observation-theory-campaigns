# CR-ANN paper — "Reranking by the Consumer's Read"

Written 2026-09-03 on the graded record as it stands (owner directive). The
paper claims exactly what the record supports: the conditional dissociation
(both arms sealed), the two preregistered FAILs reported as executed, and the
magnitude identification (gain = retrieval headroom $\Phi$ at ~unit slope,
unforecastable from calibration at natural sizes).

## Evidence sources (every number traces here)

- `../README.md` — the six construction cells (synthetic +0.42; matched
  −0.019; PCA sweep +0.08→+0.41; length/caps; LaBSE moral; cross-lingual).
- `../PREREG-CR-ANN.md` + `../prereg/graded_result.json` +
  `../RESULTS-CR-ANN.md` — family V1, FAIL, post-mortem.
- `../PREREG-CR-ANN-V2.md` + `../prereg/graded_v2.json` +
  `../RESULTS-CR-ANN-V2.md` — family V2, FAIL.
- `../CONVERSION-DETERMINANT.md` + `../prereg/conversion_pm.json` — the
  determinant study; Figure 1 regenerates from it
  (`build/fig_gain_vs_phi.py`).

## Build

MiKTeX: `pdflatex cr_ann_paper.tex` (twice). Figure:
`python build/fig_gain_vs_phi.py` (reads `../prereg/conversion_pm.json`).
5 pages, article class as a local placeholder; retarget class at venue
choice.

## Venue candidates (owner decision)

- TMLR (measurement + honest-negatives culture fits; no page pressure)
- SIGIR / ECIR short or resource track (the IR audience for the reranking
  surface; delineation vs learned rerankers is in Related Work)
- An ML evaluation/benchmarks venue (the two-FAIL discipline is the story)

## Finalization checklist

- [ ] Owner email in the author block.
- [ ] `% verify vol/pages on final` on kaski2001, peltonen2004,
      elmachtoub2022, joshiboyd2009 (venna2010 verified against JMLR
      2026-09-03; arXiv:2506.01599 flagged on the watch-list, cite only if
      the latent-alignment contrast enters).
- [ ] Repository/DOI pointer in the Reproducibility section once the branch
      merges (currently the campaign branch).
- [ ] Venue class swap + length pass.
- [ ] Owner submits; nothing here is submitted by tooling.
