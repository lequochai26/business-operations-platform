import unicodedata
from pathlib import Path

from reader.fidelity import check, extract_items
from reader.rewrite import Block
from reader.sections import split_sections

SOURCE = """## Màn hình và quy tắc kiểm tra dữ liệu

- R-AUT-04: Mật khẩu dài hơn 128 ký tự → lỗi "Mật khẩu tối đa 128 ký tự".
- R-AUT-06: Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên không tồn tại, để không lộ tên nào có thật):
  - 5 lần sai trong cửa sổ 15 phút (tính từ lần sai đầu của cửa sổ) → khóa 15 phút; lần sai thứ 5 trả ngay 429;
  - đang khóa: mọi lần đăng nhập tên đó (kể cả đúng mật khẩu) → 429 `LOGIN_LOCKED`, "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (cùng câu cho màn Đăng nhập và Đổi mật khẩu, R-AUT-20), `<n>` = số phút còn lại làm tròn lên, tối thiểu 1; header `Retry-After` = số giây còn lại làm tròn lên. Không kiểm mật khẩu, không đếm thêm, không kéo dài khóa;
  - hết khóa: bộ đếm bắt đầu lại từ 0;
  - đồng thời (câu hỏi mở 7): mọi lần đọc để ghi bộ đếm chạy trong transaction có khóa dòng (`SELECT … FOR UPDATE` / upsert):
    - ghi lần sai (`recordFailure`): đang khóa → trả 429;
    - đúng mật khẩu (`confirmSuccess`): đang khóa → trả 429; request đã qua `verify` mà gặp khóa vẫn nhận 429.
"""

REWRITE = """### Quy tắc kiểm tra dữ liệu

**R-AUT-04.** Mật khẩu dài quá 128 ký tự thì báo lỗi "Mật khẩu tối đa 128 ký tự".

**R-AUT-06: Giới hạn số lần đăng nhập sai.** Một tên đăng nhập bị nhập sai mật khẩu 5 lần trong vòng 15 phút thì bị khóa 15 phút.

- Trong thời gian bị khóa, mọi lần đăng nhập đều bị từ chối với lỗi 429. Người dùng thấy: "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." Trong đó `<n>` là số phút còn lại, ít nhất là 1.
- Câu này dùng chung với màn Đổi mật khẩu, xem R-AUT-20.
- Khi hết thời gian khóa, bộ đếm quay về 0.
- Khi nhiều yêu cầu đến cùng lúc (câu hỏi mở 7), app chỉ tính tối đa 5 lần sai.

**Chi tiết kỹ thuật:** lỗi `LOGIN_LOCKED`, header `Retry-After`; transaction có khóa dòng (`SELECT … FOR UPDATE`); `recordFailure`, `confirmSuccess`, `verify`.
"""


def blocks_for(source, rewrite):
    section = split_sections(source)[0]
    return [split_sections(source)[0]], [Block(section.key, section.hash, rewrite)]


def test_extract_items_kinds():
    items = extract_items('Xem R-AUT-01 … R-AUT-03, lỗi "Tối đa 50", `LOGIN_LOCKED`, file docs/design/db-schema.md, https://x.vn/a, 15 phút.')
    assert ("mã", "R-AUT-02") in items
    assert ("chuỗi", "Tối đa 50") in items
    assert ("code", "LOGIN_LOCKED") in items
    assert ("đường dẫn", "docs/design/db-schema.md") in items
    assert ("đường dẫn", "https://x.vn/a") in items
    assert ("con số", "15") in items
    assert ("con số", "50") not in items  # nằm trong chuỗi nguyên văn, đã được kiểm qua chuỗi


def test_check_passes_when_rewrite_keeps_items():
    sections, blocks = blocks_for(SOURCE, REWRITE)
    assert check(Path("design/auth.md"), SOURCE, sections, blocks) == []


def test_check_reports_missing_number_and_string():
    broken = REWRITE.replace(' dài quá 128 ký tự thì báo lỗi "Mật khẩu tối đa 128 ký tự"', " dài quá giới hạn thì báo lỗi").replace(
        '"Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."', "thông báo khóa"
    )
    sections, blocks = blocks_for(SOURCE, broken)
    report = check(Path("design/auth.md"), SOURCE, sections, blocks)
    assert report[0] == "design/auth.md – bản đọc thiếu 3 mục so với bản gốc:"
    assert '- con số "128 ký tự" (mục Màn hình và quy tắc kiểm tra dữ liệu)' in report
    assert '- chuỗi "Mật khẩu tối đa 128 ký tự" (mục Màn hình và quy tắc kiểm tra dữ liệu)' in report
    assert '- chuỗi "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (mục Màn hình và quy tắc kiểm tra dữ liệu)' in report


def test_check_ignores_whitespace_and_nfd():
    nfd = unicodedata.normalize("NFD", REWRITE).replace(". Người dùng", ".\n   Người dùng")
    sections, blocks = blocks_for(SOURCE, nfd)
    assert check(Path("design/auth.md"), SOURCE, sections, blocks) == []


def test_check_ignores_abbreviation_definition_lines():
    source = "## Ghi chú chạy\n\n- `<api>` = `http://127.0.0.1:3000/api/v1`;\n- Gọi `<api>/sessions` 2 lần.\n"
    rewrite = "### Ghi chú chạy\n\nGọi `<api>/sessions` 2 lần.\n"
    sections, blocks = blocks_for(source, rewrite)
    assert check(Path("t.md"), source, sections, blocks) == []


def test_check_reports_changed_fenced_code():
    source = "## Lệnh\n\n```sql\nSELECT * FROM users;\n```\n"
    rewrite = "### Lệnh\n\n```sql\nDROP TABLE users;\n```\n"
    sections, blocks = blocks_for(source, rewrite)
    report = check(Path("t.md"), source, sections, blocks)
    assert any("SELECT * FROM users;" in line for line in report)


def test_check_reports_changed_unit():
    source = "## Khóa\n\nKhóa 15 phút.\n"
    sections, blocks = blocks_for(source, "### Khóa\n\nKhóa 15 giây.\n")
    assert '- con số "15 phút" (mục Khóa)' in check(Path("t.md"), source, sections, blocks)
