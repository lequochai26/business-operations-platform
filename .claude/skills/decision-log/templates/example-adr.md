# 0003 – HTTPS bằng Caddy + DuckDNS

- Ngày: 2026-11-02
- Trạng thái: chấp nhận
- Liên quan: docs/project/04-technical.md mục 3; tính năng group-settings, auth

## Bối cảnh

Webhook Meta và web push bắt buộc HTTPS với tên miền cố định. Máy chủ là Oracle Free, ưu tiên không tốn tiền.

## Các phương án

### A. Caddy + tên miền phụ DuckDNS
- Ưu: miễn phí, Caddy tự lấy chứng chỉ Let's Encrypt, tên miền cố định.
- Nhược: phụ thuộc dịch vụ DuckDNS; phải mở cổng 80/443 trên Oracle.

### B. Cloudflare Tunnel
- Ưu: không mở cổng, có bảo vệ của Cloudflare.
- Nhược: cần tên miền riêng trên Cloudflare (tốn phí), quick tunnel đổi URL mỗi lần chạy nên không dùng được cho webhook.

## Quyết định

Chọn A vì miễn phí và có tên miền cố định ngay.

## Hệ quả

- Được: có HTTPS cho webhook và web app mà không tốn tiền.
- Mất / rủi ro: nếu DuckDNS ngừng hoạt động phải chuyển tên miền và cập nhật webhook trong Meta app.
