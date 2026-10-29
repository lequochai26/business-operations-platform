# 0001 – Monorepo pnpm, test đặt trong thư mục test/ riêng

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Cấu trúc thư mục code; docs/project/04-technical.md mục 2, 3

## Bối cảnh

Hệ thống gồm NestJS (API, lịch, nghiệp vụ), worker trình duyệt Playwright, web app PWA và phần dùng chung (type, zod schema). Worker trình duyệt cần image Playwright linux/arm64 nặng, các phần khác thì không. POC dùng npm, test đặt trong `tests/` riêng.

## Các phương án

### A. Monorepo pnpm workspace (`apps/api`, `apps/browser-worker`, `apps/web`, `packages/shared`)
- Ưu: tách image Docker theo app; dùng chung type; pnpm giữ dependency chặt, cài nhanh.
- Nhược: cấu hình workspace nhiều hơn; thêm công cụ so với POC.

### B. Monorepo npm workspaces, bố cục như A
- Ưu: giống POC, không cài thêm công cụ.
- Nhược: chậm hơn, dependency ngầm (hoisting) dễ lọt.

### C. Một project NestJS, web nằm trong thư mục con
- Ưu: đơn giản nhất.
- Nhược: image phình vì kéo cả Chromium; khó tách worker trình duyệt.

Vị trí test: cạnh code (`foo.service.test.ts` cùng thư mục) hoặc thư mục `test/` riêng mỗi app (giống POC).

## Quyết định

Chọn A. Test đặt trong `apps/<app>/test/` với cây thư mục giống `src/`, theo thói quen của POC và để `src/` gọn.

## Hệ quả

- Được: worker trình duyệt tách riêng, dễ thay hoặc chuyển sang máy khác; type dùng chung qua `@mio/shared`.
- Mất / rủi ro: phải giữ cây `test/` song song với `src/`; khó thấy ngay file nào thiếu test (`review-code` phải kiểm tra).
