---
name: change-request
description: Xử lý thay đổi yêu cầu hoặc thiết kế - dò mọi chỗ bị ảnh hưởng (docs/project, thiết kế tính năng, db-schema, API, UI, component, test case, traceability, plan, code), trình bày, rồi cập nhật theo thứ tự và lùi trạng thái tính năng. Use for a requirement change / change request.
argument-hint: "<nội dung thay đổi>"
---

# change-request

## Mục đích

Đổi yêu cầu hoặc thiết kế mà không để sót tài liệu, test hay code nào còn theo bản cũ.

## Điều kiện tiên quyết

- Có nội dung thay đổi rõ ràng. Mơ hồ: hỏi lại tới khi nêu được "trước → sau".
- Cây làm việc git sạch.

## Input

- Tham số: nội dung thay đổi (hoặc từ `feedback`, `bug-fix`).
- Toàn bộ nơi có thể bị ảnh hưởng: `docs/project/`, `docs/phases/*/design/`, `docs/design/` (db-schema, api, ui-style, components, ui), `docs/phases/*/test/cases/`, `traceability.md`, `plan.md`, code và test.
- `docs/phases/phase-N/status.md`.

## Các bước

1. Viết lại thay đổi dạng "trước → sau" và lý do.
2. Dò ảnh hưởng: tìm theo từ khóa, mã quy tắc `R-…`, tên bảng/cột/endpoint, tên màn hình/component, mã case. Ghi kết quả theo `templates/impact.md`, đúng thứ tự cập nhật.
3. Trình bày danh sách ảnh hưởng và cách sửa từng chỗ; nêu trạng thái tính năng sẽ bị lùi về đâu.
4. Sau khi duyệt, cập nhật **theo đúng thứ tự** trong `templates/impact.md`:
   1. `docs/project/` (nếu thay đổi yêu cầu khái quát);
   2. thiết kế tính năng (ghi `## Lịch sử thay đổi`, thêm/sửa `R-…`; không tái sử dụng mã đã xóa);
   3. `docs/design/`: `db-schema.md`, `api/*.md` rồi sinh lại `openapi.yaml` và lint như `detailed-design`; style qua `ui-style-update`; component qua `component-design`; mockup như `ui-design`;
   4. test case và `traceability.md` (case cũ không còn đúng: sửa, hoặc thêm dòng `- Đã bỏ: <YYYY-MM-DD>, <lý do>` ngay dưới heading của case, không xóa);
   5. `plan.md`: thêm task mới (đánh số tiếp) cho phần code cần đổi;
   6. code và test: làm qua `/implement-task` với task mới, không sửa trực tiếp ở đây.
5. Lùi trạng thái tính năng trong `status.md` về bước sớm nhất bị ảnh hưởng (ví dụ đổi quy tắc kiểm tra dữ liệu → `thiết kế chi tiết`; chỉ thêm case → `test case`).
6. Thay đổi ảnh hưởng ngoài một tính năng: gọi `decision-log`.
7. Nếu đến từ `feedback`: cập nhật mục `issues.md` tương ứng.

## Điểm dừng

Sau bước 3: người dùng duyệt danh sách ảnh hưởng trước khi sửa bất kỳ file nào.

## Output

- Phân tích ảnh hưởng theo `templates/impact.md` (trong câu trả lời; lưu vào `## Lịch sử thay đổi` của thiết kế dưới dạng tóm tắt).
- Các tài liệu đã cập nhật; task mới trong `plan.md`.

## Tự kiểm tra

- Grep giá trị/tên cũ không còn sót ở tài liệu đang hiệu lực (trừ phần lịch sử).
- Mọi `R-…` mới/sửa có case trong `traceability.md`.
- `openapi.yaml` lint sạch nếu đổi API.

## Cập nhật status.md

Lùi trạng thái tính năng về bước sớm nhất bị ảnh hưởng; ghi `- <ngày> | <slug> | change-request: <tóm tắt> | <người duyệt>` vào `## Nhật ký duyệt`.

## Báo cáo kết thúc

- Danh sách file đã sửa, trạng thái mới của tính năng, task mới, ADR (nếu có).
- Cần người dùng quyết: duyệt lại bước bị lùi.
- Bước tiếp theo: lệnh của bước bị lùi về (ví dụ `/design-review <slug>`), hoặc `/implement-task <task mới>`.
