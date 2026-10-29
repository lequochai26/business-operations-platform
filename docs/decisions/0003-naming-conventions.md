# 0003 – Quy ước đặt tên bảng DB và endpoint API

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Đặt tên; docs/design/db-schema.md, docs/design/api/

## Bối cảnh

Mọi tính năng đều thêm bảng và endpoint. Cần một quy tắc duy nhất để thiết kế, code và review đối chiếu được.

## Các phương án

### Tên bảng

#### A. snake_case số nhiều (`fb_groups`)
- Ưu: phổ biến với Postgres/Drizzle, đọc tự nhiên khi query.
- Nhược: phải nhớ số nhiều bất quy tắc.

#### B. snake_case số ít (`fb_group`)
- Ưu: khớp tên entity.
- Nhược: dễ đụng từ khóa (`user`).

### Endpoint

#### A. `/api/<danh-từ-số-nhiều>`
- Ưu: ngắn; app nội bộ, server và client deploy cùng lúc.
- Nhược: không có sẵn chỗ cho phiên bản API sau này.

#### B. `/api/v1/<danh-từ-số-nhiều>`
- Ưu: có version sẵn nếu sau này có app native cũ còn chạy.
- Nhược: dài hơn, hiện chưa cần.

## Quyết định

Tên bảng chọn A (số nhiều). Endpoint chọn B (`/api/v1/...`), kebab-case; field JSON và query param camelCase.

## Hệ quả

- Được: quy tắc kiểm tra được trong `review-code`; sẵn đường nâng version API.
- Mất / rủi ro: mọi đường dẫn dài thêm `/v1`; khóa ngoại dùng dạng số ít (`fb_group_id`) nên phải chuyển số nhiều ↔ số ít.
