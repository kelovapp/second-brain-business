#!/usr/bin/env python3
"""
Split book.txt (output of extract_book.py) into reading chunks + manifest.json.

Strategy, in order:
  1. [CH ...] markers (epub)  -> split per document, then merge/split to size.
  2. Heading heuristic on [PAGE]-tagged pdf text (Chapter/Part/roman numerals).
  3. Equal-size paragraph chunks as fallback.

Emits:
  <outdir>/chunk_000.md ...      (markdown files, one per chunk)
  <outdir>/manifest.json         (index, heading, words per chunk)

Usage: split_chunks.py <book.txt> <outdir> [--target 16000]
"""
import sys
import os
import re
import json

HEAD_RE = re.compile(
    r"^\s*(chapter|part|book|section|chapitre|annex)\s+([0-9ivxlcdm]+)",
    re.I,
)
CAPS_RE = re.compile(r"^[A-ZÀ-Ü][A-ZÀ-Ü0-9 ,'’\.\-\&]{4,89}$")


def read_blocks(text):
    """Split text on [PAGE n] / [CH label] markers -> list of (label, content)."""
    blocks = []
    cur = ""
    label = None
    for line in text.splitlines(keepends=True):
        m = re.match(r"^\s*\[(PAGE|CH)\s+([^\]]+)\]\s*$", line)
        if m:
            if cur.strip():
                blocks.append((label, cur))
            label = (m.group(1), m.group(2).strip())
            cur = ""
        else:
            cur += line
    if cur.strip():
        blocks.append((label, cur))
    return blocks


def looks_like_heading(s):
    s = s.strip()
    if not s or len(s) > 90:
        return False
    if ".." in s or "..." in s:
        return False
    if HEAD_RE.match(s):
        return True
    if CAPS_RE.match(s) and len(s) >= 5:
        return True
    return False


def find_heads(blocks):
    """Return [(block_index, heading)] for detected chapter starts."""
    heads = []
    for i, (label, content) in enumerate(blocks):
        if isinstance(label, tuple) and label[0] == "CH":
            heads.append((i, label[1]))
            continue
        for line in content.splitlines():
            if looks_like_heading(line):
                heads.append((i, line.strip()))
                break
    return heads


def merge_text(blocks):
    if blocks and isinstance(blocks[0], tuple):
        return "\n".join(c for _, c in blocks)
    return "\n".join(blocks)


def split_on_paragraph(text, target):
    """Split text into paragraph groups, each roughly target chars."""
    paras = re.split(r"\n\s*\n", text)
    chunks = []
    cur = ""
    for p in paras:
        if not p.strip():
            continue
        if len(cur) + len(p) > target * 1.6 and cur:
            chunks.append(cur)
            cur = p
        else:
            cur = cur + "\n\n" + p if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def main():
    args = [a for a in sys.argv[1:]]
    target = 16000
    if "--target" in args:
        i = args.index("--target")
        target = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit("usage: split_chunks.py <book.txt> <outdir> [--target N]")
    book_path, outdir = args
    os.makedirs(outdir, exist_ok=True)
    with open(book_path) as f:
        text = f.read()

    blocks = read_blocks(text)
    if not blocks:
        sys.exit("ERROR: empty text")

    heads = find_heads(blocks)

    if heads:
        # group blocks by detected chapter
        hmap = {i: h for i, h in heads}
        groups = []
        cur = []
        cur_head = None
        for i, (label, content) in enumerate(blocks):
            if i in hmap:
                if cur:
                    groups.append((cur_head, cur))
                cur = [content]
                cur_head = hmap[i]
            else:
                cur.append(content)
        if cur:
            groups.append((cur_head, cur))

        chunks = []
        for head, group in groups:
            if not head:
                head = "Intro / Front matter"
            txt = merge_text(group)
            if len(txt) <= target * 1.6:
                chunks.append((head, txt))
            else:
                for i, part in enumerate(split_on_paragraph(txt, target)):
                    chunks.append((f"{head} ({i + 1})" if i else head, part))
    else:
        # fallback: merge all blocks, split on paragraphs
        txt = merge_text(blocks)
        chunks = [("Untitled", c) for c in split_on_paragraph(txt, target)]

    # merge small consecutive chunks to limit subagent count
    merged = []
    for head, txt in chunks:
        if merged and len(merged[-1][1]) + len(txt) < target * 1.4:
            h0, t0 = merged[-1]
            merged[-1] = (
                f"{h0} + {head}" if (h0 and head and h0 != head) else (h0 or head),
                t0 + "\n\n" + txt,
            )
        else:
            merged.append((head, txt))
    chunks = merged

    manifest = []
    for i, (head, content) in enumerate(chunks):
        name = f"chunk_{i:03d}.md"
        with open(os.path.join(outdir, name), "w") as f:
            f.write(f"# {head}\n\n{content}\n")
        manifest.append({
            "index": i,
            "file": name,
            "heading": head,
            "chars": len(content),
            "words": len(content.split()),
        })

    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    total = sum(m["words"] for m in manifest)
    print(f"chunks: {len(chunks)}  (target ~{target} chars)")
    print(f"words: {total}")
    print(f"manifest: {os.path.join(outdir, 'manifest.json')}")
    for m in manifest:
        print(f"  {m['file']}: {m['words']}w  {m['heading']}")


if __name__ == "__main__":
    main()
