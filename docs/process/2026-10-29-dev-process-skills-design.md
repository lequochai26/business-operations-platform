# Thiết kế quy trình phát triển và bộ skill Claude Code

- **Ngày:** 29/10/2026
- **Phạm vi:** quy trình phát triển hệ thống Tiệm Nhà Mio (`docs/project/`), hiện thực bằng bộ skill Claude Code riêng của dự án
- **Trạng thái:** chờ review

---

## Tóm tắt

- Mọi việc phát triển đi theo **một vòng đời cố định cho từng giai đoạn** của roadmap: mở giai đoạn → thiết kế chi tiết → thiết kế UI → thiết kế test case → review → lập kế hoạch → code (TDD) → manual test có evidence → nghiệm thu.
- Mỗi bước là **một skill** trong `.claude/skills/`, gọi bằng slash command (ví dụ `/detailed-design group-settings`). Skill tự đọc input theo quy ước thư mục, ghi output theo mẫu, dừng chờ duyệt ở các điểm quy định, và báo lệnh tiếp theo.
- Bộ skill **độc lập hoàn toàn**, không gọi superpowers. Trong repo này, skill của dự án được ưu tiên hơn mọi skill khác.
- Tài liệu dùng chung cho cả app nằm ở `docs/design/`:
  - schema DB;
  - API: Markdown là nguồn chính, OpenAPI được sinh ra từ Markdown;
  - style UI, component dùng chung, mockup màn hình.
- Tài liệu của từng giai đoạn nằm ở `docs/phases/phase-N/`.
- Manual test bao gồm mọi thứ con người làm được bằng tay qua trình duyệt, DB, cookie, Facebook và thiết bị. Test case được thiết kế bài bản (bảng khía cạnh test + kỹ thuật thiết kế test), có evidence. Báo cáo quản lý bằng Markdown, xuất ra Excel và PDF (qua mẫu HTML).
- Mọi phản hồi trong lúc test (bug, điểm chưa hợp lý, câu hỏi) đi qua một cửa chung là `/feedback`. Skill này phân loại rồi chuyển sang skill phù hợp, và ghi vào sổ `issues.md`.
- **Đợt 1** gồm 20 skill và 1 command:
  - **Khởi tạo:** `conventions-init`, `ui-style-init`, `ui-style-update`, `test-viewpoints-init`.
  - **Thiết kế:** `phase-kickoff`, `detailed-design`, `ui-design`, `component-design`, `test-case-design`, `design-review`, `decision-log`.
  - **Code:** `implementation-plan`, `implement-task`, `tdd`, `code-review`, `bug-fix`, `change-request`.
  - **Test và nghiệm thu:** `manual-test-run`, `feedback`, `acceptance-report`.
  - **Command:** `/phase-status`.
- **Đợt sau:** fixture thật, eval AI, deploy, sửa lỗi khi Facebook đổi giao diện, đổi prompt/model, bật tính năng theo nấc, diễn tập khôi phục sao lưu.

---

## 1. Mục tiêu và phạm vi

### Mục tiêu
- Mỗi tình huống phát triển có một quy trình rõ ràng, lặp lại được, có điểm dừng để người duyệt.
- Không nhảy bước: không code khi thiết kế chưa duyệt, không nghiệm thu khi test chưa đạt.
- Truy vết được từ yêu cầu → thiết kế → test case → kết quả test → nghiệm thu.
- Claude Code tự biết bước tiếp theo, người dùng không phải nhớ quy trình.

### Trong phạm vi (đợt 1)
- 20 skill và command `/phase-status` liệt kê ở mục 5.
- `CLAUDE.md` chứa các quy tắc chung (mục 2).
- Mẫu tài liệu và checklist cho từng skill.
- Script xuất báo cáo Excel/PDF.

### Ngoài phạm vi
- Hướng dẫn vận hành cho chủ tiệm (ví dụ xử lý checkpoint): làm thành tài liệu riêng, sau.
- Các workflow đợt sau (mục 12).
- Không dùng hay phụ thuộc vào plugin superpowers.

---

## 2. Quy tắc chung (ghi trong `CLAUDE.md`)

- **Ưu tiên:** trong repo này, skill của dự án được ưu tiên hơn mọi skill khác, kể cả superpowers. Không dùng `brainstorming`, `writing-plans` của superpowers cho công việc phát triển hệ thống.
- **Vòng đời:** đi đúng thứ tự ở mục 3. Skill nào cũng kiểm tra điều kiện tiên quyết qua `status.md` trước khi làm.
- **Điểm dừng:** tại điểm dừng, skill dừng hẳn và chờ người dùng duyệt rõ ràng. Lần duyệt được ghi vào `status.md` kèm ngày. Duyệt một bước không có nghĩa là duyệt các bước sau.
- **Ngôn ngữ:** tên file, tên skill, mã định danh bằng tiếng Anh. Nội dung tài liệu bằng tiếng Việt.
- **Định dạng tài liệu:** ưu tiên heading và gạch đầu dòng. Chỉ dùng bảng khi dữ liệu thật sự là bảng (ví dụ cột DB, bảng đối chiếu).
- **Mã định danh:**
  - Giai đoạn: `phase-0` … `phase-4`.
  - Tính năng: kebab-case, ví dụ `group-settings`.
  - Test case: `P<giai đoạn>-<mã tính năng 3 chữ>-<số 3 chữ số>`, ví dụ `P0-GRP-012`. Mã 3 chữ do `detailed-design` đặt và ghi trong `status.md`.
  - Task code: `T<số 2 chữ số>` trong phạm vi giai đoạn, ví dụ `T06`.
  - Quyết định: `NNNN-<slug>`, ví dụ `0003-https-via-caddy`.
  - Vấn đề trong sổ theo dõi: `P<giai đoạn>-ISS-<số 3 chữ số>`, ví dụ `P0-ISS-007`.
  - Lần chạy test: `<YYYY-MM-DD>-<số thứ tự>`, ví dụ `2026-11-10-01`.
