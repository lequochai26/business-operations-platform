# Reader View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sinh bản cho người đọc (Markdown + HTML) từ tài liệu do skill sinh ra, giữ nguyên bản gốc, có kiểm tra độ trung thực và cảnh báo bản cũ.

**Architecture:** Gói Python `tools/reader/` gồm các module nhỏ (chia mục, bảng mã, viết tắt, kiểm tra trung thực, chèn ý nghĩa, HTML) và một CLI `todo | build | stale`. AI chỉ viết lại các mục được CLI đánh dấu TODO trong `docs/reader/_rewrite/`; mọi bước còn lại do script làm. Skill mới `reader-view` điều phối; 18 skill có ghi tài liệu gọi nó trước điểm dừng.

**Tech Stack:** Python 3.15 (`py`), pytest, Markdown 3.11 (đã có trong `tools/requirements.txt`); không thêm thư viện mới.

**Spec:** `docs/process/2026-10-31-reader-view-design.md`

## Global Constraints

- Bản gốc không bị sửa bởi bất kỳ bước nào. Không skill nào đọc bản đọc làm input.
- Phạm vi bản gốc: mọi `.md` trong `docs/phases/`, `docs/design/`, `docs/decisions/`, `docs/testing/`. Không gồm `docs/reader/` và mọi thư mục khác.
- Đường dẫn: bản đọc `docs/reader/<đường dẫn tương đối so với docs/>`; bản viết lại `docs/reader/_rewrite/<cùng đường dẫn>`; HTML `docs/reader/html/<cùng đường dẫn, đuôi .html>`.
- Dòng đầu bản đọc, đúng mẫu: `> Bản đọc sinh từ <đường dẫn gốc> (phiên bản <hash 7 ký tự>, <YYYY-MM-DD HH:MM>). Không sửa tay.`
- Marker mục trong bản viết lại: `<!-- src-section: <key> <hash> -->`; mục chờ viết lại có thêm dòng `<!-- TODO: viết lại mục này -->`.
- Ý nghĩa ngắn: bỏ đoạn trong ngoặc đơn, cắt ở ký tự đầu tiên trong `→ : ; . ,`, tối đa 60 ký tự (dài hơn thì cắt và thêm `…`).
- Chèn ý nghĩa dạng `[<mã>](<link> "<ý nghĩa>") *(<ý nghĩa>)*`, mỗi mã một lần trên một dòng.
- Fidelity tối đa 3 vòng sửa trong skill `reader-view`.
- Mọi file đọc/ghi `encoding="utf-8"`, chấp nhận BOM và CRLF, so sánh sau chuẩn hóa NFC.
- Chạy test: `py -m pytest tools .claude/skills -q`. Kiểm tra skill: `py tools/skills/validate_skills.py`.
- Commit theo `CLAUDE.md` mục Quy ước (Conventional Commits, scope `process`/`skills`), không có dòng `Co-Authored-By` hay dấu vết Claude.
- Làm trong git worktree nhánh `process/reader-view` (Task 0). Không đụng thư mục làm việc trên `main`.

## Review Focus

- **Bản gốc bị sửa giữa lúc `todo` và `build`** → `build` phát hiện hash mục trong marker khác hash hiện tại, từ chối và nhắc chạy lại `todo`. Test: `test_build_rejects_outdated_rewrite` (Task 7).
- **Một file có hai heading trùng chữ** (ví dụ `### Quy tắc` dưới hai mục `##` khác nhau) → hai mục có key khác nhau, không lẫn nội dung. Test: `test_split_sections_duplicate_headings_get_distinct_keys` (Task 1).
- **Mã được nhắc nhưng không có định nghĩa** (gõ nhầm, mã giai đoạn khác) → để nguyên, không chèn ý nghĩa, in cảnh báo, không crash. Test: `test_expand_unknown_id_left_plain_with_warning` (Task 5).
- **Bản gốc lưu CRLF hoặc có BOM** → hash giống hệt bản LF, không bị coi là đã đổi. Test: `test_section_hash_ignores_crlf_and_bom` (Task 1).
- **AI làm mất hoặc sửa marker trong bản viết lại** → lỗi nêu tên file và số dòng, không âm thầm mất mục. Test: `test_parse_rewrite_rejects_text_before_first_marker`, `test_parse_rewrite_rejects_malformed_marker` (Task 1).

