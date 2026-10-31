# Tiệm Nhà Mio – Business Operations Platform

Web app nội bộ tự động hóa marketing cho Tiệm Nhà Mio. Thiết kế khái quát: `docs/project/`. Quy trình phát triển: `docs/process/2026-10-29-dev-process-skills-design.md`.

## Ưu tiên skill

- Trong repo này, skill của dự án (`.claude/skills/`) được ưu tiên hơn mọi skill khác, kể cả superpowers.
- Không dùng `brainstorming`, `writing-plans`, `executing-plans`, `test-driven-development` của superpowers cho công việc phát triển hệ thống. Dùng skill tương ứng của dự án.

## Vòng đời

Mỗi giai đoạn trong `docs/project/05-roadmap.md` đi theo thứ tự:

```text
/phase-kickoff
  → (từng tính năng) /detailed-design → /ui-design (nếu có màn hình, gọi /component-design khi cần)
     → /test-case-design → /design-review
  → /implementation-plan
  → (từng task) /implement-task → /review-code
  → (từng tính năng) /manual-test-run → [/feedback | /bug-fix → /manual-test-run --retest]
  → /acceptance-report
```

- Nhánh phụ dùng bất kỳ lúc nào: `/feedback`, `/change-request`, `/decision-log`, `/phase-status`.
- Nhóm khởi tạo chạy một lần trước giai đoạn 0: `/conventions-init` → `/ui-style-init` → `/test-viewpoints-init`. Đổi style về sau: `/ui-style-update`.
- Skill nào cũng kiểm tra điều kiện tiên quyết qua `docs/phases/phase-N/status.md` trước khi làm. Chưa thỏa thì dừng và báo, không tự nhảy bước.

## Điểm dừng

- Tại điểm dừng, dừng hẳn và chờ người dùng duyệt rõ ràng.
- Lần duyệt được ghi vào `## Nhật ký duyệt` của `status.md` kèm ngày.
- Duyệt một bước không có nghĩa là duyệt các bước sau.

## Ngôn ngữ và định dạng

- Tên file, tên skill, mã định danh: tiếng Anh. Nội dung tài liệu: tiếng Việt.
- Ưu tiên heading và gạch đầu dòng. Chỉ dùng bảng khi dữ liệu thật sự là bảng (cột DB, bảng đối chiếu).
- Trả lời người dùng ngắn gọn, tập trung vào thông tin quan trọng.

## Mã định danh

- Giai đoạn: `phase-0` … `phase-4`.
- Tính năng: kebab-case, ví dụ `group-settings`; mã 3 chữ in hoa, ví dụ `GRP`.
- Quy tắc trong thiết kế: `R-<ABC>-<nn>`, ví dụ `R-GRP-03`.
- Test case: `P<N>-<ABC>-<nnn>`, ví dụ `P0-GRP-012`.
- Task code: `T<nn>`, ví dụ `T06`.
- Quyết định: `NNNN-<slug>`, ví dụ `0003-https-via-caddy`.
- Lần chạy test: `YYYY-MM-DD-NN`, ví dụ `2026-11-10-01`.
- Vấn đề: `P<N>-ISS-<nnn>`, ví dụ `P0-ISS-007`.

## Ghi quyết định

- Ghi ADR (`/decision-log`) khi quyết định chọn giữa nhiều phương án **và** ảnh hưởng rộng hơn một tính năng: thư viện, kiến trúc, quy ước chung, style.
- Quyết định chỉ thuộc một tính năng: ghi trong file thiết kế của tính năng đó.

## Dữ liệu thật và evidence

- Evidence không che thông tin; người dùng tự xóa sau khi xác nhận.
- Không bao giờ commit: `docs/phases/*/test/runs/*/evidence/`, `docs/phases/*/acceptance/*.xlsx`, `docs/phases/*/acceptance/*.pdf`, `.local/`.

## Báo cáo kết thúc

Mỗi skill kết thúc bằng 3 phần:
- đã làm gì và ghi vào file nào;
- cần người dùng quyết gì;
- bước tiếp theo là lệnh nào.

## Cấu trúc tài liệu

