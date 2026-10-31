# API – system

Nguồn chính của API. `docs/design/api/openapi.yaml` được sinh từ các file này, không sửa tay.

- Base path: `/api/v1`
- Xác thực: phiên đăng nhập, cookie `mio_session` (ADR 0015, thiết kế `auth`). Thiếu phiên → 401 `UNAUTHENTICATED`. Riêng endpoint trong file này không cần đăng nhập.
- Lỗi chung: thân `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`; `fields` chỉ có khi lỗi gắn với trường cụ thể (R-SKL-15).
- Header trên mọi response: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin` (R-AUT-18).
- Mã lỗi dùng cho mọi endpoint:
  - `400` `INVALID_JSON`: thân request không phải JSON hợp lệ, thông báo "Dữ liệu gửi lên không đúng định dạng JSON" (R-SKL-15).
  - `400` `VALIDATION_ERROR`: dữ liệu sai quy tắc, có `fields`; khóa của `fields` là đường dẫn trường (`goldenHours[1].end`), lỗi ở gốc dùng `_root` (R-SKL-11, R-SKL-15).
  - `401` `UNAUTHENTICATED`: route cần đăng nhập mà không có phiên, phiên không hợp lệ hoặc đã hết hạn, thông báo "Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn"; cookie không hợp lệ thì response kèm xóa cookie (R-AUT-11).
  - `403` `FORBIDDEN`: đã đăng nhập nhưng vai trò không được dùng route, thông báo "Bạn không có quyền thực hiện thao tác này" (R-AUT-15).
  - `403` `INVALID_ORIGIN`: request `POST`, `PUT`, `PATCH`, `DELETE` có header `Origin` khác origin của `PUBLIC_URL`, thông báo "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ <PUBLIC_URL>"; áp dụng cả route công khai (R-AUT-17).
  - `404` `NOT_FOUND`: đường dẫn `/api/...` không có route, thông báo "Không tìm thấy địa chỉ yêu cầu" (R-SKL-15).
  - `409` `INVALID_STORED_SETTING`: chỉ ở endpoint `/api/v1/settings/<khóa>`; giá trị cài đặt đang lưu không qua schema hiện tại, `message` và `fields` theo R-SKL-12.
  - `413` `PAYLOAD_TOO_LARGE`: thân request lớn hơn 1 MB, thông báo "Dữ liệu gửi lên quá lớn" (R-SKL-15).
  - `500` `INTERNAL_ERROR`: lỗi không lường trước, thông báo "Lỗi hệ thống, vui lòng thử lại sau", không có stack trace (R-SKL-16).

### GET /api/v1/health

Kiểm tra API còn chạy và kết nối được DB, Redis. Dùng cho healthcheck của Docker và theo dõi vận hành.

- Quyền: công khai (không cần đăng nhập)
- Request:
  - Không có tham số.
- Response:
  - `200`: `{ "status": "ok", "checks": { "database": "up", "redis": "up" } }`
  - `503`: `{ "status": "error", "checks": { "database": "up" | "down", "redis": "up" | "down" } }`, ít nhất một trường là `down` (R-SKL-13)
- Mã lỗi:
  - `503` (thân như trên, không theo định dạng lỗi chung): DB hoặc Redis không trả lời trong 2 giây (R-SKL-13)
  - `500` `INTERNAL_ERROR`: lỗi không lường trước (R-SKL-16)

## Lịch sử thay đổi

- 2026-10-29 | app-skeleton | tạo file; thêm `GET /api/v1/health` và mã lỗi chung `NOT_FOUND`, `INTERNAL_ERROR`
- 2026-10-31 | app-skeleton | thêm mã lỗi chung `INVALID_JSON`, `VALIDATION_ERROR`, `INVALID_STORED_SETTING`, `PAYLOAD_TOO_LARGE` (review RV-08)
- 2026-10-31 | auth | xác thực bằng cookie `mio_session`; thêm mã lỗi chung `UNAUTHENTICATED`, `FORBIDDEN`, `INVALID_ORIGIN`; header bảo mật chung
