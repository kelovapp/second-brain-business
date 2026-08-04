#!/usr/bin/env python3
"""
Extract full text from a PDF or EPUB into a single .txt file, tagged for
chunking:
  - PDF  -> [PAGE n] markers (via poppler's pdfinfo/pdftotext)
  - EPUB -> [CH <spine-label>] markers, in correct spine order via content.opf

Usage:
  python3 extract_book.py <book.pdf|book.epub> <out.txt>

Prints a short report to stdout. Exit 1 on failure.
"""
import sys
import os
import re
import zipfile
import subprocess
from html.parser import HTMLParser

BLOCK_TAGS = (
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "tr", "blockquote", "section", "header", "footer",
)

PAGE = lambda n: f"\n\n[PAGE {n}]\n\n"
CH = lambda name: f"\n\n[CH {name}]\n\n"


# ---------------- PDF ----------------

def pdf_page_count(path):
    r = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    m = re.search(r"^Pages:\s*(\d+)", r.stdout, re.M)
    return int(m.group(1)) if m else None


def extract_pdf(path, out):
    total = pdf_page_count(path)
    written = 0
    i = 1
    while total is not None and i <= total:
        r = subprocess.run(
            ["pdftotext", "-f", str(i), "-l", str(i), path, "-"],
            capture_output=True,
        )
        text = r.stdout.decode("utf-8", "replace")
        if text.strip():
            out.write(PAGE(i) + text)
            written += 1
        i += 1
    if written == 0:
        sys.exit(
            "ERROR: no text extracted from PDF (scanned book? try: "
            f"ocrmypdf -l eng '{path}' /tmp/ocr.pdf)"
        )
    return written, total


# ---------------- EPUB ----------------

class Txt(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK_TAGS:
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag in BLOCK_TAGS:
            self.parts.append("\n\n")

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def strip_html(data):
    p = Txt()
    p.feed(data)
    raw = "".join(p.parts)
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    return raw


def epub_spine(path):
    """Return ordered list of hrefs from container.xml -> content.opf, or None."""
    try:
        with zipfile.ZipFile(path) as z:
            container = z.read("META-INF/container.xml").decode("utf-8", "replace")
            m = re.search(r'full-path="([^"]+\.opf)"', container)
            if not m:
                return None
            xml = z.read(m.group(1)).decode("utf-8", "replace")
            hrefs = re.findall(r'<itemref[^>]+idref="([^"]+)"', xml)
            id2href = {}
            for tag in re.finditer(r"<item\b[^>]*>", xml):
                mid = re.search(r'\bid="([^"]+)"', tag.group(0))
                mhref = re.search(r'\bhref="([^"]+)"', tag.group(0))
                if mid and mhref:
                    id2href[mid.group(1)] = mhref.group(1)
            base = os.path.dirname(m.group(1))
            order = []
            for ref in hrefs:
                if ref in id2href:
                    order.append(os.path.normpath(os.path.join(base, id2href[ref])))
            if order:
                return order
    except Exception:
        pass
    return None


def clean_label(name):
    name = os.path.basename(name)
    name = re.sub(r"\.(x?html?)$", "", name, flags=re.I)
    name = re.sub(r"^\d+[_-]+", "", name)
    return name.replace("_", " ").replace("-", " ").strip() or "untitled"


def extract_epub(path, out):
    written = 0
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        order = epub_spine(path)
        if not order:
            order = sorted(
                n for n in names
                if n.endswith((".xhtml", ".html", ".htm"))
                and not n.startswith(("META-INF", "mimetype", "toc"))
            )
        for rel in order:
            rel = rel.replace("\\", "/")
            if rel not in names:
                continue
            text = strip_html(z.read(rel).decode("utf-8", "replace"))
            if text.strip():
                out.write(CH(clean_label(rel)) + text)
                written += 1
    if written == 0:
        sys.exit("ERROR: no text extracted from EPUB")
    return written, len(names)


# ---------------- main ----------------

def main():
    if len(sys.argv) != 3:
        sys.exit("usage: extract_book.py <book.pdf|book.epub> <out.txt>")
    book, out_path = sys.argv[1], sys.argv[2]
    if not os.path.exists(book):
        sys.exit(f"ERROR: file not found: {book}")
    ext = os.path.splitext(book)[1].lower()
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as out:
        if ext == ".pdf":
            parts, total = extract_pdf(book, out)
            print(f"OK pdf: {parts}/{total} pages extracted -> {out_path}")
        elif ext == ".epub":
            parts, total = extract_epub(book, out)
            print(f"OK epub: {parts} spine documents -> {out_path}")
        else:
            sys.exit(f"ERROR: unsupported format {ext} (pdf/epub only)")
    with open(out_path) as f:
        wc = len(f.read().split())
    print(f"words: {wc}")


if __name__ == "__main__":
    main()
