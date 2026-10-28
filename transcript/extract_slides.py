"""Extract one image per slide from the lecture video.

Usage:
    uv run --no-project --with numpy --with pillow python -I transcript/extract_slides.py \
        VIDEO.mp4 transcript/slides

VIDEO.mp4 is the 720p video-only stream: the yt-dlp command in build.py with
`-f 136` instead of the subtitle flags. It is ~250 MB and is not kept in the repo.

ffmpeg decodes one small grayscale frame per second. A slide is a run of at least
MIN_STABLE_S seconds in which consecutive frames barely change. The last second of
each run is saved at full resolution: the encoder sharpens a still picture over
time, and incremental builds are complete by then. A run that looks the same as a
slide already saved is recorded as a reappearance instead of a new file. Shorter
runs, mostly slides flipped past in a second or two, are kept only when they show
something no longer run does; the index lists seconds on screen so they stand out.

Writes NNN_H-MM-SS.png per slide (time of first appearance), sheets/sheet_NN.jpg
(numbered thumbnails for browsing many slides at once) and index.md.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

VIDEO_ID = "raNP3IMgwRU"
SMALL_W, SMALL_H = 160, 88
STABLE_DIFF = 1.0   # mean abs change between consecutive seconds that still counts as still
MIN_STABLE_S = 3    # shortest still run that counts as a slide
BLOCK = 8           # side of the square blocks compared by slide_distance
SAME_SLIDE = 10.0   # slide_distance below which two runs show the same slide
BLANK_STD = 3.0     # frames this uniform (black or empty) are not slides
SHEET_COLS, SHEET_ROWS, THUMB_W = 5, 6, 320
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def hms(s, sep=":"):
    s = int(s)
    return f"{s // 3600}{sep}{s % 3600 // 60:02d}{sep}{s % 60:02d}"


def read_small(video, cache):
    if cache and Path(cache).exists():
        raw = Path(cache).read_bytes()
    else:
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-threads", "0", "-i", video, "-an",
             "-vf", f"fps=1,scale={SMALL_W}:{SMALL_H}:flags=area,format=gray",
             "-f", "rawvideo", "-"],
            check=True, capture_output=True,
        ).stdout
        if cache:
            Path(cache).write_bytes(raw)
    return np.frombuffer(raw, np.uint8).reshape(-1, SMALL_H, SMALL_W).astype(np.int16)


def still_runs(frames):
    diffs = np.abs(frames[1:] - frames[:-1]).mean(axis=(1, 2))
    runs, start = [], 0
    for t, d in enumerate(diffs, start=1):
        if d >= STABLE_DIFF:
            runs.append((start, t - 1))
            start = t
    runs.append((start, len(frames) - 1))
    return [(a, b) for a, b in runs if frames[b].std() >= BLANK_STD]


def slide_distance(x, y):
    # Largest per-block mean difference: a whole-frame mean lets two mostly white
    # slides with different titles look alike.
    h, w = SMALL_H // BLOCK * BLOCK, SMALL_W // BLOCK * BLOCK
    d = np.abs(x - y)[:h, :w].reshape(h // BLOCK, BLOCK, w // BLOCK, BLOCK)
    return d.mean(axis=(1, 3)).max()


def closest(rep, slides):
    dists = [slide_distance(rep, s["small"]) for s in slides]
    best = int(np.argmin(dists)) if dists else -1
    return best if best >= 0 and dists[best] < SAME_SLIDE else -1


def group_slides(frames, runs):
    slides = []  # dicts: first, last, shot (second to export), small, seconds, again
    long_runs = [(a, b) for a, b in runs if b - a + 1 >= MIN_STABLE_S]
    for a, b in long_runs:
        rep = frames[b]
        best = closest(rep, slides)
        if best < 0:
            slides.append({"first": a, "last": b, "shot": b, "small": rep, "seconds": 0, "again": []})
            best = len(slides) - 1
        elif best == len(slides) - 1:
            slides[best].update(last=b, shot=b, small=rep)
        else:
            slides[best]["again"].append(a)
        slides[best]["seconds"] += b - a + 1
    for a, b in runs:
        if b - a + 1 < MIN_STABLE_S and closest(frames[b], slides) < 0:
            slides.append({"first": a, "last": b, "shot": b, "small": frames[b],
                           "seconds": b - a + 1, "again": []})
    return sorted(slides, key=lambda s: s["first"])


def export(video, slides, out):
    for n, s in enumerate(slides, start=1):
        s["file"] = f"{n:03d}_{hms(s['first'], '-')}.png"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-ss", str(max(s["first"], s["shot"] - 0.5)),
             "-i", video, "-frames:v", "1", str(out / s["file"])],
            check=True,
        )


def contact_sheets(slides, out):
    sheets = out / "sheets"
    sheets.mkdir(exist_ok=True)
    font = ImageFont.truetype(FONT, 16) if Path(FONT).exists() else ImageFont.load_default()
    per = SHEET_COLS * SHEET_ROWS
    names = []
    for i in range(0, len(slides), per):
        page = slides[i:i + per]
        thumbs = []
        for s in page:
            im = Image.open(out / s["file"]).convert("RGB")
            thumbs.append(im.resize((THUMB_W, round(im.height * THUMB_W / im.width))))
        th = thumbs[0].height
        cell_h = th + 26
        rows = -(-len(page) // SHEET_COLS)
        sheet = Image.new("RGB", (SHEET_COLS * (THUMB_W + 6) + 6, rows * cell_h + 6), "white")
        draw = ImageDraw.Draw(sheet)
        for k, (s, im) in enumerate(zip(page, thumbs)):
            x, y = 6 + k % SHEET_COLS * (THUMB_W + 6), 6 + k // SHEET_COLS * cell_h
            sheet.paste(im, (x, y))
            draw.rectangle((x - 1, y - 1, x + THUMB_W, y + th), outline="#888888")
            draw.text((x, y + th + 3), f"{s['file'][:3]}  {hms(s['first'])}", fill="black", font=font)
        name = f"sheet_{i // per + 1:02d}.jpg"
        sheet.save(sheets / name, quality=88)
        names.append((name, page[0]["file"][:3], page[-1]["file"][:3]))
    return names


def write_index(slides, sheet_names, out):
    lines = [
        "# Слайды",
        "",
        f"Кадры из видео https://www.youtube.com/watch?v={VIDEO_ID} (720p), по одному на слайд;",
        "собраны скриптом `../extract_slides.py`. Время в имени файла и в таблице: первый показ",
        "слайда, оно совпадает с метками абзацев в `../transcript.md`. Слайды, которые лектор",
        "пролистал за 1–2 секунды, тоже сохранены: у них мало секунд на экране.",
        "",
        "Листы с миниатюрами для быстрого просмотра:",
        "",
    ]
    lines += [f"- [{name}](sheets/{name}): слайды {lo}–{hi}" for name, lo, hi in sheet_names]
    lines += ["", "| # | Время | Файл | Секунд на экране | Показан снова |", "|---|---|---|---|---|"]
    for s in slides:
        t = s["first"]
        again = ", ".join(f"[{hms(x)}](https://youtu.be/{VIDEO_ID}?t={x})" for x in s["again"])
        lines.append(
            f"| {s['file'][:3]} | [{hms(t)}](https://youtu.be/{VIDEO_ID}?t={t}) "
            f"| [{s['file']}]({s['file']}) | {s['seconds']} | {again} |"
        )
    (out / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("out")
    p.add_argument("--small", help="raw 1 fps gray frames: read if present, else written after decoding")
    p.add_argument("--dry-run", action="store_true", help="print the detection result only")
    args = p.parse_args()

    frames = read_small(args.video, args.small)
    runs = still_runs(frames)
    slides = group_slides(frames, runs)
    print(
        f"seconds={len(frames)} still_runs={len(runs)} slides={len(slides)} "
        f"brief={sum(s['seconds'] < MIN_STABLE_S for s in slides)} "
        f"reappearances={sum(len(s['again']) for s in slides)}",
        file=sys.stderr,
    )
    if args.dry_run:
        for n, s in enumerate(slides, start=1):
            print(f"{n:03d} {hms(s['first'])} {s['seconds']:>5}s again={[hms(x) for x in s['again']]}")
        return

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in list(out.glob("[0-9][0-9][0-9]_*.png")) + list(out.glob("sheets/sheet_*.jpg")):
        old.unlink()
    export(args.video, slides, out)
    write_index(slides, contact_sheets(slides, out), out)


if __name__ == "__main__":
    main()
