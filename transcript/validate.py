"""Validate the tspu-docs chapters: links, section references, contents, navigation, images.

Usage:
    python3 -I transcript/validate.py [--online] [--strict] [slug ...]

Reads README.md, docs/*.md and the stubs in chapters/*.md, and reports:

  links    local link targets exist; #anchors match a heading (GitHub slug rules)
  refs     «раздел N.N» references, linked or plain, and numbered link texts point
           to headings that exist (in the linked file, or in chapter N)
  toc      README contents match each chapter's H1 and numbered ## headings;
           heading numbers follow the chapter number and run in sequence
  nav      the navigation lines link the previous and next chapter in README order
  stubs    nothing in docs/ or README.md links to the old chapters/ pages
  lecture  docs/ never mentions the lecture, the recording or the slides
           (a plain mention of YouTube is only a warning: it may be about the service)
  images   image files exist; alt texts are real; alt texts, captions and file
           names never mention the lecture. Warnings: no caption, file over 300 KB,
           width attribute larger than the picture, unused file in docs/images/,
           and missing or placeholder alt texts on the existing remote (GitHub
           attachment) images; their chapter sessions write real ones, so none are
           left by the final pass (only replacing such an image is a proposal).
  terms    (warnings) names that came from speech recognition or the vendor manuals
           where the slides show another form, e.g. `show counters div`, `call rdp
           install`, `firmware reset`; README included. The list is TERMS below.
  vendor   (warnings) vendor attributions such as «по документации производителя» or
           «в более поздних версиях ПО»: each one is checked against the video in its
           chapter session; the fact stays without the attribution, or goes.

--online also fetches remote images; without it they are counted but not fetched.
--strict reports every warning as an error; the final pass runs with it.
Slugs (e.g. echelon) limit the report to those chapters; everything is still read,
so cross-references are checked in full.
Exit status: 1 if the report contains errors, otherwise 0.
"""

import argparse
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STUBS = ROOT / "chapters"
IMAGES = DOCS / "images"
README = ROOT / "README.md"

LECTURE = re.compile(
    r"лекци|лектор|слайд|таймкод|тайм-код|транскрипт|видеозапис|вебинар|докладчик|презентаци", re.I
)
VIDEO = re.compile(r"youtube\.com|youtu\.be|raNP3IMgwRU", re.I)
YOUTUBE = re.compile(r"youtube|ютуб", re.I)
IMAGE_TEXT = re.compile(
    LECTURE.pattern + r"|youtube|youtu\.be|ютуб|из видео|кадр из|скриншот|снимок экрана|спикер", re.I
)
IMAGE_NAME = re.compile(
    r"lecture|lektsi|lekci|slide|slajd|transcript|youtube|video|timecode|timestamp|screenshot|kadr"
    r"|\d{3}_\d-\d\d-\d\d",
    re.I,
)
PLACEHOLDER_ALT = {
    "image", "img", "picture", "pic", "photo", "screenshot",
    "изображение", "картинка", "рисунок", "фото", "скриншот", "снимок",
}
MAX_IMAGE_BYTES = 300 * 1024

