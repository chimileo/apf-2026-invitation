#!/usr/bin/env python3
"""Build the public website into _site/.

    python build.py

Joins src/head.html (the public <head>: link preview and "don't index" tags)
with src/invitation.html (the master page, also published to claude.ai),
checks public/photos.json, and copies public/ alongside. GitHub runs this on
every pull request and on every change to main. Standard library only.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "invitation.html"
HEAD = ROOT / "src" / "head.html"
PUBLIC = ROOT / "public"
OUT = ROOT / "_site"

# Lines at the top of src/invitation.html that only make sense on claude.ai.
# The public head supplies its own title and description.
ARTIFACT_ONLY = (
    re.compile(r"^<title>.*</title>\s*$"),
    re.compile(r'^<meta name="claude:[^"]*"'),
    re.compile(r'^<meta name="description"'),
)
# claude.ai wraps the page itself, so the master page must not carry its own skeleton.
SKELETON = re.compile(r"<!doctype|<html[\s>]|<head[\s>]|<body[\s>]", re.IGNORECASE)
PHOTO_SRC = re.compile(r"^photos/[A-Za-z0-9_.\-]+$")


def fail(msg: str) -> None:
    print(f"build failed: {msg}", file=sys.stderr)
    sys.exit(1)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def page_body() -> str:
    lines = read(SRC).splitlines(keepends=True)
    top = [l for l in lines[:10] if not any(p.match(l) for p in ARTIFACT_ONLY)]
    body = "".join(top + lines[10:])
    m = SKELETON.search(body)
    if m:
        fail(f"src/invitation.html must not contain {m.group(0)!r}; claude.ai adds the page skeleton")
    return body


def check_photos() -> int:
    try:
        photos = json.loads(read(PUBLIC / "photos.json"))
    except json.JSONDecodeError as e:
        fail(f"public/photos.json is not valid JSON: {e}")
    if not isinstance(photos, list):
        fail("public/photos.json must be a list, for example []")
    for i, p in enumerate(photos):
        if not isinstance(p, dict) or not isinstance(p.get("src"), str):
            fail(f'public/photos.json entry {i} needs a "src" text value')
        if not PHOTO_SRC.match(p["src"]):
            fail(f"public/photos.json entry {i}: src must look like photos/name.jpg (got {p['src']!r})")
        if not (PUBLIC / p["src"]).is_file():
            fail(f"public/photos.json entry {i}: public/{p['src']} does not exist")
        if "caption" in p and not isinstance(p["caption"], str):
            fail(f"public/photos.json entry {i}: caption must be text")
    return len(photos)


def main() -> None:
    head = read(HEAD)
    if 'name="robots" content="noindex' not in head:
        fail("src/head.html must keep the robots noindex tag")
    body = page_body()
    count = check_photos()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(PUBLIC, OUT, ignore=shutil.ignore_patterns(".gitkeep"))
    with open(OUT / "index.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(head + body + "\n</body>\n</html>\n")
    print(f"built _site/ with {count} forum photo{'' if count == 1 else 's'}")


if __name__ == "__main__":
    main()
