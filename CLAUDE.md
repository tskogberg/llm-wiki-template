# LLM Wiki — schema

A knowledge wiki (Karpathy's LLM Wiki pattern), viewed in Obsidian, stored in git.
The user adds sources and reads; Claude writes and maintains the wiki. Follow these rules every time.

## Layout
- `raw/` — source material (articles, transcripts, notes, PDFs as markdown); images in `raw/assets/`. **Immutable: read, never edit, move, or rename.**
- `notes/` — the user's own thoughts. Read and link to them; **never edit.**
- `wiki/sources/` — one summary page per raw file.
- `wiki/concepts/` — ideas, techniques, theories, terms; built up across sources.
- `wiki/entities/` — concrete things: people, organizations, products, systems, places, projects.
- `wiki/syntheses/` — saved answers, comparisons, and analyses that span pages.
- `wiki/index.md` — catalog of every wiki page, one line each, grouped by type.
- `wiki/log.md` — append-only history, one dated entry per ingest or significant change.
- `views/` — Obsidian Bases (`.base`) views over wiki frontmatter; `setup/` — tool config (Web Clipper template, `/wiki-note` skill). Not wiki pages.

## Domains
Domains are **tags, not folders**: `domain/<name>` (e.g. `domain/nutrition`). A page may carry several.
Unrelated domains live side by side; cross-domain links are welcome.

## Page template
```markdown
---
type: source | concept | entity | synthesis
tags: [domain/<name>, <other-tags>]
sources: ["[[source-page]]", ...]   # source pages this page draws on
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
# Title

> One- to three-sentence summary of what this page is and why it matters.

## What sources say
- Claim. ([[source-page]])

## Synthesis
My (Claude's) interpretation, connections, and open questions.

## Related
- [[other-page]]
```
Source pages also carry `raw: raw/<file>` in frontmatter, plus `author`, `date`, and `url` when known; their `sources` field is empty.
Use "Key points" instead of "What sources say" on source pages.

## Naming
- File names are kebab-case: `spaced-repetition.md`, `andrej-karpathy.md`. The page title is the readable form.
- Source pages are named after the work, not the raw file name: `sources/attention-is-all-you-need.md`.
- One concept per page. **Before creating a page, search for an existing one** (including synonyms
  and plural/singular forms). Prefer updating it over making a near-duplicate; add aliases to its
  frontmatter (`aliases: [...]`) so Obsidian resolves alternate names.

## Linking
- Use `[[wikilinks]]` generously, by file name without extension: `[[spaced-repetition]]`; add display text with `[[file|Text]]`.
- Links go both ways: when page A starts relying on B, make sure B links back to A, under Related or inline.
  Pages in the same series (below) are already connected by Previous/Next and the Timeline.
- Every factual claim traces to a source page; link the source inline next to the claim.
- Link to `notes/` as `[[note-name]]` when the user's own thinking is relevant; treat notes as the user's views, not as sources.

## Sources vs. synthesis
- Keep "What sources say" (attributed claims) separate from "Synthesis" (your reasoning). Never present inference as a sourced fact.
- **Flag contradictions explicitly; never silently pick a side:**
  ```markdown
  > [!warning] Contradiction
  > [[source-a]] says X; [[source-b]] says Y. Possible reasons: ... Unresolved.
  ```
- When a newer source supersedes an older claim, keep both, mark the old one `(superseded by [[source-b]])`.

## Series (projects with many sources)
- A project with its own entity page (e.g. `website-redesign`) gets a series once it has about three sources.
  Each of its source pages has, right under the summary: `**Series:** [[project|Title]] · Previous: [[a]] · Next: [[b]]`,
  ordered by date, then ingest order. Adding a source also sets `Next:` on the previous one.
- The project page has a `## Timeline` after "What sources say": `- YYYY-MM-DD — [[source]] — what happened`.
  "What sources say" then describes the project as it is now: update claims in place and mark replaced ones superseded,
  instead of adding a block per session. Related lists don't repeat sources that are in the Timeline.

## Bookkeeping (every time pages change)
1. Set `updated:` on each touched page.
2. Update `wiki/index.md`: add/rename/remove lines; keep each section sorted alphabetically.
   Format: `- [[page-name]] — one-line description #domain/<name>`
3. Append to `wiki/log.md` (newest at the bottom, never rewrite past entries):
   `## YYYY-MM-DD — <ingest|update|lint|query|refactor> — <subject>` plus bullets of pages created/updated.

## Hard rules
- Never edit anything in `raw/` or `notes/`.
- Never commit; the Obsidian Git plugin auto-commits a few minutes after changes. The user reviews changes in the git history.
- Don't delete or merge wiki pages without asking.
- Skills: `/ingest <raw file>`, `/lint`, `/query <question>` (see `.claude/skills/`), and `/wiki-note` from other projects (see `setup/wiki-note/`).
