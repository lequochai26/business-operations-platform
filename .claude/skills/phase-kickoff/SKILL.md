---
name: phase-kickoff
description: Mở một giai đoạn của roadmap - chốt phạm vi, danh sách tính năng (slug, mã 3 chữ), vấn đề đang chặn và tạo docs/phases/phase-N/status.md. Dùng khi bắt đầu giai đoạn mới. Use to start/kick off a roadmap phase.
argument-hint: "<số giai đoạn>"
---

# phase-kickoff

## Mục đích

Tạo `docs/phases/phase-N/status.md`: nguồn sự thật về phạm vi và trạng thái của giai đoạn N. Mọi skill sau đều đọc file này.

## Điều kiện tiên quyết

- Mục `## Quy ước` trong `CLAUDE.md` đã chốt (không còn "Chưa chốt").
- Đã có `docs/design/ui-style.md` và `docs/testing/viewpoints.md`.
- Chưa có `docs/phases/phase-N/status.md`.
- Giai đoạn N-1 (nếu có) đã nghiệm thu (có dòng `nghiệm thu` trong `## Nhật ký duyệt`), **hoặc** người dùng nói rõ chấp nhận chạy song song.
- Thiếu điều kiện nào: dừng, báo lệnh cần chạy trước.

## Input

- Tham số: số giai đoạn N.
- `docs/project/05-roadmap.md`: mục "Giai đoạn N": mục tiêu, danh sách việc, tiêu chí "Xong khi".
- `docs/project/06-open-issues-and-assumptions.md`: thông tin còn thiếu, quyết định chưa chốt.
- `docs/project/02-features/*`: để gắn tính năng với mục tài liệu liên quan.
- `docs/phases/phase-(N-1)/status.md` và `issues.md` (nếu có): việc còn tồn.

## Các bước

1. Đọc mục giai đoạn N trong roadmap. Chép tiêu chí "Xong khi" nguyên văn.
2. Chia danh sách việc thành **tính năng**: mỗi tính năng là một khối thiết kế được độc lập (một màn hình + API + bảng, hoặc một job). Với mỗi tính năng:
   - slug kebab-case, mã 3 chữ in hoa không trùng trong giai đoạn;
   - có màn hình hay không;
   - mục tài liệu khái quát liên quan (file + mục).
3. Tìm vấn đề đang chặn: thông tin còn thiếu trong `06-...md` mà tính năng cần; hạ tầng chưa có; việc tồn từ giai đoạn trước.
4. Đề xuất thứ tự thiết kế các tính năng (tính năng nền như đăng nhập trước).
5. Trình bày phạm vi cho người dùng.
6. Sau khi duyệt, ghi `docs/phases/phase-N/status.md` theo `templates/status.md`. Mọi tính năng ở trạng thái `chưa bắt đầu`.
7. Tạo `docs/phases/phase-N/issues.md` rỗng theo mẫu `.claude/skills/feedback/templates/issues.md`.

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

Sau bước 5: người dùng xác nhận phạm vi, danh sách tính năng và thứ tự.

## Output

- `docs/phases/phase-N/status.md` theo `templates/status.md` (ví dụ: `templates/example-status.md`).
- `docs/phases/phase-N/issues.md` rỗng.

## Tự kiểm tra

- Mọi việc trong mục giai đoạn N của roadmap thuộc ít nhất một tính năng, hoặc được ghi rõ "ngoài phạm vi" kèm lý do.
- Slug và mã 3 chữ không trùng.
- Cột `Trạng thái` chỉ dùng đúng các chuỗi: `chưa bắt đầu`, `thiết kế chi tiết`, `UI`, `test case`, `đã duyệt thiết kế`, `đang code`, `đã code`, `đang manual test`, `đạt`.

## Cập nhật status.md

Tạo mới. Ghi dòng `- <ngày> | giai đoạn | mở giai đoạn | <người duyệt>` vào `## Nhật ký duyệt`.

## Báo cáo kết thúc

- Đã tạo `status.md` với <n> tính năng, <m> vấn đề đang chặn.
- Cần người dùng quyết: các vấn đề đang chặn cần ai xử lý.
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: `/detailed-design <slug của tính năng đầu tiên>`.
