"""Generate encyclopedia entries from the records. Run from the repository root:

    python encyclopedia/generate.py <source root>

<source root> is the directory holding the local checkouts named in entries.toml, for example
C:\\source. Writes encyclopedia/generated/<id>.md, one per [[entry]], with the headings of
SCHEMA.md. Every record it reads is named with the commit of its repository at generation time,
and a record path that does not exist fails the run. Nothing here is prose the generator made
up. Definitions come from the book's glossary, equations from the book's numbered displays,
ledger rows from the claims ledger, measurements from the book's sources tables and the
campaign track tables, corrections from errata files and the records that carry them, and
conditions from entries.toml, where they are curated by hand and marked as such.
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys
import tomllib
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CFG = tomllib.load(open(os.path.join(HERE, "entries.toml"), "rb"))
REPOS = {name: os.path.join(SRC, rel) for name, rel in CFG["repos"].items()}
OUT = os.path.join(HERE, "generated")
os.makedirs(OUT, exist_ok=True)
BOOK = REPOS["observation-data-mining"]
problems = []


def commit(repo):
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPOS[repo], capture_output=True, text=True)
    return r.stdout.strip() or "unknown"


COMMITS = {name: commit(name) for name in REPOS if os.path.isdir(REPOS[name])}


def record(repo, rel):
    """Path of a record, checked to exist. A missing record is a build failure."""
    p = os.path.join(REPOS[repo], rel.replace("\\", "/"))
    if not os.path.exists(p):
        problems.append(f"missing record {repo}/{rel}")
        return None
    return p


def read(repo, rel):
    p = record(repo, rel)
    return open(p, encoding="utf-8").read() if p else ""


# ---------------------------------------------------------------- the book
CHAPTERS = sorted(glob.glob(os.path.join(BOOK, "chapters", "ch*.md")))
CHTEXT = {os.path.basename(p): open(p, encoding="utf-8").read() for p in CHAPTERS}
GLOSSARY = open(os.path.join(BOOK, "chapters", "glossary.md"), encoding="utf-8").read()


def glossary_definition(key):
    m = re.search(r"^\*\*" + re.escape(key) + r"\.\*\* (.*)$", GLOSSARY, re.M)
    return m.group(1).strip() if m else ""


def book_equation(tag):
    for name, text in CHTEXT.items():
        m = re.search(r"^\$\$([^\n]*?)\s*\\tag\{" + re.escape(tag) + r"\}\$\$", text, re.M)
        if m:
            return m.group(1).strip()
    problems.append(f"book equation {tag} not found")
    return ""


def sources_rows(substrings):
    """Rows of the book's sources tables whose Source cell mentions any of the substrings."""
    rows = []
    for name, text in CHTEXT.items():
        chnum = int(name[2:4])
        in_sources = False
        for line in text.split("\n"):
            if line.startswith("## Sources for every number"):
                in_sources = True
            if not in_sources or not line.startswith("| ") or line.startswith("| Section"):
                continue
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) < 3:
                continue
            if any(s in cells[2] for s in substrings):
                rows.append((f"chapter {chnum} section {cells[0]}", cells[1], cells[2]))
    return rows


def chapters_mentioning(patterns):
    rx = re.compile("|".join(patterns), re.I)
    out = []
    for name, text in CHTEXT.items():
        body = "\n".join(l for l in text.split("\n") if not l.startswith("|"))
        if rx.search(body):
            out.append(int(name[2:4]))
    return out


# ---------------------------------------------------------------- the ledger
LEDGER_PATH = record("geometric-observation", "claims/LEDGER.md")
LEDGER = open(LEDGER_PATH, encoding="utf-8").read().split("\n") if LEDGER_PATH else []


def ledger_rows(prefixes):
    out = []
    for i, line in enumerate(LEDGER, 1):
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) < 3:
            continue
        key = re.sub(r"\*\*", "", cells[0])
        for p in prefixes:
            if key.startswith(p):
                cls = re.findall(r"`?\[(\w+)\]`?", cells[2])
                out.append((key, re.sub(r"\*\*", "", cells[1]), cls[0] if cls else cells[2], i))
    return out