- **Ghi quyết định:** xem quy tắc ở skill `decision-log` (mục 5.2).
- **Dữ liệu thật:** evidence và báo cáo xuất ra (`.xlsx`, `.pdf`) không bao giờ được commit (mục 8.6).
- **Kết thúc mỗi skill** luôn báo theo 3 phần: đã làm gì và ghi vào file nào; cần người dùng quyết gì; bước tiếp theo là lệnh nào.

---

## 3. Vòng đời của một giai đoạn

```text
/phase-kickoff
  → (với từng tính năng)
     /detailed-design → /ui-design (nếu có màn hình, gọi /component-design khi cần)
     → /test-case-design → /design-review
  → /implementation-plan
  → (với từng task) /implement-task → /code-review
  → (với từng tính năng) /manual-test-run → [/bug-fix → /manual-test-run --retest]
  → /acceptance-report
```

Nhánh phụ dùng bất kỳ lúc nào: `/change-request`, `/decision-log`, `/phase-status`.

Nhóm khởi tạo chạy **một lần** trước giai đoạn 0, theo thứ tự: `/conventions-init` → `/ui-style-init` → `/test-viewpoints-init`. `/ui-style-update` dùng khi muốn đổi style về sau.

### 3.1 Luồng chính (ví dụ: GĐ0, tính năng "Cài đặt danh sách group")

**1. Mở giai đoạn**
```text
> /phase-kickoff 0
```
- **Input:**
  - `0`: số giai đoạn.
  - `docs/project/05-roadmap.md`: mục tiêu, danh sách việc, tiêu chí "Xong khi" của GĐ0.
  - `docs/project/06-open-issues-and-assumptions.md`: thông tin còn thiếu có thể chặn GĐ0.
- **Output:** `docs/phases/phase-0/status.md`: phạm vi, danh sách tính năng (kèm slug và mã 3 chữ), vấn đề đang chặn.
- **Điểm dừng:** người dùng xác nhận phạm vi.

**2. Thiết kế chi tiết**
```text
> /detailed-design group-settings
```
- **Input:**
  - `group-settings`: tên tính năng, lấy từ `status.md`.
  - `phase-0/status.md`: phạm vi và mục tài liệu khái quát liên quan.
  - Các mục liên quan trong `docs/project/`: nguồn yêu cầu.
  - Thiết kế đã duyệt trước đó và `docs/design/` (DB, API): giữ thống nhất.
- **Output:**
  - `phase-0/design/group-settings.md`;
  - cập nhật `docs/design/db-schema.md`, `docs/design/api/<resource>.md`, sinh lại `docs/design/api/openapi.yaml`.
- **Điểm dừng:** người dùng trả lời các câu hỏi mở và duyệt.

**3. Thiết kế UI** (chỉ với tính năng có màn hình)
```text
> /ui-design group-settings
```
- **Input:**
  - thiết kế chi tiết ở bước 2: các trường, quy tắc kiểm tra, thông báo lỗi;
  - `docs/design/ui-style.md`, `ui-tokens.css`;
  - `docs/design/components/index.md`.
- **Output:** `docs/design/ui/<màn hình>/`: mockup HTML và ảnh chụp từng trạng thái. Gọi `/component-design` khi gặp phần dùng lại được.
- **Điểm dừng:** người dùng duyệt mockup. Chỉnh UI làm đổi trường hoặc quy tắc thì cập nhật ngược thiết kế chi tiết.

**4. Thiết kế test case**
```text
> /test-case-design group-settings
```
- **Input:**
  - thiết kế chi tiết (bước 2) và mockup (bước 3);
  - `docs/testing/viewpoints.md`: khía cạnh test bắt buộc phải xét.
- **Output:** `phase-0/test/cases/group-settings.md`, cập nhật `phase-0/test/traceability.md`.

**5. Review thiết kế và test case**
```text
> /design-review group-settings
```
- **Input:** thiết kế, mockup, test case, `traceability.md`, các mục liên quan trong `docs/project/`.
- **Output:** `phase-0/design/reviews/group-settings-review.md`, sửa sau khi người dùng đồng ý.
- **Điểm dừng:** người dùng duyệt. Tính năng chuyển sang "đã duyệt thiết kế".

**6. Lập kế hoạch code**
```text
> /implementation-plan
```
- **Input:** mọi thiết kế đã duyệt của giai đoạn, code hiện có, POC.
- **Output:** `phase-0/plan.md`.
- **Điểm dừng:** người dùng duyệt.

**7. Code một task**
```text
> /implement-task T06
```
- **Input:** task trong `plan.md`, thiết kế mà task trỏ tới.
- **Output:** nhánh, code kèm test đã pass (qua `tdd`), commit, `plan.md` đánh dấu xong.

**8. Review code**
```text
> /code-review
```
- **Input:** diff nhánh hiện tại so với `main`, task và thiết kế liên quan, `db-schema.md`, `openapi.yaml`.
- **Output:** danh sách vấn đề → sửa → merge (khi người dùng đồng ý).

**9. Chạy manual test**
```text
> /manual-test-run group-settings
```
- **Input:** file case, môi trường test (người dùng cung cấp), kết quả và ảnh của các case làm tay.
- **Output:** `phase-0/test/runs/<mã lần chạy>/results.md` và `evidence/`.

