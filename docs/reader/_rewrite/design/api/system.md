<!-- src-section: 0b0fa0b228 584a2a5d4b56 -->
# API – system

**Tóm tắt.** File này mô tả endpoint kiểm tra tình trạng hệ thống và các quy ước dùng cho mọi endpoint: xác thực, định dạng lỗi, header bảo mật và mã lỗi chung. Đây là nguồn chính của API. File `docs/design/api/openapi.yaml` được sinh từ các file này và không sửa tay.

**Quy ước chung**
- Endpoint cần phiên đăng nhập, giữ bằng cookie (ADR 0015, thiết kế `auth`). Request thiếu phiên nhận lỗi 401 `UNAUTHENTICATED`.
- Riêng endpoint trong file này không cần đăng nhập.
- Lỗi trả về theo một định dạng chung. Trường `fields` chỉ có khi lỗi gắn với một trường cụ thể (R-SKL-15).
- Mọi response đều có các header bảo mật (R-AUT-18).

**Mã lỗi dùng cho mọi endpoint**
- `400` `INVALID_JSON`: thân request không phải JSON hợp lệ. Thông báo là "Dữ liệu gửi lên không đúng định dạng JSON" (R-SKL-15).
- `400` `VALIDATION_ERROR`: dữ liệu sai quy tắc, response có `fields`. Khoá của `fields` là đường dẫn tới trường, ví dụ `goldenHours[1].end`. Lỗi ở gốc dùng khoá `_root` (R-SKL-11, R-SKL-15).
- `401` `UNAUTHENTICATED`: route cần đăng nhập nhưng không có phiên, phiên không hợp lệ hoặc đã hết hạn. Thông báo là "Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn". Nếu cookie không hợp lệ, response kèm lệnh xoá cookie (R-AUT-11).
- `403` `FORBIDDEN`: người dùng đã đăng nhập nhưng vai trò không được dùng route này. Thông báo là "Bạn không có quyền thực hiện thao tác này" (R-AUT-15).
- `403` `INVALID_ORIGIN`: request `POST`, `PUT`, `PATCH`, `DELETE` có header `Origin` khác origin của `PUBLIC_URL`. Thông báo là "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ <PUBLIC_URL>". Quy tắc này áp dụng cả với route công khai (R-AUT-17).
- `404` `NOT_FOUND`: đường dẫn `/api/...` không có route. Thông báo là "Không tìm thấy địa chỉ yêu cầu" (R-SKL-15).
- `409` `INVALID_STORED_SETTING`: chỉ dùng ở endpoint `/api/v1/settings/<khóa>`. Lỗi xảy ra khi giá trị cài đặt đang lưu không qua được schema hiện tại. Trường `message` và `fields` theo R-SKL-12.
- `413` `PAYLOAD_TOO_LARGE`: thân request lớn hơn 1 MB. Thông báo là "Dữ liệu gửi lên quá lớn" (R-SKL-15).
- `500` `INTERNAL_ERROR`: lỗi không lường trước. Thông báo là "Lỗi hệ thống, vui lòng thử lại sau". Response không chứa stack trace (R-SKL-16).

**Chi tiết kỹ thuật**
- Base path: `/api/v1`.
- Tên cookie phiên: `mio_session`.
- Thân lỗi: `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`.
- Header trên mọi response: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`.

<!-- src-section: 41ba6e25dc 072f52897b16 -->
### GET /api/v1/health

**Tóm tắt.** Kiểm tra API còn chạy và kết nối được DB, Redis. Healthcheck của Docker và việc theo dõi vận hành dùng endpoint này. Endpoint công khai, không cần đăng nhập.

**Request**
- Không có tham số.

**Response**
- `200`: cả DB và Redis đều hoạt động. Thân là `{ "status": "ok", "checks": { "database": "up", "redis": "up" } }`.
- `503`: ít nhất một trong hai trường là `down` (R-SKL-13). Thân là `{ "status": "error", "checks": { "database": "up" | "down", "redis": "up" | "down" } }`.

**Lỗi**
- `503`: DB hoặc Redis không trả lời trong 2 giây (R-SKL-13). Thân như trên, không theo định dạng lỗi chung.
- `500` `INTERNAL_ERROR`: lỗi không lường trước (R-SKL-16).

<!-- src-section: 80b54c0db6 8269f75cc622 -->
## Lịch sử thay đổi

Các thay đổi của file này theo thứ tự thời gian.

- 2026-10-29, tính năng app-skeleton: tạo file, thêm `GET /api/v1/health` và mã lỗi chung `NOT_FOUND`, `INTERNAL_ERROR`.
- 2026-10-31, tính năng app-skeleton: thêm mã lỗi chung `INVALID_JSON`, `VALIDATION_ERROR`, `INVALID_STORED_SETTING`, `PAYLOAD_TOO_LARGE` (review RV-08).
- 2026-10-31, tính năng auth: xác thực bằng cookie `mio_session`. Thêm mã lỗi chung `UNAUTHENTICATED`, `FORBIDDEN`, `INVALID_ORIGIN` và các header bảo mật chung.
