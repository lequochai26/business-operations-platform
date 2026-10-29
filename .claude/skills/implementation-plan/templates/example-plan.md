# Kế hoạch code – Giai đoạn 0

- Duyệt: 2026-11-06
- Thiết kế: `docs/phases/phase-0/design/`

### T05 Bảng fb_group và repository
- Tính năng: group-settings
- Thiết kế: group-settings.md mục "Thay đổi DB"; db-schema.md mục `fb_group`; R-GRP-03
- Phụ thuộc: T01
- File: tạo `apps/api/migrations/0003_fb_group.sql`, `apps/api/src/groups/groups.repository.ts`, `groups.repository.int.test.ts`
- Test tự động: `rejects duplicate group ref` – unique index chặn group trùng; `stores comment_limit null by default`
- Test case manual: không
- Tiêu chí xong: `pnpm test:int -- groups.repository` pass
- Trạng thái: xong

### T06 API groups
- Tính năng: group-settings
- Thiết kế: group-settings.md mục "API", "Quy tắc"; api/groups.md; R-GRP-01..05
- Phụ thuộc: T05, T03
- File: tạo `apps/api/src/groups/groups.controller.ts`, `groups.service.ts`, `packages/shared/src/group-ref.ts`, các file `*.test.ts` tương ứng
- Test tự động: `parseGroupRef accepts link with ?ref=share`; `PATCH rejects comment_limit 51 with GROUP_LIMIT_RANGE`; `technician gets 403`
- Test case manual: P0-GRP-001..015, P0-GRP-020, P0-GRP-021
- Tiêu chí xong: `pnpm test` và `pnpm typecheck` pass; endpoint khớp `docs/design/api/openapi.yaml`
- Trạng thái: chưa làm