**10. Nghiệm thu giai đoạn**
```text
> /acceptance-report 0
```
- **Input:** mọi lần chạy test, `traceability.md`, tiêu chí "Xong khi", số liệu chạy thật.
- **Output:** `phase-0/acceptance/report.md`, `.xlsx`, `.pdf`.
- **Điểm dừng:** chủ tiệm ký nghiệm thu.

### 3.2 Nhánh phụ
- **Phản hồi trong lúc test** (bug, điểm chưa hợp lý, câu hỏi): `/feedback "<nội dung>"` → phân loại → chuyển sang `/bug-fix`, `/change-request`, bổ sung test case, hoặc trả lời luôn.
- **Case không đạt:** `/bug-fix P0-GRP-012` → `/manual-test-run --retest P0-GRP-012`.
- **Yêu cầu thay đổi:** `/change-request "<nội dung>"`.
- **Ghi quyết định:** `/decision-log "<tiêu đề>"` (cũng được các skill thiết kế tự gọi).
- **Xem tiến độ:** `/phase-status`.

---

## 4. Cấu trúc thư mục

```text
CLAUDE.md                          # quy tắc chung (mục 2), quy ước code (từ conventions-init)
.claude/
├── skills/<tên>/                  # mỗi skill một thư mục (mục 6)
└── commands/phase-status.md
docs/
├── project/                       # thiết kế khái quát (đã có)
├── process/                       # tài liệu này
├── decisions/                     # NNNN-<slug>.md
├── testing/viewpoints.md          # bảng khía cạnh test dùng chung
├── design/                        # thiết kế dùng chung cho cả app
│   ├── db-schema.md
│   ├── api/
│   │   ├── <resource>.md          # nguồn chính
│   │   └── openapi.yaml           # sinh ra, không sửa tay
│   ├── ui-style.md                # nguồn chính của style
│   ├── ui-tokens.css              # sinh từ ui-style.md
│   ├── ui-style-preview.html
│   ├── components/
│   │   ├── index.md               # danh mục component
│   │   ├── <tên>.md
│   │   └── <tên>.html
│   └── ui/<màn hình>/             # mockup + ảnh chụp
└── phases/phase-N/
    ├── status.md
    ├── design/
    │   ├── <tính năng>.md
    │   └── reviews/<tính năng>-review.md
    ├── plan.md
    ├── issues.md                  # sổ theo dõi vấn đề (feedback, case không đạt)
    ├── test/
    │   ├── cases/<tính năng>.md
    │   ├── traceability.md
    │   └── runs/<mã lần chạy>/
    │       ├── results.md
    │       └── evidence/          # gitignore
    └── acceptance/
        ├── report.md
        └── report.xlsx, report.pdf  # gitignore
```

---

## 5. Danh mục skill

Mỗi skill được mô tả theo: mục đích, lệnh gọi, điều kiện tiên quyết, input, output, điểm dừng, skill khác được gọi.

### 5.1 Nhóm khởi tạo

#### `conventions-init`
- **Mục đích:** chốt quy ước phát triển cho toàn dự án.
- **Lệnh:** `/conventions-init`
- **Điều kiện tiên quyết:** chưa có mục "Quy ước" trong `CLAUDE.md`, hoặc người dùng muốn làm lại.
- **Input:** `docs/project/04-technical.md`, POC (cấu trúc, cách viết test), câu trả lời của người dùng.
- **Nội dung cần chốt:**
  - cấu trúc thư mục code (monorepo hay không, module NestJS, worker, web);
  - quy ước đặt tên (file, class, biến, bảng, cột, endpoint);
  - quy ước nhánh và commit (ví dụ `phase-0/t06-<slug>`, Conventional Commits);
  - công cụ lint, format, typecheck;
  - quy ước test (vị trí file, đặt tên, fixture, đồng hồ giả).
- **Output:** mục "Quy ước" trong `CLAUDE.md`, ADR cho các lựa chọn lớn.
- **Điểm dừng:** người dùng duyệt quy ước.
- **Gọi:** `decision-log`.

#### `ui-style-init`
- **Mục đích:** chốt style UI cho toàn hệ thống.
- **Lệnh:** `/ui-style-init`
- **Input:** `docs/story/BusinessContext.md` mục 2 (màu, font của tiệm), lộ trình nền tảng ở mục 13 (web máy tính trước → responsive → app native).
- **Output:**
  - `docs/design/ui-style.md` (nguồn chính): bảng màu và ý nghĩa, font, thang cỡ chữ, khoảng cách, bo góc, đổ bóng, icon, lưới bố cục và **breakpoint** (định nghĩa sẵn cho responsive về sau), quy ước component cơ bản (nút, ô nhập, thẻ, thông báo, badge), trạng thái tương tác, khả năng truy cập (độ tương phản, cỡ vùng chạm). Giá trị token viết độc lập với nền tảng để sau này sinh được token cho app native;
  - `docs/design/ui-tokens.css`: biến CSS sinh từ `ui-style.md`;
  - `docs/design/ui-style-preview.html` và ảnh chụp: trưng bày mọi component cơ bản.
- **Điểm dừng:** người dùng duyệt style.
- **Gọi:** `decision-log`.

#### `ui-style-update`
- **Mục đích:** đổi style hệ thống sau này.
- **Lệnh:** `/ui-style-update "<nội dung muốn đổi>"`
- **Điều kiện tiên quyết:** đã có `ui-style.md`.
- **Input:** nội dung thay đổi, `ui-style.md`, `components/index.md`, `docs/design/ui/`.
- **Output:**
  - cập nhật `ui-style.md` (kèm lịch sử thay đổi), sinh lại `ui-tokens.css` và `ui-style-preview.html`;
  - danh sách component và màn hình bị ảnh hưởng, chụp lại ảnh mockup;
  - danh sách test case UI cần chạy lại.
