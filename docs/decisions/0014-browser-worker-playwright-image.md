# 0014 – browser-worker dùng image Playwright chính thức kèm Node của image

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan: phase-0 app-skeleton (mục Tham số – phiên bản hạ tầng, R-SKL-21); fb-account-session (Xvfb, noVNC), render (giai đoạn 4); ADR 0009; review `docs/phases/phase-0/design/reviews/app-skeleton-review.md` RV-07

## Bối cảnh

- api chạy Node 26 (`node:26-bookworm-slim`). browser-worker cần Chromium và thư viện hệ thống để chạy Playwright, build được cho `linux/amd64` và `linux/arm64`.
- Image `mcr.microsoft.com/playwright:v1.63.0-noble` mang sẵn Node của Playwright, không chắc trùng Node 26. Phiên bản Chromium do phiên bản Playwright quyết định, không phụ thuộc lựa chọn image.

## Các phương án

### A. Dùng image Playwright chính thức, chấp nhận Node đi kèm
- Ưu: Microsoft đã cài và kiểm sẵn thư viện hệ thống cho Chromium trên cả hai kiến trúc; ít việc tự bảo trì; ít rủi ro nhất.
- Nhược: hai phiên bản Node trong hệ thống (api 26, worker theo Playwright), nâng Node của worker phải nâng Playwright; image lớn (cỡ 2 GB, có cả Firefox, WebKit không dùng), kéo và build arm64 qua QEMU chậm hơn.

### B. Build từ `node:26-bookworm-slim` + `playwright install --with-deps chromium`
- Ưu: một phiên bản Node cho cả hệ thống; image nhỏ hơn nhiều (chỉ Chromium).
- Nhược: tự chịu phần thư viện hệ thống, font; rủi ro thiếu thư viện trên một kiến trúc chỉ lộ ra lúc chạy.

## Quyết định

Chọn A vì ít rủi ro nhất cho giai đoạn kiểm chứng phiên Facebook. Nếu dung lượng image hoặc thời gian build gây phiền thì đổi sang B; việc đổi chỉ nằm trong Dockerfile của browser-worker.

## Hệ quả

- Được: không phải tự lo thư viện hệ thống của Chromium; build đa kiến trúc ổn định.
- Mất / rủi ro: `@mio/shared` và `apps/browser-worker` chỉ được dùng tính năng có trên Node của image Playwright (ghi phiên bản cụ thể trong `plan.md` lúc implement); image lớn hơn cần thiết; nâng Node của worker gắn với lịch nâng Playwright.
