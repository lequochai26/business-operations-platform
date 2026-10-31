# Giai đoạn 0 – Nền móng

## Phạm vi

- Mục tiêu: có khung app chạy được bằng Docker trên máy local, dời được lên máy chủ sau này mà không sửa code, và kiểm chứng những điều kiện kỹ thuật lớn.
- Chạy Docker Compose trên máy local (x64). Image phải build được cho cả linux/amd64 và linux/arm64 (ADR `0009-local-first-deployment`).
- Email khẩn khi app tự dừng được làm sớm từ giai đoạn 1 (thuộc `emergency-stop`).
- Ngoài phạm vi:
  - Dựng VM Oracle, HTTPS, tên miền: chuyển sang mục "Triển khai lên máy chủ" của roadmap vì chưa đăng ký được Oracle Free.
  - Lọc từ khóa, lọc tuổi bài, phân loại AI, comment: giai đoạn 1.
  - Cài PWA, web push: giai đoạn 1, cần HTTPS.
  - Màn hình quản lý tài khoản thợ: giai đoạn 2, khi thợ bắt đầu dùng app. Giai đoạn 0 tạo tài khoản bằng lệnh CLI.
  - Trang chính đầy đủ và Nhật ký hệ thống đầy đủ: giai đoạn 0 chỉ có khối "Trạng thái tự động hóa" và sự kiện tự dừng.

## Tiêu chí Xong khi

- Chạy quét bằng Docker trên máy local, **tổng cộng ít nhất 24 giờ** (có thể chia nhiều lần), bằng tài khoản phụ mà không bị đăng xuất, hoặc nếu bị thì app tự dừng và báo đúng.
- Bài mới trong group xuất hiện trong cơ sở dữ liệu trong vòng 1 chu kỳ quét.
- Ghi lại mức RAM và CPU thực tế của từng container, để ước lượng cho máy chủ.

## Tính năng

Thứ tự thiết kế đề xuất: app-skeleton → auth → crawler-verification → group-settings → crawl-settings → fb-account-session → group-crawl-job → emergency-stop → backup

| Slug | Mã | Có màn hình | Tài liệu liên quan | Trạng thái |
|---|---|---|---|---|
| app-skeleton | SKL | không | 04-technical.md mục 1, 3; 05-roadmap.md giai đoạn 0; ADR 0009 | đã duyệt thiết kế |
| auth | AUT | có | 07-screens-and-settings.md Yêu cầu chung, mục 2 Người dùng; 03-data-model.md mục 1; 04 mục 7 | đã duyệt thiết kế |
| crawler-verification | VRF | không | 05-roadmap.md giai đoạn 0; 04 mục 2; spec POC mục 9 (checklist), mục 10 | chưa bắt đầu |
| group-settings | GRP | có | 07 mục 2 Group; 01-group-auto-comment.md mục 2; 03 mục 2 | chưa bắt đầu |
| crawl-settings | CRS | có | 07 mục 2 Quét và comment (lịch quét); 01 mục 2 Lịch quét, Giới hạn lượt quét | chưa bắt đầu |
| fb-account-session | ACC | có | 07 mục 2 Tài khoản vận hành; 04 mục 4.2 | chưa bắt đầu |
| group-crawl-job | CRW | không | 01 mục 2, 10; 03 mục 2, 7; 04 mục 2, 3 | chưa bắt đầu |
| emergency-stop | STP | có | 01 mục 8; 07 Yêu cầu chung (email khẩn), mục 1.1; 03 mục 7 | chưa bắt đầu |
| backup | BAK | không | 04 mục 7; ADR 0009 | chưa bắt đầu |

Ghi chú phạm vi từng tính năng:
- `app-skeleton`: monorepo, NestJS, PostgreSQL, Redis, BullMQ, Docker Compose đa kiến trúc; `browser-worker` là tiến trình riêng chỉ nối Redis (ADR 0011); bảng cài đặt chung; `Clock`; cách đo RAM/CPU từng container.
- `auth`: đăng nhập 2 vai trò, giữ phiên lâu, giới hạn đăng nhập sai, đổi mật khẩu, tạo tài khoản bằng CLI, khung app và menu theo vai trò.
- `crawler-verification`: chạy bằng code POC; hoàn thành checklist nghiệm thu thủ công còn dở (7 mục) và kiểm chứng `CHRONOLOGICAL`, `createdAt`, nội dung bị cắt, ảnh cỡ đầy đủ. Kết quả đưa vào thiết kế `group-crawl-job`.
- `group-settings`: thêm/xóa group, các công tắc, giới hạn riêng, ghi chú luật, trạng thái truy cập.
- `crawl-settings`: giờ vàng, chu kỳ trong/ngoài giờ vàng, giờ nghỉ, số lượt mở group tối đa mỗi ngày, giới hạn scroll.
- `fb-account-session`: trạng thái phiên, kiểm tra phiên định kỳ, Xvfb + noVNC trong container, hướng dẫn đăng nhập lại.
- `group-crawl-job`: chuyển crawler POC, job quét định kỳ không chồng chu kỳ, xáo thứ tự group, merge bài theo quy tắc POC, lưu lượt quét, xử lý group không truy cập được.
- `emergency-stop`: nút dừng khẩn cấp và chạy lại, tự dừng khi phiên hết hạn hoặc checkpoint (lưu ảnh màn hình + HTML), email khẩn, khối "Trạng thái tự động hóa" trên trang chính.
- `backup`: `pg_dump` + ảnh hằng đêm ra thư mục cấu hình được, giữ 7 bản; đẩy lên Object Storage tùy chọn; dọn debug dump cũ hơn 14 ngày.

## Vấn đề đang chặn

- Docker Desktop đã cài nhưng lệnh `docker` chưa có trong PATH (hoặc Docker Desktop chưa chạy) — ảnh hưởng: app-skeleton và mọi tính năng cần `pnpm test:int` — người xử lý: Hải
- Cần danh sách 6 group (link hoặc ID) và tài khoản phụ sẵn sàng để tự đăng nhập qua trình duyệt — ảnh hưởng: crawler-verification, fb-account-session, group-crawl-job — người xử lý: chủ tiệm
- Cần tài khoản Gmail gửi thư kèm mật khẩu ứng dụng cho email khẩn — ảnh hưởng: emergency-stop — người xử lý: Hải

## Nhật ký duyệt

- 2026-10-29 | giai đoạn | mở giai đoạn | Hải
- 2026-10-29 | app-skeleton | duyệt thiết kế chi tiết | Hải
- 2026-10-31 | app-skeleton | duyệt thiết kế | Hải
- 2026-10-31 | auth | duyệt thiết kế chi tiết | Hải
- 2026-10-31 | auth | duyệt UI | Hải
- 2026-10-31 | giai đoạn | đổi style: thêm quy ước vị trí thông báo, không đổi token (ADR 0016) | Hải
- 2026-10-31 | auth | duyệt thiết kế | Hải