- **Điểm dừng:** người dùng duyệt bản preview mới trước khi cập nhật mockup.
- **Gọi:** `decision-log` nếu thay đổi lớn.

#### `test-viewpoints-init`
- **Mục đích:** tạo bảng khía cạnh test dùng chung cho mọi tính năng.
- **Lệnh:** `/test-viewpoints-init`
- **Input:** mục 8 của tài liệu này, `docs/project/` (đặc thù Facebook, Messenger, AI, lịch).
- **Output:** `docs/testing/viewpoints.md`, gồm từng khía cạnh, câu hỏi gợi ý và ví dụ (mục 8.2).
- **Điểm dừng:** người dùng duyệt.

### 5.2 Nhóm thiết kế

#### `phase-kickoff`
- **Mục đích:** mở một giai đoạn.
- **Lệnh:** `/phase-kickoff <N>`
- **Điều kiện tiên quyết:** nhóm khởi tạo đã xong. Giai đoạn trước (nếu có) đã nghiệm thu, hoặc người dùng chấp nhận chạy song song.
- **Input:** `05-roadmap.md`, `06-open-issues-and-assumptions.md`, `status.md` của giai đoạn trước.
- **Output:** `docs/phases/phase-N/status.md`: phạm vi, danh sách tính năng (slug, mã 3 chữ, có màn hình hay không, mục tài liệu khái quát liên quan), vấn đề đang chặn, tiêu chí "Xong khi".
- **Điểm dừng:** người dùng xác nhận phạm vi.

#### `detailed-design`
- **Mục đích:** viết thiết kế chi tiết cho một tính năng.
- **Lệnh:** `/detailed-design <tính năng>`
- **Điều kiện tiên quyết:** tính năng có trong `status.md`.
- **Input:** như mục 3.1 bước 2.
- **Output:** `phase-N/design/<tính năng>.md`, gồm:
  - tóm tắt và mục tài liệu khái quát liên quan;
  - chia module và interface;
  - **thay đổi DB** (trỏ tới `db-schema.md`);
  - **API** liên quan (trỏ tới `api/<resource>.md`);
  - màn hình: danh sách trường, **quy tắc kiểm tra dữ liệu** (bắt buộc, kiểu, khoảng, định dạng, duy nhất), thông báo lỗi;
  - job và hàng đợi: lịch chạy, ưu tiên, retry, timeout;
  - trạng thái và bước chuyển, thuật toán;
  - tích hợp bên ngoài (selector/GraphQL Facebook, webhook Messenger, prompt và schema Gemini);
  - xử lý lỗi, log, bảo mật, phân quyền;
  - tham số cài đặt: mặc định, khoảng hợp lệ;
  - câu hỏi mở, lịch sử thay đổi.
- Đồng thời cập nhật `db-schema.md`, `api/<resource>.md`, sinh lại `openapi.yaml` và chạy linter.
- **Điểm dừng:** người dùng trả lời câu hỏi mở và duyệt.
- **Gọi:** `decision-log`.

#### `ui-design`
- **Mục đích:** thiết kế màn hình trước khi thiết kế test case.
- **Lệnh:** `/ui-design <tính năng>`
- **Điều kiện tiên quyết:** thiết kế chi tiết đã duyệt, đã có `ui-style.md`.
- **Input:** như mục 3.1 bước 3.
- **Output:** `docs/design/ui/<màn hình>/`:
  - `index.html`: mockup ở khung máy tính 1440×900, dùng `ui-tokens.css`, **nhúng** HTML của component thay vì chép code. Khi tới giai đoạn responsive thì bổ sung khung điện thoại 390×844;
  - ảnh chụp từng trạng thái: bình thường, trống, đang tải, lỗi nhập, lỗi hệ thống, không có quyền;
  - `notes.md`: luồng thao tác, component dùng, chỗ khác với thiết kế chi tiết.
- Có thể đăng mockup thành link riêng tư để chủ tiệm xem và góp ý.
- **Điểm dừng:** người dùng duyệt mockup.
- **Gọi:** `component-design`, `decision-log`.

#### `component-design`
- **Mục đích:** thiết kế component nghiệp vụ dùng lại được.
- **Lệnh:** `/component-design <tên>`, hoặc được `ui-design` gọi khi một phần giao diện xuất hiện ở từ 2 màn hình trở lên hoặc mang tính chung.
- **Phân vai:** component cơ bản (nút, ô nhập…) thuộc `ui-style-init`. Skill này lo component ghép, gắn với nghiệp vụ, ví dụ `StatusBadge`, `ApprovalCard`, `SlotPicker`.
- **Luồng:** tra `components/index.md` trước. Có thì dùng lại hoặc thêm biến thể; chưa có mới thiết kế.
- **Input:** nhu cầu từ `ui-design`, `ui-style.md`, `ui-tokens.css`, `components/index.md`.
- **Output:**
  - `components/<tên>.md`: mục đích, cấu tạo, thuộc tính và biến thể, trạng thái, hành vi, nên/không nên dùng, **màn hình đang dùng**;
  - `components/<tên>.js`: Web Component, là phần được mockup màn hình nhúng vào;
  - `components/<tên>.html`: mockup mọi biến thể và trạng thái;
  - cập nhật `components/index.md`.
- Khi sửa component: liệt kê màn hình bị ảnh hưởng từ danh sách "màn hình đang dùng", chụp lại ảnh.
- **Điểm dừng:** người dùng duyệt component mới hoặc thay đổi component đang được dùng.

