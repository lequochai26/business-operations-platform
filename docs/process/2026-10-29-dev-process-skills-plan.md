# Dev Process Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tạo bộ 20 skill + command `/phase-status` + quy tắc `CLAUDE.md` + các script hỗ trợ (sinh token CSS, chụp mockup, xuất báo cáo Excel/PDF) theo spec.

**Architecture:** Mỗi skill là một thư mục `.claude/skills/<tên>/` gồm `SKILL.md` theo khung cố định, `templates/`, `checklists/`. Một validator Python kiểm tra cấu trúc mọi skill, đóng vai trò test cho phần nội dung Markdown. Phần có logic (sinh token, chụp ảnh, xuất báo cáo) là script Python có pytest.

**Tech Stack:** Python 3.15 (`py`), pytest, PyYAML, openpyxl, Pillow, Jinja2, Markdown, Playwright for Python (Chromium); Redocly CLI qua `npx`.

**Spec:** `docs/process/2026-10-29-dev-process-skills-design.md`

## Global Constraints

- Danh sách skill (đúng tên thư mục): `conventions-init`, `ui-style-init`, `ui-style-update`, `test-viewpoints-init`, `phase-kickoff`, `detailed-design`, `ui-design`, `component-design`, `test-case-design`, `design-review`, `decision-log`, `implementation-plan`, `implement-task`, `tdd`, `code-review`, `bug-fix`, `change-request`, `manual-test-run`, `feedback`, `acceptance-report`. Command: `.claude/commands/phase-status.md`.
- Không skill nào gọi hay nhắc tới skill của superpowers.
- Tên file, tên skill, mã định danh: tiếng Anh. Nội dung `SKILL.md`, mẫu, tài liệu sinh ra: tiếng Việt.
- Frontmatter mỗi `SKILL.md`: `name` (trùng tên thư mục), `description` (≤ 1024 ký tự, có từ khóa tiếng Việt và tiếng Anh), `argument-hint` (chuỗi, rỗng nếu không có tham số).
- Mỗi `SKILL.md` có đủ các heading cấp 2, đúng thứ tự: `## Mục đích`, `## Điều kiện tiên quyết`, `## Input`, `## Các bước`, `## Điểm dừng`, `## Output`, `## Tự kiểm tra`, `## Cập nhật status.md`, `## Báo cáo kết thúc`. Mục không áp dụng ghi "Không áp dụng."
- Mã định danh (spec mục 2): giai đoạn `phase-N`; test case `P<N>-<ABC>-<nnn>`; task `T<nn>`; ADR `NNNN-<slug>`; lần chạy `YYYY-MM-DD-NN`; vấn đề `P<N>-ISS-<nnn>`.
- Trạng thái tính năng, đúng chuỗi (spec mục 7): `chưa bắt đầu`, `thiết kế chi tiết`, `UI`, `test case`, `đã duyệt thiết kế`, `đang code`, `đã code`, `đang manual test`, `đạt`.
- Kết quả test, đúng chuỗi: `đạt`, `không đạt`, `bị chặn`, `bỏ qua`.
- Mockup: khung 1440×900; component là Web Component thuần (`components/<tên>.js`), mockup nhúng bằng `<script src>` + thẻ custom element, mở được bằng `file://`.
- Mọi file đọc/ghi bằng `encoding="utf-8"` (Windows mặc định không phải UTF-8); parser chấp nhận BOM và CRLF.
- Không commit: `docs/phases/*/test/runs/*/evidence/`, `docs/phases/*/acceptance/*.xlsx`, `docs/phases/*/acceptance/*.pdf`, `.local/`.
- Chạy toàn bộ test: `py -m pytest tools .claude/skills -q`.
- Làm trên nhánh `docs/dev-process-skills` hiện tại.

## Review Focus

