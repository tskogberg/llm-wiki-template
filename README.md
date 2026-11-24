# LLM Wiki template

A starting point for a knowledge wiki in the [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
you collect sources, [Claude Code](https://claude.com/claude-code) writes and maintains the wiki, and you read it in [Obsidian](https://obsidian.md).
Everything is versioned in git, and the Obsidian Git plugin commits and pushes for you.

## Layout
| Folder | Who writes it | What it holds |
|---|---|---|
| `raw/` | you, or Claude sessions in your projects | Source material: articles, transcripts, PDFs converted to markdown, session notes. Never edited after adding. |
| `notes/` | you | Your own thoughts. Claude may link to them but never edits them. |
| `wiki/` | Claude | Source summaries, concept, entity, and synthesis pages, plus `index.md` and `log.md`. |
| `CLAUDE.md` | both | The schema and rules Claude follows. |
| `.claude/skills/` | both | The `ingest`, `lint` and `query` skills; `lint/lint.py` runs the mechanical checks. |
| `views/`, `setup/` | both | Obsidian Bases views; the Web Clipper template and the `/wiki-note` skill. |

Domains are tags (`#domain/<name>`), not folders, so unrelated subjects can live side by side.

## What you need
- [Claude Code](https://claude.com/claude-code)
- [Obsidian](https://obsidian.md) with the community plugin **Git** (by Vinzent)
- git, and a remote repository for your wiki (optional, but it's your backup)
- Optional: [Obsidian Web Clipper](https://obsidian.md/clipper) for saving web pages

**Before using it for work material**, check that your employer allows that material to go through Claude, and under which account.
Every ingest and query sends the relevant documents to the model.

## Set up a new wiki
1. **Clone the template** and point it at your own repository. Keeping the template as a second remote lets you pull improvements later.
   ```sh
   git clone https://github.com/tskogberg/llm-wiki-template.git ~/Projects/my-wiki
   cd ~/Projects/my-wiki
   git remote rename origin template
   git remote add origin <your-wiki-repo-url>
   git push -u origin main
   ```
   If git doesn't know your name yet: `git config user.name "Your Name"` and `git config user.email "you@example.com"`.
2. **Open it in Obsidian**: *Open folder as vault*, then *Settings → Community plugins → Turn on community plugins → Browse*,
   search for **Git** (by Vinzent), *Install* and *Enable*. Its settings are already in the repo: commit and push 5 minutes after changes stop,
   pull when Obsidian starts. Installing the plugin deletes that settings file, so restore it and then reload Obsidian:
   ```sh
   git checkout -- .obsidian/plugins/obsidian-git/data.json
   ```
3. **Install `/wiki-note`** so any Claude Code session can add its work to this wiki:
   ```sh
   ln -s "$PWD/setup/wiki-note" ~/.claude/skills/wiki-note
   ```
   The skill finds the wiki through this link, so only one wiki per computer can own `/wiki-note`.
4. **Optional, Web Clipper**: in its settings, set the vault to this folder's name, import `setup/web-clipper-template.json`,
   and move "Wiki source" to the top of the template list.
5. **Start**: put a file in `raw/` and run `/ingest raw/<file>.md` in Claude Code in this folder. The first ingest creates the first domain tag.

## Day to day
1. **Add a source.**
   - From a project: type `/wiki-note` in the Claude Code session working there (optionally with what to focus on). It writes a note into `raw/` and ingests it under the current rules.
   - From the web: clip it with Obsidian Web Clipper (the "Wiki source" template saves to `raw/`).
   - Other material: save it as markdown in `raw/`, for example a PDF converted to markdown. Pasted images go to `raw/assets/` automatically.
2. **Ingest it.** In Claude Code in this folder, run `/ingest raw/<file>.md`. Claude writes the summary, updates related pages, and reports what changed.
3. **Review.** The Obsidian Git plugin commits and pushes 5 minutes after changes stop. Browse the changed pages in Obsidian, or check the latest commits with `git log -p`.
4. **Ask questions.** Run `/query <question>`. Answers cite wiki pages. Save good answers to `wiki/syntheses/`.
5. **Maintain.** Run `/lint` now and then (say, after every 5–10 ingests) to find contradictions, orphans, broken links, and gaps.
   For a quick mechanical check without Claude, run `python3 .claude/skills/lint/lint.py`.
   Names that keep coming up can go in `.claude/skills/lint/terms.txt`, and lint will suggest pages for them.
6. **Think.** Write freely in `notes/`. Claude can link to your notes from the wiki.

After changing `CLAUDE.md` or a skill, tell any Claude sessions that are already running, since they may still be using the old rules.

## Projects, series and timelines
A project with several sources has an entity page that describes it as it is now, with a **Timeline** listing every source in order.
Each of those source pages starts with a **Series** line linking to the project and to the previous and next source, so you can read a project's history step by step.
A project gets a series once it has about three sources.

## Getting template updates
Improvements to the rules and skills are made in the template. To bring them into your wiki:
```sh
git fetch template
git merge template/main
```
Your content lives in `raw/`, `wiki/` and `notes/`, which the template leaves empty, so merges only touch the rules, skills and settings.
Pause Obsidian Git's auto-commit while merging, or run the merge when Obsidian is closed.

## Obsidian tips
- Start from `wiki/index.md`; use graph view to see how pages connect.
- `wiki/log.md` shows what changed recently.
- `views/wiki.base` has table views: all pages by type, recently updated, stale (6+ months), and sources.

## License
The template is released under the [MIT License](LICENSE). It covers the template's own files; what you put in your wiki is yours.
The Obsidian Git plugin isn't included here; you install it from Obsidian's Community plugins under its own license.
