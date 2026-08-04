#!/usr/bin/env bash
set -euo pipefail
pdflatex -interaction=nonstopmode -halt-on-error projection-fold-pair-creation.tex
bibtexu projection-fold-pair-creation || true
pdflatex -interaction=nonstopmode -halt-on-error projection-fold-pair-creation.tex
pdflatex -interaction=nonstopmode -halt-on-error projection-fold-pair-creation.tex