# Forms in the docs that came from speech recognition or the vendor manuals, with what the
# slides (or the transcript) show instead: pattern, hint, optional file-name filter.
TERMS = [
    (r"show counters div\b", "`show counters diff` (slide 084)", None),
    (r"show syslog", "`show logs` (slide 085)", None),
    (r"show ip if\b", "`show ipif` (slide 078)", None),
    (r"show statistic\b", "`show statistics` (slide 083)", None),
    (r"show dpi (?:match|state|records)", "one word: `show dpimatch`, `show dpistate`, `show dpirecords` (slides 086, 087)", None),
    (r"\bdpi (?:load|run)\b", "one word: `dpiload`, `dpirun` (slide 086)", None),
    (r"\bdpi lists?\b", "`dpilist`; the branch is `system dpi dpilistN` (slides 046, 075)", None),
    (r"list_0\.dpi", "`list0.dpi` (4:09:38)", None),
    (r"3\.14\.040", "`3.1.4.0.40.bp` (slide 078)", None),
    (r"\b40(?:31|38)\b", "`3.1.4.0.31.bp`, `3.1.4.0.38.bp` (slide 049)", r"^filter-firmware"),
    (r"show xl\b", "`show xlate` (slide 043)", None),
    (r"show session\b", "`show sessions` (slides 043, 044)", None),
    (r"show sessions? (?:la|ga|ra)\b|`(?:la|ga|ra)`", "`lap`, `gap`, `rap` (slide 044)", None),
    (r"firmware reset\b(?!-)", "`firmware revert` (slide 051)", None),
    (r"\breload\b", "`reboot`, confirmed with y (slide 051)", r"^filter"),
    (r"\bfb on\b", "`fallback on` (slide 058)", None),
    (r"secret 15", "`secret 5` is the stored hash, 15 the privilege level (slide 057)", None),
    (r"time shift", "`timeskew` (slide 061)", None),
    (r"access-lists", "`acls` (slide 046)", None),
    (r"mng-if", "`mng_if` on the filter (slides 046, 053)", r"^filter"),
    (r"\bgo to\b", "`goto` (slides 068, 069)", None),
    (r"aclacl|create acl acl", "`create acl fake` creates `aclfake` (slide 068)", None),
    (r"\bno-ip\b", "`no_ip` (slide 075)", None),
    (r"\bbehavior\b", "`behaviour` (slides 075, 077)", None),
    (r"send RST\b", "`send_rst` (slide 072)", None),
    (r"extra analysis", "`extra_analyze` (slide 072)", None),
    (r"6212(?!U)", "Xeon Gold 6212U (slides 036, 119)", None),
    (r"EcoFilter (?:20|40)\b", "EcoFilter 2020 / 2040 (slides 033, 034)", None),
    (r"\bP[49][1-4]\b", "`p4-1`-style port names (slide 027)", None),
    (r"call rdp install|call rdp firmware",
     "`call rdp-firmware download from-url … to-file …`, `call rdp-firmware install from-file …` (slide 118)", None),
    (r"show rdp firmware", "`show rdp-firmware` (slide 126)", None),
    (r"show hardware info",
     "`show hardware-info [all | cpu | fans | memory | platform-info | psu | sensors | storage]` (slide 125)", None),
    (r"show mng if\b", "`show mng-if` (slide 125)", None),
    (r"show port \S+ (?:sfp|statistics)",
     "`show port tranceiver-eeprom port-number N`, `show port statistic port pX-Y` (slide 127)", None),
    (r"show (?:balance-group|filters)\b",
     "`show ecofilter-balancer balance-groups`, `show ecofilter-balancer filters … flows …` (slides 128, 129)", None),
    (r"set ports\b", "`port label pN-L { number … lane … speed … mtu … }` (slides 117, 119)", None),
    (r"\b(?:lan|wan)-port\b", "`lan` / `wan` inside `links` and `filter-group` (slides 120, 121)", None),
    (r"set liveness profile", "`liveness-profiles <имя> { … }` (slide 121)", None),
    (r"vlan 0 id", "`vlan0-tag N` (slides 122, 123)", None),
    (r"bypass-unit|udp-port", "`bypass-watchdog-groups … tcp-port 4001` (slide 124)", None),
    (r"set management\b", "`mng-if { addresses default { … } routes default { … } }` (slides 124, 125)", None),
    (r"set-bypass-ecofilter-unit|profile-status|balancing-config-hash",
     "a vendor-manual command; the lecture shows none (5:13:44)", None),
]
TERMS = [(re.compile(p), hint, files) for p, hint, files in TERMS]
VENDOR = re.compile(
    r"(?:по|в|согласно)\s+(?:документаци|руководств)\w*(?:\s+пользовател\w*)?\s+"
    r"(?:производител|вендор|EcoSGE|Silicom|RDP)\w*"
    r"|(?:по|в)\s+руководств\w*\s+пользовател\w*"
    r"|производител\w*\s+(?:описыва|указыва|приводит|рекоменду)\w*"
    r"|в\s+(?:более\s+)?(?:поздн|нов)\w+\s+(?:верси\w*\s+(?:ПО|прошив\w*)|прошивк\w*)"
    r"|по\s+данным\s+производител\w*|datasheet|даташит",
    re.I,
)

