"""Build the encyclopedia as a static website, the web-first form.

    python encyclopedia/build_site.py

Writes encyclopedia/site/. index.html carries the search box, the letter index, and every
entry as a card with its one-line definition. Each entry has its own page, <id>.html, that
opens with a compact card: the canonical definition and aliases, the exact book version and
commit, the epistemic and correction status, the defining equation, the assumptions and
scope, the prior-art relationship, the evidence links, and the last semantic review date.
Below the card come the figure and the full entry. kinds.html, chapters.html, lean.html, and
ledger.html are the back matter, ledger.html printing each ledger row once in full, and
provenance.html names the records' commits. all.html is the whole site in one file with
hash routing, for viewing without a server. Equations render with MathJax from a CDN;
everything else is inlined.
"""
import collections
import datetime
import html
import json
import os
import re
import subprocess
import sys
import tomllib

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SITE = os.path.join(ROOT, "site")
os.makedirs(SITE, exist_ok=True)
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(REPO)
GITHUB = "https://github.com/ahb-sjsu"


def run(cmd, cwd=None, inp=None):
    return subprocess.run(cmd, cwd=cwd, input=inp, capture_output=True, text=True, encoding="utf-8", errors="replace")


COMMIT = run(["git", "rev-parse", "--short", "HEAD"], REPO).stdout.strip()
DATE = datetime.date.today().isoformat()
CFG = tomllib.load(open(os.path.join(ROOT, "entries.toml"), "rb"))
entries = CFG["entry"]
REPOS = {name: os.path.join(SRC, rel) for name, rel in CFG["repos"].items()}


def sort_key(e):
    t = e["title"].lower()
    for pre in ("the ", "a ", "an "):
        if t.startswith(pre):
            t = t[len(pre):]
    return re.sub(r"[^a-z0-9]", "", t) or t


entries.sort(key=sort_key)
by_id = {e["id"]: e for e in entries}
captions = tomllib.load(open(os.path.join(ROOT, "figures", "captions.toml"), "rb")) if os.path.exists(os.path.join(ROOT, "figures", "captions.toml")) else {}

# ---------------------------------------------------------------- parse the generated pages
SECTIONS = ["definition", "equation", "conditions", "ledger", "first stated", "measurements", "failures and corrections",
            "invariance envelope", "machine checked", "used in", "related", "see also", "status"]


def parse_page(eid):
    lines = open(os.path.join(ROOT, "generated", eid + ".md"), encoding="utf-8").read().split("\n")
    secs = collections.OrderedDict()
    cur = None
    head = []
    for line in lines[1:]:
        if line.startswith("## "):
            cur = line[3:].strip()
            secs[cur] = []
            continue
        (secs[cur] if cur else head).append(line)
    return {k: "\n".join(v).strip() for k, v in secs.items()}, "\n".join(head)


pages = {e["id"]: parse_page(e["id"]) for e in entries}
book_commit = "?"
for e in entries:
    m = re.search(r"observation-data-mining (\w+)", pages[e["id"]][0].get("status", ""))
    if m:
        book_commit = m.group(1)
        break


def md_to_html(md):
    """Markdown to HTML through pandoc, with display equations for MathJax."""
    out = []
    for line in md.split("\n"):
        if line.startswith("    ") and "\\" in line:
            out.append("$$" + line.strip() + "$$")
        else:
            out.append(line)
    r = run(["pandoc", "-f", "markdown+pipe_tables+tex_math_dollars+smart", "-t", "html5", "--mathjax"], inp="\n".join(out))
    return r.stdout


# convert every section of every entry in one pandoc pass, split on markers
chunks = []
for e in entries:
    secs, _ = pages[e["id"]]
    for k in SECTIONS:
        if k in secs:
            chunks.append(f"<!--@@{e['id']}@@{k}@@-->\n\n" + secs[k] + "\n")
