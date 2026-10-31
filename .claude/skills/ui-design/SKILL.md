---
name: ui-design
description: Thiết kế màn hình (mockup HTML khung 1440x900, đủ các trạng thái, ảnh chụp) cho tính năng có giao diện, sau thiết kế chi tiết và trước thiết kế test case; gọi component-design cho phần dùng chung. Use for UI design / screen mockups / wireframes of a feature.
argument-hint: "<slug tính năng>"
---

# ui-design

## Mục đích

Cho người dùng thấy trước màn hình trông thế nào, chỉnh và chốt trước khi thiết kế test case và code.

## Điều kiện tiên quyết

- Tính năng có màn hình (cột `Có màn hình` = `có` trong `status.md`) và trạng thái là `UI`.
- Đã có `docs/design/ui-style.md` và `docs/design/ui-tokens.css`.
- Không thỏa: dừng, báo lệnh cần chạy trước.

## Input

- Tham số: slug tính năng.
- `docs/phases/phase-N/design/<slug>.md`: màn hình, trường, quy tắc `R-…`, thông báo lỗi nguyên văn, phân quyền.
- `docs/design/ui-style.md`, `docs/design/ui-tokens.css`.
- `docs/design/components/index.md`: component đã có.

## Các bước

1. Với mỗi màn hình trong thiết kế chi tiết, tạo thư mục `docs/design/ui/<màn hình>/` (kebab-case).
2. Xác định phần giao diện dùng lại được: xuất hiện ở từ 2 màn hình trở lên, hoặc mang tính chung (badge trạng thái, thẻ chờ duyệt, ô chọn khung giờ…). Với mỗi phần: gọi `component-design`.
3. Vẽ mỗi trạng thái thành một file từ `templates/mockup-state.html`: `normal.html`, `empty.html`, `loading.html`, `validation-error.html`, `system-error.html`, `forbidden.html`. Trạng thái không áp dụng thì không vẽ và ghi lý do trong `notes.md`.
   - Khung 1440×900; chỉ dùng `var(--...)`; nhúng component bằng `<script src>` + thẻ `mio-…`, không chép code component.
   - Dữ liệu mẫu thực tế, tiếng Việt có dấu; thông báo lỗi đúng nguyên văn thiết kế chi tiết.
   - Đặt thông báo theo `ui-style.md` mục "Vị trí thông báo". Thông báo dùng chung nhiều màn hình mà đọc sai nghĩa ở màn đang vẽ: báo người dùng, sửa câu trong thiết kế chi tiết (bước 7).
4. Tạo `index.html` liệt kê link tới từng trạng thái, và `notes.md` theo `templates/screen-notes.md`.
5. Chụp: `py tools/ui/screenshot.py docs/design/ui/<màn hình> --out docs/design/ui/<màn hình>/screenshots`.
6. Gửi người dùng ảnh chụp (có thể đăng thành link riêng tư để chủ tiệm xem và góp ý).
7. Nếu chỉnh UI làm đổi trường, quy tắc hoặc thông báo: cập nhật ngược `docs/phases/phase-N/design/<slug>.md`, ghi `## Lịch sử thay đổi` ở cả hai nơi.
8. Quyết định UI ảnh hưởng nhiều màn hình (ví dụ bố cục điều hướng chung): gọi `decision-log`.

## Điểm dừng

Sau bước 6: người dùng duyệt mockup. Sửa thì quay lại bước 3.

## Output

- `docs/design/ui/<màn hình>/`: các file trạng thái, `index.html`, `notes.md` theo `templates/screen-notes.md`, `screenshots/`.
- Component mới/sửa (qua `component-design`).
- Thiết kế chi tiết đã cập nhật (nếu có thay đổi).

## Tự kiểm tra

- Mọi màn hình trong thiết kế chi tiết đều có mockup.
- Mọi quy tắc `R-…` có thông báo lỗi hiện trên màn hình đều được minh họa ở `validation-error.html`.
- Mockup vai trò không có quyền (`forbidden.html`) khớp quy tắc phân quyền.
- Thông báo đặt đúng `ui-style.md` mục "Vị trí thông báo" (ADR 0016): lỗi theo trường dưới ô; thông báo cấp form trong vùng thông báo ngay trên hàng nút gửi (cả trong hộp thoại); thông báo cấp trang dưới đầu trang; thành công dùng toast.
- Không có mã màu, cỡ chữ viết cứng; ảnh chụp không lỗi script, chữ tiếng Việt đúng.

## Cập nhật status.md

Sau khi duyệt: trạng thái `UI` → `test case`; ghi `- <ngày> | <slug> | duyệt UI | <người duyệt>` vào `## Nhật ký duyệt`.

## Báo cáo kết thúc

- Các màn hình và trạng thái đã vẽ, component đã tạo/dùng, thay đổi ngược vào thiết kế chi tiết.
- Cần người dùng quyết: duyệt mockup.
- Bước tiếp theo: `/test-case-design <slug>`.
