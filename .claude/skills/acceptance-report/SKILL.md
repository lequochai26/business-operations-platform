---
name: acceptance-report
description: Lập báo cáo nghiệm thu giai đoạn - đối chiếu tiêu chí Xong khi, thống kê test case, vấn đề còn mở, số liệu chạy thật vào report.md, rồi xuất report.xlsx (có ảnh evidence) và report.pdf (qua mẫu HTML), chờ chủ tiệm ký nghiệm thu. Use for phase acceptance report / sign-off.
argument-hint: "<số giai đoạn>"
---

# acceptance-report

## Mục đích

Chứng minh giai đoạn đã đạt tiêu chí, có bằng chứng, để chủ tiệm ký nghiệm thu.

## Điều kiện tiên quyết

- Mọi tính năng trong `status.md` ở trạng thái `đạt`, **hoặc** người dùng nói rõ chấp nhận nghiệm thu với vấn đề còn mở (ghi tên vấn đề).
- Đã có ít nhất một lần chạy trong `docs/phases/phase-N/test/runs/`.

## Input

- Tham số: số giai đoạn N.
- `docs/phases/phase-N/status.md`: tiêu chí "Xong khi", tính năng.
- `docs/phases/phase-N/test/runs/*/results.md` và `evidence/`.
- `docs/phases/phase-N/test/traceability.md`, `docs/phases/phase-N/issues.md`.
- Từ người dùng: số liệu chạy thật (số ngày chạy, số lần checkpoint, RAM, CPU) nếu app chưa tự ghi.

## Các bước

1. Đọc input. Với mỗi tiêu chí "Xong khi": tìm bằng chứng (case đạt, lần chạy, số liệu). Thiếu bằng chứng: hỏi người dùng hoặc ghi `chưa đạt`.
2. Hỏi người dùng số liệu chạy thật còn thiếu.
3. Viết `docs/phases/phase-N/acceptance/report.md` theo `templates/report.md`. Số liệu thống kê lấy đúng từ kết quả mới nhất của từng case.
4. Xuất: `py .claude/skills/acceptance-report/scripts/export_report.py docs/phases/phase-N`. Đọc mọi dòng `Cảnh báo:` (thường là evidence đã bị xóa) và báo người dùng. Lỗi "Đóng file … rồi chạy lại": nhắc người dùng đóng file Excel/PDF đang mở.
5. Gửi người dùng đường dẫn `report.xlsx` và `report.pdf` để kiểm tra và đưa chủ tiệm ký.
6. Sau khi ký: điền mục `## Ký nghiệm thu`, cập nhật `status.md`.

## Điểm dừng

Sau bước 5: chờ chủ tiệm ký nghiệm thu (đồng ý hoặc không, kèm lý do).

## Output

- `docs/phases/phase-N/acceptance/report.md` theo `templates/report.md` (commit).
- `report.xlsx` (sheet "Tổng hợp", "Danh sách case", mỗi case một sheet có ảnh) và `report.pdf` (mẫu `templates/report.html`) — **không commit** (có ảnh evidence chưa che).

## Tự kiểm tra

- Mọi tiêu chí "Xong khi" có kết luận và bằng chứng.
- Số liệu trong `report.md` khớp sheet "Tổng hợp".
- Mọi vấn đề `mở`/`đang xử lý`/`chờ test lại` trong `issues.md` có trong mục `## Vấn đề còn mở`.
- Case `chưa chạy` (sheet "Tổng hợp") bằng 0, hoặc từng case chưa chạy có lý do được người dùng chấp nhận trong `report.md`.
- `git status` không có `report.xlsx`, `report.pdf`, `evidence/` chờ commit.

## Cập nhật status.md

Sau khi chủ tiệm đồng ý: ghi `- <ngày> | giai đoạn | nghiệm thu | <chủ tiệm>` vào `## Nhật ký duyệt`.

## Báo cáo kết thúc

- Đường dẫn báo cáo, kết luận từng tiêu chí, cảnh báo khi xuất.
- Cần người dùng quyết: chủ tiệm ký nghiệm thu; có xóa evidence sau khi xác nhận không.
- Bước tiếp theo: `/phase-kickoff <N+1>`.
