# API – sessions

Nguồn chính của API. `docs/design/api/openapi.yaml` được sinh từ các file này, không sửa tay.

- Base path: `/api/v1`
- Xác thực: phiên đăng nhập, cookie `mio_session` (ADR 0015). Thiếu phiên → 401 `UNAUTHENTICATED`. Endpoint công khai được ghi rõ ở mục Quyền.
- Lỗi chung: thân `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`; mã lỗi dùng chung ở `system.md`.
- Mọi response trong file này có `Cache-Control: no-store` (R-AUT-18).
- Cookie phiên `mio_session=<token>; HttpOnly; SameSite=Lax; Path=/; Max-Age=<giây tới hết hạn>`, thêm `Secure` khi `PUBLIC_URL` là `https://` (R-AUT-09). Xóa cookie: cùng thuộc tính, giá trị rỗng, `Max-Age=0`.
- Người dùng của phiên (`SessionUser`): `{ "id": "<uuid>", "username": "<tên đăng nhập>", "displayName": "<tên hiển thị>", "role": "manager" | "technician" }`.

### POST /api/v1/sessions

Đăng nhập bằng tên đăng nhập và mật khẩu, tạo phiên mới và đặt cookie.

- Quyền: công khai (R-AUT-16)
- Request:
  - Body: `username`: string, bắt buộc; được chuẩn hóa (bỏ khoảng trắng hai đầu, đổi chữ thường), tên đã chuẩn hóa dài 1–32 ký tự (R-AUT-01, R-AUT-02, R-AUT-07)
  - Body: `password`: string, bắt buộc, dài 1–128 ký tự, không bỏ khoảng trắng (R-AUT-03, R-AUT-04)
- Response:
  - `201`: `{ "user": SessionUser }`, header `Set-Cookie` đặt cookie phiên (R-AUT-08, R-AUT-09); request mang cookie của một phiên còn hiệu lực thì phiên đó bị xóa (R-AUT-08)
- Mã lỗi:
  - `400` `VALIDATION_ERROR`: `message` "Dữ liệu đăng nhập không hợp lệ", `fields.username` / `fields.password` theo R-AUT-01 … R-AUT-04
  - `400` `INVALID_JSON`: thân không phải JSON (R-SKL-15)
  - `401` `INVALID_CREDENTIALS`: tên đăng nhập không tồn tại hoặc mật khẩu sai, "Tên đăng nhập hoặc mật khẩu không đúng" (R-AUT-05)
  - `403` `INVALID_ORIGIN`: R-AUT-17
  - `413` `PAYLOAD_TOO_LARGE`: R-SKL-15
  - `429` `LOGIN_LOCKED`: tên đăng nhập đang bị khóa hoặc lần sai này làm khóa, "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút.", header `Retry-After` (giây) (R-AUT-06)
  - `500` `INTERNAL_ERROR`: R-SKL-16

### GET /api/v1/sessions/current

Lấy người dùng của phiên hiện tại. Web gọi khi mở app để biết đã đăng nhập chưa và vai trò là gì.

- Quyền: Quản lý, Thợ (R-AUT-16)
- Request:
  - Không có tham số.
- Response:
  - `200`: `{ "user": SessionUser }`; có thể kèm `Set-Cookie` khi phiên được gia hạn (R-AUT-10)
- Mã lỗi:
  - `401` `UNAUTHENTICATED`: không có phiên, phiên không hợp lệ hoặc đã hết hạn; kèm xóa cookie nếu cookie không hợp lệ (R-AUT-11)
  - `500` `INTERNAL_ERROR`: R-SKL-16

### DELETE /api/v1/sessions/current

Đăng xuất: xóa phiên hiện tại và xóa cookie. Idempotent.

- Quyền: công khai (R-AUT-12, R-AUT-16)
- Request:
  - Không có tham số.
- Response:
  - `204`: không có thân, header `Set-Cookie` xóa cookie; trả cả khi không có phiên hoặc phiên đã hết hạn (R-AUT-12)
- Mã lỗi:
  - `403` `INVALID_ORIGIN`: R-AUT-17
  - `500` `INTERNAL_ERROR`: R-SKL-16

## Lịch sử thay đổi

- 2026-10-31 | auth | tạo file; thêm `POST /api/v1/sessions`, `GET /api/v1/sessions/current`, `DELETE /api/v1/sessions/current`
- 2026-10-31 | auth | đổi thông báo `LOGIN_LOCKED` thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (góp ý duyệt UI)
- 2026-10-31 | auth | `POST /sessions`: độ dài `username` đo sau khi chuẩn hóa; đăng nhập thay phiên đang có của cookie (review RV-08, RV-15)
