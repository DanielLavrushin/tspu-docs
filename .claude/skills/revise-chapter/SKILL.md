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
- Research findings, transcript/research/findings-*.md (one file per /tspu-research run; a later run updates an earlier one) with the source register sources.md: what newer public sources say about the chapter's claims, with dates and confidence. The chapter map lists the items picked for each chapter under «Research». The facts may go into a chapter; the findings files, run dates and source ids may not.

The vendor documents in tspu-equipment/ are in the repo only as references. They are outdated and can contradict the lecture, so don't add content from them and don't change a chapter to match them. Earlier passes wrote some vendor-based statements into the chapters (phrased like «по документации производителя…» or «в более поздних версиях ПО…»). Check each one in your chapter: keep a fact only where the slides or transcript support it, and then drop the vendor attribution; remove statements that are vendor-only or that contradict the video, and list them in your report.

transcript/chapter-map.md lists each chapter's transcript ranges and slides. Queued fixes are in memory (tspu-docs-followups); many of them cite vendor docs, so apply one only when the slides or transcript support it.

Steps

1. Read the chapter, its transcript ranges and its slides, its «Research» items in the chapter map, and the chapter's sections in every findings file.
2. Fix wrong facts, add missing ones, remove invented claims. Keep the chapter's structure and the approved writing rules (one home per fact, headings name topics, neutral version notes).
   - Research items: apply the high-confidence ones only. The design described in the chapter stays as written; add what changed later as a dated note. A dated note is a plain paragraph after the text it qualifies that names its source type and the date the fact applies to, either up front («По официальным данным (конец 2023 года), …», «По данным ФГУП «ГРЧЦ» (июнь 2024 года), …», «По данным измерений (2022), …») or inside the fact («…приказом от 29.12.2021 № 343»). Past tense or explicitly dated; never «сейчас» or «на текущем этапе»; no URLs. Differences between software versions keep their own form («В более поздних версиях ПО…»). Medium- and low-confidence items, and material that needs a new section, go in the report; the post-2021 chapter in the map's proposals table is where most of it will live.
   - When a fix also applies to other chapters, make it there too. Search docs/ and README.md for every place the wrong fact, name or number appears and fix them all. Add or remove material in another chapter when you know it belongs there: a fact lives in its home chapter, and other chapters link to it instead of repeating it.
   - Verify each change in another chapter against the slides or transcript, as for your own chapter, and record it under that chapter in transcript/chapter-map.md so its own session knows. List every cross-chapter change in your report.
3. Images: at most 3 per chapter, counting the ones already there, only where a picture explains more than text (topologies, packet paths, hardware). transcript/chapter-map.md lists the images each chapter already has; add yours there.
   - Crop the slide to its content: no slide-number badge, no black side bars, no mouse pointer (crop it out or patch it). Use photocraft (`image.crop`, then export); if it is not in the session, ffmpeg (`-vf crop=w:h:x:y`) or Pillow through `uv run --no-project --with pillow python -I`. Open the result to check the crop.
   - Fix a misprint on a slide only when the correct value is certain, and name the fix in your report.
   - Save as docs/imgs/<slug>/<descriptive-name>.png (JPEG for photos), under about 300 KB.
   - Embed like the existing images: <img width="1024" alt="..." src="imgs/<slug>/<name>.png" />, with a real Russian alt text and a caption in the style the chapters already use. When the image is narrower than 1024 px, give its real width so it is not upscaled.
   - An ASCII diagram of the same subject goes when the image replaces it, provided every fact it held is still in the prose.
   - CLI output and config go in code blocks, not pictures. Every fact shown in an image is also in the text.
   - Give the existing alt="image" images real alt texts. Propose replacements for them, don't make them.
4. Verify with three independent subagents: (a) fidelity to the transcript; (b) technical accuracy against the slides (names, syntax, defaults, numbers); (c) completeness and consistency with other chapters, including every other chapter you changed. Give each one the file paths, transcript ranges and slide numbers, not your conclusions. Dated notes and other facts taken from the research findings are checked against the cited findings sections, not against the transcript or slides; give the verifiers those sections too. Apply what you can confirm; list what you can't.
5. Run transcript/validate.py. Realign this chapter's tables and any table you changed elsewhere, nothing more.
6. Report the changes, open questions and new images. Give a git add command with exact paths (docs/, README.md, chapters/ as touched; never -A, transcript/ or .claude/). Don't commit. Update memory: mark the chapter done in the current revision's status note, remove the follow-ups you fixed from tspu-docs-followups, and add new ones there.

Rules: chapters, image file names, alt texts and captions never mention the lecture, lecturer, slides, timestamps or recording, and chapters never mirror the lecture's structure. Keep the Russian typography of the existing chapters (« » quotes, em dashes).
