---
name: decision-log
description: Ghi lại một quyết định quan trọng (ADR) vào docs/decisions/ - khi chọn giữa nhiều phương án và ảnh hưởng rộng hơn một tính năng (thư viện, kiến trúc, quy ước chung, style). Được các skill thiết kế tự gọi, hoặc gọi tay. Use to record an architecture decision record.
argument-hint: "<tiêu đề quyết định>"
---

# decision-log

## Mục đích

Lưu lý do của các quyết định lớn để sau này không phải bàn lại từ đầu.

## Điều kiện tiên quyết

- Quyết định thỏa **cả hai**: chọn giữa ít nhất 2 phương án, **và** ảnh hưởng rộng hơn một tính năng (thư viện, kiến trúc, quy ước chung, style, hạ tầng).
- Không thỏa: không tạo ADR. Quyết định chỉ thuộc một tính năng thì ghi trong mục `## Câu hỏi mở` / `## Lịch sử thay đổi` của file thiết kế tính năng đó. Báo lại cho người gọi.

## Input

- Tiêu đề (tham số) hoặc ngữ cảnh từ skill gọi.
- Bối cảnh, các phương án đã cân nhắc, lý do chọn. Thiếu thì hỏi người dùng.
- `docs/decisions/`: để lấy số tiếp theo và tìm quyết định cũ bị thay thế.

## Các bước

1. Kiểm tra điều kiện tiên quyết.
2. Tìm ADR cũ cùng chủ đề trong `docs/decisions/`. Nếu quyết định mới thay thế ADR cũ: sửa dòng `- Trạng thái:` của ADR cũ thành `thay thế bởi <NNNN mới>`.
3. Số `NNNN` = số lớn nhất hiện có + 1 (bắt đầu `0001`). Slug: kebab-case tiếng Anh, ngắn.
4. Viết `docs/decisions/NNNN-<slug>.md` theo `templates/adr.md`. Trạng thái `chấp nhận` nếu người dùng đã đồng ý, ngược lại `đề xuất`.

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

Không có điểm dừng riêng. Khi gọi tay mà thiếu thông tin phương án hoặc lý do: hỏi trước khi viết.

## Output

`docs/decisions/NNNN-<slug>.md` theo `templates/adr.md` (ví dụ: `templates/example-adr.md`).

## Tự kiểm tra

- Có ít nhất 2 phương án, mỗi phương án có ưu và nhược.
- Mục `## Hệ quả` nêu cả mặt được và mặt mất.
- Nếu thay thế ADR cũ: ADR cũ đã được cập nhật trạng thái.

## Cập nhật status.md

Không đổi trạng thái tính năng.

## Báo cáo kết thúc

- Đã ghi `docs/decisions/NNNN-<slug>.md` (và ADR bị thay thế, nếu có).
- Cần người dùng quyết: chuyển trạng thái `đề xuất` → `chấp nhận` (nếu chưa).
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: quay lại skill đang làm dở.
