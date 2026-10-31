> Bản đọc sinh từ docs/decisions/0014-browser-worker-playwright-image.md (phiên bản f40518e, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0014 – browser-worker dùng image Playwright chính thức kèm Node của image

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 app-skeleton (mục Tham số – phiên bản hạ tầng, [R-SKL-21](../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "image api và browser-worker build được cho linux/amd64 và l…") *(image api và browser-worker build được cho linux/amd64 và l…)*);
  - fb-account-session (Xvfb, noVNC), render (giai đoạn 4);
  - [ADR 0009](0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)*;
  - review `docs/phases/phase-0/design/reviews/app-skeleton-review.md` RV-07.

**Tóm tắt.** browser-worker dùng image Playwright chính thức và chấp nhận phiên bản Node đi kèm image đó. Đây là cách ít rủi ro nhất cho giai đoạn kiểm chứng phiên Facebook.

<a id="s-0bc81167ac"></a>

## Bối cảnh

- api chạy Node 26 trên image `node:26-bookworm-slim`.
- browser-worker cần Chromium và thư viện hệ thống để chạy Playwright. Image của worker phải build được cho `linux/amd64` và `linux/arm64`.
- Image `mcr.microsoft.com/playwright:v1.63.0-noble` có sẵn Node của Playwright. Phiên bản Node này không chắc trùng với Node 26.
- Phiên bản Chromium do phiên bản Playwright quyết định, không phụ thuộc vào việc chọn image nào.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-1cb6f3a453"></a>

### A. Dùng image Playwright chính thức, chấp nhận Node đi kèm

**Ưu**

- Microsoft đã cài và kiểm sẵn thư viện hệ thống cho Chromium trên cả hai kiến trúc.
- Ít việc phải tự bảo trì.
- Ít rủi ro nhất.

**Nhược**

- Hệ thống có hai phiên bản Node: api dùng 26, worker dùng bản theo Playwright. Muốn nâng Node của worker thì phải nâng Playwright.
- Image lớn, cỡ 2 GB, vì có cả Firefox và WebKit không dùng tới.
- Kéo image và build arm64 qua QEMU chậm hơn.

<a id="s-ee0252d264"></a>

### B. Build từ `node:26-bookworm-slim` rồi chạy `playwright install --with-deps chromium`

**Ưu**

- Cả hệ thống dùng một phiên bản Node.
- Image nhỏ hơn nhiều vì chỉ có Chromium.

**Nhược**

- Phải tự chịu phần thư viện hệ thống và font.
- Nếu thiếu thư viện trên một kiến trúc thì lỗi chỉ lộ ra lúc chạy.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án A.

**Vì sao.** Phương án A ít rủi ro nhất cho giai đoạn kiểm chứng phiên Facebook.

Nếu dung lượng image hoặc thời gian build gây phiền thì đổi sang phương án B. Việc đổi chỉ nằm trong Dockerfile của browser-worker.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Không phải tự lo thư viện hệ thống của Chromium.
- Build đa kiến trúc ổn định.

**Mất và rủi ro**

- `@mio/shared` và `apps/browser-worker` chỉ được dùng tính năng có trên Node của image Playwright. Phiên bản Node cụ thể được ghi trong `plan.md` lúc implement.
- Image lớn hơn mức cần thiết.
- Việc nâng Node của worker gắn với lịch nâng Playwright.
