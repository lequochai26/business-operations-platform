"""CLI sinh bản đọc.

    py tools/reader/cli.py todo <file… | phase-N | all>   đánh dấu mục cần AI viết lại
    py tools/reader/cli.py build [file… | phase-N | all]   kiểm tra trung thực, sinh Markdown và HTML
    py tools/reader/cli.py stale [file… | phase-N | all]   liệt kê bản đọc cũ hoặc còn thiếu
"""

import sys
from datetime import datetime
from pathlib import Path

if __name__ == "__main__":
    # Chạy dạng script: thay thư mục tools/reader bằng tools/ để import gói `reader`.
    sys.path[0] = str(Path(__file__).resolve().parents[1])

from reader.expand import render_reader, stale_reports  # noqa: E402
from reader.fidelity import check  # noqa: E402
from reader.html_site import render_site  # noqa: E402
from reader.ids import Index  # noqa: E402
from reader.paths import html_path, reader_path, rewrite_path, select_sources, source_files  # noqa: E402
from reader.rewrite import Block, format_rewrite, parse_rewrite, sync_rewrite  # noqa: E402
from reader.sections import Section, split_sections  # noqa: E402
from reader.text import read_text  # noqa: E402


def _rel(docs_root: Path, path: Path) -> str:
    return path.relative_to(docs_root.parent).as_posix()


def _load_blocks(docs_root: Path, src: Path) -> list[Block] | None:
    path = rewrite_path(docs_root, src)
    return parse_rewrite(read_text(path), path) if path.exists() else None


def _problems(docs_root: Path, src: Path, sections: list[Section], blocks: list[Block] | None) -> list[str]:
    rel = _rel(docs_root, src)
    if blocks is None:
        return [f"{rel}: chưa chạy todo"]
    todo = sum(1 for b in blocks if b.is_todo)
    if todo:
        return [f"{rel}: còn {todo} mục chưa viết lại"]
    current = {s.key: s.hash for s in sections}
    if {b.key: b.src_hash for b in blocks} != current:
        return [f"{rel}: bản gốc đã đổi sau lần chạy todo, chạy lại todo"]
    return []


def cmd_todo(docs_root: Path, targets: list[str]) -> int:
    for src in select_sources(docs_root, targets):
        sections = split_sections(read_text(src))
        synced, todo = sync_rewrite(sections, _load_blocks(docs_root, src) or [])
        path = rewrite_path(docs_root, src)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(format_rewrite(synced), encoding="utf-8")
        print(f"{_rel(docs_root, src)}: {len(todo)} mục cần viết lại")
        for section in todo:
            print(f"  - {section.heading or 'đầu tài liệu'}")
    return 0


def cmd_build(docs_root: Path, targets: list[str], now: datetime) -> int:
    selected = select_sources(docs_root, targets)
    errors: list[str] = []
    for src in selected:
        src_text = read_text(src)
        sections = split_sections(src_text)
        blocks = _load_blocks(docs_root, src)
        problems = _problems(docs_root, src, sections, blocks)
        errors += problems or check(Path(_rel(docs_root, src)), src_text, sections, blocks)
    if errors:
        print("\n".join(errors))
        return 1

    all_sources = source_files(docs_root)
    index = Index.build(docs_root, all_sources)
    warnings = list(index.warnings)
    for src in all_sources:
        blocks = _load_blocks(docs_root, src)
        if _problems(docs_root, src, split_sections(read_text(src)), blocks):
            continue
        text, render_warnings = render_reader(docs_root, src, blocks, index, now)
        warnings += render_warnings
        out = reader_path(docs_root, src)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")

    stale = {reader_path(docs_root, src) for src in all_sources if stale_reports(docs_root, [src])}
    render_site(docs_root, stale)
    for warning in dict.fromkeys(warnings):
        print(f"Cảnh báo: {warning}")
    for src in selected:
        md = reader_path(docs_root, src)
        print(f"{_rel(docs_root, md)} | {_rel(docs_root, html_path(docs_root, md))}")
    return 0


def cmd_stale(docs_root: Path, targets: list[str]) -> int:
    reports = stale_reports(docs_root, select_sources(docs_root, targets))
    print("\n".join(reports) if reports else "Mọi bản đọc đều mới")
    return 0


def main(argv: list[str], docs_root: Path, now: datetime) -> int:
    if not argv or argv[0] not in ("todo", "build", "stale"):
        print(__doc__)
        return 2
    command, targets = argv[0], argv[1:] or ["all"]
    if command == "todo":
        return cmd_todo(docs_root, targets)
    if command == "build":
        return cmd_build(docs_root, targets, now)
    return cmd_stale(docs_root, targets)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], Path(__file__).resolve().parents[2] / "docs", datetime.now()))
