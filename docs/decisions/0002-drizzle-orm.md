# 0002 – Drizzle cho truy cập DB và migration

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước; docs/design/db-schema.md; skill detailed-design, review-code

## Bối cảnh

Dùng PostgreSQL. Cần công cụ truy cập DB có type, sinh migration để `review-code` đối chiếu với `db-schema.md`, chạy tốt trên máy ARM của Oracle Free.

## Các phương án

### A. Drizzle
- Ưu: schema viết bằng TS; drizzle-kit sinh migration SQL dễ đọc và đối chiếu; có drizzle-zod; nhẹ, không cần engine riêng.
- Nhược: ít tài liệu hơn Prisma; một số API còn đổi theo phiên bản.

### B. Prisma
- Ưu: phổ biến, tài liệu nhiều.
- Nhược: có engine riêng (nặng hơn trên ARM); viết SQL thô kém linh hoạt.

### C. Kysely + migration SQL viết tay
- Ưu: kiểm soát SQL hoàn toàn, có type.
- Nhược: phải tự giữ type đồng bộ với schema.

### D. TypeORM
- Ưu: mặc định của NestJS.
- Nhược: type lỏng, decorator nhiều, migration hay lệch.

## Quyết định

Chọn A vì migration là SQL đọc được và type an toàn mà không tốn tài nguyên.

## Hệ quả

- Được: schema ở `apps/api/src/db/schema/`, migration ở `apps/api/migrations/`; zod schema sinh từ bảng.
- Mất / rủi ro: phải theo dõi thay đổi API của Drizzle khi nâng cấp; không sửa tay migration đã merge.
