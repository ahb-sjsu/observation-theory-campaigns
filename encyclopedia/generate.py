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
GITHUB = "https://github.com/ahb-sjsu"
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
CHAPTERS = sorted(glob.glob(os.path.join(BOOK, "chapters", "ch*.md"))) + sorted(glob.glob(os.path.join(BOOK, "chapters", "appendix_*.md")))
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
        if not name.startswith("ch"):
            continue
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
        if rx.search(body) and name.startswith("ch"):
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
            if key.startswith(p) and not key[len(p):len(p) + 1].isdigit():
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
    return ["Part A, recorded at commit " + d.get("commit", "?") + " of theory-radar.", ""] + part_a + ["", "Part B.", ""] + part_b


def lean_theorems(spec):
    repo, rel = spec.split(":", 1)
    text = read(repo, rel)
    names = re.findall(r"^theorem (\w+)", text, re.M)
    url = f"{GITHUB}/{repo}/blob/{COMMITS.get(repo, 'master')}/{rel}"
    appx = f"{GITHUB}/{repo}/blob/{COMMITS.get(repo, 'master')}/chapters/machine_checked.md"
    return (f"[`{rel}`]({url}), theorems " + ", ".join(f"`{n}`" for n in names)
            + f", at {repo} {COMMITS.get(repo, '?')}; what the check covers is stated in the book's [appendix C]({appx}).")


# ---------------------------------------------------------------- relationships
CLASS_EDGE = {"proved": "proves", "demonstrated": "measures", "replicated": "measures", "predicted": "measures",
              "exploratory": "measures", "refuted": "refutes or corrects", "missed": "refutes or corrects",
              "void": "refutes or corrects", "witness": "refutes or corrects", "revised": "refutes or corrects"}


# ---------------------------------------------------------------- transformation registries

def load_registries():
    """Every claims/transformations/*.toml in the campaigns repository, read from the
    repository this generator lives in (so a worktree sees its own registries)."""
    base = os.path.dirname(HERE)
    d = os.path.join(base, "claims", "transformations")
    if not os.path.isdir(d):
        return []
    regs = []
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".toml"):
            regs.append(tomllib.load(open(os.path.join(d, fn), "rb")))
    return regs


REGISTRIES = load_registries()


def envelope_lines(e):
    """The invariance envelope of an entry: every registry test that names it, grouped by
    outcome, each with its transformation, claim, record, and, for failures and boundaries,
    the witness and what absorbed it."""
    groups = {"survived": [], "proved": [], "boundary": [], "failed": [], "predicted": []}
    for reg in REGISTRIES:
        fams = {t["id"]: t for t in reg.get("transformation", [])}
        for t in reg.get("test", []):
            if e["id"] not in t.get("entries", []):
                continue
            fam = fams.get(t["transformation"], {})
            claim = t["claim"][:1].upper() + t["claim"][1:]
            line = f"- {t['transformation']}, {fam.get('family', '')}. Claim: {claim}. {linkify('`' + t['record'] + '`')}."
            if t.get("boundary"):
                line += f" Boundary: {t['boundary']}."
            if t.get("witness"):
                line += f" Witness: {t['witness']}. Absorbed by: {t.get('absorbed_by', '?')}."
            if t.get("revision") and t["revision"] != "none":
                line += f" Revision: {t['revision']}."
            groups.setdefault(t["outcome"], []).append(line)
    out = []
    labels = [("proved", "Proved invariant"), ("survived", "Survived"), ("boundary", "Boundary measured"),
              ("failed", "Failed, with witness"), ("predicted", "Predicted, sealed and unrun")]
    for key, label in labels:
        if groups.get(key):
            out += [f"**{label}.**", ""] + groups[key] + [""]
    return out if out else ["none declared", ""]


def term_patterns(e):
    pats = [re.compile(p, re.I) for p in e.get("book_terms", [])]
    words = [w for w in re.split(r"[^a-z0-9]+", e["title"].lower()) if len(w) > 2]
    if words:
        pats.append(re.compile(r"\b" + r"\W+".join(re.escape(w) for w in words) + r"s?\b", re.I))
    return pats


def about(e, *texts):
    """Whether any of the texts names the entry, by its book terms or its title. A result or
    correction entry, or one that sets strict = false, trusts every record it cites."""
    if not e.get("strict", e["kind"] not in ("result", "correction")):
        return True
    pats = term_patterns(e)
    return any(p.search(t) for t in texts if t for p in pats)