- **Evidence đã bị xóa** (người dùng xóa ảnh sau khi xác nhận) mà vẫn xuất báo cáo → không crash, ô ghi "Thiếu file evidence: <tên>" và in cảnh báo. Test: `test_build_xlsx_missing_evidence_warns`, `test_build_pdf_missing_evidence_warns` (Task 12).
- **File `report.xlsx` đang mở trong Excel** khi xuất lại → báo "Đóng file <đường dẫn> rồi chạy lại", thoát mã 1, không traceback. Test: `test_main_reports_locked_output` (Task 12).
- **`results.md` bị lưu kiểu CRLF hoặc có BOM** (git trên Windows đổi LF → CRLF) → parse như bình thường. Test: `test_parse_results_handles_crlf_and_bom` (Task 12); `test_validate_skill_accepts_crlf_and_bom` (Task 1).
- **Kết quả viết lệch** (`Đạt`, ` đạt `, tổ hợp dấu NFD) → chuẩn hóa NFC + lowercase + strip; giá trị lạ → lỗi nêu đường dẫn và số dòng. Test: `test_parse_results_normalizes_result`, `test_parse_results_rejects_unknown_result` (Task 12).
- **`ui-style.md` thiếu khối tokens hoặc token lồng nhiều cấp** → lỗi rõ ràng / tên biến nối bằng `-`. Test: `test_extract_tokens_missing_block`, `test_tokens_to_css_nested` (Task 3).

---

## File Structure

```text
CLAUDE.md                                  # quy tắc chung (spec mục 2–4), mục "Quy ước" để conventions-init điền
.gitignore                                 # thêm các mẫu không commit
tools/
├── requirements.txt
├── skills/
│   ├── expected_skills.txt                # danh sách skill đã làm xong, mỗi dòng một tên
│   ├── validate_skills.py
│   └── test_validate_skills.py
└── ui/
    ├── gen_tokens.py                      # ui-style.md → ui-tokens.css
    ├── screenshot.py                      # chụp HTML → PNG
    ├── test_gen_tokens.py
    └── test_screenshot.py
.claude/
├── commands/phase-status.md
└── skills/<tên>/{SKILL.md, templates/, checklists/}
    acceptance-report/scripts/{export_report.py, test_export_report.py}
```

Script dùng chung (`gen_tokens.py`, `screenshot.py`) đặt ở `tools/ui/` thay vì trong một skill, vì nhiều skill cùng dùng.

---

### Task 1: Nền móng — validator, CLAUDE.md, gitignore

**Files:**
- Create: `tools/requirements.txt`, `tools/skills/validate_skills.py`, `tools/skills/test_validate_skills.py`, `tools/skills/expected_skills.txt` (rỗng), `CLAUDE.md`
- Modify: `.gitignore`

**Interfaces:**
- Produces:
  - `REQUIRED_SECTIONS: list[str]` (9 heading ở Global Constraints)
  - `read_text(path: Path) -> str` — đọc UTF-8, bỏ BOM, đổi CRLF → LF
  - `validate_skill(skill_dir: Path, repo_root: Path) -> list[str]` — trả danh sách lỗi
  - `validate_command(path: Path) -> list[str]`
  - `main(repo_root: Path) -> int` — kiểm tra mọi tên trong `expected_skills.txt` và `phase-status` nếu file command tồn tại; in từng lỗi dạng `<tên>: <lỗi>`; khi không lỗi in `<n> skill hợp lệ, <m> command hợp lệ`; trả 0/1
  - Chạy: `py tools/skills/validate_skills.py`

- [ ] **Step 1: Viết `tools/requirements.txt`**: `pytest`, `PyYAML`, `openpyxl`, `Pillow`, `Jinja2`, `Markdown`, `playwright`, mỗi gói ghim bản mới nhất lúc làm (`==`). Chạy `py -m pip install -r tools/requirements.txt` rồi `py -m playwright install chromium`.

- [ ] **Step 2: Viết test thất bại** trong `tools/skills/test_validate_skills.py`, dùng `tmp_path` tạo skill giả:
  - `test_valid_skill_has_no_errors`: skill đủ frontmatter + 9 heading đúng thứ tự → `[]`
  - `test_name_must_match_directory`: `name: other` → lỗi chứa `"name"`
  - `test_missing_section_reported`: thiếu `## Điểm dừng` → lỗi chứa `"## Điểm dừng"`
  - `test_sections_out_of_order_reported`: đổi chỗ 2 heading → lỗi chứa `"thứ tự"`
  - `test_description_too_long`: 1025 ký tự → lỗi chứa `"description"`
  - `test_referenced_template_must_exist`: nội dung nhắc `` `templates/x.md` `` mà không có file → lỗi chứa `"templates/x.md"`; đường dẫn bắt đầu bằng `.claude/`, `tools/` được kiểm tra tương đối với `repo_root`; đường dẫn `docs/...` không kiểm tra (là output, có thể chưa tồn tại)
  - `test_validate_skill_accepts_crlf_and_bom`: file lưu `﻿` + `\r\n` → `[]`
  - `test_command_requires_description`: command không có `description` → lỗi
  - `test_repo_skills_are_valid`: chạy `main(Path(repo_root))` trên repo thật → `0`