```text
docs/
├── project/            # thiết kế khái quát
├── process/            # quy trình phát triển
├── decisions/          # ADR
├── testing/viewpoints.md
├── design/             # dùng chung cả app: db-schema.md, api/, ui-style.md, ui-tokens.css, components/, ui/
└── phases/phase-N/     # status.md, design/, plan.md, issues.md, test/, acceptance/
tools/                  # script dùng chung: kiểm tra skill, sinh token, chụp mockup
```

- Kiểm tra skill: `py tools/skills/validate_skills.py`.
- Test của script: `py -m pytest tools .claude/skills -q`.

## Quy ước

Chốt ngày 2026-10-29. ADR liên quan: 0001-monorepo-pnpm, 0002-drizzle-orm, 0003-naming-conventions, 0004-branching-and-commits, 0005-eslint-prettier, 0006-test-tooling, 0007-date-fns-tz, 0009-local-first-deployment.

### Cấu trúc thư mục code

- Monorepo pnpm workspace; package có scope `@mio/*`. TypeScript strict, ESM; `tsconfig.base.json` ở gốc lấy từ POC (`strict`, `noUncheckedIndexedAccess`).
- `apps/api` (`@mio/api`): NestJS – API, lịch chạy, nghiệp vụ, worker các hàng đợi `ai-text`, `ai-image`, `messenger`, `page-publish`.
- `apps/browser-worker` (`@mio/browser-worker`): NestJS standalone + Playwright – hàng đợi `fb-browser`, `fb-inbox`, `render` (render dùng Chromium riêng, không gắn profile Facebook).
- `apps/web` (`@mio/web`): React + Vite, PWA.
- `packages/shared` (`@mio/shared`): zod schema, type dùng chung, interface `Clock`, hằng số.
- Module nghiệp vụ: `apps/<app>/src/modules/<slug-tính-năng>/`, slug trùng slug tính năng trong `status.md`.
- DB (Drizzle): schema `apps/api/src/db/schema/*.ts`; migration SQL do drizzle-kit sinh trong `apps/api/migrations/`, không sửa tay migration đã merge.
- Prompt AI: `apps/api/prompts/<tác-vụ>.v<n>.md`.
- Test: `apps/<app>/test/`, cây thư mục giống `src/`; fixture `apps/<app>/test/fixtures/`; helper và bản giả `apps/<app>/test/support/`.
- Docker: `compose.yml` ở gốc, `apps/<app>/Dockerfile`; image build được cho linux/amd64 (máy local) và linux/arm64 (Oracle A1). Khác biệt giữa các máy chỉ nằm ở biến môi trường và volume (ADR 0009-local-first-deployment).

### Đặt tên

- File: kebab-case cho mọi file, kể cả component React (`slot-picker.tsx`); hậu tố NestJS `.module.ts`, `.controller.ts`, `.service.ts`, `.repository.ts`, `.processor.ts` (BullMQ).
- Class, interface, type, component React: PascalCase; lớp lỗi kết thúc bằng `Error` (`SessionExpiredError`).
- Biến, hàm: camelCase; boolean bắt đầu bằng `is`/`has`/`can`/`should`. Hằng số cấp module: UPPER_SNAKE_CASE.
- Bảng DB: snake_case số nhiều (`fb_groups`). Cột: snake_case; khóa chính `id`; khóa ngoại `<bảng số ít>_id`; thời gian `created_at`, `updated_at` kiểu `timestamptz`. Index `<bảng>_<cột>_idx`, unique `<bảng>_<cột>_key`.
- Endpoint API: `/api/v1/<danh-từ-số-nhiều>` kebab-case (`/api/v1/fb-groups/:id`); hành động là sub-resource POST (`/api/v1/appointments/:id/confirm`). Field JSON và query param: camelCase.
- Hàng đợi và tên job BullMQ: kebab-case (`fb-browser`, `classify-post`).
- Biến môi trường: UPPER_SNAKE_CASE; chỉ chứa khóa bí mật và đường dẫn, cấu hình nghiệp vụ nằm trong DB.

### Nhánh và commit

- Tên nhánh (tạo từ `main` mới nhất):
  - task (`/implement-task`): `phase-<N>/t<nn>-<slug>`, ví dụ `phase-0/t06-groups-api`;
  - sửa lỗi (`/bug-fix`): `phase-<N>/fix-p<N>-iss-<nnn>`, ví dụ `phase-0/fix-p0-iss-007`;
  - thay đổi yêu cầu (`/change-request`): `phase-<N>/cr-<slug>`, ví dụ `phase-0/cr-comment-limit`.
