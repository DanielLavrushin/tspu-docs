"""Build a readable Markdown transcript from YouTube json3 captions.

Usage:
    python3 -I transcript/build.py transcript/source/raNP3IMgwRU.ru-orig.json3 > transcript/transcript.md

Input is YouTube's automatic Russian recognition (track ru-orig), fetched with:
    uvx --with secretstorage yt-dlp --js-runtimes node --cookies-from-browser chrome \
        --ignore-no-formats-error --skip-download --write-auto-subs --sub-langs ru-orig \
        --sub-format json3 -o "transcript/source/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=raNP3IMgwRU"
(the video is age-restricted, so a signed-in browser session is required).

The text is not edited: words, recognition errors and punctuation stay as YouTube
produced them. The script only joins caption fragments into paragraphs at pauses and
sentence ends, capitalises each paragraph's first letter, and adds a timestamp link
per paragraph plus a heading every SECTION_S seconds.
"""

import json
import re
import sys

VIDEO_ID = "raNP3IMgwRU"
TITLE = "Архитектура и принципы работы ТСПУ"
CHANNEL = "xntwrkLAB | Exploitation Laboratory of Network"
SECTION_S = 15 * 60
SENTENCE_END = re.compile(r"[.?!…]$")


def hms(ms):
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def load_words(path):
    events = json.load(open(path, encoding="utf-8"))["events"]
    words = []
    for e in events:
        for seg in e.get("segs", []):
            for w in seg.get("utf8", "").split():
                words.append((e["tStartMs"] + seg.get("tOffsetMs", 0), w))
    words.sort(key=lambda x: x[0])
    return words


def should_break(n, word, gap):
    sentence_end = bool(SENTENCE_END.search(word))
    return (
        (n >= 40 and gap >= 2000)
        or (n >= 60 and sentence_end and gap >= 700)
        or (n >= 120 and (sentence_end or gap >= 1200))
        or n >= 220
    )


def paragraphs(words):
    para = []
    for i, (t, w) in enumerate(words):
        para.append((t, w))
        nxt = words[i + 1][0] if i + 1 < len(words) else None
        if nxt is None or should_break(len(para), w, nxt - t):
            yield para
            para = []


def render(words):
    end_ms = words[-1][0]
    out = [
        f"# {TITLE}",
        "",
        f"- Видео: https://www.youtube.com/watch?v={VIDEO_ID}",
        f"- Канал: {CHANNEL}",
        f"- Длительность: {hms(end_ms)}",
        "- Источник текста: автоматические русские субтитры YouTube (дорожка ru-orig), без ручной правки.",
        "  Ошибки распознавания сохранены; метка времени в начале абзаца открывает видео с этого места.",
        "",
    ]
    next_section = 0
    for para in paragraphs(words):
        start = para[0][0]
        while start >= next_section * 1000:
            lo, hi = next_section, min(next_section + SECTION_S, end_ms // 1000 + 1)
            out += [f"## {hms(lo * 1000)} – {hms(hi * 1000)}", ""]
            next_section += SECTION_S
        text = " ".join(w for _, w in para)
        text = text[:1].upper() + text[1:]
        out += [f"[{hms(start)}](https://youtu.be/{VIDEO_ID}?t={start // 1000}) {text}", ""]
    return "\n".join(out)


def main():
    words = load_words(sys.argv[1])
    sys.stdout.write(render(words))
    paras = list(paragraphs(words))
    sizes = sorted(len(p) for p in paras)
    print(
        f"words={len(words)} paragraphs={len(paras)} "
        f"median_words={sizes[len(sizes) // 2]} max_words={sizes[-1]} min_words={sizes[0]}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