- [ ] **Step 3: Chạy** `py -m pytest tools/skills -q` → FAIL (`ModuleNotFoundError: validate_skills`).

- [ ] **Step 4: Viết `validate_skills.py`** theo Interfaces. Frontmatter parse bằng PyYAML giữa hai dòng `---`. Đường dẫn được nhắc tới = mọi chuỗi trong backtick khớp `^(templates|checklists|scripts)/\S+$` (tương đối với skill) hoặc `^(\.claude|tools)/\S+$` (tương đối với repo).

- [ ] **Step 5: Chạy** `py -m pytest tools/skills -q` → PASS.

- [ ] **Step 6: Viết `CLAUDE.md`** gồm các heading: `# Tiệm Nhà Mio – Business Operations Platform`, `## Ưu tiên skill`, `## Vòng đời`, `## Điểm dừng`, `## Ngôn ngữ và định dạng`, `## Mã định danh`, `## Ghi quyết định`, `## Dữ liệu thật và evidence`, `## Báo cáo kết thúc`, `## Cấu trúc tài liệu`, `## Quy ước` (để trống: "Chưa chốt. Chạy `/conventions-init`."). Nội dung lấy từ spec mục 2, sơ đồ mục 3, cây thư mục mục 4.

- [ ] **Step 7: Thêm vào `.gitignore`** 4 mẫu ở Global Constraints.

- [ ] **Step 8: Commit**
```bash
git add tools CLAUDE.md .gitignore
git commit -m "feat(process): add skill validator, CLAUDE.md rules, gitignore for evidence"
```

---

### Quy trình chung cho Task 2, 4–11 (task tạo skill)

Mỗi skill đi theo đúng 5 bước, task chỉ ghi phần riêng:
1. Thêm tên skill vào `tools/skills/expected_skills.txt`.
2. Chạy `py tools/skills/validate_skills.py` → FAIL (`skill thiếu: <tên>`).
3. Viết `SKILL.md` theo khung + `templates/` + `checklists/` như task mô tả. Nội dung lấy từ spec mục được trỏ tới, không chép lại spec mà viết thành hướng dẫn hành động. Mỗi template có kèm một ví dụ đã điền (`templates/example-*.md`) dùng tính năng `group-settings`.
4. Chạy `py -m pytest tools .claude/skills -q` → PASS.
5. Commit `feat(skills): add <tên>` (một commit cho cả task được phép).

---

### Task 2: Nhóm khởi tạo — `conventions-init`, `test-viewpoints-init`

**Nguồn:** spec mục 5.1, 8.2, 9.

- `conventions-init`
  - `argument-hint: ""`. Điều kiện: `CLAUDE.md` mục `## Quy ước` còn "Chưa chốt" hoặc người dùng yêu cầu làm lại.
  - Các bước: đọc `docs/project/04-technical.md`, `poc/fb-post-crawler-poc` (nếu có) → đề xuất từng nhóm quy ước, mỗi nhóm 2–3 phương án kèm khuyến nghị → hỏi từng nhóm → ghi vào `## Quy ước`.
  - `templates/conventions-section.md`: heading cấp 3 `Cấu trúc thư mục code`, `Đặt tên`, `Nhánh và commit`, `Lint, format, typecheck`, `Test tự động` (gồm các mục spec mục 9).
  - Gọi `decision-log` cho mỗi nhóm có chọn phương án.
- `test-viewpoints-init`
  - Output `docs/testing/viewpoints.md` theo `templates/viewpoints.md`: 12 khía cạnh spec mục 8.2, mỗi khía cạnh có `Câu hỏi gợi ý` và `Ví dụ` (lấy từ nhóm thao tác spec mục 8.4).
  - `## Cập nhật status.md`: "Không áp dụng."

---

### Task 3: Script UI — `gen_tokens.py`, `screenshot.py`

**Files:**
- Create: `tools/ui/gen_tokens.py`, `tools/ui/test_gen_tokens.py`, `tools/ui/screenshot.py`, `tools/ui/test_screenshot.py`