---

## File Structure

```text
tools/reader/
├── __init__.py
├── paths.py         # phạm vi bản gốc, ánh xạ gốc ↔ bản đọc ↔ rewrite ↔ html
├── text.py          # đọc file, chuẩn hóa (NFC, LF, bỏ BOM), hash
├── sections.py      # chia mục theo heading, key, hash
├── rewrite.py       # định dạng _rewrite: parse, đồng bộ với bản gốc, ghi
├── ids.py           # nhận diện mã, bảng mã → ý nghĩa, phân giải phạm vi
├── abbrev.py        # viết tắt (kể cả có tham số): đọc định nghĩa, triển khai
├── fidelity.py      # kiểm tra độ trung thực
├── expand.py        # sinh bản đọc Markdown, dòng đầu, phát hiện bản cũ
├── html.py          # sinh HTML
├── cli.py           # py tools/reader/cli.py todo|build|stale
└── test_*.py        # một file test cho mỗi module
docs/process/writing-guide.md
.claude/skills/reader-view/SKILL.md
```

---

### Task 0: Worktree và đưa spec vào nhánh

- [ ] **Step 1:** Dùng `superpowers:using-git-worktrees` tạo worktree nhánh `process/reader-view` từ `main` (commit `ee54ce6` trở đi).
- [ ] **Step 2:** Chép vào worktree 3 file chưa được commit trên `main`: `docs/process/2026-10-31-reader-view-design.md`, `docs/process/2026-10-31-reader-view-plan.md`, `docs/process/skills-usage-guide.md`.
- [ ] **Step 3:** Commit: `docs(process): add reader view design, plan and skills usage guide`.

---

### Task 1: Đọc file, chia mục, định dạng bản viết lại

**Files:** Create `tools/reader/__init__.py`, `paths.py`, `text.py`, `sections.py`, `rewrite.py`, `test_sections.py`, `test_rewrite.py`, `test_paths.py`

**Interfaces — Produces:**
- `paths.py`: `DOCS_ROOT_NAME = "docs"`; `SOURCE_DIRS = ("phases", "design", "decisions", "testing")`; `source_files(docs_root: Path) -> list[Path]`; `reader_path(docs_root, src) -> Path`; `rewrite_path(docs_root, src) -> Path`; `html_path(docs_root, reader_md) -> Path`; `select_sources(docs_root, targets: list[str]) -> list[Path]` (`all`, `phase-N`, hoặc đường dẫn file).
- `text.py`: `read_text(path) -> str` (bỏ BOM, CRLF → LF, NFC); `normalize(s: str) -> str` (NFC, gộp khoảng trắng); `short_hash(s: str, n: int = 12) -> str` (sha256 hex).
- `sections.py`: `@dataclass Section(key: str, heading: str, level: int, body: str, hash: str)`; `split_sections(text: str) -> list[Section]`. Chia ở heading cấp 2 và 3; phần trước heading đầu là mục `heading=""`, `level=0`. `key = short_hash(<chuỗi heading cha › heading con> + "#" + <lần xuất hiện thứ mấy>, 10)`; `hash = short_hash(normalize(heading + body))`.
- `rewrite.py`: `TODO_MARK = "<!-- TODO: viết lại mục này -->"`; `@dataclass Block(key: str, src_hash: str, body: str)`, `is_todo` = `TODO_MARK in body`; `parse_rewrite(text: str, path: Path) -> list[Block]`; `format_rewrite(blocks) -> str`; `sync_rewrite(sections: list[Section], blocks: list[Block]) -> tuple[list[Block], list[Section]]` (giữ khối có cùng key và hash; mục mới/đổi thành khối TODO chứa nguyên văn mục gốc; bỏ khối của mục đã xóa; giữ thứ tự bản gốc; trả về danh sách mục cần viết lại).