big = md_to_html("\n\n".join(chunks))
HTML = collections.defaultdict(dict)
for part in re.split(r"<!--@@([a-z0-9-]+)@@([a-z ]+)@@-->", big)[1:]:
    pass
parts = re.split(r"<!--@@([a-z0-9-]+)@@([a-z ]+)@@-->", big)
for i in range(1, len(parts), 3):
    HTML[parts[i]][parts[i + 1]] = parts[i + 2].strip()


def rel_links(s, single):
    """Rewrite entry links for the static pages or the single file."""
    if single:
        return s.replace('href="e/', 'href="#')
    return s


# ---------------------------------------------------------------- the card
def status_of(eid):
    led = pages[eid][0].get("ledger", "")
    classes = re.findall(r"`\[(\w+)\]`", led)
    edges = re.findall(r"\*(proves|measures|refutes or corrects)\.\*", led)
    if not classes:
        epi = "no ledger row names this entry"
    else:
        c = collections.Counter(zip(edges, classes))
        epi = "; ".join(f"{k[0]} [{k[1]}]" + (f" ×{v}" if v > 1 else "") for k, v in c.items())
    fails = pages[eid][0].get("failures and corrections", "").strip()
    corr = "none recorded" if fails == "none" or not fails else f"{fails.count(chr(10) + '- ') + 1} item(s), see below"
    return epi, corr


def evidence_links(eid):
    secs = pages[eid][0]
    links = []
    for k in ("ledger", "measurements", "failures and corrections", "machine checked"):
        for m in re.finditer(r"\[`([^`]+)`\]\((https?://[^)]+)\)", secs.get(k, "")):
            links.append((m.group(1), m.group(2)))
    lean = by_id[eid].get("lean", [])
    lean = [lean] if isinstance(lean, str) else (lean or [])
    for spec in lean:
        repo, rel = spec.split(":", 1)
        links.append((rel.split("/")[-1], f"{GITHUB}/{repo}/blob/{book_commit}/{rel}"))
    seen, out = set(), []
    for label, url in links:
        if url not in seen:
            seen.add(url)
            out.append((label, url))
    return out


def aliases(e):
    al = []
    if e.get("glossary") and e["glossary"] != e["title"]:
        al.append(e["glossary"])
    for p in e.get("book_terms", []):
        if re.fullmatch(r"[A-Za-z][A-Za-z -]*", p) and p.lower() != e["title"].lower():
            al.append(p)
    return al


def card(e):
    eid = e["id"]
    secs = pages[eid][0]
    epi, corr = status_of(eid)
    eq_html = HTML[eid].get("equation", "")
    first_eq = ""
    m = re.search(r"(<p>Book equation [^<]*</p>\s*<p>\$\$.*?\$\$</p>|<p>Book equation [^<]*</p>\s*\\\[.*?\\\])", eq_html, re.S)
    if m:
        first_eq = m.group(1)
    elif "none" not in eq_html[:40]:
        first_eq = eq_html.split("</p>", 2)[0] + "</p>"
    conds = re.findall(r"<li>(.*?)</li>", HTML[eid].get("conditions", ""), re.S)
    ex = re.search(r"<p><strong>Example\.</strong>(.*?)</p>", HTML[eid].get("definition", ""), re.S)
    rows = [
        ("Definition", html.escape(secs.get("definition", "none").split("\n")[0]) + (" <span class=al>Also " + ", ".join(html.escape(a) for a in aliases(e)) + ".</span>" if aliases(e) else "")),
        ("Example", ex.group(1).strip() if ex else "none"),
        ("Book",f"<em>Data Mining as Observation</em>, draft 0.2, commit <code>{book_commit}</code>; entry id <code>{eid}</code>, kind {e['kind']}."),
        ("Status", f"{html.escape(epi)}. Corrections: {corr}."),
        ("Defining equation", first_eq or "none"),
        ("Assumptions and scope", ("<ul>" + "".join(f"<li>{c}</li>" for c in conds) + "</ul>") if conds else "none"),
        ("Prior art", html.escape(e["known_as"]) if e.get("known_as") else "none recorded"),
        ("Evidence", ", ".join(f'<a href="{u}"><code>{html.escape(l)}</code></a>' for l, u in evidence_links(eid)) or "none"),
        ("Reviewed", (f"semantic review {e['reviewed']}" if e.get("reviewed") else "not yet reviewed") + f"; generated {DATE} from records at the commits on the provenance page."),
    ]
    return '<table class="card">' + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</table>"


