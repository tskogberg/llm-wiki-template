---
name: query
description: Answer a question from the wiki — start at index.md, read the relevant pages, answer with [[link]] citations, then offer to save the answer as a synthesis page. Use when the user asks a question about something they've learned or says "query".
argument-hint: <question>
---

# Query the wiki

1. **Start at `wiki/index.md`** to find candidate pages; then grep `wiki/` (and `notes/`) for key terms and aliases the index might miss.
2. **Read the relevant pages** and follow links one hop where useful. Go to `raw/` only to verify a specific claim or when wiki pages are too thin.
3. **Answer** concisely and cite pages inline with `[[links]]`. Keep it clear what comes from the sources and what you inferred.
   Point out contradictions between pages. If the wiki doesn't cover the question, say so plainly. Don't fill gaps
   with outside knowledge unless you label it as such ("not in the wiki:").
4. **Offer to save**, if the answer is worth keeping (non-trivial synthesis, a comparison, something likely to be asked again):
   suggest a file name like `wiki/syntheses/<kebab-name>.md`. If the user says yes, write it from the template
   (`type: synthesis`), add backlinks from the cited pages, update index.md, and append a `query` entry to log.md. Don't commit.
   Also mention gaps you noticed (missing pages, sources worth adding).