**Interfaces:**
- Produces:
  - `extract_tokens(md_text: str) -> dict` — lấy khối ```` ```yaml ```` đầu tiên nằm dưới heading `## Tokens`
  - `tokens_to_css(tokens: dict) -> str` — `:root { --<khóa-nối-bằng-gạch>: <giá trị>; }`, dòng đầu `/* File sinh tự động từ ui-style.md, không sửa tay. */`
  - CLI: `py tools/ui/gen_tokens.py <ui-style.md> <ui-tokens.css>`
  - `capture(html_files: list[Path], out_dir: Path, viewport: tuple[int, int] = (1440, 900)) -> list[Path]` — mở `file://`, chụp `full_page=True`, tên ảnh = tên file HTML đổi đuôi `.png`
  - CLI: `py tools/ui/screenshot.py <file-hoặc-thư-mục>... --out <thư-mục> [--viewport 1440x900]` (thư mục → mọi `*.html` trong đó)

- [ ] **Step 1: Viết test thất bại**
  - `test_tokens_to_css_nested`: `{"color": {"primary": "#8FA284", "surface": {"card": "#FAF7F0"}}}` → chứa `--color-primary: #8FA284;` và `--color-surface-card: #FAF7F0;`
  - `test_tokens_to_css_header`: dòng đầu đúng chuỗi ở Interfaces
  - `test_extract_tokens_reads_block_under_heading`: markdown có khối yaml khác trước `## Tokens` → chỉ lấy khối dưới `## Tokens`
  - `test_extract_tokens_missing_block`: không có → `ValueError` chứa `"## Tokens"`
  - `test_capture_uses_viewport_width` (cần Chromium): HTML đơn giản → PNG rộng 1440 (đọc bằng Pillow)
  - `test_capture_renders_vietnamese` : HTML chứa "Mẫu mới đón 20/10" → PNG tạo được, không lỗi

- [ ] **Step 2: Chạy** `py -m pytest tools/ui -q` → FAIL.
- [ ] **Step 3: Viết hai script** theo Interfaces (Playwright sync API).
- [ ] **Step 4: Chạy** `py -m pytest tools/ui -q` → PASS.
- [ ] **Step 5: Commit** `feat(process): add token generator and HTML screenshot tools`

---

### Task 4: Style UI — `ui-style-init`, `ui-style-update`

**Nguồn:** spec mục 5.1, 13 (lộ trình nền tảng).

- `ui-style-init`
  - `templates/ui-style.md`: heading `## Nguyên tắc`, `## Tokens` (một khối yaml: `color`, `font`, `font-size`, `line-height`, `space`, `radius`, `shadow`, `breakpoint`), `## Typography`, `## Bố cục và breakpoint`, `## Component cơ bản` (nút, ô nhập, thẻ, thông báo, badge — mỗi cái có biến thể và trạng thái), `## Trạng thái tương tác`, `## Khả năng truy cập`, `## Lịch sử thay đổi`.
  - Giá trị khởi đầu từ `docs/story/BusinessContext.md` mục 2: `#8FA284`, `#FAF7F0`, `#4E6045`, Playfair Display, Be Vietnam Pro (Dancing Script chỉ dùng trang trí, không dùng cho chữ giao diện).
  - `templates/ui-style-preview.html`: link `ui-tokens.css`, trưng bày mọi component cơ bản.
  - Các bước kết thúc bằng: `py tools/ui/gen_tokens.py docs/design/ui-style.md docs/design/ui-tokens.css` và `py tools/ui/screenshot.py docs/design/ui-style-preview.html --out docs/design/screenshots`.
- `ui-style-update`
  - `argument-hint: "<nội dung muốn đổi>"`. Điều kiện: đã có `docs/design/ui-style.md`.
  - Các bước: sửa `ui-style.md` + ghi `## Lịch sử thay đổi` → sinh lại token và preview → **điểm dừng** duyệt preview → đọc `docs/design/components/index.md` và `docs/design/ui/` để liệt kê component/màn hình bị ảnh hưởng → chụp lại ảnh → liệt kê test case có khía cạnh "hiển thị" của các màn hình đó.

---

### Task 5: Điều phối — `phase-kickoff`, `decision-log`, `/phase-status`

**Nguồn:** spec mục 3, 5.2, 5.5, 7.