# ---------------------------------------------------------------- page assembly
CSS = """
:root { color-scheme: light; --surface:#fcfcfb; --panel:#ffffff; --code:#f3f2ee; --ink:#0b0b0b; --ink2:#52514e; --ink3:#8a897f; --grid:#e6e5e1; --blue:#2a78d6; --green:#1baf7a; --orange:#eb6834; --red:#d03b3b; --violet:#4a3aa7; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { color-scheme: dark; --surface:#141412; --panel:#1c1c1a; --code:#262623; --ink:#ececea; --ink2:#b6b4ad; --ink3:#8a897f; --grid:#2e2e2a; --blue:#6aa3ea; --green:#3fc793; --orange:#f08a5e; --red:#e2605f; --violet:#8f80d8; } }
:root[data-theme="dark"] { color-scheme: dark; --surface:#141412; --panel:#1c1c1a; --code:#262623; --ink:#ececea; --ink2:#b6b4ad; --ink3:#8a897f; --grid:#2e2e2a; --blue:#6aa3ea; --green:#3fc793; --orange:#f08a5e; --red:#e2605f; --violet:#8f80d8; }
* { box-sizing: border-box; }
body { margin:0; background:var(--surface); color:var(--ink); font-family: Inter, 'Segoe UI', Helvetica, Arial, sans-serif; font-size:16.5px; line-height:1.55; font-variant-numeric: tabular-nums; }
h1, h2, .tile a.t { font-family: 'Source Serif 4', Georgia, 'Times New Roman', serif; text-wrap: balance; }
header.top { border-bottom:1px solid var(--grid); padding:10px 24px; display:flex; gap:18px; align-items:baseline; flex-wrap:wrap; }
header.top a { color:var(--ink2); text-decoration:none; } header.top a.brand { color:var(--ink); font-weight:600; }
main { max-width: 900px; margin: 0 auto; padding: 18px 24px 60px; }
h1 { font-size:2rem; margin:.4em 0 .2em; } h2 { font-size:1.35rem; margin:1.6em 0 .4em; } h3 { font-size:.82rem; letter-spacing:.06em; text-transform:uppercase; color:var(--ink2); margin:1.4em 0 .3em; }
a { color: var(--blue); } a:hover { text-decoration: underline; }
code { font-family: ui-monospace, Consolas, monospace; font-size:.88em; background:var(--code); padding:1px 4px; border-radius:3px; overflow-wrap:anywhere; }
table { border-collapse: collapse; width:100%; font-size:.93em; } th, td { text-align:left; vertical-align:top; padding:6px 8px; border-bottom:1px solid var(--grid); } th { color:var(--ink2); font-weight:600; }
table.card { border:1px solid var(--grid); border-radius:8px; background:var(--panel); margin:10px 0 18px; } table.card th { width:11.5em; white-space:nowrap; } table.card ul { margin:0; padding-left:1.1em; }
.kind { display:inline-block; font-size:.78em; padding:1px 8px; border-radius:10px; color:#fff; vertical-align:middle; margin-left:6px; }
.kind.concept{background:var(--blue)} .kind.instrument{background:var(--green)} .kind.result{background:var(--orange)} .kind.correction{background:var(--red)} .kind.reference{background:var(--violet)}
.al { color:var(--ink2); }
figure { margin:14px 0; } figure svg { width:100%; height:auto; border:1px solid var(--grid); border-radius:8px; background:#fcfcfb; } figcaption { font-size:.9em; color:var(--ink2); font-style:italic; margin-top:4px; }
.grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:10px; }
.tile { border:1px solid var(--grid); border-radius:8px; padding:10px 12px; background:var(--panel); } .tile a.t { font-weight:600; text-decoration:none; color:var(--ink); } .tile p { margin:4px 0 0; font-size:.9em; color:var(--ink2); }
.letters a { margin-right:8px; text-decoration:none; font-weight:600; }
input.search { width:100%; font-size:1.05em; padding:10px 12px; border:1px solid var(--grid); border-radius:8px; margin:10px 0 16px; background:var(--panel); color:var(--ink); } input.search:focus, a:focus-visible { outline:2px solid var(--blue); outline-offset:2px; }
.prevnext { display:flex; justify-content:space-between; margin-top:30px; color:var(--ink2); font-size:.95em; }
ul.evidence li { overflow-wrap:anywhere; }
.entry { display:none; } .entry:target, .entry.show { display:block; }
@media (max-width:600px) { table.card th { width:7em; white-space:normal; } body { font-size:15.5px; } }
"""
MATHJAX = '<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\\\(","\\\\)"]],displayMath:[["$$","$$"],["\\\\[","\\\\]"]]}};</script><script defer src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"></script>'


