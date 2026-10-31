<!-- src-section: 0b0fa0b228 f85440737761 -->
# 0008 – Hướng style UI: kem ấm, sage nhấn, thanh điều hướng xanh đậm

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - docs/design/ui-style.md, docs/design/ui-tokens.css, docs/design/ui-style-preview.html;
  - docs/story/BusinessContext.md mục 2;
  - docs/process/2026-10-29-dev-process-skills-design.md mục 13.

**Tóm tắt.** Giao diện dùng nền kem ấm, màu sage chỉ để nhấn, và thanh điều hướng nền xanh đậm. Phương án này cân bằng giữa nhận diện của tiệm và nhu cầu vận hành hằng ngày.

<!-- src-section: 0bc81167ac cf7a78a3e826 -->
## Bối cảnh

- Web app nội bộ dùng nhận diện của tiệm. Màu gồm sage `#8FA284`, kem `#FAF7F0` và xanh đậm `#4E6045`. Font gồm Playfair Display, Dancing Script và Be Vietnam Pro.
- Màn hình chính là các danh sách dày như bài trong group, khách, báo giá, nhật ký. Ngoài ra còn có form cài đặt dài, lịch và màn hình duyệt. Giao diện cần dễ đọc, dễ quét và trạng thái phải rõ.
- Web cho máy tính được làm trước, responsive và app native làm sau. Vì vậy token phải độc lập với nền tảng.
- Có ràng buộc về tương phản. Chữ trắng trên nền sage chỉ đạt 2.74:1, không đủ mức 4.5:1 cho chữ thường.
- Các phương án được so sánh bằng mockup 1440×900 trên hai màn hình: Hôm nay và Bài trong group.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: cec5866a64 55c5ab941261 -->
### A. Kem ấm, sage nhấn

**Ưu**

- Gọn, hiển thị nhiều thông tin trên một màn hình.
- Badge nền nhạt chữ đậm dễ đọc.
- Dễ đạt tương phản.

**Nhược**

- Màu của tiệm thể hiện kín đáo, giao diện ít "chất tiệm".

<!-- src-section: d8735437b4 7b5ccf358d7f -->
### B. Sage thương hiệu đậm

**Ưu**

- Nhận diện mạnh. Sidebar xanh đậm, dải tiêu đề sage, Playfair cho tiêu đề khối và số liệu, bo góc lớn, nút dạng viên thuốc.

**Nhược**

- Kém gọn cho danh sách dày.
- Chữ trên dải sage không đạt tương phản, chỉ khoảng 2.3:1.
- Số kiểu old-style của Playfair khó đọc, ví dụ "Q11", "18".

<!-- src-section: 3c7b08a17b c80347113335 -->
### C. Lai: A kèm thanh điều hướng xanh đậm của B

**Ưu**

- Giữ được độ gọn và độ dễ đọc của A.
- Nhận diện rõ hơn nhờ thanh điều hướng nền `#4E6045` chữ kem và logo "Mio" viết bằng Dancing Script.

**Nhược**

- Phải thêm một bộ màu riêng cho thanh điều hướng: hover, mục đang chọn, viên số, focus trên nền tối.

<!-- src-section: 254160d409 586b59c911bb -->
## Quyết định

Chọn phương án C. Người dùng chốt phương án này sau khi xem mockup.

**Vì sao.** Phương án C cân bằng giữa nhận diện của tiệm và nhu cầu vận hành.

**Quy tắc đi kèm**

- Sage chỉ dùng để nhấn, không làm nền cho chữ.
- Playfair chỉ dùng cho tiêu đề trang. Số liệu dùng Be Vietnam Pro.
- Dancing Script chỉ dùng cho logo.

<!-- src-section: 58c5fdb1ed 1d6f4c552c4a -->
## Hệ quả

**Được**

- Có một nguồn token duy nhất, đặt tên độc lập với nền tảng. Token được viết trong `ui-style.md` rồi sinh ra `ui-tokens.css`.
- Các cặp chữ và nền chính đạt tương phản từ 4.5:1 trở lên. Viền ô nhập đạt 3:1.
- Mockup và code UI sau này dùng chung một bộ component cơ bản đã có trong preview.

**Mất và rủi ro**

- Giao diện ít "poster" hơn phương án B.
- Khi làm responsive phải thiết kế lại thanh điều hướng, ví dụ thành thanh dưới hoặc menu trượt, mà vẫn giữ màu.
- Nếu về sau đổi màu nhận diện thì phải kiểm lại tương phản của cả nhóm màu `nav`.