#### `test-case-design`
- **Mục đích:** thiết kế manual test case cho một tính năng.
- **Lệnh:** `/test-case-design <tính năng>`
- **Điều kiện tiên quyết:** thiết kế chi tiết đã duyệt; mockup đã duyệt (nếu có màn hình); đã có `viewpoints.md`.
- **Input:** thiết kế chi tiết, mockup, `viewpoints.md`, `traceability.md` hiện có.
- **Luồng:** theo mục 8.3.
- **Output:** `phase-N/test/cases/<tính năng>.md` (định dạng mục 8.5), cập nhật `traceability.md`.
- **Tự kiểm tra:** mọi quy tắc trong thiết kế có ít nhất một case; mọi khía cạnh trong `viewpoints.md` đã được xét (có case, hoặc ghi rõ lý do không áp dụng).

#### `design-review`
- **Mục đích:** review thiết kế chi tiết, mockup và test case của một tính năng.
- **Lệnh:** `/design-review <tính năng>`
- **Điều kiện tiên quyết:** đã có test case.
- **Input:** như mục 3.1 bước 5.
- **Checklist:** khớp yêu cầu, không mâu thuẫn với thiết kế khác và `docs/design/`, không có chỗ mơ hồ, đủ quy tắc kiểm tra và thông báo lỗi, đủ trạng thái lỗi, đủ case, không vi phạm các điều "tuyệt đối không được xảy ra" (`01-overview.md` mục 5).
- **Output:** `phase-N/design/reviews/<tính năng>-review.md`: danh sách điểm cần sửa, mức độ, cách sửa đề xuất, kết quả.
- **Điểm dừng:** người dùng chọn điểm nào sửa, rồi duyệt sau khi sửa.
- **Gọi:** `decision-log`.

#### `decision-log`
- **Mục đích:** ghi lại quyết định quan trọng.
- **Lệnh:** `/decision-log "<tiêu đề>"`, hoặc được skill khác gọi.
- **Khi nào ghi:** quyết định **chọn giữa nhiều phương án** và **ảnh hưởng rộng hơn một tính năng** (thư viện, kiến trúc, quy ước chung, style). Quyết định chỉ thuộc một tính năng thì ghi trong file thiết kế của tính năng đó.
- **Input:** tiêu đề, bối cảnh, các phương án, lý do chọn (hỏi người dùng nếu thiếu).
- **Output:** `docs/decisions/NNNN-<slug>.md`: bối cảnh, phương án, quyết định, hệ quả, trạng thái (đề xuất / chấp nhận / thay thế bởi …).

### 5.3 Nhóm code

#### `implementation-plan`
- **Mục đích:** chia thiết kế đã duyệt thành task code.
- **Lệnh:** `/implementation-plan`
- **Điều kiện tiên quyết:** mọi tính năng trong phạm vi đã duyệt thiết kế, hoặc người dùng chỉ định lập kế hoạch cho một phần.
- **Input:** như mục 3.1 bước 6.
- **Output:** `phase-N/plan.md`. Mỗi task gồm:
  - mã, tiêu đề, tính năng và mục thiết kế liên quan;
  - task phụ thuộc;
  - file tạo hoặc sửa;
  - test tự động cần viết (unit, integration, contract);
  - test case manual liên quan;
  - tiêu chí xong.
- Task đủ nhỏ để làm và review trong một lần.
- **Điểm dừng:** người dùng duyệt.

#### `implement-task`
- **Mục đích:** làm một task.
- **Lệnh:** `/implement-task <mã task>`
- **Điều kiện tiên quyết:** kế hoạch đã duyệt, các task phụ thuộc đã xong.
- **Luồng:** tạo nhánh theo quy ước → `tdd` cho từng hành vi → chạy toàn bộ test, typecheck, lint → tự review theo checklist của `code-review` → commit → cập nhật `plan.md` và `status.md`.
- **Output:** nhánh có commit, kết quả test.
- **Gọi:** `tdd`.

#### `tdd`
- **Mục đích:** viết code theo vòng đỏ → xanh → refactor.
- **Lệnh:** `/tdd "<hành vi>"`, hoặc được `implement-task`, `bug-fix` gọi.
- **Quy tắc:** viết test thất bại trước và xác nhận nó thất bại đúng lý do → code tối thiểu để pass → refactor khi test vẫn xanh. Không viết code nghiệp vụ khi chưa có test thất bại.
- **Quy ước test tự động** (mục 9) áp dụng ở đây.

#### `code-review`
- **Mục đích:** review code theo checklist dự án.
- **Lệnh:** `/code-review`
- **Input:** như mục 3.1 bước 8.
- **Checklist:**
  - đúng và đủ theo task và thiết kế;
  - migration khớp `db-schema.md`; endpoint khớp `openapi.yaml`; UI khớp mockup và `ui-tokens.css`;
  - có test cho mọi hành vi mới; test không bị bỏ qua mà không báo (`skip` phải có lý do);
  - quy ước trong `CLAUDE.md`;
  - xử lý lỗi, bảo mật, không lộ secret, không log dữ liệu cá nhân;
  - các lằn ranh đỏ: không thể tạo lịch trùng, không comment trùng khi retry, AI không tự sinh giá hoặc giờ.
- **Output:** danh sách vấn đề theo mức độ; sửa sau khi người dùng đồng ý.
- **Điểm dừng:** merge chỉ khi người dùng đồng ý.

#### `bug-fix`
- **Mục đích:** sửa lỗi có kiểm chứng.
- **Lệnh:** `/bug-fix <mã case | mô tả lỗi>`
- **Luồng:** đọc kết quả và evidence lần không đạt → tái hiện → tìm nguyên nhân gốc (không sửa triệu chứng) → `tdd`: test tự động tái hiện lỗi → sửa → toàn bộ test pass → gắn cờ regression cho case → cập nhật `results.md` (trạng thái "đã sửa, chờ test lại").
- Nếu lỗi do thiết kế sai: dừng, chuyển sang `change-request`.
- **Gọi:** `tdd`, `change-request`.