- `phase-kickoff`
  - `argument-hint: "<số giai đoạn>"`. Điều kiện: `CLAUDE.md` `## Quy ước` đã chốt, `docs/design/ui-style.md` và `docs/testing/viewpoints.md` đã có.
  - `templates/status.md` (định dạng cố định, `/phase-status` và mọi skill đọc theo):
    - `# Giai đoạn N – <tên>`
    - `## Phạm vi`, `## Tiêu chí Xong khi`
    - `## Tính năng`: bảng cột `Slug | Mã | Có màn hình | Tài liệu liên quan | Trạng thái`
    - `## Vấn đề đang chặn`
    - `## Nhật ký duyệt`: dòng `- YYYY-MM-DD | <slug hoặc "giai đoạn"> | <bước> | <người duyệt>`
- `decision-log`
  - `argument-hint: "<tiêu đề>"`. Số `NNNN` = số lớn nhất trong `docs/decisions/` + 1.
  - `templates/adr.md`: `# NNNN – <tiêu đề>`, `- Ngày`, `- Trạng thái` (`đề xuất` | `chấp nhận` | `thay thế bởi NNNN`), `## Bối cảnh`, `## Các phương án`, `## Quyết định`, `## Hệ quả`.
  - Ghi rõ quy tắc khi nào ghi (spec mục 5.2).
- `.claude/commands/phase-status.md`
  - Frontmatter `description`, `argument-hint: "[số giai đoạn]"`. Không ghi file.
  - Mặc định: giai đoạn số lớn nhất trong `docs/phases/` chưa có dòng nghiệm thu trong `## Nhật ký duyệt`.
  - Đầu ra đúng các dòng spec mục 5.5, cuối cùng là `Lệnh nên chạy tiếp: ...`.
- Bổ sung vào validator: không cần (đã kiểm `phase-status` ở Task 1).

---

### Task 6: `detailed-design`

**Nguồn:** spec mục 3.1 bước 2, 5.2, 13.

- `argument-hint: "<slug tính năng>"`. Điều kiện: slug có trong `status.md`, trạng thái `chưa bắt đầu` hoặc `thiết kế chi tiết`.
- `templates/feature-design.md`: heading đúng các mục spec mục 5.2 (Tóm tắt, Module và interface, Thay đổi DB, API, Màn hình và quy tắc kiểm tra dữ liệu, Job và hàng đợi, Trạng thái và thuật toán, Tích hợp bên ngoài, Xử lý lỗi – log – bảo mật – phân quyền, Tham số cài đặt, Câu hỏi mở, Lịch sử thay đổi). Quy tắc kiểm tra dữ liệu viết thành danh sách có mã `R-<ABC>-nn` để test case và traceability trỏ tới.
- `templates/db-schema.md`: mỗi bảng một heading cấp 2, bảng cột `Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú`, mục Index, mục Quan hệ; đầu file có `## Quy ước chung` (UTC, `created_at`, `updated_at` từ `docs/project/03-data-model.md`).
- `templates/api-resource.md`: mỗi endpoint một heading `### <METHOD> <path>` với các mục cố định `Quyền`, `Request`, `Response`, `Mã lỗi`.
- Các bước có bước sinh `docs/design/api/openapi.yaml` từ mọi `api/*.md` (dòng đầu `# File sinh tự động từ docs/design/api/*.md, không sửa tay.`) rồi lint: `npx --yes @redocly/cli@<bản ghim> lint docs/design/api/openapi.yaml`. Ghim bản mới nhất lúc làm (`npm view @redocly/cli version`) và ghi thẳng số bản vào `SKILL.md`.
- Mã 3 chữ của tính năng: đặt ở đây nếu `status.md` chưa có, ghi vào cột `Mã`.
- Chuyển trạng thái: `thiết kế chi tiết` → (sau duyệt) `UI` nếu có màn hình, ngược lại `test case`.

---

### Task 7: `ui-design`, `component-design`

**Nguồn:** spec mục 3.1 bước 3, 5.2, Global Constraints (Web Component).

- `ui-design`
  - Output trong `docs/design/ui/<màn hình>/`: mỗi trạng thái một file `<trạng thái>.html` (`normal`, `empty`, `loading`, `validation-error`, `system-error`, `forbidden` — bỏ trạng thái không áp dụng và ghi lý do trong `notes.md`), `index.html` liên kết tới các trạng thái, `notes.md` (`templates/screen-notes.md`: luồng thao tác, component dùng, chỗ khác thiết kế chi tiết), `screenshots/`.
  - `templates/mockup-state.html`: khung 1440×900, link `../../ui-tokens.css`, `<script type="module" src="../../components/<tên>.js">`.
  - Bước tra component: phần giao diện xuất hiện ≥ 2 màn hình hoặc mang tính chung → gọi `component-design`.
  - Chụp: `py tools/ui/screenshot.py docs/design/ui/<màn hình> --out docs/design/ui/<màn hình>/screenshots`.
  - Nếu đổi trường/quy tắc → cập nhật ngược `feature-design` và ghi `## Lịch sử thay đổi`.