SECNUM = r"\d+(?:\.\d+)*"
REF = re.compile(rf"[Рр]аздел[а-яё]*\s+({SECNUM}(?:\s*(?:,|–|—|-|и)\s*{SECNUM})*)")
BARE_REF = re.compile(r"\d+(?:\.\d+)+(?:\s*[–—-]\s*\d+(?:\.\d+)+)?")
CHAPTER_ENTRY = re.compile(r"(\d+)\.\s+(.+)")
LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)]*)\)")
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
ATTR = re.compile(r'([\w-]+)\s*=\s*"([^"]*)"')
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)\.\s+(.*)$")
FENCE = re.compile(r"^\s{0,3}(```|~~~)")
README_ENTRY = re.compile(r"^####\s+\[(\d+)\.\s+(.+?)\]\(([^)]+)\)\s*$")
README_SUB = re.compile(r"^-\s+(\d+(?:\.\d+)+)\.\s+(.*?)\s*$")
CAPTION = re.compile(r"^\s*([_*])(?![\s_*]).*(?<!\s)\1\s*$")


@dataclass
class Heading:
    level: int
    text: str
    line: int
    slug: str
    num: str | None
    title: str


@dataclass
class Doc:
    path: Path
    lines: list[str]
    code: list[bool]
    headings: list[Heading] = field(default_factory=list)

    @property
    def h1(self):
        return next((h for h in self.headings if h.level == 1), None)

    @property
    def chapter(self):
        return self.h1.num if self.h1 else None

    @property
    def numbers(self):
        return {h.num for h in self.headings if h.num}

    @property
    def anchors(self):
        return {h.slug for h in self.headings}

    def by_slug(self, slug):
        return next((h for h in self.headings if h.slug == slug), None)

    def text_lines(self):
        """(line number, line with inline code blanked) for lines outside fenced code."""
        for i, line in enumerate(self.lines):
            if not self.code[i]:
                yield i + 1, re.sub(r"`[^`]*`", lambda m: " " * len(m.group()), line)


@dataclass
class Finding:
    severity: str
    check: str
    path: Path
    line: int
    msg: str
    chapter: str | None = None


def rel(path):
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def gh_slug(text):
    """GitHub heading anchor: rendered text, lowercased, punctuation dropped, spaces to hyphens."""
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    t = re.sub(r"<[^>]+>", "", t).replace("`", "").strip().lower()
    keep = (c for c in t if c.isalnum() or c in "-_ " or unicodedata.category(c).startswith("M"))
    return "".join(keep).replace(" ", "-")


def parse(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    code, fence = [], None
    for line in lines:
        m = FENCE.match(line)
        if fence:
            code.append(True)
            if m and m.group(1) == fence:
                fence = None
        elif m:
            code.append(True)
            fence = m.group(1)
        else:
            code.append(False)
    doc = Doc(path, lines, code)
    seen = {}
    for i, line in enumerate(lines):
        m = None if code[i] else HEADING.match(line)
        if not m:
            continue
        text = m.group(2)
        slug = gh_slug(text)
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug}-{seen[slug]}"
        else:
            seen[slug] = 0
        n = NUMBERED.match(text)
        doc.headings.append(
            Heading(len(m.group(1)), text, i + 1, slug, n.group(1) if n else None, n.group(2) if n else text)
        )
    return doc