#### `change-request`
- **Mục đích:** xử lý thay đổi yêu cầu.
- **Lệnh:** `/change-request "<nội dung>"`
- **Luồng:**
  1. Dò mọi chỗ bị ảnh hưởng: `docs/project/`, thiết kế tính năng, `docs/design/` (DB, API, UI, component), test case, `traceability.md`, `plan.md`, code, test tự động.
  2. Trình danh sách ảnh hưởng và cách sửa.
  3. **Điểm dừng:** người dùng duyệt.
  4. Cập nhật tài liệu theo thứ tự từ trên xuống, ghi lịch sử thay đổi, đặt lại trạng thái tính năng trong `status.md` về bước sớm nhất bị ảnh hưởng.
- **Gọi:** `decision-log`.

### 5.4 Nhóm test và nghiệm thu

#### `manual-test-run`
- **Mục đích:** chạy manual test và thu evidence.
- **Lệnh:** `/manual-test-run <tính năng>`, `/manual-test-run --retest <mã case>`, `/manual-test-run --regression` (chạy mọi case có cờ regression).
- **Điều kiện tiên quyết:** code của tính năng đã merge (hoặc người dùng chỉ định nhánh).
- **Luồng:**
  1. Hỏi môi trường (máy dev hoặc Oracle, URL); tự lấy commit.
  2. Tạo `runs/<mã lần chạy>/`.
  3. Với từng case:
     - case Claude làm được (trình duyệt qua Playwright, DB qua lệnh SQL, cookie): tự chạy và tự chụp ảnh;
     - case cần người (thiết bị thật, Facebook thật, đánh giá bằng mắt): hướng dẫn từng bước, nhận ảnh và kết quả từ người dùng;
     - ghi đạt / không đạt / bị chặn / bỏ qua kèm lý do;
     - case không đạt tự tạo một mục trong `issues.md`.
  4. Với test lại: giữ nguyên kết quả và evidence lần trước, ghi lần mới cạnh đó; cập nhật mục tương ứng trong `issues.md`.
  5. Người dùng có phản hồi giữa chừng thì chuyển qua `feedback`.
- **Output:** `results.md` (mục 8.6), `evidence/`, cập nhật `issues.md`.
- **Gọi:** `feedback`, `bug-fix` (đề xuất, khi có case không đạt).

#### `feedback`
- **Mục đích:** cửa vào chung cho mọi phản hồi trong lúc test: bug, điểm chưa hợp lý, câu hỏi.
- **Lệnh:** `/feedback "<nội dung>"`, hoặc được `manual-test-run` gọi.
- **Input:**
  - nội dung phản hồi, ảnh chụp nếu có;
  - tính năng liên quan: tự đoán từ `status.md` và nội dung, đoán không ra thì hỏi;
  - thiết kế chi tiết, mockup, test case của tính năng: để đối chiếu.
- **Phân loại:**
  - **bug:** app chạy khác thiết kế → `bug-fix`;
  - **thiết kế chưa hợp lý:** app chạy đúng thiết kế nhưng thiết kế chưa tốt → `change-request`;
  - **thiếu test case:** tình huống chưa có case → bổ sung case vào file test case và `traceability.md`;
  - **câu hỏi hoặc hiểu nhầm:** trả lời, dẫn chứng từ thiết kế.
- **Điểm dừng:** trình bày cách phân loại và hướng xử lý, chờ người dùng xác nhận rồi mới chuyển skill.
- **Output:** mục mới trong `phase-N/issues.md`: mã, ngày, nội dung, phân loại, tính năng, tên file evidence, trạng thái (mở / đang xử lý / đã xong / không sửa kèm lý do), liên kết tới cách xử lý (commit, phiên bản thiết kế, case mới).
- **Gọi:** `bug-fix`, `change-request`.

#### `acceptance-report`
- **Mục đích:** nghiệm thu giai đoạn.
- **Lệnh:** `/acceptance-report <N>`
- **Điều kiện tiên quyết:** mọi tính năng ở trạng thái "đạt", hoặc người dùng chấp nhận lỗi còn mở.
- **Input:** như mục 3.1 bước 10, cộng `issues.md`.
- **Output:**
  - `acceptance/report.md`: tổng quan, đối chiếu từng tiêu chí "Xong khi", thống kê case, vấn đề còn mở (từ `issues.md`), số liệu chạy thật, phần ký nghiệm thu;
  - `report.xlsx`: sheet "Tổng hợp", sheet "Danh sách case", mỗi case có evidence một sheet và ảnh được nhúng;
  - `report.pdf`: render `report.md` qua mẫu HTML (`templates/report.html`) rồi in PDF bằng Playwright, ảnh evidence nhúng theo từng case.
- **Điểm dừng:** chủ tiệm ký nghiệm thu; `status.md` ghi ngày nghiệm thu.

### 5.5 Command `/phase-status`
- **Input:** `status.md`, `plan.md`, `test/runs/`, `issues.md` của giai đoạn hiện tại.
- **Output** (chỉ in ra, không ghi file): số tính năng theo từng bước, số task xong, số case đạt / không đạt / chưa chạy, số vấn đề đang mở, vấn đề đang chặn, lệnh nên chạy tiếp.

---

## 6. Cấu trúc bên trong một skill

```text
.claude/skills/<tên>/
├── SKILL.md
├── templates/     # mẫu output + một ví dụ output đã điền
├── checklists/    # danh sách tự kiểm tra
└── scripts/       # nếu cần
```

