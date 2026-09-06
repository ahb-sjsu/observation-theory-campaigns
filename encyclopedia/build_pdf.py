"""Build the encyclopedia as one PDF.

    python encyclopedia/build_pdf.py

The document has a preface that says what an entry is and how to read one, a table of
contents, the entries in alphabetical order under letter headings with cross-references
carrying page numbers, and back matter that lists the entries by kind, by chapter of the
book, by Lean file, and by ledger row, followed by the provenance of the records the entries
were built from. Every entry page comes from generated/ and is rewritten only in form:
indented equation lines become display math, the related ids become links, and the
per-entry status line is gathered into the provenance section. Output goes to
encyclopedia/pdf/Observation-Theory-Encyclopedia.pdf, stamped with the commit.
"""
import collections
import datetime
import glob
import os
import re
import shutil
import subprocess
import sys
import tomllib

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
BUILD = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "pdf")
os.makedirs(BUILD, exist_ok=True)
os.makedirs(OUT, exist_ok=True)


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


COMMIT = run(["git", "rev-parse", "--short", "HEAD"], REPO).stdout.strip()
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FIGPDF = os.path.join(BUILD, "figpdf")
os.makedirs(FIGPDF, exist_ok=True)
for svg in sorted(glob.glob(os.path.join(ROOT, "figures", "*.svg"))):
    name = os.path.basename(svg)[:-4]
    pdfp = os.path.join(FIGPDF, name + ".pdf")
    if os.path.exists(pdfp) and os.path.getmtime(pdfp) > os.path.getmtime(svg):
        continue
    s = open(svg, encoding="utf-8").read()
    w = int(re.search(r'width="(\d+)"', s).group(1))
    h = int(re.search(r'height="(\d+)"', s).group(1))
    html = (f'<html><head><style>@page{{size:{w}px {h}px;margin:0}} html,body{{margin:0;padding:0}} svg{{display:block}}</style></head>'
            f'<body>{s}</body></html>')
    hp = os.path.join(FIGPDF, name + ".html")
    open(hp, "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdfp}", "file:///" + hp.replace("\\", "/")],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if not os.path.exists(pdfp):
        print("figure conversion failed", name)
DATE = datetime.date.today().isoformat()

entries = tomllib.load(open(os.path.join(ROOT, "entries.toml"), "rb"))["entry"]


def sort_key(e):
    t = e["title"].lower()
    for pre in ("the ", "a ", "an "):
        if t.startswith(pre):
            t = t[len(pre):]
    return re.sub(r"[^a-z0-9]", "", t) or t


entries.sort(key=sort_key)
by_id = {e["id"]: e for e in entries}


def link(eid):
    e = by_id[eid]
    return f"[{e['title']}](#{eid}) (p.\\ \\pageref{{{eid}}})"


# ---------------------------------------------------------------- read the entry pages
pages = {}
status_lines = {}
used_in = collections.defaultdict(list)
for e in entries:
    p = os.path.join(ROOT, "generated", e["id"] + ".md")
    lines = open(p, encoding="utf-8").read().split("\n")
    assert lines[0].startswith("# "), p
    out = []
    section = None
    i = 0
    for line in lines[1:]:
        if line.startswith("## "):
            section = line[3:].strip()
            if section == "status":
                continue
            out.append("### " + section[0].upper() + section[1:])
            continue
        if section == "status":
            if line.strip():
                status_lines[e["id"]] = line.strip()
            continue
        if line.startswith("**id.**") or line.startswith("**kind.**"):
            continue
        if section == "related" and line.strip() and line.strip() != "none":
            ids = [x.strip() for x in line.split(",")]
            out.append("; ".join(link(x) for x in ids if x in by_id) + ".")
            continue
        if section == "used in":
            m = re.search(r"chapters? ([0-9, ]+)", line)
            if m:
                for c in re.findall(r"\d+", m.group(1)):
                    used_in[int(c)].append(e["id"])
        if line.startswith("    ") and "\\" in line:
            out.append("$$" + line.strip() + "$$")
            continue
        if line.startswith("![") and "](../figures/" in line:
            out.append(re.sub(r"\]\(\.\./figures/([a-z0-9-]+)\.svg\)", r"](figpdf/\1.pdf){width=100%}", line))
            continue
        if line.startswith("|---|---|---|"):
            out.append("|-----|--------|-------|")
            continue
        if line.startswith("|---|---|"):
            out.append("|----|--------|")
            continue
        line = line.replace("✅", "pass").replace("⚠️", "warning").replace("⚠", "warning").replace("❌", "fail").replace("️", "")
        out.append(line)
    head = f"## {e['title']} {{#{e['id']}}}\n\n*{e['kind']}.* Entry id `{e['id']}`.\n"
    pages[e["id"]] = head + "\n".join(out)

# ---------------------------------------------------------------- front matter
kinds = collections.Counter(e["kind"] for e in entries)
kind_words = {"concept": "concepts", "instrument": "instruments", "result": "results", "correction": "corrections", "reference": "references"}
schema = open(os.path.join(ROOT, "SCHEMA.md"), encoding="utf-8").read()
field_rows = [l for l in schema.split("\n") if l.startswith("| `")]
field_table = "\n".join(["| Field | What it holds | Source of truth |", "|----|----------|------|"] + field_rows)

