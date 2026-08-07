#!/usr/bin/env python3
"""Build the G1 domain pool mechanically from the arXiv taxonomy.

The first pool document listed two archive-level entries among
otherwise leaf-level entries, which is ambiguous, and its lists
were hand transcribed, which leaves discretion in a pool whose
purpose is to remove it. This script replaces transcription with
derivation. It fetches the published taxonomy once, keeps every
leaf category in the declared archive groups, removes the declared
exclusions, and freezes the result.

Run before any beacon value exists, so nothing it produces can be
steered toward a wanted draw.
"""
from __future__ import annotations

import json
import os
import platform
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from projection_fold import canonical_sha256  # noqa: E402

TAXONOMY_URL = "https://arxiv.org/category_taxonomy"

# archive groups, declared in the pool document
GROUPS = {
    "N": ["astro-ph", "cond-mat", "nucl-ex", "nucl-th", "physics",
          "nlin"],
    "F": ["math", "cs", "stat"],
    "A": ["q-bio", "q-fin", "econ", "eess"],
}

# areas that contributed to the kernel's construction
EXCLUSIONS = {
    "quant-ph", "cond-mat.stat-mech", "hep-th", "hep-ph", "gr-qc",
    "cs.IT", "math.IT", "cs.CR", "econ.TH", "nlin.CG",
}


PLACEHOLDER = "Description coming soon"


def fetch_descriptions(html):
    """Map category to its published description, exactly as
    printed. A category whose description is the placeholder has no
    description at all."""
    import re as _re
    blocks = _re.findall(
        r"<h4>([a-zA-Z.\-]+)\s*<span>.*?</span></h4>.*?<p>(.*?)</p>",
        html, _re.S)
    return {c: _re.sub(r"<[^>]+>", "", d).strip()
            for c, d in blocks}


def fetch_categories():
    req = urllib.request.Request(
        TAXONOMY_URL, headers={"User-Agent": "g1-pool-builder"})
    with urllib.request.urlopen(req, timeout=60) as fh:
        html = fh.read().decode("utf-8", "replace")
    globals()["_HTML"] = html
    found = set(re.findall(
        r"\b([a-z-]+(?:\.[A-Za-z-]+)?)\b(?=</span>)", html))
    # keep only identifiers that look like arXiv categories
    cats = set()
    for token in re.findall(r"[a-z-]+\.[A-Za-z-]+", html):
        cats.add(token)
    for bare in ("nucl-ex", "nucl-th", "quant-ph", "hep-th",
                 "hep-ph", "gr-qc", "hep-ex", "hep-lat",
                 "math-ph"):
        if bare in html:
            cats.add(bare)
    return sorted(cats | {c for c in found if "." in c})


def archive_of(cat):
    return cat.split(".")[0] if "." in cat else cat


def main() -> int:
    record: dict = {"schema": "g1-domain-pool-v2",
                    "label": "infrastructure"}
    cats = fetch_categories()
    desc = fetch_descriptions(globals()["_HTML"])
    # a category whose published description is the placeholder
    # cannot supply the experiment's required input, so it is
    # removed. The criterion is an exact match on the placeholder
    # and not a length threshold, because a length threshold would
    # also have removed stat.CO, whose description is terse but
    # real, and choosing a threshold after seeing the data is the
    # discretion this pool exists to eliminate.
    no_description = sorted(
        c for c in cats if desc.get(c, "").strip() == PLACEHOLDER)
    strata = {}
    for name, archives in GROUPS.items():
        keep = sorted({
            c for c in cats
            if archive_of(c) in archives and c not in EXCLUSIONS
            and c not in no_description
            and (("." in c) or c in ("nucl-ex", "nucl-th"))})
        strata[name] = keep
        print(f"stratum {name}: {len(keep)} categories", flush=True)

    record["taxonomy_url"] = TAXONOMY_URL
    record["fetched_utc"] = datetime.now(timezone.utc).isoformat()
    record["groups"] = GROUPS
    record["exclusions"] = sorted(EXCLUSIONS)
    record["removed_no_published_description"] = no_description
    record["placeholder_string"] = PLACEHOLDER
    record["descriptions"] = {
        c: desc.get(c, "")
        for st in strata.values() for c in st}
    record["strata"] = strata
    record["counts"] = {k: len(v) for k, v in strata.items()}
    record["notes"] = (
        "aliases are not deduplicated and a draw of an alias is "
        "treated as its subject; leaf categories only, with the "
        "two archives that have no subcategories kept as "
        "themselves")
    record["runtime"] = {
        "python": sys.version, "platform": platform.platform(),
        "hostname": platform.node(),
        "code_commit": os.environ.get("CODE_COMMIT", "unknown")}
    record["record_sha256"] = canonical_sha256(
        {k: v for k, v in record.items() if k != "runtime"})
    out = Path(__file__).resolve().parents[1] / "results" \
        / "g1-domain-pool.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True),
                   encoding="utf-8")
    for k, v in strata.items():
        print(f"{k}: {' '.join(v)}")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