- Commit message: Conventional Commits `<type>(<scope>): <mô tả tiếng Anh, thể mệnh lệnh, chữ thường>`. Type: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`, `ci`. Scope: `api`, `browser-worker`, `web`, `shared`, `db`, hoặc khu vực docs/tools (`process`, `skills`, `phase-0`…).
- Không có dòng `Co-Authored-By`, "Generated with Claude Code" hay bất kỳ dấu vết Claude nào trong commit và PR.
- Merge: squash merge vào `main` sau khi `/review-code` được duyệt; tiêu đề commit squash kèm mã: `feat(api): add fb-groups endpoint (phase-0 T06)`, `fix(api): … (P0-ISS-007)`. Xóa nhánh sau khi merge.

### Lint, format, typecheck

- Công cụ: ESLint (flat config `eslint.config.js`, typescript-eslint `recommendedTypeChecked`), Prettier (`singleQuote`, `trailingComma: all`, `printWidth: 120`), `tsc --noEmit` từng package. Không dùng git hook; `implement-task`, `bug-fix`, `review-code` bắt buộc chạy đủ lint, format check, typecheck trước khi commit/merge.
- Rule ESLint bắt buộc:
  - `@typescript-eslint/no-floating-promises`: error;
  - `unicorn/filename-case`: kebab-case;
  - `no-restricted-syntax`: cấm `Date.now()` và `new Date()` không tham số trong `src/`, trừ `system-clock.ts`;
  - `@vitest/eslint-plugin`: cấm `.only`, `.skip`, `.todo`, `skipIf`;
  - `eslint-config-prettier`.
- Xong task khi không có lỗi và không có warning (`--max-warnings 0`).
- Lệnh: `pnpm lint`, `pnpm format` (ghi), `pnpm format:check`, `pnpm typecheck`.

### Test tự động

- Công cụ: vitest (+ `unplugin-swc` cho decorator NestJS), fast-check, Testcontainers (PostgreSQL, Redis cùng phiên bản với `compose.yml`), Ajv đối chiếu `openapi.yaml`.
- Vị trí và đặt tên file test: trong `apps/<app>/test/`, cây giống `src/`. Unit `*.test.ts`, contract `*.contract.test.ts`, integration `*.int.test.ts`, kịch bản đầu-cuối `*.e2e.test.ts`.
- Đồng hồ: interface `Clock` (`now(): Date`) trong `@mio/shared`, inject qua token `CLOCK`; test dùng `FakeClock`. Cấm `Date.now()` / `new Date()` không tham số trong logic nghiệp vụ (lint chặn).
- Ngày giờ: date-fns + `@date-fns/tz`; múi giờ lấy từ hằng `APP_TIME_ZONE = 'Asia/Ho_Chi_Minh'`; DB lưu `timestamptz`.
- Property-based: bắt buộc cho bất biến quan trọng (lịch không trùng, khung đề xuất luôn trống, phanh an toàn không vượt giới hạn); dùng `fc.assert`, khi fail in seed.
- Integration: chạy migration thật lên container; mỗi file test dùng database riêng tạo từ template đã migrate. Thiếu Docker thì `pnpm test:int` fail với thông báo rõ, không skip.
- Contract:
  - response API đối chiếu `docs/design/api/openapi.yaml` qua helper `expectMatchesOpenApi(res, operationId)`;
  - adapter Facebook chạy trên fixture payload/HTML đã lưu; webhook Messenger trên fixture JSON;
  - nhà cung cấp AI có bản giả cùng interface.
- Kịch bản đầu-cuối: luồng nghiệp vụ chạy với DB thật + bản giả Facebook, AI, Messenger.
- Fixture: `apps/<app>/test/fixtures/`; dữ liệu thô để trong `.local/`, ẩn thông tin cá nhân bằng `pnpm anonymize <file>` trước khi đưa vào fixture.
- Skip: không commit test bị skip. Test cần fixture thật gọi `requireFixture(path)`; thiếu fixture thì fail và in đường dẫn thiếu; không được báo pass khi thiếu dữ liệu.
- Lệnh: `pnpm test` (unit + contract, không cần Docker), `pnpm test:int` (integration + đầu-cuối, cần Docker), chạy riêng: `pnpm --filter @mio/api test -- <mẫu>`.
