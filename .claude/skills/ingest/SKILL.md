---
name: ingest
description: Ingest a source file from raw/ into the wiki — write its source summary, create or update every concept and entity page it touches, cross-link both ways, and update index.md and log.md. Use when the user says "ingest", adds a file to raw/, or asks to process a source.
argument-hint: <path in raw/>
---

# Ingest a source

Follow CLAUDE.md for every convention. Input: a file in `raw/` (if none given, list files in `raw/` not yet referenced by any `raw:` frontmatter in `wiki/sources/` and ask which).

## Steps
1. **Read** the raw file in full (and any images in `raw/assets/` it references). Never modify it.
2. **Orient**: read `wiki/index.md`. Identify the domain tag(s); reuse existing `domain/*` tags where they fit.
3. **Source page** `wiki/sources/<work-name>.md`: frontmatter (`type: source`, `raw:`, author/date/url if known),
   summary, "Key points" (faithful to the source, no editorializing), notable quotes if useful,
   "Synthesis" (your take: how it relates to existing pages, strengths, doubts), and links to every concept/entity below.
   If a source page already exists for this file, update it instead.
   For to-do lists and planning documents, keep the facts, options and decisions (made and still open);
   leave open tasks in the raw file.
   **Series**: if the source is about a project whose entity page has a `## Timeline` (or the raw note says
   "follow-up to …"), follow the Series rules in CLAUDE.md: add the `**Series:**` line with `Previous:` = the last Timeline
   entry, add `Next:` to that page's Series line, append a Timeline line on the project page, and update the project's
   "What sources say" in place. If a project without a series reaches about three sources, start one (create the
   project's entity page if it has none) and backfill the earlier sources.
4. **Concepts and entities**: list every significant concept and entity in the source. For each:
   - Search for an existing page (grep file names, titles, `aliases`, synonyms). Update it if found.
   - Otherwise create one from the template, only if it's substantive enough to stand alone; minor mentions just get a link
     from the source page if a page exists.
   - Add the new claims under "What sources say" with an inline `([[source-page]])` citation, and add the source to `sources:`.
   - If a claim conflicts with what the page already says, add a `> [!warning] Contradiction` callout. Don't overwrite.
5. **Backlinks**: make sure every page you linked to links back where relevant (source ↔ concept ↔ entity, concept ↔ related concept).
   Pages in the same series don't need extra backlinks. Run `python3 .claude/skills/lint/lint.py` and fix anything
   under sections 1, 2, 2b and 3 that your changes caused.
   Check `notes/` for related user notes and link to them from wiki pages (never edit notes).
6. **Bookkeeping**: set `updated:` dates, update `wiki/index.md`, append a `wiki/log.md` entry listing pages created and updated.
7. **Don't commit**: the Obsidian Git plugin commits and pushes a few minutes after changes stop. Report to the user:
   - Source page created
   - Pages created (with one-line reason each) and pages updated (what changed)
   - Contradictions or open questions found
   - Suggested follow-ups (e.g. concepts that deserve a page later)
   Keep it short; the user reviews the changes in Obsidian or the git history.
