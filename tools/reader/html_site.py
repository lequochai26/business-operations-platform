"""Sinh trang HTML từ bản đọc Markdown: ý nghĩa của mã thành tooltip, link .md thành .html, dải cảnh báo bản cũ."""

import os
import re
from html import escape
from pathlib import Path

import markdown

from reader.paths import HTML_DIR, READER_DIR, REWRITE_DIR, html_path
from reader.text import read_text

STALE_BANNER = '<div class="stale">Bản đọc này đã cũ so với bản gốc. Chạy /reader-view để sinh lại.</div>'
INLINE_GLOSS = re.compile(r'(<a [^>]*title="([^"]*)"[^>]*>.*?</a>) <em>\(\2\)</em>')
MD_HREF = re.compile(r'href="([^"#]*?)\.md(#[^"]*)?"')
STYLE = """
body { font-family: var(--font-family-body, sans-serif); color: var(--color-text-default, #2B2B2B);
       background: var(--color-surface-page, #FAF7F0); max-width: 960px; margin: 0 auto; padding: 24px; line-height: 1.6; }
a[title] { text-decoration: underline dotted; }
blockquote { color: var(--color-text-muted, #6B6B6B); border-left: 3px solid var(--color-surface-border, #E2DED3);
             margin: 0 0 16px; padding-left: 12px; }
code { background: var(--color-surface-card, #FFFFFF); padding: 0 4px; border-radius: 4px; }
table { border-collapse: collapse; } th, td { border: 1px solid var(--color-surface-border, #E2DED3); padding: 4px 8px; }
.stale { background: #FFF3CD; border: 1px solid var(--color-status-warning, #B7791F); padding: 8px 12px; margin-bottom: 16px; }
"""


def _reader_pages(docs_root: Path) -> list[Path]:
    reader_root = docs_root / READER_DIR
    return sorted(
        p for p in reader_root.rglob("*.md") if p.relative_to(reader_root).parts[0] not in (REWRITE_DIR, HTML_DIR)
    )


def _page(title: str, css_href: str, body: str) -> str:
    return (
        '<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
        f"<title>{escape(title)}</title>\n"
        f'<link rel="stylesheet" href="{css_href}">\n<style>{STYLE}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n'
    )


def _title(text: str, fallback: str) -> str:
    match = re.search(r"^#{1,3} (.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def render_site(docs_root: Path, stale_readers: set[Path]) -> list[Path]:
    written: list[Path] = []
    pages = _reader_pages(docs_root)
    css = docs_root / "design" / "ui-tokens.css"
    for md_path in pages:
        text = read_text(md_path)
        content = markdown.markdown(text, extensions=["tables", "fenced_code"])
        content = INLINE_GLOSS.sub(r"\1", content)
        content = MD_HREF.sub(lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', content)
        if md_path in stale_readers:
            content = STALE_BANNER + "\n" + content
        out = html_path(docs_root, md_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        css_href = os.path.relpath(css, out.parent).replace("\\", "/")
        out.write_text(_page(_title(text, md_path.stem), css_href, content), encoding="utf-8")
        written.append(out)

    html_root = docs_root / READER_DIR / HTML_DIR
    html_root.mkdir(parents=True, exist_ok=True)
    groups: dict[str, list[str]] = {}
    for out in written:
        rel = out.relative_to(html_root).as_posix()
        groups.setdefault(os.path.dirname(rel) or ".", []).append(rel)
    items = "\n".join(
        f"<h2>{escape(group)}</h2>\n<ul>\n"
        + "\n".join(f'<li><a href="{rel}">{escape(os.path.basename(rel))}</a></li>' for rel in rels)
        + "\n</ul>"
        for group, rels in sorted(groups.items())
    )
    index = html_root / "index.html"
    css_href = os.path.relpath(css, html_root).replace("\\", "/")
    index.write_text(_page("Bản đọc tài liệu", css_href, f"<h1>Bản đọc tài liệu</h1>\n{items}"), encoding="utf-8")
    written.append(index)
    return written