- `component-design`
  - `argument-hint: "<tên component, PascalCase>"`; file dùng kebab-case (`StatusBadge` → `status-badge`), thẻ custom element `mio-<kebab>`.
  - `templates/component.md` (mục spec 5.2, có `## Màn hình đang dùng`), `templates/component.js` (class kế thừa `HTMLElement`, đọc thuộc tính `variant`/`state`, style chỉ dùng biến từ `ui-tokens.css`), `templates/component-gallery.html` (mọi biến thể × trạng thái), `templates/components-index.md` (danh sách: tên, mô tả một dòng, link).
  - Bước đầu tiên luôn là đọc `docs/design/components/index.md`.

---

### Task 8: `test-case-design`, `design-review`

**Nguồn:** spec mục 5.2, 8.

- `test-case-design`
  - Điều kiện: trạng thái `test case`; đã có `docs/testing/viewpoints.md`.
  - `templates/test-cases.md`: đầu file liệt kê khía cạnh không áp dụng kèm lý do; mỗi case một heading `## P<N>-<ABC>-<nnn> <tiêu đề>` với các dòng cố định: `- Thiết kế:` (mã `R-…` hoặc mục), `- Khía cạnh:`, `- Kỹ thuật:`, `- Ưu tiên:` (`cao`|`trung bình`|`thấp`), `- Regression:` (`có`|`không`), `- Người thực hiện:` (`Claude`|`người`), `- Tiền điều kiện:`, `- Các bước:` (danh sách đánh số, mỗi bước `→ mong đợi`, bước cần evidence đánh dấu `[evidence]`).
  - `templates/traceability.md`: bảng `Quy tắc | Mô tả | Case`.
  - `checklists/test-case-design.md`: mọi `R-…` có case; mọi khía cạnh đã xét; mọi trạng thái có bước chuyển không hợp lệ; mọi tham số có giá trị biên dưới/trên.
- `design-review`
  - `checklists/design-review.md`: đúng các điểm spec mục 5.2, có dòng riêng cho từng lằn ranh đỏ trong `docs/project/01-overview.md` mục 5.
  - `templates/review.md`: mỗi điểm `### RV-nn` với `- Mức độ:` (`chặn`|`nên sửa`|`gợi ý`), `- Vị trí:`, `- Vấn đề:`, `- Đề xuất:`, `- Kết quả:`.
  - Sau duyệt: trạng thái `đã duyệt thiết kế`, ghi `## Nhật ký duyệt`.

---

### Task 9: Nhóm code — `implementation-plan`, `implement-task`, `tdd`, `code-review`

**Nguồn:** spec mục 5.3, 9.

- `implementation-plan`: `templates/plan.md`, mỗi task `### T<nn> <tiêu đề>` với `- Tính năng:`, `- Thiết kế:`, `- Phụ thuộc:`, `- File:`, `- Test tự động:`, `- Test case manual:`, `- Tiêu chí xong:`, `- Trạng thái:` (`chưa làm`|`đang làm`|`xong`).
- `implement-task`: điều kiện task phụ thuộc đều `xong`; tên nhánh theo `## Quy ước` trong `CLAUDE.md`; trước commit chạy lệnh test/typecheck/lint ghi trong `## Quy ước`; tự review bằng `.claude/skills/code-review/checklists/code-review.md`; đổi trạng thái tính năng `đang code` → `đã code` khi task cuối của tính năng xong.
- `tdd`: quy tắc đỏ → xanh → refactor; cấm code nghiệp vụ khi chưa có test thất bại; phải chạy và thấy test thất bại đúng lý do; quy ước spec mục 9 (đồng hồ truyền vào, property-based, DB thật trong Docker, `skip` phải có lý do in ra).
- `code-review`: `checklists/code-review.md` đúng các điểm spec mục 5.3; đầu ra mỗi vấn đề `- [mức độ] file:dòng — vấn đề — cách sửa`; merge chỉ khi người dùng đồng ý.

---

### Task 10: Xử lý vấn đề — `bug-fix`, `change-request`, `feedback`

