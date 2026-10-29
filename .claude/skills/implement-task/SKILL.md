---
name: implement-task
description: Làm một task trong plan.md của giai đoạn - tạo nhánh theo quy ước, viết code bằng tdd, chạy test/typecheck/lint, tự review theo checklist, commit và cập nhật plan.md, status.md. Use to implement a planned task.
argument-hint: "<mã task, ví dụ T06>"
---

# implement-task

## Mục đích

Hiện thực đúng một task của `docs/phases/phase-N/plan.md`, có test và đã tự review.

## Điều kiện tiên quyết

- `plan.md` đã duyệt (có dòng `duyệt kế hoạch code` trong `## Nhật ký duyệt` của `status.md`).
- Task tồn tại, `- Trạng thái:` là `chưa làm` hoặc `đang làm`.
- Mọi task trong `- Phụ thuộc:` đã `xong`.
- Cây làm việc git sạch (không có thay đổi chưa commit của việc khác).

## Input

- Tham số: mã task.
- Task trong `docs/phases/phase-N/plan.md`.
- File thiết kế mà task trỏ tới; `docs/design/db-schema.md`, `docs/design/api/openapi.yaml`, mockup và `docs/design/ui-tokens.css` nếu task có UI.
- `CLAUDE.md` mục `## Quy ước`: tên nhánh, lệnh test/typecheck/lint, commit message.

## Các bước

1. Tạo nhánh theo quy ước (ví dụ `phase-<N>/t<nn>-<slug>`) từ `main` mới nhất. Đặt `- Trạng thái: đang làm` cho task; nếu là task đầu tiên của tính năng, đặt trạng thái tính năng `đang code` trong `status.md`.
2. Với từng hành vi trong `- Test tự động:` và các `R-…` của task: gọi `tdd`.
3. UI: dùng đúng component và token như mockup; chỉ `var(--...)` từ `ui-tokens.css`.
4. Chạy lệnh test, typecheck, lint trong `## Quy ước`. Mọi lệnh phải sạch.
5. Tự review bằng `.claude/skills/review-code/checklists/review-code.md`; sửa chỗ không đạt (theo `tdd` nếu là hành vi).
6. Kiểm tra `- Tiêu chí xong:` bằng đúng lệnh/quan sát ghi trong task.
7. **Trước khi commit**: đặt `- Trạng thái: xong` cho task trong `plan.md`; nếu mọi task của tính năng đã xong, đặt trạng thái tính năng `đã code` trong `status.md`.
8. Commit code, test, `plan.md` và `status.md` trong cùng một commit theo quy ước commit message. Cây làm việc phải sạch sau commit.

## Điểm dừng

- Không có điểm dừng thường lệ.
- Dừng và hỏi khi: thiết kế mâu thuẫn hoặc thiếu (gợi ý `/change-request`); task lớn hơn dự kiến cần tách; phải làm việc ngoài phạm vi task.

## Output

- Nhánh có commit; kết quả các lệnh test, typecheck, lint.
- `plan.md` và `status.md` đã cập nhật.

## Tự kiểm tra

- Mọi test ghi trong task tồn tại và pass; đã thấy chúng thất bại trước (qua `tdd`).
- Đạt mọi mục trong checklist review.
- Không sửa file ngoài danh sách `- File:` mà không ghi lý do trong báo cáo.

## Cập nhật status.md

Tính năng: `đã duyệt thiết kế` → `đang code` (task đầu) → `đã code` (task cuối của tính năng).

## Báo cáo kết thúc

- Nhánh, commit, kết quả test/typecheck/lint, file đã sửa.
- Cần người dùng quyết: chỗ lệch kế hoạch (nếu có).
- Bước tiếp theo: `/review-code`.