Khung chung của `SKILL.md`:
1. **Frontmatter:** `name`, `description` (có từ khóa tiếng Việt và tiếng Anh), `argument-hint`.
2. **Mục đích.**
3. **Điều kiện tiên quyết:** cách kiểm tra qua `status.md`; chưa thỏa thì dừng và báo.
4. **Input:** tham số, file tự đọc, những gì phải hỏi.
5. **Các bước.**
6. **Điểm dừng.**
7. **Output:** file và mẫu trong `templates/`.
8. **Tự kiểm tra:** chạy checklist trước khi báo xong.
9. **Cập nhật `status.md`.**
10. **Báo cáo kết thúc:** đã làm gì, cần quyết gì, lệnh tiếp theo.

---

## 7. `status.md`

Mỗi giai đoạn có một file, gồm:
- phạm vi và tiêu chí "Xong khi";
- danh sách tính năng: slug, mã 3 chữ, có màn hình hay không, mục tài liệu khái quát liên quan, **trạng thái**;
- vấn đề đang chặn;
- nhật ký duyệt: bước nào, ai duyệt, ngày nào.

Trạng thái của một tính năng:
```text
chưa bắt đầu → thiết kế chi tiết → UI (bỏ qua nếu không có màn hình) → test case
→ đã duyệt thiết kế → đang code → đã code → đang manual test → đạt
```
- Skill chỉ chuyển trạng thái tiến lên khi bước của nó xong và đã qua điểm dừng.
- `change-request` có thể đưa trạng thái lùi về bước sớm nhất bị ảnh hưởng.

---

## 8. Manual test

### 8.1 Phạm vi
- Kiểm chứng những gì unit test và test tự động không làm được:
  - hành vi thật khi thao tác có khớp thiết kế không;
  - edge case và regression;
  - thao tác sai của người dùng đã được kiểm tra và chặn chưa;
  - tình huống thực tế có thể xảy ra.
- Bao gồm mọi thứ con người làm được bằng tay: trình duyệt, sửa DB, cookie, thao tác trên Facebook và Messenger, thiết bị thật, đánh giá bằng mắt (poster, ảnh chỉnh, giọng văn), chạy thật dài ngày.
- **Không bao gồm** những case phải can thiệp vào luồng xử lý của code (thay giá trị lúc chạy, đặt breakpoint để gây timeout…). Phần đó thuộc test tự động.

### 8.2 Bảng khía cạnh test (`viewpoints.md`)
Ít nhất gồm:
- hiển thị (đúng mockup, đúng dữ liệu, chữ tiếng Việt, các kích thước cửa sổ);
- kiểm tra dữ liệu nhập;
- logic nghiệp vụ;
- chuyển trạng thái (hợp lệ và không hợp lệ);
- phân quyền;
- phiên đăng nhập và cookie;
- thao tác đồng thời;
- dữ liệu bất thường trong DB;
- phía Facebook và Messenger;
- thời gian (giờ nghỉ, hết hạn, múi giờ);
- lỗi mạng và lỗi hệ thống bên ngoài;
- regression.

### 8.3 Quy trình thiết kế test case
1. Đọc thiết kế chi tiết và mockup.
2. Với từng khía cạnh trong `viewpoints.md`: xác định có áp dụng không, liệt kê điều cần kiểm chứng.
3. Sinh case bằng các kỹ thuật:
   - **phân vùng tương đương và giá trị biên** cho dữ liệu nhập và tham số cài đặt;
   - **bảng quyết định** cho quy tắc nhiều điều kiện;
   - **chuyển trạng thái** cho lịch hẹn, khách, comment, yêu cầu báo giá…;
   - **đoán lỗi và tình huống thực tế** theo các nhóm thao tác ở mục 8.4.
4. Viết case theo định dạng mục 8.5, gắn với mục thiết kế.
5. Cập nhật `traceability.md`: mỗi quy tắc trong thiết kế → các case.
6. Gắn cờ regression cho case cốt lõi.

### 8.4 Các nhóm thao tác tay
- **Trình duyệt:** bấm gửi hai lần, Back, tải lại giữa chừng, hai tab cùng sửa, mất mạng, thu nhỏ cửa sổ.
- **Cookie và phiên:** xóa cookie, phiên hết hạn, dùng phiên vai trò Thợ vào URL của Quản lý.
- **DB:** sửa thời điểm để giả lập thời gian trôi qua, đặt dữ liệu về trạng thái lạ, xóa bản ghi liên quan.
- **Facebook:** xóa bài trước khi app comment, tắt comment, rời group, đăng xuất tài khoản vận hành, người thật trả lời khách từ Page.
- **Messenger:** trả lời sai cú pháp, trả lời yêu cầu đã hết hạn, tin thoại, ảnh không kèm chữ.
- **Thiết bị thật:** web push và PWA trên iPhone, Messenger trên Android, email báo khẩn.

Môi trường Facebook thật: tài khoản phụ, group riêng tư và Page thử do chủ tiệm tạo.

### 8.5 Định dạng test case
Mỗi case gồm:
- mã (`P0-GRP-012`), tiêu đề;
- mục thiết kế liên quan;
- khía cạnh và kỹ thuật dùng;
- mức ưu tiên; cờ regression;
- người thực hiện: Claude hoặc người;
- tiền điều kiện (tài khoản, vai trò, dữ liệu, cài đặt, môi trường);
- các bước, mỗi bước có kết quả mong đợi và đánh dấu bước cần evidence.