preface = f"""
# Preface {{-}}

\\markboth{{Preface}}{{}}

This is the encyclopedia of the observation theory program, the companion to the textbook
*Data Mining as Observation*. It has {len(entries)} entries, one for every headword of the
book's glossary and three that were filled by hand before the generator existed. Of the
entries, {kinds['concept']} are concepts, {kinds['instrument']} are instruments,
{kinds['result']} are results, {kinds['correction']} are corrections, and {kinds['reference']}
is a reference.

**Where the entries come from.** An entry is built from the program's records rather than
written beside them. The claims ledger in the repository geometric-observation is the
authority for what a result is worth. A campaign track file is the authority for what was
measured. The book's sources tables are the authority for every number the book states. The
generator, `encyclopedia/generate.py`, gathers what those records say about one thing, keyed
by their identifiers, so that a correction in a record propagates to the entry on the next
rebuild and never has to be chased by hand. The curated parts of an entry, its definition,
its conditions, and the list of related entries, live in `encyclopedia/entries.toml`.

**How to read an entry.** Every entry carries the same headings in the same order. A heading
with nothing to say keeps the word none, so that a missing field and an empty field cannot be
confused. A record joins an entry by a typed edge. An equation defines the entry when the
book's paragraph around it names the entry's terms. A ledger row proves, measures, or refutes
and corrects the entry, by its class, when its claim names the entry, and a sources-table row
measures the entry when its claim names it. Records that were cited beside an entry without
naming it are not printed in the body. They are listed under the entry's see-also heading,
and the back matter lists every ledger row with the entries it bears on. A result or
correction entry trusts every record chosen for it. The status line at the end of each entry
gives the date it was generated and the book commit, and the provenance section gives the
commit of every other record.

{field_table}

**Conventions.** A ledger row carries its class in brackets, proved, demonstrated,
replicated, predicted, exploratory, refuted, missed, or void, and a refuted row sits in the
entry at the same size as the results it bounds. A ledger row is printed once in full in the
ledger itself. An entry carries the row's first sentence, its class, and a link to the line. A number names its repository, file, line range, and
commit, exactly as the book's sources tables do, and a number without a row was removed. The
machine-checked heading names the Lean file and theorems that check the entry's core against
Mathlib, built with no sorry and the standard axioms only, and the book's appendix C says
what each check does and does not cover. Book equation numbers, chapter numbers, and section
numbers refer to *Data Mining as Observation*, draft 0.2.

**Prior art.** Where an idea has a name outside the program, the entry says so under the
heading known as. The read operator is, in the scalar Euclidean case, the active-subspace
matrix of Constantine and Gleich, and consumer-relative compression sits beside the
information bottleneck and task-based quantization. What the program adds is the output-metric
pullback, the observer triple, the budget, and the audit discipline.

**How to cite.** Cite the repository ahb-sjsu/observation-theory-campaigns at commit
{COMMIT}, the entry by its id, and, for a number, the source row the entry gives. The
provenance section at the end names the commit of every record the entries were read from.

**Cross-references.** Each entry ends with its related entries, and each reference carries
the page it is found on. The back matter lists the entries by kind, by chapter of the book,
by the Lean file that checks them, and by the ledger row that bears on them.
"""

# ---------------------------------------------------------------- entries by letter
body = []
current = None
for e in entries:
    letter = sort_key(e)[0].upper()
    if letter != current:
        current = letter
        body.append(f"\n\\clearpage\n\n# {letter}\n")
    body.append(pages[e["id"]])
    body.append("")

# ---------------------------------------------------------------- back matter
def back_heading(title, columns=True):
    s = f"\n\\clearpage\n\n# {title} {{-}}\n\n\\markboth{{{title}}}{{}}\n"
    if columns:
        s += "\n```{=latex}\n\\begin{multicols}{2}\\small\n```\n"
    return s


COLS_END = "\n```{=latex}\n\\end{multicols}\n```\n"
back = [back_heading("Entries by kind")]
for k in ("concept", "instrument", "result", "correction", "reference"):
    items = [e for e in entries if e["kind"] == k]
    back.append(f"\n**{kind_words[k][0].upper() + kind_words[k][1:]}, {len(items)}.** " + "; ".join(link(e["id"]) for e in items) + ".\n")

back.append(COLS_END + back_heading("Entries by chapter of the book"))
back.append("\nThe chapter of *Data Mining as Observation* in whose body the entry's terms appear.\n")
for c in sorted(used_in):
    items = sorted(set(used_in[c]), key=lambda i: sort_key(by_id[i]))
    back.append(f"\n**Chapter {c}, {len(items)} entries.** " + "; ".join(link(i) for i in items) + ".\n")

