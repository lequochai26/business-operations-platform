<!-- src-section: 0b0fa0b228 45b77c3bb6a4 -->
# Schema cơ sở dữ liệu

**Tóm tắt.** Đây là nguồn chính về schema của toàn app. Migration trong code phải khớp với file này, và bước `/review-code` kiểm tra điều đó.

<!-- src-section: 6ef5855010 fae819a716a3 -->
## Quy ước chung

**Tóm tắt.** Cơ sở dữ liệu là PostgreSQL. Mọi bảng lưu thời điểm theo UTC và có đủ ba cột `id`, `created_at`, `updated_at`.

**Cách hoạt động**
- Tên bảng và tên cột theo mục `## Quy ước` trong `CLAUDE.md`.
- Mọi thời điểm được lưu theo UTC. Khi hiển thị, thời điểm được đổi sang giờ Việt Nam. Phiên kết nối DB cũng dùng múi giờ UTC.
- App tự đặt hai cột thời gian theo đồng hồ của app mỗi khi ghi, kể cả ở nhánh INSERT của upsert. Giá trị mặc định của DB chỉ là dự phòng cho SQL viết tay.
- Bản ghi đã được lịch sử tham chiếu thì không bị xoá cứng. Thay vào đó, bản ghi được đánh dấu bằng cờ lưu trữ.
- Chỉ api được truy cập DB (ADR 0011).

**Chi tiết kỹ thuật**
- Kiểu cột thời gian: `timestamptz`. Múi giờ hiển thị: `Asia/Ho_Chi_Minh`. Múi giờ của phiên DB: `UTC`.
- App đặt `created_at`, `updated_at` bằng `CLOCK.now()`. Mặc định của DB là `now()`.
- Schema Drizzle nằm ở `apps/api/src/db/schema/*.ts`.
- Migration do drizzle-kit sinh, nằm ở `apps/api/migrations/`.

<!-- src-section: 8637443dd5 07246a1d5115 -->
## app_settings

**Tóm tắt.** Bảng lưu các cài đặt nghiệp vụ chỉnh được trên web. Mỗi dòng là một mục cài đặt (ADR 0010).

**Cách hoạt động**
- Tính năng `app-skeleton` sở hữu bảng này.
- Nội dung của từng khoá do tính năng khai báo khoá đó sở hữu.

Bảng dưới liệt kê các cột. Mỗi mục cài đặt có một khoá dạng kebab-case và một giá trị JSON được kiểm tra ở tầng ứng dụng.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| key | text | không | | unique; check `key ~ '^[a-z0-9]+(-[a-z0-9]+)*$'` | khoá trong `SETTINGS` của `@mio/shared`, kebab-case, ví dụ `crawl-schedule` |
| value | jsonb | không | | | cả mục cài đặt; kiểm tra bằng zod schema của khoá ở tầng ứng dụng |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` khi tạo |
| updated_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` khi ghi |

<!-- src-section: c5987787a9 ef0e746e5c76 -->
### Index

**Tóm tắt.** Bảng có một index unique trên cột khoá, nên mỗi khoá chỉ có một dòng.

**Chi tiết kỹ thuật**
- `app_settings_key_key`: cột `key`, unique.

<!-- src-section: 86797db1d4 63788fddef4b -->
### Quan hệ

Bảng này không có quan hệ nào.

<!-- src-section: 43122b8e6d 1e5ee462e224 -->
## users

**Tóm tắt.** Bảng lưu tài khoản đăng nhập web app. Tính năng `auth` sở hữu bảng này.

**Cách hoạt động**
- Ở giai đoạn 0, tài khoản được tạo bằng CLI.
- Các cột cho Messenger, web push và khoá tài khoản sẽ do tính năng của giai đoạn sau thêm vào.

Bảng dưới liệt kê các cột. Tên đăng nhập được lưu ở dạng đã chuẩn hoá, còn mật khẩu chỉ được lưu dưới dạng chuỗi băm.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| username | text | không | | unique; check `username ~ '^[a-z0-9._-]{3,32}$'` | đã chuẩn hoá chữ thường (R-AUT-07) |
| password_hash | text | không | | | chuỗi PHC argon2id (R-AUT-08) |
| role | text | không | | check `role in ('manager', 'technician')` | `manager` là Quản lý, `technician` là Thợ |
| display_name | text | không | | check `char_length(display_name) between 1 and 50` | đã bỏ khoảng trắng hai đầu |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |
| updated_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |

<!-- src-section: 02246412ee 4bc12daea685 -->
### Index

**Tóm tắt.** Bảng có một index unique trên tên đăng nhập, nên không có hai tài khoản trùng tên.