def shell(title, body, single=False, extra_head=""):
    nav = (f'<header class="top"><a class="brand" href="{"#top" if single else "index.html"}">The Observation Theory Encyclopedia</a>'
           f'<a href="{"#tsk" if single else "tsk.html"}">From TSK</a><a href="{"#about" if single else "about.html"}">About</a><a href="{"#kinds" if single else "kinds.html"}">By kind</a>'
           f'<a href="{"#chapters" if single else "chapters.html"}">By chapter</a><a href="{"#lean" if single else "lean.html"}">By Lean file</a>'
           f'<a href="{"#ledger" if single else "ledger.html"}">Ledger</a><a href="{"#provenance" if single else "provenance.html"}">Provenance</a></header>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)}</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Source+Serif+4:wght@600&display=swap"><style>{CSS}</style>{MATHJAX}{extra_head}</head><body>{nav}<main>{body}</main></body></html>')


def figure_html(eid):
    p = os.path.join(ROOT, "figures", eid + ".svg")
    if not os.path.exists(p):
        return ""
    svg = open(p, encoding="utf-8").read()
    return f'<figure>{svg}<figcaption>{html.escape(captions.get(eid, ""))}</figcaption></figure>'


def entry_body(e, single):
    eid = e["id"]
    h = HTML[eid]
    body = [f'<h1 id="{eid}">{html.escape(e["title"])} <span class="kind {e["kind"]}">{e["kind"]}</span></h1>', card(e), figure_html(eid)]
    for k in ("equation", "conditions", "ledger", "first stated", "measurements", "failures and corrections", "invariance envelope", "machine checked", "used in"):
        if k in h:
            body.append(f"<h3>{k[0].upper() + k[1:]}</h3>" + h[k])
    rel = [x for x in e.get("related", []) if x in by_id]
    if rel:
        body.append("<h3>Related</h3><p>" + "; ".join(f'<a href="{("#" if single else "") + x + ("" if single else ".html")}">{html.escape(by_id[x]["title"])}</a>' for x in rel) + ".</p>")
    if "see also" in h:
        see = h["see also"]
        see = re.sub(r"\b((?:GO|NEG|OT)-[A-Za-z0-9-]+)", lambda m: f'<a href="{"#ledger" if single else "ledger.html#" + m.group(1)}">{m.group(1)}</a>', see)
        body.append("<h3>See also</h3>" + see)
    if "status" in h:
        body.append("<h3>Status</h3>" + h["status"])
    return "\n".join(body)


def letter(e):
    return sort_key(e)[0].upper()


