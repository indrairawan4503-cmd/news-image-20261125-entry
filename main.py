#!/usr/bin/env python3
"""Entry program for news-image-20261125 (variant A: classic broadsheet).

Copies the shipped front-page image to /output/entry.png. The image is
drawn by draw.py (PIL) at build time and shipped as entry.png; this program
is a deterministic byte-identical copy, standard library only, no network.
The grader runs with a read-only repo, so /output is written first and any
repo-root copy is guarded in try/except.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
