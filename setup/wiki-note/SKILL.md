---
name: wiki-note
description: Write a note about this session's work into the user's LLM wiki (its raw/ folder) and ingest it, following the wiki's own rules. Use when the user types /wiki-note or asks to add this work to the wiki, write a wiki note, or update the wiki from this session.
argument-hint: "[optional: what the note should focus on]"
---

# Write a wiki note and ingest it

## 0. Find the wiki
This skill is installed as a link, `~/.claude/skills/wiki-note` → `<wiki>/setup/wiki-note`, so the wiki is two folders up
from the link's real target:
```sh
WIKI="$(cd "$(dirname "$(realpath ~/.claude/skills/wiki-note/SKILL.md)")/../.." && pwd)"
```
Check that `$WIKI/CLAUDE.md` exists; if not, stop and tell the user the link is broken.
Use absolute paths under `$WIKI` throughout; this session's working directory is usually another project.

The wiki's own files hold the rules, and they change, so **read them fresh every time**:
`$WIKI/CLAUDE.md` and `$WIKI/.claude/skills/ingest/SKILL.md`. If they disagree with this file, they win.

## 1. Decide what the note covers
- The work done in this session since the last wiki note from this session (look back in the conversation for an earlier `/wiki-note`),
  narrowed to the argument if one was given.
- If nothing worth recording happened (no decision, finding, change or result), say so and stop. Don't write empty notes.
- One note per call. If the session covered unrelated topics, ask whether to write one note or several.

## 2. Find the project and the previous note
- Read `$WIKI/wiki/index.md`. If the work belongs to a project with a series (an entity page with a `## Timeline`),
  the previous note is that Timeline's last entry. Otherwise look in `$WIKI/raw/` for the latest note on the same topic.
- Name the file `raw/<project-or-topic>-<short-topic>-YYYY-MM-DD.md` in kebab-case, starting with the project's page name
  when there is one (e.g. `website-redesign-checkout-flow-2026-11-12.md`), so lint can spot a missing Series line.
- `raw/` is immutable: never overwrite or edit an existing file. If the name is taken, choose another.

## 3. Write the note
Get the user's name with `git -C "$WIKI" config user.name`.
```markdown
# <Project> – <what this note is about> (D Mon YYYY)

Note written by Claude (Claude Code) at <user name>'s request, follow-up to `<previous-note-file-name-without-.md>`.
<For code: repo, commit(s), whether pushed and deployed.>

## What was asked
- <the request, briefly; quote the user's words when short>

## What was done
- <changes, findings and decisions, with the reason for each decision>

## Verified
- <what was checked and how; say plainly what wasn't tested>

## Open
- <unresolved questions or known gaps, if any>
```
- Leave out the "follow-up to" part when there's no previous note, and skip sections with nothing in them.
- Facts, options and decisions only, written so someone outside the session understands them. No step-by-step logs.
- Keep it short: usually 10–30 lines.
- **Never include secrets**: passwords, tokens, API keys, private keys, recovery codes. Say where a secret lives instead.

## 4. Ingest it
Follow `$WIKI/.claude/skills/ingest/SKILL.md` for the new file, including the Series rules in CLAUDE.md.
Other sessions may be editing the wiki at the same time: re-read `wiki/index.md`, `wiki/log.md` and each page just before
changing it, and make small edits rather than rewriting whole files.
Then run `cd "$WIKI" && python3 .claude/skills/lint/lint.py` and fix anything in sections 1, 2, 2b and 3 caused by your changes.

## 5. Report
Don't commit: the wiki's Obsidian Git plugin commits and pushes a few minutes after changes stop.
Tell the user, briefly: the note's file name, the source page, pages created and updated, and anything lint flagged that you left alone.
