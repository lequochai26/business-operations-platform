---
name: conventions-init
description: Chốt quy ước phát triển cho toàn dự án (cấu trúc thư mục code, đặt tên, nhánh và commit, lint/format/typecheck, test tự động) rồi ghi vào CLAUDE.md. Dùng một lần trước giai đoạn 0, hoặc khi muốn làm lại quy ước. Use to set up project coding conventions, naming, branching, commit rules.
argument-hint: ""
---

# conventions-init

## Mục đích

Chốt các quy ước mà mọi skill code về sau (`implement-task`, `tdd`, `review-code`) phải tuân theo, và ghi vào mục `## Quy ước` của `CLAUDE.md`.

## Điều kiện tiên quyết

- Mục `## Quy ước` trong `CLAUDE.md` còn ghi "Chưa chốt", **hoặc** người dùng nói rõ muốn làm lại.
- Nếu đã chốt mà người dùng không yêu cầu làm lại: dừng, báo quy ước hiện tại và gợi ý `/change-request` nếu muốn đổi một phần.

## Input

- `docs/project/04-technical.md`: stack đã chốt (NestJS, BullMQ, PostgreSQL, Playwright, Oracle ARM).
- `docs/process/2026-10-29-dev-process-skills-design.md` mục 9: quy ước test tự động bắt buộc.
- `poc/fb-post-crawler-poc/` (nếu có): cấu trúc, cách viết test, cấu hình TypeScript đang dùng.
- Câu trả lời của người dùng cho từng nhóm quy ước.

## Các bước

1. Đọc các input. Ghi nhận những gì POC đã làm và nên giữ.
2. Đi lần lượt 5 nhóm theo `templates/conventions-section.md`. Với **mỗi nhóm**:
   - đưa 2–3 phương án, mỗi phương án một dòng ưu/nhược;
   - nêu phương án khuyến nghị và lý do;
   - hỏi người dùng, **một nhóm mỗi lượt**.
3. Nhóm "Test tự động" phải bao gồm đủ các ý ở spec mục 9: đồng hồ truyền vào, property-based test, integration test với DB thật trong Docker, contract test, không skip test mà không báo.
4. Ghi kết quả vào `CLAUDE.md`, thay toàn bộ nội dung dưới `## Quy ước` theo mẫu `templates/conventions-section.md`. Mỗi quy ước phải cụ thể đến mức kiểm tra được (ví dụ "tên file kebab-case", không phải "đặt tên rõ ràng"). Ghi cả các lệnh chạy test, typecheck, lint.
5. Với mỗi nhóm có chọn giữa nhiều phương án: gọi `decision-log`.

## Điểm dừng

- Sau mỗi nhóm: chờ người dùng chọn phương án.
- Trước khi ghi `CLAUDE.md`: trình bày toàn bộ mục `## Quy ước` sẽ ghi, chờ người dùng duyệt.

## Output

- Mục `## Quy ước` trong `CLAUDE.md` theo `templates/conventions-section.md` (ví dụ đã điền: `templates/example-conventions-section.md`).
- ADR trong `docs/decisions/` cho các lựa chọn lớn.

## Tự kiểm tra

- Đủ 5 nhóm heading cấp 3 của mẫu.
- Có lệnh chạy test, typecheck, lint cụ thể.
- Có quy tắc đặt tên nhánh mà `implement-task` dùng được (chứa `phase-N` và mã task).
- Không quy ước nào mâu thuẫn với `docs/project/04-technical.md`.

## Cập nhật status.md

Không áp dụng (chạy trước khi có giai đoạn).

## Báo cáo kết thúc

- Đã ghi mục `## Quy ước` vào `CLAUDE.md`, liệt kê các ADR đã tạo.
- Cần người dùng quyết: các điểm còn bỏ ngỏ (nếu có).
- Bước tiếp theo: `/ui-style-init`.
