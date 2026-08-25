# OFC paper — rendered PDF + DOCX deliverables

These are **renderings** of `../ofc-qot.tex` for sharing/review, produced locally
because the official Optica meeting class (`opticameet3.sty` / `opticajnl.bst`) is
Overleaf-only and not redistributed here.

| File | What |
|---|---|
| `ofc-qot-preview.pdf` | PDF rendering (standard `article` twocolumn, ~2 pp) |
| `ofc-qot-preview.docx` | Word rendering (pandoc; both figures embedded as 300-dpi PNG) |
| `ofc-qot-preview.tex` | The portable source (article class, PNG figures) |
| `ml_cliff.png`, `fc_footprint.png` | 300-dpi raster figures for the DOCX |

**Content is identical to the canonical `../ofc-qot.tex`** — same title, abstract,
sections, and figures. Every number is sealed-and-graded (XPROTO-QOT + XPROTO-QOT-ML,
sealed 2026-08-25, both PASS) or deterministic (§3.2 capacity on real SNDlib
janos-us-ca; §3.3 refresh floor). Only the *typesetting* differs from the Optica class.

**For the actual OFC 2027 submission**, build `../ofc-qot.tex` in Overleaf's Optica
meeting template (drop in `opticameet3.sty` + `opticajnl.bst`), which enforces the
official 2-column layout, and verify the ≤3 pp / ≤2 MB / ≤35-word-abstract limits.

Rebuild:

    # figures (qot venv, numpy<2)
    python ../../analysis/qot/plot_fig2.py ../../analysis/qot/QOTML-preds.json ml_cliff.png
    python ../../analysis/qot/plot_fig1.py ../../analysis/qot/QOT-paths.json fc_footprint.png
    pdflatex ofc-qot-preview.tex && pdflatex ofc-qot-preview.tex   # PDF
    pandoc ofc-qot-preview.tex -o ofc-qot-preview.docx --resource-path=.  # DOCX
