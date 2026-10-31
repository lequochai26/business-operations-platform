import re

from reader.html_site import render_site

PAGE = """> Bản đọc sinh từ docs/phases/phase-0/test/cases/auth.md (phiên bản a3f9c21, 2026-10-31 14:20). Không sửa tay.

<a id="s-0123456789"></a>

### P0-AUT-001: Quản lý đăng nhập

Dựa trên [R-AUT-07](../../design/auth.md#s-abcdef0123 "Tên đăng nhập được chuẩn hóa") *(Tên đăng nhập được chuẩn hóa)*.
"""


def make_reader(tmp_path):
    docs = tmp_path / "docs"
    reader = docs / "reader/phases/phase-0/test/cases/auth.md"
    reader.parent.mkdir(parents=True)
    reader.write_text(PAGE, encoding="utf-8")
    rewrite = docs / "reader/_rewrite/phases/phase-0/test/cases/auth.md"
    rewrite.parent.mkdir(parents=True)
    rewrite.write_text("không được render", encoding="utf-8")
    (docs / "design").mkdir(parents=True)
    (docs / "design/ui-tokens.css").write_text(":root {}", encoding="utf-8")
    return docs, reader


def page_html(docs):
    return (docs / "reader/html/phases/phase-0/test/cases/auth.html").read_text(encoding="utf-8")


def test_html_tooltip_replaces_inline_gloss(tmp_path):
    docs, _ = make_reader(tmp_path)
    render_site(docs, set())
    html = page_html(docs)
    assert 'title="Tên đăng nhập được chuẩn hóa"' in html
    assert "<em>(Tên đăng nhập được chuẩn hóa)</em>" not in html


def test_html_links_point_to_html(tmp_path):
    docs, _ = make_reader(tmp_path)
    render_site(docs, set())
    html = page_html(docs)
    assert 'href="../../design/auth.html#s-abcdef0123"' in html
    assert 'href="../../../../../../design/ui-tokens.css"' in html


def test_html_nested_list_with_two_space_indent(tmp_path):
    docs, reader = make_reader(tmp_path)
    reader.write_text("- Cha:\n  - con một;\n  - con hai.\n- Cha hai.\n", encoding="utf-8")
    render_site(docs, set())
    html = page_html(docs)
    assert html.count("<ul>") == 2
    assert re.search(r"<li>Cha:\s*<ul>\s*<li>con một;</li>", html)


def test_html_stale_banner(tmp_path):
    docs, reader = make_reader(tmp_path)
    render_site(docs, {reader})
    assert 'class="stale"' in page_html(docs)
    render_site(docs, set())
    assert 'class="stale"' not in page_html(docs)


def test_html_index_lists_pages(tmp_path):
    docs, _ = make_reader(tmp_path)
    written = render_site(docs, set())
    index = (docs / "reader/html/index.html").read_text(encoding="utf-8")
    assert 'href="phases/phase-0/test/cases/auth.html"' in index
    assert not (docs / "reader/html/_rewrite").exists()
    assert len(written) == 2


def test_html_tooltip_for_gloss_with_special_chars(tmp_path):
    docs, reader = make_reader(tmp_path)
    reader.write_text(r'Xem [R-AUT-25](x.md#s-a "Vai trò <manager|technician>") *(Vai trò \<manager\|technician\>)*.' + "\n", encoding="utf-8")
    render_site(docs, set())
    html = page_html(docs)
    assert 'title="Vai trò &lt;manager|technician&gt;"' in html
    assert "<em>" not in html


def test_html_tooltip_for_gloss_with_double_quotes(tmp_path):
    docs, reader = make_reader(tmp_path)
    reader.write_text('Xem [R-AUT-32](x.md#s-a "Bấm \'Đăng xuất\'") *(Bấm "Đăng xuất")*.\n', encoding="utf-8")
    render_site(docs, set())
    assert "<em>" not in page_html(docs)