# ---------------------------------------------------------------- back matter data
used_in = collections.defaultdict(list)
by_lean = collections.defaultdict(list)
by_row = collections.defaultdict(list)
for e in entries:
    m = re.search(r"chapters? ([0-9, ]+)", pages[e["id"]][0].get("used in", ""))
    if m:
        for c in re.findall(r"\d+", m.group(1)):
            used_in[int(c)].append(e["id"])
    m = re.search(r"primers? ([LS](?: and [LS])?)", pages[e["id"]][0].get("used in", ""))
    if m:
        for c in re.findall(r"[LS]", m.group(1)):
            used_in[c].append(e["id"])
    lean = e.get("lean", [])
    for l in ([lean] if isinstance(lean, str) else lean):
        by_lean[l.split("/")[-1]].append(e["id"])
    for r in e.get("ledger", []):
        by_row[r].append(e["id"])

LEDGER = []
lp = os.path.join(REPOS.get("geometric-observation", ""), "claims", "LEDGER.md")
if os.path.exists(lp):
    for i, line in enumerate(open(lp, encoding="utf-8").read().split("\n"), 1):
        if line.startswith("| "):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) >= 3:
                key = re.sub(r"\*\*", "", cells[0])
                if any(key.startswith(p) and not key[len(p):len(p) + 1].isdigit() for p in by_row):
                    cls = re.findall(r"`?\[(\w+)\]`?", cells[2])
                    LEDGER.append((key, re.sub(r"\*\*", "", cells[1]), cls[0] if cls else "", i))


def elink(eid, single):
    return f'<a href="{"#" if single else ""}{eid}{"" if single else ".html"}">{html.escape(by_id[eid]["title"])}</a>'


def lists_html(single):
    parts = []
    kinds = collections.OrderedDict((k, [e for e in entries if e["kind"] == k]) for k in ("concept", "instrument", "result", "correction", "reference"))
    parts.append(('kinds', "Entries by kind", "".join(f"<h2>{k}, {len(v)}</h2><p>" + "; ".join(elink(e["id"], single) for e in v) + ".</p>" for k, v in kinds.items())))
    parts.append(('chapters', "Entries by chapter of the book", "<p>The two primers, L for linear algebra and S for probability and statistics, come before chapter 0 in the book.</p>" + "".join(f"<h2>{'Primer' if isinstance(c, str) else 'Chapter'} {c}, {len(set(v))}</h2><p>" + "; ".join(elink(i, single) for i in sorted(set(v), key=lambda i: sort_key(by_id[i]))) + ".</p>" for c, v in sorted(used_in.items(), key=lambda kv: (0, kv[0]) if isinstance(kv[0], str) else (1, f"{kv[0]:02d}")))))
    parts.append(('lean', "Entries by Lean file", "<p>The file in the book's repository that machine-checks the entry's core.</p>" + "".join(f'<h2><a href="{GITHUB}/observation-data-mining/blob/{book_commit}/lean/DataMiningAsObservation/{f}"><code>{f}</code></a></h2><p>' + "; ".join(elink(i, single) for i in sorted(set(v), key=lambda i: sort_key(by_id[i]))) + ".</p>" for f, v in sorted(by_lean.items(), key=lambda kv: kv[0].lower()))))
    led = ["<p>Every ledger row an entry cites, printed once in full from geometric-observation's claims ledger, with the entries it bears on.</p>"]
    for key, claim, cls, ln in LEDGER:
        ents = sorted({i for p, v in by_row.items() if key.startswith(p) and not key[len(p):len(p) + 1].isdigit() for i in v}, key=lambda i: sort_key(by_id[i]))
        led.append(f'<h2 id="{html.escape(key)}">{html.escape(key)} <code>[{cls}]</code></h2><p>{html.escape(claim)} <a href="{GITHUB}/geometric-observation/blob/master/claims/LEDGER.md#L{ln}">LEDGER.md:{ln}</a></p><p class=al>Entries: ' + "; ".join(elink(i, single) for i in ents) + ".</p>")
    parts.append(('ledger', "The ledger", "".join(led)))
    status = pages[entries[0]["id"]][0].get("status", "")
    prov = (f"<p>This site was built on {DATE} from commit <code>{COMMIT}</code> of ahb-sjsu/observation-theory-campaigns by <code>encyclopedia/build_site.py</code>. "
            f"The book is <em>Data Mining as Observation</em>, draft 0.2, at commit <code>{book_commit}</code>. {html.escape(status)}</p>"
            "<p>The hand-filled entries, the flip, the false-clear rate, and the Youden F1 bound, were written on 2026-09-03 to fix the schema and are the generator's acceptance test. "
            "<code>encyclopedia/check.py</code> verifies that every number in each of them appears in its generated counterpart and that every cited path exists. "
            "An archival PDF snapshot, <code>encyclopedia/pdf/Observation-Theory-Encyclopedia.pdf</code>, is rebuilt and committed with the site.</p>")
    parts.append(('provenance', "Provenance", prov))
    tsk_rows = tomllib.load(open(os.path.join(ROOT, "tsk_map.toml"), "rb"))["row"]
    tb = ["<p>A student reading Tan, Steinbach, Karpatne, and Kumar, <em>Introduction to Data Mining</em>, second edition, meets a term and does not know which entries to read. For each TSK term, the entries to read in order and the chapter of <em>Data Mining as Observation</em> that takes the term up.</p>",
          "<table><tr><th>TSK term</th><th>TSK</th><th>Entries to read</th><th>Book chapter</th></tr>"]
    for r in tsk_rows:
        tb.append(f"<tr><td>{html.escape(r['tsk'])}</td><td>{html.escape(r['where'])}</td><td>" + "; ".join(elink(i, single) for i in r["entries"] if i in by_id) + f"</td><td>{r['chapter']}</td></tr>")
    tb.append("</table>")
    parts.insert(0, ('tsk', "From TSK to the encyclopedia", "".join(tb)))
    return parts


