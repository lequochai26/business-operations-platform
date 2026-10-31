# API – users

Nguồn chính của API. `docs/design/api/openapi.yaml` được sinh từ các file này, không sửa tay.

- Base path: `/api/v1`
- Xác thực: phiên đăng nhập, cookie `mio_session` (ADR 0015). Thiếu phiên → 401 `UNAUTHENTICATED`.
- Lỗi chung: thân `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`; mã lỗi dùng chung ở `system.md`.
- Mọi response dưới `/api/v1/users/me/` có `Cache-Control: no-store` (R-AUT-18).
- Giai đoạn 0 chỉ có thao tác của người dùng trên tài khoản của chính mình (`me`). Quản lý tài khoản thợ thêm ở giai đoạn 2.

### POST /api/v1/users/me/change-password

Người dùng đang đăng nhập đổi mật khẩu của chính mình. Thiết bị hiện tại nhận phiên mới; phiên của các thiết bị khác bị xóa nếu `signOutOtherDevices` là `true`, giữ nguyên nếu `false`.

- Quyền: Quản lý, Thợ (R-AUT-16)
- Request:
  - Body: `currentPassword`: string, bắt buộc, dài 1–128 ký tự (R-AUT-19, R-AUT-20)
  - Body: `newPassword`: string, bắt buộc, dài 8–128 ký tự, không trùng tên đăng nhập, khác mật khẩu hiện tại (R-AUT-21)
  - Body: `signOutOtherDevices`: boolean, bắt buộc; `true` đăng xuất mọi thiết bị khác, `false` giữ nguyên (R-AUT-23, R-AUT-34)
- Response:
  - `204`: không có thân, header `Set-Cookie` đặt cookie phiên mới (R-AUT-23)
- Mã lỗi:
  - `400` `VALIDATION_ERROR`: `message` "Dữ liệu đổi mật khẩu không hợp lệ"; `fields.currentPassword` theo R-AUT-19, R-AUT-20 ("Mật khẩu hiện tại không đúng"); `fields.newPassword` theo R-AUT-21; `fields.signOutOtherDevices` "Chọn có đăng xuất các thiết bị khác hay không" (R-AUT-23)
  - `400` `INVALID_JSON`: R-SKL-15
  - `401` `UNAUTHENTICATED`: R-AUT-11
  - `403` `INVALID_ORIGIN`: R-AUT-17
  - `413` `PAYLOAD_TOO_LARGE`: R-SKL-15
  - `429` `LOGIN_LOCKED`: tên đăng nhập của người dùng đang bị khóa hoặc lần nhập sai mật khẩu hiện tại này làm khóa, "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút.", header `Retry-After` (giây) (R-AUT-06, R-AUT-20)
  - `500` `INTERNAL_ERROR`: R-SKL-16

## Lịch sử thay đổi

- 2026-10-31 | auth | tạo file; thêm `POST /api/v1/users/me/change-password`
- 2026-10-31 | auth | `change-password` thêm trường bắt buộc `signOutOtherDevices` (R-AUT-34)
- 2026-10-31 | auth | đổi thông báo `LOGIN_LOCKED` thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (góp ý duyệt UI)
