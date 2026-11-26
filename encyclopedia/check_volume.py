"""Check one volume's entry file without building anything.

    python encyclopedia/check_volume.py encyclopedia/volumes/<repo>.toml <volumes root>

Verifies what `generate.py` will require of the file: it parses, ids are new and well formed,
every entry has a definition, an example, conditions, and a `first_stated` that cites the
volume's files by line (files exist, lines in range), related ids exist, the online page is
in the volume's published site, and the prose rule holds (no em dash, colon or semicolon in a
sentence). Writes nothing.
"""

import os
import re
import subprocess
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
path, vroot = sys.argv[1], os.path.abspath(sys.argv[2])
v = tomllib.load(open(path, "rb"))
meta = v["volume"]
for k in ("number", "title", "repo", "slug", "standing"):
    assert k in meta, f"[volume] lacks {k}"
repo_dir = os.path.join(vroot, meta["repo"])
assert os.path.isdir(repo_dir), f"no checkout at {repo_dir}"
base = tomllib.load(open(os.path.join(HERE, "entries.toml"), "rb"))
existing = {e["id"] for e in base["entry"]}
for other in os.listdir(os.path.join(HERE, "volumes")):
    if other.endswith(".toml") and os.path.abspath(os.path.join(HERE, "volumes", other)) != os.path.abspath(path):
        try:
            existing |= {e["id"] for e in tomllib.load(open(os.path.join(HERE, "volumes", other), "rb")).get("entry", [])}
        except Exception:  # noqa: BLE001  another file being written
            pass
own = [e["id"] for e in v.get("entry", [])]
examples = v.get("examples", {})
problems = []
KINDS = {"concept", "instrument", "result", "correction"}
PROSE = re.compile(r"[—–;]|(?<![\d`/\w]):(?!//)")


def prose(eid, field, text):
    bare = re.sub(r"`[^`]*`|\$[^$]*\$", "", text)
    if PROSE.search(bare):
        problems.append(f"{eid}: {field} has an em dash, a colon or a semicolon in a sentence")


for e in v.get("entry", []):
    eid = e.get("id", "?")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", eid):
        problems.append(f"{eid}: id must be lowercase words joined by hyphens")
    if eid in existing:
        problems.append(f"{eid}: id already used by another entry")
    if own.count(eid) > 1:
        problems.append(f"{eid}: id appears twice in this file")
    if e.get("kind") not in KINDS:
        problems.append(f"{eid}: kind must be one of {sorted(KINDS)}")
    for f in ("title", "definition", "first_stated"):
        if not str(e.get(f, "")).strip():
            problems.append(f"{eid}: no {f}")
    if not e.get("conditions"):
        problems.append(f"{eid}: no conditions")
    if eid not in examples:
        problems.append(f"{eid}: no example")
    prose(eid, "definition", e.get("definition", ""))
    prose(eid, "example", examples.get(eid, ""))
    for c in e.get("conditions", []):
        prose(eid, "a condition", c)
    for f in ("known_as", "standing"):
        if e.get(f):
            prose(eid, f, e[f])
    cites = re.findall(r"`([\w.-]+)[\\/]([^`:]+?):(\d+)(?:-(\d+))?`", e.get("first_stated", ""))
    mine = [c for c in cites if c[0] == meta["repo"]]
    if not mine:
        problems.append(f"{eid}: first_stated cites no file of {meta['repo']} by line, as `{meta['repo']}/path:a-b`")
    for repo, rel, a, b in mine:
        p = os.path.join(repo_dir, rel)
        if not os.path.exists(p):
            problems.append(f"{eid}: cited file missing, {repo}/{rel}")
            continue
        n = sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
        if int(b or a) > n or int(a) < 1 or int(b or a) < int(a):
            problems.append(f"{eid}: {repo}/{rel}:{a}-{b or a} is outside the file's {n} lines")
    for r in e.get("related", []):
        if r not in existing and r not in own:
            problems.append(f"{eid}: related id '{r}' does not exist")
    page = e.get("online_page") or (os.path.splitext(os.path.basename(mine[0][1]))[0] + ".html" if mine else "")
    if page and page != "none":
        r = subprocess.run(["git", "cat-file", "-e", f"origin/site:{page}"], cwd=repo_dir, capture_output=True)
        if r.returncode != 0:
            problems.append(f"{eid}: online page {page} is not in the published site (set online_page; see `git ls-tree --name-only origin/site`)")
for k in examples:
    if k not in own:
        problems.append(f"example for unknown entry {k}")
prose("volume", "standing", meta["standing"])
print(f"{meta['title']}: {len(own)} entries, {len(problems)} problems")
for p in problems:
    print("  ", p)
sys.exit(1 if problems else 0)
