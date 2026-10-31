from datetime import datetime

from reader.cli import main
from reader.paths import html_path, reader_path, rewrite_path
from reader.rewrite import TODO_MARK

NOW = datetime(2026, 10, 31, 14, 20)

DESIGN = """# Thiết kế – auth

## Quy tắc

- R-AUT-01: Tên đăng nhập trống → lỗi "Nhập tên đăng nhập".
- R-AUT-07: Tên đăng nhập được chuẩn hóa (bỏ khoảng trắng) trước khi tra cứu, đếm R-AUT-01.
"""

CASES = """# Test case

## P0-AUT-001 Quản lý đăng nhập
- Thiết kế: R-AUT-07
- Bước: nhập trống → "Nhập tên đăng nhập"
"""


def make_docs(tmp_path):
    docs = tmp_path / "docs"
    for rel, body in {"phases/phase-0/design/auth.md": DESIGN, "phases/phase-0/test/cases/auth.md": CASES}.items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return docs


def fill_todos(docs, transform=lambda s: s):
    """Giả lập AI viết lại: bỏ dòng TODO, giữ nguyên văn (qua transform nếu có)."""
    for path in (docs / "reader/_rewrite").rglob("*.md"):
        text = path.read_text(encoding="utf-8").replace(TODO_MARK + "\n", "")
        path.write_text(transform(text), encoding="utf-8")


def run(docs, *argv):
    return main(list(argv), docs, NOW)


def test_todo_creates_rewrite_with_todos(tmp_path, capsys):
    docs = make_docs(tmp_path)
    assert run(docs, "todo", "all") == 0
    out = capsys.readouterr().out
    assert "docs/phases/phase-0/design/auth.md: 2 mục cần viết lại" in out
    rewrite = rewrite_path(docs, docs / "phases/phase-0/design/auth.md").read_text(encoding="utf-8")
    assert rewrite.count(TODO_MARK) == 2


def test_build_fails_while_todo_remains(tmp_path, capsys):
    docs = make_docs(tmp_path)
    run(docs, "todo", "all")
    assert run(docs, "build", "all") == 1
    assert "còn 2 mục chưa viết lại" in capsys.readouterr().out


def test_build_rejects_outdated_rewrite(tmp_path, capsys):
    docs = make_docs(tmp_path)
    run(docs, "todo", "all")
    fill_todos(docs)
    (docs / "phases/phase-0/design/auth.md").write_text(DESIGN.replace("trống", "rỗng"), encoding="utf-8")
    assert run(docs, "build", "all") == 1
    assert "chạy lại todo" in capsys.readouterr().out


def test_build_reports_fidelity_and_exits_1(tmp_path, capsys):
    docs = make_docs(tmp_path)
    run(docs, "todo", "all")
    fill_todos(docs, lambda s: s.replace('"Nhập tên đăng nhập"', "thông báo lỗi"))
    assert run(docs, "build", "all") == 1
    out = capsys.readouterr().out
    assert "bản đọc thiếu" in out and '- chuỗi "Nhập tên đăng nhập"' in out


def test_build_success_writes_reader_and_html(tmp_path, capsys):
    docs = make_docs(tmp_path)
    run(docs, "todo", "all")
    fill_todos(docs)
    assert run(docs, "build", "all") == 0
    cases_reader = reader_path(docs, docs / "phases/phase-0/test/cases/auth.md")
    text = cases_reader.read_text(encoding="utf-8")
    assert text.startswith("> Bản đọc sinh từ docs/phases/phase-0/test/cases/auth.md (phiên bản ")
    assert "*(Tên đăng nhập được chuẩn hóa trước khi tra cứu)*" in text
    assert html_path(docs, cases_reader).exists()
    assert (docs / "reader/html/index.html").exists()


def test_stale_after_source_change(tmp_path, capsys):
    docs = make_docs(tmp_path)
    run(docs, "todo", "all")
    fill_todos(docs)
    run(docs, "build", "all")
    capsys.readouterr()
    assert run(docs, "stale") == 0
    assert "Mọi bản đọc đều mới" in capsys.readouterr().out
    (docs / "phases/phase-0/design/auth.md").write_text(DESIGN + "\nThêm.\n", encoding="utf-8")
    run(docs, "stale")
    assert "docs/phases/phase-0/design/auth.md: bản gốc đã đổi" in capsys.readouterr().out
