---
name: review-code
description: Review code của nhánh hiện tại theo checklist của dự án (đúng task và thiết kế, migration khớp db-schema.md, endpoint khớp openapi.yaml, UI khớp mockup, test đủ và không skip ngầm, quy ước, bảo mật, lằn ranh đỏ) trước khi merge. Use to review project code changes before merge.
argument-hint: ""
---

# review-code

## Mục đích

Bắt lỗi trước khi merge vào `main`, đối chiếu code với thiết kế và quy ước của dự án.

## Điều kiện tiên quyết

- Đang ở nhánh task (không phải `main`) và nhánh có commit so với `main`.
- Không thỏa: dừng, báo.

## Input

- Diff: `git diff main...HEAD` và danh sách commit `git log main..HEAD`.
- Task tương ứng trong `docs/phases/phase-N/plan.md` (suy từ tên nhánh) và thiết kế mà task trỏ tới.
- `docs/design/db-schema.md`, `docs/design/api/openapi.yaml`, mockup và `docs/design/ui-tokens.css`.
- `CLAUDE.md` mục `## Quy ước`.

## Các bước

1. Đọc task, thiết kế, rồi đọc toàn bộ diff.
2. Đi lần lượt từng mục trong `checklists/review-code.md`.
3. Chạy lệnh test, typecheck, lint trong `## Quy ước`; đọc kết quả, đếm test skip và lý do.
4. Liệt kê vấn đề, mỗi vấn đề một dòng: `- [chặn | nên sửa | gợi ý] <file>:<dòng> — <vấn đề> — <cách sửa>`.
5. Trình bày cho người dùng, hỏi vấn đề nào sửa.
6. Sửa các vấn đề được đồng ý; vấn đề về hành vi sửa theo `tdd` (test tái hiện trước). Chạy lại bước 3.
7. Khi người dùng đồng ý: merge vào `main` theo cách trong `## Quy ước`.

## Điểm dừng

- Sau bước 5: người dùng chọn vấn đề nào sửa.
- Trước bước 7: merge **chỉ** khi người dùng đồng ý rõ ràng.

## Output

Danh sách vấn đề (trong câu trả lời, không ghi file), các commit sửa, kết quả test cuối, merge (nếu được đồng ý).

## Tự kiểm tra

- Đã đi hết checklist.
- Không còn vấn đề `chặn` chưa sửa trước khi merge.
- Test, typecheck, lint sạch sau lần sửa cuối.

## Cập nhật status.md

Không đổi trạng thái (đã cập nhật ở `implement-task`).

## Báo cáo kết thúc

- Số vấn đề theo mức độ, đã sửa / bỏ qua, kết quả test, đã merge hay chưa.
- Cần người dùng quyết: merge.
- Bước tiếp theo: `/implement-task <task tiếp theo>`, hoặc `/manual-test-run <slug>` nếu tính năng đã `đã code`.