ABOUT = """
<p>This is the encyclopedia of the observation theory program, the companion to the textbook <em>Data Mining as Observation</em>. It has one entry for every headword of the book's glossary and three that were filled by hand before the generator existed.</p>
<p><strong>Where the entries come from.</strong> An entry is built from the program's records rather than written beside them. The claims ledger in geometric-observation is the authority for what a result is worth, a campaign track file for what was measured, and the book's sources tables for every number the book states. The generator gathers what those records say about one thing, keyed by their identifiers, so that a correction in a record propagates on the next rebuild. The curated parts, the definition, the conditions, the prior art, and the related entries, live in <code>entries.toml</code>.</p>
<p><strong>The card.</strong> Every entry opens with a card: the canonical definition and aliases, the exact book version and commit, the epistemic and correction status, the defining equation, the assumptions and scope, the prior-art relationship, the evidence links, and the last semantic review date. Below the card come a schematic, the full entry, the related entries, and what was cited beside the entry without naming it.</p>
<p><strong>Typed edges.</strong> A record joins an entry when it names the entry. A book equation defines the entry when the paragraph around it names the entry's terms. A ledger row proves, measures, or refutes and corrects the entry by its class, proved, demonstrated, replicated, predicted, exploratory, refuted, missed, or void. A sources-table row measures the entry when its claim names it. Records cited beside an entry without naming it are listed under see also. A ledger row is printed once in full on the ledger page, and an entry carries its first sentence, its class, and a link to the line.</p>
<p><strong>How to cite.</strong> Cite ahb-sjsu/observation-theory-campaigns at the commit on the provenance page, the entry by its id, and for a number the source row the entry gives.</p>
"""


