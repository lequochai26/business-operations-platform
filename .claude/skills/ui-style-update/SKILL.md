---
name: ui-style-update
description: Đổi style UI của hệ thống sau khi đã có ui-style.md (đổi màu, font, cỡ chữ, component cơ bản), sinh lại token và preview, rồi cập nhật component và mockup bị ảnh hưởng. Use to change the design system / theme / UI style later.
argument-hint: "<nội dung muốn đổi>"
---

# ui-style-update

## Mục đích

Thay đổi style toàn hệ thống mà vẫn giữ mọi component và mockup đồng bộ.

## Điều kiện tiên quyết

- Đã có `docs/design/ui-style.md`. Chưa có thì dừng, gợi ý `/ui-style-init`.
- Có nội dung thay đổi (tham số). Thiếu thì hỏi.

## Input

- Nội dung muốn đổi (tham số).
- `docs/design/ui-style.md`, `docs/design/ui-tokens.css`.
- `docs/design/components/index.md` và các `components/<tên>.md`: biết component nào dùng token nào.
- `docs/design/ui/`: các mockup màn hình.
- `docs/phases/*/test/cases/`: test case có khía cạnh "Hiển thị".

## Các bước

1. Diễn giải thay đổi thành danh sách token cần đổi (thêm, sửa, xóa) và quy tắc trong các mục diễn giải. Trình bày cho người dùng.
2. Sửa `docs/design/ui-style.md`: khối `## Tokens` và mục diễn giải liên quan; thêm dòng vào `## Lịch sử thay đổi` (ngày, nội dung, lý do).
3. Sinh lại: `py tools/ui/gen_tokens.py docs/design/ui-style.md docs/design/ui-tokens.css`.
4. Cập nhật `docs/design/ui-style-preview.html` nếu thêm/xóa token hoặc component cơ bản, rồi chụp: `py tools/ui/screenshot.py docs/design/ui-style-preview.html --out docs/design/screenshots`.
5. Tìm phần bị ảnh hưởng:
   - token bị xóa hoặc đổi tên: grep `var(--<tên>` trong `docs/design/components/` và `docs/design/ui/`;
   - token đổi giá trị: mọi component và màn hình dùng token đó.
6. Sửa component và mockup dùng token bị xóa/đổi tên. Chụp lại ảnh:
   - component: `py tools/ui/screenshot.py docs/design/components --out docs/design/components/screenshots`;
   - từng màn hình: `py tools/ui/screenshot.py docs/design/ui/<màn hình> --out docs/design/ui/<màn hình>/screenshots`.
7. Liệt kê test case khía cạnh "Hiển thị" của các màn hình bị ảnh hưởng, đề xuất chạy lại bằng `/manual-test-run --retest <mã case>`.
8. Thay đổi lớn (đổi màu chủ đạo, đổi font): gọi `decision-log`.

## Điểm dừng

- Sau bước 1: người dùng xác nhận danh sách token cần đổi.
- Sau bước 4: người dùng duyệt ảnh preview mới **trước** khi sửa component và mockup.

## Output

- `ui-style.md` đã cập nhật (kèm lịch sử), `ui-tokens.css` sinh lại, preview và ảnh mới.
- Component, mockup và ảnh chụp đã cập nhật.
- Danh sách test case cần chạy lại.

## Tự kiểm tra

- Không còn tham chiếu tới token đã xóa (grep `var(--` theo tên cũ trả về rỗng).
- `ui-tokens.css` được sinh lại, không sửa tay.
- Mọi ảnh chụp của phần bị ảnh hưởng đã được chụp lại.

## Cập nhật status.md

Không đổi trạng thái tính năng. Ghi một dòng vào `## Nhật ký duyệt` của giai đoạn đang chạy (nếu có): `- <ngày> | giai đoạn | đổi style: <tóm tắt> | <người duyệt>`.

## Báo cáo kết thúc

- Token đã đổi, component và màn hình đã cập nhật, ADR (nếu có).
- Cần người dùng quyết: có chạy lại các test case hiển thị ngay không.
- Bước tiếp theo: `/manual-test-run --retest <mã case>` cho các case đã liệt kê, hoặc tiếp tục công việc đang dở.
