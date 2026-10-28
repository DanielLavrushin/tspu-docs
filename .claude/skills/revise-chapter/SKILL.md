---
name: revise-chapter
description: Procedure for revising tspu-docs chapters. Checks them against the lecture transcript and slides, fixes and enriches them, adds slide images, then verifies with three subagents and the validator. Use when the user asks to revise specific chapters, for example /revise-chapter echelon.
---

Revision of tspu-docs: review and update the chapters named in the arguments. Arguments are slugs: `echelon` means docs/echelon.md, and several slugs are revised together. If no slug was given, ask which chapter.

Before starting, check that transcript/chapter-map.md and transcript/validate.py exist. If either is missing, the setup session has not run yet: stop and say so.

Sources. All are local; none of them may be mentioned in the chapters.

- Slides, transcript/slides/: the authority for exact names, CLI syntax, defaults, numbers and diagrams. Look at the contact sheets in transcript/slides/sheets/ first, then open only the PNGs you need. Slides shown for 1-2 seconds were flipped past: real content, but never explained.
- Transcript, transcript/transcript.md: YouTube speech recognition, with errors. Repair garbled terms when you are confident.
- Your own knowledge, where the material is wrong or obsolete. State it neutrally, and check current facts on the web when you can.

The vendor documents in tspu-equipment/ are in the repo only as references. They are outdated and can contradict the lecture, so don't add content from them and don't change a chapter to match them. Earlier passes wrote some vendor-based statements into the chapters (phrased like «по документации производителя…» or «в более поздних версиях ПО…»). Check each one in your chapter: keep a fact only where the slides or transcript support it, and then drop the vendor attribution; remove statements that are vendor-only or that contradict the video, and list them in your report.

transcript/chapter-map.md lists each chapter's transcript ranges and slides. Queued fixes are in memory (tspu-docs-followups); many of them cite vendor docs, so apply one only when the slides or transcript support it.

Steps

1. Read the chapter, its transcript ranges and its slides.
2. Fix wrong facts, add missing ones, remove invented claims. Keep the chapter's structure and the approved writing rules (one home per fact, headings name topics, neutral version notes). Small edits to other chapters are fine; list them.
3. Images: at most 3 per chapter, only where a picture explains more than text (topologies, packet paths, hardware).
   - Crop the slide to its content: no slide-number badge, no black side bars. Use ffmpeg (`-vf crop=w:h:x:y`) or Pillow through `uv run --no-project --with pillow python -I`. Open the result to check the crop.
   - Save as docs/images/<slug>/<descriptive-name>.png (JPEG for photos), under about 300 KB.
   - Embed like the existing images: <img width="1024" alt="..." src="images/<slug>/<name>.png" />, with a real Russian alt text and a caption in the style the chapters already use. When the image is narrower than 1024 px, give its real width so it is not upscaled.
   - CLI output and config go in code blocks, not pictures. Every fact shown in an image is also in the text.
   - Give the existing alt="image" images real alt texts. Propose replacements for them, don't make them.
4. Verify with three independent subagents: (a) fidelity to the transcript; (b) technical accuracy against the slides (names, syntax, defaults, numbers); (c) completeness and consistency with other chapters. Give each one the file paths, transcript ranges and slide numbers, not your conclusions. Apply what you can confirm; list what you can't.
5. Run transcript/validate.py. Realign only this chapter's tables.
6. Report the changes, open questions and new images. Give a git add command with exact paths (docs/, README.md, chapters/ as touched; never -A, transcript/ or .claude/). Don't commit. Update memory: mark the chapter done in the current revision's status note, remove the follow-ups you fixed from tspu-docs-followups, and add new ones there.

Rules: chapters, image file names, alt texts and captions never mention the lecture, lecturer, slides, timestamps or recording, and chapters never mirror the lecture's structure. Keep the Russian typography of the existing chapters (« » quotes, em dashes); the dash ban in /home/dala/CLAUDE.md is for the design kit and does not apply here.