def index_body(single):
    tiles = []
    cur = None
    for e in entries:
        L = letter(e)
        if L != cur:
            cur = L
            tiles.append(f'</div><h2 id="L{L}">{L}</h2><div class="grid">')
        d = html.escape(pages[e["id"]][0].get("definition", ""))
        d = d.split(". ")[0]
        tiles.append(f'<div class="tile" data-k="{html.escape((e["title"] + " " + e["id"] + " " + " ".join(aliases(e)) + " " + d).lower())}"><a class="t" href="{("#" if single else "") + e["id"] + ("" if single else ".html")}">{html.escape(e["title"])}</a><span class="kind {e["kind"]}">{e["kind"]}</span><p>{d}.</p></div>')
    letters = sorted({letter(e) for e in entries})
    search = ('<input class="search" id="q" placeholder="Search entries, aliases, and definitions" oninput="filt()">'
              '<script>function filt(){var q=document.getElementById("q").value.toLowerCase();document.querySelectorAll(".tile").forEach(function(t){t.style.display=(!q||t.dataset.k.indexOf(q)>=0)?"":"none"});}</script>')
    return (f'<h1 id="top">The Observation Theory Encyclopedia</h1><p class=al>{len(entries)} entries, companion to <em>Data Mining as Observation</em>. Built {DATE} from commit <code>{COMMIT}</code>.</p>'
            + search + '<p class="letters">' + "".join(f'<a href="#L{L}">{L}</a>' for L in letters) + "</p><div>" + "".join(tiles) + "</div>")


# ---------------------------------------------------------------- write the static pages
open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(shell("The Observation Theory Encyclopedia", index_body(False)))
open(os.path.join(SITE, "about.html"), "w", encoding="utf-8").write(shell("About the encyclopedia", "<h1>About</h1>" + ABOUT))
for key, title, body in lists_html(False):
    open(os.path.join(SITE, key + ".html"), "w", encoding="utf-8").write(shell(title, f"<h1>{title}</h1>" + body))
for i, e in enumerate(entries):
    prev = entries[i - 1] if i > 0 else None
    nxt = entries[i + 1] if i + 1 < len(entries) else None
    pn = '<div class="prevnext"><span>' + (f'← <a href="{prev["id"]}.html">{html.escape(prev["title"])}</a>' if prev else "") + "</span><span>" + (f'<a href="{nxt["id"]}.html">{html.escape(nxt["title"])}</a> →' if nxt else "") + "</span></div>"
    open(os.path.join(SITE, e["id"] + ".html"), "w", encoding="utf-8").write(shell(e["title"], entry_body(e, False) + pn))

# ---------------------------------------------------------------- the single file
single = ['<div id="home" class="entry show">' + index_body(True) + "</div>", '<div id="about" class="entry"><h1>About</h1>' + ABOUT + "</div>"]
for key, title, body in lists_html(True):
    single.append(f'<div id="{key}" class="entry"><h1>{title}</h1>{body}</div>')
for e in entries:
    single.append(f'<div id="{e["id"]}" class="entry">' + entry_body(e, True).replace(f'<h1 id="{e["id"]}"', "<h1") + "</div>")
ROUTER = """<script>
function route(){var h=location.hash.replace('#','')||'home';if(h==='top'){h='home';}
document.querySelectorAll('.entry').forEach(function(d){d.classList.remove('show')});
var el=document.getElementById(h)||document.getElementById('home');el.classList.add('show');window.scrollTo(0,0);
if(window.MathJax&&MathJax.typesetPromise){MathJax.typesetPromise([el]);}}
window.addEventListener('hashchange',route);window.addEventListener('DOMContentLoaded',route);
</script>"""
open(os.path.join(SITE, "all.html"), "w", encoding="utf-8").write(shell("The Observation Theory Encyclopedia", "\n".join(single) + ROUTER, single=True))
print("wrote", SITE, "pages", len(entries) + 7, "single file", os.path.getsize(os.path.join(SITE, "all.html")) // 1024, "KB")
