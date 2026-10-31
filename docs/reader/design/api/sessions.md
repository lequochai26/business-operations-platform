> Bản đọc sinh từ docs/design/api/sessions.md (phiên bản 276b7c5, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# API – sessions

**Tóm tắt.** File này mô tả các endpoint đăng nhập, xem phiên hiện tại và đăng xuất. Đây là nguồn chính của API. File `docs/design/api/openapi.yaml` được sinh từ các file này và không sửa tay.

**Quy ước chung**
- Endpoint cần phiên đăng nhập, trừ endpoint được ghi rõ là công khai ở mục Quyền. Request thiếu phiên nhận lỗi 401 `UNAUTHENTICATED`.
- Phiên đăng nhập được giữ bằng cookie ([ADR 0015](../../decisions/0015-server-side-sessions.md "Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…") *(Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…)*).
- Lỗi trả về theo định dạng chung. Mã lỗi dùng chung được liệt kê ở `system.md`.
- Mọi response trong file này đều không được cache ([R-AUT-18](../../phases/phase-0/design/auth.md#s-0f1edd606c "Header bảo mật trên mọi response của api") *(Header bảo mật trên mọi response của api)*).
- Cookie phiên có các thuộc tính theo [R-AUT-09](../../phases/phase-0/design/auth.md#s-0f1edd606c "Phiên và cookie") *(Phiên và cookie)*. Khi xoá cookie, server gửi lại cookie với cùng thuộc tính nhưng giá trị rỗng.

**Chi tiết kỹ thuật**
- Base path: `/api/v1`.
- Tên cookie phiên: `mio_session`.
- Thân lỗi: `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`.
- Header cache: `Cache-Control: no-store`.
- Đặt cookie: `mio_session=<token>; HttpOnly; SameSite=Lax; Path=/; Max-Age=<giây tới hết hạn>`. Thêm `Secure` khi `PUBLIC_URL` là `https://`.
- Xoá cookie: cùng thuộc tính, giá trị rỗng, `Max-Age=0`.
- Người dùng của phiên (`SessionUser`): `{ "id": "<uuid>", "username": "<tên đăng nhập>", "displayName": "<tên hiển thị>", "role": "manager" | "technician" }`.

<a id="s-61190625e2"></a>

### POST /api/v1/sessions

**Tóm tắt.** Đăng nhập bằng tên đăng nhập và mật khẩu. Endpoint tạo phiên mới và đặt cookie phiên. Endpoint công khai, ai cũng gọi được ([R-AUT-16](../../phases/phase-0/design/auth.md#s-0f1edd606c "Quyền của các route trong tính năng này") *(Quyền của các route trong tính năng này)*).

**Request**
- Thân request có 2 trường bắt buộc, đều kiểu string.
  - `username`: được chuẩn hoá bằng cách bỏ khoảng trắng hai đầu và đổi sang chữ thường. Tên sau khi chuẩn hoá dài từ 1 đến 32 ký tự ([R-AUT-01](../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)*, [R-AUT-02](../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)*, [R-AUT-07](../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập được chuẩn hóa trước khi tra cứu") *(Tên đăng nhập được chuẩn hóa trước khi tra cứu)*).
  - `password`: dài từ 1 đến 128 ký tự. Khoảng trắng được giữ nguyên, không bị bỏ ([R-AUT-03](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)*, [R-AUT-04](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)*).

**Response**
- `201`: thân là `{ "user": SessionUser }`. Header `Set-Cookie` đặt cookie phiên ([R-AUT-08](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đăng nhập đúng") *(Đăng nhập đúng)*, [R-AUT-09](../../phases/phase-0/design/auth.md#s-0f1edd606c "Phiên và cookie") *(Phiên và cookie)*).
- Nếu request đang mang cookie của một phiên còn hiệu lực, phiên đó bị xoá ([R-AUT-08](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đăng nhập đúng") *(Đăng nhập đúng)*).

**Lỗi**
- `400` `VALIDATION_ERROR`: dữ liệu sai theo [R-AUT-01](../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)*, [R-AUT-02](../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)*, [R-AUT-03](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)*, [R-AUT-04](../../phases/phase-0/design/auth.md#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)*. Trường `message` là "Dữ liệu đăng nhập không hợp lệ". Lỗi của từng trường nằm ở `fields.username` và `fields.password`.
- `400` `INVALID_JSON`: thân request không phải JSON ([R-SKL-15](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*).
- `401` `INVALID_CREDENTIALS`: tên đăng nhập không tồn tại hoặc mật khẩu sai. Thông báo là "Tên đăng nhập hoặc mật khẩu không đúng" ([R-AUT-05](../../phases/phase-0/design/auth.md#s-0f1edd606c "Tên đăng nhập không tồn tại hoặc mật khẩu sai") *(Tên đăng nhập không tồn tại hoặc mật khẩu sai)*).
- `403` `INVALID_ORIGIN`: theo [R-AUT-17](../../phases/phase-0/design/auth.md#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*.
- `413` `PAYLOAD_TOO_LARGE`: theo [R-SKL-15](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*.
- `429` `LOGIN_LOCKED`: tên đăng nhập đang bị khoá, hoặc lần sai này làm tên bị khoá ([R-AUT-06](../../phases/phase-0/design/auth.md#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*). Thông báo là "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." Header `Retry-After` cho biết thời gian chờ, tính bằng giây.
- `500` `INTERNAL_ERROR`: theo [R-SKL-16](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*.

<a id="s-2bc46bde8d"></a>

### GET /api/v1/sessions/current

**Tóm tắt.** Lấy người dùng của phiên hiện tại. Web gọi endpoint này khi mở app để biết người dùng đã đăng nhập chưa và có vai trò gì. Quản lý và Thợ đều gọi được ([R-AUT-16](../../phases/phase-0/design/auth.md#s-0f1edd606c "Quyền của các route trong tính năng này") *(Quyền của các route trong tính năng này)*).

**Request**
- Không có tham số.

**Response**
- `200`: thân là `{ "user": SessionUser }`. Khi phiên được gia hạn, response có thể kèm header `Set-Cookie` ([R-AUT-10](../../phases/phase-0/design/auth.md#s-0f1edd606c "Hết hạn trượt") *(Hết hạn trượt)*).

**Lỗi**
- `401` `UNAUTHENTICATED`: không có phiên, phiên không hợp lệ hoặc đã hết hạn. Nếu cookie không hợp lệ, response kèm lệnh xoá cookie ([R-AUT-11](../../phases/phase-0/design/auth.md#s-0f1edd606c "Request tới route không công khai mà không có cookie") *(Request tới route không công khai mà không có cookie)*).
- `500` `INTERNAL_ERROR`: theo [R-SKL-16](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*.

<a id="s-e2d91bebc9"></a>

### DELETE /api/v1/sessions/current

**Tóm tắt.** Đăng xuất: xoá phiên hiện tại và xoá cookie. Endpoint công khai, ai cũng gọi được ([R-AUT-12](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đăng xuất là route công khai và idempotent") *(Đăng xuất là route công khai và idempotent)*, [R-AUT-16](../../phases/phase-0/design/auth.md#s-0f1edd606c "Quyền của các route trong tính năng này") *(Quyền của các route trong tính năng này)*). Endpoint có tính idempotent.

**Request**
- Không có tham số.

**Response**
- `204`: không có thân. Header `Set-Cookie` xoá cookie.
- Endpoint vẫn trả `204` khi không có phiên hoặc phiên đã hết hạn ([R-AUT-12](../../phases/phase-0/design/auth.md#s-0f1edd606c "Đăng xuất là route công khai và idempotent") *(Đăng xuất là route công khai và idempotent)*).

**Lỗi**
- `403` `INVALID_ORIGIN`: theo [R-AUT-17](../../phases/phase-0/design/auth.md#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*.
- `500` `INTERNAL_ERROR`: theo [R-SKL-16](../../phases/phase-0/design/app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

Các thay đổi của file này theo thứ tự thời gian.

- 2026-10-31, tính năng auth: tạo file và thêm `POST /api/v1/sessions`, `GET /api/v1/sessions/current`, `DELETE /api/v1/sessions/current`.
- 2026-10-31, tính năng auth: theo góp ý khi duyệt UI, đổi thông báo `LOGIN_LOCKED` thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút."
- 2026-10-31, tính năng auth: ở `POST /sessions`, độ dài `username` được đo sau khi chuẩn hoá. Đăng nhập sẽ thay phiên đang có của cookie (review RV-08, RV-15).
