---
name: implementation-plan
description: Chia các thiết kế đã duyệt của giai đoạn thành task code nhỏ có thứ tự phụ thuộc, mỗi task ghi file sửa, test tự động cần viết, test case manual liên quan và tiêu chí xong; ghi docs/phases/phase-N/plan.md. Use to write the implementation plan / task breakdown for a phase.
argument-hint: "[slug tính năng, nếu chỉ lập cho một phần]"
---

# implementation-plan

## Mục đích

Tạo `docs/phases/phase-N/plan.md`: danh sách task code để `/implement-task` làm lần lượt.

## Điều kiện tiên quyết

- Mọi tính năng trong `status.md` ở trạng thái `đã duyệt thiết kế` trở đi, **hoặc** người dùng chỉ định lập kế hoạch cho một phần (tham số slug) và tính năng đó đã duyệt thiết kế.
- `CLAUDE.md` mục `## Quy ước` đã chốt.
- Nếu `plan.md` đã có: chỉ thêm task mới (đánh số tiếp), không đánh số lại task cũ.

## Input

- `docs/phases/phase-N/status.md`: danh sách tính năng, thứ tự.
- Mọi `docs/phases/phase-N/design/<slug>.md` đã duyệt, `docs/design/db-schema.md`, `docs/design/api/*.md`, `docs/design/ui/`, `docs/design/components/`.
- `docs/phases/phase-N/test/cases/*.md`: để gắn case manual vào task.
- Code hiện có trong repo; `poc/fb-post-crawler-poc/` và `docs/project/04-technical.md` mục 2 (phần POC dùng lại).
- `CLAUDE.md` mục `## Quy ước`: cấu trúc thư mục, lệnh test.

## Các bước

1. Liệt kê mọi thứ cần làm từ thiết kế: migration, module, API, job, component UI, màn hình, tích hợp, phần chuyển từ POC.
2. Chia thành task. Mỗi task:
   - là đơn vị nhỏ nhất có chu trình test riêng và đáng review riêng (một migration + repository, một endpoint, một màn hình…);
   - gộp phần dựng khung, cấu hình vào task cần nó; không tạo task "chỉ cấu hình";
   - làm và review được trong một lần.
3. Sắp thứ tự theo phụ thuộc: hạ tầng và DB trước, rồi logic, API, UI. Task đầu tiên của dự án (nếu chưa có code) là dựng khung repo theo `## Quy ước`.
4. Viết từng task theo `templates/plan.md`: mã `T<nn>` tăng dần, các mục cố định. `Test tự động` ghi tên test và điều nó khẳng định; `Test case manual` ghi mã case sẽ chạy được sau task.
5. Kiểm tra: mọi `R-…` trong thiết kế được ít nhất một task hiện thực; mọi case manual gắn với ít nhất một task.

## Điểm dừng

Sau bước 5: người dùng duyệt kế hoạch.

## Output

`docs/phases/phase-N/plan.md` theo `templates/plan.md` (ví dụ: `templates/example-plan.md`).

## Tự kiểm tra

- Không task nào phụ thuộc vòng.
- Mọi task có `Tiêu chí xong` kiểm tra được bằng lệnh hoặc quan sát.
- Mọi `R-…` và mọi case manual đã được gắn.
- Mọi task có `- Trạng thái: chưa làm`.

## Cập nhật status.md

Ghi `- <ngày> | giai đoạn | duyệt kế hoạch code | <người duyệt>` vào `## Nhật ký duyệt`. Không đổi trạng thái tính năng.

## Báo cáo kết thúc

- Số task, thứ tự, task phụ thuộc dài nhất.
- Cần người dùng quyết: duyệt kế hoạch.
- Bước tiếp theo: `/implement-task T01`.
