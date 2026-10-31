# Hướng dẫn sử dụng bộ skill phát triển

Tài liệu này hướng dẫn cách dùng bộ skill Claude Code của dự án Tiệm Nhà Mio để phát triển hệ thống, từ lúc mở một giai đoạn tới lúc nghiệm thu.

- Thiết kế chi tiết của quy trình: `docs/process/2026-10-29-dev-process-skills-design.md`.
- Quy tắc chung Claude Code luôn tuân theo: `CLAUDE.md`.
- Mã nguồn các skill: `.claude/skills/<tên>/SKILL.md`.

---

## 1. Bộ skill là gì

- Mỗi bước trong quy trình phát triển là một **skill**: một tập hướng dẫn để Claude Code làm đúng một việc (thiết kế chi tiết, thiết kế test case, code một task, chạy manual test…).
- Bạn gọi skill bằng **slash command**, ví dụ `/detailed-design group-settings`. Claude Code tự đọc tài liệu đầu vào theo quy ước thư mục, ghi kết quả theo mẫu, rồi **dừng chờ bạn duyệt** ở những điểm quan trọng.
- Bạn không cần nhớ thứ tự các bước: skill nào cũng kết thúc bằng lệnh nên chạy tiếp, và `/phase-status` luôn cho biết đang ở đâu.

Vai trò của bạn: **trả lời câu hỏi, duyệt kết quả, làm các bước test cần người thật**. Claude Code lo phần viết tài liệu, viết code, viết test, chạy test.

---

## 2. Chuẩn bị một lần

1. Cài Claude Code và mở thư mục repo bằng Claude Code.
2. Cài công cụ Python (Python 3.15, gọi bằng `py`):
   ```bash
   py -m pip install -r tools/requirements.txt
   py -m playwright install chromium
   ```
3. Có Node.js (để chạy `npx @redocly/cli` khi sinh API spec) và Docker (cho integration test).
4. Kiểm tra bộ skill còn nguyên vẹn:
   ```bash
   py tools/skills/validate_skills.py     # kỳ vọng: 20 skill hợp lệ, 1 command hợp lệ
   py -m pytest tools .claude/skills -q   # kỳ vọng: toàn bộ pass
   ```

---

## 3. Cách gọi skill

- **Cách 1, gõ slash command (khuyến nghị):** `/<tên skill> <tham số>`, ví dụ `/manual-test-run group-settings`. Chắc chắn gọi đúng skill.
- **Cách 2, nói tự nhiên:** ví dụ "case 12 fail rồi, app vẫn lưu được 51". Claude Code tự chọn skill phù hợp (ở đây là `bug-fix`). Tiện hơn nhưng đôi khi chọn nhầm.

Mỗi skill kết thúc bằng đúng 3 phần:
- **đã làm gì** và ghi vào file nào;
- **cần bạn quyết gì**;
- **bước tiếp theo** là lệnh nào.

Lưu ý:
- Dùng `/review-code`, **không phải** `/code-review`. `/code-review` là lệnh có sẵn của Claude Code, không biết các quy ước của dự án.
- Skill luôn kiểm tra điều kiện tiên quyết trong `status.md`. Nếu bước trước chưa xong, skill dừng và báo lệnh cần chạy trước. Đó là chủ ý, không phải lỗi.

---

## 4. Điểm dừng và việc duyệt

- Tại **điểm dừng**, Claude Code dừng hẳn và chờ bạn trả lời. Bạn có thể đồng ý, yêu cầu sửa, hoặc trả lời câu hỏi mở.
- Duyệt phải **rõ ràng** ("duyệt", "ok, chốt"). Lần duyệt được ghi vào mục `## Nhật ký duyệt` của `status.md` kèm ngày.
- Duyệt một bước **không** có nghĩa là duyệt luôn các bước sau.
- Merge vào `main` chỉ xảy ra khi bạn đồng ý ở bước `/review-code`.

### Đọc tài liệu qua bản đọc