### 8.6 Kết quả và evidence
- `results.md` gồm: mã lần chạy, môi trường, commit, người chạy, ngày; với từng case: kết quả (đạt / không đạt / bị chặn / bỏ qua), kết quả thực tế khi không đạt, tên file evidence, ghi chú; các lần test lại.
- Loại evidence: ảnh chụp trước và sau thao tác, quay màn hình cho hành vi phụ thuộc thời gian, ID và bản ghi DB, log có thời điểm, ảnh app tự chụp.
- Tên file: `<mã case>_<số bước>_<mô tả ngắn>.png`, ví dụ `P0-GRP-012_02_error-shown.png`.
- **Evidence không che thông tin.** Vì vậy:
  - `evidence/`, `report.xlsx`, `report.pdf` nằm trong `.gitignore`;
  - chỉ commit `results.md` và `report.md`;
  - người dùng tự xóa evidence sau khi xác nhận.

---

## 9. Quy ước test tự động (dùng trong `tdd`, `implement-task`, `code-review`)

- **Unit test** cho logic nghiệp vụ, đồng hồ truyền vào từ ngoài (không gọi `Date.now()` trực tiếp).
- **Property-based test** cho bất biến quan trọng (lịch không trùng, khung đề xuất luôn trống).
- **Integration test** với Postgres và Redis thật trong Docker cho ràng buộc DB, giao dịch, hàng đợi, migration.
- **Contract test** cho adapter bên ngoài: fixture Facebook (payload và HTML đã lưu), fixture webhook Messenger, bản giả của nhà cung cấp AI; đối chiếu code với `openapi.yaml`.
- **Kịch bản đầu-cuối với bản giả** cho các luồng nghiệp vụ.
- **Không bỏ qua test mà không báo:** test phụ thuộc fixture thật phải báo rõ khi thiếu fixture (bài học từ POC: `story-parser.real.test.ts` bị skip mà vẫn báo pass).
- Chi tiết công cụ (vitest, Testcontainers…) do `conventions-init` chốt.

---

## 10. Công cụ

- **Excel:** Python (`py`, đã có 3.15) + `openpyxl`, nhúng ảnh evidence.
- **PDF:** mẫu HTML + Playwright (Chromium) in PDF. Không phụ thuộc Excel hay LibreOffice.
- **OpenAPI:** sinh từ `api/*.md`, kiểm tra bằng Redocly CLI.
- **Mockup:** HTML tĩnh + `ui-tokens.css`, mỗi trạng thái một file HTML, chụp bằng Playwright ở khung 1440×900 (thêm 390×844 khi làm responsive).
- **Component:** Web Component thuần (`components/<tên>.js`); mockup nhúng bằng `<script src>` + thẻ custom element, nên mở được trực tiếp bằng `file://` và sửa component thì mọi mockup đổi theo.
- **Token:** `ui-style.md` có một khối YAML dưới heading `## Tokens`; script sinh `ui-tokens.css` từ khối này (sau này sinh được token cho app native).
- **Manual test do Claude chạy:** Playwright cho trình duyệt; lệnh SQL cho DB.
- Script chỉ một skill dùng thì đặt trong `scripts/` của skill đó; script dùng chung (sinh token, chụp mockup, kiểm tra skill) đặt ở `tools/`.

---

## 11. Kiểm chứng bộ skill

- **Chạy thử thật:** đi trọn vòng đời với tính năng `group-settings` của GĐ0 (sau khi chạy nhóm khởi tạo). Ghi lại chỗ skill hướng dẫn sai hoặc thiếu, rồi sửa skill.
- Mỗi skill có một ví dụ output đã điền trong `templates/` để so sánh.
- **Điều kiện xong:**
  - chạy hết luồng chính từ bước 1 tới bước 10 (bỏ phần chạy thật dài ngày) và mỗi nhánh phụ ít nhất một lần;
  - không phải sửa tay output;
  - xuất được `report.xlsx` và `report.pdf` có ảnh evidence.

---

## 12. Đợt sau
- Lấy và làm mới fixture thật.
- Chạy eval AI khi đổi prompt hoặc model.
- Deploy và smoke test.
- Sửa lỗi khi Facebook đổi giao diện.
- Đổi prompt, model hoặc nhà cung cấp AI.
- Bật tính năng theo nấc (chế độ bóng → duyệt trước → tự gửi).
- Diễn tập khôi phục sao lưu.
- Hướng dẫn vận hành cho chủ tiệm.

---

## 13. Quyết định và giả định trong tài liệu này
- Chọn hướng bộ skill độc lập, không dùng superpowers (người dùng chọn).
- Evidence không che, không commit; người dùng tự xóa sau khi xác nhận (người dùng chốt). Phần không commit gồm cả `report.xlsx` và `report.pdf` vì có nhúng ảnh (giả định của người viết).
- PDF xuất từ mẫu HTML bằng Playwright, song song với Excel; cả hai cùng sinh từ `report.md` (người dùng chốt).
- **Lộ trình nền tảng UI** (người dùng chốt): trước mắt là web tối ưu cho máy tính; tiếp theo là responsive cho điện thoại; sau này là app native. Hệ quả:
  - mockup vẽ ở khung 1440×900 (giả định kích thước);
  - `ui-style.md` định nghĩa sẵn breakpoint và token độc lập nền tảng;
  - API giữ sạch, đầy đủ trong `openapi.yaml` để app native dùng lại.
- **Cần cập nhật tài liệu khái quát:** `docs/project/02-features/07-screens-and-settings.md` và `05-roadmap.md` đang ghi "ưu tiên điện thoại", PWA và web push. Việc này làm bằng `/change-request` sau khi có bộ skill, và phải xem lại kênh thông báo cho chủ tiệm (dùng iPhone).
- `/phase-status` là command chỉ đọc, không ghi file.
- Lần chạy thử bộ skill dùng tính năng `group-settings` của GĐ0.
