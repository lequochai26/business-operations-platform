---
name: detailed-design
description: Viết thiết kế chi tiết cho một tính năng của giai đoạn (module, DB, API, màn hình và quy tắc kiểm tra dữ liệu, job, trạng thái, tích hợp, lỗi, tham số) từ tài liệu khái quát; cập nhật db-schema.md, api/*.md và sinh openapi.yaml. Use for detailed design / technical design of a feature.
argument-hint: "<slug tính năng>"
---

# detailed-design

## Mục đích

Biến yêu cầu khái quát trong `docs/project/` thành thiết kế đủ chi tiết để thiết kế test case và code mà không phải đoán.

## Điều kiện tiên quyết

- Có `docs/phases/phase-N/status.md` (N = giai đoạn đang mở) và slug nằm trong bảng `## Tính năng`.
- Trạng thái tính năng là `chưa bắt đầu` hoặc `thiết kế chi tiết` (đang làm dở). Trạng thái sau đó: dừng, gợi ý `/change-request` nếu muốn sửa thiết kế đã duyệt.

## Input

- Tham số: slug tính năng.
- `docs/phases/phase-N/status.md`: mã 3 chữ, có màn hình hay không, mục tài liệu liên quan.
- Các mục `docs/project/` ghi trong cột `Tài liệu liên quan`, cùng `03-data-model.md`, `04-technical.md`, `06-open-issues-and-assumptions.md`.
- `docs/design/db-schema.md`, `docs/design/api/*.md`: thiết kế dùng chung đã có.
- Các file thiết kế đã duyệt trong `docs/phases/*/design/`: giữ thống nhất tên, kiểu, mã lỗi.
- `CLAUDE.md` mục `## Quy ước`: quy tắc đặt tên bảng, cột, endpoint.

## Các bước

1. Đặt trạng thái tính năng `thiết kế chi tiết` trong `status.md`.
2. Đọc input. Liệt kê mọi yêu cầu, quy tắc, con số trong tài liệu khái quát liên quan tới tính năng.
3. Viết `docs/phases/phase-N/design/<slug>.md` theo `templates/feature-design.md`, đủ mọi heading; heading không áp dụng ghi "Không áp dụng" kèm lý do.
   - Mỗi quy tắc kiểm tra dữ liệu, quy tắc nghiệp vụ, ràng buộc phân quyền là một dòng có mã `R-<ABC>-<nn>`. Test case và traceability trỏ tới mã này.
   - Mỗi trường nhập ghi: kiểu, bắt buộc, khoảng/định dạng, duy nhất, giá trị mặc định, thông báo lỗi nguyên văn.
   - Mỗi tham số cài đặt ghi: mặc định, khoảng hợp lệ, nguồn (tài liệu khái quát hay quyết định mới).
   - Không tự bịa điều tài liệu khái quát chưa nói: ghi vào `## Câu hỏi mở` kèm đề xuất.
4. Cập nhật `docs/design/db-schema.md` (tạo từ `templates/db-schema.md` nếu chưa có): thêm/sửa bảng; ghi `## Lịch sử thay đổi`. File thiết kế tính năng chỉ ghi tóm tắt thay đổi DB và trỏ tới đây.
5. Cập nhật `docs/design/api/<resource>.md` (tạo từ `templates/api-resource.md` nếu chưa có), mỗi endpoint đủ các mục cố định. File thiết kế tính năng chỉ liệt kê endpoint và trỏ tới đây.
6. Sinh lại `docs/design/api/openapi.yaml` (OpenAPI 3.1) từ **toàn bộ** `docs/design/api/*.md`. Dòng đầu: `# File sinh tự động từ docs/design/api/*.md, không sửa tay.` Không thêm gì không có trong Markdown.
7. Lint: `npx --yes @redocly/cli@2.72.0 lint docs/design/api/openapi.yaml`. Lỗi thì sửa Markdown hoặc cách sinh, sinh lại tới khi sạch.
8. Gọi `decision-log` cho quyết định ảnh hưởng ngoài tính năng này.
9. Trình bày tóm tắt thiết kế và danh sách `## Câu hỏi mở` cho người dùng. Cập nhật thiết kế theo câu trả lời, ghi vào `## Lịch sử thay đổi`.

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

Sau bước 9: người dùng trả lời câu hỏi mở và duyệt thiết kế. Chưa duyệt thì không đổi trạng thái tiếp.

## Output

- `docs/phases/phase-N/design/<slug>.md` theo `templates/feature-design.md` (ví dụ: `templates/example-feature-design.md`).
- `docs/design/db-schema.md` theo `templates/db-schema.md`.
- `docs/design/api/<resource>.md` theo `templates/api-resource.md`; `docs/design/api/openapi.yaml`.

## Tự kiểm tra

- Mọi yêu cầu liệt kê ở bước 2 đã nằm trong thiết kế hoặc trong `## Câu hỏi mở`.
- Mọi quy tắc có mã `R-<ABC>-<nn>`, không trùng.
- Mọi trường nhập có thông báo lỗi nguyên văn.
- Không vi phạm các điều trong `docs/project/01-overview.md` mục 5.
- `redocly lint` sạch.

## Cập nhật status.md

- Bắt đầu: `thiết kế chi tiết`.
- Sau khi duyệt: `UI` nếu tính năng có màn hình, ngược lại `test case`. Ghi `- <ngày> | <slug> | duyệt thiết kế chi tiết | <người duyệt>` vào `## Nhật ký duyệt`.
- Nếu `status.md` chưa có mã 3 chữ cho tính năng: đặt mã và ghi vào cột `Mã`.

## Báo cáo kết thúc

- Đã ghi file thiết kế, các thay đổi `db-schema.md`, `api/*.md`, `openapi.yaml`, ADR (nếu có).
- Cần người dùng quyết: câu hỏi mở còn lại.
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: `/ui-design <slug>` nếu có màn hình, ngược lại `/test-case-design <slug>`.
