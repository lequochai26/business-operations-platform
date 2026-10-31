<!-- src-section: 0b0fa0b228 7a1ece9dad25 -->
# 0001 – Monorepo pnpm, test đặt trong thư mục test/ riêng

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - CLAUDE.md mục Quy ước › Cấu trúc thư mục code;
  - docs/project/04-technical.md mục 2, 3.

**Tóm tắt.** Mã nguồn được tổ chức thành một monorepo dùng pnpm workspace, mỗi app là một package riêng và có một package dùng chung. Test của mỗi app nằm trong thư mục `test/` riêng có cây thư mục giống `src/`, theo thói quen của POC và để `src/` gọn.

<!-- src-section: 0bc81167ac 6891b8c6c21b -->
## Bối cảnh

Hệ thống gồm các phần sau:
- NestJS lo API, lịch và nghiệp vụ;
- worker trình duyệt chạy Playwright;
- web app dạng PWA;
- phần dùng chung như type và zod schema.

Worker trình duyệt cần image Playwright linux/arm64 rất nặng. Các phần khác thì không cần image này. POC dùng npm và đặt test trong thư mục `tests/` riêng.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 2a849f9102 06801b0b24ac -->
### A. Monorepo pnpm workspace

Bố cục gồm `apps/api`, `apps/browser-worker`, `apps/web` và `packages/shared`.

**Ưu**

- Mỗi app có image Docker riêng.
- Các app dùng chung type.
- pnpm giữ dependency chặt và cài nhanh.

**Nhược**

- Cấu hình workspace nhiều hơn.
- Phải thêm công cụ so với POC.

<!-- src-section: 0b65988536 b852e3be3256 -->
### B. Monorepo npm workspaces, bố cục như A

**Ưu**

- Giống POC, không phải cài thêm công cụ.

**Nhược**

- Chậm hơn pnpm.
- Dependency ngầm (do hoisting) dễ lọt vào code.

<!-- src-section: fe47dc3ef7 7c3ff9760272 -->
### C. Một project NestJS, web nằm trong thư mục con

**Ưu**

- Đơn giản nhất.

**Nhược**

- Image phình to vì kéo theo cả Chromium.
- Khó tách worker trình duyệt ra riêng.

**Vị trí test.** Có hai cách đặt test. Cách thứ nhất là đặt test cạnh code, ví dụ `foo.service.test.ts` nằm cùng thư mục với file được test. Cách thứ hai là mỗi app có thư mục `test/` riêng, giống POC.

<!-- src-section: 254160d409 9094ac034e84 -->
## Quyết định

Chọn phương án A. Test đặt trong `apps/<app>/test/`, có cây thư mục giống `src/`.

**Vì sao.** Cách đặt test này theo thói quen của POC. Nó cũng giữ cho `src/` gọn.

<!-- src-section: 58c5fdb1ed b11190be96bd -->
## Hệ quả

**Được**

- Worker trình duyệt tách riêng, dễ thay hoặc chuyển sang máy khác.
- Các app dùng chung type qua package `@mio/shared`.

**Mất và rủi ro**

- Phải giữ cây `test/` song song với `src/`.
- Khó thấy ngay file nào thiếu test. Bước `review-code` phải kiểm tra việc này.
