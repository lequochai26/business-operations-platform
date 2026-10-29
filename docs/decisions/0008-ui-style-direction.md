# 0008 – Hướng style UI: kem ấm, sage nhấn, thanh điều hướng xanh đậm

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: docs/design/ui-style.md, docs/design/ui-tokens.css, docs/design/ui-style-preview.html; docs/story/BusinessContext.md mục 2; docs/process/2026-10-29-dev-process-skills-design.md mục 13

## Bối cảnh

- Web app nội bộ dùng nhận diện của tiệm: sage `#8FA284`, kem `#FAF7F0`, xanh đậm `#4E6045`; font Playfair Display, Dancing Script, Be Vietnam Pro.
- Màn hình chính là danh sách dày (bài trong group, khách, báo giá, nhật ký), form cài đặt dài, lịch và màn hình duyệt. Cần dễ đọc, dễ quét, trạng thái rõ.
- Nền tảng: web máy tính trước, responsive và app native sau, nên token phải độc lập nền tảng.
- Ràng buộc tương phản: chữ trắng trên sage chỉ đạt 2.74:1, không đủ 4.5:1 cho chữ thường.
- Các phương án được so sánh bằng mockup 1440×900 trên hai màn hình Hôm nay và Bài trong group.

## Các phương án

### A. Kem ấm, sage nhấn
- Ưu: gọn, nhiều thông tin trên một màn hình; badge nền nhạt chữ đậm dễ đọc; dễ đạt tương phản.
- Nhược: màu tiệm thể hiện kín đáo, giao diện ít "chất tiệm".

### B. Sage thương hiệu đậm
- Ưu: nhận diện mạnh: sidebar xanh đậm, dải tiêu đề sage, Playfair cho tiêu đề khối và số liệu, bo góc lớn, nút dạng viên thuốc.
- Nhược:
  - kém gọn cho danh sách dày;
  - chữ trên dải sage không đạt tương phản (khoảng 2.3:1);
  - số old-style của Playfair khó đọc ("Q11", "18").

### C. Lai: A + thanh điều hướng xanh đậm của B
- Ưu: giữ độ gọn và độ dễ đọc của A; nhận diện rõ hơn nhờ thanh điều hướng nền `#4E6045` chữ kem, logo "Mio" Dancing Script.
- Nhược: thêm một bộ màu riêng cho thanh điều hướng (hover, mục đang chọn, viên số, focus trên nền tối).

## Quyết định

Chọn C (người dùng chốt sau khi xem mockup) vì cân bằng giữa nhận diện của tiệm và nhu cầu vận hành. Kèm các quy tắc:
- sage chỉ dùng để nhấn, không làm nền cho chữ;
- Playfair chỉ cho tiêu đề trang, số liệu dùng Be Vietnam Pro;
- Dancing Script chỉ cho logo.

## Hệ quả

- Được:
  - một nguồn token duy nhất (`ui-style.md` → `ui-tokens.css`), đặt tên độc lập nền tảng;
  - các cặp chữ/nền chính đạt ≥ 4.5:1, viền ô nhập đạt 3:1;
  - mockup và code UI sau này dùng chung một bộ component cơ bản đã có trong preview.
- Mất / rủi ro:
  - giao diện ít "poster" hơn phương án B;
  - khi làm responsive phải thiết kế lại thanh điều hướng (thanh dưới hoặc menu trượt) mà vẫn giữ màu;
  - đổi màu nhận diện về sau phải kiểm lại tương phản của cả nhóm màu `nav`.
