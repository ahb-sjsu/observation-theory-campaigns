"""Regenerate build/ofc-qot-preview.tex body from the canonical ofc-qot.tex so the
two cannot drift. Keeps the preview's own preamble and banner; swaps figure
extensions to .png for pandoc; strips build comments on figure lines."""
import re

canon = open("ofc-qot.tex", encoding="utf-8").read()
prev = open("build/ofc-qot-preview.tex", encoding="utf-8").read()

# sync the abstract into the preview banner block so it cannot drift either
c_abs = canon.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0].strip()
prev = re.sub(r"(\\noindent\\textbf\{Abstract:\} ).*?(\n  \\end\{minipage\})",
              lambda m: m.group(1) + c_abs + m.group(2), prev, flags=re.S)

c_body = canon.split(r"\section{Introduction}", 1)[1].rsplit(r"\end{document}", 1)[0]
c_body = c_body.replace(".pdf}", ".png}")
c_body = re.sub(r"(\\includegraphics\[[^\]]*\]\{[^}]*\})\s*%[^\n]*", r"\1", c_body)
c_body = c_body.replace("\\begin{thebibliography}{9}",
                        "\\begin{thebibliography}{9}\n\\small")

p_head = prev.split(r"\section{Introduction}", 1)[0]
out = p_head + r"\section{Introduction}" + c_body + "\\end{document}\n"
open("build/ofc-qot-preview.tex", "w", encoding="utf-8").write(out)
print("preview synced from canonical,", len(out), "chars")
