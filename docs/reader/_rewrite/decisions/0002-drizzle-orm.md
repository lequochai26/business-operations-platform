<!-- src-section: 0b0fa0b228 2eb080e0fbb6 -->
# 0002 – Drizzle cho truy cập DB và migration

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước; docs/design/db-schema.md; skill detailed-design, review-code

**Tóm tắt.** Dự án dùng Drizzle để truy cập PostgreSQL và sinh migration. Lý do chính là migration ở dạng SQL đọc được, type an toàn và không tốn tài nguyên.

<!-- src-section: 0bc81167ac 9ea9bb44df41 -->
## Bối cảnh

Dự án dùng PostgreSQL. Công cụ truy cập DB cần đáp ứng các yêu cầu sau:
- có type;
- sinh được migration để bước `review-code` đối chiếu với `db-schema.md`;
- chạy tốt trên máy ARM của Oracle Free.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 59e6983cf3 128d47dfa54f -->
### A. Drizzle

**Ưu**

- Schema viết bằng TS.
- drizzle-kit sinh migration SQL dễ đọc và dễ đối chiếu.
- Có drizzle-zod.
- Nhẹ, không cần engine riêng.

**Nhược**

- Ít tài liệu hơn Prisma.
- Một số API còn thay đổi theo phiên bản.

<!-- src-section: 1113c30854 a0f5a2821956 -->
### B. Prisma

**Ưu**

- Phổ biến, nhiều tài liệu.

**Nhược**

- Có engine riêng, nặng hơn khi chạy trên ARM.
- Viết SQL thô kém linh hoạt.

<!-- src-section: 8021410443 51ee2e1e2a97 -->
### C. Kysely kèm migration SQL viết tay

**Ưu**

- Kiểm soát SQL hoàn toàn mà vẫn có type.

**Nhược**

- Phải tự giữ type đồng bộ với schema.

<!-- src-section: e778faa610 6e8346806841 -->
### D. TypeORM

**Ưu**

- Là lựa chọn mặc định của NestJS.

**Nhược**

- Type lỏng.
- Dùng nhiều decorator.
- Migration hay bị lệch.

<!-- src-section: 254160d409 43667909666b -->
## Quyết định

Chọn phương án A (Drizzle).

**Vì sao.** Migration là SQL đọc được. Type an toàn mà không tốn tài nguyên.

<!-- src-section: 58c5fdb1ed a659a9939e81 -->
## Hệ quả

**Được**

- Schema nằm ở `apps/api/src/db/schema/`.
- Migration nằm ở `apps/api/migrations/`.
- Zod schema được sinh từ định nghĩa bảng.

**Mất và rủi ro**

- Phải theo dõi thay đổi API của Drizzle mỗi lần nâng cấp.
- Không được sửa tay migration đã merge.
