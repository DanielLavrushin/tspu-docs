---
name: tspu-research
description: Search the open web for newer public sources about ТСПУ, keep a dated source register and write per-chapter findings, without editing chapters. Optional arguments: chapter slugs or a topic to focus on. Use when the user asks to look for updated or newer sources.
---

The chapters in docs/ are built mainly from an older lecture (its content dates from around 2020), so parts of them age. Find publicly available, more recent sources about ТСПУ and record what they say. Don't edit chapters, the README or anything in docs/, and don't commit. You may use a deep-research skill for the searching, and the ru-route skill for Russian sites that fail from here.

Scope: the arguments, if any, are chapter slugs (`echelon` means docs/echelon.md) or a topic; focus on those. Without arguments, cover all chapters.

Earlier runs: if transcript/research/sources.md exists, read it and the latest findings file first. Look for what is new since the last run, re-check only sources that may have changed, and don't repeat earlier findings.

Steps

1. Skim the chapters in scope and list the claims most likely to have aged: hardware and vendors, capacity and deployment scale, the legal and organisational framework (Роскомнадзор, ЦМУ ССОП), central management (ЦСУ), what is blocked or slowed and how (DPI lists, SNI, QUIC, VPN protocols, throttling), and placement in operator networks.
2. Search the open web in Russian and English, in several rounds, following citations. Look for: laws, government decrees and regulator documents; public procurement records; vendor material newer than what tspu-equipment/ holds; peer-reviewed and measurement research (for example IMC papers, OONI, Censored Planet, net4people); reputable journalism and technical write-ups.
3. Use only publicly published material. If something looks leaked or confidential, note that it exists but don't open or use it. Don't copy documents: record short quotes with links.
4. Update transcript/research/sources.md, the register kept across runs: one row per source with title, author or publisher, date, URL, type (official, research, vendor, journalism, forum), access (direct, Russia only, or unreachable from both routes), a reliability note and the date you last checked it. Add new rows; never delete old ones, mark them when they are gone or superseded.
5. Write transcript/research/findings-YYYY-MM-DD.md with today's date, grouped by chapter: the chapter's current claim, what the newer sources say, the date it applies to, the sources, and your confidence. Mark each finding as confirms, updates or contradicts. Then list topics the chapters don't cover at all.
6. In the current revision's status note in memory, record the run: date, scope and the findings file.
7. Report the most important updates, the open questions, which chapters are most out of date, and whether the Russian route was needed and worked.