**Chi tiết kỹ thuật**
- `users_username_key`: cột `username`, unique.

<!-- src-section: 84e1817357 e4c67c55d8fa -->
### Quan hệ

- Bảng này không có khoá ngoại trỏ ra bảng khác.
- Cột `user_sessions.user_id` trỏ tới bảng này.

<!-- src-section: 1718d4b8f6 2de71a25bc34 -->
## user_sessions

**Tóm tắt.** Bảng lưu phiên đăng nhập web (ADR 0015). Tính năng `auth` sở hữu bảng này.

**Cách hoạt động**
- Phiên bị xoá cứng khi người dùng đăng xuất, đổi hoặc đặt lại mật khẩu, hoặc khi phiên hết hạn.
- Xoá cứng được vì không bảng nào tham chiếu tới bảng này.

Bảng dưới liệt kê các cột. DB chỉ lưu chuỗi băm của token, không lưu token gốc.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| user_id | uuid | không | | FK tới `users.id` | |
| token_hash | text | không | | unique | SHA-256 hex của token trong cookie `mio_session`; không lưu token gốc (R-AUT-09) |
| expires_at | timestamptz | không | | | lần gia hạn gần nhất cộng 90 ngày (R-AUT-10) |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |
| updated_at | timestamptz | không | now() | | thời điểm gia hạn gần nhất; app đặt bằng `CLOCK.now()` |

<!-- src-section: 9678ddc600 4b2f3d8b8e44 -->
### Index

**Tóm tắt.** Bảng có ba index. Index thứ nhất giữ chuỗi băm token là duy nhất. Index thứ hai tìm phiên theo người dùng. Index thứ ba dùng để dọn phiên hết hạn (R-AUT-13).

**Chi tiết kỹ thuật**
- `user_sessions_token_hash_key`: cột `token_hash`, unique.
- `user_sessions_user_id_idx`: cột `user_id`.
- `user_sessions_expires_at_idx`: cột `expires_at`.

<!-- src-section: 71bcb4eb1e b4dce39f441c -->
### Quan hệ

**Tóm tắt.** Mỗi phiên thuộc về một người dùng. Khi người dùng bị xoá, các phiên của người đó cũng bị xoá theo.

**Chi tiết kỹ thuật**
- `user_id` tham chiếu `users.id`, on delete cascade.

<!-- src-section: b80093d38c e87c1e1b82de -->
## login_throttles

**Tóm tắt.** Bảng đếm số lần đăng nhập sai theo tên đăng nhập, kể cả tên không tồn tại (R-AUT-06). Tính năng `auth` sở hữu bảng này.

**Vì sao.** Bảng không có khoá ngoại tới `users` vì phải đếm cả những tên không có thật.

Bảng dưới liệt kê các cột. Mỗi dòng giữ số lần sai trong cửa sổ hiện tại và thời điểm hết khoá, nếu có.

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| username | text | không | | unique; check `char_length(username) between 1 and 32` | tên đã chuẩn hoá như người dùng nhập |
| failed_count | integer | không | 0 | check `failed_count between 0 and 4` | số lần sai trong cửa sổ hiện tại; về 0 khi bắt đầu khoá |
| window_started_at | timestamptz | không | | | lần sai đầu của cửa sổ 15 phút |
| locked_until | timestamptz | có | | | đang khoá khi giá trị khác null và lớn hơn thời điểm hiện tại |
| created_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()` |
| updated_at | timestamptz | không | now() | | app đặt bằng `CLOCK.now()`; dùng để dọn dòng cũ hơn 24 giờ (R-AUT-13) |

<!-- src-section: 433bb943e3 3588ebb2b5de -->
### Index

**Tóm tắt.** Bảng có một index unique trên tên đăng nhập, nên mỗi tên chỉ có một bộ đếm.

**Chi tiết kỹ thuật**
- `login_throttles_username_key`: cột `username`, unique.

<!-- src-section: 4fe558dec2 63788fddef4b -->
### Quan hệ

Bảng này không có quan hệ nào.

<!-- src-section: 80b54c0db6 69afad4768ca -->
## Lịch sử thay đổi

Các thay đổi của file này theo thứ tự thời gian.

- 2026-10-29, tính năng app-skeleton: tạo file và thêm bảng `app_settings`.
- 2026-10-31, tính năng app-skeleton: sửa mục Quy ước chung để `created_at`, `updated_at` lấy từ `CLOCK` (review RV-11).
- 2026-10-31, tính năng auth: thêm bảng `users`, `user_sessions`, `login_throttles`.
