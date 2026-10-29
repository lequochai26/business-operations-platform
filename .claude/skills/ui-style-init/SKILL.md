---
name: ui-style-init
description: Chốt style UI cho toàn hệ thống (màu, font, cỡ chữ, khoảng cách, bo góc, breakpoint, component cơ bản) và ghi vào docs/design/ui-style.md, sinh ui-tokens.css và trang preview. Dùng một lần trước giai đoạn 0. Use to define the design system / UI style guide and design tokens.
argument-hint: ""
---

# ui-style-init

## Mục đích

Tạo nguồn chính về style UI để mọi mockup và code UI dùng chung: `docs/design/ui-style.md`, từ đó sinh `docs/design/ui-tokens.css` và trang trưng bày `docs/design/ui-style-preview.html`.

## Điều kiện tiên quyết

- Chưa có `docs/design/ui-style.md`. Nếu đã có: dừng, gợi ý `/ui-style-update`.
- Nên chạy sau `/conventions-init` (không bắt buộc).

## Input

- `docs/story/BusinessContext.md` mục 2: màu `#8FA284`, `#FAF7F0`, `#4E6045`; font Playfair Display, Dancing Script, Be Vietnam Pro.
- `docs/process/2026-10-29-dev-process-skills-design.md` mục 13: lộ trình nền tảng (web máy tính trước → responsive → app native).
- `docs/project/02-features/07-screens-and-settings.md`: danh sách màn hình, vai trò người dùng.
- Câu trả lời của người dùng.

## Các bước

1. Đọc các input. Liệt kê các loại màn hình sẽ có (danh sách, form cài đặt, lịch, màn hình duyệt) để style phục vụ đúng nhu cầu.
2. Đề xuất hướng style tổng thể (2 phương án, khuyến nghị một), hỏi người dùng.
3. Điền `templates/ui-style.md` vào `docs/design/ui-style.md`:
   - giữ nguyên các heading của mẫu;
   - khối yaml dưới `## Tokens` là **nguồn duy nhất** của giá trị; các mục khác chỉ diễn giải, không lặp lại giá trị khác;
   - token đặt tên độc lập nền tảng (không dùng tên riêng của CSS), để sau này sinh được token cho app native;
   - Dancing Script chỉ dùng trang trí, không dùng cho chữ giao diện;
   - kiểm tra độ tương phản chữ/nền tối thiểu 4.5:1 cho chữ thường.
4. Sinh token: `py tools/ui/gen_tokens.py docs/design/ui-style.md docs/design/ui-tokens.css`.
5. Tạo `docs/design/ui-style-preview.html` từ `templates/ui-style-preview.html`, trưng bày mọi component cơ bản ở mọi biến thể và trạng thái.
6. Chụp: `py tools/ui/screenshot.py docs/design/ui-style-preview.html --out docs/design/screenshots`.
7. Gửi người dùng ảnh preview (có thể đăng thành link riêng tư để xem).
8. Gọi `decision-log` cho hướng style đã chọn.

## Điểm dừng

- Sau bước 2: chờ người dùng chọn hướng style.
- Sau bước 7: chờ người dùng duyệt preview. Sửa thì quay lại bước 3.

## Output

- `docs/design/ui-style.md` theo `templates/ui-style.md` (mẫu đã điền sẵn giá trị khởi đầu từ nhận diện của tiệm).
- `docs/design/ui-tokens.css` (sinh tự động).
- `docs/design/ui-style-preview.html` theo `templates/ui-style-preview.html`, ảnh `docs/design/screenshots/ui-style-preview.png`.
- ADR cho hướng style.

## Tự kiểm tra

- `gen_tokens.py` chạy không lỗi.
- Preview dùng **chỉ** biến `var(--...)` từ `ui-tokens.css`, không có mã màu hay cỡ chữ viết cứng.
- Có token `breakpoint` cho responsive về sau.
- Chữ tiếng Việt có dấu hiển thị đúng trong ảnh chụp.

## Cập nhật status.md

Không áp dụng (chạy trước khi có giai đoạn).

## Báo cáo kết thúc

- Đã tạo `ui-style.md`, `ui-tokens.css`, `ui-style-preview.html` và ảnh chụp; ADR đã tạo.
- Cần người dùng quyết: điểm style còn băn khoăn (nếu có).
- Bước tiếp theo: `/test-viewpoints-init`.