back.append(COLS_END + back_heading("Entries by Lean file"))
back.append("\nThe Lean file in the book's repository that machine-checks each entry's core, and the entries it checks.\n")
by_lean = collections.defaultdict(list)
for e in entries:
    lean = e.get("lean", [])
    if isinstance(lean, str):
        lean = [lean]
    for l in lean:
        by_lean[l.split("/")[-1]].append(e["id"])
for f in sorted(by_lean, key=str.lower):
    items = sorted(set(by_lean[f]), key=lambda i: sort_key(by_id[i]))
    back.append(f"\n`{f}`. " + "; ".join(link(i) for i in items) + ".\n")

back.append(COLS_END + back_heading("Entries by ledger row"))
back.append("\nThe rows of the claims ledger in geometric-observation, and the entries each bears on.\n")
by_row = collections.defaultdict(list)
for e in entries:
    for r in e.get("ledger", []):
        by_row[r].append(e["id"])


def row_key(r):
    m = re.match(r"([A-Z]+)-?([A-Z]*)-?(\d*)", r)
    return (m.group(1), m.group(2), int(m.group(3) or 0), r) if m else ("", "", 0, r)


for r in sorted(by_row, key=row_key):
    items = sorted(set(by_row[r]), key=lambda i: sort_key(by_id[i]))
    back.append(f"\n**{r}.** " + "; ".join(link(i) for i in items) + ".\n")

back.append(COLS_END + back_heading("Provenance", columns=False))
status = next(iter(status_lines.values()), "")
back.append(f"\nThis document was built on {DATE} from commit {COMMIT} of ahb-sjsu/observation-theory-campaigns by `encyclopedia/build_pdf.py`. The entries were {status[0].lower() + status[1:] if status else 'generated by encyclopedia/generate.py.'}\n")
back.append("\nThe hand-filled entries, the flip, the false-clear rate, and the Youden F1 bound, were written on 2026-09-03 to fix the schema and are the generator's acceptance test. `encyclopedia/check.py` verifies that every number in each of them appears in its generated counterpart and that every cited path exists.\n")

# ---------------------------------------------------------------- assemble and build
parts = [
    "---",
    "title: The Observation Theory Encyclopedia",
    f"subtitle: Companion to *Data Mining as Observation*, {len(entries)} entries",
    "author: The observation theory program, ahb-sjsu",
    f"date: Built {DATE} from commit {COMMIT}",
    "toc-title: Contents",
    "---",
    preface,
    "\n\\clearpage\n",
    "\n".join(body),
    "\n".join(back),
]
allmd = os.path.join(BUILD, "encyclopedia.md")
open(allmd, "w", encoding="utf-8", newline="\n").write("\n".join(parts))

header = os.path.join(BUILD, "header.tex")
open(header, "w", encoding="utf-8").write(r"""
\setlength{\emergencystretch}{3em}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\nouppercase{\leftmark}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.2pt}
\setlength{\parskip}{4pt}
\setlength{\parindent}{0pt}
\usepackage{titlesec}
\titleformat{\section}[display]{\normalfont\Huge\bfseries}{}{0pt}{}
\titleformat{\subsection}{\normalfont\Large\bfseries}{}{0pt}{}
\titleformat{\subsubsection}{\normalfont\small\bfseries\scshape}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{18pt}{6pt}
\titlespacing*{\subsubsection}{0pt}{8pt}{2pt}
\renewcommand{\arraystretch}{1.15}
\usepackage{multicol}
\setlength{\columnsep}{18pt}
\let\oldtableofcontents\tableofcontents
\renewcommand{\tableofcontents}{\clearpage\markboth{Contents}{}\oldtableofcontents}
""")

pdf = os.path.join(BUILD, "encyclopedia.pdf")
cmd = ["pandoc", allmd, "-f", "markdown+pipe_tables+tex_math_dollars+smart+raw_tex", "-o", pdf,
       "--pdf-engine=xelatex", "--toc", "--toc-depth=2", "--top-level-division=section",
       "-V", "documentclass=article", "-V", "geometry:letterpaper", "-V", "geometry:margin=1in",
       "-V", "mainfont=Cambria", "-V", "mainfontoptions=Ligatures=NoCommon", "-V", "monofont=Consolas",
       "-V", "monofontoptions=Scale=0.82", "--lua-filter", os.path.join(ROOT, "code_breaks.lua"),
       "-V", "colorlinks=true", "-V", "linkcolor=blue", "-V", "urlcolor=blue", "-V", "fontsize=10pt",
       "-V", "secnumdepth=0", "-H", header]
r = run(cmd, BUILD)
sys.stdout.write(r.stdout[-3000:])
sys.stdout.write(r.stderr[-3000:])
if r.returncode != 0 or not os.path.exists(pdf):
    print("pandoc exit", r.returncode)
    sys.exit(1)
dest = os.path.join(OUT, "Observation-Theory-Encyclopedia.pdf")
shutil.copy(pdf, dest)
log = open(os.path.join(BUILD, "encyclopedia.log"), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(BUILD, "encyclopedia.log")) else ""
m = re.findall(r"Output written on .*? \((\d+) pages", log)
print("wrote", dest, "from commit", COMMIT, "pages", m[-1] if m else "?", "entries", len(entries))