**Nguồn:** spec mục 3.2, 5.3, 5.4.

- `feedback`
  - `templates/issues.md`: `# Sổ vấn đề – Giai đoạn N`, mỗi mục `## P<N>-ISS-<nnn> <tóm tắt>` với `- Ngày:`, `- Nguồn:` (`feedback`|`manual test <mã lần chạy>`), `- Tính năng:`, `- Phân loại:` (`bug`|`thiết kế chưa hợp lý`|`thiếu test case`|`câu hỏi`), `- Nội dung:`, `- Evidence:`, `- Trạng thái:` (`mở`|`đang xử lý`|`đã xong`|`không sửa`), `- Xử lý:`.
  - Điểm dừng: trình bày phân loại + hướng xử lý trước khi chuyển skill.
- `bug-fix`: `argument-hint: "<mã case | mã vấn đề | mô tả>"`; lỗi do thiết kế → dừng, chuyển `change-request`; kết thúc: case gắn `Regression: có`, mục `issues.md` sang `đã xong` kèm commit, `results.md` không sửa (test lại ghi lần chạy mới).
- `change-request`: `templates/impact.md` liệt kê theo đúng thứ tự cập nhật: `docs/project/` → thiết kế tính năng → `docs/design/` → test case + traceability → `plan.md` → code + test; điểm dừng trước khi sửa; lùi trạng thái tính năng về bước sớm nhất bị ảnh hưởng.

---

### Task 11: `manual-test-run`

**Nguồn:** spec mục 5.4, 8.6.

- `argument-hint: "<slug> | --retest <mã case> | --regression"`.
- `templates/results.md` (định dạng cố định, script Task 12 parse đúng định dạng này):
```markdown
# Kết quả chạy test 2026-11-10-01
- Môi trường: máy dev, http://localhost:3000
- Commit: abc1234
- Người chạy: Claude + Hải
- Ngày: 2026-11-10

## P0-GRP-012 Giới hạn comment/ngày = 51
- Kết quả: không đạt
- Thực tế: lưu được giá trị 51
- Evidence: P0-GRP-012_01_input.png, P0-GRP-012_02_saved.png
- Ghi chú:
- Vấn đề: P0-ISS-003
```
- Test lại / regression: tạo lần chạy mới, chỉ chứa các case chạy lại.
- Hướng dẫn chạy case `Claude`: Playwright (MCP hoặc script tạm) chụp vào `evidence/` đúng tên `<mã case>_<bước 2 chữ số>_<mô tả>.png`; case `người`: in từng bước, chờ người dùng gửi ảnh và kết quả, lưu ảnh vào `evidence/`.
- Case `không đạt` → thêm mục vào `issues.md` (định dạng Task 10) và điền `- Vấn đề:`.

---

### Task 12: `acceptance-report` + script xuất

**Files:**
- Create: `.claude/skills/acceptance-report/SKILL.md`, `templates/report.md`, `templates/report.html`, `scripts/export_report.py`, `scripts/test_export_report.py`

**Interfaces:**
- Consumes: định dạng `results.md` (Task 11), `issues.md` (Task 10), `status.md` (Task 5).
- Produces (`export_report.py`):
  - `@dataclass CaseResult(case_id: str, title: str, result: str, actual: str, evidence: list[str], note: str, issue: str | None)`
  - `@dataclass Run(run_id: str, environment: str, commit: str, tester: str, date: str, cases: list[CaseResult], dir: Path)`
  - `parse_results(path: Path) -> Run`
  - `collect_runs(phase_dir: Path) -> list[Run]` — sắp theo `run_id`
  - `latest_by_case(runs: list[Run]) -> dict[str, tuple[Run, CaseResult]]` — lần chạy sau thắng
  - `build_xlsx(phase_dir: Path, runs: list[Run], out: Path) -> list[str]` — trả cảnh báo
  - `build_pdf(phase_dir: Path, runs: list[Run], out: Path) -> list[str]`
  - `main(argv: list[str]) -> int` — CLI `py .claude/skills/acceptance-report/scripts/export_report.py docs/phases/phase-0`, ghi `acceptance/report.xlsx` và `acceptance/report.pdf`

