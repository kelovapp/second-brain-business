#!/usr/bin/env python3
"""Audit de sante du vault : liens morts, orphelins, notes stale, tirets longs.

Usage : python3 scripts/audit-vault.py
Sortie : rapport concis. Code 0 si propre, 1 si des ecarts sont trouves.
"""
import os
import re
import sys
from datetime import date, datetime

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", ".opencode", "scripts", "_Templates"}
SECRET_FILES = {"Identifiants.md"}  # mots de passe en clair, jamais indexes ni lies
INDEX_FILES = {"Accueil.md", "Index des livres.md", "Projets.md", "Concepts.md", "Captures.md"}
STALE_DAYS = 60
LINK_RE = re.compile(r"\[\[([^\]|#]+)")

def md_files():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(root, f)

files = sorted(md_files())
basenames = {os.path.splitext(os.path.basename(f))[0] for f in files}
content = {f: open(f, encoding="utf-8").read() for f in files}

dead_links, orphans, stale, dashes = [], [], [], []
referenced = set()
for f, text in content.items():
    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        referenced.add(target)
        if target not in basenames:
            dead_links.append((os.path.relpath(f, VAULT), target))

for f in files:
    base = os.path.basename(f)
    if base in INDEX_FILES:
        continue
    if base in SECRET_FILES:
        continue
    if os.path.splitext(base)[0] not in referenced:
        orphans.append(base)

today = date.today()
for f, text in content.items():
    m = re.search(r"derniere-maj:\s*(\d{4}-\d{2}-\d{2})", text)
    if m:
        d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        age = (today - d).days
        if age > STALE_DAYS:
            stale.append((os.path.basename(f), m.group(1), age))

for f, text in content.items():
    for bad in re.findall(r"[—–−]", text):
        dashes.append(os.path.relpath(f, VAULT))
        break

print(f"Audit du vault ({len(files)} notes, {len(basenames)} noms uniques)")
print("=" * 60)
for label, items in (("LIENS MORTS", dead_links), ("ORPHELINS", orphans),
                     ("STALE (> 60j)", stale), ("TIRETS LONGS", dashes)):
    if items:
        print(f"\n{label} : {len(items)}")
        for it in items[:20]:
            print(f"  - {it}")
        if len(items) > 20:
            print(f"  ... et {len(items) - 20} de plus")
    else:
        print(f"\n{label} : OK")

n = len(dead_links) + len(orphans) + len(stale) + len(dashes)
print("=" * 60)
print(f"Verdict : {n} ecart(s)" if n else "Vault sain, aucun ecart")
sys.exit(1 if n else 0)
