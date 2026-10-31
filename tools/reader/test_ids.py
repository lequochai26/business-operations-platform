from reader.ids import Index, expand_range, find_refs, short_gloss

AUTH_DESIGN = """# Thiết kế chi tiết – Đăng nhập (`auth`, `AUT`)

## Màn hình và quy tắc kiểm tra dữ liệu

- R-AUT-06: Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên không tồn tại):
  - 5 lần sai trong cửa sổ 15 phút → khóa 15 phút;
- R-AUT-07: Tên đăng nhập được chuẩn hóa (bỏ khoảng trắng hai đầu, đổi chữ thường) trước khi tra cứu.

## Câu hỏi mở

- [x] 7. (phát hiện ở `/test-case-design`, P0-AUT-023) Nhiều request sai gửi đồng thời: `getLock` nằm ngoài transaction.
"""

AUTH_CASES = """# Test case – Đăng nhập

## P0-AUT-001 Quản lý đăng nhập từ trang cần đăng nhập
- Thiết kế: R-AUT-06; câu hỏi mở 7
"""

AUTH_REVIEW = """# Review – auth

### RV-03 Thiếu case dán link group không tồn tại
- Mức độ: nên sửa
"""

ISSUES = "# Sổ vấn đề\n\n## P0-ISS-003 Lưu được giới hạn 51\n- Trạng thái: mở\n"
PLAN0 = "# Kế hoạch\n\n### T06 API groups\n- Trạng thái: chưa làm\n"
PLAN1 = "# Kế hoạch\n\n### T06 Lịch hẹn\n- Trạng thái: chưa làm\n"
ADR = "# 0015 – Phiên lưu phía máy chủ\n\n- Ngày: 2026-10-31\n"


def make_docs(tmp_path, extra=None):
    docs = tmp_path / "docs"
    files = {
        "phases/phase-0/design/auth.md": AUTH_DESIGN,
        "phases/phase-0/design/reviews/auth-review.md": AUTH_REVIEW,
        "phases/phase-0/test/cases/auth.md": AUTH_CASES,
        "phases/phase-0/issues.md": ISSUES,
        "phases/phase-0/plan.md": PLAN0,
        "phases/phase-1/plan.md": PLAN1,
        "phases/phase-1/status.md": "Làm T06 trước.\n",
        "decisions/0015-server-side-sessions.md": ADR,
        **(extra or {}),
    }
    for rel, body in files.items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return docs


def build(docs):
    return Index.build(docs, sorted(docs.rglob("*.md")))


def test_short_gloss_examples():
    assert short_gloss("Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên…):") == "Giới hạn đăng nhập sai"
    assert (
        short_gloss("Chưa đăng nhập (`GET /api/v1/sessions/current` trả 401) mà mở trang cần đăng nhập → chuyển …")
        == "Chưa đăng nhập mà mở trang cần đăng nhập"
    )
    assert (
        short_gloss("Tên đăng nhập được chuẩn hóa (bỏ khoảng trắng hai đầu, đổi chữ thường) trước khi tra cứu, đếm R-AUT-06")
        == "Tên đăng nhập được chuẩn hóa trước khi tra cứu"
    )
    assert short_gloss("Hết hạn trượt: phiên hết hạn sau 90 ngày") == "Hết hạn trượt"
    long = short_gloss("a" * 80)
    assert len(long) == 60 and long.endswith("…")


def test_find_refs_skips_code_and_detects_range():
    refs = find_refs("R-AUT-01 … R-AUT-04 trả 400, `R-AUT-09` trong code, xem R-AUT-06 và câu hỏi mở 7, ADR 0015, T06, RV-03")
    assert [r.id for r in refs] == ["R-AUT-01..R-AUT-04", "R-AUT-06", "câu hỏi mở 7", "ADR 0015", "T06", "RV-03"]
    assert expand_range("R-AUT-01..R-AUT-04") == ["R-AUT-01", "R-AUT-02", "R-AUT-03", "R-AUT-04"]
    assert find_refs("T06-groups và AT06 không phải task") == []


def test_index_rule_case_issue_adr(tmp_path):
    docs = make_docs(tmp_path)
    index = build(docs)
    cases = docs / "phases/phase-0/test/cases/auth.md"
    rule = index.resolve("R-AUT-06", cases)
    assert rule.gloss == "Giới hạn đăng nhập sai"
    assert rule.source == docs / "phases/phase-0/design/auth.md"
    assert index.resolve("P0-AUT-001", cases).gloss == "Quản lý đăng nhập từ trang cần đăng nhập"
    assert index.resolve("P0-ISS-003", cases).gloss == "Lưu được giới hạn 51"
    assert index.resolve("ADR 0015", cases).gloss == "Phiên lưu phía máy chủ"
    assert index.resolve("R-AUT-99", cases) is None


def test_task_ids_scoped_to_phase(tmp_path):
    docs = make_docs(tmp_path)
    index = build(docs)
    assert index.resolve("T06", docs / "phases/phase-1/status.md").gloss == "Lịch hẹn"
    assert index.resolve("T06", docs / "phases/phase-0/issues.md").gloss == "API groups"


def test_open_question_resolves_to_design_of_same_slug(tmp_path):
    docs = make_docs(tmp_path)
    definition = build(docs).resolve("câu hỏi mở 7", docs / "phases/phase-0/test/cases/auth.md")
    assert definition.gloss == "Nhiều request sai gửi đồng thời"
    assert definition.source == docs / "phases/phase-0/design/auth.md"


def test_rv_resolves_to_review_file(tmp_path):
    docs = make_docs(tmp_path)
    definition = build(docs).resolve("RV-03", docs / "phases/phase-0/design/auth.md")
    assert definition.gloss == "Thiếu case dán link group không tồn tại"
    assert definition.source == docs / "phases/phase-0/design/reviews/auth-review.md"


def test_duplicate_definition_warns(tmp_path):
    docs = make_docs(tmp_path, {"phases/phase-0/design/other.md": "## Quy tắc\n\n- R-AUT-06: Bản trùng\n"})
    index = build(docs)
    assert any("R-AUT-06" in w for w in index.warnings)


def test_short_gloss_is_plain_text_without_backticks():
    gloss = short_gloss("Đọc cài đặt qua `SettingsService.get(key)` có cache 30 giây")
    assert "`" not in gloss
    assert gloss == "Đọc cài đặt qua SettingsService"
