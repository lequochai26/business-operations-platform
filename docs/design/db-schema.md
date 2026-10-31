# Schema cơ sở dữ liệu

Nguồn chính về schema của toàn app. Migration trong code phải khớp file này (`/review-code` kiểm tra).

## Quy ước chung

- PostgreSQL. Tên bảng, cột theo `CLAUDE.md` mục `## Quy ước`.
- Mọi thời điểm lưu UTC (`timestamptz`); hiển thị theo `Asia/Ho_Chi_Minh`. Phiên DB dùng múi giờ `UTC`.
- Mọi bảng có `id`, `created_at`, `updated_at`. App đặt `created_at`, `updated_at` bằng `CLOCK.now()` khi ghi (cả nhánh INSERT của upsert); mặc định `now()` của DB chỉ là dự phòng cho SQL viết tay.
- Không xóa cứng bản ghi đã được tham chiếu bởi lịch sử; dùng cờ lưu trữ.
- Schema Drizzle ở `apps/api/src/db/schema/*.ts`, migration do drizzle-kit sinh ở `apps/api/migrations/`. Chỉ api truy cập DB (ADR 0011).

## app_settings

Cài đặt nghiệp vụ chỉnh được trên web, mỗi dòng là một mục cài đặt (ADR 0010). Tính năng sở hữu: `app-skeleton` (bảng); nội dung từng khóa do tính năng khai báo khóa đó sở hữu.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| key | text | không | | unique; check `key ~ '^[a-z0-9]+(-[a-z0-9]+)*$'` | khóa trong `SETTINGS` của `@mio/shared`, kebab-case, ví dụ `crawl-schedule` |
| value | jsonb | không | | | cả mục cài đặt; kiểm tra bằng zod schema của khóa ở tầng ứng dụng |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` khi tạo |
| updated_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` khi ghi |

### Index
- `app_settings_key_key`: `key`, unique

### Quan hệ
- Không có.

## users

Tài khoản đăng nhập web app. Tính năng sở hữu: `auth`. Giai đoạn 0 tạo bằng CLI; cột Messenger, web push, khóa tài khoản do tính năng của giai đoạn sau thêm.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| username | text | không | | unique; check `username ~ '^[a-z0-9._-]{3,32}$'` | đã chuẩn hóa chữ thường (R-AUT-07) |
| password_hash | text | không | | | chuỗi PHC argon2id (R-AUT-08) |
| role | text | không | | check `role in ('manager', 'technician')` | `manager` = Quản lý, `technician` = Thợ |
| display_name | text | không | | check `char_length(display_name) between 1 and 50` | đã bỏ khoảng trắng hai đầu |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |
| updated_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |

### Index
- `users_username_key`: `username`, unique

### Quan hệ
- Không có khóa ngoại đi ra. `user_sessions.user_id` trỏ tới bảng này.

## user_sessions

Phiên đăng nhập web (ADR 0015). Tính năng sở hữu: `auth`. Xóa cứng khi đăng xuất, đổi/đặt lại mật khẩu hoặc hết hạn (không bảng nào tham chiếu).

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| user_id | uuid | không | | FK → `users.id` | |
| token_hash | text | không | | unique | SHA-256 hex của token trong cookie `mio_session`; không lưu token gốc (R-AUT-09) |
| expires_at | timestamptz | không | | | lần gia hạn gần nhất + 90 ngày (R-AUT-10) |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |
| updated_at | timestamptz | không | now() | | thời điểm gia hạn gần nhất; app đặt bằng `CLOCK.now()` |

### Index
- `user_sessions_token_hash_key`: `token_hash`, unique
- `user_sessions_user_id_idx`: `user_id`
- `user_sessions_expires_at_idx`: `expires_at` (dọn phiên hết hạn, R-AUT-13)

### Quan hệ
- `user_id` → `users.id`, on delete cascade

## login_throttles

Bộ đếm đăng nhập sai theo tên đăng nhập, kể cả tên không tồn tại (R-AUT-06). Tính năng sở hữu: `auth`. Không có khóa ngoại tới `users` vì phải đếm cả tên không có thật.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| username | text | không | | unique; check `char_length(username) between 1 and 32` | tên đã chuẩn hóa như người dùng nhập |
| failed_count | integer | không | 0 | check `failed_count between 0 and 4` | số lần sai trong cửa sổ hiện tại; về 0 khi bắt đầu khóa |
| window_started_at | timestamptz | không | | | lần sai đầu của cửa sổ 15 phút |
| locked_until | timestamptz | có | | | khác null và > bây giờ: đang khóa |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |
| updated_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()`; dùng để dọn dòng cũ hơn 24 giờ (R-AUT-13) |

### Index
- `login_throttles_username_key`: `username`, unique

### Quan hệ
- Không có.

## Lịch sử thay đổi

- 2026-10-29 | app-skeleton | tạo file; thêm bảng `app_settings`
- 2026-10-31 | app-skeleton | Quy ước chung: `created_at`, `updated_at` lấy từ `CLOCK` (review RV-11)
- 2026-10-31 | auth | thêm bảng `users`, `user_sessions`, `login_throttles`
