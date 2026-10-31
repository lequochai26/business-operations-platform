---
name: design-review
description: Review thiết kế chi tiết, mockup và test case của một tính năng theo checklist (khớp yêu cầu, không mâu thuẫn, không mơ hồ, đủ quy tắc và trạng thái lỗi, đủ case, không vi phạm lằn ranh đỏ), sửa sau khi người dùng đồng ý rồi chốt duyệt thiết kế. Use to review a feature design and its test cases.
argument-hint: "<slug tính năng>"
---

# design-review

## Mục đích

Bắt lỗi thiết kế và thiếu sót test case trước khi code, rồi chốt duyệt thiết kế của tính năng.

## Điều kiện tiên quyết

- Trạng thái tính năng là `test case` và đã có `docs/phases/phase-N/test/cases/<slug>.md`.
- Thiếu: dừng, gợi ý `/test-case-design <slug>`.

## Input

- Tham số: slug tính năng.
- `docs/phases/phase-N/design/<slug>.md`.
- `docs/design/ui/<màn hình>/` (nếu có).
- `docs/phases/phase-N/test/cases/<slug>.md`, `docs/phases/phase-N/test/traceability.md`.
- Các mục `docs/project/` liên quan (cột `Tài liệu liên quan` trong `status.md`) và `docs/project/01-overview.md` mục 5.
- `docs/design/db-schema.md`, `docs/design/api/*.md`, thiết kế đã duyệt của các tính năng khác.

## Các bước

1. Đi lần lượt từng mục trong `checklists/design-review.md`. Mỗi chỗ không đạt là một điểm review.
2. Ghi các điểm vào `docs/phases/phase-N/design/reviews/<slug>-review.md` theo `templates/review.md`: mức độ (`chặn` | `nên sửa` | `gợi ý`), vị trí, vấn đề, đề xuất.
3. Trình bày danh sách cho người dùng, hỏi điểm nào sửa.
4. Sửa các điểm được đồng ý ở đúng nơi (thiết kế, mockup, test case, traceability, `db-schema.md`, `api/*.md`; sinh lại `openapi.yaml` và lint như `detailed-design` nếu đổi API). Ghi `## Lịch sử thay đổi` ở file bị sửa.
5. Điền `- Kết quả:` cho từng điểm (`đã sửa` | `không sửa: <lý do>`).
6. Quyết định ảnh hưởng ngoài tính năng: gọi `decision-log`.

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

- Sau bước 3: người dùng chọn điểm nào sửa.
- Sau bước 5: người dùng duyệt thiết kế. Không còn điểm `chặn` nào chưa xử lý thì mới được duyệt.

## Output

- `docs/phases/phase-N/design/reviews/<slug>-review.md` theo `templates/review.md`.
- Các file thiết kế, mockup, test case đã sửa.

## Tự kiểm tra

- Đã đi hết mọi mục trong `checklists/design-review.md`.
- Mọi điểm có `- Kết quả:`.
- Không còn điểm `chặn` với kết quả `không sửa`.

## Cập nhật status.md

Sau khi duyệt: trạng thái `test case` → `đã duyệt thiết kế`; ghi `- <ngày> | <slug> | duyệt thiết kế | <người duyệt>` vào `## Nhật ký duyệt`. Trong file thiết kế, đổi `- Trạng thái:` thành `đã duyệt ngày <ngày>`.

## Báo cáo kết thúc

- Số điểm theo mức độ, số đã sửa / không sửa.
- Cần người dùng quyết: duyệt thiết kế.
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: `/detailed-design <slug tiếp theo>` nếu còn tính năng chưa thiết kế, ngược lại `/implementation-plan`.
