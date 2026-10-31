# 0013 – Profile trình duyệt nằm trong named volume riêng

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan: phase-0 app-skeleton (R-SKL-20, biến `BROWSER_PROFILE_DIR`), fb-account-session, backup; docs/project/04-technical.md mục 4.2, 7; ADR 0009; review `docs/phases/phase-0/design/reviews/app-skeleton-review.md` RV-06

## Bối cảnh

- Giai đoạn 0 chạy Docker Desktop trên Windows (ADR 0009). `MIO_DATA_DIR` nhiều khả năng là thư mục trên ổ NTFS, gắn vào container qua bind mount.
- Bind mount từ ổ Windows không giữ quyền Unix: `chmod 700` cho thư mục profile không có tác dụng. Truy cập file chậm, khóa file SQLite (cookie, phiên đăng nhập của Chromium) kém tin cậy, ảnh hưởng bài chạy quét 24 giờ không bị đăng xuất.
- 04 mục 7: profile chỉ người chạy dịch vụ được đọc, không đưa vào bản sao lưu công khai. ADR 0009: dời máy thì không copy profile, đăng nhập lại.

## Các phương án

### A. Profile trong named volume `mio-browser-profile`, gắn vào `/browser-profile`; ảnh và debug dump vẫn ở `MIO_DATA_DIR`
- Ưu: volume nằm trên ext4 trong máy ảo Docker, quyền `700` có hiệu lực, SQLite ổn định, nhanh; giống nhau trên Windows và Linux; tự tách profile khỏi thư mục sao lưu.
- Nhược: profile không mở trực tiếp được từ Windows Explorer (cần `docker` để xem); thêm một biến `BROWSER_PROFILE_DIR`; xóa nhầm bằng `docker compose down -v` sẽ mất phiên (đăng nhập lại qua noVNC).

### B. Giữ cả `MIO_DATA_DIR` (kể cả profile) là bind mount trên ổ Windows
- Ưu: không thêm gì; mọi dữ liệu nằm một chỗ, xem được bằng Explorer.
- Nhược: quyền `700` vô hiệu; rủi ro hỏng hoặc mất phiên do khóa file; chậm.

### C. Chạy Docker từ WSL2, `MIO_DATA_DIR` đặt trong filesystem của WSL2
- Ưu: quyền Unix và hiệu năng tốt cho mọi dữ liệu, không chỉ profile.
- Nhược: đổi cách làm việc hằng ngày (lệnh chạy từ WSL2, đường dẫn kiểu Linux); thêm bước cài đặt máy dev; không giúp gì khi đã lên máy chủ Linux.

## Quyết định

Chọn A vì giải quyết đúng phần nhạy cảm nhất (phiên đăng nhập Facebook) mà không đổi cách làm việc, và chạy giống nhau trên máy local và máy chủ.

## Hệ quả

- Được: quyền `700` thật; phiên ổn định hơn; profile không lẫn vào bản sao lưu; khi dời máy chỉ cần tạo volume mới và đăng nhập lại.
- Mất / rủi ro: `docker compose down -v` xóa profile (phải đăng nhập lại); muốn xem file trong profile phải dùng `docker`; thêm biến môi trường `BROWSER_PROFILE_DIR` cho browser-worker.