- [ ] **Step 1: Viết test**
  - `test_split_sections_levels`: văn bản có `# Tiêu đề`, `## A`, `### A1`, `## B` → heading `["", "A", "A1", "B"]`, `#` cấp 1 thuộc mục đầu.
  - `test_split_sections_duplicate_headings_get_distinct_keys`: `## A` / `### Quy tắc` / `## B` / `### Quy tắc` → hai mục "Quy tắc" có key khác nhau; key ổn định giữa hai lần chạy.
  - `test_section_hash_ignores_crlf_and_bom`: cùng nội dung, một bản `﻿` + `\r\n` → mọi `hash` bằng nhau.
  - `test_section_hash_changes_when_body_changes`.
  - `test_sync_keeps_unchanged_block_and_todos_changed`: 3 mục, sửa mục 2, thêm mục 4, xóa mục 3 → khối 1 giữ nguyên body đã viết lại; khối 2 và 4 có `TODO_MARK` và chứa nguyên văn mục gốc; không còn khối 3; danh sách trả về là mục 2 và 4.
  - `test_format_parse_roundtrip`.
  - `test_parse_rewrite_rejects_text_before_first_marker`: `ValueError` chứa tên file và `"dòng 1"`.
  - `test_parse_rewrite_rejects_malformed_marker`: dòng `<!-- src-section: abc -->` (thiếu hash) ở dòng 5 → `ValueError` chứa tên file và `"dòng 5"`.
  - `test_sync_drops_block_with_unknown_key`: khối có key không còn trong bản gốc (mục đã xóa) → bị bỏ, không lỗi.
  - `test_select_sources_phase_and_all`, `test_reader_and_rewrite_paths`.
- [ ] **Step 2:** `py -m pytest tools/reader -q` → FAIL (thiếu module).
- [ ] **Step 3:** Viết các module theo Interfaces.
- [ ] **Step 4:** `py -m pytest tools/reader -q` → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader sections and rewrite format`.

---

### Task 2: Bảng mã

**Files:** Create `tools/reader/ids.py`, `test_ids.py`

**Interfaces — Consumes:** `sections.split_sections`, `text.read_text`. **Produces:**
- `@dataclass Ref(id: str, start: int, end: int)`; `find_refs(line: str) -> list[Ref]` — bỏ qua phần trong `code`; khoảng `R-AUT-01 … R-AUT-04` (hoặc `...`) trả về một `Ref` có `id="R-AUT-01..R-AUT-04"`.
- `expand_range(id: str) -> list[str]`.
- `short_gloss(text: str) -> str` theo Global Constraints.
- `@dataclass Definition(id: str, gloss: str, source: Path, section_key: str)`.
- `class Index`: `build(docs_root: Path, sources: list[Path]) -> Index`; `resolve(id: str, from_source: Path) -> Definition | None`; `warnings: list[str]`.

Mẫu nhận diện:
- quy tắc `R-[A-Z]{3}-\d{2}`, định nghĩa ở dòng `- R-XXX-nn: <text>`;
- case/vấn đề `P\d-[A-Z]{3}-\d{3}`, định nghĩa ở heading `## <mã> <tiêu đề>`;
- task `T\d{2}` (không dính chữ/gạch hai bên), định nghĩa ở heading `### T<nn> <tiêu đề>` trong `phases/phase-N/plan.md`; phạm vi: cùng thư mục `phase-N`;
- `RV-\d{2}` định nghĩa ở heading `### RV-nn <tiêu đề>`; `câu hỏi mở <n>` (không phân biệt hoa thường) định nghĩa ở dòng `- [x] <n>. <text>` hoặc `- [ ] <n>. <text>` trong mục `## Câu hỏi mở`; phạm vi: cùng file → `phases/phase-N/design/<slug>.md` → `phases/phase-N/design/reviews/<slug>-review.md`, với `slug` là tên file bỏ hậu tố `-review`;
- `ADR \d{4}`, định nghĩa là heading cấp 1 của `docs/decisions/<NNNN>-*.md` (phần sau `–`).