- [ ] **Step 1: Viết test thất bại** (`tmp_path` dựng `phase-0/test/runs/...` và `acceptance/report.md`):
  - `test_parse_results_reads_header_and_cases`: ví dụ ở Task 11 → `run_id == "2026-11-10-01"`, `cases[0].evidence == ["P0-GRP-012_01_input.png", "P0-GRP-012_02_saved.png"]`, `issue == "P0-ISS-003"`
  - `test_parse_results_handles_crlf_and_bom`
  - `test_parse_results_normalizes_result`: `- Kết quả:  Đạt ` → `"đạt"`; dạng NFD → `"đạt"`
  - `test_parse_results_rejects_unknown_result`: `- Kết quả: ok` → `ValueError` chứa đường dẫn và `"dòng"`
  - `test_latest_by_case_prefers_later_run`: hai lần chạy cùng case → lấy `2026-11-11-01`
  - `test_build_xlsx_creates_sheets`: tên sheet `["Tổng hợp", "Danh sách case", "P0-GRP-012"]`; sheet case có 1 ảnh (`len(ws._images) == 1`); ảnh rộng hơn 900px được thu về 900px
  - `test_build_xlsx_missing_evidence_warns`: ảnh không tồn tại → cảnh báo chứa tên file; ô ghi `"Thiếu file evidence: <tên>"`
  - `test_build_pdf_writes_pdf` (cần Chromium): file bắt đầu bằng `b"%PDF"`
  - `test_build_pdf_missing_evidence_warns`
  - `test_main_reports_locked_output`: monkeypatch `Workbook.save` ném `PermissionError` → `main` trả `1`, stderr chứa `"Đóng file"`

- [ ] **Step 2: Chạy** `py -m pytest .claude/skills/acceptance-report -q` → FAIL.

- [ ] **Step 3: Viết `export_report.py`** theo Interfaces.
  - Sheet "Tổng hợp": số case theo từng kết quả, theo từng mã tính năng (`P0-GRP`), số vấn đề còn mở đọc từ `issues.md` (đếm `- Trạng thái: mở` và `đang xử lý`).
  - Sheet "Danh sách case": cột `Mã | Tiêu đề | Kết quả | Lần chạy | Vấn đề | Ghi chú` từ `latest_by_case`.
  - PDF: Jinja2 render `templates/report.html` với nội dung `report.md` (qua thư viện Markdown) + mỗi case một mục kèm ảnh (`Path.as_uri()`), rồi `page.pdf(format="A4", print_background=True)`.

- [ ] **Step 4: Chạy** `py -m pytest .claude/skills/acceptance-report -q` → PASS.

- [ ] **Step 5: Viết `SKILL.md`, `templates/report.md`** (`# Báo cáo nghiệm thu – Giai đoạn N`, `## Tổng quan`, `## Tiêu chí Xong khi` (từng tiêu chí: đạt/chưa + bằng chứng), `## Thống kê test case`, `## Vấn đề còn mở`, `## Số liệu chạy thật`, `## Ký nghiệm thu`), `templates/report.html` (font Be Vietnam Pro qua Google Fonts, dự phòng sans-serif). Các bước: viết `report.md` → chạy script → in cảnh báo → điểm dừng ký nghiệm thu → ghi `## Nhật ký duyệt`.

- [ ] **Step 6: Thêm `acceptance-report` vào `expected_skills.txt`, chạy** `py -m pytest tools .claude/skills -q` → PASS.

- [ ] **Step 7: Commit** `feat(skills): add acceptance-report with Excel/PDF export`

---

### Task 13: Kiểm tra cuối

- [ ] **Step 1:** `expected_skills.txt` có đủ 20 tên ở Global Constraints. Chạy `py tools/skills/validate_skills.py` → in `20 skill hợp lệ, 1 command hợp lệ`, mã thoát 0.
- [ ] **Step 2:** `py -m pytest tools .claude/skills -q` → PASS toàn bộ, không có test bị skip không lý do.
- [ ] **Step 3:** Chạy thử xuất báo cáo với dữ liệu mẫu trong `templates/example-*` của `manual-test-run` (chép vào thư mục tạm ngoài repo) → mở `report.xlsx` bằng Excel và `report.pdf`, xác nhận ảnh và chữ tiếng Việt hiển thị đúng.
- [ ] **Step 4:** Grep `superpowers` trong `.claude/` → không có kết quả.
- [ ] **Step 5:** Cập nhật spec mục 11: ghi rằng bước chạy thử thật (`group-settings`) sẽ thực hiện ở đầu Giai đoạn 0. Commit `docs(process): mark skills ready for phase-0 pilot`.
