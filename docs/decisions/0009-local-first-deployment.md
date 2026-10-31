# 0009 – Chạy trên máy local trước, giữ khả năng dời lên Oracle

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: docs/project/04-technical.md mục 1, 3, 7; docs/project/05-roadmap.md giai đoạn 0 và mục "Triển khai lên máy chủ"; CLAUDE.md mục Quy ước – Docker; phase-0: app-skeleton, fb-account-session, backup

## Bối cảnh

- Thiết kế khái quát chọn Oracle Cloud Free (Ampere A1, linux/arm64) làm nơi chạy 24/7, và đặt việc dựng VM, HTTPS, tên miền vào giai đoạn 0.
- Hiện chưa đăng ký được Oracle Free. Người dùng muốn chạy giai đoạn 0 bằng Docker trên máy của mình trước, và sau này dời lên Oracle mà không phải sửa code.
- Máy dev là Windows x64 (linux/amd64 trong Docker). Oracle A1 là linux/arm64.
- Giai đoạn 0 không cần HTTPS: web app chỉ truy cập qua `localhost`. Giai đoạn 1 (web push trên iPhone) và giai đoạn 2 (webhook Messenger) bắt buộc HTTPS và tên miền cố định.

## Các phương án

### A. Local trước, image đa kiến trúc, cấu hình theo môi trường
- Ưu: bắt đầu ngay, không tốn tiền; IP nhà mạng ít bị Facebook nghi ngờ hơn IP datacenter; dời lên Oracle chỉ cần build image arm64, đổi biến môi trường và đăng nhập lại.
- Nhược: máy dev không chạy 24/7, nên tiêu chí "chạy liên tục 3 ngày" phải nới; chưa kiểm chứng được rủi ro IP datacenter và tài nguyên của Oracle A1; phải giữ image chạy được trên cả amd64 và arm64.

### B. Chờ có Oracle rồi mới làm giai đoạn 0
- Ưu: giữ nguyên roadmap; kiểm chứng đúng môi trường thật ngay từ đầu.
- Nhược: bị chặn vô thời hạn, không làm được gì.

### C. Thuê VPS trả phí (x64) ngay
- Ưu: chạy 24/7, có IP cố định cho HTTPS sớm.
- Nhược: tốn tiền hằng tháng, trái ưu tiên "không tốn tiền máy chủ"; IP datacenter vẫn có rủi ro như Oracle.

## Quyết định

Chọn A vì không bị chặn, không tốn tiền, và nếu ràng buộc tính khả chuyển ngay từ `app-skeleton` thì việc dời lên Oracle chỉ còn là việc triển khai.

Ràng buộc kèm theo:
- Image Docker build được cho `linux/amd64` và `linux/arm64` (dùng base image đa kiến trúc, kể cả image Playwright). Không dùng gì chỉ có trên một kiến trúc.
- Mọi khác biệt giữa các máy nằm ở biến môi trường và volume: đường dẫn dữ liệu (ảnh, debug dump, profile trình duyệt), đích sao lưu, URL công khai. Không có giá trị phụ thuộc máy trong code hoặc trong `compose.yml`.
- Sao lưu ghi ra thư mục cấu hình được. Đẩy lên Object Storage (giao thức tương thích S3) là bước tùy chọn, bật bằng biến môi trường.
- HTTPS và reverse proxy (Caddy) là lớp tách riêng, thêm vào khi triển khai lên máy chủ, không làm thay đổi app.
- Khi dời máy: khôi phục DB từ bản sao lưu; **không copy profile trình duyệt**, đăng nhập lại trên máy mới qua noVNC (04-technical.md mục 4.2).

## Hệ quả

- Được: giai đoạn 0 làm được ngay; tách rõ app và hạ tầng; có sẵn quy trình dời máy (sao lưu → khôi phục → đăng nhập lại).
- Mất / rủi ro:
  - Rủi ro IP datacenter và mức tài nguyên trên Oracle A1 chưa được kiểm chứng. Phải kiểm chứng lại khi dời lên Oracle.
  - Phải có HTTPS và tên miền cố định trước khi bật web push ở giai đoạn 1. Nếu lúc đó vẫn chưa có Oracle thì cần phương án tạm (ví dụ Cloudflare Tunnel có tên miền) và sẽ ghi ADR riêng.
  - Build arm64 trên máy amd64 cần buildx/QEMU, chậm hơn build thường.