- [ ] **Step 1: Viết test**
  - `test_short_gloss_examples`: `"Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên…):"` → `"Giới hạn đăng nhập sai"`; `"Chưa đăng nhập (`GET /api/v1/sessions/current` trả 401) mà mở trang cần đăng nhập → chuyển …"` → `"Chưa đăng nhập mà mở trang cần đăng nhập"`; `"Tên đăng nhập được chuẩn hóa (bỏ khoảng trắng hai đầu, đổi chữ thường) trước khi tra cứu"` → `"Tên đăng nhập được chuẩn hóa"`; `"Hết hạn trượt: phiên …"` → `"Hết hạn trượt"`; chuỗi 80 ký tự không dấu cắt → 60 ký tự kết thúc bằng `…`.
  - `test_find_refs_skips_code_and_detects_range`.
  - `test_index_rule_case_issue_adr`: cây `docs/` tạm có design, test cases, issues, ADR → `resolve` trả đúng `gloss` và `source`.
  - `test_task_ids_scoped_to_phase`: `T06` ở phase-0 và phase-1 khác nghĩa; tham chiếu từ file phase-1 trả định nghĩa phase-1.
  - `test_open_question_resolves_to_design_of_same_slug`: `test/cases/auth.md` nhắc "câu hỏi mở 7" → định nghĩa trong `design/auth.md`, gloss `"Nhiều request sai gửi đồng thời"` (định nghĩa mẫu: `- [x] 7. (phát hiện ở `/test-case-design`, P0-AUT-023) Nhiều request sai gửi đồng thời: …`).
  - `test_rv_resolves_to_review_file`.
  - `test_duplicate_definition_warns`.
- [ ] **Step 2:** chạy test → FAIL. **Step 3:** viết `ids.py`. **Step 4:** chạy test → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader id index`.

---

### Task 3: Viết tắt

**Files:** Create `tools/reader/abbrev.py`, `test_abbrev.py`

**Interfaces — Produces:**
- `@dataclass Abbrev(name: str, pattern: re.Pattern, template: str, line: int)`.
- `parse_abbreviations(text: str) -> list[Abbrev]` — đọc mọi cặp `` `<lhs>` = `<rhs>` `` trên các dòng danh sách (nhiều cặp trên một dòng, ngăn bằng `;`). `lhs` bắt đầu bằng `<tên>`; phần còn lại của `lhs` có thể chứa tham số `<x>`, biến thành nhóm bắt `(.+?)` (phần chữ khác được escape).
- `definition_lines(text: str) -> set[int]` — số dòng chứa định nghĩa viết tắt.
- `expand_abbreviations(text: str, abbrevs: list[Abbrev]) -> str` — thay cả trong `code`; lặp tới khi không đổi, tối đa 5 lần (viết tắt lồng nhau).

- [ ] **Step 1: Viết test**
  - `test_simple_abbreviation`: `` - `<api>` = `http://127.0.0.1:3000/api/v1`; `` → `` `<api>/sessions` `` thành `` `http://127.0.0.1:3000/api/v1/sessions` ``.
  - `test_parametric_abbreviation`: định nghĩa `` `<psql> "<sql>"` = `docker compose exec -T postgres psql -U mio -d mio -c "<sql>"` ``; `` `<psql> "delete from user_sessions"` `` → `` `docker compose exec -T postgres psql -U mio -d mio -c "delete from user_sessions"` ``.
  - `test_nested_abbreviation`: `<đăng nhập mio>` dùng `<origin>` và `<api>` → triển khai hết.
  - `test_two_definitions_on_one_line`: `` `<origin>` = `-H 'Origin: http://localhost:3000'`; `<json>` = `-H 'Content-Type: application/json'` ``.
  - `test_unknown_abbreviation_left_as_is`.
  - `test_definition_lines`.
- [ ] **Step 2–4:** FAIL → viết `abbrev.py` → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader abbreviation expansion`.

---

### Task 4: Kiểm tra độ trung thực

**Files:** Create `tools/reader/fidelity.py`, `test_fidelity.py`

**Interfaces — Consumes:** `Section`, `Block`, `ids.find_refs`, `abbrev.definition_lines`. **Produces:**
- `extract_items(text: str) -> set[str]` — mã (khoảng mã được triển khai), con số (`\d+(?:[.,]\d+)*` không nằm trong mã hoặc `code`), chuỗi trong `"…"` và `“…”`, nội dung `code`, URL `https?://\S+` và đường dẫn file có đuôi `md|ts|tsx|py|json|ya?ml|sql|html|css|js`; mọi phần tử qua `normalize`.
- `check(src_path: Path, src_text: str, sections: list[Section], blocks: list[Block]) -> list[str]` — với mỗi mục: phần tử của mục gốc (bỏ các dòng định nghĩa viết tắt) phải có trong khối viết lại cùng key; trả về thông báo theo mẫu spec mục 5.4: dòng tiêu đề `<đường dẫn> – bản đọc thiếu <n> mục so với bản gốc:` và mỗi dòng `- <loại> "<giá trị>" (mục <heading>)`, loại ∈ `mã`, `con số`, `chuỗi`, `code`, `đường dẫn`.

