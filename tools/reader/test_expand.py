from datetime import datetime

from reader.expand import header_line, parse_header, render_reader, stale_reports
from reader.ids import Index
from reader.paths import reader_path, rewrite_path
from reader.rewrite import TODO_MARK, Block, format_rewrite
from reader.sections import split_sections
from reader.text import read_text, short_hash

NOW = datetime(2026, 10, 31, 14, 20)

DESIGN = """# Thiết kế – auth

## Quy tắc

- R-AUT-01: Tên đăng nhập trống → lỗi "Nhập tên đăng nhập".
- R-AUT-02: Tên đăng nhập dài hơn 32 ký tự → lỗi.
- R-AUT-07: Tên đăng nhập được chuẩn hóa (bỏ khoảng trắng) trước khi tra cứu, đếm R-AUT-06.

## Trạng thái và thuật toán

Bước 1.
"""

CASES = """# Test case

## Ghi chú chạy

- `<api>` = `http://127.0.0.1:3000/api/v1`;

## P0-AUT-001 Quản lý đăng nhập
- Thiết kế: R-AUT-07
"""


def make_docs(tmp_path):
    docs = tmp_path / "docs"
    for rel, body in {"phases/phase-0/design/auth.md": DESIGN, "phases/phase-0/test/cases/auth.md": CASES}.items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return docs


def render_line(tmp_path, src_rel, line):
    docs = make_docs(tmp_path)
    src = docs / src_rel
    index = Index.build(docs, sorted(docs.rglob("*.md")))
    section = split_sections(read_text(src))[-1]
    text, warnings = render_reader(docs, src, [Block(section.key, section.hash, line)], index, NOW)
    return text, warnings


def test_header_line_format():
    line = header_line("docs/phases/phase-0/design/auth.md", "a3f9c21bd0e1", NOW)
    assert line == "> Bản đọc sinh từ docs/phases/phase-0/design/auth.md (phiên bản a3f9c21, 2026-10-31 14:20). Không sửa tay."
    assert parse_header(line + "\n\nnội dung") == ("docs/phases/phase-0/design/auth.md", "a3f9c21")


def test_render_inserts_gloss_once_per_line(tmp_path):
    text, warnings = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "Theo R-AUT-07, và lần nữa R-AUT-07.")
    gloss = "Tên đăng nhập được chuẩn hóa trước khi tra cứu"
    assert text.count(f"*({gloss})*") == 1
    assert f'[R-AUT-07](../../design/auth.md#s-' in text
    assert f'"{gloss}")' in text
    assert warnings == []


def test_render_expands_range(tmp_path):
    text, _ = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "Xem R-AUT-01 … R-AUT-02.")
    assert "*(Tên đăng nhập trống)*" in text
    assert "*(Tên đăng nhập dài hơn 32 ký tự)*" in text
    assert "R-AUT-01 …" not in text


def test_render_skips_headings_and_code(tmp_path):
    text, _ = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "### Liên quan R-AUT-07\n\nGiá trị `R-AUT-07` trong code.")
    assert "*(" not in text


def test_render_links_section_reference(tmp_path):
    text, _ = render_line(tmp_path, "phases/phase-0/design/auth.md", "Chi tiết ở mục Trạng thái và thuật toán.")
    key = [s for s in split_sections(DESIGN) if s.heading == "Trạng thái và thuật toán"][0].key
    assert f"[mục Trạng thái và thuật toán](#s-{key})" in text


def test_render_expands_abbreviations(tmp_path):
    text, _ = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "Gọi `<api>/sessions`.")
    assert "`http://127.0.0.1:3000/api/v1/sessions`" in text


def test_render_keeps_abbreviation_definition_lines_unexpanded(tmp_path):
    text, _ = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "- `<api>` = `http://127.0.0.1:3000/api/v1`;\n- Gọi `<api>/x`.")
    assert "- `<api>` = `http://127.0.0.1:3000/api/v1`;" in text
    assert "`http://127.0.0.1:3000/api/v1` = " not in text
    assert "Gọi `http://127.0.0.1:3000/api/v1/x`." in text


def test_expand_unknown_id_left_plain_with_warning(tmp_path):
    text, warnings = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "Xem R-XYZ-09.")
    assert "Xem R-XYZ-09." in text
    assert any("R-XYZ-09" in w for w in warnings)


def test_render_starts_with_header_and_anchor(tmp_path):
    text, _ = render_line(tmp_path, "phases/phase-0/test/cases/auth.md", "Nội dung.")
    lines = text.split("\n")
    assert lines[0].startswith("> Bản đọc sinh từ docs/phases/phase-0/test/cases/auth.md (phiên bản ")
    assert any(line.startswith('<a id="s-') for line in lines)


def test_stale_reports_three_reasons(tmp_path):
    docs = make_docs(tmp_path)
    design, cases = docs / "phases/phase-0/design/auth.md", docs / "phases/phase-0/test/cases/auth.md"
    assert stale_reports(docs, [design]) == ["docs/phases/phase-0/design/auth.md: chưa có bản đọc"]

    reader = reader_path(docs, design)
    reader.parent.mkdir(parents=True)
    reader.write_text(header_line("docs/phases/phase-0/design/auth.md", short_hash(read_text(design)), NOW), encoding="utf-8")
    assert stale_reports(docs, [design]) == []
    design.write_text(DESIGN + "\nThêm dòng.\n", encoding="utf-8")
    assert stale_reports(docs, [design]) == ["docs/phases/phase-0/design/auth.md: bản gốc đã đổi"]

    reader = reader_path(docs, cases)
    reader.parent.mkdir(parents=True)
    reader.write_text(header_line("docs/phases/phase-0/test/cases/auth.md", short_hash(read_text(cases)), NOW), encoding="utf-8")
    rewrite = rewrite_path(docs, cases)
    rewrite.parent.mkdir(parents=True)
    rewrite.write_text(format_rewrite([Block("abcdef0123", "0123456789ab", f"{TODO_MARK}\nx")]), encoding="utf-8")
    assert stale_reports(docs, [cases]) == ["docs/phases/phase-0/test/cases/auth.md: còn mục chưa viết lại"]