Tài liệu do skill sinh ra (bản gốc) viết cho AI: nhiều mã số, tham chiếu chéo, văn kiểu ghi chú. Để review nhanh, mỗi tài liệu có một **bản đọc**:
- **Markdown:** `docs/reader/<cùng đường dẫn như trong docs/>`, ví dụ `docs/reader/phases/phase-0/design/auth.md`.
- **HTML:** mở `docs/reader/html/index.html` để xem danh sách; rê chuột lên mã để xem ý nghĩa, bấm mã để nhảy tới chỗ định nghĩa.
- Trong bản Markdown, phần *nghiêng trong ngoặc* sau mã, ví dụ R-AUT-06 *(Giới hạn đăng nhập sai)*, là ý nghĩa do script chèn từ định nghĩa gốc.
- Ở mỗi điểm dừng, skill gửi kèm link bản đọc của các file vừa ghi. Lần duyệt vẫn được ghi cho bản gốc.
- Bản đọc **không sửa tay**. Muốn sửa nội dung thì yêu cầu sửa bản gốc; bản đọc được sinh lại.
- Bản đọc cũ hơn bản gốc: trang HTML có dải cảnh báo vàng, `/phase-status` liệt kê ở dòng "Bản đọc đã cũ". Sinh lại bằng `/reader-view <file>`, `/reader-view phase-N` hoặc `/reader-view all`.

---

## 5. Toàn cảnh vòng đời

```text
Khởi tạo (một lần):  /conventions-init → /ui-style-init → /test-viewpoints-init

Mỗi giai đoạn:
/phase-kickoff N
  → (từng tính năng) /detailed-design → /ui-design (nếu có màn hình) → /test-case-design → /design-review
  → /implementation-plan
  → (từng task) /implement-task → /review-code
  → (từng tính năng) /manual-test-run → [/feedback | /bug-fix → /manual-test-run --retest]
  → /acceptance-report N

Dùng bất kỳ lúc nào: /phase-status, /feedback, /change-request, /decision-log, /ui-style-update
```

Các giai đoạn lấy từ `docs/project/05-roadmap.md`. Mỗi giai đoạn đi trọn vòng đời trên rồi mới sang giai đoạn sau.

---

## 6. Khởi tạo dự án (chạy một lần)

Chạy theo thứ tự trước Giai đoạn 0. Đã chạy rồi thì bỏ qua mục này.

1. **`/conventions-init`**: chốt quy ước code (cấu trúc thư mục, đặt tên, nhánh và commit, lint, test). Claude Code đưa phương án cho từng nhóm, bạn chọn. Kết quả ghi vào mục `## Quy ước` của `CLAUDE.md`.
2. **`/ui-style-init`**: chốt style giao diện (màu, font, cỡ chữ, khoảng cách, component cơ bản). Kết quả: `docs/design/ui-style.md`, `ui-tokens.css` và trang preview để bạn xem bằng mắt.
3. **`/test-viewpoints-init`**: tạo bảng khía cạnh test dùng chung cho mọi tính năng: `docs/testing/viewpoints.md`.

---

## 7. Làm một giai đoạn, từng bước

Ví dụ xuyên suốt: Giai đoạn 0, tính năng "Cài đặt danh sách group" (`group-settings`).

### Bước 1. Mở giai đoạn
```text
/phase-kickoff 0
```
- Claude Code đọc roadmap, chia giai đoạn thành các tính năng (mỗi tính năng có slug và mã 3 chữ, ví dụ `GRP`), liệt kê việc đang chặn.
- **Bạn:** xác nhận phạm vi, danh sách tính năng, thứ tự làm.
- **Kết quả:** `docs/phases/phase-0/status.md`, `issues.md`.