# ---------------------------------------------------------------- track tables, errata, results
def table_rows(repo, rel, pattern):
    text = read(repo, rel)
    rx = re.compile(pattern)
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        if rx.search(line):
            cells = [re.sub(r"\*\*|`", "", c.strip()) for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            out.append((cells, i))
    return out


def errata_sections(repo, rel, pattern):
    """Passages of a record that match the pattern, with their line range. A match in a
    heading returns the whole section under it. A match elsewhere returns its paragraph."""
    text = read(repo, rel)
    rx = re.compile(pattern)
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("## ") and rx.search(lines[i]):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            body = " ".join(l.strip() for l in lines[i:j] if l.strip())
            out.append((i + 1, j, body[:3000]))
            i = j
            continue
        if lines[i].strip() and not lines[i].startswith("#") and rx.search(lines[i]):
            a = i
            while a > 0 and lines[a - 1].strip():
                a -= 1
            b = i
            while b + 1 < len(lines) and lines[b + 1].strip():
                b += 1
            body = " ".join(l.strip() for l in lines[a:b + 1])
            out.append((a + 1, b + 1, body[:1200]))
            i = b + 1
            continue
        i += 1
    return out


def results_summary(repo, rel):
    text = read(repo, rel)
    if not text:
        return []
    d = json.loads(text)
    lines = []
    for r in d.get("part_a", []):
        lines.append(f"| {r['dataset']} | {r['pairs']} | {r['best_f1_exhaustive']:.4f} | "
                     f"{r['auroc_prefilter']['0.75']['evaluated']}, {'yes' if r['auroc_prefilter']['0.75']['admissible'] else 'no'} | "
                     f"{r['youden_prune']['evaluated']}, {'yes' if r['youden_prune']['admissible'] else 'no'} | {r['pairs_with_f1_above_auroc_ceiling']} |")
    part_a = ["| Dataset, depth 2 pairs | Pairs | Exhaustive F1 | AUROC pre-filter at 0.75, evaluated, admissible | Youden pruning, evaluated, admissible | Pairs whose F1 exceeds the AUROC ceiling |",
              "|---|---|---|---|---|---|"] + lines
    lines = []
    for r in d.get("part_b", []):
        s, f, y = r["strict"], r["fast"], r["youden"]
        lines.append(f"| {r['dataset']} | {s['f1']:.4f}, {s['formula']} | {f['f1']:.4f} | {y['f1']:.4f}, {y['formula']} | {s['expansions']}, {f['expansions']}, {y['expansions']} |")
    part_b = ["| Dataset | strict F1 and formula | fast F1 | youden F1 and formula | expansions strict, fast, youden |",
              "|---|---|---|---|---|"] + lines
    return ["Part A, recorded at commit " + d.get("commit", "?") + " of theory-radar."] + part_a + [""] + ["Part B."] + part_b


def lean_theorems(spec):
    repo, rel = spec.split(":", 1)
    text = read(repo, rel)
    names = re.findall(r"^theorem (\w+)", text, re.M)
    return f"`{rel}`, theorems " + ", ".join(f"`{n}`" for n in names) + f", at {repo} {COMMITS.get(repo, '?')}."


# ---------------------------------------------------------------- assembly
def build(e):
    out = [f"# {e['title']}", "", f"**id.** {e['id']}", f"**kind.** {e['kind']}", ""]
    out += ["## definition", "", glossary_definition(e["glossary"]) if e.get("glossary") else "none", ""]
    out += ["## equation", ""]
    for tag in e.get("equations", []):
        eq = book_equation(tag)
        if eq:
            out += [f"Book equation {tag}.", "", "    " + eq.replace("\n", " "), ""]
    out += ["## ledger", ""]
    rows = ledger_rows(e.get("ledger", []))
    if rows:
        for key, claim, cls, ln in rows:
            out.append(f"- {key}. {claim} `[{cls}]`. `geometric-observation/claims/LEDGER.md:{ln}` at {COMMITS['geometric-observation']}.")
    else:
        out.append("none")
    out += ["", "## first stated", "", e.get("first_stated", "none"), ""]
    out += ["## measurements", ""]
    srows = sources_rows(e.get("book_records", []))
    cells = [(c, table_rows(c["repo"], c["file"], c["match"]), c) for c in e.get("cells", [])]
    if srows:
        out += ["| Where the book states it | Numbers, as the book's sources table records them | Source |", "|---|---|---|"]
        for where, claim, src in srows:
            out.append(f"| {where} | {claim} | {src} |")
        out.append("")
    for c, rows_, spec in cells:
        if rows_:
            out += [f"From `{c['repo']}/{c['file']}` at {COMMITS[c['repo']]}.", ""]
            for cells_, ln in rows_:
                out.append("- line " + str(ln) + ". " + " | ".join(cells_))
            out.append("")
    for r in e.get("results", []):
        if r.get("note"):
            out += [r["note"], ""]
        out += results_summary(r["repo"], r["file"]) + [""]
    if not srows and not cells and not e.get("results"):
        out += ["none", ""]
    out += ["## failures and corrections", ""]
    found = False
    for key, claim, cls, ln in rows:
        if cls == "refuted":
            out.append(f"- {key}, `[refuted]`. {claim}")
            found = True
    for er in e.get("errata", []):
        for a, b, para in errata_sections(er["repo"], er["file"], er["match"]):
            out.append(f"- `{er['repo']}/{er['file']}:{a}-{b}` at {COMMITS[er['repo']]}. {para}")
            found = True
    if not found:
        out.append("none")
    out += ["", "## conditions", ""]
    conds = e.get("conditions", [])
    out += [f"- {c}" for c in conds] if conds else ["none"]
    if conds:
        out.append("")
        out.append("Conditions are curated in `entries.toml` rather than read from a record.")
    out += ["", "## machine checked", "", lean_theorems(e["lean"]) if e.get("lean") else "none", ""]
    chs = chapters_mentioning(e.get("book_terms", [])) if e.get("book_terms") else []
    out += ["## used in", "", ("*Data Mining as Observation* chapters " + ", ".join(str(c) for c in chs) + ".") if chs else "none", ""]
    out += ["## related", "", ", ".join(e.get("related", [])) or "none", ""]
    commits = ", ".join(f"{k} {v}" for k, v in COMMITS.items())
    out += ["## status", "", f"Generated {date.today().isoformat()} by `encyclopedia/generate.py` from {commits}.", ""]
    return "\n".join(out)


for e in CFG["entry"]:
    text = build(e)
    open(os.path.join(OUT, e["id"] + ".md"), "w", encoding="utf-8").write(text)
    print("generated", e["id"])
if problems:
    print("PROBLEMS")
    for p in problems:
        print(" ", p)
    sys.exit(1)
