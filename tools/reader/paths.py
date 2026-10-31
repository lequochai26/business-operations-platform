"""Phạm vi bản gốc và vị trí của bản đọc, bản viết lại, bản HTML."""

from pathlib import Path

DOCS_ROOT_NAME = "docs"
SOURCE_DIRS = ("phases", "design", "decisions", "testing")
READER_DIR = "reader"
REWRITE_DIR = "_rewrite"
HTML_DIR = "html"


def source_files(docs_root: Path) -> list[Path]:
    files = []
    for name in SOURCE_DIRS:
        base = docs_root / name
        if base.is_dir():
            files += base.rglob("*.md")
    return sorted(files, key=lambda p: p.relative_to(docs_root).as_posix())


def select_sources(docs_root: Path, targets: list[str]) -> list[Path]:
    all_files = source_files(docs_root)
    selected: list[Path] = []
    for target in targets:
        if target == "all":
            selected += all_files
        elif target.startswith("phase-"):
            base = docs_root / "phases" / target
            selected += [p for p in all_files if base in p.parents]
        else:
            selected.append(Path(target))
    return list(dict.fromkeys(selected))


def reader_path(docs_root: Path, src: Path) -> Path:
    return docs_root / READER_DIR / src.relative_to(docs_root)


def rewrite_path(docs_root: Path, src: Path) -> Path:
    return docs_root / READER_DIR / REWRITE_DIR / src.relative_to(docs_root)


def html_path(docs_root: Path, reader_md: Path) -> Path:
    rel = reader_md.relative_to(docs_root / READER_DIR)
    return (docs_root / READER_DIR / HTML_DIR / rel).with_suffix(".html")