class Validator:
    def __init__(self, online):
        self.online = online
        self.findings = []
        self.cache = {}
        self.readme = self.doc(README)
        self.chapters = [self.doc(p) for p in sorted(DOCS.glob("*.md"))]
        self.stubs = [self.doc(p) for p in sorted(STUBS.glob("*.md"))]
        self.by_number = {d.chapter: d for d in self.chapters if d.chapter}
        self.entries = self.readme_entries()
        self.captions = {}
        self.remote_images = []

    def doc(self, path):
        path = path.resolve()
        if path not in self.cache:
            self.cache[path] = parse(path) if path.is_file() and path.suffix == ".md" else None
        return self.cache[path]

    def add(self, severity, check, path, line, msg, chapter=None):
        self.findings.append(Finding(severity, check, path, line, msg, chapter))

    def readme_entries(self):
        entries, current = [], None
        for no, line in enumerate(self.readme.lines, 1):
            if self.readme.code[no - 1]:
                continue
            m = README_ENTRY.match(line)
            if m:
                current = {
                    "num": m.group(1), "title": m.group(2), "line": no,
                    "path": (README.parent / unquote(m.group(3))).resolve(), "subs": [],
                }
                entries.append(current)
            elif line.startswith("#"):
                current = None
            elif current and (s := README_SUB.match(line)):
                current["subs"].append((s.group(1), s.group(2), no))
        return entries

    # links, refs, stubs ------------------------------------------------------------

    def check_links(self):
        for doc in [self.readme, *self.chapters, *self.stubs]:
            for no, line in doc.text_lines():
                for m in LINK.finditer(line):
                    if m.group(1):
                        continue
                    self.check_link(doc, no, m.group(2), m.group(3))

    def check_link(self, doc, no, text, target):
        target = target.strip()
        target = target.split()[0].strip("<>") if target else ""
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            return
        part, _, anchor = target.partition("#")
        dest = doc.path if not part else (doc.path.parent / unquote(part)).resolve()
        if not dest.exists():
            self.add("error", "links", doc.path, no, f"missing target {target}")
            return
        if STUBS in dest.parents and doc.path.parent != STUBS:
            self.add("error", "stubs", doc.path, no, f"link to an old chapters/ page: {target}")
        tdoc = self.doc(dest)
        heading = None
        if anchor:
            anchor = unquote(anchor).lower()
            if tdoc is None:
                self.add("error", "links", doc.path, no, f"anchor #{anchor} on a non-Markdown target {target}")
            elif anchor not in tdoc.anchors:
                self.add("error", "links", doc.path, no, f"no heading for #{anchor} in {rel(dest)}")
            else:
                heading = tdoc.by_slug(anchor)
        if tdoc is not None:
            self.check_link_text(doc, no, text, tdoc, heading)

    def check_link_text(self, doc, no, text, tdoc, heading):
        nums = [n for m in REF.finditer(text) for n in re.findall(SECNUM, m.group(1))]
        if not nums and BARE_REF.fullmatch(text.strip()):
            nums = re.findall(SECNUM, text)
        entry = CHAPTER_ENTRY.fullmatch(text.strip())
        if not nums and entry and doc is not self.readme:
            nums = [entry.group(1)]
            h1 = tdoc.h1
            if h1 and h1.num == entry.group(1) and norm(h1.title) != norm(entry.group(2)):
                self.add("warning", "refs", doc.path, no,
                         f"link text «{text}» differs from the H1 «{h1.text}» of {rel(tdoc.path)}")
        for n in nums:
            chapter = n.split(".")[0]
            if tdoc.chapter != chapter:
                where = f"chapter {tdoc.chapter}" if tdoc.chapter else "not a chapter"
                self.add("error", "refs", doc.path, no,
                         f"«{text}» names {'chapter' if '.' not in n else 'section'} {n}, "
                         f"but links to {rel(tdoc.path)} ({where})")
            elif "." in n and n not in tdoc.numbers:
                self.add("error", "refs", doc.path, no, f"«{text}»: no section {n} in {rel(tdoc.path)}")
            elif heading and "." in n and len(nums) == 1 and heading.num != n:
                self.add("error", "refs", doc.path, no,
                         f"«{text}» links to the anchor of section {heading.num or heading.text}")

    def check_plain_refs(self):
        for doc in self.chapters + self.stubs:
            for no, line in doc.text_lines():
                spans = [(m.start(2), m.end(2)) for m in LINK.finditer(line)]
                for m in REF.finditer(line):
                    if any(a <= m.start() < b for a, b in spans):
                        continue
                    for n in re.findall(SECNUM, m.group(1)):
                        target = self.by_number.get(n.split(".")[0])
                        if target is None:
                            self.add("error", "refs", doc.path, no, f"«{m.group(0)}»: there is no chapter {n.split('.')[0]}")
                        elif "." in n and n not in target.numbers:
                            self.add("error", "refs", doc.path, no,
                                     f"«{m.group(0)}»: no section {n} in {rel(target.path)}")

    # contents and headings -------------------------------------------------------------

    def check_toc(self):
        listed = set()
        for i, e in enumerate(self.entries, 1):
            if e["num"] != str(i):
                self.add("error", "toc", README, e["line"], f"README chapter numbers out of sequence: {e['num']} where {i} was expected")
            doc = self.doc(e["path"])
            if doc is None:
                continue
            listed.add(doc.path)
            slug = doc.path.stem
            h1 = doc.h1
            if h1 is None:
                self.add("error", "toc", doc.path, 1, "no H1 heading", slug)
                continue
            if h1.num != e["num"] or norm(h1.title) != norm(e["title"]):
                self.add("error", "toc", doc.path, h1.line,
                         f"H1 «{h1.text}» ≠ README «{e['num']}. {e['title']}» (README:{e['line']})", slug)
            subs = {num: (title, line) for num, title, line in e["subs"]}
            heads = {h.num: h for h in doc.headings if h.level == 2 and h.num}
            for num, (title, line) in subs.items():
                if num not in heads:
                    self.add("error", "toc", README, line, f"README lists {num}. «{title}», {rel(doc.path)} has no such ## heading", slug)
                elif norm(heads[num].title) != norm(title):
                    self.add("error", "toc", doc.path, heads[num].line,
                             f"heading «{heads[num].text}» ≠ README «{num}. {title}» (README:{line})", slug)
            for num, h in heads.items():
                if num not in subs:
                    self.add("error", "toc", doc.path, h.line, f"heading «{h.text}» is missing from the README contents", slug)
            common_readme = [n for n, _, _ in e["subs"] if n in heads]
            common_doc = [n for n in heads if n in subs]
            if common_readme != common_doc:
                self.add("error", "toc", README, e["line"], f"README lists the sections of {rel(doc.path)} in a different order", slug)
            self.check_numbering(doc)
        for doc in self.chapters:
            if doc.path not in listed:
                self.add("error", "toc", doc.path, 1, "chapter is not in the README contents", doc.path.stem)

    def check_numbering(self, doc):
        chapter, slug = doc.chapter, doc.path.stem
        last, seen = {}, set()
        for h in doc.headings:
            if h.level == 1:
                if h is not doc.h1:
                    self.add("error", "toc", doc.path, h.line, f"second H1 «{h.text}»", slug)
                continue
            if not h.num:
                if h.level == 2:
                    self.add("warning", "toc", doc.path, h.line,
                             f"unnumbered ## heading «{h.text}» (not in the README contents)", slug)
                continue
            parts = h.num.split(".")
            parent = ".".join(parts[:-1])
            if parts[0] != chapter:
                self.add("error", "toc", doc.path, h.line, f"heading {h.num} in chapter {chapter}", slug)
            elif len(parts) != h.level:
                self.add("error", "toc", doc.path, h.line,
                         f"heading {h.num} is at level {'#' * h.level}; expected {'#' * len(parts)}", slug)
            elif len(parts) > 2 and parent not in seen:
                self.add("error", "toc", doc.path, h.line, f"heading {h.num} has no parent heading {parent}", slug)
            elif int(parts[-1]) != last.get(parent, 0) + 1:
                self.add("error", "toc", doc.path, h.line,
                         f"heading {h.num} out of sequence (expected {parent}.{last.get(parent, 0) + 1})", slug)
            last[parent] = int(parts[-1])
            seen.add(h.num)

    # navigation ------------------------------------------------------------------------

    def check_nav(self):
        docs = [self.doc(e["path"]) for e in self.entries]
        for i, doc in enumerate(docs):
            if doc is None:
                continue
            prev = docs[i - 1] if i > 0 else None
            nxt = docs[i + 1] if i + 1 < len(docs) else None
            slug = doc.path.stem
            navs = [(no, line) for no, line in doc.text_lines() if "Оглавление" in line and "README.md" in line]
            if len(navs) != 2:
                self.add("error", "nav", doc.path, navs[0][0] if navs else 1,
                         f"expected 2 navigation lines (top and bottom), found {len(navs)}", slug)
                if not navs:
                    continue
            nonblank = [no for no, line in enumerate(doc.lines, 1) if line.strip()]
            if navs[0][0] > 5:
                self.add("warning", "nav", doc.path, navs[0][0], "top navigation line is not right under the H1", slug)
            if navs[-1][0] != nonblank[-1]:
                self.add("warning", "nav", doc.path, navs[-1][0], "bottom navigation line is not the last line", slug)
            for where, (no, line) in (("top", navs[0]), ("bottom", navs[-1])):
                links = [(m.group(2).strip(), m.group(3)) for m in LINK.finditer(line) if not m.group(1)]
                back = [(t, (doc.path.parent / unquote(u)).resolve()) for t, u in links
                        if t.startswith("←") and "Оглавление" not in t]
                fwd = [(t, (doc.path.parent / unquote(u)).resolve()) for t, u in links if t.endswith("→")]
                # The top line may omit the next-chapter link; the bottom line needs both.
                for kind, got, want in (
                    ("previous", [p for _, p in back], [prev.path] if prev else []),
                    ("next", [p for _, p in fwd], [nxt.path] if nxt and (fwd or where == "bottom") else []),
                ):
                    if got != want:
                        self.add("error", "nav", doc.path, no,
                                 f"{where}: {kind}-chapter link goes to {', '.join(map(rel, got)) or 'nothing'}; "
                                 f"expected {', '.join(map(rel, want)) or 'none'}", slug)
                for text, path in back + fwd:
                    target = self.doc(path)
                    m = re.search(r"Раздел\s+\d+:\s*(.+?)\s*→?$", text)
                    if target and target.h1 and m and not norm(target.h1.title).startswith(norm(m.group(1))):
                        self.add("warning", "nav", doc.path, no,
                                 f"{where}: «{m.group(1)}» is not the start of the H1 «{target.h1.title}»", slug)

    # lecture words -----------------------------------------------------------------------

    def check_lecture(self):
        for doc in self.chapters:
            for i, raw in enumerate(doc.lines, 1):
                if (doc.path, i) in self.captions:
                    continue
                line = IMG_TAG.sub(" ", LINK.sub(lambda m: " " if m.group(1) else m.group(0), raw))
                for m in LECTURE.finditer(line):
                    self.add("error", "lecture", doc.path, i, f"lecture word «{context(line, m)}»")
                video = list(VIDEO.finditer(line))
                if video:
                    self.add("error", "lecture", doc.path, i, f"link to the recording «{context(line, video[0])}»")
                for m in YOUTUBE.finditer(line):
                    if not any(v.start() <= m.start() < v.end() for v in video):
                        self.add("warning", "lecture", doc.path, i, f"mentions YouTube «{context(line, m)}»: fine only if it is about the service")

    # wording ---------------------------------------------------------------------------------

    def chapter_of(self, doc, no):
        """The chapter a line belongs to: the file's own, or the README entry the line sits under."""
        if doc is not self.readme:
            return doc.path.stem
        for e in self.entries:
            last = e["subs"][-1][2] if e["subs"] else e["line"]
            if e["line"] <= no <= last:
                return e["path"].stem
        return None

    def check_terms(self):
        for doc in [self.readme, *self.chapters]:
            for no, line in enumerate(doc.lines, 1):
                for pattern, hint, files in TERMS:
                    if files and not re.search(files, doc.path.name):
                        continue
                    for m in pattern.finditer(line):
                        self.add("warning", "terms", doc.path, no, f"«{m.group(0)}» → {hint}", self.chapter_of(doc, no))

    def check_vendor(self):
        for doc in [self.readme, *self.chapters]:
            for no, line in enumerate(doc.lines, 1):
                if m := VENDOR.search(line):
                    self.add("warning", "vendor", doc.path, no,
                             f"vendor attribution «{context(line, m)}»: keep the fact only where the slides "
                             f"or transcript support it, without the attribution", self.chapter_of(doc, no))

    # images --------------------------------------------------------------------------------

    def check_images(self):
        used = set()
        for doc in [self.readme, *self.chapters]:
            for no, line in doc.text_lines():
                found = []
                for tag in IMG_TAG.finditer(doc.lines[no - 1]):
                    attrs = {k.lower(): v for k, v in ATTR.findall(tag.group(0))}
                    found.append((attrs.get("src", ""), attrs.get("alt"), attrs.get("width")))
                for m in LINK.finditer(doc.lines[no - 1]):
                    if m.group(1):
                        found.append((m.group(3).strip().split()[0] if m.group(3).strip() else "", m.group(2), None))
                for src, alt, width in found:
                    used |= self.check_image(doc, no, src, alt, width)
        if IMAGES.is_dir():
            for f in sorted(IMAGES.rglob("*")):
                if f.is_file() and f.resolve() not in used:
                    self.add("warning", "images", f, 0, "image file is not used by any chapter")

    def check_image(self, doc, no, src, alt, width):
        slug = doc.path.stem if doc is not self.readme else None
        remote = bool(re.match(r"^https?://", src, re.I))
        alt_severity = "warning" if remote else "error"
        if alt is None:
            self.add(alt_severity, "images", doc.path, no, "image has no alt text", slug)
        elif not alt.strip():
            self.add(alt_severity, "images", doc.path, no, "image has an empty alt text", slug)
        elif alt.strip().lower() in PLACEHOLDER_ALT or re.search(r"\.(png|jpe?g|gif|svg|webp)$|^screenshot\b", alt.strip(), re.I):
            self.add(alt_severity, "images", doc.path, no, f'placeholder alt text "{alt}": write a real one', slug)
        if alt and (m := IMAGE_TEXT.search(alt)):
            self.add("error", "images", doc.path, no, f"alt text mentions the lecture «{context(alt, m)}»", slug)
        self.check_caption(doc, no, slug)
        if not src:
            self.add("error", "images", doc.path, no, "image without a source", slug)
            return set()
        if remote:
            self.remote_images.append((doc, no, src))
            return set()
        path = (doc.path.parent / unquote(src)).resolve()
        if not path.is_file():
            self.add("error", "images", doc.path, no, f"missing image file {src}", slug)
            return set()
        if m := IMAGE_NAME.search(path.relative_to(DOCS).as_posix() if DOCS in path.parents else path.name):
            self.add("error", "images", doc.path, no, f"image file name mentions the lecture or a slide: {src}", slug)
        size = path.stat().st_size
        if size > MAX_IMAGE_BYTES:
            self.add("warning", "images", doc.path, no, f"{src} is {size // 1024} KB (limit about {MAX_IMAGE_BYTES // 1024} KB)", slug)
        real = pixel_width(path)
        if width and width.isdigit() and real and int(width) > real:
            self.add("warning", "images", doc.path, no, f'width="{width}" upscales {src}, which is {real} px wide', slug)
        return {path}

    def check_caption(self, doc, no, slug):
        for i in range(no, len(doc.lines)):
            line = doc.lines[i]
            if not line.strip():
                continue
            if CAPTION.match(line):
                self.captions[(doc.path, i + 1)] = line
                if m := IMAGE_TEXT.search(line):
                    self.add("error", "images", doc.path, i + 1, f"caption mentions the lecture «{context(line, m)}»", slug)
            else:
                self.add("warning", "images", doc.path, no, "image has no caption (an italic line right after it)", slug)
            return
        self.add("warning", "images", doc.path, no, "image has no caption (an italic line right after it)", slug)

    def check_remote(self):
        for doc, no, src in self.remote_images:
            ok, status = fetch_ok(src)
            if not ok:
                self.add("error", "images", doc.path, no, f"remote image does not load ({status}): {src}",
                         doc.path.stem if doc is not self.readme else None)

    def run(self):
        self.check_links()
        self.check_plain_refs()
        self.check_toc()
        self.check_nav()
        self.check_images()
        self.check_lecture()
        self.check_terms()
        self.check_vendor()
        if self.online:
            self.check_remote()


