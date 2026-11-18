---
name: tspu-digest
description: Turn a /tspu-research run into a public reader article in docs/updates/YYYY-MM-DD.md (Russian, ordered by topic, real source links), list it in the README and link it to the previous article, then verify and stop for review. Optional argument: the run date (YYYY-MM-DD). Use after a /tspu-research run, or when the user asks to write up or publish a research run.
---

Each research run gets a dated article for readers in docs/updates/. The findings files in transcript/research/ are English working notes keyed to chapter sections. The article is a rewrite in Russian for people reading the docs, not a reformat. An article is frozen once published. The cumulative current picture belongs in the planned chapter on the system's development after 2021 (a row in the proposals table of transcript/chapter-map.md), which this skill does not write.

Don't edit chapters, transcript/research/, or the body of a published article. The only change allowed to an earlier article is the next-article link in its header. Don't commit.

## Which run

- With an argument, use transcript/research/findings-<date>.md.
- Without one, take every findings file that has no docs/updates/<same date>.md yet, oldest first, so the prev/next chain stays in order. If there are none, stop and say so.
- The first article ever (2026-10-28) is the baseline since 2021, and every later one covers only what is new. Keep it that way: a later run's article never restates the baseline.

## Read first

- **The findings file, in full.** Its Summary is the spine of the article.
- **The latest article in docs/updates/,** to know what readers already have and to copy its «Как читать» paragraph and footer.
- **The earlier findings file,** only for the sections the new one says it "moves".
- **transcript/research/sources.md,** for the URL of every id the article will cite.
- **The chapter passages the article compares against.** Chapters change after a run (dated notes, corrections), so quote what a chapter says now, not what the findings file says it said.

## Write docs/updates/<date>.md

Structure, as in the existing articles:

1. **Title:** `# …` naming the period or the main themes.
2. **Line 3, the header:** `_Обзор от D месяца YYYY года · [← Предыдущий обзор: D месяца YYYY](<prev>.md)_`. If the article is written later than the run and mentions later decisions, use `_Источники проверены …, обзор опубликован …_` instead.
3. **Intro:** one paragraph saying what period it covers and how it relates to the previous review. Then the «Как читать» paragraph.
4. **`## Коротко`:** 5–10 numbered items, each with a bold lead. Every item must appear in the body with its source.
5. **Topic sections (`##`), ordered by topic, not by chapter number.** Where a finding moves a chapter's claim, end the section with a «Что это значит.» paragraph that links the chapter section.
6. **Optional `## Как распознать по симптомам`:** include it when the findings have troubleshooting items.
7. **`## Открытые вопросы`:** «Продвинулись» and «Новые» lists, then «Остальные вопросы прошлого обзора остаются открытыми.»
8. **`## Без изменений`:** the chapters with no new sources.
9. **Footer:** `---`, then an italic line: public material only, documents that look leaked were not opened, and (if vendor data is used) vendor data is given as the vendor's claims.

What goes in:

- Findings of medium or high confidence, plus low-confidence ones only when they matter, saying plainly what they rest on.
- Leave out register re-checks, access and route notes, and items with no value to a reader.
- An event that is older but new to the register gets an italic line under its heading: «_Событие <месяц года>, в прошлый обзор не попало._»

Writing rules:

- **Language.** Russian, neutral reference tone, the same register as the chapters.
- **Source links.**
  - Every claim gets a link. The link text is the outlet or document name, and the URL is copied exactly from the URL column of sources.md.
  - For a row read through the Wayback Machine ("read as …"), assemble the archive URL and expect the checker to flag it.
  - Never S-ids, and never links to transcript/ or the findings files.
- **Figures.** Findings list sources per item, not per figure. When the article ties a figure to one outlet, open that page (obscura: browser_navigate, then browser_markdown) and confirm the figure is there, or cite every source the finding lists. Keep a list of what you confirmed for the report.
- **Confidence in words:**
  - официально (закон, постановление, должностное лицо);
  - измерено (рецензируемое исследование);
  - по данным СМИ со ссылкой на анонимные источники;
  - по сообщениям на форуме;
  - в пересказе, оригинал не найден.

  For disputed items, give both readings side by side and say which question stays open.
- **Quotes.** Russian quotes stay verbatim in «». English sources are paraphrased in Russian, never quoted in English.
- **Chapter references.** `[раздел N.M](../slug.md)` and `[глава N](../slug.md)`, with numbers from the README.
- **Forbidden content** (the chapters' rule):
  - no лекция, лектор, слайд, транскрипт or similar;
  - no route or access mechanics;
  - nothing from leaked material.
- **No new facts.** Nothing beyond the findings. Your own knowledge appears only as a clearly framed cross-reference to the chapters.
- **Formatting.**
  - Dates as «18 ноября 2026 года».
  - Numbers with a space for thousands and a comma for decimals: 1 406, 132,3 Тбит/с.
  - Table separators as `| --- |`.

## Link it

- **Previous article.** Append ` · [Следующий обзор: D месяца YYYY →](<date>.md)` to its line-3 header. This is the only edit to it.
- **README.** In «Обзоры открытых источников», add a bullet at the top of the list: `- [Месяц YYYY: two or three main themes](docs/updates/<date>.md)`.

## Verify

1. **Checker.** Run `python3 -I .claude/skills/tspu-digest/check_article.py`.
   - Errors must be 0.
   - Open every URL listed under warnings, then fix it or confirm it is right. The ЦМУ ССОП Wayback link in 2026-10-28.md is a known, confirmed warning.
2. **Validator.** Run `python3 -I transcript/validate.py`. The error count must not change: it does not scan docs/updates/, but it checks README links and the contents list.
3. **Reread.** Go through Коротко against the body, and every «Что это значит» against the chapter text it cites.

## Record and report

- **Proposals row.** In transcript/chapter-map.md, add the article's date to the proposals row of the post-2021 chapter.
- **Memory.** Update the memory note on the research articles with the date and its status (uncommitted).
- **Report:**
  - a «Written for:» line;
  - what the article covers;
  - which figures you re-checked against live pages;
  - the attributions you are least sure of;
  - what you left out and why;
  - any choices left to the user.

  Don't commit.
