"""Generate per-page Markdown, llms.txt, and llms-full.txt from a built site.

Zensical has no plugin API yet (https://zensical.org/docs/community/faqs/) and
no llms.txt support, so this runs as a post-build step instead.

This works from the *rendered* HTML rather than docs/*.md so that any rendered
directives (e.g. mkdocstrings) are captured as real content rather than their
source form.

Usage: python scripts/gen_llms.py [site_dir]
"""

from __future__ import annotations

import os
import pathlib
import re
import sys
from html.parser import HTMLParser
from typing import ClassVar

# Read the Docs sets this per version, so /en/stable/ does not advertise
# /en/latest/ URLs. Falls back to latest for local builds.
SITE_URL = os.environ.get("READTHEDOCS_CANONICAL_URL", "https://django-friendship.readthedocs.io/en/latest/").rstrip(
    "/"
)
NAME = "django-friendship"
SUMMARY = "Create and manage follows, blocks, and bi-directional friendships between users."

# Page order for the index and the full corpus. Anything not listed is appended
# alphabetically, so a new page still shows up without editing this.
ORDER = [
    "index",
    "usage",
    "signals",
]

SKIP = {"404"}


class Extractor(HTMLParser):
    """Pull the <article> body out of a rendered page and re-emit Markdown."""

    BLOCK: ClassVar[set[str]] = {"p", "div", "section", "article", "ul", "ol", "table", "tr", "br"}
    HEADING: ClassVar[dict[str, int]] = {f"h{n}": n for n in range(1, 7)}

    def __init__(self) -> None:
        super().__init__()
        self.depth = 0  # >0 once inside <article>
        self.parts: list[str] = []
        self.title: str | None = None
        self._skip = 0  # inside nav/script/style
        self._pre = 0
        self._heading: int | None = None
        self._buf: list[str] = []
        self._code: list[str] = []
        self._lang = ""
        self._href: list[str] = []
        self.code: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "nav"):
            self._skip += 1
            return
        # Skip mkdocstrings' permalink anchors and heading self-links.
        if tag == "a" and "headerlink" in (a.get("class") or ""):
            self._skip += 1
            return
        if tag == "article":
            self.depth += 1
            return
        if not self.depth or self._skip:
            return
        if tag == "pre":
            self._pre += 1
            self._code = []
        elif tag == "div" and "language-" in (a.get("class") or ""):
            # Zensical wraps highlighted blocks in
            # <div class="language-python highlight">; the language is only there.
            m = re.search(r"language-(\w+)", a["class"])
            self._lang = m.group(1) if m else ""
            self.parts.append("\n")
        elif tag == "a" and not self._pre:
            href = a.get("href") or ""
            self._href.append(href)
            if href:
                self.parts.append("[")
        elif tag in self.HEADING:
            self._heading = self.HEADING[tag]
            self._buf = []
        elif tag in self.BLOCK:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav"):
            self._skip = max(0, self._skip - 1)
            return
        if tag == "a" and self._skip:
            self._skip = max(0, self._skip - 1)
            return
        if tag == "a" and self.depth and not self._pre and self._href:
            href = self._href.pop()
            if href:
                self.parts.append(f"]({href})")
            return
        if tag == "article":
            self.depth = max(0, self.depth - 1)
            return
        if not self.depth or self._skip:
            return
        if tag == "pre":
            self._pre = max(0, self._pre - 1)
            # Stash verbatim; whitespace normalisation below must not touch it,
            # or Python indentation in every example is destroyed.
            self.code.append((self._lang, "".join(self._code).strip("\n")))
            self.parts.append(f"\n\n\x00{len(self.code) - 1}\x00\n\n")
            self._code = []
        elif tag in self.HEADING and self._heading:
            text = re.sub(r"\s+", " ", "".join(self._buf)).strip()
            if text:
                if self.title is None and self._heading == 1:
                    self.title = text
                self.parts.append(f"\n\n{'#' * self._heading} {text}\n\n")
            self._heading = None
            self._buf = []

    def handle_data(self, data):
        if not self.depth or self._skip:
            return
        if self._heading:
            self._buf.append(data)
        elif self._pre:
            self._code.append(data)
        else:
            self.parts.append(re.sub(r"[ \t]*\n[ \t]*", " ", data))

    @staticmethod
    def _fence(lang: str, code: str) -> str:
        return f"```{lang}\n{code}\n```"

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t]{2,}", " ", text)
        # Strip trailing whitespace per line first, so blank-line collapsing
        # below sees genuinely empty lines rather than lines of spaces.
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Restore code blocks after normalisation, fenced.
        text = re.sub(r"\x00(\d+)\x00", lambda m: self._fence(*self.code[int(m.group(1))]), text)
        return text.strip() + "\n"


def slug_of(page: pathlib.Path, site: pathlib.Path) -> str:
    rel = page.relative_to(site)
    return "index" if rel.parent == pathlib.Path(".") else rel.parent.as_posix()


def main() -> int:
    site = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    if not site.is_dir():
        print(f"error: {site} does not exist -- build the site first", file=sys.stderr)
        return 1

    pages = {}
    for html_file in site.rglob("index.html"):
        slug = slug_of(html_file, site)
        if slug in SKIP:
            continue
        parser = Extractor()
        parser.feed(html_file.read_text(encoding="utf-8"))
        pages[slug] = (parser.title or slug, parser.markdown())

    ordered = [s for s in ORDER if s in pages]
    ordered += sorted(set(pages) - set(ordered))

    index = [f"# {NAME}\n", f"> {SUMMARY}\n", "## Docs\n"]
    full = [f"# {NAME}\n", f"> {SUMMARY}\n"]

    for slug in ordered:
        title, body = pages[slug]
        # A Markdown twin next to every page: /usage/ -> /usage.md
        md_path = site / ("index.md" if slug == "index" else f"{slug}.md")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(body, encoding="utf-8")

        url = f"{SITE_URL}/" if slug == "index" else f"{SITE_URL}/{slug}.md"
        index.append(f"- [{title}]({url})")
        full.append(f"\n---\n\n<!-- {slug} -->\n\n{body}")

    (site / "llms.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    (site / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")

    words = len((site / "llms-full.txt").read_text().split())
    print(f"wrote llms.txt ({len(ordered)} pages), llms-full.txt (~{words:,} words), and {len(ordered)} .md twins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