- [ ] **Step 1: Viết test**
  - `test_extract_items_kinds`.
  - `test_check_passes_when_rewrite_keeps_items`: dùng mục R-AUT-06 ở spec mục 3 làm bản gốc và bản đọc ví dụ trong spec làm bản viết lại (đã bỏ phần chèn) → `[]`.
  - `test_check_reports_missing_number_and_string`: bỏ `128` và câu "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." → thông báo chứa đúng hai dòng `- con số "128"` và `- chuỗi "Nhập sai…"`.
  - `test_check_ignores_whitespace_and_nfd`.
  - `test_check_ignores_abbreviation_definition_lines`: mục định nghĩa `<api>` mà bản viết lại bỏ danh sách viết tắt → `[]`.
- [ ] **Step 2–4:** FAIL → viết → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader fidelity check`.

---

### Task 5: Sinh bản đọc Markdown và phát hiện bản cũ

**Files:** Create `tools/reader/expand.py`, `test_expand.py`

**Interfaces — Consumes:** `Index`, `Block`, `abbrev`, `paths`. **Produces:**
- `header_line(src_rel: str, src_hash: str, now: datetime) -> str` — đúng mẫu Global Constraints, hash 7 ký tự đầu của `short_hash(read_text(src))`.
- `render_reader(docs_root: Path, src: Path, blocks: list[Block], index: Index, now: datetime) -> tuple[str, list[str]]` — mỗi khối mở đầu bằng `<a id="s-<key>"></a>`; triển khai viết tắt của chính file gốc; chèn ý nghĩa theo Global Constraints (link là đường dẫn tương đối tới bản đọc chứa định nghĩa + `#s-<section_key>`; khoảng mã thành danh sách từng mã có ý nghĩa, ngăn bằng dấu phẩy); "mục <X>" khớp (không phân biệt hoa thường) với heading trong cùng file thành link `#s-<key>`; bỏ qua dòng heading và nội dung `code`; trả về văn bản và cảnh báo (mã không có định nghĩa).
- `parse_header(text: str) -> tuple[str, str] | None` — (đường dẫn gốc, hash).
- `stale_reports(docs_root: Path, sources: list[Path]) -> list[str]` — mỗi dòng `<đường dẫn gốc>: <lý do>`, lý do ∈ `chưa có bản đọc`, `bản gốc đã đổi`, `còn mục chưa viết lại`.

- [ ] **Step 1: Viết test**
  - `test_header_line_format`: `header_line("docs/phases/phase-0/design/auth.md", "a3f9c21…", datetime(2026, 10, 31, 14, 20))` == `"> Bản đọc sinh từ docs/phases/phase-0/design/auth.md (phiên bản a3f9c21, 2026-10-31 14:20). Không sửa tay."`.
  - `test_render_inserts_gloss_once_per_line`: dòng nhắc `R-AUT-07` hai lần → chỉ lần đầu có `*(Tên đăng nhập được chuẩn hóa)*`, link có title.
  - `test_render_expands_range`.
  - `test_render_skips_headings_and_code`.
  - `test_render_links_section_reference`.
  - `test_render_expands_abbreviations`.
  - `test_expand_unknown_id_left_plain_with_warning`.
  - `test_stale_reports_three_reasons`.
