## Quy ước

Chốt ngày 2026-11-01. ADR liên quan: 0001-monorepo-pnpm, 0002-vitest-testcontainers.

### Cấu trúc thư mục code

- Monorepo pnpm workspace.
- `apps/api` (NestJS), `apps/browser-worker` (Playwright), `apps/web` (React + Vite), `packages/shared` (type, schema zod).
- Test cạnh code: `*.test.ts`; integration test: `*.int.test.ts`; fixture: `test/fixtures/`; migration: `apps/api/migrations/`.

### Đặt tên

- File: kebab-case (`group-settings.service.ts`).
- Class, interface, type: PascalCase.
- Biến, hàm: camelCase.
- Bảng, cột DB: snake_case, tên bảng số ít (`fb_group`).
- Endpoint API: `/api/<danh-từ-số-nhiều>`, kebab-case.
- Biến môi trường: UPPER_SNAKE_CASE.

### Nhánh và commit

- Tên nhánh: `phase-<N>/t<nn>-<slug>`, ví dụ `phase-0/t06-groups-api`.
- Commit message: Conventional Commits, phần mô tả tiếng Anh.
- Merge: squash merge vào `main` sau khi `/review-code` xong.

### Lint, format, typecheck

- Công cụ: ESLint, Prettier, `tsc --noEmit`.
- Lệnh: `pnpm lint`, `pnpm format`, `pnpm typecheck`.

### Test tự động

- Công cụ: vitest, fast-check, Testcontainers (PostgreSQL, Redis).
- Vị trí và đặt tên file test: như mục Cấu trúc thư mục code.
- Đồng hồ: interface `Clock` inject qua constructor; cấm `Date.now()` / `new Date()` không tham số trong logic nghiệp vụ.
- Fixture: `test/fixtures/`, ẩn thông tin cá nhân bằng `pnpm anonymize` trước khi commit.
- Skip: dùng `describe.skipIf(...)` phải kèm `console.warn` lý do.
- Lệnh: `pnpm test`, `pnpm test:int`.