def equation_context(tag):
    """The equation with the paragraph before and after its display in the book."""
    for name, text in CHTEXT.items():
        m = re.search(r"^\$\$([^\n]*?)\s*\\tag\{" + re.escape(tag) + r"\}\$\$", text, re.M)
        if m:
            before = text[:m.start()].rstrip().split("\n\n")[-1]
            after = text[m.end():].lstrip().split("\n\n")[0]
            return m.group(1).strip(), before + " " + after
    problems.append(f"book equation {tag} not found")
    return "", ""


def clean(s):
    """One hyphen, no raw markdown headings, no stray pipes or dollars from record text."""
    s = s.replace("‑", "-").replace("‐", "-")
    s = re.sub(r"(^|\s)#{1,6}\s+", r"\1", s)
    return s


def cell_text(s):
    return clean(s).replace("|", "\|")


def linkify(src):
    """Turn `repo\\path:a-b` citations into links to the file at the commit it was read at,
    with one separator convention."""
    def rep(m):
        repo, path, a, b = m.group(1), m.group(2).replace("\\", "/"), m.group(3), m.group(4)
        lines = (f":{a}" + (f"-{b}" if b else "")) if a else ""
        label = f"{repo}/{path}{lines}"
        if repo not in REPOS:
            return f"`{label}`"
        frag = (f"#L{a}" + (f"-L{b}" if b else "")) if a else ""
        return f"[`{label}`]({GITHUB}/{repo}/blob/{COMMITS.get(repo, 'master')}/{path}{frag})"
    return re.sub(r"`([\w.-]+)[\\/]([^`:]+?)(?::(\d+)(?:-(\d+))?)?`", rep, clean(src))


def ledger_link(ln):
    return f"[`geometric-observation/claims/LEDGER.md:{ln}`]({GITHUB}/geometric-observation/blob/{COMMITS['geometric-observation']}/claims/LEDGER.md#L{ln})"


def short(claim, n=240):
    claim = clean(claim.strip())
    first = re.split(r"(?<=[.!?])\s+(?=[A-Z])", claim, maxsplit=1)[0]
    if len(first) > n:
        first = first[:n].rsplit(" ", 1)[0] + " …"
    return first


# ---------------------------------------------------------------- assembly
EXAMPLES = tomllib.load(open(os.path.join(HERE, "examples.toml"), "rb")) if os.path.exists(os.path.join(HERE, "examples.toml")) else {}
FIGDIR = os.path.join(HERE, "figures")
CAPTIONS = {}
if os.path.exists(os.path.join(FIGDIR, "captions.toml")):
    CAPTIONS = tomllib.load(open(os.path.join(FIGDIR, "captions.toml"), "rb"))


