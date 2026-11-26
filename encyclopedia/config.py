"""Load the encyclopedia's entry table: `entries.toml` plus one file per volume in `volumes/`.

`entries.toml` holds the Observation Theory entries, built from the program's records. A file
`volumes/<repo>.toml` holds the entries of one other volume of the Geometric Series:

    [volume]
    number = 4
    title = "Geometric Economics"
    repo = "geometric-economics"        # the volume's repository
    slug = "geometric-economics"        # its directory on erisml.org
    standing = "..."                    # what the volume says of its own evidence, with the source

    [[entry]]
    id = "bond-geodesic-equilibrium"
    kind = "concept"                    # concept, instrument, result, correction
    title = "Bond geodesic equilibrium"
    definition = "One or two sentences a reader can act on."
    first_stated = "Chapter 7, `geometric-economics/chapters/ch07_x.md:120-141`."
    conditions = ["...", "..."]
    known_as = "the prior art it sits beside"       # optional
    related = ["decision-manifold", "mahalanobis-distance"]
    standing = "..."                    # optional, overrides the volume's
    online_page = "ch07_x.html"         # optional, when the page name is not the cited file's stem

    [examples]
    bond-geodesic-equilibrium = "A line a student can check by hand."

A volume entry has no ledger rows of its own. Its `standing` says what kind of statement it is,
in the volume's own words (most volumes are posited frameworks), and prints where an
Observation Theory entry prints its ledger classes.

The volume repositories are read from `--volumes-root` (or the environment variable
ENC_VOLUMES_ROOT) when given, and from the source root otherwise. Use a root of clean,
up-to-date clones: an entry cites files by line, and the lines are checked against the
checkout the generator reads.
"""

import glob
import os
import sys
import tomllib


def volumes_root(default):
    for i, a in enumerate(sys.argv):
        if a == "--volumes-root" and i + 1 < len(sys.argv):
            return os.path.abspath(sys.argv[i + 1])
    return os.path.abspath(os.environ.get("ENC_VOLUMES_ROOT", default))


def load(here, src):
    cfg = tomllib.load(open(os.path.join(here, "entries.toml"), "rb"))
    cfg["examples"] = {}
    cfg["volumes"] = []
    cfg["repo_paths"] = {name: os.path.join(src, rel) for name, rel in cfg["repos"].items()}
    vroot = volumes_root(src)
    seen = {e["id"] for e in cfg["entry"]}
    for path in sorted(glob.glob(os.path.join(here, "volumes", "*.toml"))):
        v = tomllib.load(open(path, "rb"))
        meta = v["volume"]
        meta["file"] = os.path.basename(path)
        cfg["volumes"].append(meta)
        cfg["repos"][meta["repo"]] = meta["repo"]
        cfg["repo_paths"][meta["repo"]] = os.path.join(vroot, meta["repo"])
        for e in v.get("entry", []):
            if e["id"] in seen:
                raise SystemExit(f"{meta['file']}: entry id '{e['id']}' is already used")
            seen.add(e["id"])
            e["volume"] = meta
            e.setdefault("standing", meta.get("standing", ""))
            e.setdefault("strict", False)
            cfg["entry"].append(e)
        for k, text in v.get("examples", {}).items():
            cfg["examples"][k] = text
    return cfg