### Bước 2. Thiết kế chi tiết từng tính năng
```text
/detailed-design group-settings
```
- Biến yêu cầu khái quát thành thiết kế đủ chi tiết: DB, API, màn hình, quy tắc kiểm tra dữ liệu (mỗi quy tắc có mã `R-GRP-01`…), thông báo lỗi nguyên văn, tham số.
- Cập nhật luôn tài liệu dùng chung: `docs/design/db-schema.md`, `docs/design/api/*.md`, sinh `openapi.yaml`.
- **Bạn:** trả lời các câu hỏi mở (những điều tài liệu khái quát chưa nói), rồi duyệt.
- **Kết quả:** `docs/phases/phase-0/design/group-settings.md`.

### Bước 3. Thiết kế màn hình (chỉ khi tính năng có giao diện)
```text
/ui-design group-settings
```
- Vẽ mockup HTML khung 1440×900 cho mọi trạng thái (bình thường, trống, đang tải, lỗi nhập, lỗi hệ thống, không có quyền) và chụp ảnh.
- Phần giao diện dùng lại được (ví dụ badge trạng thái) được tách thành component dùng chung qua `/component-design`.
- **Bạn:** xem ảnh mockup, góp ý, duyệt.
- **Kết quả:** `docs/design/ui/<màn hình>/`, `docs/design/components/`.

### Bước 4. Thiết kế manual test case
```text
/test-case-design group-settings
```
- Sinh test case từ thiết kế và mockup, xét đủ 12 khía cạnh trong `viewpoints.md`, dùng các kỹ thuật giá trị biên, bảng quyết định, chuyển trạng thái, đoán lỗi.
- Mỗi case có mã `P0-GRP-012`, trỏ về quy tắc `R-GRP-…`, ghi rõ ai làm (Claude hay người) và bước nào cần chụp evidence.
- **Kết quả:** `docs/phases/phase-0/test/cases/group-settings.md`, bảng đối chiếu `test/traceability.md`.

### Bước 5. Review thiết kế
```text
/design-review group-settings
```
- Review thiết kế, mockup, test case theo checklist (khớp yêu cầu, không mâu thuẫn, đủ trường hợp lỗi, không vi phạm "lằn ranh đỏ" của dự án).
- **Bạn:** chọn điểm nào sửa, rồi duyệt thiết kế.
- **Kết quả:** `docs/phases/phase-0/design/reviews/group-settings-review.md`; tính năng chuyển sang "đã duyệt thiết kế".

Lặp bước 2–5 cho từng tính năng của giai đoạn.

### Bước 6. Lập kế hoạch code
```text
/implementation-plan
```
- Chia mọi thiết kế đã duyệt thành task nhỏ `T01`, `T02`… có thứ tự phụ thuộc, mỗi task ghi file sửa, test cần viết, tiêu chí xong.
- **Bạn:** duyệt kế hoạch.
- **Kết quả:** `docs/phases/phase-0/plan.md`.

### Bước 7. Code từng task
```text
/implement-task T06
```
- Tạo nhánh theo quy ước, viết code theo TDD (test trước, thấy fail rồi mới code), chạy test, lint, typecheck, tự review, commit.
- **Kết quả:** nhánh có commit; `plan.md`, `status.md` được cập nhật trong cùng commit.

### Bước 8. Review code và merge
```text
/review-code
```
- Đối chiếu code với task, thiết kế, `db-schema.md`, `openapi.yaml`, mockup; chạy lại toàn bộ kiểm tra.
- **Bạn:** chọn vấn đề nào sửa; đồng ý merge.

Lặp bước 7–8 cho từng task.

### Bước 9. Chạy manual test
```text
/manual-test-run group-settings
```
- **Bạn:** cho biết môi trường test (máy dev hay máy chủ) và URL.
- Case "Claude": Claude Code tự thao tác trình duyệt, DB, cookie và tự chụp evidence.
- Case "người" (Facebook thật, điện thoại thật, đánh giá bằng mắt): Claude Code đưa từng bước, **bạn** làm, chụp ảnh và gửi lại.
- Case không đạt tự được ghi vào sổ vấn đề `issues.md`.
- **Kết quả:** `docs/phases/phase-0/test/runs/<mã lần chạy>/results.md` và thư mục `evidence/`.

