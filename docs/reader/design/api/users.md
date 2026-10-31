> Bản đọc sinh từ docs/design/api/users.md (phiên bản ddaf239, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# API – users

**Tóm tắt.** File này mô tả endpoint để người dùng thao tác trên tài khoản của chính mình. Đây là nguồn chính của API. File `docs/design/api/openapi.yaml` được sinh từ các file này và không sửa tay.

**Quy ước chung**
- Endpoint cần phiên đăng nhập, giữ bằng cookie ([ADR 0015](../../decisions/0015-server-side-sessions.md "Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…") *(Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…)*). Request thiếu phiên nhận lỗi 401 `UNAUTHENTICATED`.
- Lỗi trả về theo định dạng chung. Mã lỗi dùng chung được liệt kê ở `system.md`.
- Mọi response dưới `/api/v1/users/me/` đều không được cache ([R-AUT-18](../../phases/phase-0/design/auth.md#s-0f1edd606c "Header bảo mật trên mọi response của api") *(Header bảo mật trên mọi response của api)*).
- Giai đoạn 0 chỉ có thao tác của người dùng trên tài khoản của chính mình (`me`).
- Việc quản lý tài khoản thợ được thêm ở giai đoạn 2.

**Chi tiết kỹ thuật**
- Base path: `/api/v1`.
- Tên cookie phiên: `mio_session`.
- Thân lỗi: `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`.
- Header cache: `Cache-Control: no-store`.

<a id="s-4d82423ace"></a>

### POST /api/v1/users/me/change-password

**Tóm tắt.** Người dùng đang đăng nhập đổi mật khẩu của chính mình. Quản lý và Thợ đều gọi được ([R-AUT-16](../../phases/phase-0/design/auth.md#s-0f1edd606c "Quyền của các route trong tính năng này") *(Quyền của các route trong tính năng này)*).

**Cách hoạt động**
- Thiết bị hiện tại nhận một phiên mới.
- Người dùng chọn có đăng xuất các thiết bị khác hay không. Nếu chọn có, phiên của các thiết bị khác bị xoá. Nếu chọn không, các phiên đó được giữ nguyên.

**Request**
- `currentPassword`: string, bắt buộc, dài từ 1 đến 128 ký tự ([R-AUT-19](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu hiện tại trống") *(Mật khẩu hiện tại trống)*, [R-AUT-20](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*).
- `newPassword`: string, bắt buộc, dài từ 8 đến 128 ký tự. Mật khẩu mới không được trùng tên đăng nhập và phải khác mật khẩu hiện tại ([R-AUT-21](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)*).
- `signOutOtherDevices`: boolean, bắt buộc ([R-AUT-23](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*, [R-AUT-34](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đổi mật khẩu trên web luôn qua hộp thoại xác nhận 'có đăng…") *(Đổi mật khẩu trên web luôn qua hộp thoại xác nhận "có đăng…)*).
  - Giá trị `true`: đăng xuất mọi thiết bị khác.
  - Giá trị `false`: giữ nguyên các thiết bị khác.

**Response**
- `204`: không có thân. Header `Set-Cookie` đặt cookie phiên mới ([R-AUT-23](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*).

**Lỗi**
- `400` `VALIDATION_ERROR`: trường `message` là "Dữ liệu đổi mật khẩu không hợp lệ". Lỗi của từng trường như sau.
  - `fields.currentPassword`: theo [R-AUT-19](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu hiện tại trống") *(Mật khẩu hiện tại trống)*, [R-AUT-20](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*, trong đó có thông báo "Mật khẩu hiện tại không đúng".
  - `fields.newPassword`: theo [R-AUT-21](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)*.
  - `fields.signOutOtherDevices`: thông báo "Chọn có đăng xuất các thiết bị khác hay không" ([R-AUT-23](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*).
- `400` `INVALID_JSON`: theo [R-SKL-15](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*.
- `401` `UNAUTHENTICATED`: theo [R-AUT-11](../../phases/phase-0/design/auth.md#s-0f1edd606c "Request tới route không công khai mà không có cookie") *(Request tới route không công khai mà không có cookie)*.
- `403` `INVALID_ORIGIN`: theo [R-AUT-17](../../phases/phase-0/design/auth.md#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*.
- `413` `PAYLOAD_TOO_LARGE`: theo [R-SKL-15](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*.
- `429` `LOGIN_LOCKED`: tên đăng nhập của người dùng đang bị khoá, hoặc lần nhập sai mật khẩu hiện tại này làm tên bị khoá ([R-AUT-06](../../phases/phase-0/design/auth.md#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*, [R-AUT-20](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*). Thông báo là "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." Header `Retry-After` cho biết thời gian chờ, tính bằng giây.
- `500` `INTERNAL_ERROR`: theo [R-SKL-16](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

Các thay đổi của file này theo thứ tự thời gian.

- 2026-10-31, tính năng auth: tạo file và thêm `POST /api/v1/users/me/change-password`.
- 2026-10-31, tính năng auth: endpoint `change-password` thêm trường bắt buộc `signOutOtherDevices` ([R-AUT-34](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đổi mật khẩu trên web luôn qua hộp thoại xác nhận 'có đăng…") *(Đổi mật khẩu trên web luôn qua hộp thoại xác nhận "có đăng…)*).
- 2026-10-31, tính năng auth: theo góp ý khi duyệt UI, đổi thông báo `LOGIN_LOCKED` thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."
