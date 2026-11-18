#!/usr/bin/env python3
"""Check reader articles in docs/updates/ before they are handed to the user.

Usage (from the repo root):
    python3 -I .claude/skills/tspu-digest/check_article.py [docs/updates/YYYY-MM-DD.md ...]

With no arguments, every article in docs/updates/ is checked.

Errors (exit 1):
  - a relative link whose target file does not exist;
  - a leftover register id (S001-style) or an internal path (transcript/, sources.md, findings-);
  - a word the chapters may not use (the lecture list from transcript/validate.py);
  - an article not listed in the README, or a README entry pointing to a missing article;
  - a broken prev/next chain between consecutive articles.

Warnings (review by hand):
  - an external URL that is not an exact match for a URL in transcript/research/sources.md
    (a typo, or a link assembled from a register note: open it and confirm);
  - a table separator row not written as "| --- |".
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
UPDATES = ROOT / "docs" / "updates"
REGISTER = ROOT / "transcript" / "research" / "sources.md"
README = ROOT / "README.md"

LINK = re.compile(r"\]\(([^)\s]+)\)")
URL = re.compile(r"https?://[^\s|;)]+")
SID = re.compile(r"\bS\d{3}\b")
INTERNAL = re.compile(r"transcript/|sources\.md|findings-\d")
LECTURE = re.compile(
    r"лекци|лектор|слайд|таймкод|тайм-код|транскрипт|видеозапис|вебинар|докладчик|презентаци", re.I
)
SEPARATOR = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
GOOD_SEPARATOR = re.compile(r"^\|( :?---:? \|)+$")
ARTICLE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


def main(argv):
    articles = sorted(p for p in UPDATES.glob("*.md") if ARTICLE.match(p.name))
    targets = [Path(a).resolve() for a in argv] if argv else articles
    register = {unquote(u) for u in URL.findall(REGISTER.read_text(encoding="utf-8"))}
    readme = README.read_text(encoding="utf-8")
    errors, warnings = [], []

    for path in targets:
        name = path.relative_to(ROOT)
        lines = path.read_text(encoding="utf-8").splitlines()
        for no, line in enumerate(lines, 1):
            where = f"{name}:{no}"
            for target in LINK.findall(line):
                if target.startswith("http"):
                    if unquote(target) not in register:
                        warnings.append(f"{where} URL not in the register exactly: {target}")
                elif not (path.parent / target.split("#")[0]).resolve().exists():
                    errors.append(f"{where} link target missing: {target}")
            for m in SID.finditer(line):
                errors.append(f"{where} register id left in the text: {m.group()}")
            if INTERNAL.search(line):
                errors.append(f"{where} internal path in the text: {line.strip()[:80]}")
            if m := LECTURE.search(line):
                errors.append(f"{where} forbidden word «{m.group()}»")
            if SEPARATOR.match(line) and not GOOD_SEPARATOR.match(line):
                warnings.append(f"{where} table separator not in '| --- |' style")
        if f"docs/updates/{path.name}" not in readme:
            errors.append(f"{name} is not listed in README.md")

    for listed in re.findall(r"\(docs/updates/([^)]+)\)", readme):
        if not (UPDATES / listed).exists():
            errors.append(f"README.md lists a missing article: docs/updates/{listed}")

    for older, newer in zip(articles, articles[1:]):
        if f"]({newer.name})" not in older.read_text(encoding="utf-8").splitlines()[2]:
            errors.append(f"{older.relative_to(ROOT)}: header has no link to the next article {newer.name}")
        if f"]({older.name})" not in newer.read_text(encoding="utf-8").splitlines()[2]:
            errors.append(f"{newer.relative_to(ROOT)}: header has no link to the previous article {older.name}")

    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARNING", w)
    print(f"{len(targets)} article(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