### Bước 10. Nghiệm thu giai đoạn
```text
/acceptance-report 0
```
- Đối chiếu từng tiêu chí "Xong khi", thống kê test case, liệt kê vấn đề còn mở.
- **Bạn:** cung cấp số liệu chạy thật (số ngày chạy, số lần bị checkpoint, RAM, CPU) nếu app chưa tự ghi; đưa báo cáo cho chủ tiệm ký.
- **Kết quả:** `acceptance/report.md`, `report.xlsx` (có ảnh evidence), `report.pdf`.

Sau đó: `/phase-kickoff 1` cho giai đoạn tiếp theo.

---

## 8. Các tình huống thường gặp

### "Đang ở đâu, làm gì tiếp?"
```text
/phase-status
```
In ra tiến độ: tính năng ở bước nào, số task xong, kết quả test case, vấn đề đang mở, việc đang chặn, và lệnh nên chạy tiếp. Lệnh này chỉ đọc, không sửa file.

### Đang test thấy lỗi, thấy chỗ chưa hợp lý, hoặc có thắc mắc
```text
/feedback "Danh sách group không sắp xếp theo tên, khó tìm"
```
- Claude Code đối chiếu với thiết kế và phân loại: **bug** (app chạy khác thiết kế), **thiết kế chưa hợp lý** (app đúng thiết kế nhưng thiết kế chưa tốt), **thiếu test case**, hoặc **câu hỏi**.
- **Bạn:** xác nhận phân loại. Sau đó Claude Code ghi vào `issues.md` và chuyển sang cách xử lý tương ứng.
- Khi không chắc nên dùng lệnh nào, cứ dùng `/feedback`.

### Một case không đạt
```text
/bug-fix P0-GRP-012
/review-code
/manual-test-run --retest P0-GRP-012
```
- `bug-fix` tìm nguyên nhân gốc, viết test tự động tái hiện lỗi rồi sửa. Vấn đề chuyển sang trạng thái "chờ test lại".
- Test lại đạt thì vấn đề được đóng. Vẫn lỗi thì vấn đề cũ được mở lại, không sinh vấn đề mới.
- Nếu lỗi nằm ở thiết kế chứ không ở code, `bug-fix` dừng và chuyển sang `change-request`.

### Yêu cầu thay đổi
```text
/change-request "Giới hạn comment/ngày tối đa 100"
```
- Claude Code dò mọi chỗ bị ảnh hưởng (tài liệu khái quát, thiết kế, DB, API, mockup, test case, kế hoạch, code) và trình bày trước.
- **Bạn:** duyệt danh sách ảnh hưởng. Sau đó tài liệu được cập nhật theo thứ tự, tính năng lùi về bước sớm nhất bị ảnh hưởng, phần code được thêm thành task mới.

### Chạy lại toàn bộ case quan trọng sau một thay đổi lớn
```text
/manual-test-run --regression
```
Chạy mọi case có cờ regression của giai đoạn.

### Ghi lại một quyết định lớn
```text
/decision-log "HTTPS dùng Caddy"
```
- Chỉ dùng cho quyết định chọn giữa nhiều phương án **và** ảnh hưởng rộng hơn một tính năng (thư viện, kiến trúc, quy ước chung, style).
- Các skill thiết kế tự gọi lệnh này khi cần. Quyết định nhỏ của một tính năng được ghi ngay trong file thiết kế của tính năng đó.
- **Kết quả:** `docs/decisions/NNNN-<slug>.md`.

### Đổi style giao diện
```text
/ui-style-update "Đổi màu nhấn sang nâu ca cao"
```
Cập nhật `ui-style.md`, sinh lại token, cho bạn duyệt bản preview, rồi cập nhật component và mockup bị ảnh hưởng và liệt kê test case hiển thị cần chạy lại.

---

## 9. Trạng thái cần biết

### Trạng thái của một tính năng (trong `status.md`)
```text
chưa bắt đầu → thiết kế chi tiết → UI (bỏ qua nếu không có màn hình) → test case
→ đã duyệt thiết kế → đang code → đã code → đang manual test → đạt
```
`/change-request` có thể đưa tính năng lùi về bước sớm hơn.

