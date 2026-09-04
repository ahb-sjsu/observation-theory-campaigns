"""Acceptance test for the generator. Run from the repository root after generate.py:

    python encyclopedia/check.py <source root>

For each hand-filled entry in encyclopedia/entries/ with a generated counterpart in
encyclopedia/generated/, every number that appears in the hand-filled entry's measurements
and failures sections must appear in the generated entry, and every repository path cited in
either file must exist under the source root. Prose is not compared. A number the generator
cannot find is a record the generator does not yet read, or a number the hand-filled entry
should not have carried, and either way it is listed.
"""

import glob
import os
import re
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(sys.argv[1])
CFG = tomllib.load(open(os.path.join(HERE, "entries.toml"), "rb"))
REPOS = {name: os.path.join(SRC, rel) for name, rel in CFG["repos"].items()}
NUM = re.compile(r"(?<![\w.])\d+\.\d+(?!\d)|(?<![\w.])\d{2,}(?!\w)")
PATH = re.compile(r"`([A-Za-z0-9_.\-]+)[/\\]([^`:]+)(?::[\d,\-]+)?`")


def section(text, heading):
    m = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def cited_paths(text):
    out = []
    for repo, rel in PATH.findall(text):
        if repo in REPOS:
            out.append((repo, rel))
    return out


failures = 0
for hand in sorted(glob.glob(os.path.join(HERE, "entries", "*.md"))):
    eid = os.path.basename(hand)[:-3]
    gen = os.path.join(HERE, "generated", eid + ".md")
    if not os.path.exists(gen):
        print(f"{eid}: no generated entry")
        failures += 1
        continue
    h = open(hand, encoding="utf-8").read()
    g = open(gen, encoding="utf-8").read()
    strip = lambda t: re.sub(r"([0-9]),([0-9]{3})", lambda m: m.group(1) + m.group(2), t)  # thousands separators
    wanted = set(NUM.findall(strip(section(h, "measurements") + section(h, "failures and corrections"))))
    have = set(NUM.findall(strip(g)))
    missing = sorted(wanted - have, key=lambda s: (len(s), s))
    for repo, rel in cited_paths(h) + cited_paths(g):
        p = os.path.join(REPOS[repo], rel.replace("\\", "/"))
        if not os.path.exists(p):
            print(f"{eid}: cited path missing {repo}/{rel}")
            failures += 1
    print(f"{eid}: {len(wanted)} numbers in the hand-filled entry, {len(wanted) - len(missing)} found in the generated one"
          + (", missing " + ", ".join(missing) if missing else ""))
    if missing:
        failures += 1
sys.exit(1 if failures else 0)
