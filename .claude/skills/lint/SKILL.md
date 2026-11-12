---
name: lint
description: Health-check the wiki — report contradictions, orphan pages, broken links, near-duplicates, stale claims, missing pages for frequently mentioned concepts, and index/log drift. Proposes fixes but applies nothing without asking. Use when the user says "lint" or asks to check or clean up the wiki.
argument-hint: "[optional domain tag or folder to limit scope]"
---

# Lint the wiki

Read-only until the user approves fixes. Follow CLAUDE.md conventions when proposing them.

## Script
Run `python3 .claude/skills/lint/lint.py` from the wiki root first. It prints numbered sections matching the checks below and covers the mechanical ones: 1 (broken links), 2 (orphans, one-way links; links within a series count as two-way), 2b (series Previous/Next and Timeline consistency, and project-named sources missing a Series line), 3 (index drift), 4 (sources frontmatter vs. citations), 8 (terms listed in `terms.txt` that appear on 3+ pages without a page) and 9 (schema). Checks 5, 6 and 7 need reading the pages. Treat the output as leads to confirm, not as fixes to apply blindly.

## Checks
1. **Broken links**: `[[targets]]` in `wiki/` that resolve to no file in `wiki/`, `notes/`, or `raw/` (match by file name without extension, also against `aliases`).
2. **Orphans**: wiki pages with no inbound links from other wiki pages (index.md doesn't count). Also flag one-way links that should be reciprocal.
3. **Index drift**: pages missing from `wiki/index.md`, index lines pointing to missing pages, wrong section, unsorted sections.
4. **Unsourced claims**: bullets under "What sources say" with no `[[source]]` citation; `sources:` frontmatter not matching cited sources.
5. **Contradictions**: open `[!warning] Contradiction` callouts, plus conflicting claims across pages that aren't flagged yet.
6. **Near-duplicates**: pages that cover the same thing (similar names, overlapping aliases, mostly the same content). Propose merges.
7. **Stale claims**: claims superseded by a newer source but not marked; pages whose `updated:` is older than a newer source that cites them; time-sensitive statements ("currently", "latest", prices, versions).
8. **Missing pages**: concepts/entities mentioned (plain text or broken link) on 3+ pages with no page of their own.
9. **Schema**: missing or invalid frontmatter fields, non-kebab-case file names, pages without a `domain/*` tag, raw files with no source page.

## Output
A report grouped by check, most important first. Each item: the page(s), the problem, and the proposed fix.
Skip checks that found nothing with a single "✓" line. End by asking which fixes to apply (e.g. "all", "1, 3, 5", "none").
After applying approved fixes, update index.md and append a `lint` entry to log.md. Don't commit.
