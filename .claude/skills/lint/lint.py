"""Mechanical wiki checks for the lint skill: broken links, orphans and one-way links,
series links, index drift, sources mismatches, schema, and frequent terms without a page.
Usage: python3 .claude/skills/lint/lint.py [wiki root]  (defaults to this repo)
"""
import re, sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
wiki = root / "wiki"
pages = {p.stem: p for p in wiki.rglob("*.md")}
other = {p.stem for d in ("notes", "raw") for p in (root / d).rglob("*.md")}

def split(t):
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    return (m.group(1), m.group(2)) if m else ("", t)

def strip_code(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", t)

link_re = re.compile(r"\[\[([^\]|#\\]+)")
aliases, fm, body, links = {}, {}, {}, {}
for name, p in pages.items():
    f, b = split(p.read_text())
    fm[name], body[name] = f, b
    m = re.search(r"^aliases: \[(.*)\]", f, re.M)
    for a in (m.group(1).split(",") if m else []):
        aliases[a.strip().strip('"').lower()] = name
    links[name] = set(link_re.findall(strip_code(b)))

print("## 1 broken links")
for n, ls in links.items():
    for l in ls:
        if l not in pages and l not in other and l.lower() not in aliases:
            print(f"  {n} -> [[{l}]]")

series_re = re.compile(r"^\*\*Series:\*\* \[\[([^\]|]+)", re.M)
series = {n: m.group(1) for n in pages if (m := series_re.search(body[n]))}

def same_series(a, b):
    return a in series and (series.get(b) == series[a] or b == series[a])

print("## 2 orphans / one-way")
content = [n for n in pages if n not in ("index", "log")]
inbound = {n: set() for n in pages}
for n in content:
    for l in links[n]:
        if l in inbound and l != n:
            inbound[l].add(n)
for n in content:
    if not inbound[n]:
        print(f"  orphan: {n}")
for n in content:
    for l in links[n]:
        if l in pages and l not in ("index", "log") and n not in links[l] and not same_series(n, l):
            print(f"  one-way: {n} -> {l}")

print("## 2b series")
for n, proj in series.items():
    nav = re.search(r"^\*\*Series:\*\*.*", body[n], re.M).group(0)
    for rel, back in (("Previous", "Next"), ("Next", "Previous")):
        m = re.search(rf"{rel}: \[\[([^\]|]+)", nav)
        if m and not re.search(rf"{back}: \[\[{re.escape(n)}\]\]", body.get(m.group(1), "")):
            print(f"  {n}: {rel} [[{m.group(1)}]] doesn't point back")
    tl = re.search(r"## Timeline\n(.*?)(\n## |\Z)", body.get(proj, ""), re.S)
    if not tl or f"[[{n}]]" not in tl.group(1):
        print(f"  {n}: missing from {proj}'s Timeline")
for proj in sorted(set(series.values())):
    for n in content:
        if n.startswith(f"{proj}-") and "type: source" in fm[n] and n not in series:
            print(f"  {n}: looks like part of {proj}'s series but has no Series line")

print("## 3 index drift")
idx = (wiki / "index.md").read_text()
idx_links = set(link_re.findall(strip_code(idx)))
for n in content:
    if n not in idx_links:
        print(f"  missing from index: {n}")
for l in idx_links - set(pages):
    print(f"  index points to missing: {l}")
sec = None; secs = {}
for line in idx.splitlines():
    if line.startswith("## "): sec = line[3:]; secs[sec] = []
    elif sec and line.startswith("- [["): secs[sec].append(link_re.search(line).group(1))
want = {"Sources": "source", "Concepts": "concept", "Entities": "entity", "Syntheses": "synthesis"}
for s, ns in secs.items():
    if ns != sorted(ns): print(f"  unsorted: {s}")
    for n in ns:
        t = re.search(r"^type: (\w+)", fm.get(n, ""), re.M)
        if t and t.group(1) != want.get(s): print(f"  wrong section: {n} in {s}")

print("## 4 unsourced / sources mismatch")
for n in content:
    b = body[n]
    m = re.search(r"## What sources say\n(.*?)(\n## |\Z)", b, re.S)
    if m:
        lines = m.group(1).splitlines()
        for i, line in enumerate(lines):
            if line.startswith("- ") and not link_re.search(line):
                # a heading bullet counts as sourced when its sub-bullets cite
                sub = []
                for nxt in lines[i + 1:]:
                    if not nxt.startswith((" ", "\t")): break
                    sub.append(nxt)
                if not any(link_re.search(s) for s in sub):
                    print(f"  unsourced bullet in {n}: {line[:80]}")
    fs = re.search(r"^sources: \[(.*)\]", fm[n], re.M)
    declared = set(link_re.findall(fs.group(1))) if fs else set()
    no_related = re.sub(r"\n## Related\n.*?(?=\n## |\Z)", "", strip_code(b), flags=re.S)
    cited = {l for l in link_re.findall(no_related) if l in pages and "type: source" in fm[l]}
    if "type: source" not in fm[n]:
        if cited - declared: print(f"  {n}: cited but not in sources: {sorted(cited - declared)}")
        if declared - links[n]: print(f"  {n}: in sources but never linked: {sorted(declared - links[n])}")

print("## 9 schema")
for n in content:
    f = fm[n]
    for k in ("type", "tags", "sources", "created", "updated"):
        if not re.search(rf"^{k}:", f, re.M): print(f"  {n}: missing {k}")
    if "domain/" not in f: print(f"  {n}: no domain tag")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n): print(f"  {n}: not kebab-case")
    if "type: source" in f and not re.search(r"^raw: ", f, re.M): print(f"  {n}: source without raw")
raws = {re.search(r"^raw: (.*)", fm[n], re.M).group(1).strip() for n in content if re.search(r"^raw: ", fm[n], re.M)}
for p in (root / "raw").glob("*.md"):
    if f"raw/{p.name}" not in raws: print(f"  raw without source page: {p.name}")

print("## 8 frequent terms without page")
terms_file = Path(__file__).with_name("terms.txt")
terms = [l.strip() for l in terms_file.read_text().splitlines()
         if l.strip() and not l.lstrip().startswith("#")] if terms_file.exists() else []
for t in terms:
    term_re = re.compile(rf"(?<!\w){re.escape(t)}(?!\w)", re.I)
    hits = [n for n in content if term_re.search(body[n])]
    has = any(t.lower().replace(" ", "-") == n or t.lower() in aliases for n in pages)
    if len(hits) >= 3 and not has:
        print(f"  {t}: {len(hits)} pages ({', '.join(sorted(hits))})")