### Trạng thái của một vấn đề (trong `issues.md`)
- **mở**, **đang xử lý**, **chờ test lại**: còn mở, được tính vào báo cáo nghiệm thu.
- **đã xong**, **không sửa** (kèm lý do): đã đóng.

### Kết quả của một test case
`đạt`, `không đạt`, `bị chặn`, `bỏ qua`. Case chưa có kết quả nào được tính là "chưa chạy". Case có dòng `- Đã bỏ:` (do thay đổi yêu cầu) không chạy và không tính.

---

## 10. Tài liệu nằm ở đâu

```text
docs/
├── project/            # thiết kế khái quát (yêu cầu gốc)
├── process/            # quy trình phát triển và hướng dẫn này
├── decisions/          # quyết định lớn (ADR)
├── testing/viewpoints.md
├── design/             # dùng chung cả app
│   ├── db-schema.md, api/ (Markdown là nguồn chính, openapi.yaml sinh ra)
│   ├── ui-style.md, ui-tokens.css, components/, ui/<màn hình>/
└── phases/phase-N/
    ├── status.md       # trạng thái giai đoạn, nhật ký duyệt
    ├── design/         # thiết kế chi tiết từng tính năng, review
    ├── plan.md         # kế hoạch code
    ├── issues.md       # sổ vấn đề
    ├── test/           # cases/, traceability.md, runs/<mã lần chạy>/
    └── acceptance/     # báo cáo nghiệm thu
```

Không sửa tay các file sinh tự động: `docs/design/api/openapi.yaml`, `docs/design/ui-tokens.css`.

---

## 11. Evidence và dữ liệu thật

- Ảnh evidence **không che thông tin** nên có thể chứa dữ liệu thật của khách. Bạn tự xóa sau khi đã xác nhận.
- Các thư mục và file sau **không bao giờ được commit** (đã có trong `.gitignore`): `docs/phases/*/test/runs/*/evidence/`, `docs/phases/*/acceptance/*.xlsx`, `docs/phases/*/acceptance/*.pdf`, `.local/`.
- Chỉ commit `results.md` và `report.md` (chỉ chứa tên file ảnh, không chứa ảnh).
- Xuất lại báo cáo sau khi đã xóa evidence vẫn chạy được; ô ảnh sẽ ghi "Thiếu file evidence".
- Nếu xuất báo cáo báo "Đóng file … rồi chạy lại": đóng file Excel/PDF đang mở rồi chạy lại.

---

## 12. Mã định danh

- Giai đoạn: `phase-0` … `phase-4`.
- Tính năng: slug kebab-case `group-settings`, mã 3 chữ `GRP`.
- Quy tắc trong thiết kế: `R-GRP-03`.
- Test case: `P0-GRP-012`.
- Task code: `T06`.
- Quyết định: `0003-https-via-caddy`.
- Lần chạy test: `2026-11-10-01`.
- Vấn đề: `P0-ISS-007`.

---

## 13. Bảo trì bộ skill

- Thấy skill hướng dẫn sai hoặc thiếu trong lúc dùng: sửa trực tiếp `.claude/skills/<tên>/SKILL.md` (hoặc mẫu trong `templates/`), rồi chạy lại `py tools/skills/validate_skills.py`.
- Mỗi `SKILL.md` phải giữ đủ 9 mục theo thứ tự: Mục đích, Điều kiện tiên quyết, Input, Các bước, Điểm dừng, Output, Tự kiểm tra, Cập nhật status.md, Báo cáo kết thúc. Validator sẽ báo nếu thiếu.
- Thêm skill mới: tạo thư mục trong `.claude/skills/`, thêm tên vào `tools/skills/expected_skills.txt`, chạy validator.
- Sửa script trong `tools/` hoặc `acceptance-report/scripts/`: chạy `py -m pytest tools .claude/skills -q` trước khi commit.