- [ ] **Step 2–4:** FAIL → viết → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader markdown rendering and stale check`.

---

### Task 6: HTML

**Files:** Create `tools/reader/html.py`, `test_html.py`

**Interfaces — Produces:** `render_site(docs_root: Path, stale: list[str]) -> list[Path]` — với mọi `docs/reader/**/*.md` (trừ `_rewrite/`, `html/`): Markdown → HTML (extension `tables`, `fenced_code`); bỏ `<em>(<ý nghĩa>)</em>` đứng ngay sau thẻ `<a … title="<ý nghĩa>">` (tooltip đã đủ); đổi link `.md` thành `.html`; bản cũ có `<div class="stale">Bản đọc này đã cũ so với bản gốc. Chạy /reader-view để sinh lại.</div>` đầu trang; link `ui-tokens.css` bằng đường dẫn tương đối tới `docs/design/ui-tokens.css`; sinh `docs/reader/html/index.html` liệt kê mọi trang theo thư mục. Trả về danh sách file đã ghi.

- [ ] **Step 1: Viết test**: `test_html_tooltip_replaces_inline_gloss`, `test_html_links_point_to_html`, `test_html_stale_banner`, `test_html_index_lists_pages`.
- [ ] **Step 2–4:** FAIL → viết → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader html rendering`.

---

### Task 7: CLI

**Files:** Create `tools/reader/cli.py`, `test_cli.py`

**Interfaces — Consumes:** mọi module trên. **Produces:** `main(argv: list[str], docs_root: Path, now: datetime) -> int`; chạy bằng `py tools/reader/cli.py <lệnh> [<mục tiêu>…]` (tự thêm `tools/` vào `sys.path`, `docs_root` = `docs/` của repo, `now` = giờ máy).
- `todo <mục tiêu>…` — với mỗi bản gốc: `sync_rewrite`, ghi `_rewrite`; in `<đường dẫn>: <n> mục cần viết lại` và từng heading. Mã thoát 0.
- `build [<mục tiêu>…]` (mặc định `all`):
  1. với bản gốc được chọn: lỗi nếu còn khối TODO (`<đường dẫn>: còn <n> mục chưa viết lại`) hoặc hash marker khác hash mục hiện tại (`<đường dẫn>: bản gốc đã đổi sau lần chạy todo, chạy lại todo`);
  2. chạy `fidelity.check`; có thiếu thì in và thoát 1;
  3. `render_reader` cho **mọi** bản gốc có `_rewrite` không còn TODO; in cảnh báo;
  4. `render_site`; in đường dẫn bản đọc `.md` và `.html` của các file được chọn. Thoát 0.
- `stale [<mục tiêu>…]` — in `stale_reports`, hoặc `Mọi bản đọc đều mới`. Thoát 0.

- [ ] **Step 1: Viết test** (cây `docs/` tạm với một design và một test case):
  - `test_todo_creates_rewrite_with_todos`;
  - `test_build_fails_while_todo_remains`;
  - `test_build_rejects_outdated_rewrite`: chạy `todo`, thay mọi TODO bằng nguyên văn, sửa bản gốc, chạy `build` → thoát 1, thông báo chứa `chạy lại todo`;
  - `test_build_reports_fidelity_and_exits_1`;
  - `test_build_success_writes_reader_and_html`: dòng đầu đúng mẫu, có `*(` gloss, có file `.html`;
  - `test_stale_after_source_change`.
- [ ] **Step 2–4:** FAIL → viết → PASS.
- [ ] **Step 5:** Commit `feat(process): add reader cli`.

---

### Task 8: Skill `reader-view` và hướng dẫn viết

**Files:** Create `.claude/skills/reader-view/SKILL.md`, `docs/process/writing-guide.md`; Modify `tools/skills/expected_skills.txt`

- [ ] **Step 1:** Thêm `reader-view` vào `expected_skills.txt`; `py tools/skills/validate_skills.py` → FAIL (`reader-view: thiếu SKILL.md`).
- [ ] **Step 2:** Viết `docs/process/writing-guide.md` từ spec mục 4, thêm 3 quy tắc cho bản viết lại:
  - giữ nguyên mọi marker `<!-- src-section: … -->`, chỉ thay phần thân và xóa dòng TODO;
  - giữ nguyên viết tắt (`<api>`, `<psql> "…"`), không viết lại danh sách định nghĩa viết tắt (script triển khai);
  - viết con số bằng chữ số.
