"""Sinh bản đọc Markdown từ bản viết lại: dòng đầu, anchor mục, triển khai viết tắt, chèn ý nghĩa của mã, link mục."""

import os
import re
from datetime import datetime
from pathlib import Path

from reader.abbrev import expand_abbreviations, parse_abbreviations
from reader.ids import Index, expand_range, find_refs
from reader.paths import reader_path, rewrite_path
from reader.rewrite import parse_rewrite
from reader.sections import split_sections
from reader.text import read_text, short_hash

HEADER_RE = re.compile(r"^> Bản đọc sinh từ (\S+) \(phiên bản ([0-9a-f]{7}), [^)]*\)\. Không sửa tay\.$")


def _src_rel(docs_root: Path, src: Path) -> str:
    return src.relative_to(docs_root.parent).as_posix()


def header_line(src_rel: str, src_hash: str, now: datetime) -> str:
    return f"> Bản đọc sinh từ {src_rel} (phiên bản {src_hash[:7]}, {now:%Y-%m-%d %H:%M}). Không sửa tay."


def parse_header(text: str) -> tuple[str, str] | None:
    first = text.lstrip("﻿").split("\n", 1)[0].rstrip("\r")
    match = HEADER_RE.match(first)
    return (match.group(1), match.group(2)) if match else None


def _link_sections(line: str, headings: list[tuple[str, str]]) -> str:
    for heading, key in headings:
        pattern = re.compile(rf"(?<!\[)mục {re.escape(heading)}(?![\w])", re.IGNORECASE)
        line = pattern.sub(lambda m: f"[{m.group(0)}](#s-{key})", line)
    return line


def render_reader(docs_root: Path, src: Path, blocks: list, index: Index, now: datetime) -> tuple[str, list[str]]:
    src_text = read_text(src)
    src_rel = _src_rel(docs_root, src)
    abbrevs = parse_abbreviations(src_text)
    headings = sorted(
        ((s.heading, s.key) for s in split_sections(src_text) if s.heading),
        key=lambda h: len(h[0]),
        reverse=True,
    )
    own_reader_dir = reader_path(docs_root, src).parent
    warnings: list[str] = []

    def render_id(id: str, text: str, block_key: str, seen: set[str]) -> str:
        definition = index.resolve(id, src)
        if definition is None:
            warnings.append(f"{src_rel}: không tìm thấy định nghĩa của {id}")
            return text
        if definition.source == src and definition.section_key == block_key:
            return text
        target = reader_path(docs_root, definition.source)
        link = "" if target == reader_path(docs_root, src) else os.path.relpath(target, own_reader_dir).replace("\\", "/")
        if definition.section_key:
            link += f"#s-{definition.section_key}"
        if id in seen:
            return f"[{text}]({link})"
        seen.add(id)
        gloss = definition.gloss.replace('"', "'")
        return f'[{text}]({link} "{gloss}") *({gloss})*'

    def render_line(line: str, block_key: str) -> str:
        if line.lstrip().startswith("#"):
            return line
        line = _link_sections(line, headings)
        seen: set[str] = set()
        refs = find_refs(line)
        rendered = []
        position = 0
        for ref in refs:
            if line[ref.start - 1 : ref.start] == "[":  # đã là link (vd. link mục)
                continue
            rendered.append(line[position : ref.start])
            original = line[ref.start : ref.end]
            if ".." in ref.id:
                rendered.append(", ".join(render_id(id, id, block_key, seen) for id in expand_range(ref.id)))
            else:
                rendered.append(render_id(ref.id, original, block_key, seen))
            position = ref.end
        rendered.append(line[position:])
        return "".join(rendered)

    out = [header_line(src_rel, short_hash(src_text), now), ""]
    for block in blocks:
        body = expand_abbreviations(block.body, abbrevs)
        out.append(f'<a id="s-{block.key}"></a>')
        out.append("")
        out.extend(render_line(line, block.key) for line in body.split("\n"))
        out.append("")
    return "\n".join(out), warnings


def stale_reports(docs_root: Path, sources: list[Path]) -> list[str]:
    reports = []
    for src in sources:
        src_rel = _src_rel(docs_root, src)
        reader = reader_path(docs_root, src)
        if not reader.exists():
            reports.append(f"{src_rel}: chưa có bản đọc")
            continue
        header = parse_header(read_text(reader))
        if header is None or header[1] != short_hash(read_text(src))[:7]:
            reports.append(f"{src_rel}: bản gốc đã đổi")
            continue
        rewrite = rewrite_path(docs_root, src)
        if rewrite.exists() and any(b.is_todo for b in parse_rewrite(read_text(rewrite), rewrite)):
            reports.append(f"{src_rel}: còn mục chưa viết lại")
    return reports