def context(text, m, width=25):
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    return ("…" if a else "") + text[a:b].strip() + ("…" if b < len(text) else "")


def pixel_width(path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big")
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return int.from_bytes(data[6:8], "little")
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data) and data[i] == 0xFF:
            marker = data[i + 1]
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                return int.from_bytes(data[i + 7:i + 9], "big")
            i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
    return None


def fetch_ok(url):
    request = urllib.request.Request(url, headers={"Range": "bytes=0-0", "User-Agent": "tspu-docs-validate"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status in (200, 206), response.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except (urllib.error.URLError, TimeoutError) as e:
        return False, getattr(e, "reason", e)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("slugs", nargs="*", help="limit the report to these chapters (docs/<slug>.md)")
    parser.add_argument("--online", action="store_true", help="also fetch remote images")
    parser.add_argument("--strict", action="store_true", help="report every warning as an error (final pass)")
    args = parser.parse_args()

    v = Validator(args.online)
    unknown = [s for s in args.slugs if not (DOCS / f"{s}.md").is_file()]
    if unknown:
        sys.exit(f"no such chapter: {', '.join(unknown)}")
    v.run()

    findings = v.findings
    if args.slugs:
        files = {(DOCS / f"{s}.md").resolve() for s in args.slugs}
        findings = [f for f in findings if f.chapter in args.slugs or f.path.resolve() in files]
    if args.strict:
        for f in findings:
            f.severity = "error"
    order = {"error": 0, "warning": 1}
    findings.sort(key=lambda f: (order[f.severity], f.check, rel(f.path), f.line))

    scope = ", ".join(args.slugs) if args.slugs else f"README.md, {len(v.chapters)} chapters, {len(v.stubs)} stubs"
    print(f"validate.py: {scope}{' (strict)' if args.strict else ''}")
    for severity in ("error", "warning"):
        group = [f for f in findings if f.severity == severity]
        print(f"\n{severity.upper()}S: {len(group)}")
        for f in group:
            where = f"{rel(f.path)}:{f.line}" if f.line else rel(f.path)
            print(f"  [{f.check}] {where}  {f.msg}")
    remote = [r for r in v.remote_images if not args.slugs or r[0].path.stem in args.slugs]
    if remote and args.online:
        print(f"\nRemote images fetched: {len(remote)} (failures are listed as errors above)")
    elif remote:
        print(f"\nRemote images not fetched: {len(remote)} (run with --online to check that they load)")
    sys.exit(1 if any(f.severity == "error" for f in findings) else 0)


if __name__ == "__main__":
    main()
