> Bản đọc sinh từ docs/decisions/0002-drizzle-orm.md (phiên bản f3fb979, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0002 – Drizzle cho truy cập DB và migration

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước; docs/design/db-schema.md; skill detailed-design, review-code

**Tóm tắt.** Dự án dùng Drizzle để truy cập PostgreSQL và sinh migration. Lý do chính là migration ở dạng SQL đọc được, type an toàn và không tốn tài nguyên.

<a id="s-0bc81167ac"></a>

## Bối cảnh

Dự án dùng PostgreSQL. Công cụ truy cập DB cần đáp ứng các yêu cầu sau:
- có type;
- sinh được migration để bước `review-code` đối chiếu với `db-schema.md`;
- chạy tốt trên máy ARM của Oracle Free.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-59e6983cf3"></a>

### A. Drizzle

**Ưu**

- Schema viết bằng TS.
- drizzle-kit sinh migration SQL dễ đọc và dễ đối chiếu.
- Có drizzle-zod.
- Nhẹ, không cần engine riêng.

**Nhược**

- Ít tài liệu hơn Prisma.
- Một số API còn thay đổi theo phiên bản.

<a id="s-1113c30854"></a>

### B. Prisma

**Ưu**

- Phổ biến, nhiều tài liệu.

**Nhược**

- Có engine riêng, nặng hơn khi chạy trên ARM.
- Viết SQL thô kém linh hoạt.

<a id="s-8021410443"></a>

### C. Kysely kèm migration SQL viết tay

**Ưu**

- Kiểm soát SQL hoàn toàn mà vẫn có type.

**Nhược**

- Phải tự giữ type đồng bộ với schema.

<a id="s-e778faa610"></a>

### D. TypeORM

**Ưu**

- Là lựa chọn mặc định của NestJS.

**Nhược**

- Type lỏng.
- Dùng nhiều decorator.
- Migration hay bị lệch.

<a id="s-254160d409"></a>

## Quyết định

Chọn phương án A (Drizzle).

**Vì sao.** Migration là SQL đọc được. Type an toàn mà không tốn tài nguyên.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Schema nằm ở `apps/api/src/db/schema/`.
- Migration nằm ở `apps/api/migrations/`.
- Zod schema được sinh từ định nghĩa bảng.

**Mất và rủi ro**

- Phải theo dõi thay đổi API của Drizzle mỗi lần nâng cấp.
- Không được sửa tay migration đã merge.