- [ ] **Step 3:** Viết `reader-view/SKILL.md` đủ 9 heading; `argument-hint: "<file>… | phase-N | all"`; các bước đúng spec mục 6, dùng `py tools/reader/cli.py todo …`, viết lại khối TODO theo `docs/process/writing-guide.md`, kiểm tra câu chữ theo skill `vietnamese-tech-writing`, `py tools/reader/cli.py build …`, sửa tối đa 3 vòng khi `build` báo thiếu; `## Cập nhật status.md`: không áp dụng.
- [ ] **Step 4:** `py tools/skills/validate_skills.py` → `21 skill hợp lệ, 1 command hợp lệ`; `py -m pytest tools .claude/skills -q` → PASS.
- [ ] **Step 5:** Commit `feat(skills): add reader-view skill and writing guide`.

---

### Task 9: Tích hợp vào bộ skill và tài liệu

**Files:** Modify `tools/skills/validate_skills.py`, `tools/skills/test_validate_skills.py`, 18 `SKILL.md` ở spec mục 7, `.claude/commands/phase-status.md`, `CLAUDE.md`, `docs/process/skills-usage-guide.md`, `.gitignore`

**Interfaces — Produces:** trong `validate_skills.py`: `READER_SKILLS: tuple[str, ...]` = 18 skill ở spec mục 7; `validate_skill` báo lỗi `"thiếu bước gọi reader-view"` nếu tên skill thuộc `READER_SKILLS` mà nội dung không chứa `reader-view`.

- [ ] **Step 0a:** Viết test `test_reader_skill_must_mention_reader_view`, `test_other_skill_does_not_need_reader_view`; chạy → FAIL.
- [ ] **Step 0b:** Thêm `READER_SKILLS` và kiểm tra; `py tools/skills/validate_skills.py` → lỗi `thiếu bước gọi reader-view` cho đúng 18 skill.
- [ ] **Step 1:** Mỗi skill trong `READER_SKILLS`:
  - dòng đầu mục `## Điểm dừng`: `Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi \`reader-view\` cho các file trong \`docs/\` vừa ghi, gửi kèm link bản đọc Markdown và HTML.`;
  - mục `## Báo cáo kết thúc` thêm gạch đầu dòng: `- Link bản đọc của các file vừa ghi.`
- [ ] **Step 2:** `phase-status.md`: thêm dòng `- Bản đọc đã cũ: <danh sách> | không có` vào khối kết quả, lấy từ `py tools/reader/cli.py stale phase-N`.
- [ ] **Step 3:** `CLAUDE.md` thêm mục `## Bản đọc` (sau `## Báo cáo kết thúc`): bản đọc ở `docs/reader/`, sinh bằng `reader-view`, không sửa tay, không dùng làm input của skill nào.
- [ ] **Step 4:** `skills-usage-guide.md` thêm mục "Đọc tài liệu qua bản đọc": vị trí Markdown và HTML (`docs/reader/html/index.html`), ý nghĩa phần nghiêng trong ngoặc, cảnh báo bản cũ, lệnh `/reader-view`.
- [ ] **Step 5:** `.gitignore` thêm `docs/reader/html/`.
- [ ] **Step 6:** `py tools/skills/validate_skills.py` → `21 skill hợp lệ, 1 command hợp lệ`; `py -m pytest tools .claude/skills -q` → PASS.
- [ ] **Step 7:** Commit `feat(skills): call reader-view before every stop point`.

---

### Task 10: Kiểm tra cuối

- [ ] **Step 1:** Chép `docs/phases/phase-0/design/auth.md` và `docs/phases/phase-0/test/cases/auth.md` từ thư mục làm việc `main` vào một cây `docs/` tạm ngoài repo; chạy `todo`, viết lại 2 mục (R-AUT-06 và P0-AUT-001) theo ví dụ spec mục 3, chép nguyên văn các mục còn lại; chạy `build` → thoát 0; mở HTML, xác nhận tooltip và link.
- [ ] **Step 2:** `py -m pytest tools .claude/skills -q` → PASS, không skip.
- [ ] **Step 3:** Ghi vào spec mục 8: sau khi merge, chạy `/reader-view all` trên `main`. Commit `docs(process): mark reader view ready`.
