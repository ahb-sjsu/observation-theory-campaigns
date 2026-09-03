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

## Venue: TMLR (owner decision 2026-09-03)

Converted to the official TMLR style (tmlr.sty/bst fetched from
JmlrOrg/tmlr-style-file 2026-09-03; files committed beside the tex). Builds
5 pp in submission mode: the style anonymizes the author block by default
("Anonymous authors, paper under double-blind review"); switch to
`\usepackage[accepted]{tmlr}` at camera-ready to restore the name. The
Reproducibility section promises an anonymized record copy at submission and
the repository link on acceptance.

## Finalization checklist

- [x] References verified 2026-09-03 (DBLP + JMLR + Boyd's page): Kaski
      IEEE TNN 12(4):936-947 2001; Peltonen Neural Networks 17(8-9):1087-1100
      2004; Venna JMLR 11:451-490 2010; Elmachtoub Management Science
      68(1):9-26 2022; Joshi-Boyd IEEE TSP 57(2):451-462 2009. No % verify
      flags remain.
- [x] TMLR class conversion; natbib author-year bibliography; builds clean.
- [ ] Owner email in the author block (renders only at camera-ready).
- [ ] Prepare the anonymized records bundle for submission (strip owner
      names/paths from the JSON copies).
- [ ] OpenReview submission by the owner; nothing here is submitted by
      tooling.
