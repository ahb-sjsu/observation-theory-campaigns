"""Copy the built site to the erisml-lib checkout, where GitHub Pages serves it at
https://erisml.org/encyclopedia/.

    python encyclopedia/build_site.py C:/source
    python encyclopedia/publish_site.py [C:/source/erisml-lib/docs/encyclopedia]

Then commit and push erisml-lib. The Pages workflow deploys docs/ on main.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site")
DST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(ROOT)), "erisml-lib", "docs", "encyclopedia")
if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
print("copied", len(os.listdir(DST)), "files to", DST)