def build(e):
    out = [f"# {e['title']}", "", f"**id.** {e['id']}", f"**kind.** {e['kind']}", ""]
    if os.path.exists(os.path.join(FIGDIR, e["id"] + ".svg")):
        out += [f"![{CAPTIONS.get(e['id'], e['title'])}](../figures/{e['id']}.svg)", ""]
    definition = e.get("definition") or (glossary_definition(e["glossary"]) if e.get("glossary") else "")
    out += ["## definition", "", definition or "none", ""]
    if e["id"] in EXAMPLES:
        out += [f"**Example.** {EXAMPLES[e['id']]}", ""]
    if e.get("known_as"):
        out += [f"**Known as, or related to prior art.** {e['known_as']}", ""]
    # equations: defining ones are those whose paragraph in the book names the entry
    defining, nearby = [], []
    for tag in e.get("equations", []):
        eq, ctx = equation_context(tag)
        if not eq:
            continue
        (defining if about(e, ctx, eq) else nearby).append((tag, eq))
    out += ["## equation", ""]
    if defining:
        for tag, eq in defining:
            out += [f"Book equation {tag}.", "", "    " + eq.replace("\n", " "), ""]
    else:
        out += ["none", ""]
    conds = e.get("conditions", [])
    out += ["## conditions", ""]
    out += [f"- {c}" for c in conds] if conds else ["none"]
    if conds:
        out += ["", "Conditions are curated in `entries.toml` rather than read from a record."]
    out.append("")
    # ledger rows: typed, and only rows that name the entry appear in the body
    rows = ledger_rows(e.get("ledger", []))
    typed = {"proves": [], "measures": [], "refutes or corrects": []}
    mentions = []
    for key, claim, cls, ln in rows:
        edge = CLASS_EDGE.get(cls, "measures")
        if about(e, key, claim):
            typed[edge].append((key, claim, cls, ln))
        else:
            mentions.append(key)
    out += ["## ledger", ""]
    any_row = False
    for edge in ("proves", "measures", "refutes or corrects"):
        for key, claim, cls, ln in typed[edge]:
            out.append(f"- *{edge}.* {key} `[{cls}]`. {short(claim)} {ledger_link(ln)}.")
            any_row = True
    if not any_row:
        out.append("none")
    out += ["", "## first stated", "", clean(e.get("first_stated", "none")), ""]
    # measurements: only rows whose claim or section names the entry appear in the body
    out += ["## measurements", ""]
    srows = sources_rows(e.get("book_records", []))
    kept = [(w, c, s) for w, c, s in srows if about(e, w, c)]
    passing = [(w, c, s) for w, c, s in srows if not about(e, w, c)]
    cells = [(c, table_rows(c["repo"], c["file"], c["match"]), c) for c in e.get("cells", [])]
    if kept:
        out += ["| Where the book states it | Numbers, as the book's sources table records them | Source |", "|---|---|---|"]
        for where, claim, src in kept:
            out.append(f"| {where} | {clean(claim)} | {linkify(src)} |")
        out.append("")
    for c, rows_, spec in cells:
        if rows_:
            out += [f"From `{c['repo']}/{c['file']}` at {COMMITS[c['repo']]}.", ""]
            for cells_, ln in rows_:
                out.append("- line " + str(ln) + ". " + "; ".join(cell_text(x) for x in cells_ if x))
            out.append("")
    for r in e.get("results", []):
        if r.get("note"):
            out += [r["note"], ""]
        out += [""] + results_summary(r["repo"], r["file"]) + [""]
    if not kept and not cells and not e.get("results"):
        out += ["none", ""]
    out += ["## failures and corrections", ""]
    found = False
    for key, claim, cls, ln in typed["refutes or corrects"]:
        out.append(f"- {key}, `[{cls}]`. {short(claim)} {ledger_link(ln)}.")
        found = True
    for er in e.get("errata", []):
        for a, b, para in errata_sections(er["repo"], er["file"], er["match"]):
            out.append(f"- {linkify('`' + er['repo'] + '/' + er['file'] + ':' + str(a) + '-' + str(b) + '`')} at {COMMITS[er['repo']]}. {cell_text(para)}")
            found = True
    if not found:
        out.append("none")
    out += ["", "## invariance envelope", ""] + envelope_lines(e)
    lean = e.get("lean")
    lean = [lean] if isinstance(lean, str) else (lean or [])
    out += ["", "## machine checked", "", "\n\n".join(lean_theorems(s) for s in lean) if lean else "none", ""]
    chs = chapters_mentioning(e.get("book_terms", [])) if e.get("book_terms") else []
    out += ["## used in", "", ("*Data Mining as Observation* chapters " + ", ".join(str(c) for c in chs) + ".") if chs else "none", ""]
    out += ["## related", "", ", ".join(e.get("related", [])) or "none", ""]
    # what was cited beside the entry but is not about it, kept out of the body
    see = []
    if nearby:
        see.append("Book equations stated beside the entry's terms, not defining it: " + ", ".join(t for t, _ in nearby) + ".")
    if mentions:
        see.append("Ledger rows that cite the entry's records without naming it: " + ", ".join(mentions) + ".")
    if passing:
        secs = sorted({w for w, _, _ in passing}, key=lambda s: [int(x) for x in re.findall(r"\d+", s)])
        see.append("Sources-table rows that share a record with the entry without naming it: " + ", ".join(secs) + ".")
    out += ["## see also", "", "\n\n".join(see) if see else "none", ""]
    out += ["## status", "", f"Generated {date.today().isoformat()} by `encyclopedia/generate.py`; book at observation-data-mining {COMMITS.get('observation-data-mining', '?')}; the commit of every record is listed in the encyclopedia's provenance.", ""]
    return "\n".join(out)


ids = {e["id"] for e in CFG["entry"]}
for k in EXAMPLES:
    if k not in ids:
        problems.append(f"example for unknown entry {k}")
for e in CFG["entry"]:
    if e["id"] not in EXAMPLES:
        problems.append(f"no example for {e['id']}")
for e in CFG["entry"]:
    text = build(e)
    open(os.path.join(OUT, e["id"] + ".md"), "w", encoding="utf-8").write(text)
    print("generated", e["id"])
if problems:
    print("PROBLEMS")
    for p in problems:
        print(" ", p)
    sys.exit(1)
